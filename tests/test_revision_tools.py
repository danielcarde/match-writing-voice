"""Synthetic end-to-end tests for comparisons, retained history, and imported evaluations."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/match-writing-voice/scripts/revision_tools.py"


class RevisionToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="revision-test-", dir=ROOT / "tests")
        self.root = Path(self.temp.name).resolve()
        if not self.root.is_relative_to((ROOT / "tests").resolve()):
            raise RuntimeError("Test cleanup escaped its parent")
        self.addCleanup(self.temp.cleanup)
        self.source = self.text("original.txt", "Overall, we may meet Tuesday. The room closes at 5 pm.\n")
        self.draft = self.text("revised.txt", "We may meet Tuesday, but the room closes at 5 pm.\n")
        self.profile = self.json("profile.json", {
            "schema_version": 1, "profile_id": "writer", "defaults": {"mode": "faithful", "context": {}},
            "samples": [],
            "observations": [
                {"context": {"medium": "essay", "language": "en"}, "measurements": {"word_count": 95}},
                {"context": {"medium": "email", "language": "en"}, "measurements": {"word_count": 32}},
            ],
            "traits": [{"id": "recap", "category": "vocabulary", "instruction": "Keep Overall when requested.",
                        "state": "preferred", "confirmed": True, "scope": {"medium": "essay"},
                        "policy": "preserve", "support": [], "counterevidence": []}],
            "rules": [{"id": "recap-word", "trait_id": "recap", "kind": "require", "text": "Overall"}],
        })

    def text(self, name, content):
        path = self.root / name
        path.write_bytes(content.encode("utf-8"))
        return path

    def json(self, name, value):
        return self.text(name, json.dumps(value, ensure_ascii=False))

    def run_tool(self, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8")

    def compare(self, *args):
        return self.run_tool("compare", "--source", self.source, "--draft", self.draft, *args)

    def decode(self, result, code=0):
        self.assertEqual(code, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def with_profile(self, *args):
        return self.compare("--profile", self.profile, "--context", '{"medium":"essay","language":"en"}', *args)

    def test_exact_edits_reconstruct_revision_with_bom_crlf_and_unicode(self):
        original = "\ufeffFirst 😀 sentence.\r\n\r\nLast line.\r\n"
        revised = "First 😀 sentence!\n\nAn inserted line.\nLast line."
        self.source.write_bytes(original.encode())
        self.draft.write_bytes(revised.encode())
        result = self.decode(self.compare())
        rebuilt, cursor = [], 0
        for edit in result["edits"]:
            a, b = edit["source_span"]
            c, d = edit["revision_span"]
            self.assertEqual(original[a:b], edit["before"])
            self.assertEqual(revised[c:d], edit["after"])
            rebuilt.extend([original[cursor:a], edit["after"]])
            cursor = b
        rebuilt.append(original[cursor:])
        self.assertEqual(revised, "".join(rebuilt))
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(), result["source"]["sha256"])

    def test_comparison_uses_scoped_traits_baselines_and_rule_deltas(self):
        result = self.decode(self.with_profile())
        self.assertEqual(["recap"], [t["id"] for t in result["applicable_traits"]])
        self.assertEqual(["recap-word"], result["profile_rule_changes"]["introduced"])
        self.assertEqual([95], [g["measurements"]["word_count"] for g in result["authored_baselines"]["groups"]])
        self.assertFalse(result["profile_evidence_verified_now"])
        self.assertEqual("not_supplied", result["editorial_review"]["coverage"])
        self.assertIsNone(result["source"]["measurements"]["mattr_50"])
        self.assertFalse(result["mechanical_checks"]["manual_review_completed"])

    def test_mismatched_context_does_not_mix_evidence(self):
        report = self.decode(self.compare("--profile", self.profile, "--context", '{"medium":"chat"}'))
        self.assertEqual([], report["applicable_traits"])
        self.assertEqual("no_matching_context", report["authored_baselines"]["status"])
        self.assertEqual([], report["profile_rule_changes"]["introduced"])
        report = self.decode(self.compare("--profile", self.profile))
        self.assertEqual("context_required", report["authored_baselines"]["status"])

    def test_large_enough_text_has_rolling_lexical_diversity(self):
        self.source.write_bytes(("red blue " * 30).encode())
        self.draft.write_bytes(" ".join(f"word{i}" for i in range(60)).encode())
        report = self.decode(self.compare())
        self.assertEqual(0.04, report["source"]["measurements"]["mattr_50"])
        self.assertEqual(1.0, report["revision"]["measurements"]["mattr_50"])

    def test_noop_has_no_edits_and_is_reproducible(self):
        self.draft.write_bytes(self.source.read_bytes())
        first = self.decode(self.with_profile())
        second = self.decode(self.with_profile())
        self.assertEqual(first, second)
        self.assertTrue(first["text_identical"])
        self.assertEqual([], first["edits"])

    def test_review_annotations_are_bound_and_partial_review_stays_visible(self):
        before = self.decode(self.with_profile())
        eid = before["edits"][0]["id"]
        review = self.json("review.json", {"schema_version": 1, "comparison_id": before["comparison_id"], "reviewer": "human",
                                           "edits": [{"id": eid, "decision": "revert", "purpose": "unnecessary",
                                                      "voice_effect": "weakens", "reason": "Removes the requested recap.",
                                                      "trait_ids": ["recap"]}]})
        after = self.decode(self.with_profile("--review", review))
        self.assertEqual("partial", after["editorial_review"]["coverage"])
        self.assertEqual([eid], after["editorial_review"]["flagged_edit_ids"])
        self.assertEqual(before["mechanical_checks"], after["mechanical_checks"])
        self.assertEqual(before["comparison_id"], after["comparison_id"])
        self.draft.write_bytes(self.draft.read_bytes() + b"A new line.\n")
        self.assertEqual(2, self.with_profile("--review", review).returncode)

    def test_complete_supplied_review_does_not_suppress_mechanical_block(self):
        self.draft.write_bytes(self.draft.read_bytes().replace(b"5 pm", b"6 pm"))
        report = self.decode(self.with_profile(), 1)
        review = self.json("review.json", {"schema_version": 1, "comparison_id": report["comparison_id"], "reviewer": "model",
                           "meaning": {"status": "changed", "reason": "The closing time changed."},
                           "voice": {"status": "needs_review", "reason": "The recap is absent."},
                           "edits": [{"id": e["id"], "decision": "review", "purpose": "uncertain", "voice_effect": "uncertain",
                                      "reason": "Needs source review."} for e in report["edits"]]})
        result = self.decode(self.with_profile("--review", review), 1)
        self.assertEqual("complete", result["editorial_review"]["coverage"])
        self.assertEqual("BLOCK", result["mechanical_checks"]["verdict"])
        self.assertFalse(result["mechanical_checks"]["manual_review_completed"])

    def test_history_is_opt_in_exact_and_never_overwritten(self):
        before_files = set(self.root.iterdir())
        self.decode(self.with_profile())
        self.assertEqual(before_files, set(self.root.iterdir()))
        history = self.root / "history"
        saved = self.decode(self.with_profile("--history-dir", history, "--source-origin", "human", "--draft-origin", "ai_assisted"))
        self.assertEqual(self.source.read_bytes(), (history / "original.txt").read_bytes())
        self.assertEqual(self.draft.read_bytes(), (history / "revision.txt").read_bytes())
        self.assertEqual("ai_assisted", saved["revision"]["origin_supplied"])
        self.assertTrue(self.decode(self.run_tool("verify-history", "--history-dir", history))["verified"])
        previous = (history / "history.json").read_bytes()
        self.assertEqual(2, self.with_profile("--history-dir", history).returncode)
        self.assertEqual(previous, (history / "history.json").read_bytes())
        (history / "revision.txt").write_bytes(b"tampered")
        self.assertFalse(self.decode(self.run_tool("verify-history", "--history-dir", history), 1)["verified"])

    def test_alias_and_internal_snapshot_output_are_rejected_before_writing(self):
        original = self.source.read_bytes()
        history = self.root / "run"
        self.assertEqual(2, self.compare("--output", self.source, "--history-dir", history).returncode)
        self.assertEqual(2, self.compare("--output", history / "original.txt", "--history-dir", history).returncode)
        self.assertFalse(history.exists())
        self.assertEqual(original, self.source.read_bytes())

    def test_history_index_cannot_reference_another_file(self):
        history = self.root / "run"
        self.decode(self.compare("--history-dir", history))
        path = history / "history.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"]["../original.txt"] = data["files"]["original.txt"]
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(2, self.run_tool("verify-history", "--history-dir", history).returncode)

    def test_manifest_reverification_excludes_holdouts_and_other_contexts(self):
        manifest = self.json("samples.json", {"samples": [
            {"id": "essay", "path": self.source.name, "author_id": "writer", "kind": "typed", "provenance": "author", "context": {"medium": "essay", "language": "en"}},
            {"id": "other", "path": self.draft.name, "author_id": "writer", "kind": "typed", "provenance": "author", "context": {"medium": "email", "language": "en"}},
            {"id": "held", "path": self.draft.name, "author_id": "writer", "kind": "typed", "provenance": "author", "held_out": True, "context": {"medium": "essay", "language": "en"}},
        ]})
        measured = self.root / "measured.json"
        result = subprocess.run([sys.executable, str(SCRIPT.with_name("voice_tools.py")), "measure", "--manifest", str(manifest),
                                 "--profile-id", "writer", "--output", str(measured)], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        data = json.loads(measured.read_text(encoding="utf-8"))
        data["traits"] = json.loads(self.profile.read_text(encoding="utf-8"))["traits"]
        measured.write_text(json.dumps(data), encoding="utf-8")
        report = self.decode(self.compare("--profile", measured, "--manifest", manifest, "--context", '{"medium":"essay","language":"en"}'))
        self.assertTrue(report["profile_evidence_verified_now"])
        self.assertEqual([["essay"]], [b["sample_ids"] for b in report["authored_baselines"]["groups"]])
        self.source.write_bytes(self.source.read_bytes() + b"Modified.")
        self.assertEqual(2, self.compare("--profile", measured, "--manifest", manifest).returncode)

    def detector_rows(self):
        rows = []
        for name, origin, prediction in [("human1", "human", "ai_paraphrased"), ("human2", "human", "mixed"),
                                         ("human3", "human", "uncertain"), ("assisted", "ai_assisted", "ai_paraphrased"),
                                         ("ai1", "ai", "ai"), ("unknown1", "unknown", "human")]:
            path = self.text(name + ".txt", f"Synthetic test text {name}.\n")
            rows.append({"id": name, "path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "known_origin": origin, "prediction": prediction, "raw_label": prediction + " (synthetic)"})
        return rows

    def detector_input(self, rows):
        return self.json("detector-results.json", {"schema_version": 1,
                         "detector": {"name": "Synthetic fixture", "version": "test-1", "run_date": "2026-11-11", "settings": "synthetic labels"},
                         "samples": rows})

    def test_evaluation_separates_origins_and_reports_uncertainty(self):
        rows = self.detector_rows()
        rows.append({**rows[0], "id": "duplicate"})
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        self.assertEqual(6, report["sample_count"])
        self.assertEqual(0, report["network_calls"])
        self.assertEqual("test-1", report["detector"]["version"])
        self.assertEqual(1, report["counts_by_origin_and_prediction"]["ai_assisted"]["ai_paraphrased"])
        self.assertEqual(3, report["human_baseline"]["count"])
        self.assertEqual(1, report["human_baseline"]["definite_ai_flags"])
        self.assertEqual(1, report["human_baseline"]["mixed"])
        self.assertEqual(1, report["human_baseline"]["uncertain"])
        self.assertAlmostEqual(1 / 3, report["human_baseline"]["definite_ai_flag_fraction"], places=5)
        low, high = report["human_baseline"]["wilson_95_interval"]
        self.assertTrue(low < 1 / 3 < high)
        self.assertEqual([{"id": "duplicate", "duplicate_of": "human1"}], report["exact_duplicates_excluded"])

    def test_evaluation_without_human_baseline_reports_no_rate(self):
        rows = [r for r in self.detector_rows() if r["known_origin"] != "human"]
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        self.assertIsNone(report["human_baseline"]["definite_ai_flag_fraction"])
        self.assertIsNone(report["human_baseline"]["wilson_95_interval"])

    def test_matched_observations_keep_origins_and_incomplete_pairs_visible(self):
        rows = self.detector_rows()
        rows[0].update(pair_id="sample-a", variant="baseline")
        rows[3].update(pair_id="sample-a", variant="candidate", prediction="human", raw_label="human (synthetic)")
        rows[1].update(pair_id="missing-candidate", variant="baseline")
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        paired = report["paired_observations"]
        self.assertEqual(1, paired["complete_pairs"])
        self.assertEqual(["missing-candidate"], paired["incomplete_pair_ids"])
        self.assertEqual(1, paired["paraphrasing_flag_only_at_baseline"])
        self.assertEqual("human", paired["pairs"][0]["baseline_origin"])
        self.assertEqual("ai_assisted", paired["pairs"][0]["candidate_origin"])
        self.assertEqual(1, report["human_baseline"]["definite_ai_flags"])

    def test_duplicate_pairs_use_canonical_rows_and_count_once(self):
        rows = self.detector_rows()
        rows[0].update(pair_id="original-pair", variant="baseline")
        rows[3].update(pair_id="original-pair", variant="candidate", prediction="human", raw_label="human (synthetic)")
        rows += [{**rows[0], "id": "base-copy", "pair_id": "copy-pair"},
                 {**rows[3], "id": "candidate-copy", "pair_id": "copy-pair"}]
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        paired = report["paired_observations"]
        self.assertEqual(6, report["sample_count"])
        self.assertEqual(1, paired["complete_pairs"])
        self.assertEqual(1, paired["paraphrasing_flag_only_at_baseline"])
        self.assertEqual([{"pair_id": "copy-pair", "duplicate_of": "original-pair"}], paired["exact_duplicate_pairs_excluded"])
        ids = {r["id"] for r in report["records"]}
        self.assertTrue(all(p["baseline_id"] in ids and p["candidate_id"] in ids for p in paired["pairs"]))

    def test_evaluation_rejects_stale_bytes_and_conflicting_duplicates(self):
        rows = self.detector_rows()
        rows.append({**rows[0], "id": "conflict", "known_origin": "ai"})
        result = self.run_tool("evaluate-detector", "--results", self.detector_input(rows))
        self.assertEqual(2, result.returncode)
        self.assertIn("conflicting", result.stderr)
        rows.pop()
        (self.root / rows[0]["path"]).write_bytes(b"different text")
        result = self.run_tool("evaluate-detector", "--results", self.detector_input(rows))
        self.assertEqual(2, result.returncode)
        self.assertIn("hash", result.stderr)

    def test_evaluation_report_cannot_overwrite_detector_input_text(self):
        rows = self.detector_rows()
        source = self.root / rows[0]["path"]
        before = source.read_bytes()
        result = self.run_tool("evaluate-detector", "--results", self.detector_input(rows), "--output", source)
        self.assertEqual(2, result.returncode)
        self.assertEqual(before, source.read_bytes())

    def test_compare_uses_protection_file_and_does_not_overwrite_it(self):
        self.source.write_text("LabGate opened. LabGate closed.", encoding="utf-8")
        self.draft.write_text("LabGate opened and closed.", encoding="utf-8")
        inventory = self.json("protected.json", {"spans": ["LabGate"]})
        result = self.compare("--protect-file", inventory)
        self.assertEqual(1, result.returncode)
        self.assertIn("protected_text_count_drift", result.stdout)
        original = inventory.read_bytes()
        result = self.compare("--protect-file", inventory, "--output", inventory)
        self.assertEqual(2, result.returncode)
        self.assertEqual(original, inventory.read_bytes())

    def test_provider_badge_transitions_are_independent_of_overall_predictions(self):
        rows = self.detector_rows()
        rows[0].update(prediction="ai", raw_label="ai", pair_id="draft", variant="baseline")
        rows[3].update(prediction="ai", raw_label="ai", pair_id="draft", variant="candidate", paraphrasing_badge="absent")
        rows.append({**rows[0], "id": "same-scan-with-badge", "paraphrasing_badge": "present"})
        del rows[-1]["pair_id"], rows[-1]["variant"]
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        self.assertEqual([{"baseline": "ai", "candidate": "ai", "count": 1}],
                         report["paired_observations"]["prediction_transitions"])
        badge = report["provider_observations"]["paraphrasing_badge"]
        self.assertEqual([{"baseline": "present", "candidate": "absent", "count": 1}], badge["paired_transitions"])
        self.assertEqual(2, badge["counts_by_origin"]["human"]["unrecorded"])
        rows.append({**rows[-1], "id": "conflict", "paraphrasing_badge": "absent"})
        result = self.run_tool("evaluate-detector", "--results", self.detector_input(rows))
        self.assertEqual(2, result.returncode)
        self.assertIn("conflicting paraphrasing_badge", result.stderr)

    def test_suppressed_score_remains_distinct_from_zero_and_a_reported_positive(self):
        rows = self.detector_rows()[:3]
        rows[0].update(prediction="uncertain", raw_label="*%", reported_score="*%", score_state="suppressed",
                       pair_id="essay", variant="baseline")
        rows[1].update(prediction="human", raw_label="0%", reported_score="0%", score_state="zero",
                       pair_id="essay", variant="candidate")
        rows[2].update(prediction="ai", raw_label="35%", reported_score="35%", score_state="reported")
        report = self.decode(self.run_tool("evaluate-detector", "--results", self.detector_input(rows)))
        states = report["provider_observations"]["score_state"]
        self.assertEqual({"zero": 1, "suppressed": 1, "reported": 1, "unrecorded": 0}, states["counts_by_origin"]["human"])
        self.assertEqual([{"baseline": "suppressed", "candidate": "zero", "count": 1}], states["paired_transitions"])
        self.assertEqual(1, report["human_baseline"]["definite_ai_flags"])
        rows[0]["prediction"] = "human"
        result = self.run_tool("evaluate-detector", "--results", self.detector_input(rows))
        self.assertEqual(2, result.returncode)
        self.assertIn("suppressed score", result.stderr)


if __name__ == "__main__":
    unittest.main()
