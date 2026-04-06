"""Parse and summarize output from asmap-tool.py diff.

asmap-tool.py diff (bitcoin/contrib/asmap/) produces three line formats:

  "{net} AS{new} # was AS{old}"    — reassignment (prefix in both files)
  "# {net} was AS{old}"            — in file1 only (unassigned in file2)
  "{net} AS{new} # was unassigned" — in file2 only (unassigned in file1)

This script reads those lines and prints aggregate statistics: how many
entries fall into each category, and which ASes appear most frequently.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

RE_REASSIGNMENT = re.compile(r"^(\S+)\s+AS(\d+)\s+#\s+was\s+AS(\d+)$")
RE_REMOVAL = re.compile(r"^#\s+(\S+)\s+was\s+AS(\d+)$")
RE_ADDITION = re.compile(r"^(\S+)\s+AS(\d+)\s+#\s+was\s+unassigned$")


def parse_diff(path):
    """Parse a diff file into three categories of counters.

    Returns (reassignments, removals, additions). Each is a dict with
    'ipv4'/'ipv6' counts and Counter objects keyed by ASN.
    """
    reassignments = {"new": Counter(), "old": Counter(), "ipv4": 0, "ipv6": 0}
    removals = {"old": Counter(), "ipv4": 0, "ipv6": 0}
    additions = {"new": Counter(), "ipv4": 0, "ipv6": 0}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("# Summary") or line.startswith("IPv"):
                continue

            m = RE_REASSIGNMENT.match(line)
            if m:
                ver = "ipv6" if ":" in m.group(1) else "ipv4"
                reassignments["new"][int(m.group(2))] += 1
                reassignments["old"][int(m.group(3))] += 1
                reassignments[ver] += 1
                continue

            m = RE_REMOVAL.match(line)
            if m:
                ver = "ipv6" if ":" in m.group(1) else "ipv4"
                removals["old"][int(m.group(2))] += 1
                removals[ver] += 1
                continue

            m = RE_ADDITION.match(line)
            if m:
                ver = "ipv6" if ":" in m.group(1) else "ipv4"
                additions["new"][int(m.group(2))] += 1
                additions[ver] += 1

    return reassignments, removals, additions


def print_top(counter, label, n=10):
    """Print the top N entries from a Counter."""
    if not counter:
        return
    print(f"  Top ASes ({label}):")
    for asn, count in counter.most_common(n):
        print(f"    AS{asn:<10} {count:>6}")


def print_report(path, reassignments, removals, additions):
    n_reassign = reassignments["ipv4"] + reassignments["ipv6"]
    n_removal = removals["ipv4"] + removals["ipv6"]
    n_addition = additions["ipv4"] + additions["ipv6"]
    total = n_reassign + n_removal + n_addition

    print(f"\n{'='*60}")
    print(f"  {path.name}")
    print(f"{'='*60}")
    print(f"\n  Reassignments:         {n_reassign:>8,}  (prefix in both, different AS)")
    print(f"  Only in file1:         {n_removal:>8,}  (assigned in file1, not in file2)")
    print(f"  Only in file2:         {n_addition:>8,}  (assigned in file2, not in file1)")
    print(f"  Total:                 {total:>8,}")

    if n_reassign:
        print(f"\n--- Reassignments (IPv4: {reassignments['ipv4']:,}  IPv6: {reassignments['ipv6']:,}) ---")
        print_top(reassignments["new"], "new")
        print_top(reassignments["old"], "old")

    if n_removal:
        print(f"\n--- Only in file1 (IPv4: {removals['ipv4']:,}  IPv6: {removals['ipv6']:,}) ---")
        print_top(removals["old"], "AS")

    if n_addition:
        print(f"\n--- Only in file2 (IPv4: {additions['ipv4']:,}  IPv6: {additions['ipv6']:,}) ---")
        print_top(additions["new"], "AS")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize asmap-tool.py diff output files.")
    parser.add_argument("files", nargs="+", type=Path,
                        help="one or more diff output files to analyze")
    args = parser.parse_args()

    for path in args.files:
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            continue
        reassignments, removals, additions = parse_diff(path)
        print_report(path, reassignments, removals, additions)


if __name__ == "__main__":
    main()
