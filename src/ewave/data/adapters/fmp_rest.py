"""
Financial Modeling Prep REST adapter. Pure stdlib (urllib). Needs FMP_API_KEY
and egress to financialmodelingprep.com.

FMP quirks handled here: intraday `historical-chart` timestamps are
America/New_York wall-clock (converted to unix UTC); results arrive newest-first
(re-sorted); daily comes from `historical-price-full` (split/dividend adjusted
close series).
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Optional

from . import AdapterUnavailable, DataProvider
from ..models import BarSeries

_INTRADAY = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min",
             "1h": "1hour", "4h": "4hour"}
_BASE = "https://financialmodelingprep.com/api/v3"


def _ny_to_unix(s: str) -> int:
    d = datetime.fromisoformat(s)
    try:
        from zoneinfo import ZoneInfo
        d = d.replace(tzinfo=ZoneInfo("America/New_York"))
    except Exception:
        from datetime import timedelta
        d = d.replace(tzinfo=timezone(timedelta(hours=-4)))
    return int(d.timestamp())


class FmpRest(DataProvider):
    name = "fmp"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FMP_API_KEY")

    def _get(self, path: str, **params) -> object:
        params["apikey"] = self.api_key
        url = f"{_BASE}/{path}?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            raise AdapterUnavailable(f"fmp: request failed ({e})") from e

    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        if not self.api_key:
            raise AdapterUnavailable("fmp: set FMP_API_KEY (see .env.example)")
        sym = symbol.split(":")[-1].upper()
        rows = []
        if tf in _INTRADAY:
            params = {}
            if start:
                params["from"] = start
            if end:
                params["to"] = end
            data = self._get(f"historical-chart/{_INTRADAY[tf]}/{urllib.parse.quote(sym)}",
                             **params)
            for x in data or []:
                rows.append((_ny_to_unix(x["date"]), x["open"], x["high"],
                             x["low"], x["close"], x.get("volume", 0)))
        elif tf in ("1d", "1w"):
            params = {}
            if start:
                params["from"] = start
            if end:
                params["to"] = end
            data = self._get(f"historical-price-full/{urllib.parse.quote(sym)}", **params)
            hist = (data or {}).get("historical", [])
            for x in hist:
                t = int(datetime.fromisoformat(x["date"]).replace(
                    tzinfo=timezone.utc).timestamp())
                rows.append((t, x["open"], x["high"], x["low"], x["close"],
                             x.get("volume", 0)))
            if tf == "1w":
                from ..resample import resample
                rows = resample(sorted(rows), "1d", "1w", calendar="America/New_York")
        else:
            raise AdapterUnavailable(f"fmp: unsupported timeframe '{tf}'")
        asof = datetime.now(timezone.utc).date().isoformat()
        return BarSeries.from_rows(sym, tf, asof, rows, source="fmp_rest",
                                   adjustment="split", session="regular")
