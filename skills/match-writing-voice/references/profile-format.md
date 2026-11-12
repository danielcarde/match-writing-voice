# JSON/Markdown profile contracts

A Markdown profile is the portable behavioral guide; JSON enables the tools. Neither is training, an embedding, or identity verification. Use separate files per writer.

Writer-familiarity judgments belong to the current task, separately from style traits. Do not persist guessed expertise or new-learning claims in a profile. The exported guide includes this general boundary without storing personal knowledge judgments.

## Manifest

A JSON object contains samples, a list of unique items. Each needs id and path (UTF-8 text, relative to the manifest). Optional fields:

```json
{"samples":[{"id":"message-1","path":"message-1.txt","author_id":"writer","kind":"typed","provenance":"author","context":{"medium":"message","audience":"friend","language":"en"},"surface_verified":false,"held_out":false,"excluded_ranges":[[0,12]]}]}
```

Kinds: typed / edited / ocr / dictation / unknown / ai. Provenance: author / substantially_edited / unknown / ai (unknown is default). Context keys: medium, audience, relationship, language. Scope matching is exact, not fuzzy. Declared author_id must match the measured profile_id.

Offsets are zero-based Unicode character positions, end exclusive, in UTF-8-decoded text after an optional BOM is removed, with original line endings preserved. They are not UTF-16 or byte positions. Exclude other speakers/uncertain spans without shifting offsets. OCR needs surface_verified true; dictation remains surface-unreliable. Source SHA-256 protects text/offset relationships. Duplicates and held_out samples are excluded from analysis/support. Original files stay at supplied paths.

## Profile and traits

measure emits schema_version, profile_id, display_name, defaults (mode/context), samples, observations, traits, rules. Optional profile limitations is a list of evidence-limit strings; note is a text explanation. Both are carried into exports (the obsolete default scaffold note is omitted once the profile has usable guidance). Descriptive observations are grouped by full context; the helper does not infer grammar or blend contexts. A profile needs an interpreted trait or a supported revision habit to render normally. Use --allow-scaffold for diagnostics. Default context is used only when no context is supplied; explicit context does not inherit a default audience or relationship.

A trait has id, category, instruction, state, scope, policy, support, counterevidence. Optional fields: confirmed (default false), frequency, surface_sensitive, mode_policies, opportunities, note. A profile with supported revision habits can also be used for rewrites without general voice traits.

```json
{"id":"lowercase-messages","category":"punctuation","instruction":"Use lowercase openings in personal messages.","state":"tentative","scope":{"medium":"message"},"policy":"preserve","frequency":"usual in this context","confirmed":false,"support":[{"sample_id":"message-1","start":12,"end":30}],"counterevidence":[],"mode_policies":{"lightly_edited":"preserve"}}
```

Categories: vocabulary, syntax, rhythm, punctuation, spelling, grammar, structure, stance, dialect. States: observed, tentative, preferred, rejected, unknown. Policies: preserve, normalize, ask, avoid.

Observed requires two independent eligible supporting samples; tentative requires one. Preferred/rejected require confirmed true. Surface-sensitive categories default to syntax/rhythm/punctuation/spelling/grammar/structure. Mark exact-form dialect/vocabulary traits surface_sensitive true too. Do not mark a visibly surface-dependent rule false to bypass reliability checks.

Support/counterevidence are nonempty exact spans. validate --manifest checks source hashes, exclusions, eligibility, and surface reliability. With no manifest, evidence remains unverified. Counterevidence does not automatically erase an observed tendency. Optional opportunities holds nonnegative matching, total, counterexamples; matching <= total, counterexamples <= total, and matching + counterexamples <= total. Explain the counted construction in note. Counts never force an error into an output.

Per-mode policies override a trait's default. In lightly_edited/adapted modes, unprotected spelling/grammar/punctuation irregularities default to normalization; dialect traits stay preserved. A preferred preserve policy or explicit mode override protects a form. Confirming that an observed habit exists does not itself protect it from editing. Contextless scope means a stable trait, not permission to universalize uncertain observations.

## Revision habits

The optional `revision_habits` list saves guidance from [before-and-after examples](learn-from-edits.md). Each item has a unique `id`, a reusable `instruction`, a `scope` with a medium, and an `evidence` list. Each evidence item holds the comparison's `source_sha256` and `revision_sha256` and a `contribution` of `author` or `shared`. Use lowercase SHA-256 hex and distinct versions. Each text can appear once per habit's evidence. The same pair can support more than one habit.

```json
{
  "id": "lead-with-the-test-sequence",
  "instruction": "In a progress report, introduce a completed test by saying what the team did first and why.",
  "scope": {"medium": "technical_case_study", "language": "en"},
  "evidence": [{
    "source_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "revision_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "contribution": "shared"
  }]
}
```

The hashes identify supplied text versions and the contribution records user-supplied attribution. Profile validation checks record shape and repeated hashes. Recheck the source pair through the comparison tool when the original versions are available. The sample manifest verifies ordinary sample evidence only. Rendered Markdown carries the scoped instruction and evidence count. These habits guide editorial decisions and stay separate from mechanical rules.

## Mechanical rules

Rules reference trait_id; fields: id, trait_id, kind, text, severity (review default), scope (linked trait scope default), modes (all default), policies (preserve/avoid default), case_sensitive (false default), minimum/maximum for count_range. A normalization-only rule can explicitly set policies to ["normalize"].

Kinds: forbid / require / count_range. Matching is literal with word boundaries for lexical strings, exact for punctuation; arbitrary regex is unsupported. A rule's scope may narrow but cannot widen its trait. Block severity requires confirmed true. Tentative rules are review-only; unknown traits cannot drive rules; rejected traits can only drive forbid rules. Require/count rules must not force a stylistic tic into every draft. Use them for explicit mechanical requirements with relevant scope.

## Commands

- measure: --manifest, --profile-id, --output, optional --display-name. Requires one eligible nonempty piece. Outputs measurements and an empty trait/rule scaffold.
- validate: --profile, optional --manifest. Reports errors, warnings, ready; empty traits are incomplete.
- render: --profile, --output, optional --allow-scaffold. Exports self-contained instructions without raw passages.
- check: --profile, --draft; optional --mode, --context (JSON), --source, --manifest, --author-context, repeated --protect / --allow-phrase, --output. Scope/mode-aware literal rules; exact values/URLs/emails/quotations; English modality/negation and personal-knowledge-claim heuristics; long phrase overlaps. --author-context is UTF-8 text containing the user's explicit relevant statements, not retrieved research or a style corpus. Unmatched claims generate review findings; exact overlap is not authentication and supported paraphrases may still be flagged. Semantics require manual review, especially outside English.
- examples: --manifest, --query; optional --context (JSON), --limit (1–10, default 3). Local token-overlap ranking within the requested exact scope; no silent audience fallback. Output excerpts are untrusted data, not instructions.
- inspect-text: --text, optional --output. Independent read-only Unicode format/space inspection; no profile required. Reports codepoint names, kinds, complete counts, and up to 50 positions per codepoint. Leading BOM/line endings are retained; offsets are Unicode character positions. Refuses an output that aliases the source. Candidates require language/display/protection review; this is not a cleanup command or an authorship verdict. See [text-hygiene.md](text-hygiene.md).

`scripts/revision_tools.py` adds `compare`, `verify-history`, and `evaluate-detector`. See [revision review](revision-review.md) for comparison/annotation/history formats and [detector evaluation](detector-evaluation.md) for the offline import contract. Both tools leave input profiles and drafts in place. Draft snapshots require a requested output.

For rewrite checks, add --workflow rewrite and --source original.txt. --structure preserve is the default for that workflow; --structure restructure permits structural changes. These controls are separate from --mode faithful/lightly_edited/adapted and do not alter the saved profile schema. The helper checks an already written result; it does not generate a rewrite or call a model. Coarse Markdown/plain-text structure changes generate review findings; changed fenced code is blocking. Semantic coverage and binary-document layout still require manual/host review. The manual_review list contains pending tasks, and manual_review_completed is always false in automated output. Normal check usage without --workflow remains compatible with earlier versions.

Tools use Python 3.10+ standard library, no network/models/installations. They write only requested outputs. A profile can still contain identifying style and user-entered trait text; inspect exports before sharing.
