"""Protected source spans survive a rewrite or restoration fails closed."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/match-writing-voice/scripts/voice_tools.py"
spec = importlib.util.spec_from_file_location("protected_voice_tools", SCRIPT)
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class ProtectedRewriteTests(unittest.TestCase):
    def test_restores_repeated_spans_unicode_and_exact_whitespace(self):
        source = '\ufeffLabGate reports “12 µs”.\r\n\r\nLabGate uses p < 0.03.'
        bundle = voice.freeze_text(source, ["LabGate", "“12 µs”", "p < 0.03", "LabGate"])
        self.assertEqual(4, len(bundle["spans"]))
        draft = bundle["text"].replace("reports", "recorded").replace("uses", "reported")
        self.assertEqual(source.replace("reports", "recorded").replace("uses", "reported"),
                         voice.restore_text(source, draft, bundle))

    def test_rejects_missing_duplicate_reordered_unknown_or_damaged_markers(self):
        source = "LabGate recorded 12 ms."
        bundle = voice.freeze_text(source, ["LabGate", "12 ms"])
        first, second = [item["marker"] for item in bundle["spans"]]
        for draft in (bundle["text"].replace(first, ""), bundle["text"] + first,
                      f"{second} recorded {first}.", bundle["text"] + "[[MWV_unknown]]",
                      bundle["text"] + "[[MWV_broken", bundle["text"].replace(first, first.lower())):
            with self.subTest(draft=draft), self.assertRaisesRegex(ValueError, "marker"):
                voice.restore_text(source, draft, bundle)

    def test_stale_source_or_modified_bundle_is_rejected(self):
        source = "LabGate recorded 12 ms."
        bundle = voice.freeze_text(source, ["12 ms"])
        altered = copy.deepcopy(bundle)
        altered["spans"][0]["text"] = "20 ms"
        for original, candidate in ((source + " Updated.", bundle), (source, altered),
                                    (source, {**bundle, "text": "Other text"}),
                                    (source, {**bundle, "spans": None})):
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                voice.restore_text(original, bundle["text"], candidate)

    def test_invalid_absent_overlapping_or_reserved_spans_are_rejected(self):
        for source, spans in (("A result.", []), ("A result.", [""]), ("A result.", [12]),
                              ("A result.", ["absent"]), ("12 ms", ["12", "12 ms"]),
                              ("[[MWV_literal]] result", ["result"])):
            with self.subTest(source=source, spans=spans), self.assertRaises(ValueError):
                voice.freeze_text(source, spans)

    def test_cli_restores_bytes_and_refuses_input_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="protected-rewrite-") as folder:
            root = Path(folder)
            source, inventory, bundle, draft, restored = [root / name for name in
                ("source.txt", "protected.json", "bundle.json", "draft.txt", "restored.txt")]
            original = b"LabGate recorded 12 ms.\r\n"
            source.write_bytes(original)
            inventory.write_text(json.dumps({"spans": ["12 ms"]}), encoding="utf-8")
            freeze = [sys.executable, str(SCRIPT), "freeze", "--source", str(source),
                      "--protect-file", str(inventory), "--output", str(bundle)]
            result = subprocess.run(freeze, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            prepared = json.loads(bundle.read_text(encoding="utf-8"))
            draft.write_bytes(prepared["text"].replace("recorded", "measured").encode("utf-8"))
            restore = [sys.executable, str(SCRIPT), "restore", "--source", str(source),
                       "--bundle", str(bundle), "--draft", str(draft), "--output", str(restored)]
            result = subprocess.run(restore, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(original.replace(b"recorded", b"measured"), restored.read_bytes())
            for command, inputs in ((freeze, [source, inventory]), (restore, [source, bundle, draft])):
                for target in inputs:
                    before = target.read_bytes()
                    result = subprocess.run([*command[:-1], str(target)], capture_output=True, text=True)
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertEqual(before, target.read_bytes())
            before = restored.read_bytes()
            draft.write_text("A rewrite missing every marker.", encoding="utf-8")
            result = subprocess.run(restore, capture_output=True, text=True)
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual(before, restored.read_bytes())


if __name__ == "__main__":
    unittest.main()
