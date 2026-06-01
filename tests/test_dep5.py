from debian_copyright_updater.dep5 import parse_dep5


def test_parse_multiline_files_field():
    document = parse_dep5(
        """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n\nFiles: src/daemon/*\n src/library/*\n *\nCopyright: Example Corp\nLicense: MIT\n"""
    )

    assert len(document.files_stanzas) == 1
    assert document.files_stanzas[0].patterns == ("src/daemon/*", "src/library/*", "*")
