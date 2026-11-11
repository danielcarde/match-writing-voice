# Changelog

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
