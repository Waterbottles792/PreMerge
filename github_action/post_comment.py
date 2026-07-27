"""Posts (or updates) a PreMerge risk report as a PR comment.

Uses only the stdlib (urllib) against the GitHub REST API — no `requests`
dependency needed for a handful of HTTP calls.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

MARKER = "<!-- premerge-report -->"


def _api_request(url: str, token: str, method: str = "GET", data: dict | None = None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else None


def build_comment_body(report: list[dict]) -> str:
    if not report:
        return f"{MARKER}\n### PreMerge Conflict Risk Report\n\nNo other branches to compare — no risk detected."

    lines = [
        MARKER,
        "### PreMerge Conflict Risk Report",
        "",
        "| Branch A | Branch B | Risk | Why |",
        "|---|---|---|---|",
    ]
    for entry in report:
        why = entry["explanations"][0] if entry["explanations"] else "no overlap or coupling detected"
        risk = entry["score"]
        emoji = "\U0001F534" if risk >= 0.5 else "\U0001F7E1" if risk >= 0.2 else "\U0001F7E2"
        lines.append(f"| {entry['branch_a']} | {entry['branch_b']} | {emoji} {risk:.2f} | {why} |")
    return "\n".join(lines)


def main() -> None:
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["REPO"]
    pr_number = os.environ["PR_NUMBER"]
    report_path = os.environ.get("REPORT_PATH", "premerge_report.json")

    with open(report_path) as f:
        report = json.load(f)

    body = build_comment_body(report)
    comments_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    try:
        existing = _api_request(comments_url, token) or []
    except urllib.error.HTTPError:
        existing = []
    bot_comment = next((c for c in existing if MARKER in c.get("body", "")), None)

    if bot_comment:
        update_url = f"https://api.github.com/repos/{repo}/issues/comments/{bot_comment['id']}"
        _api_request(update_url, token, method="PATCH", data={"body": body})
    else:
        _api_request(comments_url, token, method="POST", data={"body": body})


if __name__ == "__main__":
    main()
