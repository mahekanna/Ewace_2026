"""
data.models — canonical bar containers (stdlib only).
=====================================================
The on-disk truth is the contract JSON (docs/ARCHITECTURE.md):

    {"symbol", "interval", "asof", "bars": [{"t","o","h","l","c","v"}, ...]}

`t` = unix seconds UTC, strictly ascending, prices split-adjusted. The engine's
internal working form is the plain tuple `(t, o, h, l, c, v)` — `BarSeries.tuples()`
bridges the two so every existing wavelib/ewave function consumes cached data
unchanged. Optional metadata (source, adjustment, session) is serialized only
when set, keeping round-trips of existing files stable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Bar:
    t: int          # unix seconds UTC (bar open time)
    o: float
    h: float
    l: float
    c: float
    v: float = 0.0

    def tuple(self) -> Tuple[int, float, float, float, float, float]:
        return (self.t, self.o, self.h, self.l, self.c, self.v)


@dataclass
class BarSeries:
    symbol: str                 # e.g. "ALPACA:AVGO" or "AVGO"
    interval: str               # 15m | 1h | 4h | 1d | 1w (see resample.TF_SECONDS)
    asof: str                   # YYYY-MM-DD the series was fetched
    bars: List[Bar] = field(default_factory=list)
    source: str = ""            # alpaca_rest | fmp_rest | yfinance | mcp:<tool> | csv | contract
    adjustment: str = ""        # split | dividend | all | raw ("" = unknown/legacy)
    session: str = ""           # regular | extended | full ("" = unknown/legacy)

    @property
    def ticker(self) -> str:
        """Bare uppercase ticker without any EXCHANGE: prefix."""
        return self.symbol.split(":")[-1].upper()

    def tuples(self) -> List[Tuple[int, float, float, float, float, float]]:
        """Legacy engine form: [(t, o, h, l, c, v), ...] ascending."""
        return [b.tuple() for b in self.bars]

    # ---------------- contract JSON round-trip ----------------
    @classmethod
    def from_dict(cls, d: dict) -> "BarSeries":
        def num(x):
            # preserve int-vs-float exactly as stored → round-trips of legacy
            # files stay byte-identical (json re-emits the same literal)
            return x if isinstance(x, (int, float)) else float(x)
        bars = [Bar(int(b["t"]), num(b["o"]), num(b["h"]), num(b["l"]),
                    num(b["c"]), num(b.get("v", 0) or 0)) for b in d.get("bars", [])]
        return cls(symbol=d.get("symbol", ""), interval=d.get("interval", ""),
                   asof=d.get("asof", ""), bars=bars,
                   source=d.get("source", ""), adjustment=d.get("adjustment", ""),
                   session=d.get("session", ""))

    def to_dict(self) -> dict:
        d = {"symbol": self.symbol, "interval": self.interval, "asof": self.asof,
             "bars": [{"t": b.t, "o": b.o, "h": b.h, "l": b.l, "c": b.c, "v": b.v}
                      for b in self.bars]}
        # optional metadata only when set — legacy files stay byte-identical
        for k in ("source", "adjustment", "session"):
            val = getattr(self, k)
            if val:
                d[k] = val
        return d

    @classmethod
    def from_rows(cls, symbol: str, interval: str, asof: str,
                  rows: Iterable[Tuple], **meta) -> "BarSeries":
        """Build from (t,o,h,l,c[,v]) tuples; sorts ascending, dedupes on t
        (last write wins — matches the historical merge behaviour)."""
        by_t = {}
        for r in rows:
            v = float(r[5]) if len(r) > 5 and r[5] is not None else 0.0
            by_t[int(r[0])] = Bar(int(r[0]), float(r[1]), float(r[2]),
                                  float(r[3]), float(r[4]), v)
        bars = [by_t[t] for t in sorted(by_t)]
        return cls(symbol=symbol, interval=interval, asof=asof, bars=bars, **meta)

    def sliced(self, start_t: Optional[int] = None, end_t: Optional[int] = None) -> "BarSeries":
        bars = [b for b in self.bars
                if (start_t is None or b.t >= start_t) and (end_t is None or b.t <= end_t)]
        return BarSeries(self.symbol, self.interval, self.asof, bars,
                         self.source, self.adjustment, self.session)

    def __len__(self) -> int:
        return len(self.bars)
