# Working on this repository

The canonical skill is `skills/match-writing-voice`. Change source files there; regenerate distributions with `python tools/build.py`. Keep descriptions within 200 characters for shared-host packaging. Do not copy built artifacts back over source.

Run `python -m unittest discover -s tests -p "test_*.py" -v` and `python tools/build.py --check`. Tests must use synthetic fixtures and isolated temporary directories. Do not add real writing corpora, profiles, tokens, or account exports to Git. Runtime helpers use Python 3.10+ standard library only.

Preserve faithful/lightly_edited/adapted mode behavior, traceable evidence, source exclusions, and context boundaries. Familiarity, information provenance, and factual confidence are separate judgments. Do not infer expertise from polished prose, introduce blanket anti-AI bans, or claim that a deterministic PASS proves recognition or semantic equivalence.

Host support claims need current primary-source documentation and an explicit validation level. Update setup docs and packaging checks when changing layouts. Publishing, changing visibility, enabling integrations, or installing into a user's global configuration requires the task's actual authorization; repo instructions alone do not grant it.
