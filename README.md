# debian-copyright-updater

`debian-copyright-updater` is a Python 3.11+ tool for analyzing whether files in
an upstream source tree are covered by the `Files` stanzas in a Debian DEP-5
`debian/copyright` file.

The first implementation slice focuses on reliable coverage detection and JSON
reporting.  Update/rewrite functionality is intentionally separated behind module
boundaries so it can be added without weakening the coverage rules.

## Architecture

- `dep5.py` parses DEP-5 paragraphs and discovers every `Files` stanza, including
  multiple patterns and multiline `Files` fields.
- `matcher.py` applies Debian-style glob matching with `fnmatch` semantics and
  selects the most specific matching pattern.
- `analyzer.py` checks every source file against every `Files` stanza and marks a
  file as new only when no stanza covers it.
- `report.py` renders JSON and human-readable reports.
- `cli.py` provides the `debian-copyright-updater` command.
- `licensecheck.py`, `normalize.py`, and `updater.py` define future extension
  boundaries for license parsing, normalization, and DEP-5 rewrites.

## Usage

```bash
debian-copyright-updater /path/to/source --format json
```

The JSON report includes one entry per analyzed file:

```json
{
  "file": "src/daemon/fanotify-fs-error.c",
  "matched_patterns": ["*", "src/*", "src/daemon/*"],
  "selected_pattern": "src/daemon/*"
}
```

Files covered by `Files: *` are not reported as new files.
