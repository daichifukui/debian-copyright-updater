"""Coverage analysis for source files against DEP-5 Files stanzas."""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterable

from .dep5 import Dep5Document, parse_dep5_file
from .matcher import matching_patterns, select_most_specific


DEFAULT_EXCLUDES = frozenset({".git", ".hg", ".svn", "__pycache__"})


@dataclass(frozen=True)
class FileCoverage:
    """Coverage decision for one source file."""

    file: str
    matched_patterns: list[str] = field(default_factory=list)
    selected_pattern: str | None = None

    @property
    def is_new_file(self) -> bool:
        """Whether no DEP-5 Files stanza covers this file."""

        return self.selected_pattern is None


@dataclass(frozen=True)
class CoverageAnalysis:
    """Full coverage report for a source tree."""

    files: list[FileCoverage]
    new_files: list[str]


def analyze_coverage(document: Dep5Document, source_files: Iterable[str]) -> CoverageAnalysis:
    """Analyze each source file against every DEP-5 Files stanza."""

    file_reports: list[FileCoverage] = []
    for file_path in sorted(_normalize_path(path) for path in source_files):
        matches = matching_patterns(file_path, document.files_stanzas)
        selected = select_most_specific(matches)
        file_reports.append(
            FileCoverage(
                file=file_path,
                matched_patterns=[match.pattern for match in matches],
                selected_pattern=selected.pattern if selected else None,
            )
        )

    return CoverageAnalysis(
        files=file_reports,
        new_files=[report.file for report in file_reports if report.is_new_file],
    )


def analyze_paths(root: str | Path, copyright_path: str | Path | None = None) -> CoverageAnalysis:
    """Parse ``debian/copyright`` and analyze files below ``root``."""

    root_path = Path(root)
    dep5_path = Path(copyright_path) if copyright_path else root_path / "debian" / "copyright"
    document = parse_dep5_file(dep5_path)
    files = iter_source_files(root_path, dep5_path)
    return analyze_coverage(document, files)


def iter_source_files(root: Path, copyright_path: Path | None = None) -> list[str]:
    """Return repository-relative source files, excluding VCS/cache files."""

    copyright_resolved = copyright_path.resolve() if copyright_path else None
    results: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        if copyright_resolved and path.resolve() == copyright_resolved:
            continue
        results.append(path.relative_to(root).as_posix())
    return results


def _normalize_path(path: str) -> str:
    return Path(path).as_posix().lstrip("./")
