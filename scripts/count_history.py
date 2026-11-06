"""
count_history.py
================
Replay the daily history bar by bar and record the Elliott/NeoWave count the
engine HELD at every bar — the continuation of the labelling, not just the
label at the end.  Writes an interactive page per symbol (scrubber / play-head
redraws the as-of legs; pattern band per bar; transitions table) and a markdown
report of the segments.

Run:  python3 scripts/count_history.py                       # AVGO MRVL, newest snapshot tag
      python3 scripts/count_history.py AVGO --tag 2026-11 --start 2021-01-01
      python3 scripts/count_history.py MRVL --window 300 --stride 1

Outputs: charts/<sym>_count_history_<tag>.html, reports/COUNT_HISTORY_<tag>.md
"""
import argparse
import datetime
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data.fetch import load_bars, latest_tag          # noqa: E402
from wavelib.count_history import (count_history, history_markdown,  # noqa: E402
                                   render_count_history_page)

CHARTS = os.path.join(ROOT, "charts")
REPORTS = os.path.join(ROOT, "reports")
DESC = {"AVGO": "Broadcom · NASDAQ:AVGO", "MRVL": "Marvell · NASDAQ:MRVL"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="bar-by-bar count continuation (causal replay)")
    ap.add_argument("symbols", nargs="*", default=["AVGO", "MRVL"])
    ap.add_argument("--tag", default=None, help="data/live snapshot tag (default: newest)")
    ap.add_argument("--tf", default="1d")
    ap.add_argument("--start", default=None, help="replay from this date (YYYY-MM-DD)")
    ap.add_argument("--window", type=int, default=300, help="trailing bars the engine sees")
    ap.add_argument("--stride", type=int, default=1, help="bars between replay steps")
    ap.add_argument("--min-history", type=int, default=60)
    ap.add_argument("--min-bars", type=int, default=1,
                    help="hide segments held fewer bars than this in the markdown")
    a = ap.parse_args(argv)

    md = ["# Count continuation — bar-by-bar causal replay", "",
          f"_Generated {datetime.date.today().isoformat()} by `scripts/count_history.py`. "
          "At each step the engine saw only the bars up to that point; every row is a "
          "labelling that was actually held, including those later abandoned. "
          "Analysis tooling only — not investment advice._", ""]
    tag_used = None
    for sym in [s.upper() for s in a.symbols]:
        tag = a.tag or latest_tag(sym, a.tf)
        if tag is None:
            print(f"{sym}: no {a.tf} snapshot — run data/fetch.py first")
            continue
        tag_used = tag
        bars = load_bars(sym, a.tf, tag=tag)
        if a.start:
            t0 = datetime.datetime.strptime(a.start, "%Y-%m-%d").replace(
                tzinfo=datetime.timezone.utc).timestamp()
            # keep `window` bars of run-up so the first steps have a full window
            k = next((i for i, b in enumerate(bars) if b[0] >= t0), 0)
            bars = bars[max(0, k - a.window):]
        t = time.time()
        h = count_history(bars, symbol=sym, window=a.window, stride=a.stride,
                          min_history=a.min_history, progress=print)
        print(f"{sym}: {len(h.snapshots)} steps, {len(h.anchored)} anchored / "
              f"{len(h.recent)} recent segments in {time.time() - t:.1f}s")
        page = os.path.join(CHARTS, f"{sym.lower()}_count_history_{tag}.html")
        render_count_history_page(h, output_path=page, desc=f"{DESC.get(sym, sym)} · {a.tf} · "
                                  f"snapshot {tag} · causal replay")
        print(f"wrote {os.path.relpath(page, ROOT)}")
        md.append(f"## {sym} — {DESC.get(sym, sym)}")
        md.extend([f"- {len(bars)} {a.tf} bars {datetime.datetime.fromtimestamp(bars[0][0], datetime.timezone.utc).date()} → "
                  f"{datetime.datetime.fromtimestamp(bars[-1][0], datetime.timezone.utc).date()}, snapshot `{tag}`; "
                   f"interactive page: `charts/{os.path.basename(page)}`", ""])
        md.append(history_markdown(h, "anchored", min_bars=a.min_bars))
        md.append(history_markdown(h, "recent", min_bars=a.min_bars))
        md.append("---\n")
    if tag_used:
        os.makedirs(REPORTS, exist_ok=True)
        rp = os.path.join(REPORTS, f"COUNT_HISTORY_{tag_used}.md")
        with open(rp, "w", encoding="utf-8") as fh:
            fh.write("\n".join(md) + "\n")
        print(f"wrote {os.path.relpath(rp, ROOT)}")


if __name__ == "__main__":
    main()
