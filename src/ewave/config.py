"""
config.py — JSON-first configuration loader.
============================================
Canonical configs are JSON files under `configs/` (repo root). A sibling `.yaml`
with the same stem is honoured when PyYAML is installed (guarded import) and the
`.json` is absent — JSON always wins when both exist, so the committed canonical
files stay authoritative.

Resolution order for the config directory:
  1. explicit `base_dir` argument
  2. $EWAVE_CONFIG_DIR
  3. ./configs relative to the current working directory
  4. <repo root>/configs found by walking up from this file (source checkouts)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional


class ConfigError(Exception):
    """A config file is missing or malformed."""


def config_dir(base_dir: Optional[str] = None) -> Path:
    if base_dir:
        return Path(base_dir)
    env = os.environ.get("EWAVE_CONFIG_DIR")
    if env:
        return Path(env)
    cwd = Path.cwd() / "configs"
    if cwd.is_dir():
        return cwd
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / "configs"
        if cand.is_dir():
            return cand
    return cwd  # best effort; load() gives a clear error if it doesn't exist


def load(name: str, base_dir: Optional[str] = None) -> Any:
    """Load `configs/<name>.json` (or `.yaml` fallback). `name` may also be a
    direct path to a .json/.yaml file."""
    p = Path(name)
    if p.suffix in (".json", ".yaml", ".yml") and p.exists():
        return _read(p)
    d = config_dir(base_dir)
    for cand in (d / f"{name}.json", d / f"{name}.yaml", d / f"{name}.yml"):
        if cand.exists():
            return _read(cand)
    raise ConfigError(f"no config '{name}' under {d} (looked for .json/.yaml)")


def _read(path: Path) -> Any:
    text = path.read_text()
    if path.suffix == ".json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ConfigError(f"{path}: invalid JSON: {e}") from e
    try:
        import yaml  # optional extra: pip install ewave[yaml]
    except ImportError as e:
        raise ConfigError(
            f"{path} is YAML but PyYAML is not installed; use the .json form "
            "or `pip install ewave[yaml]`") from e
    return yaml.safe_load(text)
