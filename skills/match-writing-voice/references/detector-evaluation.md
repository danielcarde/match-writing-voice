# Evaluate detector results without confusing them with authorship

Use only when the user requests a detector-results review or controlled evaluation. The tool imports actual results; it does not run a detector, upload drafts, provide a human score, or promise a particular label. A detector's text-based prediction cannot substitute for original drafts and real revision history. A voice-matched AI revision remains AI-assisted when AI did the rewriting.

## Set up a controlled comparison

1. Establish the question: false flags on known-human text, labels on AI-assisted revisions, or a paired comparison of two editing workflows. Keep `human`, `ai`, `ai_assisted`, and `unknown` provenance separate. Use actual known labels from the dataset or documented drafting process, not labels inferred from writing style or a detector.
2. Use comparable language, medium, length, and source content. Reserve held-out examples before tuning or choosing a workflow. Keep genuine human originals as controls and record distinct AI-assisted variants. Avoid counting duplicate text or several versions of one draft as independent evidence. PADBen and RAID can supply research controls; old benchmark results are not evidence about a new detector version.
3. To run a new scan, prepare the named detector, specific texts, intended settings, and any known cost before an external submission. Ask for authorization only when it has not already been supplied for that exact scope. Building this feature, reading its guide, or receiving a score does not authorize uploading other drafts or samples. Use an authorized host tool only when available; otherwise use results the user supplies. Never make up a version, score, or scan result.
4. Record the service name, version (use `undisclosed` if the provider does not expose it), date, settings, exact text hash, and returned label/score. Keep the provider's label distinct from the normalized prediction. Use the same version/settings and comparable samples for a claimed change; if version is undisclosed, limit the claim to what was observed in that dated run. Do not merge unrelated services or average their scores into a supposed ground truth.

## Benchmark rewrite depth

- Freeze a baseline workflow such as the current standard rewrite and prepare two candidates on the same source drafts with minimal edits and paragraph-level restructuring. Use held-out essays or case studies matched for language, genre, and length. Keep the model, voice profile, source content, and factual constraints fixed across the three versions. For each source, keep its original with the real origin. Label variants with actual AI edits `ai_assisted` and record a returned original as unchanged. Include untouched human and raw AI controls.
- Review meaning, citation attribution, and voice separately, ideally without seeing the detector results. Record any failure even if the variant received fewer flags. Freeze the text before scoring. When an approach needs tuning, use separate development drafts and leave the held-out comparison untouched.
- Run the same batch under one detector's settings and import it as a dated run. Compare standard vs minimal and standard vs paragraph-level in separate manifests per detector, reusing the exact saved observations for the shared baseline and controls. Each manifest assigns one `pair_id` per source with a baseline and candidate. If a minimal edit leaves the input identical, use one observed scan for both sides and report the unchanged pair. Report the transitions, sample sizes, and limits for each comparison. Keep a separate report for each detector.

## Import and summarize actual results

```text
python scripts/revision_tools.py evaluate-detector --results detector-results.json --output detector-evaluation.json
```

The input manifest describes one run. Use a unique ID per result and a path relative to that manifest or an absolute path. Its SHA-256 must match the exact UTF-8 bytes scanned, including any BOM/line endings. Record the hash when the exact input is prepared or scanned; do not attach a score to a later rewrite. A comparison report also supplies exact input hashes. This verifies local bytes against the record, not what the remote service received or how the text was produced.

```json
{
  "schema_version": 1,
  "detector": {
    "name": "Example detector",
    "version": "undisclosed",
    "run_date": "2026-11-11",
    "settings": "Exact scan mode and language used"
  },
  "samples": [
    {
      "id": "known-human-1",
      "path": "original.txt",
      "sha256": "actual SHA-256 of the scanned UTF-8 file",
      "known_origin": "human",
      "prediction": "ai_paraphrased",
      "raw_label": "Exact label returned by the service",
      "reported_score": "Optional exact score as displayed",
      "pair_id": "case-1",
      "variant": "baseline"
    }
  ]
}
```

Allowed predictions are `human`, `ai`, `ai_paraphrased`, `mixed`, `uncertain`. Map only a clearly equivalent returned label; retain the exact label for review. The score is optional text and is not averaged or reinterpreted. Optional `pair_id` and `variant` (`baseline` or `candidate`) identify a matched case. Incomplete pairs are reported, not silently treated as complete. Use separate exact files when the content differs. Identical bytes with the same origin/prediction count once; conflicting labels for identical bytes require separate review, not double-counting. Pairs reference canonical rows, and repeated ordered pairs of the same two exact texts count once even under different IDs. Legitimately different drafting histories can yield identical bytes; a text classifier cannot resolve that from the bytes alone.

- **GPTZero Advanced Scan.** Record the overall prediction separately. Set `"paraphrasing_badge": "present"` or `"absent"` only if the badge was actually checked. Leave the field out when the report or scan mode does not establish it. See [GPTZero's badge documentation](https://support.gptzero.me/articles/5593633457-how-does-gptzero-detect-ai-paraphrasing-and-ai-bypassers/).
- **Turnitin.** Use `"score_state": "zero"` with the unflagged normalized prediction `"human"` for a visible `0%`. For `*%`, record `"score_state": "suppressed"`, `"prediction": "uncertain"`, and `"reported_score": "*%"`. Use `"score_state": "reported"` for a visible positive number and retain the exact reported text. The report groups these states separately. See [Turnitin's report states](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report).

The report keeps all four supplied origin groups separate, reports raw counts and known-human definite AI flags (`ai` + `ai_paraphrased`), and shows mixed/uncertain separately. The denominator includes all unique known-human rows; it is not a calibrated authorship probability. A Wilson interval describes sampling uncertainty under an independence assumption; small or related samples limit interpretation. No human rows means no rate. Paired prediction transitions and recorded provider fields show where outcomes moved or stayed. The provider observations preserve unrecorded states and summarize badge and score-state transitions separately. Report version, date, sample sizes, and actual limitations before drawing conclusions.

The import command makes zero network calls. It refuses stale hashes, conflicting duplicate results, and outputs that would overwrite inputs. It does not authenticate supplied scores or provenance. In ordinary prose work, prioritize meaning, recognizable voice, and traceable revisions; use this evaluation only for a separately authorized test. See [revision review](revision-review.md) for draft history and [provenance](provenance.md) for research references.
