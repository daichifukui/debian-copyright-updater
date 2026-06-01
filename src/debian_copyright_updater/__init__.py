"""Tools for analyzing and updating Debian DEP-5 copyright files."""

from .analyzer import CoverageAnalysis, FileCoverage, analyze_coverage
from .dep5 import Dep5Document, FilesStanza, parse_dep5

__all__ = [
    "CoverageAnalysis",
    "Dep5Document",
    "FileCoverage",
    "FilesStanza",
    "analyze_coverage",
    "parse_dep5",
]
