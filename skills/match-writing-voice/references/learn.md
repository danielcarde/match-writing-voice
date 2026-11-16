# Learn and refresh

Use this workflow to create or update a profile from samples, edits, and explicit preferences. For a before-and-after pair, use [paired-edit guidance](learn-from-edits.md) to learn the revision choices. For an explicit reusable preference, record the wording or behavior and its intended context.

Use supplied material; do not require a word quota before helping. More independent examples in the relevant situation are more useful than one long sample. A single sample supports local tentative traits, while explicit preferences can be firm immediately.

Preserve original wording when extracting files/URLs. A summary is not the sample. Use host tools for binary documents and images. Transcribe visible text without normalizing case, grammar, or punctuation. Exclude uncertain OCR characters from surface evidence. If extraction is unavailable, request accessible text rather than inventing it.

Keep each independent piece as one manifest item. `typed` is directly written text; `edited` is substantially author-edited prose in that register; `ocr` has unreliable surfaces until verified; `dictation` supports wording but not spelling/punctuation/paragraph boundaries. `unknown` and `ai` origins cannot establish observed personal habits. If authorship ambiguity changes the target writer, ask once; otherwise preserve unknown provenance.

Exclude quoted replies, other speakers, boilerplate, and uncertain spans using excluded_ranges. Reserve complete held-out pieces before analysis when enough material exists. Never use held-out material to choose traits or examples. Near duplicates count once; the helper's heuristic does not certify originality.

## Analyze and contrast

Use separate passes over words/forms, sentences/rhythm, and passages/reader relationship. Sequential passes are sufficient; delegation is not required.

Examine vocabulary, idioms, contractions, code-switching, case, spelling, tense/agreement/prepositions, punctuation, fragments, sentence variation, coordination, interruptions, paragraph shape, openers/closers, rhetoric, politeness, and stance. Describe behavior, not psychological identity. Analyze languages separately; tokenization and sentence segmentation are heuristic.

For representative passages, create a competent neutral rewrite of the same meaning and compare choices. Compare the writer's own formats and audiences too. Differences are candidate habits, not proof: the neutral rewrite can introduce bias. Separate stable traits, contextual habits, platform constraints, and borrowed templates. A zero count is not “never.”

## Traceable traits

Use [profile-format.md](profile-format.md). Each useful trait needs a usable instruction, scope, state, policy, and natural frequency. Prefer a few distinctive patterns over a catalog of ordinary grammar.

- observed: repeated across at least two independent eligible samples, with reliable surfaces when needed. This minimum is bookkeeping, not statistical certainty.
- tentative: local or inconsistent evidence; apply lightly.
- preferred: explicitly requested behavior, confirmed true.
- rejected: confirmed unwanted behavior, not an observation about the user's own prose.
- unknown: insufficient support; cannot drive generation/checker rules.

Record exact source offsets and contrary examples. For irregular forms, distinguish informal convention, dialect, deliberate preference, possible slip, or unresolved status. Track relevant grammatical opportunities, not mere word totals. For example, only contexts requiring “you're” can count toward a “your/you're” substitution rate. Interpretation is the host model's job, not a regex replacement.

When a short excerpt would help a future draft, label it by writing context and section purpose, such as “Lab report — troubleshooting” or “Technical case study — results and limitations.” Cite the sample and its offsets. Keep the excerpt within eligible author prose, or label a user-selected shared example as group writing. Add examples to the existing guide under “Section examples.” In a JSON profile, use the existing `note` field so the examples carry into the Markdown export. Favor a few distinct examples with a clear use.

## Calibrate and update

For important ambiguous habits, offer short original-style and single-trait-normalized alternatives. Randomize order only if claiming a blinded comparison; allow neither. Preferring the polished variant establishes desired output, not that the original habit never occurred. Do not demand approval for every trait. With no questions requested, preserve reliable patterns and omit unsupported error reproduction.

“Change this once” is local; “I don't use that phrase in work emails” is a scoped reusable preference. Preserve observations alongside newer preferences rather than rewriting history. Add samples without discarding unrelated evidence; keep writers separate.

Create profile.json and render voice.md with tools, or a self-contained Markdown equivalent without them. On refresh, write new measurements to a separate scaffold, merge reviewed existing traits/rules, and validate before replacing the working profile. Do not overwrite learned traits with an empty measurement scaffold. No raw corpus copy is necessary. Finish interpreted traits after measurement, validate support, and demonstrate on a fresh topic. State limitations by feature/context rather than inventing a percent voice match.
