"""Tests for report rendering and the GitHub Action comment poster."""

import importlib.util
import io
import json
from pathlib import Path

from rich.console import Console

from premerge.report import print_table, to_json
from premerge.scoring import RiskScore

_spec = importlib.util.spec_from_file_location(
    "post_comment", Path(__file__).parent.parent / "github_action" / "post_comment.py"
)
post_comment = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(post_comment)


def _render(scores):
    buf = io.StringIO()
    print_table(scores, Console(file=buf, width=200, force_terminal=False))
    return buf.getvalue()


def _score(a, b, score, why):
    return RiskScore(a, b, score, set(), set(), [], why)


def test_table_headers_and_rows():
    out = _render([_score("a", "b", 0.8, ["x.py: both branches edit overlapping lines"])])
    for header in ("PreMerge Conflict Risk Report", "Branch A", "Branch B", "Risk", "Why"):
        assert header in out
    assert "0.80" in out and "x.py: both branches edit overlapping lines" in out


def test_table_empty_and_no_explanation_messages():
    assert "No branch pairs to analyze." in _render([])
    assert "no overlap or coupling detected" in _render([_score("a", "b", 0.0, [])])


def test_table_summarises_extra_explanations_and_lists_them():
    out = _render([_score("a", "b", 0.5, ["first", "second", "third"])])
    assert "first (+2 more)" in out
    assert "a vs b (risk=0.50):" in out and "  - second" in out and "  - third" in out


def test_json_values_roundtrip():
    s = RiskScore("a", "b", 0.5, {"y.py", "x.py"}, {"x.py"}, [("p", "q", 0.25)], ["why"])
    e = json.loads(to_json([s]))[0]
    assert e["branch_a"] == "a" and e["branch_b"] == "b" and e["score"] == 0.5
    assert e["file_overlap"] == ["x.py", "y.py"] and e["line_overlap_files"] == ["x.py"]
    assert e["explanations"] == ["why"]


def test_comment_body_has_marker_table_and_risk_emoji():
    report = [
        {"branch_a": "a", "branch_b": "b", "score": 0.8, "explanations": ["hot"]},
        {"branch_a": "a", "branch_b": "c", "score": 0.2, "explanations": ["warm"]},
        {"branch_a": "a", "branch_b": "d", "score": 0.0, "explanations": []},
    ]
    body = post_comment.build_comment_body(report)
    assert body.startswith(post_comment.MARKER)
    assert "| Branch A | Branch B | Risk | Why |" in body
    assert "\U0001F534 0.80" in body and "\U0001F7E1 0.20" in body and "\U0001F7E2 0.00" in body
    assert "no overlap or coupling detected" in body


def test_comment_body_empty_report():
    body = post_comment.build_comment_body([])
    assert post_comment.MARKER in body and "no risk detected" in body


def _run_main(monkeypatch, tmp_path, existing):
    calls = []
    rp = tmp_path / "r.json"
    rp.write_text("[]")
    for k, v in {"GITHUB_TOKEN": "t", "REPO": "o/r", "PR_NUMBER": "7", "REPORT_PATH": str(rp)}.items():
        monkeypatch.setenv(k, v)

    def fake(url, token, method="GET", data=None):
        calls.append((method, url))
        return existing if method == "GET" else None

    monkeypatch.setattr(post_comment, "_api_request", fake)
    post_comment.main()
    return calls


def test_main_creates_comment_when_none_exists(monkeypatch, tmp_path):
    calls = _run_main(monkeypatch, tmp_path, [{"id": 1, "body": "unrelated"}])
    assert calls[-1] == ("POST", "https://api.github.com/repos/o/r/issues/7/comments")


def test_main_updates_existing_comment_in_place(monkeypatch, tmp_path):
    calls = _run_main(monkeypatch, tmp_path, [{"id": 42, "body": post_comment.MARKER + " old"}])
    assert calls[-1] == ("PATCH", "https://api.github.com/repos/o/r/issues/comments/42")
    assert not any(m == "POST" for m, _ in calls)
