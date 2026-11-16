# Usage

## Update my voice profile

Supply real writing samples, an earlier draft and your revision, or a preference you want to reuse. The assistant records the habits that the evidence supports and where they apply. A before-and-after pair can show how you revise a section. Label shared writing examples so the assistant can use them in the group's voice.

```text
Use $match-writing-voice to update my profile with these lab reports.
Save a short example of how I describe troubleshooting.
```

A one-off correction applies to the current draft. Say “remember this for future client emails” or similar when a preference should become part of the profile. [Learning guidance](../skills/match-writing-voice/references/learn.md)

## Write or rewrite in my voice

```text
Use $match-writing-voice to rewrite this results section in my saved voice.
```

Supply notes to draft new prose or an existing passage to rewrite. The assistant uses the section's purpose to select up to two short examples from your profile or samples. A results example shows how you explain observations and limits. A methods example shows how you explain what was done and why. Current facts and claims come from your notes or draft.

Humanizer reviews every draft and rewrite. It looks for stock introductions, empty recaps, repeated framing, and formulaic transitions. It preserves the rhythm, repetition, and wording that serve the passage in your voice. Rewrites preserve content and structure by default and check exact details such as numbers, units, quotations, and citations.

Use ordinary language to adjust the edit. “Light edits only” keeps wording that already works. “Fix obvious grammar slips” allows those corrections. “You can reorganize the paragraphs” gives the assistant room to move prose while keeping claims with their evidence.

Attach your profile or ask for it by name. On a host with file access, “my saved profile” can resolve through the local catalog. The assistant can ask which profile to use when several fit. [Profile selection and catalog](../skills/match-writing-voice/references/guided-mode.md)

## Ask for feedback or show what changed

Say “tell me what sounds generic” for feedback, or “show me what changed” for a comparison. Ask to save a local edit history if you want copies of the original and revised drafts with the comparison. [Revision review and local tools](../skills/match-writing-voice/references/revision-review.md)

## Inspect unusual text characters

Say “check for hidden characters” when unusual spacing or pasted text needs inspection. Humanizer can run a read-only check and report the characters it finds. The check considers the character's role before suggesting a change. [Text inspection](../skills/match-writing-voice/references/text-hygiene.md)

## Profile tools

Use the [profile format](../skills/match-writing-voice/references/profile-format.md) for local measurement, validation, export, and preservation checks. The skill also supports Markdown profiles in hosts without Python.
