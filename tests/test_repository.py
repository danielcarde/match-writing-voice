import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build, installer, demo = tool("build"), tool("install"), tool("demo")


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "tests"
        self.temp = tempfile.TemporaryDirectory(prefix="repo-test-", dir=parent)
        self.path = Path(self.temp.name).resolve()
        if not self.path.is_relative_to(parent.resolve()):
            raise RuntimeError("Cleanup target escaped tests")
        self.addCleanup(self.temp.cleanup)

    def test_source_links_and_manifests(self):
        self.assertGreater(build.validate()["skill_files"], 0)

    def test_archives_have_matching_root_and_core_bytes(self):
        outputs = build.build(self.path)
        for path in outputs:
            if path.suffix in {".zip", ".skill"} and "plugin" not in path.name:
                with zipfile.ZipFile(path) as z:
                    self.assertTrue(all(n.startswith("match-writing-voice/") for n in z.namelist()))
                    self.assertEqual((build.SKILL / "SKILL.md").read_bytes(), z.read("match-writing-voice/SKILL.md"))
                    self.assertFalse(any("__pycache__" in n for n in z.namelist()))

    def test_build_is_reproducible(self):
        first = {p.name: p.read_bytes() for p in build.build(self.path / "one")}
        second = {p.name: p.read_bytes() for p in build.build(self.path / "two")}
        self.assertEqual(first, second)

    def test_checksums_match_every_distributed_asset(self):
        build.build(self.path)
        for line in (self.path / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, hashlib.sha256((self.path / name).read_bytes()).hexdigest())

    def test_claude_package_omits_codex_ui_metadata(self):
        build.build(self.path)
        with zipfile.ZipFile(self.path / "match-writing-voice-claude.zip") as z:
            self.assertNotIn("match-writing-voice/agents/openai.yaml", z.namelist())
            self.assertIn("match-writing-voice/references/knowledge.md", z.namelist())

    def test_editorial_guidance_and_upstream_notice_survive_all_packages(self):
        outputs = build.build(self.path)
        for path in outputs:
            if path.suffix in {".zip", ".skill"}:
                prefix = "match-writing-voice/" + ("skills/match-writing-voice/" if "plugin" in path.name else "")
                with zipfile.ZipFile(path) as z:
                    for name in ["editorial-review.md", "upstream-license.md"]:
                        source = build.SKILL / "references" / name
                        self.assertEqual(source.read_bytes(), z.read(prefix + "references/" + name))
        portable = (self.path / "match-writing-voice-portable.md").read_text(encoding="utf-8")
        # Portable instructions must resolve bundled links internally, not depend on source files.
        for name in build.ROUTES:
            self.assertNotIn("](" + name + ")", portable)
            self.assertNotIn("](references/" + name + ")", portable)
        license_body = (build.SKILL / "references/upstream-license.md").read_text(encoding="utf-8")
        self.assertIn(license_body.split("```text\n", 1)[1].split("```", 1)[0], portable)

    def test_dry_run_writes_nothing(self):
        result = installer.install("codex", "user", user_home=self.path, dry_run=True)
        self.assertFalse(result["written"])
        self.assertEqual([], list(self.path.iterdir()))

    def test_three_local_host_installations_preserve_source(self):
        for host in installer.AGENTS:
            result = installer.install(host, "project", project=self.path / host)
            target = Path(result["target"])
            self.assertEqual((installer.SOURCE / "SKILL.md").read_bytes(), (target / "SKILL.md").read_bytes())
            self.assertEqual((installer.SOURCE / "scripts/voice_tools.py").read_bytes(), (target / "scripts/voice_tools.py").read_bytes())

    def test_installer_refuses_existing_destination(self):
        result = installer.install("claude-code", "project", project=self.path)
        marker = Path(result["target"]) / "local-change.txt"
        marker.write_text("preserve this", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install("claude-code", "project", project=self.path)
        self.assertEqual("preserve this", marker.read_text())

    def test_synthetic_demo_validates_all_modes(self):
        result = demo.run(self.path / "demo")
        self.assertTrue(result["validation"]["source_verified"])
        self.assertTrue(all(v == "PASS" for v in result["draft_verdicts"].values()))


if __name__ == "__main__":
    unittest.main()
