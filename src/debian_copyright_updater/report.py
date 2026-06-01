"""Report rendering for coverage analysis."""

from __future__ import annotations

import json
from dataclasses import asdict

from .analyzer import CoverageAnalysis


def to_json(analysis: CoverageAnalysis, *, indent: int | None = 2) -> str:
    """Serialize coverage analysis to JSON."""

    return json.dumps(asdict(analysis), indent=indent)


def to_human(analysis: CoverageAnalysis) -> str:
    """Render a concise human-readable coverage report."""

    lines = ["DEP-5 coverage report", f"Files analyzed: {len(analysis.files)}"]
    if analysis.new_files:
        lines.append(f"New files: {len(analysis.new_files)}")
        lines.extend(f"  - {path}" for path in analysis.new_files)
    else:
        lines.append("New files: 0")
    return "\n".join(lines)
