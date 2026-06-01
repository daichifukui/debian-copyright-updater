"""Normalization boundaries for future copyright updates."""

from __future__ import annotations


def normalize_holder(holder: str) -> str:
    """Normalize whitespace in a copyright holder name."""

    return " ".join(holder.split())


def normalize_license_id(license_id: str) -> str:
    """Normalize simple DEP-5 license identifiers without remapping them."""

    return " ".join(license_id.split())
