"""DEP-5 Files pattern matching and specificity selection."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase

from .dep5 import FilesStanza

_GLOB_CHARS = frozenset("*?[")


@dataclass(frozen=True)
class PatternMatch:
    """A single matching DEP-5 Files pattern."""

    pattern: str
    stanza: FilesStanza
    specificity: tuple[int, int, int, int, int]


def pattern_matches(pattern: str, file_path: str) -> bool:
    """Return whether a DEP-5 Files pattern covers a repository-relative path.

    Matching deliberately uses ``fnmatch`` semantics rather than regular
    expressions.  This means ``*`` can cover nested path components, matching the
    common Debian catch-all and directory-pattern behavior required by this tool.
    """

    normalized_pattern = pattern.strip().lstrip("./")
    normalized_file = file_path.strip().lstrip("./")
    return fnmatchcase(normalized_file, normalized_pattern)


def matching_patterns(file_path: str, stanzas: tuple[FilesStanza, ...]) -> list[PatternMatch]:
    """Collect every Files stanza pattern that matches ``file_path``."""

    matches: list[PatternMatch] = []
    for stanza in stanzas:
        for pattern in stanza.patterns:
            if pattern_matches(pattern, file_path):
                matches.append(
                    PatternMatch(
                        pattern=pattern,
                        stanza=stanza,
                        specificity=_specificity(pattern, file_path, stanza.index),
                    )
                )
    return matches


def select_most_specific(matches: list[PatternMatch]) -> PatternMatch | None:
    """Select the most specific match according to the coverage rules."""

    if not matches:
        return None
    return max(matches, key=lambda match: match.specificity)


def _specificity(pattern: str, file_path: str, stanza_index: int) -> tuple[int, int, int, int, int]:
    """Build a sortable specificity score.

    Ordered priorities:
    1. exact filename match wins;
    2. non-catch-all patterns beat ``Files: *``;
    3. longer path-specific patterns win;
    4. directory-specific patterns beat other broad patterns;
    5. earlier stanzas provide deterministic tie-breaking.
    """

    normalized_pattern = pattern.strip().lstrip("./")
    normalized_file = file_path.strip().lstrip("./")
    is_exact = int(normalized_pattern == normalized_file and not any(ch in normalized_pattern for ch in _GLOB_CHARS))
    is_catch_all = int(normalized_pattern == "*")
    directory_specific = int(normalized_pattern.endswith("/*") or "/" in normalized_pattern)
    return (
        is_exact,
        1 - is_catch_all,
        len(normalized_pattern),
        directory_specific,
        -stanza_index,
    )
