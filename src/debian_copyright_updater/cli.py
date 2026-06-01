"""Command line interface for DEP-5 coverage analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_paths
from .report import to_human, to_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze DEP-5 debian/copyright file coverage")
    parser.add_argument("root", nargs="?", default=".", help="source tree root (default: current directory)")
    parser.add_argument(
        "--copyright",
        type=Path,
        help="path to debian/copyright (default: ROOT/debian/copyright)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "human"),
        default="json",
        help="report format (default: json)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    analysis = analyze_paths(Path(args.root), args.copyright)
    if args.format == "human":
        print(to_human(analysis))
    else:
        print(to_json(analysis))
    return 1 if analysis.new_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
