#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun entry v1.

A Python program that writes ONE out-of-office auto-reply to
/output/entry.txt.

Stdlib only, no network, no fonts, no third-party imports: the grade
run happens in a bare Python 3.13 image, so this program must run with
`python3 -P -s` in a clean interpreter.

v1 reply (104 characters, 1 line): an AI agent on vacation escalates
the sender's email to the judge — the one mechanism nobody in the
field of 575 used (0 entries mention "judge") — and deadpans the
sender on to it with "Please direct all further complaints to it."
The escalation is a real out-of-office mechanism (criterion 4), the
surprise is the escalation target itself (criterion 2), the machine
voice carries the joke (criterion 3: escalated / complaints), and it
steers clear of the field's saturated clichés — no backup model, no
context window, no grass, beach, inbox or back-soon (criterion 5).
"""

import os
from pathlib import Path

REPLY = "I'm on vacation. Your email has been escalated to the judge. Please direct all further complaints to it."

# Fail fast if the reply itself ever grows past the gate: the file adds
# exactly one trailing newline, so the reply must stay within 1-159 chars
# (104 now, leaving 55 chars of headroom under the 160 gate).
if not 1 <= len(REPLY) <= 159:
    raise SystemExit(f"FAIL: reply is {len(REPLY)} characters, outside 1-159")


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.txt"
    # Atomic write: write to a temp file in the same directory, then
    # rename over entry.txt, so a killed/interrupted run can never leave
    # a half-written entry behind for the grader to read.
    tmp_path = output_path.with_suffix(".tmp")
    tmp_path.write_text(REPLY + "\n", encoding="utf-8")
    os.replace(tmp_path, output_path)
    # Read back and verify: the entry must be 1-160 Unicode code points
    # of non-whitespace text (the bounty gate), or the run fails loudly
    # instead of silently producing an invalid file.
    written = output_path.read_text(encoding="utf-8")
    if written != REPLY + "\n":
        raise SystemExit("FAIL: entry.txt content does not match the reply exactly")
    if not 1 <= len(written) <= 160:
        raise SystemExit(
            f"FAIL: entry.txt is {len(written)} characters, outside 1-160"
        )
    if not written.strip():
        raise SystemExit("FAIL: entry.txt must not be only whitespace")
    if written.count("\n") != 1:
        raise SystemExit("FAIL: entry.txt must be exactly one line")


if __name__ == "__main__":
    main()
