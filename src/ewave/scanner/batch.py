"""
scanner.batch — watchlist scan: cached bars → profile signals → frozen store.
=============================================================================
Detection only: signals are generated and FROZEN (persisted) here; sizing is
the risk engine's job, execution the broker's, outcomes the validators'.
"""
from __future__ import annotations

from typing import List, Optional

from .. import config
from ..data.store import Store
from ..patterns.tree import tree_context
from ..rules.profiles import Profile, get_profile
from ..signals import wave3
from ..signals.models import Signal
from ..signals.store import SignalStore


def scan_symbol(symbol: str, tf: str, profile: Profile,
                store: Optional[Store] = None,
                with_tree_context: bool = True) -> List[Signal]:
    """Signals visible on the LAST cached bar of symbol/tf under `profile`."""
    store = store or Store()
    series = store.read(symbol, tf)
    bars = series.tuples()
    signals = wave3.generate(bars, profile, symbol=symbol, timeframe=tf)
    if signals and with_tree_context:
        ctx = tree_context(bars)
        for s in signals:
            s.tree_confidence = ctx["tree_confidence"]
            if ctx["primary"]:
                s.note = (s.note + f" | tree: {ctx['primary']}").strip(" |")
    return signals


def scan(symbols: List[str], tf: str, profile_name: str,
         store: Optional[Store] = None,
         signal_store: Optional[SignalStore] = None) -> dict:
    """Scan a symbol list; freeze any signals; return a summary dict."""
    profile = get_profile(profile_name)
    store = store or Store()
    signal_store = signal_store or SignalStore()
    found: List[Signal] = []
    errors = []
    for sym in symbols:
        try:
            found += scan_symbol(sym, tf, profile, store)
        except FileNotFoundError as e:
            errors.append(f"{sym}: {e}")
    if found:
        signal_store.append(found)          # freeze before anything else sees them
    signal_store.write_latest(found)
    return {"profile": profile_name, "timeframe": tf,
            "symbols_scanned": len(symbols), "signals": found, "errors": errors}


def resolve_watchlist(args) -> List[str]:
    if getattr(args, "symbols", None):
        return [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    wl = config.load("watchlists")
    name = getattr(args, "watchlist", "default") or "default"
    if name not in wl:
        raise config.ConfigError(
            f"unknown watchlist '{name}' (have: {', '.join(wl)})")
    return wl[name]
