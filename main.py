#!/usr/bin/env python3
"""Out-of-office one-liner for make.fun's "The Funniest Out-of-Office".

Writes a single 131-character out-of-office auto-reply to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The joke: the sender is away, so urgent matters are escalated to the
houseplant, which has been promoted to acting manager -- a promotion it
earned purely by thriving on neglect, the one management skill nobody
else in the office has.
"""

import os
import sys

MAX_CHARS = 140
TERMINAL_PUNCTUATION = ".!?"


def build_line() -> str:
    """Return the one-line out-of-office reply."""
    return (
        "I'm out until Monday. Urgent matters go to my houseplant, "
        "promoted to acting manager \u2014 it thrives on neglect "
        "and answers to no one."
    )


def validate(line: str) -> None:
    """Enforce the kit gate: 1-140 chars, single line, not blank,
    printable, ending in terminal punctuation."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not line.strip():
        raise ValueError("entry must not be blank")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if len(line) < 1:
        raise ValueError("entry must be at least 1 character")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.isprintable():
        raise ValueError("entry must be printable text")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if line[-1] not in TERMINAL_PUNCTUATION:
        raise ValueError("entry must end in terminal punctuation")


def write_entry() -> str:
    """Validate the line and write it to entry.txt. Returns the path."""
    line = build_line()
    validate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != line:
            raise RuntimeError("entry.txt does not match the validated line")
    return path


def main() -> int:
    path = write_entry()
    line = build_line()
    print(f"wrote {len(line)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
