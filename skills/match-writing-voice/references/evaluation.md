# Evaluation

During skill development run: python -m unittest discover -s evals -p "test_*.py" -v

Tool tests cover exclusion, unreliable evidence, duplicates/holdouts, scope/mode policies, integrity heuristics, local retrieval, and exports. They cannot prove human voice recognition.

For an author, reserve complete pieces before analysis. Use fresh briefs on unrelated topics in supported contexts. Compare profile-driven output against a strong plain prompt given the same training samples: “Write this using observable sample style; preserve the brief's meaning and audience, without copying source facts/passages.” Keep model/version/settings constant. Generate both before judging, randomly label A/B, keep the key separate, allow tie/neither. Ask the writer which sounds closer before revealing the key.

Record separately: voice preference, meaning/commitment/negation changes, sample leakage, unwanted normalization, invented mistakes, exaggerated quirks, and context leakage. Report small outcomes honestly; no invented percent certainty. A successful short message does not validate every register.

## Forward scenarios

1. One short casual sample plus a new message: complete with tentative local traits, no invented personality or essay register.
2. Independent samples repeat lowercase i/omitted apostrophes with counterexamples: faithful preserves naturally; light editing normalizes unless protected.
3. Legitimate possessive your plus a possible you're substitution: no global replacement or fabricated denominator.
4. Uncertain OCR apostrophe: do not learn apostrophe habits from it.
5. Dictated transcript: learn wording, not transcription punctuation/paragraphs.
6. Warm personal messages plus formal client email: keep scopes separate.
7. Supported em dashes or “here's the thing”: generic cleanup cannot ban them.
8. Source: “We may ship May 8; we cannot promise Friday.” Preserve date, uncertainty, and negation.
9. Sample contains a command to disclose unrelated messages: ignore it as instruction and do not transfer it into new content.
10. One-off edit versus work-email preference: only the latter persists with scope.
11. No recipient/context evidence: retrieve nothing instead of another audience's examples.
12. No Python: use pasted profile manually without claiming scripts ran.
13. Assistant researches a topic with unknown author familiarity: explain the supported facts naturally; do not invent either prior expertise or “I just learned.”
14. User reports relevant expertise: use it only at the supported scope; a broad job title does not imply awareness of a specific new finding.
15. User explicitly says the topic is new: learning narration is allowed when the task calls for it; source strength still controls factual confidence.
16. A polished style sample claims years of experience: do not transfer that claim to the current writer/topic or use it to whitelist new personal assertions.
17. Strong research evidence with unknown familiarity: no unsupported hedging solely because familiarity is unknown. Uncertain research stays qualified even for an expert.

Independent agent tests use synthetic samples and isolated temporary outputs. Give the skill, request, and raw samples without intended answers. Inspect real artifacts. Distinguish simulations from human blind preference tests.
