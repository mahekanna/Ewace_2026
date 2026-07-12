"""Handlers for `ewave report` and `ewave journal`."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from .markdown import daily_report


def cmd_report(args) -> int:
    date = args.date
    if date == "today":
        date = datetime.now(timezone.utc).date().isoformat()
    text = daily_report(date)
    out = Path("outputs/reports")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"daily_{date}.md"
    path.write_text(text)
    print(text)
    print(f"wrote {path}")
    return 0


def cmd_journal(args) -> int:
    """Write the human trading journal (HTML + CSV) for each symbol."""
    from .. import config
    from ..data.store import Store
    from ..rules.profiles import get_profile
    from .journal import build_records, render_html, write_csv
    try:
        profile = get_profile(args.profile)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    store = Store()
    out_root = Path("outputs/journal")
    rc = 0
    portfolio = []
    for sym in [s.strip().upper() for s in args.symbols.split(",") if s.strip()]:
        try:
            bars = store.read(sym, args.tf).tuples()
        except FileNotFoundError as e:
            print(f"{sym}: {e}", file=sys.stderr)
            rc = 1
            continue
        recs, summ = build_records(sym, bars, profile)
        d = out_root / f"{sym.lower()}_{args.tf}_{profile.name}"
        render_html(recs, summ, args.tf, profile.name, d / "journal.html")
        write_csv(recs, d / "journal.csv")
        portfolio.append(summ)
        print(f"{sym} {args.tf} [{profile.name}]: {summ['trades']} trades, "
              f"{summ['total_r']:+.2f}R net, win {summ['win_rate']}, "
              f"PF {summ['profit_factor']}, maxDD {summ['max_dd_r']}R, "
              f"fired on {summ['fire_rate_pct']}% of bars -> {d}/journal.html")
    if len(portfolio) > 1:
        tot = sum(p["total_r"] for p in portfolio)
        tr = sum(p["trades"] for p in portfolio)
        print(f"\nPORTFOLIO: {tr} trades across {len(portfolio)} symbols, "
              f"{tot:+.2f}R net "
              f"({tot / tr:+.3f}R/trade)" if tr else "no trades")
    return rc
