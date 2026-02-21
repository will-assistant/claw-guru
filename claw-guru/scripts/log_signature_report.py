#!/usr/bin/env python3
"""Summarize high-signal OpenClaw log signatures.

Usage:
  openclaw logs --follow | python3 scripts/log_signature_report.py
  python3 scripts/log_signature_report.py /path/to/logfile
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

SIGNATURES: list[tuple[str, str]] = [
    (r"Application command names must be unique", "Discord command collision (disable nativeSkills on one account)."),
    (r"Gateway start blocked: set gateway\.mode=local", "Set gateway.mode=\"local\" for local service usage."),
    (r"refusing to bind gateway .* without auth", "Configure gateway auth before non-loopback bind."),
    (r"another gateway instance is already listening|EADDRINUSE", "Port conflict: stop other process or change port."),
    (r"unknown heartbeat target", "Heartbeat target invalid for runtime routes."),
    (r"heartbeat: unknown accountId", "Heartbeat accountId not configured for target channel."),
    (r"Discord IDs must be strings", "Quote numeric Discord IDs in config."),
    (r"dmPolicy=\"open\" requires .* allowFrom .* \"\*\"", "Open DM policy requires allowFrom to include *."),
    (r"forbidden", "Permission/policy denial (sessions visibility, channel policy, or auth)."),
    (r"pairing", "Pairing gate active; approve sender/device first."),
]


def iter_lines() -> list[str]:
    if len(sys.argv) > 1:
        p = Path(sys.argv[1]).expanduser()
        return p.read_text(encoding="utf-8", errors="replace").splitlines()
    return sys.stdin.read().splitlines()


def main() -> int:
    lines = iter_lines()
    if not lines:
        print("No log input.")
        return 1

    counts: Counter[str] = Counter()
    matched_examples: dict[str, str] = {}

    for line in lines:
        for pattern, hint in SIGNATURES:
            if re.search(pattern, line, flags=re.IGNORECASE):
                counts[hint] += 1
                matched_examples.setdefault(hint, line[:220])

    if not counts:
        print("No known high-signal signatures matched.")
        return 0

    print("OpenClaw log signature summary")
    print("=" * 32)
    for hint, n in counts.most_common():
        print(f"- {n:>3}x  {hint}")
        print(f"      e.g. {matched_examples[hint]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
