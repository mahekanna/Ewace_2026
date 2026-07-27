"""Handler for `ewave backtest` — the profile-driven wave-3 trade backtest."""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .. import config
from ..data.store import Store
from ..rules.profiles import get_profile
from .engine import backtest_wave3
from .fills import FillModel
from .metrics import equity_curve, summarize


def _slice(bars, start, end):
    def ts(s, end_of_day=False):
        t = int(datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp())
        return t + 86399 if end_of_day else t
    if start:
        bars = [b for b in bars if b[0] >= ts(start)]
    if end:
        bars = [b for b in bars if b[0] <= ts(end, True)]
    return bars


def cmd_backtest(args) -> int:
    try:
        profile = get_profile(args.profile)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    store = Store()
    fills = FillModel.from_config()
    out_root = Path("outputs/backtests")
    rc = 0
    for sym in [s.strip().upper() for s in args.symbols.split(",") if s.strip()]:
        try:
            bars = _slice(store.read(sym, args.tf).tuples(), args.start, args.end)
        except FileNotFoundError as e:
            print(f"{sym}: {e}", file=sys.stderr)
            rc = 1
            continue
        trades = backtest_wave3(bars, profile, fill_model=fills)
        m = summarize(trades, symbol=sym, timeframe=args.tf, profile=profile.name)
        out_dir = out_root / f"{sym.lower()}_{args.tf}_{profile.name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / "trades.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["signal_time", "entry_time", "direction", "entry", "stop",
                        "target_1", "planned_rr", "r", "outcome", "bars_held",
                        "strands"])
            for t in trades:
                w.writerow([t.signal_time, t.entry_time, t.direction, t.entry,
                            t.stop, t.target_1, t.planned_rr, t.r, t.outcome,
                            t.bars_held, t.strands])
        with open(out_dir / "equity_curve.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t", "cum_r"])
            w.writerows(equity_curve(trades))
        with open(out_dir / "metrics.json", "w") as f:
            json.dump(m, f, indent=1)
        exp = f"{m['expectancy_r']:+.2f}R" if m["expectancy_r"] is not None else "n/a"
        print(f"{sym} {args.tf} [{profile.name}]: {m['trades']} trades, "
              f"expectancy {exp}, win {m['win_rate']}, PF {m['profit_factor']}, "
              f"maxDD {m['max_drawdown_r']}R, DSR {m['dsr']} "
              f"(trial #{m['n_trials']}) -> {out_dir}/")
    return rc
