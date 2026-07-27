import subprocess

from premerge.config import Weights
from premerge.coupling import CouplingEngine
from premerge.scoring import compute_risk


def run(repo, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def test_overlapping_branches_score_higher_than_disjoint(sample_repo):
    repo = sample_repo

    run(repo, "checkout", "-b", "risky-a", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_a(): pass\n")
    run(repo, "commit", "-q", "-am", "risky a edits auth.py")

    run(repo, "checkout", "-b", "risky-b", "main")
    (repo / "auth.py").write_text("def login_v0(): pass\ndef new_b(): pass\n")
    run(repo, "commit", "-q", "-am", "risky b edits auth.py in the same spot")

    run(repo, "checkout", "-b", "safe-a", "main")
    (repo / "unrelated.py").write_text("x = 100\n")
    run(repo, "commit", "-q", "-am", "safe a edits an unrelated file")

    weights = Weights()
    engine = CouplingEngine(str(repo), rev="main", use_cache=False)

    risky_score = compute_risk(str(repo), "risky-a", "risky-b", weights, engine)
    safe_score = compute_risk(str(repo), "main", "safe-a", weights, engine)

    assert risky_score.score > safe_score.score
    assert "auth.py" in risky_score.line_overlap_files
