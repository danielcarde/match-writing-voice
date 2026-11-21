"""Reviewed candidate selection and isolated approved rewrite examples."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/match-writing-voice/scripts"
sys.path.insert(0, str(SCRIPTS))
import revision_tools as revisions


class RewriteSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rewrite-selection-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = "The team reviewed 12 records. Further trials remain planned.\n"
        self.draft = "The team checked 12 records, and further trials remain planned.\n"
        self.profile = {"schema_version": 1, "profile_id": "team", "defaults": {"mode": "faithful", "context": {}},
                        "samples": [], "observations": [], "rules": [], "traits": [{"id": "plain", "category": "vocabulary",
                        "instruction": "Use plain wording.", "state": "preferred", "confirmed": True,
                        "scope": {}, "policy": "preserve", "support": [], "counterevidence": []}]}
        self.settings = {"profile": self.profile, "current": {"medium": "report", "language": "en"}}
        self.metadata = {"schema_version": 1, "approved_by": "user", "approval_note": "User selected this team revision.",
                         "contribution": "shared", "split": "learning", "group_id": "report-one"}

    def review(self, draft=None, **changes):
        report = revisions.comparison(self.source, draft or self.draft, **self.settings)
        result = {"schema_version": 1, "comparison_id": report["comparison_id"], "reviewer": "model",
                  "meaning": {"status": "preserved", "reason": "The record count and pending work remain."},
                  "voice": {"status": "consistent", "reason": "Uses the supplied plain team voice."},
                  "edits": [{"id": item["id"], "decision": "keep", "purpose": "voice", "voice_effect": "supports",
                             "reason": "Connects the supplied points in plain language.", "trait_ids": ["plain"]}
                            for item in report["edits"]]}
        result.update(changes)
        return result

    def save_example(self, name, metadata=None, source=None, draft=None):
        original = source or self.source
        revised = draft or self.draft
        old_source = self.source
        self.source = original
        try:
            report = revisions.comparison(original, revised, review=self.review(revised), **self.settings)
        finally:
            self.source = old_source
        return revisions.save_history(self.root / name, original, revised, report, self.profile,
                                      example=metadata or self.metadata)

    def test_selection_requires_complete_meaning_and_voice_review(self):
        candidate = {"id": "first", "text": self.draft}
        report, text = revisions.selection(self.source, [candidate], **self.settings)
        self.assertIsNone(text)
        self.assertIsNone(report["selected_id"])
        candidate["review"] = self.review()
        report, text = revisions.selection(self.source, [candidate], **self.settings)
        self.assertEqual("first", report["selected_id"])
        self.assertEqual(self.draft, text)
        for changes in ({"edits": []}, {"meaning": {"status": "changed", "reason": "Changed meaning."}},
                        {"voice": {"status": "weakened", "reason": "Lost the requested voice."}}):
            candidate["review"] = self.review(**changes)
            self.assertIsNone(revisions.selection(self.source, [candidate], **self.settings)[1])

    def test_preferred_candidate_cannot_override_a_mechanical_block(self):
        damaged = self.draft.replace("12", "18")
        candidates = [{"id": "preferred", "text": damaged, "review": self.review(damaged)},
                      {"id": "faithful", "text": self.draft, "review": self.review()}]
        report, text = revisions.selection(self.source, candidates, **self.settings)
        self.assertEqual("faithful", report["selected_id"])
        self.assertEqual(self.draft, text)

    def test_stale_review_duplicate_candidates_and_empty_sets_are_rejected(self):
        for candidates in ([], [{"id": "a", "text": self.draft}, {"id": "a", "text": self.source}],
                           [{"id": "a", "text": self.draft}, {"id": "b", "text": self.draft}],
                           [{"id": "a", "text": self.draft, "review": self.review(comparison_id="stale")} ]):
            with self.subTest(candidates=candidates), self.assertRaises(ValueError):
                revisions.selection(self.source, candidates, **self.settings)

    def test_learning_excludes_holdouts_other_contexts_and_current_document(self):
        self.save_example("learning")
        self.save_example("holdout", {**self.metadata, "split": "holdout", "group_id": "report-two"},
                          "The team checked 7 sensors.\n", "The team reviewed 7 sensors.\n")
        result = revisions.approved_examples(self.root, "team", self.settings["current"], "A new source.")
        self.assertEqual(["learning"], [item["id"] for item in result["examples"]])
        self.assertEqual("shared", result["examples"][0]["contribution"])
        self.assertEqual(1, result["holdout_count"])
        self.assertEqual([], revisions.approved_examples(self.root, "team", {"medium": "email"}, "New.")["examples"])
        self.assertEqual([], revisions.approved_examples(self.root, "team", self.settings["current"], self.source)["examples"])

    def test_examples_reject_split_leakage_and_changed_snapshots(self):
        self.save_example("first")
        self.save_example("second", {**self.metadata, "split": "holdout"},
                          "The team checked 7 sensors.\n", "The team reviewed 7 sensors.\n")
        with self.assertRaisesRegex(ValueError, "split"):
            revisions.approved_examples(self.root, "team", self.settings["current"], "New.")
        (self.root / "first/revision.txt").write_text("Changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            revisions.approved_examples(self.root, "team", self.settings["current"], "New.")

    def test_examples_do_not_guess_a_missing_audience(self):
        target = self.settings["current"]
        self.settings["current"] = {**target, "audience": "project_team"}
        self.save_example("audience-specific")
        self.assertEqual([], revisions.approved_examples(self.root, "team", target, "New.")["examples"])

    def test_unapproved_or_unreviewed_examples_cannot_be_saved(self):
        report = revisions.comparison(self.source, self.draft, **self.settings)
        with self.assertRaises(ValueError):
            revisions.save_history(self.root / "unreviewed", self.source, self.draft, report, self.profile,
                                   example=self.metadata)
        self.assertFalse((self.root / "unreviewed").exists())
        approved = revisions.comparison(self.source, self.draft, review=self.review(), **self.settings)
        with self.assertRaises(ValueError):
            revisions.save_history(self.root / "invented-approval", self.source, self.draft, approved, self.profile,
                                   example={**self.metadata, "approved_by": "model"})

    def test_cli_selects_reviewed_text_and_saves_and_retrieves_approved_example(self):
        source, draft, profile, review, candidates, metadata, output = [self.root / name for name in
            ("source.txt", "draft.txt", "profile.json", "review.json", "candidates.json", "example.json", "out.txt")]
        source.write_bytes(self.source.encode("utf-8"))
        draft.write_bytes(self.draft.encode("utf-8"))
        for path, value in ((profile, self.profile), (review, self.review()), (metadata, self.metadata),
                            (candidates, {"schema_version": 1, "candidates": [{"id": "chosen", "draft": "draft.txt", "review": "review.json"}]})):
            path.write_text(json.dumps(value), encoding="utf-8")
        base = [sys.executable, str(SCRIPTS / "revision_tools.py")]
        settings = ["--source", str(source), "--profile", str(profile), "--context", json.dumps(self.settings["current"])]
        result = subprocess.run([*base, "select", *settings, "--candidates", str(candidates), "--output", str(output)],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("chosen", json.loads(result.stdout)["selected_id"])
        self.assertEqual(self.draft.encode("utf-8"), output.read_bytes())
        result = subprocess.run([*base, "compare", *settings, "--draft", str(draft), "--review", str(review),
                                 "--example", str(metadata), "--history-dir", str(self.root / "collection/accepted")],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        source.write_text("Another source.", encoding="utf-8")
        result = subprocess.run([*base, "examples", "--collection", str(self.root / "collection"), "--profile-id", "team",
                                 "--context", json.dumps(self.settings["current"]), "--source", str(source)],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["accepted"], [item["id"] for item in json.loads(result.stdout)["examples"]])

    def test_cli_selection_preserves_inputs_and_existing_output_when_review_missing(self):
        source, draft, candidates, output = [self.root / name for name in ("source.txt", "draft.txt", "candidates.json", "out.txt")]
        source.write_text(self.source, encoding="utf-8")
        draft.write_text(self.draft, encoding="utf-8")
        candidates.write_text(json.dumps({"schema_version": 1, "candidates": [{"id": "a", "draft": "draft.txt"}]}), encoding="utf-8")
        output.write_text("Existing output", encoding="utf-8")
        command = [sys.executable, str(SCRIPTS / "revision_tools.py"), "select", "--source", str(source),
                   "--candidates", str(candidates), "--output", str(output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("Existing output", output.read_text(encoding="utf-8"))
        for target in (source, draft, candidates):
            before = target.read_bytes()
            result = subprocess.run([*command[:-1], str(target)], capture_output=True, text=True)
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual(before, target.read_bytes())


if __name__ == "__main__":
    unittest.main()
