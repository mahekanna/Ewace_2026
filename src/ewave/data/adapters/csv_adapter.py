"""CSV adapter — local files with a t,o,h,l,c[,v] header (t = unix seconds or ISO)."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from typing import Optional

from . import AdapterUnavailable, DataProvider
from ..models import BarSeries

_ALIASES = {
    "t": ("t", "time", "timestamp", "date", "datetime"),
    "o": ("o", "open"),
    "h": ("h", "high"),
    "l": ("l", "low"),
    "c": ("c", "close", "adj close", "adj_close"),
    "v": ("v", "volume", "vol"),
}


def _to_unix(val: str) -> int:
    s = val.strip()
    try:
        f = float(s)
        return int(f / 1000) if f > 1e11 else int(f)   # ms vs s heuristic
    except ValueError:
        pass
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return int(d.timestamp())


class CsvAdapter(DataProvider):
    name = "csv"

    def __init__(self, path: Optional[str] = None):
        self.path = path

    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        path = kw.get("path") or self.path
        if not path:
            raise AdapterUnavailable("csv adapter needs a file path (--path)")
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            cols = {}
            for canon, names in _ALIASES.items():
                for field in reader.fieldnames or []:
                    if field.strip().lower() in names:
                        cols[canon] = field
                        break
            missing = [k for k in ("t", "o", "h", "l", "c") if k not in cols]
            if missing:
                raise AdapterUnavailable(
                    f"{path}: cannot map columns for {missing} "
                    f"(header: {reader.fieldnames})")
            rows = []
            for row in reader:
                if not row.get(cols["t"]):
                    continue
                rows.append((_to_unix(row[cols["t"]]),
                             float(row[cols["o"]]), float(row[cols["h"]]),
                             float(row[cols["l"]]), float(row[cols["c"]]),
                             float(row[cols["v"]] or 0) if "v" in cols else 0.0))
        asof = datetime.now(timezone.utc).date().isoformat()
        return BarSeries.from_rows(symbol.upper(), tf, asof, rows, source="csv")
