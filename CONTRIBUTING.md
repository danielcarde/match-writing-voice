# Contributing

Keep changes focused on learning and applying writing voices. Open an issue for a specific failure, explain the expected behavior, and use a synthetic or thoroughly sanitized example. Separate a voice mismatch from changed meaning and from a tool bug.

## Local checks

```sh
python -m unittest discover -s tests -p "test_*.py" -v
python tools/build.py --check
python tools/build.py
python tools/demo.py
```

No dependency installation is needed. Python 3.10+ is sufficient. CI exercises Linux, Windows, and macOS; a local run only establishes results on that local environment.

## Pull requests

Explain the user-visible problem, the final behavior, and the relevant validation. Add a behavioral regression test for changed mechanics. For instruction changes, include a concrete before/after scenario and distinguish simulated/model checks from real human preference results.

Keep the core entrypoint short. Put conditional guidance in references. Preserve supported imperfections without exaggerating them, keep scope explicit, and avoid a universal word/structure blacklist.

## Distribution

Update `VERSION` and matching plugin/extension metadata together. Build packages from source and review their contents. Release notes should describe behavior and limitations, not invented performance percentages. See [release steps](docs/releases.md).

This private repository has no open-source license selected. Do not import third-party implementations without reviewing and preserving their applicable terms. Conceptual design references belong in `NOTICE.md` and the source research.
