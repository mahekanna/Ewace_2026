"""update_live.py — apply an incremental bar pull to the live snapshot files.

merge_live.py builds a month's snapshot from the prior month plus a bulk pull.
This applies a small same-month update on top of it: new sessions, and
corrections to bars that were still forming when first pulled.

Dedups daily/weekly on the UTC calendar day and intraday on `t`, fresh winning
on collision, so a partial bar is completed in place rather than duplicated.

Run:  python3 scripts/update_live.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "data", "live")
sys.path.insert(0, LIVE)

from _fresh_avgo_2026_08_19 import UPDATE, ASOF  # noqa: E402

SNAP = "2026-08"


def key_fn(tf):
    return (lambda b: b["t"] // 86400) if tf in ("1d", "1w") else (lambda b: b["t"])


def apply(sym, tf, rows):
    path = os.path.join(LIVE, f"{sym}_{tf}_{SNAP}.json")
    doc = json.load(open(path))
    key = key_fn(tf)
    by = {key(b): b for b in doc["bars"]}
    before = len(by)
    fresh = [{"t": r[0], "o": r[1], "h": r[2], "l": r[3], "c": r[4], "v": r[5]}
             for r in rows]
    revised = sum(1 for b in fresh if key(b) in by)
    by.update({key(b): b for b in fresh})
    doc["bars"] = sorted(by.values(), key=lambda b: b["t"])
    doc["asof"] = ASOF
    json.dump(doc, open(path, "w"))
    return len(doc["bars"]), len(doc["bars"]) - before, revised, doc["bars"][-1]["c"]


if __name__ == "__main__":
    for tf, rows in UPDATE.items():
        n, added, revised, last = apply("avgo", tf, rows)
        print(f"{tf:>3} bars={n:<6} added={added} revised={revised} last_close={last}")
