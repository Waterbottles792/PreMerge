"""Historical logical-coupling analysis: files that tend to change together.

coupling(A, B) = |commits touching both A and B| / |commits touching A or B|
(Jaccard similarity of the two files' change-sets across commit history.)
"""

from __future__ import annotations

import itertools
import json
import sqlite3
from collections import Counter
from pathlib import Path

from . import git_utils

CACHE_FILENAME = ".premerge_cache.sqlite"


class CouplingEngine:
    """Computes pairwise file coupling from commit history, with sqlite caching."""

    def __init__(self, repo: str, rev: str = "HEAD", use_cache: bool = True):
        self.repo = repo
        self.rev = rev
        self._use_cache = use_cache
        self._file_counts: Counter[str] | None = None
        self._pair_counts: Counter[tuple[str, str]] | None = None

    def _cache_path(self) -> Path:
        return Path(self.repo) / CACHE_FILENAME

    def _load_from_cache(self, head_hash: str) -> bool:
        if not self._use_cache or not self._cache_path().exists():
            return False
        conn = sqlite3.connect(self._cache_path())
        try:
            row = conn.execute(
                "SELECT file_counts, pair_counts FROM coupling_cache "
                "WHERE head_hash = ? AND rev = ?",
                (head_hash, self.rev),
            ).fetchone()
        finally:
            conn.close()
        if row is None:
            return False
        self._file_counts = Counter(json.loads(row[0]))
        self._pair_counts = Counter(
            {tuple(k.split("\x00")): v for k, v in json.loads(row[1]).items()}
        )
        return True

    def _save_to_cache(self, head_hash: str) -> None:
        if not self._use_cache:
            return
        assert self._file_counts is not None and self._pair_counts is not None
        conn = sqlite3.connect(self._cache_path())
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS coupling_cache ("
                "head_hash TEXT, rev TEXT, file_counts TEXT, pair_counts TEXT, "
                "PRIMARY KEY (head_hash, rev))"
            )
            pair_json = json.dumps(
                {f"{a}\x00{b}": v for (a, b), v in self._pair_counts.items()}
            )
            conn.execute(
                "INSERT OR REPLACE INTO coupling_cache VALUES (?, ?, ?, ?)",
                (head_hash, self.rev, json.dumps(self._file_counts), pair_json),
            )
            conn.commit()
        finally:
            conn.close()

    def build(self) -> None:
        """Build (or load from cache) the file co-occurrence counts.

        The cache key is just the current HEAD hash of `rev` — history is
        treated as append-only, so an unchanged HEAD means an unchanged cache.
        A rebase/force-push that rewrites history without moving HEAD would
        serve a stale entry; delete .premerge_cache.sqlite if that ever bites
        you.
        """
        head_hash = git_utils.rev_parse(self.repo, self.rev)
        if self._load_from_cache(head_hash):
            return

        file_counts: Counter[str] = Counter()
        pair_counts: Counter[tuple[str, str]] = Counter()
        for files in git_utils.commit_log_with_files(self.repo, self.rev):
            unique_files = sorted(set(files))
            for f in unique_files:
                file_counts[f] += 1
            for a, b in itertools.combinations(unique_files, 2):
                pair_counts[(a, b)] += 1

        self._file_counts = file_counts
        self._pair_counts = pair_counts
        self._save_to_cache(head_hash)

    def coupling(self, file_a: str, file_b: str) -> float:
        """Jaccard similarity of the two files' change-sets across history."""
        if self._file_counts is None:
            self.build()
        if file_a == file_b:
            return 1.0
        key = tuple(sorted((file_a, file_b)))
        together = self._pair_counts.get(key, 0)
        if together == 0:
            return 0.0
        either = self._file_counts[file_a] + self._file_counts[file_b] - together
        return together / either if either else 0.0

    def top_coupled_pairs(
        self, files_a: set[str], files_b: set[str], limit: int = 5
    ) -> list[tuple[str, str, float]]:
        """Coupling scores for cross pairs between two file sets, sorted desc."""
        if self._file_counts is None:
            self.build()
        scored = []
        for a in files_a:
            for b in files_b:
                if a == b:
                    continue
                score = self.coupling(a, b)
                if score > 0:
                    scored.append((a, b, score))
        scored.sort(key=lambda t: t[2], reverse=True)
        return scored[:limit]
