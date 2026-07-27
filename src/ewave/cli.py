"""
cli.py — the `ewave` command. Thin argparse dispatch; business logic lives in
the modules (data/, pivots/, scanner/, validation/, backtest/, execution/, …).

Every subcommand handler is imported lazily so `ewave --help` works even while
later phases are still being built; an unbuilt command exits with a clear note.
"""
from __future__ import annotations

import argparse
import sys

from . import __version__

# subcommand -> (dotted module under ewave, callable, build phase note)
_DISPATCH = {
    "fetch-data":    ("ewave.data.cli", "cmd_fetch_data", "Phase 1"),
    "validate-data": ("ewave.data.cli", "cmd_validate_data", "Phase 1"),
    "resample":      ("ewave.data.cli", "cmd_resample", "Phase 1"),
    "pivots":        ("ewave.pivots.cli", "cmd_pivots", "Phase 2"),
    "scan":          ("ewave.scanner.cli", "cmd_scan", "Phase 4"),
    "ghost-forward": ("ewave.validation.ghost_forward.cli", "cmd_ghost_forward", "Phase 5"),
    "backtest":      ("ewave.backtest.cli", "cmd_backtest", "Phase 6"),
    "paper-trade":   ("ewave.execution.cli", "cmd_paper_trade", "Phase 7"),
    "report":        ("ewave.reporting.cli", "cmd_report", "Phase 8"),
    "journal":       ("ewave.reporting.cli", "cmd_journal", "Phase 8"),
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ewave",
        description="Elliott Wave / NeoWave automation: causal detection, signals, "
                    "ghost-forward validation, backtest, paper trading.")
    p.add_argument("--version", action="version", version=f"ewave {__version__}")
    sub = p.add_subparsers(dest="command", metavar="<command>")

    sp = sub.add_parser("fetch-data", help="fetch bars via a data adapter into the contract-JSON store")
    sp.add_argument("--adapter", default="contract",
                    choices=["contract", "csv", "alpaca", "fmp", "yfinance"])
    sp.add_argument("--symbols", help="comma-separated tickers (e.g. AVGO,MRVL)")
    sp.add_argument("--watchlist", help="watchlist name from configs/watchlists.json")
    sp.add_argument("--tf", default="1d", help="timeframe: 15m|1h|4h|1d|1w")
    sp.add_argument("--start", help="YYYY-MM-DD")
    sp.add_argument("--end", help="YYYY-MM-DD")
    sp.add_argument("--path", help="input path (csv adapter)")

    sp = sub.add_parser("validate-data", help="validate contract-JSON bars (schema, monotonic, OHLC sanity, gaps)")
    sp.add_argument("--symbols", help="comma-separated tickers")
    sp.add_argument("--watchlist", help="watchlist name")
    sp.add_argument("--tf", help="restrict to one timeframe")
    sp.add_argument("--all", action="store_true", help="validate every file in the store")

    sp = sub.add_parser("resample", help="build a coarser timeframe from a finer cached one")
    sp.add_argument("--symbol", required=True)
    sp.add_argument("--from", dest="src_tf", required=True)
    sp.add_argument("--to", dest="dst_tf", required=True)
    sp.add_argument("--check", action="store_true",
                    help="compare against an existing cached series instead of writing")

    sp = sub.add_parser("pivots", help="print the causal pivot table (pivot_t vs confirmed_t) for a symbol")
    sp.add_argument("symbol")
    sp.add_argument("tf", nargs="?", default="1d")
    sp.add_argument("--method", default="pct", choices=["pct", "atr", "fractal"])
    sp.add_argument("--pct", type=float, default=0.03)
    sp.add_argument("--atr-n", type=int, default=14)
    sp.add_argument("--csv", help="also write the table to this CSV path")

    sp = sub.add_parser("scan", help="scan a watchlist for wave signals under a rule profile")
    sp.add_argument("--watchlist", default="default")
    sp.add_argument("--symbols", help="comma-separated tickers (overrides --watchlist)")
    sp.add_argument("--tf", default="1h")
    sp.add_argument("--profile", default="experimental")

    sp = sub.add_parser("ghost-forward", help="candle-by-candle causal replay of a signal profile")
    sp.add_argument("--symbols", required=True)
    sp.add_argument("--tf", default="15m")
    sp.add_argument("--profile", default="experimental")
    sp.add_argument("--roll", type=int, default=400, help="bars of history per step")
    sp.add_argument("--horizon", type=int, default=32, help="bars to resolve each call")
    sp.add_argument("--forward", default="all", help="how many steps to walk (or 'all')")
    sp.add_argument("--csv", action="store_true",
                    help="also write snapshots/outcomes as CSV (spec §17)")

    sp = sub.add_parser("backtest", help="backtest executable signals (causal entries only)")
    sp.add_argument("--symbols", required=True)
    sp.add_argument("--tf", default="15m")
    sp.add_argument("--profile", default="experimental")
    sp.add_argument("--start", help="YYYY-MM-DD")
    sp.add_argument("--end", help="YYYY-MM-DD")

    sp = sub.add_parser("paper-trade", help="run the signal→risk→paper-execution loop")
    sp.add_argument("--watchlist", default="default")
    sp.add_argument("--tf", default="15m")
    sp.add_argument("--profile", default="experimental")
    sp.add_argument("--replay", action="store_true",
                    help="drive from cached bars (deterministic; works offline)")
    sp.add_argument("--days", type=int, default=30, help="replay window in days")

    sp = sub.add_parser("report", help="write the daily markdown report")
    sp.add_argument("--date", default="today")

    sp = sub.add_parser("journal", help="write the human trading journal (every trade, its basis, P&L)")
    sp.add_argument("--symbols", required=True, help="comma-separated tickers")
    sp.add_argument("--tf", default="1h")
    sp.add_argument("--profile", default="experimental")

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    mod_name, func_name, phase = _DISPATCH[args.command]
    try:
        import importlib
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
    except (ImportError, AttributeError):
        print(f"ewave {args.command}: not built yet — arrives in {phase} "
              "(see docs/FULL_AUTOMATION_ROADMAP.md)", file=sys.stderr)
        return 2
    return int(func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
