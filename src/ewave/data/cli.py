"""Handlers for `ewave fetch-data / validate-data / resample` (thin; logic in modules)."""
from __future__ import annotations

import sys

from .. import config
from .adapters import AdapterUnavailable, get_adapter
from .models import BarSeries
from .resample import TF_SECONDS, resample
from .store import Store
from .validate import validate_file, validate_series


def _symbols(args) -> list:
    if getattr(args, "symbols", None):
        return [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    if getattr(args, "watchlist", None):
        wl = config.load("watchlists")
        if args.watchlist not in wl:
            print(f"unknown watchlist '{args.watchlist}' (have: {', '.join(wl)})",
                  file=sys.stderr)
            raise SystemExit(2)
        return wl[args.watchlist]
    return []


def cmd_fetch_data(args) -> int:
    symbols = _symbols(args)
    if not symbols:
        print("fetch-data: give --symbols or --watchlist", file=sys.stderr)
        return 2
    store = Store()
    try:
        adapter = get_adapter(args.adapter)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 2
    rc = 0
    for sym in symbols:
        try:
            series = adapter.fetch(sym, args.tf, start=args.start, end=args.end,
                                   path=getattr(args, "path", None))
        except (AdapterUnavailable, FileNotFoundError) as e:
            print(f"{sym} {args.tf}: {e}", file=sys.stderr)
            rc = 1
            continue
        if args.adapter == "contract":
            print(f"{sym} {args.tf}: cached, {len(series)} bars "
                  f"(source={series.source or 'legacy'})")
            continue
        path = store.merge_write(series)
        print(f"{sym} {args.tf}: wrote {path} ({len(series)} bars fetched)")
    return rc


def cmd_validate_data(args) -> int:
    store = Store()
    if getattr(args, "all", False) or not (args.symbols or args.watchlist):
        files = store.list(tf=args.tf)
    else:
        files = []
        for sym in _symbols(args):
            files += store.list(symbol=sym, tf=args.tf)
    if not files:
        print("validate-data: no matching files in the store", file=sys.stderr)
        return 2
    n_bad = 0
    for p in files:
        rep = validate_file(p)
        if not rep.ok:
            n_bad += 1
            print(rep.summary())
        elif rep.warnings:
            print(rep.summary())
    print(f"validate-data: {len(files)} files, {n_bad} invalid")
    return 1 if n_bad else 0


def cmd_resample(args) -> int:
    store = Store()
    try:
        src = store.read(args.symbol, args.src_tf)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 2
    data_cfg = config.load("data")
    cls = data_cfg["symbol_classes"].get(
        args.symbol.lower(), data_cfg["symbol_classes"]["_default"])
    calendar = data_cfg["session_rules"][cls]["calendar"]
    rows = resample(src.tuples(), args.src_tf, args.dst_tf, calendar=calendar)
    series = BarSeries.from_rows(src.ticker, args.dst_tf, src.asof, rows,
                                 source=f"resample:{args.src_tf}",
                                 adjustment=src.adjustment, session=src.session)
    rep = validate_series(series, name=f"{args.symbol} {args.dst_tf} (resampled)")
    if not rep.ok:
        print(rep.summary(), file=sys.stderr)
        return 1
    if args.check:
        cached = store.latest(args.symbol, args.dst_tf)
        if cached is None:
            print(f"--check: no cached {args.dst_tf} series to compare against")
            return 0
        ref = store.read_path(cached)
        ref_by_t = {b.t: b for b in ref.bars}
        common = [b for b in series.bars if b.t in ref_by_t]
        close_match = sum(1 for b in common
                          if abs(b.c - ref_by_t[b.t].c) <= 0.005 * max(abs(b.c), 1e-9))
        print(f"--check vs {cached.name}: {len(common)} common buckets, "
              f"{close_match} closes within 0.5% "
              f"({series.bars[0].t}–{series.bars[-1].t})")
        if not common:
            print("  note: no timestamp overlap — the cached series likely uses a "
                  "different session/alignment (e.g. full-session :00-aligned vs "
                  "RTH 09:30-anchored); this is a source difference, not an error")
        return 0
    path = store.write(series)
    print(f"wrote {path}: {len(series)} bars ({args.src_tf} -> {args.dst_tf}, "
          f"calendar={calendar})")
    return 0


# used by cmd_resample above; TF_SECONDS re-exported for CLI help/tests
__all__ = ["cmd_fetch_data", "cmd_validate_data", "cmd_resample", "TF_SECONDS"]
