# Conceptual provenance

Original implementation; no upstream scripts or instruction passages were copied. These links record design influences, not endorsement:

- [Hiro-Inagawa/write-like-me](https://github.com/Hiro-Inagawa/write-like-me/tree/91acc42eaf791649ef7894071956d7b09e56934e): measurement, named profiles, scoped checking, checker evaluation.
- [HopLittleBunny/write-like-me](https://github.com/HopLittleBunny/write-like-me/tree/1c697ddcaad8540dfced94f5906abd78a7646e5b): provenance, evidence states, dictation limits, integrity checks, strong baseline.
- [docwriter-org/style](https://github.com/docwriter-org/style/tree/7dc0fc4a08900d8b4ead0803d7a8772b46cce989): traceable support, several analysis scales, contrast calibration. No code copied from this repo, whose inspected revision had no identified root license.
- [shyam-ganapathy/write-like-me](https://github.com/shyam-ganapathy/write-like-me/tree/e97af8d201791b32f94c20052ac17f9a04397c59): same-content contrasts, audience/format conditioning, templates separated from voice, personal habits over generic cleanup.
- [robyroro/PersonaMCP](https://github.com/robyroro/PersonaMCP/tree/52d546dc43d497be51ed5933786be20d7a08a24d): context-matched local examples and spelling/case fidelity without artificial mistakes. No MCP server/database included here.
- [social-media-skills/voice-builder](https://github.com/social-media-skills/skills/tree/f28cef2b7067ec64e79c9d85421c022c06659e03/skills/voice-builder): distinctive operational traits, stance/rhetoric, fresh-topic tests.
- [lovstudio/style-clone-skill](https://github.com/lovstudio/style-clone-skill/tree/ed78e466117885e934fe92cdca54e623c3a66c8a): direct analyze/profile/rewrite flow and restructuring control.

Integrated additions: faithful/edit/adapt modes; hashed source spans; OCR uncertainty/exclusions; counterevidence/opportunity records; no forced quota; no-tools Markdown use. Analysis remains heuristic, not a grammar parser/dialect classifier. OCR relies on host capability. No training, account memory, or automatic cross-host installation is implied. Human evaluation is still needed for actual recognition.

Writer-knowledge guidance was added from the user's requested refinement: task-local familiarity inferences are separate from research provenance and factual support. Optional draft checks flag common personal knowledge/experience/learning claims without pretending to determine what someone knows.

## Editorial integration — 2026-11-10

At the user's request, [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing/tree/30971f1c50c6412a0c414e8c7b15032a32b21939) informed the original [editorial review](editorial-review.md): candidate-versus-finding judgment, audit-only behavior, authorized scope, protected regions, context exceptions, bounded revision, honest execution claims, and resistance to generic polishing. Inspected the canonical skill and pattern catalog, plus its voice-preserving rewriter, preservation verifier, false-positive reviewer, license, and attribution notice. The upstream notice credits Mamdouh Aboammar (imMamdouhaboammar) for the focused workflow packaging.

The synthesis uses the evidence-backed personal profile to guide repairs to justified editorial findings. The review is model-applied and uses context to evaluate vocabulary and typography. The [MIT license notice](upstream-license.md) accompanies the source acknowledgment.

## Multi-skill editorial synthesis — 2026-11-10

Further original guidance draws on:

- [blader/humanizer](https://github.com/blader/humanizer/tree/b48c832f0f809c1b5658edbb838c2521b72f2413): structure-first review, repeated setup, reader context, and checks for lost details. This is a newer revision than the repository's original presentation-research snapshot.
- [isatimur/de-slop](https://github.com/isatimur/de-slop/tree/4349a8af4116d6f02b38d62f4b19e66108c4aada): wording versus missing substance, content-grounded sharpening, restraint, and stable no-op behavior. Inspected the skill, rubric, guardrails, and license.
- [milock/humanizer](https://github.com/milock/humanizer/tree/ec66c203c0400481819fda9cb17a6f1c7977c975): publisher/channel conditioning, calibration, local keep/stet handling, and purpose-aware content gaps. Inspected the skill, channels, voice-calibration reference, and license.
- [hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer/tree/e8f1248a7d4919689c1f942e356ed95b102d9f07): overcorrection veto, editor-imposed rhythm, subtle relationship drift, and conservative character inspection. Inspected the skill, do-not-flag and text-hygiene references, and license.

All five editorial sources have retained [MIT notices](upstream-license.md). No implementation, instruction passage, or complete pattern catalog is copied. The optional read-only Unicode inspector is original Python code. It reports codepoints without removing them or claiming linguistic intent. No numerical humanness score, model-attribution heuristic, automatic rewrite threshold, fixed variance target, or assumed permission to invent stance is adopted. Concepts shared across these repositories do not represent independent empirical validation.

## Revision review and detector evaluation — 2026-11-11

- [AICL](https://github.com/ahafarag/aicl/tree/a1ae2092c40530f40e00a5dab98ea140f0d16b58): same-method before/after measurement, descriptive lexical/rhythm metrics, and explicit uncertainty about detector judgments.
- [PADBen](https://github.com/JonathanZha47/PadBen-Paraphrase-Attack-Benchmark/tree/2bdc624b6536f63dbf90a10486aa6dc0b554d135): separate original authorship from paraphrase conditions; preserve known origin labels and compare matched examples.
- [RAID](https://github.com/liamdugan/raid/tree/e8e23308f9f07a667ae8123b4d2bc8049bc61f84): held-out evaluation across model/genre conditions, known-human controls, and explicit reporting of error denominators.

The [comparison and history tools](revision-review.md) and [detector-results import](detector-evaluation.md) are original standard-library implementations. No upstream code, instruction passages, dataset rows, classifier, or provider integration was copied or bundled. Pinned research sources inform methodology; they do not measure this skill's effect on a current detector. Report edits, editorial judgment, and supplied detector outcomes separately.
