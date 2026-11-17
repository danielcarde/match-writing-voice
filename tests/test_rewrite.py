"""Source-based rewrite invariants; no model-generated fixtures or API calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/match-writing-voice/scripts/voice_tools.py"
spec = importlib.util.spec_from_file_location("rewrite_voice_tools", SCRIPT)
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class RewriteTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"schema_version": 1, "profile_id": "rewrite-fixture", "defaults": {"mode": "faithful", "context": {}},
                        "samples": [], "observations": [], "rules": [], "traits": [{"id": "plain", "category": "vocabulary", "instruction": "Use plain wording.", "state": "preferred", "confirmed": True, "scope": {}, "policy": "preserve", "support": [], "counterevidence": []}]}

    def test_paragraph_rewrite_can_change_sentence_boundaries(self):
        result = voice.check(self.profile, "We can meet Tuesday, but the room must close by 5 pm.",
                             source="We can meet Tuesday. The room must close by 5 pm.", workflow="rewrite")
        self.assertEqual("PASS", result["verdict"])
        self.assertEqual("preserve", result["structure"])

    def test_rewrite_requires_source(self):
        with self.assertRaisesRegex(ValueError, "nonempty"):
            voice.check(self.profile, "New prose.", workflow="rewrite")

    def test_empty_result_is_not_a_completed_rewrite(self):
        result = voice.check(self.profile, "  ", source="A complete original paragraph.", workflow="rewrite")
        self.assertEqual("BLOCK", result["verdict"])
        self.assertIn("rewrite_empty", [x["code"] for x in result["findings"]])

    def test_structure_option_cannot_be_silently_ignored(self):
        with self.assertRaises(ValueError):
            voice.check(self.profile, "New prose.", structure="preserve")

    def test_preserve_flags_collapsed_paragraphs(self):
        result = voice.rewrite_review("First argument.\n\nSecond argument.", "First argument. Second argument.")
        self.assertIn("paragraphs", [x.get("feature") for x in result])

    def test_preserve_flags_heading_changes(self):
        hits = voice.rewrite_review("# Findings\n\nThe result is stable.", "# Conclusion\n\nThe result stays stable.")
        self.assertIn("headings", [x.get("feature") for x in hits])

    def test_restructure_allows_layout_changes(self):
        self.assertEqual([], voice.rewrite_review("# Findings\n\nFirst point.\n\nSecond point.", "# Result\n\nFirst point and second point.", "restructure"))

    def test_code_protected_even_when_restructuring(self):
        hits = voice.rewrite_review("```python\nvalue = 1\n```", "```python\nvalue = 2\n```", "restructure")
        self.assertEqual("block", hits[0]["severity"])

    def test_unchanged_code_can_move_in_restructure(self):
        a = "Text.\n\n```python\nvalue = 1\n```"
        b = "```python\nvalue = 1\n```\n\nText."
        self.assertEqual([], voice.rewrite_review(a, b, "restructure"))

    def test_crlf_and_lf_are_equivalent(self):
        source = "# Plan\n\nText.\n\n~~~text\nexample\n~~~"
        self.assertEqual([], voice.rewrite_review(source, source.replace("\n", "\r\n")))

    def test_lists_and_tables_are_accounted_for(self):
        source = "- alpha\n- beta\n\n| a | b |\n|---|---|\n| c | d |"
        draft = "- alpha\n\n| a | b |\n|---|---|"
        hits = voice.rewrite_review(source, draft)
        self.assertEqual({"list_items", "table_columns_by_row"}, {x.get("feature") for x in hits})

    def test_citation_loss_is_reviewed_in_both_structures(self):
        for structure in ("preserve", "restructure"):
            hits = voice.rewrite_review("The claim is qualified.[^smith]\n\n[^smith]: Citation.", "The claim is qualified.", structure)
            self.assertIn("rewrite_citation_drift", [x["code"] for x in hits])

    def test_shortened_essay_gets_coverage_review(self):
        source = " ".join(["This synthetic argument includes supporting evidence and qualifications."] * 12)
        self.assertIn("rewrite_length_drop", [x["code"] for x in voice.rewrite_review(source, "A brief summary.")])

    def test_editing_mode_remains_separate(self):
        for mode in ("faithful", "lightly_edited", "adapted"):
            result = voice.check(self.profile, "The result is stable.", source="The result is stable.", mode=mode, workflow="rewrite")
            self.assertEqual(mode, result["mode"])
            self.assertEqual("rewrite", result["workflow"])
            self.assertEqual("PASS", result["verdict"])

    def test_existing_meaning_checks_still_block_value_changes(self):
        result = voice.check(self.profile, "The budget is $70.", source="The budget is $40.", workflow="rewrite", structure="restructure")
        self.assertEqual("BLOCK", result["verdict"])
        self.assertIn("exact_value_drift", [x["code"] for x in result["findings"]])

    def test_protected_inventory_detects_changed_equations_and_repeated_terms(self):
        with tempfile.TemporaryDirectory(prefix="rewrite-protection-", dir=ROOT / "tests") as folder:
            inventory = Path(folder) / "protected.json"
            equation = "$t = b - a$"
            term = "LabGate"
            inventory.write_text(json.dumps({"spans": [equation, term]}), encoding="utf-8")
            source = f"{term} uses {equation}. The team tested {term}."
            draft = f"The team tested {term} using $t = a - b$."
            protected = voice.load_protected([], inventory, source)
            result = voice.check(self.profile, draft, source=source, protected=protected,
                                 workflow="rewrite", structure="restructure")
            findings = {finding["code"]: finding for finding in result["findings"]}
            self.assertEqual("BLOCK", result["verdict"])
            self.assertEqual(equation, findings["protected_text_missing"]["text"])
            self.assertEqual((2, 1), (findings["protected_text_count_drift"]["source"],
                                     findings["protected_text_count_drift"]["draft"]))
            with self.assertRaisesRegex(ValueError, "absent from the original"):
                voice.load_protected([], inventory, draft)

    def test_automated_pass_does_not_claim_manual_review(self):
        result = voice.check(self.profile, "The result is stable.", source="The result is stable.", workflow="rewrite")
        self.assertEqual("PASS", result["verdict"])
        self.assertFalse(result["manual_review_completed"])
        self.assertTrue(result["manual_review"])

    def test_protected_statistical_expression_keeps_its_operator(self):
        expression = "p < 0.03"
        source = f"We propose a filter. The pilot found a timing difference ({expression})."
        faithful = f"The filter is our proposal. In the pilot, timing differed ({expression})."
        protected = voice.load_protected([expression], None, source)
        result = voice.check(self.profile, faithful, source=source, protected=protected, workflow="rewrite")
        self.assertEqual("PASS", result["verdict"])
        for replacement in ("p > 0.03", "p ¡ 0.03", "p 0.03"):
            with self.subTest(replacement=replacement):
                draft = faithful.replace(expression, replacement)
                result = voice.check(self.profile, draft, source=source, protected=protected, workflow="rewrite")
                self.assertEqual("BLOCK", result["verdict"])
                missing = [finding["text"] for finding in result["findings"]
                           if finding["code"] == "protected_text_missing"]
                self.assertIn(expression, missing)

    def test_cli_rewrite_controls(self):
        parent = ROOT / "tests"
        with tempfile.TemporaryDirectory(prefix="repo-test-rewrite-", dir=parent) as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(parent.resolve()))
            profile, source, draft = root / "profile.json", root / "source.txt", root / "draft.txt"
            profile.write_text(json.dumps(self.profile), encoding="utf-8")
            source.write_text("# Plan\n\nA first point.\n\nA second point.", encoding="utf-8")
            draft.write_text("# Result\n\nA first point and a second point.", encoding="utf-8")
            base = [sys.executable, str(SCRIPT), "check", "--profile", str(profile), "--draft", str(draft), "--workflow", "rewrite"]
            result = subprocess.run(base, capture_output=True, text=True)
            self.assertEqual(2, result.returncode)
            inventory = root / "protected.json"
            inventory.write_text(json.dumps({"spans": ["second point"]}), encoding="utf-8")
            options = ["--source", str(source), "--structure", "restructure", "--protect-file", str(inventory)]
            result = subprocess.run(base + options, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("PASS", json.loads(result.stdout)["verdict"])
            original = source.read_bytes()
            result = subprocess.run(base + options + ["--output", str(source)], capture_output=True, text=True)
            self.assertEqual(2, result.returncode)
            self.assertEqual(original, source.read_bytes())


if __name__ == "__main__":
    unittest.main()
