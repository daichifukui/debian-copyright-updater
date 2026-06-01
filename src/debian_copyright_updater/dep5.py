"""Minimal DEP-5 parser focused on Files stanza discovery.

The parser keeps enough structure for coverage analysis while preserving line
numbers for reports and future rewrite work.  It understands Debian control-file
continuation lines, including multiline ``Files`` fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Paragraph:
    """A Debian control paragraph parsed from ``debian/copyright``."""

    fields: dict[str, str]
    start_line: int
    end_line: int


@dataclass(frozen=True)
class FilesStanza:
    """A DEP-5 paragraph containing a ``Files`` field."""

    patterns: tuple[str, ...]
    paragraph: Paragraph
    index: int


@dataclass(frozen=True)
class Dep5Document:
    """Parsed representation of the DEP-5 file."""

    paragraphs: tuple[Paragraph, ...]
    files_stanzas: tuple[FilesStanza, ...]


def parse_dep5_file(path: str | Path) -> Dep5Document:
    """Parse a DEP-5 file from disk."""

    return parse_dep5(Path(path).read_text(encoding="utf-8"))


def parse_dep5(text: str) -> Dep5Document:
    """Parse DEP-5 text into paragraphs and Files stanzas.

    Field continuations are unfolded with newlines preserved as whitespace, so a
    multiline ``Files`` value can be split into individual DEP-5 patterns using
    normal whitespace splitting.
    """

    paragraphs: list[Paragraph] = []
    current: dict[str, list[str]] = {}
    current_field: str | None = None
    start_line: int | None = None
    last_line = 0

    def finish(end_line: int) -> None:
        nonlocal current, current_field, start_line
        if not current or start_line is None:
            current = {}
            current_field = None
            start_line = None
            return
        fields = {name: "\n".join(parts).strip() for name, parts in current.items()}
        paragraphs.append(Paragraph(fields=fields, start_line=start_line, end_line=end_line))
        current = {}
        current_field = None
        start_line = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        last_line = line_number
        if not raw_line.strip():
            finish(line_number - 1)
            continue

        if raw_line[0].isspace():
            if current_field is not None:
                current[current_field].append(raw_line.strip())
            continue

        if ":" not in raw_line:
            continue

        name, value = raw_line.split(":", 1)
        if start_line is None:
            start_line = line_number
        current_field = name.strip()
        current.setdefault(current_field, []).append(value.strip())

    finish(last_line)

    files_stanzas: list[FilesStanza] = []
    for paragraph in paragraphs:
        files_value = paragraph.fields.get("Files")
        if not files_value:
            continue
        patterns = tuple(files_value.split())
        if patterns:
            files_stanzas.append(
                FilesStanza(
                    patterns=patterns,
                    paragraph=paragraph,
                    index=len(files_stanzas),
                )
            )

    return Dep5Document(paragraphs=tuple(paragraphs), files_stanzas=tuple(files_stanzas))
