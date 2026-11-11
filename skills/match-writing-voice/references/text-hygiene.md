# Inspect copy/paste text artifacts conservatively

Use this reference only when the user asks about hidden characters, visible copy/paste damage appears, or unusual formatting is relevant to the current prose. It is not a mandatory pass over every draft. The approach is informed by hannsxpeter/humanizer; see [provenance](provenance.md) and [notices](upstream-license.md).

An invisible or non-ASCII codepoint can be ordinary language, math, typography, or display data. Inspect its role before treating it as residue. Do not infer authorship, software origin, or a watermark from it.

## Optional read-only tool

```text
python scripts/voice_tools.py inspect-text --text draft.txt --output hygiene.json
```

This command reads extracted UTF-8 text and reports selected control/format characters, variation selectors, and non-ASCII spaces. It preserves a leading BOM for inspection. The report gives each codepoint's name, kind, count, and first 50 zero-based Unicode character positions; later positions may be omitted while counts remain complete. Offsets are not byte or UTF-16 offsets. The command makes no edits and refuses an output path that aliases the input. It does not assess linguistic intent, protected spans, confusables, semantic equivalence, or authorship. Its report is separate from the voice checker's verdict.

Without tools, inspect only what the interface actually exposes; do not claim a codepoint scan ran. A rendered view may hide or normalize characters before the model receives them.

## Interpret before changing

| Character family | Possible legitimate role | Decision |
|---|---|---|
| Soft hyphen, BOM, zero-width space | Optional wrapping, encoding, script-specific word breaking | Preserve ambiguity; remove only clearly accidental residue in editable prose |
| Joiners and variation selectors | Spelling, glyph choice, emoji sequences | Preserve meaningful sequences; a hit is not a cleanup instruction |
| Direction controls and marks | Mixed right-to-left/left-to-right display | Preserve intended display; do not strip them from multilingual text by default |
| Non-breaking, narrow, or special spaces | Locale punctuation, units, alignment, protected data | Normalize only when the task and layout permit it |
| Invisible math operators, tags, other format controls | Mathematical notation or valid display sequences | Inspect in context and preserve a meaningful role |

Keep exact code, identifiers, URLs, quoted material, tables, signatures, and other protected content unchanged unless specifically placed in scope. Never apply blanket ASCII conversion, Unicode normalization, script substitution, or removal of all zero-width characters. Ordinary accents, curly punctuation, and dashes need no special inspection solely because they are non-ASCII.

If a cleanup is authorized and a candidate is clearly accidental, change only that editable span, then compare the resulting wording, codepoints, and display. Retain uncertain characters and explain a material ambiguity. Do not clean original voice evidence before measuring it: saved offsets/hashes refer to the source, and extraction artifacts should instead be excluded or marked unreliable.

Report only verified changes, such as a specific codepoint removed at an identified location. A clean scan means only that this scan found none of its listed candidate families in the text it received. It does not inspect document properties, container metadata, images, audio, vendor marks, or statistical text signals, and it cannot establish that content is watermark-free.
