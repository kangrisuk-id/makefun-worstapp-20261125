#!/usr/bin/env python3
"""UmbrellaDry — entry for make.fun's "The Worst App Idea Ever Pitched".

Writes the one-sentence pitch to entry.txt in the output directory.
Pure standard library; no network, no input, deterministic.
"""

import os

# The winning pitch, picked from 40 candidates in candidates.md by scoring
# against the judge's published criteria and a top-8 pairwise tournament.
PITCH = (
    'UmbrellaDry texts you "your umbrella is now dry" four to six hours '
    "after every rainstorm, for people who own exactly one umbrella and "
    "check on it emotionally."
)

MAX_CHARS = 240  # the competition gate: 1..240 characters, one sentence


def output_candidates() -> list:
    """Where entry.txt may go, most preferred first.

    The harness names its output directory in MAKEFUN_OUTPUT_DIR; the
    brief's own wording is /output. A local ./output keeps a laptop run
    from failing when neither is writable.
    """
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.join(os.getcwd(), "output"))
    return dirs


def check_pitch(text: str) -> None:
    """Hold the pitch to the gate before anything is written."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"pitch is {len(text)} chars, gate is 1..{MAX_CHARS}")
    if text != text.strip() or not text.endswith("."):
        raise ValueError("pitch must be one clean sentence ending in a period")
    if text.count(".") != 1:
        raise ValueError("pitch must be exactly one sentence")


def main() -> None:
    text = PITCH.strip()
    check_pitch(text)
    last_error = None
    for out_dir in output_candidates():
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            with open(path, "r", encoding="utf-8") as fh:
                if fh.read() != text:
                    raise IOError(f"round-trip mismatch in {path}")
            return
        except OSError as exc:  # try the next candidate directory
            last_error = exc
    raise SystemExit(f"could not write entry.txt anywhere: {last_error}")


if __name__ == "__main__":
    main()
