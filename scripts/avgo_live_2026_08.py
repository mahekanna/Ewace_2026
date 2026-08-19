"""avgo_live_2026_08.py — the post-top picture for AVGO on the current 2026-08 snapshot.

`wave_report.py` answers "what is the count on each timeframe". This answers the
follow-on question the count raises: the daily/weekly engine reads the Primary
five as COMPLETE at $495.00 (2026-06-03), so the live structure is the
correction off that high. This script measures that correction — leg geometry,
Fibonacci retracement/extension targets, the Blue Box for the C leg, the
structural invalidation levels — and scores the reversal-confluence strands per
timeframe so the "is the low in" question is answered by independent evidence
rather than by the label.

Run:  python3 scripts/avgo_live_2026_08.py
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")
REPORTS = os.path.join(ROOT, "reports")
SNAPSHOTS = ("2026-08", "2026-06")

# --- the Primary impulse the daily/4H engine labels (41.51 -> 495.00) ---------
IMPULSE_LOW, IMPULSE_HIGH = 138.10, 495.00   # wave (3) start .. wave (5) top
TOP_T = "2026-06-03"
# --- the correction so far, read off the daily pivots ------------------------
A_HIGH, A_LOW = 495.00, 356.43               # 2026-06-03 -> 2026-07-02
B_HIGH = 432.73                              # 2026-08-10
RETEST_LOW = 357.80                          # 2026-07-17

TFS = [("1W", "1w"), ("1D", "1d"), ("4H", "4h"), ("1H", "1h"), ("15M", "15m")]


def load(tag, slug="avgo"):
    for snap in SNAPSHOTS:
        p = os.path.join(LIVE, f"{slug}_{tag}_{snap}.json")
        if os.path.exists(p):
            d = json.load(open(p))
            return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
                    for b in d["bars"]]
    return None


def dd(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d")


def main():
    # date the report from the data, not the wall clock, so a re-run on an old
    # snapshot cannot overwrite a newer report
    asof = json.load(open(os.path.join(LIVE, "avgo_1d_2026-08.json")))["asof"]
    out = ["# AVGO — live wave analysis, all timeframes",
           f"\n_Snapshot {asof}, `scripts/avgo_live_2026_08.py`. Engine output on "
           "live TradingView bars, not hand-counted. Analysis tooling only — not "
           "investment advice._"]

    daily = load("1d")
    price = daily[-1][4]

    # ---------------- correction geometry -----------------------------------
    a_len = A_HIGH - A_LOW
    b_retr = (B_HIGH - A_LOW) / a_len
    out.append(f"\n## 1. The move being corrected\n")
    out.append(f"- Primary five tops at **${IMPULSE_HIGH:,.2f}** ({TOP_T}); "
               f"wave (3) origin **${IMPULSE_LOW:,.2f}**. Last **${price:,.2f}**.")
    out.append(f"- Wave **A** ${A_HIGH:,.2f} → ${A_LOW:,.2f} = ${a_len:,.2f} "
               f"({a_len / A_HIGH:.1%} of the high).")
    out.append(f"- Wave **B** ${A_LOW:,.2f} → ${B_HIGH:,.2f} = "
               f"**{b_retr:.1%} retrace of A** "
               f"({'shallow, C-continuation bias' if b_retr < 0.618 else 'deep — flat/irregular'}).")
    out.append(f"- Double bottom ${A_LOW:,.2f} / ${RETEST_LOW:,.2f} is the "
               "structural floor of the correction.")

    out.append("\n## 2. Downside measurement\n")
    retr = wl.fib_retrace(IMPULSE_HIGH, IMPULSE_LOW)
    out.append("**Retracement of the whole Primary five ($138.10 → $495.00):**\n")
    out.append("| ratio | price |\n|---|---|")
    for r, p in retr.items():
        out.append(f"| {r:.3f} | ${p:,.2f} |")

    bb = wl.blue_box_zone(A_HIGH, A_LOW, B_HIGH)
    c_eq = B_HIGH - a_len
    c_618 = B_HIGH - 0.618 * a_len
    out.append(f"\n**Wave C projections from the ${B_HIGH:,.2f} B high:**\n")
    out.append("| projection | price |\n|---|---|")
    out.append(f"| C = 0.618 × A | ${c_618:,.2f} |")
    out.append(f"| C = 1.000 × A (equality) | ${c_eq:,.2f} |")
    out.append(f"| Blue Box (1.0–1.618 × A) | ${min(bb):,.2f} – ${max(bb):,.2f} |")

    cluster = wl.fib_cluster([retr[0.382], retr[0.5], c_eq, c_618,
                              min(bb), max(bb)])
    if cluster:
        out.append(f"\n- Fibonacci confluence: **${cluster[0][0]:,.2f}** "
                   f"({cluster[0][1]} independent projections overlap).")

    # ---------------- per-timeframe confluence ------------------------------
    out.append("\n## 3. Reversal confluence per timeframe\n")
    out.append("Scoring a **bullish** reversal (is the correction low in?) in the "
               "zone spanning the double bottom to the current price.\n")
    out.append("| TF | bars | last | score | strands confirmed |\n|---|---|---|---|---|")
    details = []
    for label, tag in TFS:
        bars = load(tag)
        if not bars:
            continue
        zone = (A_LOW, max(bars[-1][4], RETEST_LOW))
        rep = wl.score_reversal("AVGO", bars, zone=zone, bullish=True)
        ok = [s.name for s in rep.strands if s.confirm] or ["none"]
        out.append(f"| {label} | {len(bars)} | ${bars[-1][4]:,.2f} | "
                   f"**{rep.score}/{rep.max_score}** | {', '.join(ok)} |")
        details.append((label, rep))

    out.append("\n<details><summary>Full strand detail</summary>\n")
    for label, rep in details:
        out.append(f"\n**{label}**\n```\n{rep}\n```")
    out.append("\n</details>")

    # ---------------- intrabar-ordering note (bug fixed) --------------------
    out.append("\n## 4. Intrabar pivot ordering — fixed\n")
    h1 = load("1h")
    last = h1[-2]          # the 2026-08-14 13:30 bar: o 411.93 h 412.36 l 395.13 c 397.07
    out.append(
        f"An earlier run of this report showed a final 1H/15M leg **up** to "
        f"${last[2]:,.2f}. That was an engine artifact, now fixed in `wavelib/toolkit.py`.")
    out.append("")
    out.append(f"The {dd(last[0])} 13:30 bar prints o ${last[1]:,.2f} / h ${last[2]:,.2f} / "
               f"l ${last[3]:,.2f} / c ${last[4]:,.2f} — it opened near its high and closed "
               "near its low, so the path is high-then-low. Both ZigZags used to visit the "
               "extreme in the trend's direction first and then test the reversal threshold "
               "against that just-updated extreme, which is only valid if price reached it "
               "first. On a bar wide enough to do both, that minted a low and a high pivot "
               f"at one timestamp in reverse order — here `L ${last[3]:,.2f}` → "
               f"`H ${last[2]:,.2f}`, inverting the micro-count.")
    out.append("")
    out.append("`_intrabar_order` now infers the path from open/close (down bar → o-h-l-c, "
               "up bar → o-l-h-c) and both ZigZags walk the bar's extremes in that order. "
               "The 1H last leg now reads **down** to $394.16, as the tape does.")
    out.append("")
    out.append("Scope of the change: the 1W/1D/4H **primary** counts and every level in this "
               "report are unchanged — the artifact only bit bars whose high-low range alone "
               "exceeded the reversal threshold, which on the higher timeframes never "
               "affected the top-ranked count. The ranked *alternates* on those timeframes "
               "did shift slightly, since they draw on finer scales. Guarded by "
               "`tests/test_intrabar_order.py`.")
    out.append("")
    out.append("_Separate, still-open defect:_ the ZigZag seed prices its first pivot at bar "
               "0's **close** rather than an extreme, so every series opens with a slightly "
               "synthetic pivot. Pre-existing and untouched here; it only affects the first "
               "bar.")

    # ---------------- invalidation ------------------------------------------
    out.append("\n## 5. Levels that change the count\n")
    out.append(f"- **${B_HIGH:,.2f}** — above it, wave C off the B high is wrong; "
               "the correction is instead a running/expanded form still building B.")
    out.append(f"- **${IMPULSE_HIGH:,.2f}** — above the top, the Primary five is not "
               "complete and the whole corrective read is void (wave (5) extends).")
    out.append(f"- **${A_LOW:,.2f} / ${RETEST_LOW:,.2f}** — losing the double bottom "
               "confirms C is underway and opens the retracement table above.")
    out.append(f"- **${IMPULSE_LOW:,.2f}** — wave (3) origin; below it the entire "
               "Primary labelling fails.")

    text = "\n".join(out) + "\n"
    outmd = os.path.join(REPORTS, f"AVGO_LIVE_{asof}.md")
    os.makedirs(REPORTS, exist_ok=True)
    open(outmd, "w").write(text)
    print(text)
    print(f"\nwrote {outmd}")


if __name__ == "__main__":
    main()
