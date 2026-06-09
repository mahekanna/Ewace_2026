"""
wave_report.py  —  perform & print the Elliott + NeoWave wave counts for symbols.
=================================================================================
For each (symbol, timeframe) it prints:
  ELLIOTT  : the engine's primary count (pattern @ degree, confidence, coverage),
             every labelled leg with its price/date span and sub-waves, the impulse
             HARD-RULE validation where applicable, and ranked alternates.
  NEOWAVE  : the full-range monowave swing count (:5/:3/:c3…), motive/corrective
             tally, Similarity & Balance on the key corrective pair, terminal &
             running/neutral-triangle checks, and the 2-4 line status.
  FORECAST : the projected next wave + targets + invalidation.

Run:  python3 scripts/wave_report.py [SYM ...]   (default AVGO MRVL)
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")
OUTMD = os.path.join(ROOT, "reports", "WAVE_COUNTS_AVGO_MRVL.md")
TFS = [("1W", "1w", (0.05, 0.10, 0.18, 0.30)),
       ("1D", "1d", (0.04, 0.08, 0.14, 0.22)),
       ("4H", "4h", (0.03, 0.06, 0.10, 0.16)),
       ("1H", "1h", (0.02, 0.04, 0.07, 0.12)),
       ("15M", "15m", (0.015, 0.03, 0.05, 0.09))]


def load(tag, slug):
    p = os.path.join(LIVE, f"{slug}_{tag}_2026-06.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]


def dd(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d")


def subseq(pattern, n):
    s = ("12345" if pattern in ("IMPULSE", "DIAGONAL") else
         "ABCDE" if pattern == "TRIANGLE" else "WXY" if pattern == "WXY" else "ABC")
    return [s[i] if i < len(s) else "·" for i in range(n)]


def adaptive_zigzag(bars, target=24):
    best = []
    for pct in (0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30):
        piv = [p for p in wl.zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
        if not best or abs(len(piv) - target) < abs(len(best) - target):
            best = piv
        if len(piv) <= target:
            break
    return best


def section(out, sym, tf_label, tag, scales):
    bars = load(tag, sym.lower())
    if not bars or len(bars) < 60:
        out.append(f"\n### {sym} · {tf_label}\n_(no data)_")
        return
    out.append(f"\n### {sym} · {tf_label} — {len(bars)} bars, {dd(bars[0][0])}→{dd(bars[-1][0])}, "
               f"last ${bars[-1][4]:,.2f}")

    # ---------- ELLIOTT ----------
    counts = wl.wave_counts(bars, scales=scales, max_alternates=3)
    out.append("\n**ELLIOTT WAVE**")
    if not counts:
        out.append("- no count")
    else:
        pc = counts[0]
        out.append(f"- Primary: **{pc.pattern} @ {pc.degree_label}** · confidence "
                   f"{pc.confidence:.0%} · coverage {pc.coverage:.0%}")
        for lab, node in pc.labels:
            kids = ""
            if len(node.children) >= 2:
                seq = subseq(node.pattern, len(node.children))
                kids = "  [sub: " + " ".join(
                    f"{seq[i]}={ch.end.price:,.2f}" for i, ch in enumerate(node.children)) + "]"
            out.append(f"    - **{lab}**: ${node.start.price:,.2f} ({dd(node.start.t)}) → "
                       f"${node.end.price:,.2f} ({dd(node.end.t)})  · {node.pattern}{kids}")
        # hard-rule validation if the primary (or a labelled leg) is a 5-wave impulse
        imp = None
        if pc.pattern in ("IMPULSE", "DIAGONAL") and len(pc.labels) == 5:
            imp = [n.as_wave() for _l, n in pc.labels]
        else:
            for _l, node in pc.labels:
                if node.pattern in ("IMPULSE", "DIAGONAL") and len(node.children) == 5:
                    imp = [c.as_wave() for c in node.children]
                    break
        if imp:
            res = wl.elliott_hard_rules(imp)
            out.append("    - _impulse hard-rule check:_ " + "; ".join(
                f"{r.rule.split('(')[0].strip()}={r.status.value}" for r in res))
        if counts[1:]:
            out.append("- Alternates: " + "; ".join(
                f"{a.pattern} {a.confidence:.0%}" for a in counts[1:]))

    # ---------- NEOWAVE ----------
    out.append("\n**NEOWAVE (Neely)**")
    piv = adaptive_zigzag(bars)
    if len(piv) < 4:
        out.append("- insufficient swings")
    else:
        lab = wl.label_monowaves(piv)
        swings = []
        for w, l in lab:
            d = "↑" if w.end.price >= w.start.price else "↓"
            swings.append(f"{l.split('(')[0]}{d}{w.end.price:,.2f}")
        mm = sum(1 for _w, l in lab if l.startswith(":5") or l.startswith(":L5"))
        cc = sum(1 for _w, l in lab if l.startswith(":3") or l.startswith(":c3")
                 or l.startswith(":sL3"))
        out.append(f"- Full-range swing count ({len(lab)} monowaves; {mm} motive / {cc} corrective):")
        out.append("    " + "  ".join(swings))
        # Similarity & Balance on the most recent corrective pair (last 3 legs A-B-C)
        if len(piv) >= 4:
            ws = wl.pivots_to_waves(piv[-4:])
            if len(ws) == 3:
                sb = wl.similarity_and_balance(ws[0], ws[2], context="recent A vs C")
                out.append(f"- Similarity & Balance (recent A vs C): {sb.status.value} — {sb.detail}")
        # terminal / special-structure checks on the last 5 legs
        if len(piv) >= 6:
            five = wl.pivots_to_waves(piv[-6:])
            if len(five) == 5:
                out.append(f"- Terminal check (last 5 legs): {wl.terminal_rules(five)[0].detail}")
                flags = []
                if wl.is_neutral_triangle(five).status.value == "PASS":
                    flags.append("neutral triangle")
                if wl.is_running_triangle(five).status.value == "PASS":
                    flags.append("running triangle")
                out.append(f"- Special structures (last 5 legs): {', '.join(flags) if flags else 'none'}")

    # ---------- FORECAST ----------
    fc = wl.forecast_waves(bars)
    if fc and fc.targets:
        out.append(f"\n**FORECAST**: {fc.next_wave} → "
                   + ", ".join(f"{l} ${p:,.2f}" for l, p in fc.targets)
                   + f" · invalidation ${fc.invalidation:,.2f} · conf {fc.confidence:.0%}")


def main():
    syms = [s.upper() for s in sys.argv[1:]] or ["AVGO", "MRVL"]
    out = ["# Elliott + NeoWave wave counts — " + ", ".join(syms),
           f"\n_Computed {datetime.now(timezone.utc).date()} by `scripts/wave_report.py` "
           "on the live TradingView snapshots. Engine output, not hand-counted; "
           "confidence is calibrated and typically low (counts are genuinely ambiguous). "
           "Not investment advice._"]
    for sym in syms:
        out.append(f"\n## {sym}")
        for tf_label, tag, scales in TFS:
            section(out, sym, tf_label, tag, scales)
        out.append("\n---")
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(OUTMD), exist_ok=True)
    open(OUTMD, "w").write(text)
    print(text)
    print(f"\nwrote {OUTMD}")


if __name__ == "__main__":
    main()
