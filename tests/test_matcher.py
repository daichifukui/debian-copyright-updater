from debian_copyright_updater.analyzer import analyze_coverage
from debian_copyright_updater.dep5 import parse_dep5


def test_exact_match_wins_over_directory_and_catch_all():
    document = parse_dep5(
        """Files: *\nCopyright: Example Corp\n\nFiles: src/*\nCopyright: Example Corp\n\nFiles: src/daemon/*\nCopyright: Example Corp\n\nFiles: src/daemon/fanotify-fs-error.c\nCopyright: Example Corp\n"""
    )

    analysis = analyze_coverage(document, ["src/daemon/fanotify-fs-error.c"])

    report = analysis.files[0]
    assert report.matched_patterns == [
        "*",
        "src/*",
        "src/daemon/*",
        "src/daemon/fanotify-fs-error.c",
    ]
    assert report.selected_pattern == "src/daemon/fanotify-fs-error.c"
    assert analysis.new_files == []


def test_longer_directory_pattern_wins_over_catch_all_and_parent():
    document = parse_dep5(
        """Files: *\nCopyright: Example Corp\n\nFiles: src/*\nCopyright: Example Corp\n\nFiles: src/daemon/*\nCopyright: Example Corp\n"""
    )

    analysis = analyze_coverage(document, ["src/daemon/state-report.c"])

    report = analysis.files[0]
    assert report.matched_patterns == ["*", "src/*", "src/daemon/*"]
    assert report.selected_pattern == "src/daemon/*"
    assert analysis.new_files == []


def test_catch_all_coverage_is_not_new_file():
    document = parse_dep5(
        """Files: *\nCopyright: Example Corp\nLicense: MIT\n"""
    )

    analysis = analyze_coverage(document, ["new/upstream/file.c"])

    assert analysis.files[0].matched_patterns == ["*"]
    assert analysis.files[0].selected_pattern == "*"
    assert analysis.new_files == []
