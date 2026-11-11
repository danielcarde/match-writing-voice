"""Read-only text inspection invariants with synthetic multilingual inputs."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/match-writing-voice/scripts/voice_tools.py"
spec = importlib.util.spec_from_file_location("text_hygiene_voice", SCRIPT)
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class TextInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hygiene-test-", dir=ROOT / "tests")
        self.root = Path(self.temp.name).resolve()
        if not self.root.is_relative_to((ROOT / "tests").resolve()):
            raise RuntimeError("Test cleanup escaped its parent")
        self.addCleanup(self.temp.cleanup)

    def run_cli(self, source, output=None):
        args = [sys.executable, str(SCRIPT), "inspect-text", "--text", str(source)]
        if output:
            args += ["--output", str(output)]
        return subprocess.run(args, capture_output=True, text=True, encoding="utf-8")

    def test_ordinary_language_and_typography_are_not_candidates(self):
        report = voice.inspect_text('Café — “sí,” she said.\n你好\tمرحبا\n')
        self.assertEqual([], report["candidates"])
        self.assertNotIn("verdict", report)
        self.assertFalse(report["source_modified"])

    def test_bom_line_endings_and_non_bmp_offsets_are_preserved(self):
        text = "\ufeffA\r\n😀B\u200bC\u00a0D"
        source = self.root / "input.txt"
        original = text.encode("utf-8")
        source.write_bytes(original)
        output = self.root / "report.json"
        result = self.run_cli(source, output)
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        by_code = {g["codepoint"]: g for g in report["candidates"]}
        self.assertEqual([0], by_code["U+FEFF"]["positions"])
        self.assertEqual([6], by_code["U+200B"]["positions"])
        self.assertEqual([8], by_code["U+00A0"]["positions"])
        self.assertEqual(hashlib.sha256(original).hexdigest(), report["text_sha256"])
        self.assertEqual(original, source.read_bytes())
        self.assertEqual(text.lstrip("\ufeff"), voice.read_text(source))

    def test_language_and_display_candidates_are_never_removed(self):
        text = "می\u200cروم 👩\u200d💻 ☀\ufe0f \u2067עברית\u2069 漢\U000E0100"
        report = voice.inspect_text(text)
        kinds = {g["kind"] for g in report["candidates"]}
        self.assertEqual({"joiner", "variation_selector", "direction_control"}, kinds)
        self.assertEqual("not_performed", report["linguistic_assessment"])
        self.assertFalse(report["normalization_performed"])
        self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(), report["text_sha256"])

    def test_grouping_limits_positions_but_keeps_complete_counts(self):
        report = voice.inspect_text("\u200b" * 65 + "\u00a0\u00a0")
        self.assertEqual(67, report["candidate_occurrences"])
        self.assertEqual(65, report["candidates"][0]["count"])
        self.assertEqual(list(range(50)), report["candidates"][0]["positions"])
        self.assertTrue(report["candidates"][0]["positions_truncated"])
        self.assertFalse(report["candidates"][1]["positions_truncated"])

    def test_no_normalization_of_composed_or_decomposed_characters(self):
        for text in ["é", "e\u0301"]:
            report = voice.inspect_text(text)
            self.assertEqual([], report["candidates"])
            self.assertEqual(len(text), report["input_characters"])
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), report["text_sha256"])

    def test_protected_regions_are_inspected_without_mutation(self):
        source = self.root / "source.md"
        original = '"a\u200bb"\n\n```text\n\u200cvalue\n```\nhttps://example.test/\u2060id\n'.encode()
        source.write_bytes(original)
        result = self.run_cli(source)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, json.loads(result.stdout)["candidate_occurrences"])
        self.assertEqual(original, source.read_bytes())

    def test_output_cannot_replace_source(self):
        source = self.root / "source.txt"
        source.write_bytes(b"original prose")
        result = self.run_cli(source, source)
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"original prose", source.read_bytes())

    def test_output_cannot_replace_source_through_hardlink(self):
        source = self.root / "source.txt"
        source.write_bytes(b"original prose")
        alias = self.root / "alias.txt"
        try:
            os.link(source, alias)
        except OSError as error:
            self.skipTest(f"Hardlinks unavailable: {error}")
        result = self.run_cli(source, alias)
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"original prose", source.read_bytes())
        self.assertEqual(b"original prose", alias.read_bytes())

    def test_binary_or_invalid_utf8_input_does_not_create_report(self):
        source, output = self.root / "source.txt", self.root / "report.json"
        for data in [b"\xff", b"binary\x00data"]:
            source.write_bytes(data)
            result = self.run_cli(source, output)
            self.assertEqual(2, result.returncode)
            self.assertFalse(output.exists())
            self.assertEqual(data, source.read_bytes())


if __name__ == "__main__":
    unittest.main()
