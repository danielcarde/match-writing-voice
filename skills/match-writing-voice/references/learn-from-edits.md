# Learn from before-and-after edits

Use this workflow when the user asks to learn revision habits from an earlier draft and a revised version. A request to compare drafts alone calls for [revision review](revision-review.md). A later rewrite can use the saved habits without repeating the learning step.

## Identify the evidence

- Identify the earlier version, revised version, intended profile, and writing context. Reuse the matching medium label in an existing profile. Align passages that discuss the same content, including passages that moved.
- Use the person's actual edits for evidence of personal habits. An AI-authored original is usable as the before version. With the user's request, save a group edit or another editor's work as a shared technical or editorial example. Record the contribution as `shared` and apply it as a user-selected reference. A detector label supplies no evidence about who made the edits.
- Exclude quotations, boilerplate, copied passages, and changes whose editor is unknown. For mixed contributions, isolate the known changes when possible. Count iterations and near duplicates of one piece as one example.

## Learn the decisions that transfer

1. Compare the versions using the [revision review](revision-review.md). Identify the actual decision behind a change and the context where it makes sense. If the writer rearranged information, record which point they moved and what they put before or after it. A progress report might lead with the test result and move setup details after it. Name the section in the instruction and record the known audience in the scope.
2. Check the source and revision section by section for facts, quantities, dates, citations, conditions, uncertainty, and completed versus planned work. A passage can show a useful change in voice even when other edits drop reproducibility details or change the claim. Learn only from changes that can transfer with the meaning intact. Leave subject facts and distinctive wording out of the reusable instruction.
3. Save a few specific instructions. Treat one example as provisional. Mark a personal habit as recurring in the summary only when independently supported by the person's own edits in at least two pieces. A shared example can guide work in its scoped context with the user's approval. It stays separate from evidence of the person's individual habits.

## Save and apply

When asked to save, append or merge the supported instructions into the chosen profile. Add independent evidence to an existing instruction with the same scope. Keep the existing profile's other traits and evidence. Validate the JSON before replacing it and refresh the guide the user actually loads. In a text-only host, provide an updated Markdown guide the user can reuse. For a single analysis request, report findings directly and ask about a destination only if saving is requested and the destination is unresolved.

Use the optional `revision_habits` field from the [profile format](profile-format.md). The local comparison supplies the two exact text hashes. Store hashes, contribution, scope, and a reusable instruction. Save full drafts only when requested. For a standalone Markdown guide, include the source pair's descriptive label, its context, and the evidence strength without embedding the two drafts.

When the user requests a reusable collection of approved pairs, use the approved-example metadata and private history bundles in [revision review](revision-review.md). Retain authorship labels and approval notes, and keep related sections in one split. A collection does not train model weights or establish a recurring personal habit. Do not learn from its held-out references.

Apply matching habits on future rewrites. Current instructions, protected text, requested edit depth, and evidence of the writer's personal voice govern the edit. For example, a progress-report habit can move a test and its purpose together when the user allows restructuring. Under minimal edits, apply it only where a local change is warranted.

Before delivery, compare each revised section with its source. Check technical terms, numeric details, attribution, caveats, and what the team actually completed. When paragraphs move, trace the supporting details with their claims. Show the useful changes and their limits if requested. Evaluate any detector effect separately on fresh text with the same facts and scan settings.
