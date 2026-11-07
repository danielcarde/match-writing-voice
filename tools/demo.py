#!/usr/bin/env python3
"""Reproduce a synthetic mechanics example; no hidden model generation."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("voice_tools", ROOT / "skills/match-writing-voice/scripts/voice_tools.py")
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


def run(output=None):
    output = Path(output or ROOT / ".local/demo")
    output.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / "examples/synthetic/samples.json"
    profile = voice.measure(manifest, "synthetic-friend", "Synthetic friend voice — provisional")
    scope = {"medium": "message", "audience": "friend", "language": "en"}
    originals = {s["id"]: s["text"] for s in voice.load_samples(manifest)}
    def spans(needle, ids):
        return [{"sample_id": sid, "start": originals[sid].index(needle), "end": originals[sid].index(needle) + len(needle)} for sid in ids]
    profile["traits"] = [
        {"id": "lowercase", "category": "punctuation", "instruction": "Use lowercase openings and i in faithful friend messages.", "state": "observed", "scope": scope, "policy": "preserve", "support": spans("i", list(originals)), "counterevidence": [], "frequency": "usual in these three samples"},
        {"id": "apostrophes", "category": "spelling", "instruction": "Preserve supported apostrophe omissions when those constructions arise; no random errors.", "state": "observed", "scope": scope, "policy": "preserve", "support": spans("its", ["message-1", "message-2"]), "counterevidence": [], "frequency": "construction-dependent"},
        {"id": "practical-softening", "category": "stance", "instruction": "Pair willingness with a brief practical limit when the brief calls for it; preserve the requirement.", "state": "observed", "scope": scope, "policy": "preserve", "support": spans("just", list(originals)), "counterevidence": []},
    ]
    profile["limitations"] = ["Three synthetic friend messages only; no human recognition study.", "Client email voice is unobserved; adapted output is conservative.", "Profile traits and draft texts are explicitly authored demo fixtures, not automatic inferences."]
    validation = voice.validate_profile(profile, manifest)
    if not validation["ready"] or validation["errors"]:
        raise ValueError(validation)
    drafts = {
        "faithful": "yeah i can bring the projector to the library on tuesday, its just that i need it back by 5 pm.",
        "lightly_edited": "Yeah, I can bring the projector to the library on Tuesday. It's just that I need it back by 5 pm.",
        "adapted": "I can bring the projector to the library on Tuesday. I'll need it back by 5 pm.",
    }
    voice.output_json(profile, output / "profile.json")
    voice.output_json(validation, output / "validation.json")
    voice.write_text(output / "voice.md", voice.render_profile(profile))
    reports = {}
    for mode, draft in drafts.items():
        voice.write_text(output / f"{mode}.txt", draft + "\n")
        current = scope if mode != "adapted" else {"medium": "email", "audience": "client", "language": "en"}
        reports[mode] = voice.check(profile, draft, mode=mode, current=current, samples=voice.load_samples(manifest), protected=["projector", "library", "5 pm"])
        voice.output_json(reports[mode], output / f"{mode}-check.json")
    return {"validation": validation, "draft_verdicts": {m: r["verdict"] for m, r in reports.items()}, "output": str(output)}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
