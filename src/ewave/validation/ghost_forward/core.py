"""
validation.ghost_forward.core — the causal ghost-feeding walk (stdlib only).
============================================================================
Canonical home of the Ghost Forward-Testing Kit core (the portable copy in
ghost_forward_kit/ now shims this module).

Project-agnostic. Defines the data contract, the FORECASTER contract, the causal
ghost-feeding walk, and the outcome classifier. Both `ghost_forward.py` (report)
and `ghost_diag.py` (breakdown) import from here. No third-party deps.

THE TWO CONTRACTS
-----------------
1. Bars JSON (one file per symbol+interval):
     {"symbol": "...", "interval": "15m", "asof": "YYYY-MM-DD",
      "bars": [{"t": <unix_sec_utc>, "o":.., "h":.., "l":.., "c":.., "v":..}, ...]}
   `t` strictly ascending. Anything that writes this shape works (see fetch_*.py).

2. Forecaster: a callable `forecast(bars) -> Forecast | None` where `bars` is a list
   of (t,o,h,l,c,v) tuples (oldest..newest) ending at "now". It must be CAUSAL — use
   only the bars it is given. Return None when you have no clean read. See
   forecasters/example_naive.py for a worked example.
"""
from __future__ import annotations
import importlib.util
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


def in_rth_ny(t):
    """True if unix-seconds `t` is in the US regular session (09:30-16:00 New York),
    DST-correct when zoneinfo is available, EDT fallback otherwise."""
    try:
        from zoneinfo import ZoneInfo
        d = datetime.fromtimestamp(t, ZoneInfo("America/New_York"))
    except Exception:
        d = datetime.fromtimestamp(t, timezone(timedelta(hours=-4)))
    return 930 <= d.hour * 100 + d.minute < 1600


@dataclass
class Forecast:
    direction: str            # "up" | "down" — which way the next move is expected
    target: float             # primary target price (where the move is expected to reach)
    invalidation: float       # level that voids the call (your structural stop)
    confidence: float = 0.5   # 0..1, optional — used only for the diagnostic breakdown
    kind: str = ""            # optional label (e.g. "wave-3", "breakout") for grouping
    note: str = ""            # free text, optional
    meta: dict = None         # optional provenance (e.g. setup_confirmed_t) — additive


# ----------------------------- data -----------------------------
def load_bars(path):
    """Load a bars JSON into a list of (t,o,h,l,c,v) tuples, ascending by t."""
    d = json.load(open(path))
    bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]
    bars.sort(key=lambda x: x[0])
    return bars, d.get("symbol", os.path.basename(path)), d.get("interval", "")


# ------------------------- forecaster I/O -------------------------
def load_forecaster(spec):
    """Load a forecaster from 'path/to/file.py:func' or 'dotted.module:func'."""
    if ":" not in spec:
        raise SystemExit("forecaster spec must be 'file.py:func' or 'module:func'")
    mod_part, func = spec.rsplit(":", 1)
    if mod_part.endswith(".py") or os.path.sep in mod_part:
        name = os.path.splitext(os.path.basename(mod_part))[0]
        s = importlib.util.spec_from_file_location(name, mod_part)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
    else:
        import importlib as _il
        m = _il.import_module(mod_part)
    return getattr(m, func)


def _norm(fc):
    """Accept a Forecast, a dict, or None; return a Forecast or None."""
    if fc is None:
        return None
    if isinstance(fc, Forecast):
        return fc
    if isinstance(fc, dict):
        return Forecast(direction=fc["direction"], target=float(fc["target"]),
                        invalidation=float(fc["invalidation"]),
                        confidence=float(fc.get("confidence", 0.5)),
                        kind=fc.get("kind", ""), note=fc.get("note", ""),
                        meta=fc.get("meta"))
    return Forecast(direction=fc.direction, target=float(fc.target),
                    invalidation=float(fc.invalidation),
                    confidence=float(getattr(fc, "confidence", 0.5)),
                    kind=getattr(fc, "kind", ""), note=getattr(fc, "note", ""),
                    meta=getattr(fc, "meta", None))


# ------------------------- the classifier -------------------------
def resolve(fc, future, price):
    """Ghost-feed `future` candles; return (outcome, n_bars_to_resolve).

    STALE  = target already on the wrong side of price (or invalidation on the wrong
             side) → the call is degenerate/unusable and is EXCLUDED from hit-rate.
    HIT    = target reached before invalidation, within the horizon.
    INVALIDATED = invalidation reached first.
    OPEN   = neither reached within the horizon.
    """
    if fc is None:
        return "no-forecast", 0
    up = fc.direction == "up"
    tgt, inv = fc.target, fc.invalidation
    if up and not (tgt > price and inv < price):
        return "stale", 0
    if (not up) and not (tgt < price and inv > price):
        return "stale", 0
    for i, b in enumerate(future):
        hi, lo = b[2], b[3]
        if up:
            if lo <= inv:
                return "INVALIDATED", i + 1
            if hi >= tgt:
                return "HIT", i + 1
        else:
            if hi >= inv:
                return "INVALIDATED", i + 1
            if lo <= tgt:
                return "HIT", i + 1
    return "OPEN", len(future)


# --------------------------- the walk ----------------------------
def iter_steps(bars, forecaster, roll=400, forward="all", resolve_horizon=32):
    """Yield one dict per causal step. At step t the forecaster sees ONLY
    bars[t-roll+1 .. t]; the next `resolve_horizon` bars classify the call."""
    n = len(bars)
    fwd = n if forward in ("all", None) else int(forward)
    start = max(roll, n - fwd)
    end = n - resolve_horizon
    for t in range(start, end):
        window = bars[max(0, t + 1 - roll):t + 1]
        fc = _norm(forecaster(window))
        future = bars[t + 1:t + 1 + resolve_horizon]
        outcome, nbar = resolve(fc, future, bars[t][4])
        next_up = (bars[t + 1][4] >= bars[t][4]) if t + 1 < n else None
        yield {"t": bars[t][0], "price": bars[t][4], "fc": fc,
               "outcome": outcome, "nbar": nbar, "next_up": next_up}


# --------------------- tiny indicator helpers --------------------
from ...features.indicators import atr, sma  # noqa: F401,E402 (one shared copy)
