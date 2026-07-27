"""Loads premerge.config.json, falling back to sensible defaults."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILENAME = "premerge.config.json"


@dataclass
class Weights:
    line_overlap: float = 0.5
    file_overlap: float = 0.3
    coupling: float = 0.2


def load_weights(repo: str, config_path: str | None = None) -> Weights:
    """Read `weights` from premerge.config.json if present, else use defaults."""
    path = Path(config_path) if config_path else Path(repo) / CONFIG_FILENAME
    if not path.exists():
        return Weights()
    data = json.loads(path.read_text())
    weights = data.get("weights", {})
    defaults = Weights()
    return Weights(
        line_overlap=weights.get("line_overlap", defaults.line_overlap),
        file_overlap=weights.get("file_overlap", defaults.file_overlap),
        coupling=weights.get("coupling", defaults.coupling),
    )
