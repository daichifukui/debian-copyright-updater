"""Parsing helpers for licensecheck output.

This module is intentionally small in the first implementation slice.  The
coverage analyzer does not require licensecheck, but keeping this boundary makes
future license normalization and update planning explicit.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LicenseCheckRecord:
    """One parsed licensecheck result line."""

    path: str
    license_expression: str


def parse_licensecheck_line(line: str) -> LicenseCheckRecord | None:
    """Parse the common ``path: license`` licensecheck line format."""

    if ":" not in line:
        return None
    path, license_expression = line.split(":", 1)
    path = path.strip()
    license_expression = license_expression.strip()
    if not path or not license_expression:
        return None
    return LicenseCheckRecord(path=path, license_expression=license_expression)
