"""
execution.paper — the paper broker + the replay paper-trading loop.
===================================================================
Honest fills (docs/PAPER_TRADING_POLICY.md rule 4): market orders fill at the
NEXT bar's open plus slippage — never at the signal bar's close; stop/target
exits fill at their level when it trades intra-bar (or at the open when price
gaps through). Order-level commission (incl. the account minimum) applies at
fill time. Everything appends to JSONL ledgers.

`replay_paper` drives the same loop from cached bars (deterministic, offline —
what `ewave paper-trade --replay` runs and the sandbox can test); a live-poll
loop on the user's machine would feed the same broker new bars instead.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from ..backtest.fills import FillModel
from ..risk.engine import PortfolioState, RiskEngine
from ..rules.profiles import Profile
from ..signals import wave3
from .broker import BrokerInterface, Order, OrderState, OrderType, Position


class PaperBroker(BrokerInterface):
    def __init__(self, fill_model: Optional[FillModel] = None,
                 ledger_dir: Optional[str] = None):
        self.fills = fill_model or FillModel()
        self.ledger_dir = Path(ledger_dir) if ledger_dir else None
        self._orders: Dict[str, Order] = {}
        self._positions: Dict[str, Position] = {}
        self._seq = 0

    # ------------------------- interface -------------------------
    def submit(self, order: Order) -> Order:
        order.state = OrderState.SUBMITTED
        self._orders[order.order_id] = order
        order.state = OrderState.ACCEPTED
        self._ledger("orders", asdict_order(order))
        return order

    def cancel(self, order_id: str) -> Optional[Order]:
        o = self._orders.get(order_id)
        if o and o.state in (OrderState.SUBMITTED, OrderState.ACCEPTED):
            o.state = OrderState.CANCELLED
            self._ledger("orders", asdict_order(o))
        return o

    def positions(self) -> Dict[str, Position]:
        return dict(self._positions)

    def open_orders(self) -> List[Order]:
        return [o for o in self._orders.values()
                if o.state in (OrderState.SUBMITTED, OrderState.ACCEPTED)]

    def next_id(self) -> str:
        self._seq += 1
        return f"P{self._seq:06d}"

    # ------------------------- bar processing -------------------------
    def on_bar(self, symbol: str, bar) -> List[dict]:
        """Advance one bar: fill open orders, check position exits.
        Returns realized-trade events [{symbol, qty, pnl, exit_kind, t}]."""
        t, o, h, l, c = bar[0], bar[1], bar[2], bar[3], bar[4]
        events: List[dict] = []
        for order in list(self.open_orders()):
            if order.symbol != symbol:
                continue
            fill = None
            if order.order_type is OrderType.MARKET:
                fill = self.fills.apply_slippage(o, order.side)
            elif order.order_type is OrderType.STOP and order.stop_price is not None:
                trig = (h >= order.stop_price if order.side == "buy"
                        else l <= order.stop_price)
                if trig:
                    base = max(order.stop_price, o) if order.side == "buy" \
                        else min(order.stop_price, o)
                    fill = self.fills.apply_slippage(base, order.side)
            elif order.order_type is OrderType.LIMIT and order.limit_price is not None:
                trig = (l <= order.limit_price if order.side == "buy"
                        else h >= order.limit_price)
                if trig:
                    fill = order.limit_price
            if fill is None:
                continue
            order.state = OrderState.FILLED
            order.filled_t, order.fill_price = t, round(fill, 4)
            self._ledger("fills", asdict_order(order))
            events += self._apply_fill(order, t)
        events += self._check_exits(symbol, bar)
        return events

    def _apply_fill(self, order: Order, t: float) -> List[dict]:
        signed = order.qty if order.side == "buy" else -order.qty
        pos = self._positions.get(order.symbol)
        if pos is None:
            self._positions[order.symbol] = Position(
                symbol=order.symbol, qty=signed, avg_price=order.fill_price,
                signal_id=order.signal_id, opened_t=t,
                stop=order.attach_stop, target=order.attach_target)
            self._ledger("positions", asdict(self._positions[order.symbol]))
            return []
        # closing / reducing
        pnl = (order.fill_price - pos.avg_price) * min(abs(signed), abs(pos.qty)) \
            * (1 if pos.qty > 0 else -1)
        pnl -= self._commission(order)
        pos.qty += signed
        events = [{"symbol": order.symbol, "qty": order.qty, "pnl": round(pnl, 2),
                   "exit_kind": order.note or "close", "t": t,
                   "signal_id": pos.signal_id}]
        if pos.qty == 0:
            del self._positions[order.symbol]
        self._ledger("positions", {"symbol": order.symbol, "qty": pos.qty,
                                   "t": t, "pnl_realized": round(pnl, 2)})
        return events

    def _check_exits(self, symbol: str, bar) -> List[dict]:
        pos = self._positions.get(symbol)
        if pos is None or pos.stop is None:
            return []
        t, o, h, l = bar[0], bar[1], bar[2], bar[3]
        long = pos.qty > 0
        exit_price = exit_kind = None
        # conservative ordering: stop checked before target within a bar
        if (l <= pos.stop) if long else (h >= pos.stop):
            base = min(pos.stop, o) if long else max(pos.stop, o)   # gap-through honesty
            exit_price = self.fills.apply_slippage(base, "sell" if long else "buy")
            exit_kind = "stop"
        elif pos.target is not None and ((h >= pos.target) if long else (l <= pos.target)):
            exit_price = pos.target
            exit_kind = "target"
        if exit_price is None:
            return []
        order = Order(self.next_id(), symbol, "sell" if long else "buy",
                      abs(pos.qty), OrderType.MARKET, signal_id=pos.signal_id,
                      note=exit_kind)
        order.state = OrderState.FILLED
        order.filled_t, order.fill_price = t, round(exit_price, 4)
        self._ledger("fills", asdict_order(order))
        return self._apply_fill(order, t)

    def flatten_all(self, prices: Dict[str, float], t: float) -> List[dict]:
        """Emergency close every position at the given prices (kill switch)."""
        events = []
        for sym, pos in list(self._positions.items()):
            long = pos.qty > 0
            order = Order(self.next_id(), sym, "sell" if long else "buy",
                          abs(pos.qty), OrderType.MARKET, signal_id=pos.signal_id,
                          note="kill_switch_flatten")
            order.state = OrderState.FILLED
            order.filled_t = t
            order.fill_price = round(self.fills.apply_slippage(
                prices.get(sym, pos.avg_price), "sell" if long else "buy"), 4)
            self._ledger("fills", asdict_order(order))
            events += self._apply_fill(order, t)
        return events

    def _commission(self, order: Order) -> float:
        return max(self.fills.commission_per_share * order.qty,
                   self.fills.commission_minimum) * 2   # round trip, order-level min

    def _ledger(self, name: str, row: dict) -> None:
        if not self.ledger_dir:
            return
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_dir / f"{name}.jsonl", "a") as f:
            f.write(json.dumps(row) + "\n")


def asdict_order(o: Order) -> dict:
    d = asdict(o)
    d["order_type"] = o.order_type.value
    d["state"] = o.state.value
    return d


def replay_paper(symbol_bars: Dict[str, list], profile: Profile,
                 risk: RiskEngine, broker: PaperBroker, *,
                 roll: int = 400, start: int = 400,
                 report_dir: Optional[str] = None) -> dict:
    """Deterministic replay paper loop over cached bars (one timeframe).

    Per bar (per symbol): kill-switch check → broker.on_bar (fills/exits) →
    signal on window ≤ t → risk approval → market order for the NEXT bar.
    Returns the campaign summary; writes daily_report.md when report_dir set.
    """
    state = PortfolioState(equity=float(risk.cfg.get("account_equity", 100000)))
    signals_seen = orders_placed = rejected = 0
    rejections: List[str] = []
    trades: List[dict] = []
    halted = False
    n = min(len(b) for b in symbol_bars.values())
    day = None
    for t in range(start, n):
        if risk.kill_switch_active():
            prices = {s: b[t][1] for s, b in symbol_bars.items()}
            for ev in broker.flatten_all(prices, list(symbol_bars.values())[0][t][0]):
                state.equity += ev["pnl"]
            halted = True
            break
        for sym, bars in symbol_bars.items():
            bar = bars[t]
            bar_day = datetime.fromtimestamp(bar[0], timezone.utc).date()
            if day != bar_day:
                day, state.day_pnl = bar_day, 0.0
            for ev in broker.on_bar(sym, bar):
                state.equity += ev["pnl"]
                state.day_pnl += ev["pnl"]
                state.week_pnl += ev["pnl"]
                state.bars_since_loss = 0 if ev["pnl"] < 0 else state.bars_since_loss
                trades.append(ev)
            if sym in broker.positions() or any(
                    o.symbol == sym for o in broker.open_orders()):
                continue                        # one position/order per symbol
            sigs = wave3.generate(bars[max(0, t - roll):t + 1], profile,
                                  symbol=sym, timeframe="")
            if not sigs:
                continue
            signals_seen += 1
            sig = sigs[0]
            state.open_positions = len(broker.positions())
            state.symbol_exposure = {s: p.notional
                                     for s, p in broker.positions().items()}
            state.portfolio_exposure = sum(state.symbol_exposure.values())
            verdict = risk.approve(sig, state)
            if not verdict:
                rejected += 1
                rejections.append(f"{sym}: {verdict.reason}")
                continue
            order = Order(broker.next_id(), sym,
                          "buy" if sig.direction == "long" else "sell",
                          verdict.qty, OrderType.MARKET, signal_id=sig.signal_id,
                          attach_stop=sig.stop_price, attach_target=sig.target_1)
            order.submitted_t = bar[0]
            broker.submit(order)
            orders_placed += 1
        if state.bars_since_loss is not None:   # once per bar, not per symbol
            state.bars_since_loss += 1
    summary = {
        "bars_replayed": n - start, "signals_seen": signals_seen,
        "orders_placed": orders_placed, "rejected_by_risk": rejected,
        "trades_closed": len(trades),
        "realized_pnl": round(sum(tr["pnl"] for tr in trades), 2),
        "final_equity": round(state.equity, 2),
        "open_positions": len(broker.positions()),
        "halted_by_kill_switch": halted,
        "rejections": rejections[:20],
    }
    if report_dir:
        _daily_report(summary, trades, report_dir)
    return summary


def _daily_report(summary: dict, trades: List[dict], report_dir) -> None:
    p = Path(report_dir)
    p.mkdir(parents=True, exist_ok=True)
    lines = ["# Paper trading report", "",
             f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC — replay mode._", ""]
    lines += [f"- {k}: **{v}**" for k, v in summary.items() if k != "rejections"]
    if summary["rejections"]:
        lines += ["", "## Risk rejections (first 20)"]
        lines += [f"- {r}" for r in summary["rejections"]]
    if trades:
        lines += ["", "## Closed trades", "| t | symbol | qty | pnl | exit |", "|---|---|---|---|---|"]
        for tr in trades[:50]:
            lines.append(f"| {datetime.fromtimestamp(tr['t'], timezone.utc):%Y-%m-%d %H:%M} "
                         f"| {tr['symbol']} | {tr['qty']} | {tr['pnl']:+.2f} | {tr['exit_kind']} |")
    (p / "daily_report.md").write_text("\n".join(lines) + "\n")
