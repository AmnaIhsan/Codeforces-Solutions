#!/usr/bin/env python3
"""Refresh the repository statistics block in README.md from tracked C++ solutions."""
from collections import Counter
from pathlib import Path
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
API = "https://codeforces.com/api/problemset.problems"

def main():
    files = sorted(p for p in ROOT.rglob("*.cpp") if ".git" not in p.parts)
    if not files:
        raise SystemExit("No C++ solution files found.")

    request = urllib.request.Request(API, headers={"User-Agent": "Codeforces-Solutions-README-Bot/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("status") != "OK":
        raise SystemExit("Codeforces API did not return OK.")

    problems = {
        (p.get("contestId"), p.get("index")): p
        for p in payload["result"]["problems"]
    }
    ratings = Counter()
    matched = 0
    for path in files:
        match = re.match(r"^(\d+)([A-Z][0-9]?)_", path.stem)
        if not match:
            continue
        problem = problems.get((int(match.group(1)), match.group(2)))
        if not problem:
            continue
        matched += 1
        rating = problem.get("rating")
        if rating is not None:
            if rating <= 800:
                ratings["800"] += 1
            elif rating <= 1199:
                ratings["900–1199"] += 1
            elif rating <= 1399:
                ratings["1200–1399"] += 1
            else:
                ratings["1400+"] += 1

    total = len(files)
    buckets = [("800", ratings["800"]), ("900–1199", ratings["900–1199"]),
               ("1200–1399", ratings["1200–1399"]), ("1400+", ratings["1400+"])]
    rows = "\n".join(
        f'| {label} | {count} |'
        for label, count in buckets
    )
    dashboard = f"""<div align="center">

| <sub>ACCEPTED SOLUTIONS</sub> | <sub>PRIMARY LANGUAGE</sub> | <sub>PROBLEM METADATA</sub> |
|:---:|:---:|:---:|
| <h2>{total}</h2> | <h2>C++</h2> | <h2>{matched}/{total}</h2> |
| ![Solutions](https://img.shields.io/badge/solutions-{total}-2ea44f?style=for-the-badge) | ![Language](https://img.shields.io/badge/C%2B%2B-100%25-00599C?style=for-the-badge) | ![Metadata](https://img.shields.io/badge/metadata-matched-8957e5?style=for-the-badge) |

</div>

| Codeforces rating | Solutions |
|:--|--:|
{rows}

<sub>Generated from repository C++ files and the Codeforces Problemset API. Unrated or unmatched files are not included in rating buckets.</sub>"""
    text = README.read_text(encoding="utf-8")
    start = "<!-- STATS:START -->"
    end = "<!-- STATS:END -->"
    if start not in text or end not in text:
        raise SystemExit("README statistics markers are missing.")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    updated = before + start + "\n" + dashboard + "\n" + end + after
    if updated != text:
        README.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    main()
