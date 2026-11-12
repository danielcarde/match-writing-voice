#!/usr/bin/env python3
"""Validate and reproducibly package the canonical skill. Standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "match-writing-voice"
SKILL = ROOT / "skills" / SKILL_NAME
ROUTES = {"learn.md": ("Learning a voice", "learning-a-voice"),
          "learn-from-edits.md": ("Learn from before-and-after edits", "learn-from-before-and-after-edits"),
          "guided-mode.md": ("Optional guided picker", "optional-guided-picker"),
          "write.md": ("Writing in a voice", "writing-in-a-voice"),
          "rewrite.md": ("Rewrite existing content", "rewrite-existing-content"),
          "revision-review.md": ("Compare revisions and keep an edit record", "compare-revisions-and-keep-an-edit-record"),
          "detector-evaluation.md": ("Evaluate detector results", "evaluate-detector-results"),
          "editorial-review.md": ("Editorial review that preserves the voice", "editorial-review-that-preserves-the-voice"),
          "text-hygiene.md": ("Inspect copy-paste text artifacts", "inspect-copy-paste-text-artifacts"),
          "knowledge.md": ("Writer knowledge", "writer-knowledge"),
          "profile-format.md": ("Profile format", "profile-format"),
          "evaluation.md": ("Evaluation", "evaluation"),
          "provenance.md": ("Design provenance", "design-provenance"),
          "upstream-license.md": ("Upstream license", "upstream-license")}


def source_files():
    return sorted(p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                  and not any(part.startswith("voice-test-") for part in p.parts)
                  and p.suffix in {".md", ".py", ".yaml", ".yml", ".json", ".svg"})


def validate():
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not entry.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    front = entry.split("---", 2)[1]
    fields = dict(re.findall(r"^(name|description):\s*(.+)$", front, re.M))
    if fields.get("name") != SKILL_NAME or not 1 <= len(fields.get("description", "")) <= 200:
        raise ValueError("Shared skill name/description invalid; description must be <=200 characters")
    for file in ROOT.rglob("*.md"):
        if any(part in {".git", ".local", "dist", "__pycache__"} for part in file.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            target = target.strip("<>")
            if target.startswith(("https:", "http:", "mailto:", "#")):
                continue
            path = unquote(target.split("#", 1)[0])
            if path and not (file.parent / path).exists():
                raise ValueError(f"Broken reference: {file.relative_to(ROOT)} -> {target}")
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must be semantic major.minor.patch")
    for file in [ROOT / "plugin.json", ROOT / ".codex-plugin/plugin.json",
                 ROOT / ".claude-plugin/plugin.json", ROOT / "gemini-extension.json"]:
        obj = json.loads(file.read_text(encoding="utf-8"))
        if obj.get("version") != version or obj.get("name") != SKILL_NAME:
            raise ValueError(f"Version/name mismatch: {file}")
    codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    if codex["plugins"][0]["source"]["path"] != "./" or claude["plugins"][0]["source"] != "./":
        raise ValueError("Marketplace must resolve the repository plugin root")
    ET.parse(ROOT / "assets/banner.svg")
    if not source_files():
        raise ValueError("No skill source files")
    return {"version": version, "skill_files": len(source_files())}


def portable_text():
    main = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[2].strip()
    parts = ["# Portable writing-voice guide\n\nUse this guide with supplied samples and a brief. "
             "Python and file tools are optional; perform the procedure manually when unavailable. "
             "This text does not install a skill, train a model, or create permanent account memory.\n", main]
    for filename, (title, _) in ROUTES.items():
        body = (SKILL / "references" / filename).read_text(encoding="utf-8").split("\n", 1)[1]
        parts.append(f"## {title}\n{body}")
    text = "\n\n".join(parts) + "\n"
    for filename, (_, anchor) in ROUTES.items():
        text = text.replace(f"](references/{filename})", f"](#{anchor})").replace(f"]({filename})", f"](#{anchor})")
    return text


def archive(path, entries):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError(f"Corrupt archive: {path}")


def build(destination=None):
    validate()
    destination = Path(destination or ROOT / "dist")
    destination.mkdir(parents=True, exist_ok=True)
    entries = [(SKILL_NAME + "/" + p.relative_to(SKILL).as_posix(), p.read_bytes()) for p in source_files()]
    paths = []
    for filename, selected in [
        ("match-writing-voice.zip", entries),
        ("match-writing-voice-claude.zip", [(n, b) for n, b in entries if not n.endswith("/agents/openai.yaml")]),
        ("match-writing-voice.skill", entries),
    ]:
        target = destination / filename
        archive(target, selected)
        paths.append(target)
    plugin_entries = [("match-writing-voice/" + p, (ROOT / p).read_bytes()) for p in ["plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", "gemini-extension.json", "docs/extension-context.md"]]
    plugin_entries += [("match-writing-voice/skills/" + name, data) for name, data in entries]
    target = destination / "match-writing-voice-plugin.zip"
    archive(target, plugin_entries)
    paths.append(target)
    target = destination / "match-writing-voice-portable.md"
    target.write_text(portable_text(), encoding="utf-8", newline="\n")
    paths.append(target)
    sums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in paths)
    target = destination / "SHA256SUMS"
    target.write_text(sums, encoding="utf-8", newline="\n")
    return paths + [target]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate source without building")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(validate(), indent=2))
    else:
        for path in build():
            print(path)
