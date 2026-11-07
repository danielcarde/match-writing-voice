# Release process

1. Review the source, tests, docs, and `VERSION`; keep all plugin/extension version fields aligned.
2. Run the full test suite, `python tools/build.py --check`, and `python tools/build.py`.
3. Confirm CI succeeds for the commit being released. Inspect the archive root and checksums.
4. Create a private-repository release using tag `v` plus `VERSION`, and attach files from `dist/`.
5. State actual validation: tool/format checks, synthetic exercises, and any separate live-host or human tests.

The build makes native and Claude upload ZIPs, a Gemini-compatible `.skill` file, a standalone guide, and SHA-256 checksums. A `.skill` file is a ZIP archive; it is not a model or executable installer.

Repository visibility remains private unless the owner explicitly authorizes a change. No open-source license has been selected. Do not publish to a public marketplace or change licensing as part of a routine package build.
