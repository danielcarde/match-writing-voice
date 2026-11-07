# Repository design research

Snapshot: November 6, 2026. Popularity here means GitHub stars at inspection time, not skill installations, quality, or a universal ranking. A GitHub search for agent skills with more than 10,000 stars supplied candidates; additional official/related projects were selected for their packaging relevance.

| Repository | Stars at snapshot | Relevant pattern |
|---|---:|---|
| [mattpocock/skills](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/README.md) | 316,862 | Fast installation by host, an obvious starting task, and a separated skill catalog. |
| [obra/superpowers](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/README.md) | 313,685 | Per-host setup routes, release notes, contributor surfaces, and plugin wrappers around shared skills. |
| [anthropics/skills](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/README.md) | 188,229 | Self-contained skill folders, progressive references/scripts, a concise explanation of the format, and a marketplace. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/README.md) | 78,957 | Clear skill categories and contributor guidance; useful discovery reference rather than runtime architecture. |
| [blader/humanizer](https://github.com/blader/humanizer/blob/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0/README.md) | 65,702 | Concrete writing examples near the top and explicit Claude/Codex/other-agent setup routes. |
| [vercel-labs/skills](https://github.com/vercel-labs/skills/blob/d3701c11b1101251af14c9d148f026e1a47ebe17/README.md) | 38,403 | Agent/path compatibility table, installation reference, and separation of installer behavior from skill behavior. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/README.md) | 33,649 | Small shared skill folders with a simple installation section and discovery structure. |
| [openai/skills](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) | 28,558 | Historical skills example; its inspected README marks it deprecated and points to openai/plugins. |
| [openai/plugins](https://github.com/openai/plugins/blob/d420d13051bffe4543ed39e30fa46b87148e47dd/README.md) | 7,790 | Current official plugin wrappers and repo marketplace layout. |

## Choices in this repository

- One canonical skill under `skills/match-writing-voice`; thin host wrappers rather than divergent copies of the writing method.
- A README that explains the outcome, offers an immediate installation route, shows a concrete writing example, and links deeper guides.
- Native Codex, Claude, and Gemini CLI paths distinguished from a plain-chat Markdown fallback. Documented compatibility is labeled separately from live-host testing.
- A local standard-library installer with a preview and refusal to overwrite existing copies; native/third-party installers remain optional alternatives.
- Reproducible distributions, checksums, a synthetic demo, cross-platform CI, contribution templates, and versioned release notes.
- Private repository access as requested. No public marketplace submission, invented popularity badges, or third-party affiliation claims.

No repository's branding, README prose, or runtime implementation was copied. These are design patterns adapted to this project's narrower task. Skill-level conceptual influences are tracked separately in the provenance reference.

## Source scope

Inspected repository metadata, directory trees, READMEs, and selected marketplace/plugin/contribution/agent-reference files. Exact revisions are recorded in [repository-sources.json](repository-sources.json). The initial GitHub search was a candidate-discovery query, not a claim that every high-star repository was audited.

Official host documentation, linked in [compatibility.md](compatibility.md), determines current native paths and setup behavior. `openai/skills` was retained as a historical comparison; its deprecation is why the optional Codex wrapper follows `openai/plugins` and current documentation instead.

GitHub Actions are pinned to commit revisions resolved from published action releases at inspection time. Automated mechanics/packaging tests and the synthetic demo do not establish model-independent author recognition.
