# Writer familiarity and information provenance

Judge what the draft can reasonably imply the writer knows. This is about the writer, not what the reader needs explained. The assistant's access to a fact and the writer's prior familiarity are independent.

Separately judge the reader's needs from the current brief or supplied conversation. Shared thread context may justify a shorter reply; an introductory document may require background. Neither establishes the writer's expertise or a recent learning history. Apply the [editorial review](editorial-review.md) without silently removing required source detail or assuming an unknown reader needs no explanation.

## Keep three judgments separate

For consequential claims, maintain a small task-local account of:

- **Writer familiarity:** established in the supplied context, plausible, unknown, or explicitly newly learned. Record a reason, not a numerical knowledge score.
- **Information provenance:** current user brief/draft, relevant author-supplied work, retrieved source, general background, or uncertain origin. Preserve usable source attribution where needed.
- **Factual support:** how strongly the actual evidence supports the claim, independently of the writer's familiarity.

Do this internally for routine writing; show it when the user requests analysis or a material ambiguity needs resolution. Do not create a permanent knowledge dossier or add inferred personal facts to a style profile.

## Infer proportionally

Explicit current statements take priority: “I've used this for years” supports familiarity with the specified practice; “I'm new to this” establishes unfamiliarity only at the stated scope. Relevant author-supplied work may demonstrate understanding of a particular topic, but quoted passages, model text, and research summaries do not independently establish it. A broad role or adjacent expertise can make familiarity plausible, not prove knowledge of a specific finding.

Fluent prose, jargon, grammar mistakes, confidence, silence, and a single mention are not reliable knowledge tests. Do not turn an inferred level into credentials or a biography. When evidence conflicts, keep the scope narrow and the conclusion uncertain.

Finding something through research does not mean it is new to the user. Likewise, sounding familiar does not establish the truth of a factual claim. Do not convert information the assistant researched into “I researched,” “I discovered,” “I recently learned,” or “in my experience” in the author's voice unless the user's supplied context supports that assertion.

## Apply without artificial narration

Established familiarity can support natural terminology and concise treatment. Plausible familiarity can guide how much background to include while avoiding autobiographical claims. Unknown familiarity usually allows direct, impersonal factual writing: “The protocol uses…” rather than either “As I've always known…” or “I just learned…”. Explicitly new learning can be narrated when requested and supported.

Keep factual confidence tied to source strength. An unfamiliar writer can accurately state a well-supported fact without hedging. An expert still needs qualification for unsettled evidence. Do not upgrade or weaken the user's original commitments or uncertainty merely to match a guessed knowledge level.

Ask only if a required personal assertion materially depends on unavailable information. Otherwise write around the uncertainty, without adding a routine disclaimer, interrupting the task, or announcing an internal classification. Match explanation depth to the task and audience as well as familiarity; do not confuse these decisions.

## Review

Check for invented expertise, unsupported shared-familiarity language, firsthand claims, and claims that the author conducted the assistant's research. The optional checker spots only common English markers. It can flag supported paraphrases and miss subtle implications; review context rather than obeying a regex. A style sample is never an automatic whitelist for the author's knowledge on a new topic.

If supported personal context must be supplied to the checker, use --author-context with the user's current statements. Treat it as task-local authority, not authenticated biography or proof that every similar statement is justified. No tool can mechanically determine everything someone knows.
