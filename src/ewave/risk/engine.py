"""
risk.engine — the unbypassable approval layer between signals and orders.
=========================================================================
`approve(signal, state)` returns an Approval (with position size + risk
amount) or a Rejection (with the failing control named). The execution layer
must not place an order without a fresh Approval (docs/PAPER_TRADING_POLICY.md
rule 3); tests prove each control blocks.

Controls (configs/risk.json): per-trade risk %, reduced risk below 3
confluence strands (RULESET E-1), max daily/weekly loss, max open positions,
per-symbol and portfolio exposure caps, cooldown after a loss, kill switch =
existence of the configured file (checked on EVERY call, not just startup).
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Dict, Optional

from .. import config


@dataclass
class Approval:
    qty: int
    risk_amount: float
    risk_pct: float
    reason: str = "approved"

    def __bool__(self):
        return True


@dataclass
class Rejection:
    reason: str

    def __bool__(self):
        return False


@dataclass
class PortfolioState:
    """What the risk engine needs to know about the account, kept by the caller
    (paper loop / backtest portfolio)."""
    equity: float
    day_pnl: float = 0.0
    week_pnl: float = 0.0
    open_positions: int = 0
    symbol_exposure: Dict[str, float] = field(default_factory=dict)  # $ by symbol
    portfolio_exposure: float = 0.0                                  # $ total
    bars_since_loss: Optional[int] = None                            # None = no recent loss


class RiskEngine:
    def __init__(self, cfg: Optional[dict] = None, base_dir: Optional[str] = None):
        self.cfg = cfg or config.load("risk", base_dir=base_dir)

    def kill_switch_active(self) -> bool:
        return os.path.exists(self.cfg.get("kill_switch_file", "outputs/KILL_SWITCH"))

    def approve(self, signal, state: PortfolioState):
        c = self.cfg
        if self.kill_switch_active():
            return Rejection("kill switch active "
                             f"({c.get('kill_switch_file')} exists)")
        if state.day_pnl <= -abs(c["max_daily_loss_pct"]) / 100 * state.equity:
            return Rejection(f"daily loss limit reached ({state.day_pnl:+.0f})")
        if state.week_pnl <= -abs(c["max_weekly_loss_pct"]) / 100 * state.equity:
            return Rejection(f"weekly loss limit reached ({state.week_pnl:+.0f})")
        if state.open_positions >= c["max_open_positions"]:
            return Rejection(f"max open positions ({c['max_open_positions']}) reached")
        cooldown = c.get("cooldown_bars_after_loss", 0)
        if (cooldown and state.bars_since_loss is not None
                and state.bars_since_loss < cooldown):
            return Rejection(f"cooldown after loss "
                             f"({state.bars_since_loss}/{cooldown} bars)")
        risk_per_share = abs(signal.entry_price - signal.stop_price)
        if risk_per_share <= 0:
            return Rejection("degenerate stop (risk per share <= 0)")
        risk_pct = c["max_risk_per_trade_pct"]
        if getattr(signal, "confluence_strands", 0) < 3:
            risk_pct = min(risk_pct, c.get("reduced_risk_pct_below_3_strands", risk_pct))
        risk_amount = state.equity * risk_pct / 100
        qty = math.floor(risk_amount / risk_per_share)
        if qty < 1:
            return Rejection(f"risk budget {risk_amount:.0f} < one share of risk "
                             f"({risk_per_share:.2f})")
        notional = qty * signal.entry_price
        sym_cap = c["max_symbol_exposure_pct"] / 100 * state.equity
        if state.symbol_exposure.get(signal.symbol, 0.0) + notional > sym_cap:
            return Rejection(f"symbol exposure cap ({c['max_symbol_exposure_pct']}%)")
        port_cap = c.get("max_portfolio_exposure_pct", 100) / 100 * state.equity
        if state.portfolio_exposure + notional > port_cap:
            return Rejection(f"portfolio exposure cap "
                             f"({c.get('max_portfolio_exposure_pct')}%)")
        return Approval(qty=qty, risk_amount=round(qty * risk_per_share, 2),
                        risk_pct=risk_pct)
