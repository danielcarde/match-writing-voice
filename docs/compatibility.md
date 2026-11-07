# Compatibility and validation

Checked against official documentation on November 6, 2026. The canonical package follows the Agent Skills structure: `SKILL.md`, optional references, and optional scripts. Its shared description stays under 200 characters for the more restrictive documented upload route.

| Host | Native integration | What this repo validates |
|---|---|---|
| Codex | Skills and optional plugin/marketplace wrapper | Source/tool checks and a synthetic skill application exercise |
| Claude Code | Skills; optional plugin wrapper | Paths, manifests, package structure; not a live model run |
| Claude web/desktop | Custom skill ZIP upload | Root folder/name, metadata, linked resources; not a live upload |
| Gemini CLI | Agent Skills and optional extension wrapper | Paths, manifests, source/archive consistency; not a live model run |
| Other assistants | Native format if supported; otherwise portable guide | Self-contained guide and working internal references |

**Runtime:** helpers require Python 3.10+ and only the standard library. No network/model/API calls are made by those helpers. A host without Python can still use the instructions manually. OCR and binary document extraction rely on host capabilities.

**Behavior:** models can interpret the same guide differently. Deterministic checks do not establish writer recognition, full meaning equivalence, or what someone knows. Use a real writer's held-out examples and blinded preference evaluation for stronger voice evidence.

**Private access:** installing from this repository's URL requires authorized Git credentials. Uploading an asset to another provider is a separate action from cloning the repo; review which samples/profile you provide to that host.

## Primary sources

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI: Package a plugin](https://developers.openai.com/plugins/build/plugins)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [Claude: Use custom skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Claude: Create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Gemini CLI: Agent Skills](https://geminicli.com/docs/cli/skills/)
- [Gemini CLI: Extension reference](https://geminicli.com/docs/extensions/reference/)

These document native host support. They do not certify this project or its writing quality.
