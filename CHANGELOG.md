# Changelog

## 0.10.6

- Check that rewrites preserve the force of technical claims and the full notation of statistical comparisons.

## 0.10.5

- Compare two approaches on difficult rewrites and choose the best voice match after checking the source claims and details.

## 0.10.4

- Learn a writer's order of explanation from samples and revisions, then apply it in matching report sections and emails.

## 0.10.3

- Recast awkward technical sentences around their main point and check that quantities, qualifiers, and neighboring details survive the rewrite.

## 0.10.2

- Added Humanizer guidance for unpacking dense technical prose while preserving technical terms, evidence relationships, and limits.

## 0.10.1 — 2026-11-16

- Made creating a voice profile from scratch explicit in the skill, starter prompt, and usage guide.

## 0.10.0 — 2026-11-15

- Combined profile learning and updates, and combined drafting and rewriting into one workflow with Humanizer review.
- Simplified profile selection and made ordinary editing instructions the default interface.
- Matched short voice examples to the section's purpose and checked source details before delivering rewrites.
- Kept hidden character inspection within Humanizer and moved detector benchmarking guidance to the maintainer docs.

## 0.9.0 — 2026-11-11

- Added Learn from my edits for scoped revision habits drawn from before-and-after pairs, including user-selected shared examples.
- Added validation and portable export of revision habits and a section-by-section coverage review for rewrites.

## 0.8.0 — 2026-11-11

- Added selectable minimal edits and paragraph-level restructuring alongside standard rewrites.
- Added exact protected-span inventories and occurrence checks to the rewrite checker and comparison reports.
- Added a held-out rewrite benchmark protocol and separate tracking for GPTZero's paraphrasing badge and Turnitin's score states.

## 0.7.0 — 2026-11-11

- Made Humanizer review a default priority for planning and checking drafts and rewrites.
- Used matching-context voice evidence to repair formulaic phrasing while preserving source meaning, protected wording, and purposeful voice habits.

## 0.6.0 — 2026-11-11

- Added reproducible original/revision comparisons with exact edit spans, descriptive measurements, applicable voice evidence, matched-context baselines, and narrow preservation checks.
- Added version-bound editorial annotations for edit reasons, unnecessary paraphrasing, and voice/meaning judgments, kept separate from mechanical checks.
- Added opt-in local history with exact draft snapshots, an optional profile snapshot, hash verification, and overwrite protection.
- Added offline import of named, dated detector results, with exact text hashes, separated origin groups, duplicate handling, uncertainty, and optional paired label transitions. No external scans or detector-performance claims are bundled.

## 0.5.0 — 2026-11-10

- Added opt-in guided mode (“show options” / “open the picker”) for unresolved profile, task, editing-mode, and context choices. Direct requests stay direct; known inputs are reused.
- Uses permitted host question controls with a short text-menu fallback, actual-answer waiting, cancellation, and no automatic source/profile mutation.
- Added an optional user-local profile catalog convention for named selection without packaging personal paths or samples. Selection is chat/task-local and does not create a persistent default.
- Included guided instructions in native/portable distributions and broadened package checks to every reference route. No new CLI flags or graphical app are introduced.

## 0.4.0 — 2026-11-10

- Compared Humanizer, Avoid AI Writing, De-Slop, and two related Humanizer skills at pinned revisions, retaining all five MIT notices and documenting adopted/omitted choices.
- Added structure-first, purpose-aware review: wording versus material content gaps, reader context separate from writer familiarity, smallest justified edit depth, local keep/stet handling, and checks for soft inference and editor-imposed uniformity.
- Added optional `inspect-text --text ... --output ...`: an original read-only Unicode codepoint report with exact offsets, bounded position lists, and input/output alias protection. It does not normalize text, judge linguistic roles, or infer authorship/provenance.
- Carried the general review into portable profile exports and all packages while preserving existing profiles, editing modes, source fidelity, and checker verdict behavior.

## 0.3.0 — 2026-11-10

- Integrated a profile-aware editorial review informed by Avoid AI Writing, with pinned provenance and the upstream MIT notice.
- Added candidate/context/protection checks, audit-only behavior, justified local cleanup, bounded review, and no-op handling without overriding supported vocabulary, rhythm, repetition, or imperfections.
- Included the review in writing/rewrite guidance, standalone profile exports, portable guides, and native packages. Existing profile schemas and checker verdicts remain compatible.
- Kept review model-applied: no upstream detector, global blacklist, typography quota, authorship score, or detector-acceptance guarantee is bundled.

## 0.2.0 — 2026-11-09

- Added an explicit rewrite workflow for paragraphs, essays, documents, and selected passages.
- Preserves content coverage and original structure by default, with opt-in restructuring separate from editing fidelity.
- Added optional `check --workflow rewrite --structure preserve|restructure`, with required source text, coarse structure/citation review, fenced-code protection, and substantial-shortening review.
- Included rewrite guidance in standalone profile exports and all portable distributions; existing profiles and ordinary checker usage remain compatible.
- Added targeted behavior and CLI tests. Structure heuristics do not prove complete meaning coverage or binary-document layout fidelity.

## 0.1.0 — 2026-11-06

- Evidence-backed profiles with exact source spans, source hashes, exclusions, and counterexamples.
- Faithful, lightly edited, and adapted modes; scoped habits and explicit preferences.
- Task-local writer-familiarity guidance distinct from research provenance and factual support.
- Optional measurements, local example retrieval, profile export, and narrow draft checks.
- Shared skill format and setup routes for Codex, Claude, Gemini CLI, and portable chat use.
- Reproducible builds, synthetic examples, contribution guidance, and cross-platform CI.

Tool tests and synthetic exercises do not establish real author recognition. See the compatibility and evaluation documentation for validation boundaries.
