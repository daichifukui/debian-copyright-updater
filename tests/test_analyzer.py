from debian_copyright_updater.analyzer import analyze_coverage
from debian_copyright_updater.dep5 import parse_dep5


def test_mandatory_daemon_pattern_covers_fanotify_file():
    document = parse_dep5(
        """Files: src/daemon/*\nCopyright: Example Corp\n"""
    )

    analysis = analyze_coverage(document, ["src/daemon/fanotify-fs-error.c"])

    assert analysis.new_files == []
    assert analysis.files[0].file == "src/daemon/fanotify-fs-error.c"
    assert analysis.files[0].matched_patterns == ["src/daemon/*"]
    assert analysis.files[0].selected_pattern == "src/daemon/*"


def test_mandatory_library_pattern_does_not_cover_daemon_file():
    document = parse_dep5(
        """Files: src/library/*\nCopyright: Example Corp\n"""
    )

    analysis = analyze_coverage(document, ["src/daemon/fanotify-fs-error.c"])

    assert analysis.new_files == ["src/daemon/fanotify-fs-error.c"]
    assert analysis.files[0].file == "src/daemon/fanotify-fs-error.c"
    assert analysis.files[0].matched_patterns == []
    assert analysis.files[0].selected_pattern is None


def test_multiple_patterns_in_single_files_field_are_considered():
    document = parse_dep5(
        """Files: src/library/* src/daemon/*\nCopyright: Example Corp\n"""
    )

    analysis = analyze_coverage(document, ["src/daemon/fanotify-fs-error.c"])

    assert analysis.new_files == []
    assert analysis.files[0].matched_patterns == ["src/daemon/*"]
