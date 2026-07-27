"""
execution.guard — the fail-closed live-trading gates.
=====================================================
docs/LIVE_TRADING_SAFETY_POLICY.md: live mode requires EVERY gate green, and
even then the shipped live executor refuses to trade. `evaluate_gates` names
every failing gate; tests assert fail-closed for each permutation.
"""
from __future__ import annotations

import glob
import os
from typing import List, Optional

from .. import config


class LiveTradingDisabled(Exception):
    """Raised when any live gate fails — carries the failing gates."""

    def __init__(self, failures: List[str]):
        self.failures = failures
        super().__init__("live trading disabled: " + "; ".join(failures))


def evaluate_gates(base_dir: Optional[str] = None,
                   paper_report_glob: str = "outputs/paper_trading/*report*.md",
                   env: Optional[dict] = None) -> List[str]:
    """Return the list of FAILING gates (empty == all green)."""
    env = os.environ if env is None else env
    failures: List[str] = []
    if env.get("EWAVE_ENABLE_LIVE", "").lower() != "true":
        failures.append("EWAVE_ENABLE_LIVE env flag not 'true'")
    try:
        ex = config.load("execution", base_dir=base_dir)
    except config.ConfigError as e:
        failures.append(f"execution config unreadable ({e})")
        ex = {}
    if ex.get("mode") != "live":
        failures.append("execution.mode is not 'live'")
    try:
        risk = config.load("risk", base_dir=base_dir)
    except config.ConfigError as e:
        failures.append(f"risk config unreadable ({e})")
        risk = {}
    if not risk.get("live_enabled"):
        failures.append("risk.live_enabled is not true")
    for key in ("max_daily_loss_pct", "max_open_positions", "max_symbol_exposure_pct"):
        if not risk.get(key):
            failures.append(f"risk.{key} not configured/non-zero")
    if not glob.glob(paper_report_glob):
        failures.append(f"no paper-trading report found ({paper_report_glob})")
    kill = risk.get("kill_switch_file", "outputs/KILL_SWITCH")
    if os.path.exists(kill):
        failures.append(f"kill switch present ({kill})")
    return failures
