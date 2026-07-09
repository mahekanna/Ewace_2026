"""
mcp_export.py — normalize a saved MCP finance-tool payload into contract JSON.
==============================================================================
The sandbox's data path (docs/ARCHITECTURE.md): Claude calls an MCP tool (FMP
chart, yfinance history, tvremix get_ohlcv, Alpaca get_stock_bars), saves the
raw result to a file, then runs this script to write the canonical
`data/live/<slug>_<tf>_<stamp>.json`.

  python3 scripts/mcp_export.py --format fmp --symbol AVGO --tf 1h raw.json
  python3 scripts/mcp_export.py --format tv  --symbol NVDA --tf 15m dump.json --session rth
  python3 scripts/mcp_export.py --format yf  --symbol AVGO --tf 1d raw.json --dry-run

--session rth filters to the US regular session (09:30–16:00 NY) for intraday
data; 'full' keeps everything (also written as the `_eh` variant convention
when --eh is given). Multiple input files are merged (dedupe on t, ascending).
"""
import argparse
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))

from ewave.data.adapters.mcp_bridge import FORMATS, normalize          # noqa: E402
from ewave.data.models import BarSeries                                # noqa: E402
from ewave.data.store import Store                                     # noqa: E402
from ewave.data.validate import in_rth_ny, validate_series             # noqa: E402

_INTRADAY = ("1m", "5m", "15m", "30m", "1h", "4h")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("inputs", nargs="+", help="raw MCP payload JSON file(s)")
    ap.add_argument("--format", required=True, choices=sorted(FORMATS))
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--tf", required=True)
    ap.add_argument("--out", default=None, help="store dir (default data/live)")
    ap.add_argument("--stamp", default=None, help="filename stamp YYYY-MM (default: now)")
    ap.add_argument("--session", default="rth", choices=["rth", "full"],
                    help="intraday session filter (default rth, matching the store)")
    ap.add_argument("--eh", action="store_true",
                    help="write as the _eh (extended-hours) variant")
    ap.add_argument("--dry-run", action="store_true",
                    help="parse + validate + report, write nothing")
    a = ap.parse_args()

    rows = []
    for path in a.inputs:
        with open(path) as f:
            payload = json.load(f)
        series = normalize(payload, a.format, a.symbol, a.tf)
        rows += series.tuples()
        print(f"parsed {path}: {len(series)} bars")
    merged = BarSeries.from_rows(a.symbol.upper(), a.tf, series.asof, rows,
                                 source=series.source, adjustment="split",
                                 session="extended" if a.eh else
                                 ("full" if a.session == "full" else "regular"))
    if a.session == "rth" and not a.eh and a.tf in _INTRADAY:
        kept = [b for b in merged.bars if in_rth_ny(b.t)]
        print(f"session filter rth: {len(merged.bars)} -> {len(kept)} bars")
        merged.bars = kept

    rep = validate_series(merged, name=f"{a.symbol} {a.tf}")
    print(rep.summary())
    if not rep.ok:
        return 1
    if a.dry_run:
        print("(dry-run: nothing written)")
        return 0
    store = Store(a.out)
    path = store.merge_write(merged, stamp=a.stamp, extended=a.eh)
    final = store.read_path(path)
    print(f"wrote {path}: {len(final)} bars total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
