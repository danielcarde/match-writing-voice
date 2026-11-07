#!/usr/bin/env python3
"""Copy one canonical skill to an explicitly selected local host/scope."""
import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/match-writing-voice"
AGENTS = {"codex": ".agents", "claude-code": ".claude", "gemini-cli": ".gemini"}


def destination(agent, scope, project=None, user_home=None):
    base = Path(user_home or Path.home()) if scope == "user" else Path(project or Path.cwd())
    return base.resolve() / AGENTS[agent] / "skills" / "match-writing-voice"


def install(agent, scope, project=None, user_home=None, dry_run=False):
    target = destination(agent, scope, project, user_home)
    if target.exists() or target.is_symlink():
        raise ValueError(f"Already exists; preserve local changes before replacing: {target}")
    if dry_run:
        return {"agent": agent, "scope": scope, "target": str(target), "written": False}
    # No recursive deletion or overwriting. Source is the fixed canonical folder.
    if not SOURCE.is_dir():
        raise ValueError("Canonical skill folder is missing")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "voice-test-*"))
    return {"agent": agent, "scope": scope, "target": str(target), "written": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--scope", choices=["user", "project"], required=True)
    parser.add_argument("--project", help="Project root for project scope; defaults to current directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.agent, args.scope, args.project, dry_run=args.dry_run), indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Install stopped: {error}\n")


if __name__ == "__main__":
    main()
