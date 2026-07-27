"""
backtest.fills — slippage + commission model (shared with the paper broker).
============================================================================
Costs are expressed both in price terms (apply_slippage) and in R multiples
(cost_r) so the R-based engines can net them without knowing position size.
Defaults come from configs/execution.json.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .. import config


@dataclass(frozen=True)
class FillModel:
    slippage_bps: float = 0.0        # per side, in basis points of price
    commission_per_share: float = 0.0
    commission_minimum: float = 0.0

    @classmethod
    def from_config(cls, base_dir: Optional[str] = None) -> "FillModel":
        try:
            ex = config.load("execution", base_dir=base_dir)
        except config.ConfigError:
            return cls()
        slip = ex.get("slippage", {})
        comm = ex.get("commission", {})
        return cls(
            slippage_bps=float(slip.get("value", 0)) if slip.get("model") == "bps" else 0.0,
            commission_per_share=float(comm.get("per_share", 0)),
            commission_minimum=float(comm.get("minimum", 0)))

    def apply_slippage(self, price: float, side: str) -> float:
        """Worse fill by slippage_bps: buys fill higher, sells lower."""
        adj = price * self.slippage_bps / 10_000
        return price + adj if side == "buy" else price - adj

    def cost_r(self, entry: float, stop: float) -> float:
        """Round-trip cost in R (fractions of per-share risk): slippage both
        sides + per-share commission. The order-level commission MINIMUM needs
        a position size and is applied by the paper broker, not here."""
        risk = abs(entry - stop)
        if risk <= 0:
            return 0.0
        slip = 2 * entry * self.slippage_bps / 10_000
        comm = 2 * self.commission_per_share
        return (slip + comm) / risk
