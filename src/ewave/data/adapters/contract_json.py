"""Adapter over the local contract-JSON store — the zero-network primary source."""
from __future__ import annotations

from typing import Optional

from . import DataProvider
from ..models import BarSeries
from ..store import Store


class ContractJson(DataProvider):
    name = "contract"

    def __init__(self, store: Optional[Store] = None, base_dir: Optional[str] = None):
        self.store = store or Store(base_dir)

    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        series = self.store.read(symbol, tf, extended=bool(kw.get("extended")))
        if start or end:
            from datetime import datetime, timezone

            def ts(s):
                return int(datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp())
            series = series.sliced(ts(start) if start else None,
                                   ts(end) + 86399 if end else None)
        return series
