"""Bounded behavioral tests. Synthetic samples; no remote services or personal corpus."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "voice_tools.py"
spec = importlib.util.spec_from_file_location("voice_tools", SCRIPT)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class VoiceToolsTests(unittest.TestCase):
    def setUp(self):
        # Keep fixtures inside this writable tree; some Windows sandboxes expose
        # a system temp path whose child files cannot be opened.
        fixture_parent = Path(__file__).resolve().parent
        self.temp = tempfile.TemporaryDirectory(prefix="voice-test-", dir=fixture_parent)
        if not Path(self.temp.name).resolve().is_relative_to(fixture_parent):
            raise RuntimeError("Fixture cleanup target escaped the test directory")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.texts = {
            "a": "yeah i can do friday, its just a little early for me. we could meet after lunch?",
            "b": "i think its easier if we try the new route first, then decide what actually works.",
        }
        self.items = []
        for sid, text in self.texts.items():
            self.add(sid, text)
        self.save_manifest()

    def add(self, sid, text, **options):
        (self.root / f"{sid}.txt").write_text(text, encoding="utf-8")
        self.items.append({"id": sid, "path": f"{sid}.txt", "kind": "typed", "provenance": "author", "context": {"medium": "message", "audience": "friend", "language": "en"}, **options})

    def save_manifest(self):
        self.manifest = self.root / "samples.json"
        self.manifest.write_text(json.dumps({"samples": self.items}), encoding="utf-8")

    def profile(self):
        p = v.measure(self.manifest, "writer")
        p["traits"] = [{"id": "apostrophes", "category": "spelling", "instruction": "Omit apostrophes in supported informal forms in friend messages.", "state": "observed", "scope": {"medium": "message", "audience": "friend"}, "policy": "preserve", "confirmed": False,
            "support": [{"sample_id": sid, "start": text.index("its"), "end": text.index("its") + 3} for sid, text in self.texts.items()], "counterevidence": []}]
        return p

    def add_rule(self, p, **options):
        p["rules"] = [{"id": "form", "trait_id": "apostrophes", "kind": "forbid", "text": "it's", "severity": "review", **options}]

    def test_measurements_do_not_claim_learned_traits(self):
        p = v.measure(self.manifest, "writer")
        self.assertEqual([], p["traits"])
        self.assertFalse(v.validate_profile(p, self.manifest)["ready"])
        with self.assertRaises(ValueError):
            v.render_profile(p)

    def test_valid_observed_spans_and_counterexample(self):
        p = self.profile()
        p["traits"][0]["counterevidence"] = [{"sample_id": "a", "start": 0, "end": 4}]
        result = v.validate_profile(p, self.manifest)
        self.assertEqual([], result["errors"])
        self.assertTrue(result["source_verified"])

    def test_duplicate_holdout_and_ai_excluded(self):
        self.add("copy", self.texts["a"].upper())
        self.add("hold", "My held out paragraph has a separate topic.", held_out=True)
        self.add("model", "This AI text is for diagnostics.", provenance="ai")
        self.save_manifest()
        p = v.measure(self.manifest, "writer")
        self.assertEqual(2, sum(s["eligible"] for s in p["samples"]))
        self.assertEqual("a", p["samples"][2]["duplicate_of"])
        p["traits"] = self.profile()["traits"]
        p["traits"][0]["support"][1] = {"sample_id": "hold", "start": 0, "end": 4}
        self.assertTrue(v.validate_profile(p, self.manifest)["errors"])

    def test_near_duplicate_is_not_independent(self):
        words = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo twentythree twentyfour twentyfive".split()
        self.assertTrue(v.near_duplicate(words, words + ["extra"]))
        self.assertFalse(v.near_duplicate(words, list(reversed(words))))

    def test_unknown_provenance_cannot_support(self):
        self.items[1]["provenance"] = "unknown"
        self.save_manifest()
        self.assertTrue(v.validate_profile(self.profile(), self.manifest)["errors"])

    def test_unverified_ocr_cannot_establish_spelling(self):
        self.items[1]["kind"] = "ocr"
        self.save_manifest()
        p = self.profile()
        self.assertTrue(v.validate_profile(p, self.manifest)["errors"])
        self.items[1]["surface_verified"] = True
        self.save_manifest()
        self.assertEqual([], v.validate_profile(self.profile(), self.manifest)["errors"])

    def test_dictation_surface_and_vocabulary_differ(self):
        self.items[1]["kind"] = "dictation"
        self.save_manifest()
        p = self.profile()
        self.assertTrue(v.validate_profile(p, self.manifest)["errors"])
        p["traits"][0]["category"] = "vocabulary"
        self.assertEqual([], v.validate_profile(p, self.manifest)["errors"])
        self.assertEqual(1, p["observations"][0]["measurements"]["surface_sample_count"])

    def test_surface_category_cannot_bypass_reliability(self):
        p = self.profile()
        p["traits"][0]["surface_sensitive"] = False
        self.assertTrue(v.validate_profile(p, self.manifest)["errors"])

    def test_excluded_spans_are_not_evidence(self):
        start = self.texts["a"].index("its")
        self.items[0]["excluded_ranges"] = [[start, start + 3]]
        self.save_manifest()
        self.assertTrue(v.validate_profile(self.profile(), self.manifest)["errors"])

    def test_source_mutation_invalidates_offsets(self):
        p = self.profile()
        (self.root / "a.txt").write_text("PREFIX " + self.texts["a"], encoding="utf-8")
        self.assertTrue(any("source metadata changed" in x for x in v.validate_profile(p, self.manifest)["errors"]))

    def test_cross_context_support_rejected(self):
        p = self.profile()
        p["traits"][0]["scope"]["audience"] = "client"
        self.assertTrue(v.validate_profile(p, self.manifest)["errors"])

    def test_rule_cannot_widen_trait_context(self):
        p = self.profile()
        self.add_rule(p, scope={"medium": "message"})
        self.assertTrue(v.validate_profile(p)["errors"])

    def test_invalid_scoped_trait_returns_errors_before_rule_check(self):
        p = self.profile()
        self.add_rule(p)
        p["traits"][0]["scope"] = []
        self.assertTrue(v.validate_profile(p)["errors"])

    def test_unconfirmed_block_is_invalid(self):
        p = self.profile()
        self.add_rule(p, severity="block")
        self.assertTrue(v.validate_profile(p)["errors"])

    def test_mode_normalizes_unprotected_surface_habit(self):
        p = self.profile()
        self.add_rule(p)
        ctx = {"medium": "message", "audience": "friend"}
        self.assertEqual("REVIEW", v.check(p, "it's fine", "faithful", ctx)["verdict"])
        self.assertEqual("PASS", v.check(p, "it's fine", "lightly_edited", ctx)["verdict"])
        p["traits"][0]["confirmed"] = True
        self.assertEqual("PASS", v.check(p, "it's fine", "lightly_edited", ctx)["verdict"])
        p["traits"][0]["state"] = "preferred"
        self.assertEqual("REVIEW", v.check(p, "it's fine", "lightly_edited", ctx)["verdict"])

    def test_explicit_mode_policy_overrides(self):
        p = self.profile()
        self.add_rule(p)
        p["traits"][0]["mode_policies"] = {"adapted": "preserve"}
        self.assertEqual("REVIEW", v.check(p, "it's fine", "adapted", {"medium": "message", "audience": "friend"})["verdict"])

    def test_other_audience_rule_not_applied(self):
        p = self.profile()
        self.add_rule(p)
        result = v.check(p, "it's fine", current={"medium": "message", "audience": "client"})
        self.assertEqual("PASS", result["verdict"])
        self.assertEqual([], result["applied_rules"])

    def test_missing_context_requests_review(self):
        p = self.profile()
        self.add_rule(p)
        result = v.check(p, "its fine")
        self.assertIn("context_missing", [x["code"] for x in result["findings"]])

    def test_explicit_new_audience_does_not_inherit_default_relationship(self):
        p = self.profile()
        p["defaults"]["context"] = {"audience": "friend", "relationship": "friend"}
        p["traits"][0].update(state="preferred", confirmed=True, scope={"relationship": "friend"}, support=[])
        self.add_rule(p, severity="block")
        result = v.check(p, "it's fine", current={"audience": "client"})
        self.assertEqual("REVIEW", result["verdict"])
        self.assertNotIn("relationship", result["context"])
        self.assertEqual([], result["applied_rules"])

    def test_literal_boundaries_do_not_match_inside_words(self):
        self.assertEqual(1, len(v.literal_hits("i can do friday", "i")))
        self.assertEqual(0, len(v.literal_hits("yourself", "your")))
        self.assertEqual(2, len(v.literal_hits("one; two;", ";")))

    def test_new_values_and_omitted_protected_name_block(self):
        hits = v.integrity("Project Cedar costs $40.", "Project Alder costs $50.", ["Project Cedar"])
        self.assertEqual({"exact_value_drift", "protected_text_missing"}, {x["code"] for x in hits})

    def test_modality_and_negation_change_review(self):
        hits = v.integrity("We may ship May 8; we cannot promise Friday.", "We will ship May 8; we promise Friday.")
        self.assertEqual({"possibility", "negation"}, {x["feature"] for x in hits})

    def test_contraction_equivalence_not_negation_drift(self):
        self.assertEqual([], v.integrity("I cannot do this.", "I can't do this."))

    def test_quote_url_and_email_changes_detected(self):
        source = 'He said "later". Email x@example.com; https://example.com/a.'
        draft = 'He said "now". Email y@example.com; https://example.com/b.'
        self.assertEqual({"quotation_drift", "url_drift", "email_drift"}, {x["code"] for x in v.integrity(source, draft)})

    def test_factual_writing_does_not_require_personal_familiarity(self):
        result = v.check(self.profile(), "The protocol uses a checksum to detect transmission errors.")
        self.assertEqual("PASS", result["verdict"])

    def test_new_learning_history_requires_review(self):
        result = v.check(self.profile(), "I recently learned that the protocol uses a checksum.")
        claims = [x for x in result["findings"] if x["code"] == "personal_knowledge_claim"]
        self.assertEqual("REVIEW", result["verdict"])
        self.assertEqual("learning_history", claims[0]["kind"])

    def test_unknown_does_not_justify_claiming_unfamiliarity(self):
        findings = v.knowledge_claim_review("I'm not familiar with distributed databases.")
        self.assertTrue(findings)

    def test_personal_experience_not_invented_during_rewrite(self):
        result = v.check(self.profile(), "In my experience this protocol works reliably.", source="This protocol works reliably.")
        self.assertIn("personal_knowledge_claim", [x["code"] for x in result["findings"]])

    def test_changed_domain_not_whitelisted_by_same_claim_count(self):
        hits = v.knowledge_claim_review("I've worked in neurosurgery for years.", ["I've worked in retail for years."])
        self.assertTrue(hits)

    def test_explicit_author_context_supports_literal_claim(self):
        draft = "I've worked on this protocol for years."
        result = v.check(self.profile(), draft, author_context="I have worked on this protocol for years.")
        self.assertNotIn("personal_knowledge_claim", [x["code"] for x in result["findings"]])

    def test_style_samples_do_not_authorize_expertise(self):
        self.add("claim", "In my experience this protocol works reliably.")
        self.save_manifest()
        result = v.check(self.profile(), "In my experience this protocol works reliably.", samples=v.load_samples(self.manifest))
        self.assertIn("personal_knowledge_claim", [x["code"] for x in result["findings"]])

    def test_research_is_not_attributed_to_author(self):
        hits = v.knowledge_claim_review("My research shows that the device uses less power.")
        self.assertEqual("research_history", hits[0]["kind"])

    def test_routine_acknowledgment_not_expertise(self):
        self.assertEqual([], v.knowledge_claim_review("I know what you mean."))

    def test_phrase_leakage_but_original_reuse_allowed(self):
        p, samples = self.profile(), v.load_samples(self.manifest)
        phrase = self.texts["a"]
        self.assertIn("sample_phrase_overlap", [x["code"] for x in v.check(p, phrase, samples=samples)["findings"]])
        self.assertNotIn("sample_phrase_overlap", [x["code"] for x in v.check(p, phrase, source=phrase, samples=samples)["findings"]])
        self.assertNotIn("sample_phrase_overlap", [x["code"] for x in v.check(p, phrase, samples=samples, allow_phrases=[phrase])["findings"]])

    def test_retrieval_never_falls_back_to_other_scope(self):
        samples = v.load_samples(self.manifest)
        self.assertEqual([], v.retrieve(samples, "friday", {"audience": "client"})["results"])
        self.assertEqual("a", v.retrieve(samples, "friday", {"audience": "friend"})["results"][0]["sample_id"])

    def test_export_omits_raw_sample_corpus(self):
        text = v.render_profile(self.profile())
        for raw in self.texts.values():
            self.assertNotIn(raw, text)
        self.assertIn("apostrophes", text)

    def test_export_preserves_evidence_limits_notes_and_opportunities(self):
        p = self.profile()
        p["limitations"] = ["Client email voice has not been observed."]
        p["traits"][0]["note"] = "Reviewed only it-is opportunities, not possessives."
        p["traits"][0]["opportunities"] = {"matching": 2, "total": 3, "counterexamples": 1}
        text = v.render_profile(p)
        self.assertIn(p["limitations"][0], text)
        self.assertIn(p["traits"][0]["note"], text)
        self.assertIn('"counterexamples": 1', text)
        self.assertNotIn(v.SCAFFOLD_NOTE, text)
        self.assertIn("Research does not establish that a fact is new to the writer.", text)

    def test_preferred_rule_without_corpus_is_explicit(self):
        p = self.profile()
        p["traits"][0].update(state="preferred", confirmed=True, support=[])
        self.add_rule(p, severity="block")
        self.assertEqual([], v.validate_profile(p)["errors"])
        p["traits"][0]["confirmed"] = False
        self.assertTrue(v.validate_profile(p)["errors"])

    def test_invalid_author_and_ranges_rejected(self):
        self.items[1]["author_id"] = "different"
        self.save_manifest()
        with self.assertRaises(ValueError):
            v.measure(self.manifest, "writer")
        del self.items[1]["author_id"]
        self.items[1]["excluded_ranges"] = [[0, 100000]]
        self.save_manifest()
        with self.assertRaises(ValueError):
            v.load_samples(self.manifest)

    def test_opportunity_counts_not_invented(self):
        p = self.profile()
        self.assertNotIn("opportunities", p["traits"][0])
        p["traits"][0]["opportunities"] = {"matching": 3, "counterexamples": 2, "total": 4}
        self.assertTrue(v.validate_profile(p)["errors"])

    def test_cli_pipeline_and_input_exit_codes(self):
        measured = self.root / "profile.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "measure", "--manifest", str(self.manifest), "--profile-id", "writer", "--output", str(measured)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--profile", str(measured), "--manifest", str(self.manifest)], capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        measured.write_text(json.dumps(self.profile()), encoding="utf-8")
        guide = self.root / "voice.md"
        result = subprocess.run([sys.executable, str(SCRIPT), "render", "--profile", str(measured), "--output", str(guide)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(guide.is_file())
        author_context = self.root / "author-context.txt"
        author_context.write_text("I have used Python for years.", encoding="utf-8")
        authored_draft = self.root / "new-draft.txt"
        authored_draft.write_text("I've used Python for years.", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), "check", "--profile", str(measured), "--draft", str(authored_draft), "--author-context", str(author_context)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("PASS", json.loads(result.stdout)["verdict"])
        result = subprocess.run([sys.executable, str(SCRIPT), "check", "--profile", str(measured), "--draft", str(self.root / "a.txt"), "--context", "[]"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)


if __name__ == "__main__":
    unittest.main()
