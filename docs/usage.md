# Usage

## Learn a voice

Supply authentic samples from the relevant context. Pasted text, local text files, documents, and images can work when the host can extract them accurately. Do not use a summary in place of original prose.

```text
Use Match Writing Voice. These are my messages to friends.
Build a reusable profile. Preserve recurring case, punctuation, and spelling habits.
Mark uncertain patterns instead of treating one typo as a rule.
```

The agent interprets habits, records evidence/context, and creates a profile. A measurement report alone is unfinished. A small sample can still be useful with qualified conclusions.

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

## Review generic phrasing without erasing the voice

Drafts and rewrites receive a brief internal editorial review. It looks for stock framing, filler, inflated emphasis, accidental repetition, and manufactured personality. The matching-context profile and current instructions take priority over generic cleanup: supported **Overall**, repeated topic words, long sentences, or punctuation remain available. A necessary hedge or technical sense is not an automatic finding.

```text
Use Match Writing Voice with my profile. Rewrite this in faithful mode,
then review generic phrasing while preserving my supported habits.
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
