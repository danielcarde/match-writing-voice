# Compare revisions and keep an edit record

Use when asked to compare an original and revision, assess voice drift, explain edits, or save draft history. Ordinary rewrite review still applies; it need not create a report file or retain full text. Use the exact original and actual candidate or final revision. Do not invent a before version, reuse a stale draft, or treat a plan as an edit that happened.

## Compare meaning and voice separately

1. Resolve the original, revision, requested scope, mode, context, and profile. Use context-matched author-supplied samples or saved observations; show that a baseline is missing or not reverified when appropriate. Never pool unrelated writers or registers to invent a target.
2. Read the exact changed spans and surrounding paragraphs. Check facts, quantities, negation, uncertainty, claims, relationships, protected content, and unchanged regions. A whitespace-only change may still affect display or meaning. Reconcile findings with any explicitly authorized content correction.
3. Compare the draft with the applicable trait instructions and actual support/counterevidence. Describe lost repetition, rhythm, plain wording, or other specific supported habits. A count can surface a change, but it cannot judge whether it weakens the voice or whether an edit was necessary.
4. Give each material edit a reason grounded in the current task. Distinguish purposeful voice/clarity/grammar/format edits, authorized content changes, unnecessary paraphrasing, and unresolved changes. For an audit, recommend reversions without changing the text. If rewriting is authorized, correct meaningful failures and compare the actual final versions again. Do not keep rerunning a detector to choose words.

## Local comparison tool

```text
python scripts/revision_tools.py compare --source original.txt --draft revision.txt --profile profile.json --context '{"medium":"essay","language":"en"}' --output comparison.json
```

Use extracted UTF-8 text. `--profile` accepts a structured JSON profile. A Markdown-only guide can be applied manually while the tool measures both texts. `--manifest` requires its corresponding profile and revalidates its exact evidence. Baselines use eligible context matches grouped by full context. Supply a real context or use the profile's configured default. The [rewrite guide](rewrite.md) explains `--protect-file` and `--protect` for checking exact spans. `--mode`, `--structure`, and `--author-context` use the corresponding rewrite settings. Structure defaults to preserve.

The report contains exact source/revision hashes; separate declared origins; before/after counts, rhythm, punctuation, and lexical diversity; applicable traits and literal rule changes; narrow preservation checks; and the actual edit blocks with zero-based, end-exclusive Unicode spans. The diff accounts for whitespace, BOM, and line endings. Its alignment may group several changes; it is not the only valid minimal diff. Inputs over 100,000 whitespace/non-whitespace units per text require smaller comparison sections. Do not describe partial sections as the complete document.

Treat the numbers as descriptive. Sentence segmentation is heuristic; TTR is length-sensitive; a 50-token moving average of TTR is omitted for shorter texts. Matching a statistic is not the same as matching a writer. A mechanical `PASS` leaves editorial judgments pending. Compare exits 1 on a mechanical block, 0 otherwise, and 2 on invalid input. A user-provided correction may require separate interpretation; do not conceal a literal difference by altering the check report.

## Attach the actual editorial review

Do the requested review rather than delivering an unreviewed scaffold as a verdict. For a machine-readable annotation, supply this schema with `--review review.json` after inspecting the comparison:

```json
{
  "schema_version": 1,
  "comparison_id": "copy the ID from the exact comparison report",
  "reviewer": "model",
  "meaning": {"status": "preserved", "reason": "The source's possible Tuesday meeting and 5 pm closing time remain."},
  "voice": {"status": "weakened", "reason": "The requested recap marker was dropped without a clarity benefit."},
  "edits": [
    {"id": "edit-0001", "decision": "revert", "purpose": "unnecessary", "voice_effect": "weakens", "reason": "Removed the supported recap in this context.", "trait_ids": ["recap"]}
  ]
}
```

Choose `reviewer` as `human`, `model`, or `both` according to who actually reviewed. Meaning status: `preserved`, `changed`, `needs_review`. Voice: `consistent`, `weakened`, `insufficient_evidence`, `needs_review`. Edit decisions: `keep`, `revert`, `review`. Purposes: `voice`, `clarity`, `grammar`, `format`, `authorized_content_change`, `unnecessary`, `uncertain`. Voice effects: `supports`, `neutral`, `weakens`, `uncertain`. Cite actual applicable trait IDs when relevant; use an empty list when no trait evidence supports the judgment. Unknown or repeated IDs and stale comparison IDs are rejected. Coverage is partial until every edit and both summaries are accounted for. Complete coverage does not mean the revision passed. Annotations never override mechanical findings or independently verify authorship.

Without the tool, compare visible before/after spans manually, mark conclusions as model/human judgment, and state what was not mechanically checked. Preserve the original during any authorized in-place edit; make no source changes for a comparison-only or audit-only request.

## Save history only when requested

Use `--history-dir` with a new user-chosen directory, or a clearly stated local workspace destination such as an ignored `.local/writing-history/run-name`. It records exact UTF-8 original/revision snapshots, the comparison with actual edits/review, an optional canonical JSON profile snapshot, and a hash index. It never overwrites an existing bundle or an input. Set `--source-origin` and `--draft-origin` from the actual workflow (`human`, `ai`, `ai_assisted`, `unknown`); unknown is the default. Do not label an AI rewrite as human-only because it matches a profile.

```text
python scripts/revision_tools.py compare --source original.txt --draft revision.txt --profile profile.json --context '{"medium":"essay","language":"en"}' --review review.json --history-dir .local/writing-history/run-name
python scripts/revision_tools.py verify-history --history-dir .local/writing-history/run-name
```

Use identical versions/settings, including origin labels, for the initial comparison and its review. `verify-history` checks snapshot bytes against the local index. It is an integrity check, not a tamper-proof or independently authenticated authorship record. Comparisons include excerpts of changed text; keep reports and retained originals in the requested private location. The tool does not copy a sample corpus, edit source files, or send text over the network. Use [detector evaluation](detector-evaluation.md) only as a separate requested action.

This records differences between supplied versions, not keystrokes or undocumented intermediate edits. For binary documents, keep the original file separately: the helper snapshots extracted text, not document layout or metadata. Give the user a concise, readable summary of meaning, voice, and important edits; provide the exact report/history artifact when requested.
