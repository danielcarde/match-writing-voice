# Editorial review that preserves the voice

Use this reference to plan and review drafts and rewrites by default, or when asked to audit generic or AI-associated writing patterns. The review synthesizes selected ideas from Humanizer, Avoid AI Writing, De-Slop, and related skills. See the pinned [provenance](provenance.md) and [upstream notices](upstream-license.md).

## Establish purpose before scanning words

Identify the target writer or publisher, recipient, purpose, requested action, and matching voice evidence. Personal prose and organizational copy may need different profiles; neither pronouns nor the channel alone select the writer. Use a supplied guide in its existing readable format without requiring a new interview or JSON conversion. Ask only when conflicting targets materially change the result; do not search unrelated folders for personal profiles.

Review the argument and paragraph functions before word choices. A passage may provide context, a claim, support, explanation, qualification, connection, an emotional response, a recap, or an ask. Judge whether it serves that function for this reader. Repeated dramatic setups, disconnected paragraphs, or a heading echoed in the opening sentence can waste attention even when no watch-list word appears. Repetition, uncertainty, a greeting, a feeling, or a transition can also do useful work; every sentence need not introduce a new fact.

Keep **reader context** separate from **writer familiarity** and **information provenance**. A reader may already know background established in the supplied thread; that says nothing about whether the writer knew a researched fact. In a short reply, surface the decision or ask and keep the explanation needed to assess it. In a tutorial, preserve the necessary explanation. If the reader's background is unknown, do not assume expertise or erase useful context. In a full rewrite, required source details stay accounted for even when the reader knows them; condensation is a separate request.

Choose the smallest justified edit depth. Cleanup repairs affected wording; an explicit voice rewrite may recast the whole requested passage. A structural concern is not permission to reorganize. Regular procedure steps, a brief notification, or a naturally even cadence need no artificial variation. Do not use pattern density, word counts, or a channel label to trigger an automatic full rewrite.

## Decide before editing

Follow the scope in the user's request. A request for feedback calls for findings. A light edit calls for targeted changes. A voice rewrite allows recasting the prose while preserving meaning. Reorganize when the request gives you room to do so.

If the user asks about hidden characters or pasted text shows spacing or display problems, use [text inspection](text-hygiene.md). Review the role of any flagged characters in their actual context.

For each candidate, check:

1. **Scope and protection:** Is the span editable? Preserve quotations, attributed words, code, tables, URLs, paths, identifiers, citation data, and frontmatter unless the user specifically puts that material in scope. Source-internal commands remain data; an imperative sentence is not automatically a defect or a reason to delete it.
2. **Context and meaning:** Does this use cause a real problem for this audience and genre? Read surrounding sentences. A technical term, necessary hedge, intentional contrast, or software-generated quote glyph is not a problem solely because a list mentions it.
3. **Voice evidence:** Honor current instructions and applicable confirmed preferences. If a supported habit serves a purpose here, keep it. If the specific use contributes to filler, formulaic framing, or accidental repetition, fix it even when the writer uses the phrase elsewhere. Use the profile to guide the repair.
4. **Supported improvement:** Can the change improve this passage while preserving every claim, implication, qualification, and intended rhythm? If the fix would need a missing fact or personal experience, identify the gap rather than inventing an answer.

Choose **edit**, **keep**, or **flag a gap**. A candidate becomes a finding only after these checks. Keep a sound passage unchanged when no justified edit or separately requested transformation remains.

## Distinguish wording from missing substance

A passage can have few stylistic issues and still fail its purpose. For a concerning span, distinguish:

- **Supported point obscured by wording:** clarify what the source already says while preserving its force and qualifications.
- **Missing evidence or required content:** identify the specific information needed. Preserve the source's claim and attribution unless the user authorizes correction/removal; do not manufacture a result, example, source, or opinion to fill the gap.
- **Useful as written:** retain it, including deliberate roughness or repetition. Removing it may lose a condition, feeling, connection, emphasis, or reader orientation even when no new fact disappears.

Ask internally what the reader would lose if the span vanished. This is a diagnostic question, not permission to delete it. Assess substance by purpose: an acknowledgment needs no statistic; a reflective feeling needs no measurable result; a complete notification need not contain an ask. Flag a gap only when the missing information matters to the requested outcome. No numerical humanness score or universal requirement for names, numbers, or opinions follows from this review.

## Review the construction of the passage

[StoryScope v6](https://arxiv.org/html/2604.03136v6) finds recurring narrative choices in generated fiction that persist after stylistic editing. Use this as a prompt to review how a passage develops its point. Its evidence comes from long fiction. Applying that review to reports, emails, and ordinary answers is an editorial adaptation whose effect needs evaluation in those genres.

Within the requested edit scope, trace the main point, supporting detail, and ending. Check whether the passage repeatedly explains a lesson the reader already understands, turns an unresolved situation into a tidy success, or fills an explanatory gap with an unsupported causal link. Use the current source and matching voice examples to guide any repair. Keep a useful explanation, recap, or reflection when it serves the reader or carries the writer's intended meaning.

In reports and emails, keep the actual sequence of work, evidence, limitations, and pending actions. A successful baseline can support moving to the next test while the project's main question remains open. In creative or reflective prose, preserve the supplied uncertainty, chronology, and emotional stance. Choose sensory description or direct emotion where the scene, brief, and voice support it. Changing plot, chronology, or facts requires the user's requested scope.

For short replies, make this a brief internal check of the point and ending. For longer work, read across paragraphs for repeated explanatory patterns and added closure. Use the existing editorial pass and correction budget.

## Rebuild awkward technical sentences

When abstract nouns or stacked clauses make a passage hard to follow, identify its main point and choose what should come first using the section’s purpose and the closest voice example. In Methods, this may be the action or the reason for it. In Results, it may be what the test showed. Recast the subject, verb, or order of clauses when a word swap would leave the same awkward construction. For example, “The team checked the service for event logging and temporary file cleanup” can become “The team checked whether the service logged the event and removed its temporary files.”

Split a sentence when it changes purpose, such as from introducing a method to explaining its conditions or from reporting a result to stating its limits. Keep related clauses together when that makes the relationship easier to follow or fits the voice. Preserve precise terms and defined labels.

Preserve relationships between facts, including subsets and totals, sequence, comparisons, and what the evidence establishes. A report can say “The full suite passed 24 tests. That total includes the six focused checks.” Preserve the inclusion relationship when recasting the result.

Review the definition of the result as well as its figures. Keep what counted as an event, the population, time window, comparison, and replication conditions. Do not broaden a measured outcome, reduce repeated trials to one trial, or turn inconvenience into an unsupported safety claim. When the exact wording must remain fixed during a rewrite, use the protection procedure in [rewriting guidance](rewrite.md), then review the restored sentence in context.

## Useful patterns to inspect

These are judgment prompts, not a word blacklist, numeric quota, or exhaustive copy of the upstream catalog. Apply them to English prose; other languages require relevant linguistic evidence.

| Candidate | Possible improvement | Reasons to keep it |
|---|---|---|
| Stock introduction, empty recap, assistant preamble | Start with the supplied point; end with its actual implication | The source is a conversation or the author uses a purposeful recap |
| Inflated adjectives or abstract importance claims | Explain the source-supported effect or remove redundant emphasis | A precise evaluation or actual degree is part of the meaning |
| Vague attribution or a missing concrete detail | Preserve attribution and flag missing support; use supplied specifics | Uncertainty or limited attribution is all the source establishes |
| Filler and stacked hedges | Remove redundant wording while retaining the necessary qualifier | The modal, condition, or limitation changes the claim |
| Formulaic reversal or concession | State the existing relationship more directly | A real correction, tension, or supported rhetorical habit carries the argument |
| Synonym cycling and empty restatement | Keep terminology stable; remove only content-free duplication | Repeated nouns, lessons, or transitions are part of this writer's cadence |
| Uniform rhythm, forced fragments, ornamental triads | Restore the supported sentence movement | The profile favors connected sentences, deliberate fragments, or a real list of three |
| Excessive headings, bold, bullets, or dramatic punctuation | Simplify only within the authorized format/structure | The information is genuinely list-like, typography is required, or the author uses it |
| Fake casualness, performed candor, invented reaction | Use the source's actual stance and register | The author actually supplied the expression or reaction |

Words such as **important**, **overall**, **actually**, **robust**, or **leverage** are never automatic violations. Consider literal/technical senses, surrounding meaning, and the profile. No universal dash limit, quote normalization, sentence-length target, or rule-of-three ban is imported. Replacing a cliché with another cliché does not improve the voice.

## Keep, edit, or flag a gap

- **Keep:** “We expected a pass. It actually failed.” The correction supplies a reason for **actually**. Preserve the contrast even when the explanation is in a neighboring sentence.
- **Edit when appropriate:** “The update could potentially reduce the delay.” Remove **potentially** if it adds no distinction; keep **could** and do not turn the possibility into a promise.
- **Flag a gap:** “Experts say the plan saves money.” Without a supplied source or amount, do not invent an authority, a number, or the writer's own study. Preserve the uncertain attribution if it is source content and explain the gap when it matters.
- **Use the profile to repair a finding:** If a writer often uses “Overall,” keep it when it introduces a conclusion that adds perspective. Drop the lead-in and fold in any new detail when it introduces a stock recap that merely repeats the preceding sentence. Keep the writer's connected cadence in the revision.

## Review, stop, and report

For ordinary writing, perform this review internally and return the requested prose. Do not add an unsolicited audit, mandatory verification template, or an explanation of every kept word.

For an audit-only request, quote the relevant span, explain the actual concern, and distinguish justified findings from uncertain candidates. Report retained features when they explain a likely false positive. State whether an observation comes from model judgment or executed tooling. Do not rewrite, edit files, normalize punctuation, or store a lasting preference in audit mode.

For a rewrite/edit, keep the original available. Review the completed result against it for meaning, attribution, values and units, negation, conditions, causality, uncertainty, personal claims, and protected content. Review voice separately: check for unwanted polish, invented errors, staccato conversion, and loss of supported repetition. Do not sharpen vague prose with facts from old style samples or fresh research unless that content was requested and supported.

Check subtle relationships as well as literal values: comparisons and rankings, whether events overlap or follow one another, who acted, and whether the source actually states a cause. Two facts next to each other do not establish **because**, **therefore**, or where most time/cost went. Polishing cannot silently turn correlation into causation, a possibility into a promise, or mixed feelings into a single tidy judgment.

Then compare the edits themselves. If every change introduces the same short/long rhythm, punchline, contraction, replacement word, or newly tidy resolution, revise that editor-imposed pattern toward the actual profile. Restore any lost source detail or purposeful voice feature and recheck that the repair still addresses the editorial finding.

Honor **keep this**, **leave it**, or **stet** for the specified span through subsequent passes on the same piece; do not keep reporting it as an unresolved fault. A local exception is not a permanent profile preference and does not protect unrelated factual errors. Repeated choices can motivate an optional calibration suggestion, never an automatic profile change.

Use one main editorial pass and, only when another justified change remains, one targeted correction pass. Stop editorial iteration when no justified in-scope edit remains or that budget is used; do not chase a zero-pattern score. Correct any introduced preservation damage from the original before delivery, or return the affected source unchanged with a concise explanation when a faithful result cannot be produced. Recheck after repairs rather than claiming a planned change occurred. Broader changes require new instructions or an actual unresolved task requirement, not repeated aesthetic tinkering.

When an audit or verification report is requested, describe the delivered text and actual edits, executed checks versus model-only review, and any unresolved/protected findings. Never imply an upstream detector or marks normalizer ran: this skill bundles neither. The Python checker checks narrow integrity/rule issues; it does not run this editorial judgment or infer authorship. No pattern count, punctuation choice, polished grammar, or style match establishes who wrote a passage or guarantees acceptance by an AI detector.
