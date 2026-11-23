#!/usr/bin/env python3
"""Generate README badges, statistics, solution index, and topic tables."""
from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
API = "https://codeforces.com/api/problemset.problems"

def replace_section(text, start, end, content):
    if start not in text or end not in text:
        raise SystemExit(f"README markers missing: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n" + content.rstrip() + "\n" + end + after

def rating_bucket(rating):
    if rating is None:
        return "Unrated"
    if rating <= 800:
        return "800"
    if rating <= 1199:
        return "900–1199"
    if rating <= 1399:
        return "1200–1399"
    return "1400+"

def topic_label(tag):
    labels = {
        "math": "Math",
        "implementation": "Implementation",
        "brute force": "Brute Force",
        "strings": "Strings",
        "sortings": "Sorting",
        "greedy": "Greedy",
        "constructive algorithms": "Constructive Algorithms",
        "binary search": "Binary Search",
        "two pointers": "Two Pointers",
        "data structures": "Data Structures",
        "number theory": "Number Theory",
        "graphs": "Graphs",
        "dp": "Dynamic Programming",
    }
    return labels.get(tag, tag.title())

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

    solutions = []
    unmatched = []
    for path in files:
        match = re.match(r"^(\d+)([A-Z][0-9]?)_", path.stem)
        if not match:
            unmatched.append(path)
            continue
        key = (int(match.group(1)), match.group(2))
        problem = problems.get(key)
        if not problem:
            unmatched.append(path)
            continue
        solutions.append({
            "path": path,
            "contest": key[0],
            "index": key[1],
            "name": problem.get("name", path.stem),
            "rating": problem.get("rating"),
            "tags": problem.get("tags", []),
        })

    solutions.sort(key=lambda item: (item["contest"], item["index"]))
    total = len(files)
    matched = len(solutions)

    ratings = Counter(rating_bucket(s["rating"]) for s in solutions)
    rating_order = ["800", "900–1199", "1200–1399", "1400+", "Unrated"]
    topics = defaultdict(list)
    for solution in solutions:
        for tag in solution["tags"]:
            topics[topic_label(tag)].append(solution)

    stats = [
        "<div align=\"center\">",
        "",
        "| <sub>ACCEPTED SOLUTIONS</sub> | <sub>PRIMARY LANGUAGE</sub> | <sub>PROBLEM METADATA</sub> |",
        "|:---:|:---:|:---:|",
        f"| <h2>{total}</h2> | <h2>C++</h2> | <h2>{matched}/{total}</h2> |",
        f"| ![Solutions](https://img.shields.io/badge/solutions-{total}-2ea44f?style=for-the-badge) | ![Language](https://img.shields.io/badge/C%2B%2B-100%25-00599C?style=for-the-badge) | ![Metadata](https://img.shields.io/badge/metadata-matched-8957e5?style=for-the-badge) |",
        "",
        "</div>",
        "",
        "### Difficulty distribution",
        "",
        "| Codeforces rating | Solutions |",
        "|:--|--:|",
    ]
    stats += [f"| {bucket} | {ratings[bucket]} |" for bucket in rating_order if ratings[bucket] or bucket != "Unrated"]
    stats += ["", "### Topic distribution", "", "| Topic | Problems |", "|:--|--:|"]
    stats += [f"| {topic} | {len(items)} |" for topic, items in sorted(topics.items(), key=lambda pair: (-len(pair[1]), pair[0]))]
    stats += ["", "<sub>Generated from repository C++ files and the Codeforces Problemset API. Topic totals overlap when a problem has multiple tags.</sub>"]

    index_rows = [
        "| # | Problem | Contest | Rating | Topics | Solution |",
        "|--:|:--|--:|--:|:--|:--:|",
    ]
    for number, solution in enumerate(solutions, 1):
        contest = solution["contest"]
        index = solution["index"]
        rating = solution["rating"] if solution["rating"] is not None else "—"
        tags = ", ".join(topic_label(tag) for tag in solution["tags"]) or "—"
        name = solution["name"].replace("|", "\\|")
        filename = solution["path"].relative_to(ROOT).as_posix()
        index_rows.append(
            f"| {number} | [{name}](https://codeforces.com/problemset/problem/{contest}/{index}) | {contest} | {rating} | {tags} | [C++]({filename}) |"
        )
    if unmatched:
        index_rows.append("")
        index_rows.append(f"> {len(unmatched)} C++ file(s) could not be matched to Codeforces metadata and are omitted from this index.")

    topic_sections = []
    for topic, items in sorted(topics.items(), key=lambda pair: pair[0].lower()):
        topic_sections += [f"<details>", f"<summary><b>{topic}</b> ({len(items)})</summary>", ""]
        for item in sorted(items, key=lambda s: s["name"].lower()):
            filename = item["path"].relative_to(ROOT).as_posix()
            topic_sections.append(f"- [{item['name']}]({filename})")
        topic_sections += ["", "</details>", ""]

    text = README.read_text(encoding="utf-8")
    text = re.sub(
        r"!\[Solutions\]\(https://img\.shields\.io/badge/solutions-[^)]*\)",
        f"![Solutions](https://img.shields.io/badge/solutions-{total}-2ea44f?style=for-the-badge)",
        text,
        count=1,
    )
    text = replace_section(text, "<!-- STATS:START -->", "<!-- STATS:END -->", "\n".join(stats))
    text = replace_section(text, "<!-- SOLUTIONS:START -->", "<!-- SOLUTIONS:END -->", "\n".join(index_rows))
    text = replace_section(text, "<!-- TOPICS:START -->", "<!-- TOPICS:END -->", "\n".join(topic_sections))
    README.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
