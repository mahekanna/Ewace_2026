"""Handler for `ewave paper-trade` (replay mode; live-poll is a user-machine mode)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone

from .. import config
from ..backtest.fills import FillModel
from ..data.store import Store
from ..risk.engine import RiskEngine
from ..rules.profiles import get_profile
from ..scanner.batch import resolve_watchlist
from .paper import PaperBroker, replay_paper


def cmd_paper_trade(args) -> int:
    try:
        profile = get_profile(args.profile)
        symbols = resolve_watchlist(args)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    if not args.replay:
        print("paper-trade: live-poll mode needs a machine with data access; "
              "use --replay here (cached bars, deterministic).", file=sys.stderr)
        return 2
    store = Store()
    symbol_bars = {}
    for sym in symbols:
        try:
            bars = store.read(sym, args.tf).tuples()
        except FileNotFoundError as e:
            print(f"{sym}: {e}", file=sys.stderr)
            continue
        if args.days:
            cutoff = bars[-1][0] - args.days * 86400
            kept = [b for b in bars if b[0] >= cutoff]
            # keep a rolling-window head so signals exist from day one
            head = bars[max(0, len(bars) - len(kept) - 400):len(bars) - len(kept)]
            bars = head + kept
        symbol_bars[sym] = bars
    if not symbol_bars:
        print("paper-trade: no data", file=sys.stderr)
        return 2
    risk = RiskEngine()
    broker = PaperBroker(FillModel.from_config(), ledger_dir="outputs/paper_trading")
    summary = replay_paper(symbol_bars, profile, risk, broker,
                           report_dir="outputs/paper_trading")
    print(f"paper-trade --replay [{profile.name}] {','.join(symbol_bars)} @ {args.tf}")
    for k, v in summary.items():
        if k != "rejections":
            print(f"  {k}: {v}")
    if summary["halted_by_kill_switch"]:
        print("  !! halted by kill switch", file=sys.stderr)
    print("ledgers + daily_report.md -> outputs/paper_trading/")
    return 0
