from premerge.coupling import CouplingEngine


def test_strong_coupling_between_cochanged_files(sample_repo):
    engine = CouplingEngine(str(sample_repo), rev="main", use_cache=False)
    assert engine.coupling("auth.py", "session.py") == 1.0


def test_no_coupling_for_unrelated_file(sample_repo):
    engine = CouplingEngine(str(sample_repo), rev="main", use_cache=False)
    assert engine.coupling("auth.py", "unrelated.py") == 0.0


def test_coupling_is_symmetric(sample_repo):
    engine = CouplingEngine(str(sample_repo), rev="main", use_cache=False)
    assert engine.coupling("auth.py", "session.py") == engine.coupling("session.py", "auth.py")


def test_cache_roundtrip(sample_repo):
    engine1 = CouplingEngine(str(sample_repo), rev="main", use_cache=True)
    engine1.build()
    assert (sample_repo / ".premerge_cache.sqlite").exists()

    engine2 = CouplingEngine(str(sample_repo), rev="main", use_cache=True)
    assert engine2.coupling("auth.py", "session.py") == 1.0
