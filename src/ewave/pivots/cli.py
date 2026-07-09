"""Handler for `ewave pivots` — the causal pivot table (pivot_t vs confirmed_t)."""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone

from ..data.store import Store
from . import atr_reversal, fractal, percentage_reversal
from .models import provisional_last


def _fmt(t):
    if t is None:
        return "provisional"
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M")


def cmd_pivots(args) -> int:
    store = Store()
    try:
        series = store.read(args.symbol, args.tf)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 2
    bars = series.tuples()
    if args.method == "pct":
        piv = percentage_reversal.zigzag_causal(bars, pct=args.pct)
        desc = f"pct={args.pct}"
    elif args.method == "atr":
        piv = atr_reversal.detect(bars, atr_n=args.atr_n)
        desc = f"atr_n={args.atr_n}"
    else:
        piv = fractal.detect(bars)
        desc = "fractal 2/2"
    rows = [(p.kind, p.price, _fmt(p.t), _fmt(p.confirmed_t),
             round((p.confirmed_t - p.t) / 3600, 1) if p.confirmed_t else "")
            for p in piv]
    print(f"{args.symbol} {args.tf} — {len(piv)} pivots ({args.method}, {desc}); "
          f"last {'PROVISIONAL' if provisional_last(piv) else 'confirmed'}")
    print(f"{'kind':<5}{'price':>10}  {'pivot_t (extreme)':<18}"
          f"{'confirmed_t (knowable)':<24}{'lag_h':>6}")
    for k, price, pt, ct, lag in rows[-40:]:
        print(f"{k:<5}{price:>10.2f}  {pt:<18}{ct:<24}{lag!s:>6}")
    if len(rows) > 40:
        print(f"... ({len(rows) - 40} earlier pivots not shown; use --csv for all)")
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["kind", "price", "pivot_time_utc", "confirmed_time_utc", "lag_hours"])
            w.writerows(rows)
        print(f"wrote {args.csv}")
    return 0
