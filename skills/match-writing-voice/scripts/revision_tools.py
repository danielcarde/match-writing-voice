#!/usr/bin/env python3
"""Local revision comparison, opt-in draft history, and imported detector evaluations."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from difflib import SequenceMatcher
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import voice_tools as voice


ORIGINS = ("human", "ai", "ai_assisted", "unknown")
PREDICTIONS = ("human", "ai", "ai_paraphrased", "mixed", "uncertain")
PURPOSES = ("voice", "clarity", "grammar", "format", "authorized_content_change", "unnecessary", "uncertain")
MAX_DIFF_UNITS = 100_000
SNAPSHOT_NAMES = {"original.txt", "revision.txt", "comparison.json", "profile.json"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def emit(value, path=None):
    if path:
        voice.write_text(path, json_bytes(value).decode("utf-8"))
    else:
        # ASCII escapes preserve arbitrary Unicode even on legacy Windows stdout encodings.
        print(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False))


def nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def one_of(value, choices, field):
    if value not in choices:
        raise ValueError(f"{field} must be one of: {', '.join(choices)}")
    return value


def require_version(data, label):
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError(f"Unsupported {label} schema_version; expected 1")


def reject_input_alias(output, inputs, history=None):
    if not output:
        return
    target = Path(output).resolve()
    if history and target.is_relative_to(Path(history).resolve()):
        raise ValueError("--output must be outside the new history directory")
    for item in inputs:
        if item is None:
            continue
        source = Path(item).resolve()
        if source == target or (target.exists() and source.exists() and source.samefile(target)):
            raise ValueError("Output must not overwrite or alias an input")


def metrics(text):
    words = voice.tokens(text)
    sentences = [voice.tokens(part) for part in re.split(r"[.!?。！？]+", text)]
    result = voice.statistics_for([{"kept": text, "surface_reliable": True}])
    surface = result["surface"]
    mean, sd = surface["mean_sentence_words"], surface["sentence_words_sd"]
    window = 50
    mattr = None
    if len(words) >= window:
        counts = Counter(words[:window])
        total = len(counts)
        for left, right in zip(words, words[window:]):
            counts[left] -= 1
            if counts[left] == 0:
                del counts[left]
            counts[right] += 1
            total += len(counts)
        mattr = round(total / (window * (len(words) - window + 1)), 4)
    return {"words": len(words), "sentences_heuristic": sum(bool(s) for s in sentences),
            "paragraphs": sum(bool(p.strip()) for p in re.split(r"\n\s*\n", text)),
            "mean_sentence_words": mean, "sentence_words_sd": sd,
            "sentence_length_cv": round(sd / mean, 4) if mean else None,
            "lexical_diversity_ttr": result["lexical_diversity_ttr"], "mattr_50": mattr,
            "punctuation_per_100_words": surface["punctuation_per_100_words"]}


def exact_edits(source, draft):
    def units(text):
        items, offsets = [], [0]
        for match in re.finditer(r"\s+|\S+", text):
            if len(items) >= MAX_DIFF_UNITS:
                raise ValueError(f"Comparison exceeds {MAX_DIFF_UNITS} text units; compare smaller sections")
            items.append(match.group())
            offsets.append(match.end())
        return items, offsets

    left, ls = units(source)
    right, rs = units(draft)
    changes = []
    for kind, i, j, k, l in SequenceMatcher(None, left, right).get_opcodes():
        if kind == "equal":
            continue
        before, after = source[ls[i]:ls[j]], draft[rs[k]:rs[l]]
        changes.append({"id": f"edit-{len(changes) + 1:04d}", "operation": kind,
                        "source_span": [ls[i], ls[j]], "revision_span": [rs[k], rs[l]],
                        "before": before, "after": after,
                        "whitespace_only": re.sub(r"\s+", "", before) == re.sub(r"\s+", "", after)})
    return changes


def scoped_baselines(profile, current, samples, verified):
    if profile is None:
        return {"status": "no_profile", "groups": []}
    if not current:
        return {"status": "context_required", "groups": []}
    groups = []
    if verified:
        by_context = defaultdict(list)
        for s in samples:
            if s["eligible"] and voice.matches(current, s["context"]):
                by_context[json.dumps(s["context"], sort_keys=True)].append(s)
        for ctx, group in sorted(by_context.items()):
            groups.append({"context": json.loads(ctx), "sample_ids": [s["id"] for s in group],
                           "measurements": voice.statistics_for(group), "basis": "reverified_manifest"})
    else:
        observations = profile.get("observations", [])
        for obs in observations if isinstance(observations, list) else []:
            if (isinstance(obs, dict) and isinstance(obs.get("context"), dict)
                    and isinstance(obs.get("measurements"), dict) and voice.matches(current, obs["context"])):
                groups.append({"context": obs["context"], "measurements": obs["measurements"],
                               "basis": "saved_profile_observations_not_reverified"})
    return {"status": "matched" if groups else "no_matching_context", "groups": groups}


def apply_review(report, review):
    edits = {e["id"]: e for e in report["edits"]}
    default = {"coverage": "not_supplied", "reviewer": None, "meaning": None, "voice": None,
               "unreviewed_edit_ids": list(edits), "flagged_edit_ids": [],
               "verification": "Editorial judgments are supplied annotations, not machine-verified conclusions."}
    if review is None:
        return default
    require_version(review, "review")
    if review.get("comparison_id") != report["comparison_id"]:
        raise ValueError("Review does not match this comparison; review the exact versions and settings again")
    reviewer = one_of(review.get("reviewer"), ("human", "model", "both"), "reviewer")
    supplied = review.get("edits", [])
    if not isinstance(supplied, list):
        raise ValueError("Review edits must be a list")
    traits = {t["id"] for t in report["applicable_traits"]}
    seen, flagged = set(), []
    for item in supplied:
        if not isinstance(item, dict):
            raise ValueError("Each edit review must be an object")
        eid = nonempty(item.get("id"), "edit review ID")
        if eid not in edits or eid in seen:
            raise ValueError(f"Unknown or repeated edit review ID: {eid}")
        seen.add(eid)
        decision = one_of(item.get("decision"), ("keep", "revert", "review"), "edit decision")
        purpose = one_of(item.get("purpose"), PURPOSES, "edit purpose")
        effect = one_of(item.get("voice_effect"), ("supports", "neutral", "weakens", "uncertain"), "voice_effect")
        linked = item.get("trait_ids", [])
        if not isinstance(linked, list) or any(not isinstance(t, str) or t not in traits for t in linked):
            raise ValueError(f"{eid}: review trait_ids must refer to applicable traits")
        edits[eid]["review"] = {"decision": decision, "purpose": purpose, "voice_effect": effect,
                                "reason": nonempty(item.get("reason"), "edit reason"), "trait_ids": linked}
        if decision != "keep" or purpose in {"unnecessary", "uncertain"} or effect in {"weakens", "uncertain"}:
            flagged.append(eid)

    def summary(field, statuses):
        item = review.get(field)
        if item is None:
            return None
        if not isinstance(item, dict):
            raise ValueError(f"{field} review must be an object")
        return {"status": one_of(item.get("status"), statuses, field),
                "reason": nonempty(item.get("reason"), f"{field} reason")}

    meaning = summary("meaning", ("preserved", "changed", "needs_review"))
    voice_review = summary("voice", ("consistent", "weakened", "insufficient_evidence", "needs_review"))
    unreviewed = [eid for eid in edits if eid not in seen]
    return {**default, "coverage": "complete" if not unreviewed and meaning and voice_review else "partial",
            "reviewer": reviewer, "meaning": meaning, "voice": voice_review,
            "unreviewed_edit_ids": unreviewed, "flagged_edit_ids": flagged}


def comparison(source, draft, *, profile=None, manifest=None, current=None, mode=None, structure="preserve",
               protected=(), author_context=None, source_origin="unknown", draft_origin="unknown", review=None):
    if not source.removeprefix("\ufeff").strip():
        raise ValueError("Comparison requires a nonempty original draft")
    one_of(structure, ("preserve", "restructure"), "structure")
    one_of(source_origin, ORIGINS, "source origin")
    one_of(draft_origin, ORIGINS, "revision origin")
    if manifest and profile is None:
        raise ValueError("--manifest requires the corresponding --profile")
    verified, samples, validation = False, [], None
    current = voice.context({} if current is None else current)
    if profile is not None:
        validation = voice.validate_profile(profile, manifest)
        if validation["errors"] or not validation["ready"]:
            raise ValueError("A valid interpreted profile is required: " + "; ".join(validation["errors"] or validation["warnings"]))
        verified = validation["source_verified"]
        samples = voice.load_samples(manifest, profile["profile_id"]) if manifest else []
        current = current or profile.get("defaults", {}).get("context", {})
        mode = mode or profile.get("defaults", {}).get("mode", "faithful")
    mode = one_of(mode or "faithful", tuple(sorted(voice.MODES)), "mode")
    original, revised = source.removeprefix("\ufeff"), draft.removeprefix("\ufeff")
    changes = exact_edits(source, draft)
    if profile is not None:
        checks = voice.check(profile, revised, mode, current, source=original, samples=samples,
                             protected=protected, author_context=author_context, workflow="rewrite", structure=structure)
        checks["validation_warnings"] = validation["warnings"]
        before = voice.check(profile, original, mode, current, source=original)
        before_rules = {r["rule"] for r in before["findings"] if r["code"] == "voice_rule"}
        after_rules = {r["rule"] for r in checks["findings"] if r["code"] == "voice_rule"}
        rule_changes = {"introduced": sorted(after_rules - before_rules), "resolved": sorted(before_rules - after_rules),
                        "still_present": sorted(before_rules & after_rules)}
        traits = [{"id": t["id"], "category": t["category"], "state": t["state"], "scope": t.get("scope", {}),
                   "policy": voice.effective_policy(t, mode), "instruction": t["instruction"],
                   "support": t.get("support", []), "counterevidence": t.get("counterevidence", [])}
                  for t in profile["traits"] if t["state"] != "unknown" and voice.matches(t.get("scope", {}), current)]
    else:
        findings = voice.integrity(original, revised, protected) + voice.rewrite_review(original, revised, structure)
        findings += voice.knowledge_claim_review(revised, (original, author_context))
        verdict = "BLOCK" if any(f["severity"] == "block" for f in findings) else "REVIEW" if findings else "PASS"
        checks = {"verdict": verdict, "findings": findings, "manual_review_completed": False,
                  "limits": "Narrow source checks only; no profile rules or semantic review were executed."}
        traits, rule_changes = [], None
    left, right = metrics(original), metrics(revised)
    report = {"schema_version": 1, "kind": "revision_comparison", "mode": mode, "structure": structure, "context": current,
              "source": {"sha256": digest(source.encode("utf-8")), "origin_supplied": source_origin, "measurements": left},
              "revision": {"sha256": digest(draft.encode("utf-8")), "origin_supplied": draft_origin, "measurements": right},
              "profile_id": profile["profile_id"] if profile is not None else None,
              "profile_sha256": digest(json_bytes(profile)) if profile is not None else None,
              "profile_evidence_verified_now": verified, "applicable_traits": traits,
              "review_inputs": {"protected_literals_sha256": digest(json_bytes(list(protected))),
                                "author_context_sha256": digest(author_context.encode("utf-8")) if author_context is not None else None},
              "authored_baselines": scoped_baselines(profile, current, samples, verified),
              "measurement_deltas": {k: round(right[k] - value, 4) for k, value in left.items()
                                     if isinstance(value, (int, float)) and isinstance(right[k], (int, float))},
              "punctuation_rate_deltas": {p: round(right["punctuation_per_100_words"][p] - value, 4)
                                          for p, value in left["punctuation_per_100_words"].items()},
              "mechanical_checks": checks, "profile_rule_changes": rule_changes,
              "edits": changes, "edit_count": len(changes), "text_identical": source == draft,
              "offsets": "Zero-based Unicode positions, end exclusive, in exact UTF-8-decoded input including BOM and line endings.",
              "limits": ["The whitespace/non-whitespace diff groups actual changes; it need not be the smallest possible alignment.",
                         "Counts and changes are descriptive. Short samples, segmentation, and different contexts limit comparisons; no voice or human score is inferred.",
                         "User-supplied origins and editorial annotations are separate from deterministic checks and do not authenticate authorship.",
                         "A mechanical PASS does not establish meaning preservation, voice recognition, or detector performance."]}
    report["comparison_id"] = digest(json_bytes(report))
    report["editorial_review"] = apply_review(report, review)
    return report


def save_history(path, source, draft, report, profile=None):
    root = Path(path).resolve()
    root.mkdir(parents=True, exist_ok=False)
    files = {"original.txt": source.encode("utf-8"), "revision.txt": draft.encode("utf-8"),
             "comparison.json": json_bytes(report)}
    if profile is not None:
        files["profile.json"] = json_bytes(profile)
    for name, data in files.items():
        with (root / name).open("xb") as target:
            target.write(data)
    index = {"schema_version": 1, "kind": "revision_history", "created_at_utc": datetime.now(timezone.utc).isoformat(),
             "comparison_id": report["comparison_id"],
             "files": {name: {"sha256": digest(data), "bytes": len(data)} for name, data in files.items()},
             "limits": "Local snapshot and integrity record, not tamper-proof history or proof of authorship."}
    # Write the index last so a failed partial write cannot masquerade as a complete bundle.
    with (root / "history.json").open("xb") as target:
        target.write(json_bytes(index))
    return str(root)


def verify_history(path):
    root = Path(path).resolve()
    index_path = root / "history.json"
    if index_path.is_symlink() or not index_path.is_file():
        raise ValueError("A complete local history index is required")
    index = voice.read_json(index_path)
    require_version(index, "history")
    items = index.get("files")
    required = SNAPSHOT_NAMES - {"profile.json"}
    if index.get("kind") != "revision_history" or not isinstance(items, dict) or not required <= set(items) <= SNAPSHOT_NAMES:
        raise ValueError("Invalid history file list")
    errors = []
    for name, metadata in items.items():
        file = root / name
        if not file.is_file() or file.is_symlink() or not file.resolve().is_relative_to(root):
            errors.append(f"{name}: missing or invalid snapshot path")
            continue
        checksum = hashlib.sha256()
        with file.open("rb") as source:
            for block in iter(lambda: source.read(1 << 20), b""):
                checksum.update(block)
        if not isinstance(metadata, dict) or checksum.hexdigest() != metadata.get("sha256") or file.stat().st_size != metadata.get("bytes"):
            errors.append(f"{name}: snapshot hash or size differs")
    return {"verified": not errors, "errors": errors, "files_checked": len(items),
            "limits": "Checks files against the supplied local index only; not an authenticity or authorship verdict."}


def wilson_interval(positive, total):
    if not total:
        return None
    z = 1.959963984540054
    p = positive / total
    center = p + z * z / (2 * total)
    radius = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total))
    denominator = 1 + z * z / total
    return [round(max(0, (center - radius) / denominator), 6), round(min(1, (center + radius) / denominator), 6)]


def paired_observations(groups):
    pairs, incomplete, duplicates = [], [], []
    seen = {}
    for pid, pair in groups.items():
        if set(pair) != {"baseline", "candidate"}:
            incomplete.append(pid)
            continue
        before, after = pair["baseline"], pair["candidate"]
        key = before["sha256"], after["sha256"]
        if key in seen:
            duplicates.append({"pair_id": pid, "duplicate_of": seen[key]})
            continue
        seen[key] = pid
        pairs.append({"pair_id": pid, "baseline_id": before["id"], "candidate_id": after["id"],
                      "baseline_origin": before["known_origin"], "candidate_origin": after["known_origin"],
                      "baseline_prediction": before["prediction"], "candidate_prediction": after["prediction"],
                      "identical_bytes": before["sha256"] == after["sha256"]})
    return {"complete_pairs": len(pairs), "incomplete_pair_ids": incomplete, "pairs": pairs,
            "exact_duplicate_pairs_excluded": duplicates,
            "paraphrasing_flag_only_at_baseline": sum(p["baseline_prediction"] == "ai_paraphrased" and p["candidate_prediction"] != "ai_paraphrased" for p in pairs),
            "paraphrasing_flag_only_at_candidate": sum(p["baseline_prediction"] != "ai_paraphrased" and p["candidate_prediction"] == "ai_paraphrased" for p in pairs),
            "limits": "User-declared pairs show label transitions only; a change is not automatically an improvement or a correct decision."}


def evaluate_results(path, output=None):
    data = voice.read_json(path)
    require_version(data, "detector evaluation")
    detector = data.get("detector")
    if not isinstance(detector, dict):
        raise ValueError("detector must be an object")
    meta = {k: nonempty(detector.get(k), f"detector.{k}") for k in ("name", "version", "run_date", "settings")}
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["run_date"]):
        raise ValueError("detector.run_date must be YYYY-MM-DD")
    date.fromisoformat(meta["run_date"])
    rows = data.get("samples")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Provide nonempty samples with supplied detector results")
    ids, by_hash, duplicates, accepted = set(), {}, [], []
    pair_groups = defaultdict(dict)
    counts = {origin: dict.fromkeys(PREDICTIONS, 0) for origin in ORIGINS}
    base = Path(path).resolve().parent
    inputs = [path]
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError("Each evaluation sample must be an object")
        sid = nonempty(item.get("id"), "sample id")
        if sid in ids:
            raise ValueError(f"Repeated sample id: {sid}")
        ids.add(sid)
        origin = one_of(item.get("known_origin"), ORIGINS, f"{sid} known_origin")
        prediction = one_of(item.get("prediction"), PREDICTIONS, f"{sid} prediction")
        raw_label = nonempty(item.get("raw_label"), f"{sid} raw_label")
        expected = nonempty(item.get("sha256"), f"{sid} sha256")
        source = base / nonempty(item.get("path"), f"{sid} path")
        inputs.append(source)
        text = voice.read_text(source, preserve_bom=True)
        if digest(text.encode("utf-8")) != expected:
            raise ValueError(f"{sid}: text hash does not match the recorded detector input")
        record = {"id": sid, "sha256": expected, "known_origin": origin, "prediction": prediction, "raw_label": raw_label}
        if "reported_score" in item:
            record["reported_score"] = nonempty(item["reported_score"], f"{sid} reported_score")
        if expected in by_hash:
            first = by_hash[expected]
            if (origin, prediction) != (first["known_origin"], first["prediction"]):
                raise ValueError(f"{sid}: duplicate bytes have conflicting origins or predictions; review records separately")
            duplicates.append({"id": sid, "duplicate_of": first["id"]})
            record = first
        else:
            by_hash[expected] = record
            accepted.append(record)
            counts[origin][prediction] += 1
        if "pair_id" in item or "variant" in item:
            pid = nonempty(item.get("pair_id"), f"{sid} pair_id")
            variant = one_of(item.get("variant"), ("baseline", "candidate"), f"{sid} variant")
            if variant in pair_groups[pid]:
                raise ValueError(f"Repeated {variant} for pair {pid}")
            pair_groups[pid][variant] = record
    reject_input_alias(output, inputs)
    human = counts["human"]
    total = sum(human.values())
    flagged = human["ai"] + human["ai_paraphrased"]
    return {"schema_version": 1, "kind": "supplied_detector_evaluation", "detector": meta,
            "network_calls": 0, "results_source": "supplied_not_independently_verified", "text_hashes_verified": True,
            "sample_count": len(accepted), "exact_duplicates_excluded": duplicates, "records": accepted,
            "counts_by_origin_and_prediction": counts,
            "paired_observations": paired_observations(pair_groups) if pair_groups else None,
            "human_baseline": {"count": total, "definite_ai_flags": flagged, "mixed": human["mixed"],
                               "uncertain": human["uncertain"], "paraphrasing_flags": human["ai_paraphrased"],
                               "definite_ai_flag_fraction": round(flagged / total, 6) if total else None,
                               "wilson_95_interval": wilson_interval(flagged, total)},
            "limits": ["Origins, predictions, version, and date are supplied labels. No provider call or independent provenance verification occurred.",
                       "Definite AI flags are ai plus ai_paraphrased; the denominator is all unique known-human rows. Mixed and uncertain remain separate. AI-assisted and unknown origins are not counted as human false positives.",
                       "Exact duplicate bytes are counted once. Intervals assume independent observations; small, matched, or related samples limit interpretation.",
                       "This report does not establish current provider performance beyond the supplied run, predict future results, or prove improvement without a comparable held-out baseline."]}


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("compare", help="Compare actual original/revision text and optionally save a new history bundle")
    p.add_argument("--source", required=True)
    p.add_argument("--draft", required=True)
    p.add_argument("--profile")
    p.add_argument("--manifest")
    p.add_argument("--context", default="{}")
    p.add_argument("--mode", choices=sorted(voice.MODES))
    p.add_argument("--structure", choices=["preserve", "restructure"], default="preserve")
    p.add_argument("--protect", action="append", default=[])
    p.add_argument("--author-context")
    p.add_argument("--source-origin", choices=ORIGINS, default="unknown")
    p.add_argument("--draft-origin", choices=ORIGINS, default="unknown")
    p.add_argument("--review")
    p.add_argument("--output")
    p.add_argument("--history-dir", help="New directory; never overwrite an existing history bundle")
    p = commands.add_parser("verify-history", help="Check saved snapshot hashes without changing files")
    p.add_argument("--history-dir", required=True)
    p = commands.add_parser("evaluate-detector", help="Summarize already supplied detector results; no network calls")
    p.add_argument("--results", required=True)
    p.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        if args.command == "verify-history":
            result = verify_history(args.history_dir)
            emit(result)
            return 0 if result["verified"] else 1
        if args.command == "evaluate-detector":
            emit(evaluate_results(args.results, args.output), args.output)
            return 0
        inputs = [args.source, args.draft, args.profile, args.manifest, args.review, args.author_context]
        if args.manifest:
            base = Path(args.manifest).resolve().parent
            entries = voice.read_json(args.manifest).get("samples", [])
            if isinstance(entries, list):
                inputs += [base / s["path"] for s in entries if isinstance(s, dict) and isinstance(s.get("path"), str)]
        reject_input_alias(args.output, inputs, args.history_dir)
        source = voice.read_text(args.source, preserve_bom=True)
        draft = voice.read_text(args.draft, preserve_bom=True)
        profile = voice.read_json(args.profile) if args.profile else None
        report = comparison(source, draft, profile=profile, manifest=args.manifest, current=json.loads(args.context),
                            mode=args.mode, structure=args.structure, protected=args.protect,
                            author_context=voice.read_text(args.author_context) if args.author_context else None,
                            source_origin=args.source_origin, draft_origin=args.draft_origin,
                            review=voice.read_json(args.review) if args.review else None)
        if args.history_dir:
            report["history_dir"] = save_history(args.history_dir, source, draft, report, profile)
        emit(report, args.output)
        return 1 if report["mechanical_checks"]["verdict"] == "BLOCK" else 0
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
