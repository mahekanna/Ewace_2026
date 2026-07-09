"""
signals.store — append-only JSONL persistence + latest snapshots.
=================================================================
Freeze discipline (docs/NO_LOOKAHEAD_POLICY.md §3): a signal row is written the
moment it is generated, before any future bar is inspected; rows are appended,
never rewritten. `latest_signals.{json,csv}` are convenience snapshots of the
most recent scan for downstream consumers.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional

from .models import Signal


class SignalStore:
    def __init__(self, base_dir: str = "outputs/signals"):
        self.dir = Path(base_dir)

    def _day_file(self, day: Optional[str] = None) -> Path:
        day = day or datetime.now(timezone.utc).date().isoformat()
        return self.dir / f"{day}.jsonl"

    def append(self, signals: Iterable[Signal], day: Optional[str] = None) -> Path:
        """Freeze signals to the day ledger (append-only)."""
        self.dir.mkdir(parents=True, exist_ok=True)
        path = self._day_file(day)
        with open(path, "a") as f:
            for s in signals:
                f.write(json.dumps(s.to_dict()) + "\n")
        return path

    def load(self, day: Optional[str] = None) -> List[Signal]:
        path = self._day_file(day)
        if not path.exists():
            return []
        out = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(Signal.from_dict(json.loads(line)))
        return out

    def write_latest(self, signals: List[Signal]) -> None:
        """Snapshot of the most recent scan (overwritten each run)."""
        self.dir.mkdir(parents=True, exist_ok=True)
        rows = [s.to_dict() for s in signals]
        with open(self.dir / "latest_signals.json", "w") as f:
            json.dump(rows, f, indent=1)
        cols = ["signal_id", "symbol", "timeframe", "signal_time", "pattern_type",
                "direction", "status", "entry_price", "stop_price",
                "invalidation_level", "reward_risk", "confluence_strands",
                "source_profile"]
        with open(self.dir / "latest_signals.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols + ["target_1", "target_2"])
            for s in signals:
                row = [s.status.value if c == "status" else getattr(s, c)
                       for c in cols]
                w.writerow(row + [s.target_1, s.target_2])
