"""Expose the canonical skill's behavioral suite to root-level discovery."""
import importlib.util
from pathlib import Path


def load_tests(loader, tests, pattern):
    file = Path(__file__).resolve().parents[1] / "skills/match-writing-voice/evals/test_voice_tools.py"
    spec = importlib.util.spec_from_file_location("canonical_voice_tests", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)
