"""Handler for `ewave report`."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .markdown import daily_report


def cmd_report(args) -> int:
    date = args.date
    if date == "today":
        date = datetime.now(timezone.utc).date().isoformat()
    text = daily_report(date)
    out = Path("outputs/reports")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"daily_{date}.md"
    path.write_text(text)
    print(text)
    print(f"wrote {path}")
    return 0
