"""
brief.py — print the plain-language read for a symbol (and write it to reports/).
================================================================================
    python3 scripts/brief.py                       # AVGO MRVL, newest daily snapshot
    python3 scripts/brief.py NVDA --tag 2026-11
    python3 scripts/brief.py AVGO --fast           # skip the replay-based reliability figure

The reliability line comes from the causal bar-by-bar replay (count_history);
with --fast it is omitted and the brief says so.  Writes reports/BRIEF_<tag>.md.
"""
import argparse
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data.fetch import load_bars, latest_tag                      # noqa: E402
from wavelib.brief import decision_brief, brief_markdown, glossary_markdown   # noqa: E402
from wavelib.count_history import count_history, forecast_scorecard  # noqa: E402

REPORTS = os.path.join(ROOT, "reports")


def main(argv=None):
    ap = argparse.ArgumentParser(description="plain-language read of the current wave structure")
    ap.add_argument("symbols", nargs="*", default=["AVGO", "MRVL"])
    ap.add_argument("--tag", default=None)
    ap.add_argument("--tf", default="1d")
    ap.add_argument("--window", type=int, default=300)
    ap.add_argument("--fast", action="store_true", help="skip the replay (no reliability figure)")
    ap.add_argument("--replay-bars", type=int, default=1500,
                    help="bars of history to replay for the reliability figure")
    a = ap.parse_args(argv)
    md = ["# Plain-language reads", "",
          f"_Generated {datetime.date.today().isoformat()} by `scripts/brief.py`. A reading of "
          "structure, not advice: it says what the engine expects, what confirms it, what proves "
          "it wrong, and how often such calls worked before._", ""]
    tag_used = None
    for sym in [s.upper() for s in a.symbols]:
        tag = a.tag or latest_tag(sym, a.tf)
        if tag is None:
            print(f"{sym}: no {a.tf} snapshot — run data/fetch.py first")
            continue
        tag_used = tag
        bars = load_bars(sym, a.tf, tag=tag)
        scorecard, adoption_t = None, None
        if not a.fast:
            h = count_history(bars[-a.replay_bars:], symbol=sym, window=a.window)
            scorecard = forecast_scorecard(h.anchored)
            adoption_t = h.anchored[-1].start_t if h.anchored else None
        b = decision_brief(sym, bars, window=a.window, scorecard=scorecard, adoption_t=adoption_t)
        text = brief_markdown(b)
        print(text)
        md.append(text)
    md.append(glossary_markdown())
    if tag_used:
        os.makedirs(REPORTS, exist_ok=True)
        p = os.path.join(REPORTS, f"BRIEF_{tag_used}.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(md) + "\n")
        print(f"wrote {os.path.relpath(p, ROOT)}")


if __name__ == "__main__":
    main()
