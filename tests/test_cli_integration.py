"""End-to-end tests: drive the real `premerge analyze` CLI against synthetic repos."""

import json
import subprocess

from click.testing import CliRunner

from premerge.cli import main


def run(repo, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _make_conflicting_branches(repo):
    run(repo, "checkout", "-q", "-b", "feature-a", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_a(): pass\n")
    run(repo, "commit", "-q", "-am", "a edits auth.py")
    run(repo, "checkout", "-q", "-b", "feature-b", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_b(): pass\n")
    run(repo, "commit", "-q", "-am", "b edits auth.py same spot")
    run(repo, "checkout", "-q", "main")


def _make_hidden_coupling_branches(repo):
    run(repo, "checkout", "-q", "-b", "touch-auth", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef extra(): pass\n")
    run(repo, "commit", "-q", "-am", "touch auth only")
    run(repo, "checkout", "-q", "-b", "touch-session", "main")
    (repo / "session.py").write_text("def refresh_v0(): pass\ndef extra(): pass\n")
    run(repo, "commit", "-q", "-am", "touch session only")
    run(repo, "checkout", "-q", "main")


def test_cli_pair_json_reports_line_overlap(sample_repo):
    _make_conflicting_branches(sample_repo)
    result = CliRunner().invoke(
        main, ["analyze", "feature-a", "feature-b", "--repo", str(sample_repo), "--json"]
    )
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert len(report) == 1
    assert report[0]["line_overlap_files"] == ["auth.py"]
    assert report[0]["score"] >= 0.5


def test_cli_detects_hidden_coupling_without_file_overlap(sample_repo):
    _make_hidden_coupling_branches(sample_repo)
    result = CliRunner().invoke(
        main, ["analyze", "touch-auth", "touch-session", "--repo", str(sample_repo), "--json"]
    )
    assert result.exit_code == 0, result.output
    entry = json.loads(result.output)[0]
    assert entry["file_overlap"] == []
    assert entry["coupled_pairs"] and entry["coupled_pairs"][0]["coupling"] > 0
    assert entry["score"] > 0


def test_cli_all_pairs_ranked_highest_risk_first(sample_repo):
    _make_conflicting_branches(sample_repo)
    run(sample_repo, "checkout", "-q", "-b", "safe", "main")
    (sample_repo / "unrelated.py").write_text("x = 99\n")
    run(sample_repo, "commit", "-q", "-am", "safe change")
    result = CliRunner().invoke(main, ["analyze", "--repo", str(sample_repo), "--json"])
    assert result.exit_code == 0, result.output
    scores = [e["score"] for e in json.loads(result.output)]
    assert scores == sorted(scores, reverse=True)
    assert len(scores) == 6  # C(4,2) pairs over main, feature-a, feature-b, safe


def test_cli_base_mode_compares_every_branch_to_base(sample_repo):
    _make_conflicting_branches(sample_repo)
    result = CliRunner().invoke(
        main, ["analyze", "--base", "main", "--repo", str(sample_repo), "--json"]
    )
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert {e["branch_b"] for e in report} == {"feature-a", "feature-b"}


def test_cli_table_output_renders_title_and_branches(sample_repo):
    _make_conflicting_branches(sample_repo)
    result = CliRunner().invoke(
        main, ["analyze", "feature-a", "feature-b", "--repo", str(sample_repo)]
    )
    assert result.exit_code == 0, result.output
    assert "PreMerge Conflict Risk Report" in result.output
    assert "feature-a" in result.output and "overlapping lines" in result.output


def test_cli_no_other_branches_message(sample_repo):
    result = CliRunner().invoke(
        main, ["analyze", "--base", "main", "--repo", str(sample_repo)]
    )
    assert result.exit_code == 0
    assert "No other branches" in result.output


def test_cli_custom_config_changes_score(sample_repo, tmp_path):
    _make_conflicting_branches(sample_repo)
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"weights": {"line_overlap": 0.0, "file_overlap": 0.0, "coupling": 0.0}}))
    result = CliRunner().invoke(
        main,
        ["analyze", "feature-a", "feature-b", "--repo", str(sample_repo), "--json",
         "--config", str(cfg)],
    )
    assert json.loads(result.output)[0]["score"] == 0.0


def test_cli_warm_cache_gives_same_result_as_cold(sample_repo):
    _make_hidden_coupling_branches(sample_repo)
    args = ["analyze", "touch-auth", "touch-session", "--repo", str(sample_repo), "--json"]
    cold = CliRunner().invoke(main, args + ["--no-cache"]).output
    first = CliRunner().invoke(main, args).output   # writes cache
    warm = CliRunner().invoke(main, args).output    # reads cache
    assert cold == first == warm
