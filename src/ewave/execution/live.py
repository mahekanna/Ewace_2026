"""
execution.live — live executor GATES ONLY; fails closed by design.
==================================================================
This repo ships live *infrastructure gates*, not a live executor
(docs/LIVE_TRADING_SAFETY_POLICY.md). `LiveExecutor.start()` raises
`LiveTradingDisabled` naming the first failing gate — and with every gate
green it STILL raises NotImplementedError: enabling real orders requires
writing and reviewing an executor, never flipping a flag.
"""
from __future__ import annotations

from typing import Optional

from .guard import LiveTradingDisabled, evaluate_gates


class LiveExecutor:
    def __init__(self, base_dir: Optional[str] = None, env: Optional[dict] = None):
        self.base_dir = base_dir
        self.env = env

    def start(self):
        failures = evaluate_gates(base_dir=self.base_dir, env=self.env)
        if failures:
            raise LiveTradingDisabled(failures)
        raise NotImplementedError(
            "all live gates are green, but no live executor ships with this repo "
            "— see docs/LIVE_TRADING_SAFETY_POLICY.md")
