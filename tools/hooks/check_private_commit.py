#!/usr/bin/env python3
"""PreToolUse guard: blocks `git commit` if the staged diff leaks personal data.

Reads the Claude Code hook payload from stdin, no-ops on anything that isn't
a `git commit`. On commit, greps `git diff --cached` against the shared
denylist in _privacy_patterns.py — no name is hardcoded in this repo; add
your own (and any project/people names specific to you) to
~/.hestia/private-denylist.txt.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _privacy_patterns import find_hits  # noqa: E402


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\s+commit\b", command):
        return 0

    diff = subprocess.run(
        ["git", "diff", "--cached"], capture_output=True, text=True
    ).stdout
    if not diff:
        return 0

    hits = find_hits(diff)
    if hits:
        print("Bloqueado: el commit tiene datos personales sin generalizar:", file=sys.stderr)
        for h in hits:
            print(f"  - {h}", file=sys.stderr)
        print("Generalizá (checklist de despersonalización) antes de commitear.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
