import subprocess

from premerge.overlap import compute_overlap


def run(repo, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def test_line_level_overlap_detected(sample_repo):
    repo = sample_repo
    run(repo, "checkout", "-b", "branch-a", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_a(): pass\n")
    run(repo, "commit", "-q", "-am", "branch a edits auth.py")

    run(repo, "checkout", "-b", "branch-b", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_b(): pass\n")
    run(repo, "commit", "-q", "-am", "branch b edits auth.py in the same spot")

    result = compute_overlap(str(repo), "branch-a", "branch-b")
    assert "auth.py" in result.file_overlap
    assert "auth.py" in result.line_overlap_files


def test_no_overlap_for_disjoint_files(sample_repo):
    repo = sample_repo
    run(repo, "checkout", "-b", "branch-c", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_c(): pass\n")
    run(repo, "commit", "-q", "-am", "branch c edits auth.py")

    run(repo, "checkout", "-b", "branch-d", "main")
    (repo / "unrelated.py").write_text("x = 2\n")
    run(repo, "commit", "-q", "-am", "branch d edits unrelated.py")

    result = compute_overlap(str(repo), "branch-c", "branch-d")
    assert result.file_overlap == set()
    assert result.line_overlap_files == set()
