# Usage

## Optional guided picker

Ask:

```text
Use $match-writing-voice in guided mode.
```

Or say “show options” / “open the picker.” The assistant offers unresolved choices for profile, task, editing mode, rewrite depth, and writing context. It skips choices you already supplied. Hosts with a permitted question tool can show native question cards. Other hosts use a short text menu.

```text
Use $match-writing-voice, guided mode, to rewrite this paragraph.
[paragraph]
```

Here the task and source are settled; only remaining choices are needed. A direct request such as “rewrite this using the attached profile, lightly edited” runs without a menu. Ask to show all choices if you want to change an already supplied setting. Canceling ends the pending guided workflow without making changes.

A local user can register profile names in the optional `~/.match-writing-voice/profiles.json` catalog. It contains only IDs, display names, and profile paths; it does not store samples or select a default writer automatically. The assistant reads it only for the requested workflow, checks the chosen path is accessible, and preserves entries unless an update is requested. Fileless chat hosts use attached or pasted guides instead. See the [catalog format and picker behavior](../skills/match-writing-voice/references/guided-mode.md).

## Learn a voice

Supply authentic samples from the relevant context. Pasted text, local text files, documents, and images can work when the host can extract them accurately. Do not use a summary in place of original prose.

```text
Use Match Writing Voice. These are my messages to friends.
Build a reusable profile. Preserve recurring case, punctuation, and spelling habits.
Mark uncertain patterns instead of treating one typo as a rule.
```

The agent interprets habits, records evidence/context, and creates a profile. A measurement report alone is unfinished. A small sample can still be useful with qualified conclusions.

## Learn from your edits

Supply an earlier draft and your rewrite of the same section, and identify the writing context. The earlier draft can be AI-written. You can also name a group rewrite you want to use as a shared example.

```text
Use $match-writing-voice to learn from my edits.
Compare these two versions and save useful revision habits under technical writing in my profile.
```

The profile retains scoped instructions and references to the pair. A single example is provisional. Future rewrites use it where the context fits and check each section for complete facts, citations, and caveats. [Paired-edit workflow](../skills/match-writing-voice/references/learn-from-edits.md)

## Write something new

```text
Use the attached profile in faithful mode.
Write a message saying I can bring the projector Tuesday,
but I need it back by 5 pm. Keep the facts exactly as supplied.
```

For cleanup, request lightly edited mode. For a new audience, request adapted mode. A friend-message profile does not establish a client-email voice; the agent should make a conservative adaptation and avoid claiming otherwise.

## Rewrite existing content

Supply two distinct inputs: the paragraph/essay/document to rewrite and the target profile or voice samples.

```text
Use Match Writing Voice in rewrite mode.
Rewrite the attached essay using my saved voice profile.
Preserve its meaning, arguments, examples, quotations, citations,
and section/paragraph structure. Use faithful editing.
Return the complete rewritten essay.
```

To change organization, say “Allow restructuring, but preserve every argument, example, and caveat.” For cleaner grammar, choose lightly edited mode. For a different audience, choose adapted mode. Rewriting and editing fidelity are independent choices.

Defaults preserve the supplied text's structure and approximate extent. Rewriting does not imply summarizing, researching new material, or learning the target voice from the source. For a selected passage, only that range changes. For a document, request a new output file if desired; actual file/layout support depends on the host.

After the agent writes the result, optionally check it:

```sh
python skills/match-writing-voice/scripts/voice_tools.py check --profile .local/profile.json --source original.txt --draft rewritten.txt --workflow rewrite --structure preserve
```

Replace `preserve` with `restructure` only if you authorized restructuring. The checker flags coarse plain-text/Markdown structural changes, citation-marker loss, changed fenced code, and substantial shortening. Full content coverage, selected-range integrity, and formatted-document layout still require model/host review. It checks a rewrite; it does not generate one.

Say “make minimal edits and show what changed” to keep wording that already works, or “rewrite in my voice and restructure the prose paragraphs” to allow moving, combining, or splitting them. For technical drafts, both check and compare accept `--protect-file protected.json` with a `spans` array of exact strings such as citations, commands, equations, and terms. The checker counts literal occurrences, and the editorial review verifies each one's context.

## Compare revisions and track edits

```text
Use Match Writing Voice to compare this original and revised draft against my profile.
Identify unnecessary paraphrasing, any loss of meaning, and changes to my voice.
Show the actual edits and explain why they help or hurt. Do not change either draft.
```

Add **“Save a local edit history”** and a destination if you want both exact drafts, the comparison, and an integrity index retained. Ordinary comparisons do not create full snapshots. Saved bundles use new directories and refuse to overwrite inputs or an existing bundle. Keep personal drafts, comparisons containing changed text, and profile snapshots outside Git, for example under an ignored `.local` directory.

```sh
python skills/match-writing-voice/scripts/revision_tools.py compare --source original.txt --draft revision.txt --profile .local/profile.json --context '{"medium":"essay","language":"en"}' --output .local/comparison.json
```

The report identifies exact changed spans and measured differences, applicable traits, context-matched baselines, literal rule changes, and narrow preservation checks. Editorial reasons remain separate and can be attached using a hash-bound `--review` file. Meaning and voice require judgment; no score proves that a draft sounds like a particular person. The [comparison and history reference](../skills/match-writing-voice/references/revision-review.md) includes the annotation schema, opt-in snapshot command, and verification procedure.

## Evaluate supplied detector results

```sh
python skills/match-writing-voice/scripts/revision_tools.py evaluate-detector --results .local/detector-results.json --output .local/detector-evaluation.json
```

Import a dated detector run with exact text hashes and known origins. The [benchmark protocol](../skills/match-writing-voice/references/detector-evaluation.md) compares standard, minimal, and paragraph-level editing on held-out drafts. The offline report tracks GPTZero's paraphrasing badge and Turnitin's zero, suppressed, and visible positive scores when supplied. A new external scan requires authorization for the service and text.

## Review generic phrasing without erasing the voice

Humanizer review guides drafts and rewrites from the start. The skill prioritizes fixing stock framing, filler, inflated emphasis, and accidental repetition within the requested scope. It uses the profile to choose how to express the same point. For example, it can drop an **Overall** recap that repeats the preceding sentence and keep **Overall** where it introduces a useful conclusion. Current instructions, confirmed preferences, source meaning, and protected wording govern the edits.

```text
Use Match Writing Voice to rewrite this with my saved profile.
Keep the facts, uncertainty, quotations, and original structure.
```

For feedback without a revision:

```text
Audit this document for generic or AI-associated phrasing using my profile.
Quote justified findings and explain uncertain candidates.
Do not rewrite it, edit the file, or update my profile.
```

Audit is an action, separate from faithful/lightly_edited/adapted editing modes. Cleanup makes justified local edits; broader voice transformation or restructuring needs the corresponding request. Protected quotations, code, tables, URLs, identifiers, and citation data stay intact unless specifically placed in scope. A clean passage can remain unchanged.

This layer synthesizes selected ideas from [Avoid AI Writing](https://github.com/conorbronsdon/avoid-ai-writing/tree/30971f1c50c6412a0c414e8c7b15032a32b21939). It does not install that project's detector, import its entire catalog, or normalize punctuation to a generic house style. Review is model-applied; the Python checker still performs its documented narrow mechanical checks. No word list, score, or successful review proves authorship or guarantees detector acceptance. See the [editorial decision process](../skills/match-writing-voice/references/editorial-review.md).

Existing JSON profiles remain compatible. Re-render one with the updated helper to include the general editorial instructions in its exported Markdown; no new writing samples or retraining are needed.

The review now considers structure and paragraph purpose before word substitution. It distinguishes a supported point obscured by wording from a genuine content gap, preserves useful feelings/recaps/transitions, and checks for invented causes, lost comparisons, or an editor's repeated replacement rhythm. A short reply can rely on supplied reader context; a complete source rewrite still preserves required details. Reader needs remain separate from writer familiarity. A local “keep this” choice stays in force for that span through later passes without silently changing the reusable profile. See the [five-source comparison](editorial-research.md).

## Inspect unusual text characters

When copy/paste spacing or invisible characters matter, use this independent read-only command:

```sh
python skills/match-writing-voice/scripts/voice_tools.py inspect-text --text draft.txt --output .local/hygiene.json
```

It reports selected codepoints with names, kinds, counts, and up to 50 zero-based character positions each. It retains a leading BOM and original line endings, makes no source edits, and rejects an output that aliases the input. No profile is needed. Persian/Arabic joiners, emoji selectors, direction marks, and non-breaking spaces can be legitimate; the report deliberately leaves interpretation to context. It performs no Unicode normalization, character deletion, provenance inference, or watermark test. [Scope and interpretation →](../skills/match-writing-voice/references/text-hygiene.md)

## Set familiarity explicitly when useful

```text
I understand the general topic, but this particular study is new to me.
Use the research to explain the result without implying I conducted it.
```

The skill keeps familiarity, information provenance, and factual support separate. It can make bounded inferences when context supports them, but unknown familiarity does not require hesitant factual prose. Research by the assistant does not establish that the writer just learned the information.

## Correct and refine

“Change this sentence” is local. “I avoid that phrase in work emails” is a scoped reusable preference. A correction should not silently become a global ban.

## Optional tools

From the repo root:

```sh
python skills/match-writing-voice/scripts/voice_tools.py measure --manifest examples/synthetic/samples.json --profile-id synthetic-friend --output .local/profile.json
```

This creates a measurement scaffold at `.local/profile.json`. Have the agent add interpreted, evidenced traits to that same file before continuing. Validation intentionally reports not ready while its trait list is empty. Once the profile is complete:

```sh
python skills/match-writing-voice/scripts/voice_tools.py validate --profile .local/profile.json --manifest examples/synthetic/samples.json
python skills/match-writing-voice/scripts/voice_tools.py render --profile .local/profile.json --output .local/voice.md
```

Add interpreted traits to the scaffold before validation can report ready. For a complete synthetic mechanics demonstration, run `python tools/demo.py` instead. It creates an explicitly interpreted fixture profile without claiming automatic voice learning.

The full manifest, trait, and rule contracts are documented in [profile-format.md](../skills/match-writing-voice/references/profile-format.md). The agent can follow the workflow manually when Python is unavailable.
