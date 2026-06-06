"""
04 — Auto-labeling + programmatic charting (Phase 4).

Runs the multi-scale auto-labeling engine on AVGO H1 data (no hand-picked legs),
prints the top-ranked candidate counts, and writes a programmatic SVG chart of
the zigzag wave skeleton.

    cd examples && python3 04_auto_label.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wavelib as wl
from data.avgo import H1


def main():
    cands = wl.label_and_validate(H1, degrees=(0.03, 0.05, 0.08), max_candidates=5)
    print(f"label_and_validate -> {len(cands)} candidate count(s) (ranked):")
    for i, c in enumerate(cands, 1):
        print(f"  {i}. {c.count_type:10} degree={c.degree} "
              f"hard_fails={c.hard_fails} warns={c.warns} "
              f"fib_score={c.fib_score:.2f} ({c.degree_confidence})")

    pivots = wl.zigzag(H1, pct=0.05)
    waves = wl.pivots_to_waves(pivots)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "charts",
                       "avgo_auto_zigzag.svg")
    wl.render_chart(waves, title="AVGO H1 — auto zigzag skeleton",
                    zones=[(358, 410)], output_path=out)
    print(f"\nwrote SVG: {os.path.normpath(out)} ({len(waves)} legs)")

    print("\nNOTE: candidates use only causally-confirmed pivots "
          "(provisional last pivot excluded). Degree is HEURISTIC (multi-scale), "
          "not a resolved Neely degree — see docs/research/04 §5.")


if __name__ == "__main__":
    main()
