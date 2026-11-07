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
