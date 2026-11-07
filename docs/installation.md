# Installation

Choose one route per assistant to avoid duplicate copies of the same skill. This repository is private, so authenticate Git before cloning or installing from its URL. Release assets are visible only to accounts with repository access.

## Local installer — Windows, macOS, Linux

After cloning, use Python 3.10+:

```sh
python tools/install.py --agent codex --scope user --dry-run
python tools/install.py --agent codex --scope user
python tools/install.py --agent claude-code --scope user
python tools/install.py --agent gemini-cli --scope user
```

Select project scope to install into a particular working folder:

```sh
python tools/install.py --agent codex --scope project --project /path/to/project
```

Quote paths containing spaces. The installer lists the target and refuses existing destinations. It does not configure accounts, install a model, or modify unrelated settings. Preserve local changes before manually replacing a previous copy.

| Assistant | User destination | Project destination |
|---|---|---|
| Codex | `~/.agents/skills/match-writing-voice` | `.agents/skills/match-writing-voice` |
| Claude Code | `~/.claude/skills/match-writing-voice` | `.claude/skills/match-writing-voice` |
| Gemini CLI | `~/.gemini/skills/match-writing-voice` | `.gemini/skills/match-writing-voice` |

Existing Codex setups may also discover legacy/custom skill roots. The installer follows the current documented `.agents/skills` location. Avoid installing both there and in another discovered root.

Gemini CLI can also discover the shared `.agents/skills` directory. If your Codex installation there is already visible to Gemini, you do not need a second copy in `.gemini/skills`.

## Codex

After local installation, ask:

```text
$match-writing-voice Build a profile from these samples and draft in faithful mode.
```

This repo also includes an optional Codex marketplace wrapper. Add the repo as a marketplace, then select its plugin in the host's plugin interface:

```sh
codex plugin marketplace add danielcarde/match-writing-voice
```

Use either the plugin or a copied skill, not both. Marketplace features vary by client; local skill installation is the straightforward fallback. [Official skills documentation](https://learn.chatgpt.com/docs/build-skills), [plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Claude Code

Use the local installer above, then `/match-writing-voice`. Or, in Claude Code, install the repo marketplace:

```text
/plugin marketplace add danielcarde/match-writing-voice
/plugin install match-writing-voice@match-writing-voice-marketplace
```

The plugin's command is namespaced: `/match-writing-voice:match-writing-voice`. Private repository access must be available to Claude Code's Git environment. [Official skills guide](https://code.claude.com/docs/en/skills), [plugin guide](https://code.claude.com/docs/en/discover-plugins).

## Claude web / desktop

1. Download `match-writing-voice-claude.zip` from the private release.
2. Enable code execution/file creation if required by your account.
3. Open **Customize → Skills → + → Create skill → Upload a skill**.
4. Upload the ZIP and enable it.

Then ask Claude to use **Match Writing Voice** with your samples. The ZIP contains a single correctly named skill folder, a short description, references, and standard-library Python helpers. Account/organization policies can affect availability. [Official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Gemini CLI

Use the local installer, or Gemini's native install command:

```sh
gemini skills install https://github.com/danielcarde/match-writing-voice.git --path skills/match-writing-voice
```

You can also install directly from the cloned skill directory:

```sh
gemini skills install ./skills/match-writing-voice
gemini skills list
```

In a running session, `/skills reload` refreshes discovery. Ask to use Match Writing Voice and follow Gemini's activation consent prompt. These commands target **Gemini CLI**, not the consumer Gemini chat app. [Official skill management](https://geminicli.com/docs/cli/skills/).

An optional extension wrapper is included as well: `gemini extensions install https://github.com/danielcarde/match-writing-voice`. Use the extension or a standalone skill installation, not both. Its context file is a short runtime note; repository development instructions are kept separate.

## Other agents / chats

For agents supported by Vercel's Skills CLI:

```sh
npx skills add danielcarde/match-writing-voice --skill match-writing-voice
```

That is an optional third-party installer with its own prerequisites; it is not needed for the bundled Python route. [Installer documentation](https://github.com/vercel-labs/skills).

For a chat without skill installation, attach or paste `match-writing-voice-portable.md` and request that workflow. Supply the saved writer profile again when needed in a new environment. This route conveys instructions; it does not add unavailable execution tools or permanent account memory.
