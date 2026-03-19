#!/usr/bin/env python3
"""
Git merge driver for posts.json.

Merges by taking the union of all entries (keyed by id), sorted newest-first.
Git calls this as: merge_posts.py %O %A %B
  %O = base version (ancestor)
  %A = ours (current branch) — we write the result here
  %B = theirs (incoming branch)
"""
import json
import sys
from pathlib import Path


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return []


def main():
    _, base_path, ours_path, theirs_path = sys.argv

    base = {p["id"]: p for p in load(base_path)}
    ours = {p["id"]: p for p in load(ours_path)}
    theirs = {p["id"]: p for p in load(theirs_path)}

    merged = {**base, **theirs, **ours}  # ours wins on conflict
    posts = sorted(merged.values(), key=lambda p: p["timestamp"], reverse=True)

    Path(ours_path).write_text(json.dumps(posts, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
