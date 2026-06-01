import json

from debian_copyright_updater.cli import main


def test_cli_outputs_json_coverage(tmp_path, capsys):
    debian = tmp_path / "debian"
    debian.mkdir()
    (debian / "copyright").write_text("Files: *\nCopyright: Example Corp\n", encoding="utf-8")
    source = tmp_path / "src" / "daemon"
    source.mkdir(parents=True)
    (source / "fanotify-fs-error.c").write_text("/* test */\n", encoding="utf-8")

    exit_code = main([str(tmp_path)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["new_files"] == []
    assert payload["files"] == [
        {
            "file": "src/daemon/fanotify-fs-error.c",
            "matched_patterns": ["*"],
            "selected_pattern": "*",
        }
    ]
