"""Future rewrite entry points for debian/copyright updates."""

from __future__ import annotations

from .analyzer import CoverageAnalysis


def plan_update(analysis: CoverageAnalysis) -> list[str]:
    """Return source files that need new DEP-5 coverage before rewriting."""

    return list(analysis.new_files)
