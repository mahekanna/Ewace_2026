"""
data.adapters — pluggable bar sources behind one interface.
===========================================================
Every adapter implements `fetch(symbol, tf, start=None, end=None) -> BarSeries`.
Network adapters (alpaca/fmp/yfinance) raise `AdapterUnavailable` with a clear
reason when their prerequisites (keys, package, egress) are missing — in this
cloud sandbox market-data hosts are proxy-blocked, so bars arrive via the MCP
bridge (`mcp_bridge`, `scripts/mcp_export.py`) instead; the network adapters
are for machines where access exists.
"""
from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from typing import Optional

from ..models import BarSeries


class AdapterUnavailable(Exception):
    """The adapter cannot run in this environment (missing keys/package/egress)."""


class DataProvider(ABC):
    name: str = ""

    @abstractmethod
    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        """Return bars for `symbol` at timeframe `tf` (ascending, split-adjusted
        where the source supports it). `start`/`end` are YYYY-MM-DD or None."""


_REGISTRY = {
    "contract": ("ewave.data.adapters.contract_json", "ContractJson"),
    "csv": ("ewave.data.adapters.csv_adapter", "CsvAdapter"),
    "alpaca": ("ewave.data.adapters.alpaca_rest", "AlpacaRest"),
    "fmp": ("ewave.data.adapters.fmp_rest", "FmpRest"),
    "yfinance": ("ewave.data.adapters.yfinance_adapter", "YFinanceAdapter"),
}


def get_adapter(name: str, **kw) -> DataProvider:
    if name not in _REGISTRY:
        raise KeyError(f"unknown adapter '{name}' (have: {', '.join(_REGISTRY)})")
    mod_name, cls_name = _REGISTRY[name]
    mod = importlib.import_module(mod_name)
    return getattr(mod, cls_name)(**kw)
