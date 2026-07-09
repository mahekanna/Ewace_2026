"""
data.validate — contract-JSON validation (schema, monotonicity, OHLC sanity, gaps).
===================================================================================
Errors make a file INVALID (the engine must not consume it); warnings are
informational (gaps, zero-volume streaks). Insufficient data is reported, never
silently passed — the same honesty rule as the wave validators.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Union

from .models import BarSeries
from .resample import TF_SECONDS

_T_MIN = -2208988800      # 1900-01-01 — long index histories are legitimate
_T_MAX = 4102444800       # 2100-01-01 — ms-vs-s unit bugs land far above this


def in_rth_ny(t: Union[int, float]) -> bool:
    """True if unix-seconds `t` falls in the US regular session (09:30–16:00
    New York), DST-correct when zoneinfo is available (EDT fallback otherwise).
    Same logic the ghost-forward kit has always used."""
    try:
        from zoneinfo import ZoneInfo
        d = datetime.fromtimestamp(t, ZoneInfo("America/New_York"))
    except Exception:
        d = datetime.fromtimestamp(t, timezone(timedelta(hours=-4)))
    return 930 <= d.hour * 100 + d.minute < 1600


@dataclass
class Report:
    name: str
    symbol: str = ""
    interval: str = ""
    n_bars: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        state = "OK" if self.ok else "INVALID"
        parts = [f"{self.name}: {state} n={self.n_bars}"]
        parts += [f"  ERROR {e}" for e in self.errors]
        parts += [f"  warn  {w}" for w in self.warnings]
        return "\n".join(parts)


def validate_series(series: BarSeries, name: str = "") -> Report:
    rep = Report(name=name or series.symbol, symbol=series.symbol,
                 interval=series.interval, n_bars=len(series.bars))
    # legacy quirks: tvremix files store "1D"/"1W"; extended-hours variants
    # store "15m_eh" (a session tag, not a timeframe)
    interval = series.interval.lower()
    if interval.endswith("_eh"):
        interval = interval[:-3]
    if not series.symbol:
        rep.errors.append("missing symbol")
    if interval not in TF_SECONDS:
        rep.errors.append(f"unknown interval '{series.interval}'")
    if not series.bars:
        rep.errors.append("no bars")
        return rep

    prev_t = None
    n_dup = n_desc = n_ohlc = n_negv = n_range = 0
    for b in series.bars:
        if not (_T_MIN <= b.t <= _T_MAX):
            n_range += 1
        if prev_t is not None:
            if b.t == prev_t:
                n_dup += 1
            elif b.t < prev_t:
                n_desc += 1
        prev_t = b.t
        lo, hi = min(b.o, b.c), max(b.o, b.c)
        if b.h < hi or b.l > lo or b.h < b.l:
            n_ohlc += 1
        if b.v < 0:
            n_negv += 1
    if n_range:
        rep.errors.append(f"{n_range} timestamps outside 1990–2100 (ms-vs-s unit bug?)")
    if n_dup:
        rep.errors.append(f"{n_dup} duplicate timestamps")
    if n_desc:
        rep.errors.append(f"{n_desc} descending timestamps (must be strictly ascending)")
    if n_ohlc:
        rep.errors.append(f"{n_ohlc} bars violate OHLC sanity (h>=max(o,c)>=min(o,c)>=l)")
    if n_negv:
        rep.errors.append(f"{n_negv} bars with negative volume")

    # gap report (informational): spacing > 4 calendar days for intraday/daily
    # is a data hole beyond any weekend+holiday; weekly series are exempt.
    if interval in TF_SECONDS and interval != "1w":
        gaps = sum(1 for i in range(len(series.bars) - 1)
                   if series.bars[i + 1].t - series.bars[i].t > 4 * 86400)
        if gaps:
            rep.warnings.append(f"{gaps} gaps > 4 days (holes beyond weekend+holiday)")
    return rep


def validate_file(path) -> Report:
    import json
    import os
    name = os.path.basename(str(path))
    try:
        with open(path) as f:
            d = json.load(f)
    except Exception as e:
        rep = Report(name=name)
        rep.errors.append(f"unreadable JSON: {e}")
        return rep
    missing = [k for k in ("symbol", "interval", "asof", "bars") if k not in d]
    if missing:
        rep = Report(name=name)
        rep.errors.append(f"missing keys: {', '.join(missing)}")
        return rep
    return validate_series(BarSeries.from_dict(d), name=name)
