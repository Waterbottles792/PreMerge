"""Regression tests pinning behaviour of units that were previously untested."""

import json

from premerge.config import Weights, load_weights
from premerge.git_utils import commit_log_with_files, diff_hunks, merge_base
from premerge.overlap import _ranges_intersect
from premerge.report import to_json
from premerge.scoring import RiskScore
from tests.conftest import run


def test_ranges_intersect_boundaries():
    assert _ranges_intersect((10, 5), (14, 3))        # overlap on one line
    assert not _ranges_intersect((10, 5), (15, 3))    # adjacent, not overlapping
    assert _ranges_intersect((1, 100), (50, 1))       # containment
    assert not _ranges_intersect((20, 2), (1, 5))     # disjoint


def test_pure_deletion_hunk_counts_as_one_line(sample_repo):
    run(sample_repo, "checkout", "-q", "-b", "del", "main")
    (sample_repo / "auth.py").write_text("")
    run(sample_repo, "commit", "-q", "-am", "delete all lines")
    base = merge_base(str(sample_repo), "main", "del")
    d = diff_hunks(str(sample_repo), base, "del")
    assert d.files == {"auth.py"}
    assert all(length >= 1 for _, length in d.hunks["auth.py"])


def test_binary_file_is_file_level_only(sample_repo):
    for b in ("bin-a", "bin-b"):
        run(sample_repo, "checkout", "-q", "-b", b, "main")
        (sample_repo / "logo.bin").write_bytes(b"\x00\x01" + b.encode())
        run(sample_repo, "add", "-A")
        run(sample_repo, "commit", "-q", "-m", b)
    from premerge.overlap import compute_overlap
    res = compute_overlap(str(sample_repo), "bin-a", "bin-b")
    assert "logo.bin" in res.file_overlap
    assert "logo.bin" not in res.line_overlap_files


def test_commit_log_skips_merge_commits(sample_repo):
    run(sample_repo, "checkout", "-q", "-b", "side", "main")
    (sample_repo / "side.py").write_text("s = 1\n")
    run(sample_repo, "add", "-A")
    run(sample_repo, "commit", "-q", "-m", "side")
    run(sample_repo, "checkout", "-q", "main")
    run(sample_repo, "merge", "-q", "--no-ff", "-m", "merge side", "side")
    commits = commit_log_with_files(str(sample_repo), "main")
    assert len(commits) == 6   # 4 rounds + unrelated + side; merge commit excluded


def test_config_defaults_partial_and_missing(tmp_path):
    assert load_weights(str(tmp_path)) == Weights()
    (tmp_path / "premerge.config.json").write_text(json.dumps({"weights": {"coupling": 0.9}}))
    w = load_weights(str(tmp_path))
    assert (w.line_overlap, w.file_overlap, w.coupling) == (0.5, 0.3, 0.9)


def test_json_report_schema():
    s = RiskScore("a", "b", 0.5, {"x.py"}, {"x.py"}, [("x.py", "y.py", 0.5)], ["why"])
    entry = json.loads(to_json([s]))[0]
    assert set(entry) == {"branch_a", "branch_b", "score", "file_overlap",
                          "line_overlap_files", "coupled_pairs", "explanations"}
    assert entry["coupled_pairs"] == [{"file_a": "x.py", "file_b": "y.py", "coupling": 0.5}]


def test_file_overlap_without_line_overlap_scores_lower(sample_repo):
    from premerge.coupling import CouplingEngine
    from premerge.scoring import compute_risk
    (sample_repo / "auth.py").write_text("".join(f"line{i}\n" for i in range(60)))
    run(sample_repo, "commit", "-q", "-am", "long auth")
    run(sample_repo, "checkout", "-q", "-b", "top", "main")
    (sample_repo / "auth.py").write_text("TOP\n" + "".join(f"line{i}\n" for i in range(1, 60)))
    run(sample_repo, "commit", "-q", "-am", "edit top")
    run(sample_repo, "checkout", "-q", "-b", "bottom", "main")
    (sample_repo / "auth.py").write_text("".join(f"line{i}\n" for i in range(59)) + "BOTTOM\n")
    run(sample_repo, "commit", "-q", "-am", "edit bottom")
    eng = CouplingEngine(str(sample_repo), rev="main", use_cache=False)
    r = compute_risk(str(sample_repo), "top", "bottom", Weights(), eng)
    assert "auth.py" in r.file_overlap and "auth.py" not in r.line_overlap_files
    assert r.score == round(Weights().file_overlap * 1.0, 4)
