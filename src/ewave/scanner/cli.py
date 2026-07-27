"""Handler for `ewave scan`."""
from __future__ import annotations

import sys
from datetime import datetime, timezone

from .. import config
from .batch import resolve_watchlist, scan


def cmd_scan(args) -> int:
    try:
        symbols = resolve_watchlist(args)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    try:
        result = scan(symbols, args.tf, args.profile)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    sigs = result["signals"]
    print(f"scan: {result['symbols_scanned']} symbols @ {args.tf} "
          f"profile={args.profile} -> {len(sigs)} signal(s)")
    for s in sigs:
        t = datetime.fromtimestamp(s.signal_time, timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"  {s.symbol} {s.direction.upper()} {s.pattern_type} @ {t} "
              f"entry {s.entry_price} stop {s.stop_price} T1 {s.target_1} "
              f"R:R {s.reward_risk} strands {s.confluence_strands} [{s.signal_id}]")
    for e in result["errors"]:
        print(f"  ! {e}", file=sys.stderr)
    from ..reporting.markdown import scan_report
    path = scan_report(result)
    print(f"scan report -> {path}")
    if sigs:
        from pathlib import Path

        from ..reporting.tradingview import notes_markdown
        tv = Path("outputs/reports/tradingview_notes.md")
        tv.write_text(notes_markdown(sigs))
        print(f"frozen to outputs/signals/ (JSONL) + latest_signals.{{json,csv}}; "
              f"TV notes -> {tv}")
    return 0
