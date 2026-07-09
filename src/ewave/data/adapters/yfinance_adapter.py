"""
yfinance adapter — guarded import; install with `pip install ewave[yfinance]`.
Only usable on machines where Yahoo endpoints are reachable (they are
proxy-blocked in the cloud sandbox — use the MCP bridge there instead).
Prices use auto_adjust=False with split-only repair to match the split-adjusted
convention of the rest of the store.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from . import AdapterUnavailable, DataProvider
from ..models import BarSeries

_TF = {"1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
       "1h": "1h", "4h": None, "1d": "1d", "1w": "1wk"}


class YFinanceAdapter(DataProvider):
    name = "yfinance"

    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        try:
            import yfinance as yf
        except ImportError as e:
            raise AdapterUnavailable(
                "yfinance not installed — pip install ewave[yfinance]") from e
        if tf not in _TF:
            raise AdapterUnavailable(f"yfinance: unsupported timeframe '{tf}'")
        sym = symbol.split(":")[-1].upper()
        interval = _TF[tf] or "1h"          # 4h built from 1h below
        try:
            df = yf.Ticker(sym).history(
                start=start, end=end, interval=interval,
                period=None if start else kw.get("period", "2y"),
                auto_adjust=False, actions=False)
        except Exception as e:
            raise AdapterUnavailable(f"yfinance: fetch failed ({e})") from e
        rows = []
        for ts, row in df.iterrows():
            t = int(ts.timestamp()) if ts.tzinfo else int(
                ts.replace(tzinfo=timezone.utc).timestamp())
            rows.append((t, float(row["Open"]), float(row["High"]),
                         float(row["Low"]), float(row["Close"]),
                         float(row.get("Volume", 0) or 0)))
        if tf == "4h":
            from ..resample import resample
            rows = resample(sorted(rows), "1h", "4h")
        asof = datetime.now(timezone.utc).date().isoformat()
        return BarSeries.from_rows(sym, tf, asof, rows, source="yfinance",
                                   adjustment="split", session="regular")
