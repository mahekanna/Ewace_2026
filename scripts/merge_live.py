"""merge_live.py — fold freshly-pulled bars into the data/live history files.

The 2026-06 snapshots in data/live/ carry the long history; a live pull only
needs to supply the bars minted since. This merges on `t` (fresh wins on
collision), keeps the series sorted and gap-free, and writes a new
`<sym>_<tf>_<asof-month>.json` in the same shape every wavelib script expects.

Usage:
  python3 scripts/merge_live.py            # AVGO 1w/1d/4h, base 2026-06 -> 2026-08
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "data", "live")
sys.path.insert(0, LIVE)

from _fresh_avgo_2026_08 import FRESH  # noqa: E402

ASOF = "2026-08-14"
BASE_TAG, NEW_TAG = "2026-06", "2026-08"


def rows_to_bars(rows):
    return [{"t": r[0], "o": r[1], "h": r[2], "l": r[3], "c": r[4], "v": r[5]}
            for r in rows]


def key_fn(tf):
    """Collision key. The 2026-06 daily snapshot anchors bars at 00:00-ish UTC
    while the live pull anchors at the 13:30 UTC open, so identical sessions
    carry different `t`. Dedup daily/weekly on the UTC calendar day (weeks are
    already Monday-anchored in both sources); intraday `t` matches exactly."""
    if tf in ("1d", "1w"):
        return lambda b: b["t"] // 86400
    return lambda b: b["t"]


def merge(sym, tf):
    base_path = os.path.join(LIVE, f"{sym}_{tf}_{BASE_TAG}.json")
    with open(base_path) as fh:
        doc = json.load(fh)

    key = key_fn(tf)
    by_k = {key(b): b for b in doc["bars"]}
    fresh = rows_to_bars(FRESH[tf])
    overlap = sum(1 for b in fresh if key(b) in by_k)
    mismatch = [b["t"] for b in fresh
                if key(b) in by_k and abs(by_k[key(b)]["c"] - b["c"]) > 0.01]
    by_k.update({key(b): b for b in fresh})

    doc["bars"] = sorted(by_k.values(), key=lambda b: b["t"])
    doc["asof"] = ASOF
    out = os.path.join(LIVE, f"{sym}_{tf}_{NEW_TAG}.json")
    with open(out, "w") as fh:
        json.dump(doc, fh)
    return out, len(doc["bars"]), len(fresh), overlap, mismatch


def standalone(sym, tf, rows):
    """Write a fresh-only series (see _fresh_avgo_intraday_2026_08 docstring)."""
    doc = {"symbol": "NASDAQ:" + sym.upper(), "interval": tf, "asof": ASOF,
           "bars": rows_to_bars(rows)}
    out = os.path.join(LIVE, f"{sym}_{tf}_{NEW_TAG}.json")
    with open(out, "w") as fh:
        json.dump(doc, fh)
    return out, len(doc["bars"])


if __name__ == "__main__":
    for tf in ("1w", "1d", "4h"):
        out, n, nf, ov, mm = merge("avgo", tf)
        print(f"{tf:>3}  bars={n:<6} fresh={nf:<4} overlap={ov:<3} "
              f"close-mismatch={len(mm)}  -> {os.path.basename(out)}")
        if mm:
            print(f"     mismatched t: {mm}")

    from _fresh_avgo_intraday_2026_08 import FRESH_INTRADAY  # noqa: E402
    for tf, rows in FRESH_INTRADAY.items():
        out, n = standalone("avgo", tf, rows)
        print(f"{tf:>3}  bars={n:<6} standalone (fresh-only) "
              f"        -> {os.path.basename(out)}")
