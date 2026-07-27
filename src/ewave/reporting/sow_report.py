"""
sow_report.py — visual analysis page that follows the INSTRUCTOR'S method order.
================================================================================
The step sequence is the Sutra-of-Waves procedure (docs/research/SOW_METHOD.md,
Day-2 notes p9 "Steps"): timeframe → draw channel/lines → impulse-or-corrective →
diagnose the corrective family BY WAVE B (time vs a, retracement band) → count →
plot Ichimoku → execution notes. Every applicable RULESET §A-§I validator runs on
the recent structure and is shown in a full PASS/FAIL/WARN/REF table — nothing is
hidden. REF/WARN outputs are analysis only; the automated path still trades only
the wave-3 confirmation entry through the risk gates.

Fixes vs the legacy page (documented in SOW_METHOD.md compliance matrix):
 - the "recent: CORRECTION" headline bias (3-leg candidates face fewer WARN-able
   checks than 5-leg ones, so ranking by violation count always picked them) —
   this page shows the best candidate PER TYPE side by side instead;
 - the §I validators (0-B/B-D/diametric confirmations, triangle sub-rules, flat
   bands, time rules) now actually run and render;
 - Ichimoku (the SOW overlay) is computed and shown (display-only);
 - the 0-B / 2-4 / B-D confirmation lines are drawn on the chart itself.
"""
from __future__ import annotations

import datetime

from ..patterns.candidates import label_and_validate
from ..patterns.tree import wave_counts
from ..pivots.models import pivots_to_waves
from ..pivots.percentage_reversal import zigzag_causal
from ..rules import (Status, bd_confirmation, bd_line_test, classify_correction,
                     correction_time_rules, diametric_boundary_confirmation,
                     diametric_pair_checks, flat_b_band, is_extracting_triangle,
                     is_neutral_triangle, is_running_triangle, label_monowaves,
                     retracement_logic, similarity_and_balance, triangle_subrules,
                     two_four_confirmation, validate_correction, validate_impulse,
                     zero_b_confirmation, zigzag_c_check)
from ..rules.fib import blue_box_zone, fib_retrace
from ..signals.confluence import score_reversal
from ..signals.trade_plan import trade_plan


def _fmt(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")


_ST_CLS = {"PASS": "g", "FAIL": "r", "WARN": "k", "REF": "dim", "N/A": "dim",
           "UNKNOWN": "dim"}


def _rule_rows(results):
    """RuleResults -> table rows (rule, colored status, detail)."""
    out = []
    for r in results:
        cls = _ST_CLS.get(r.status.value, "dim")
        out.append(f"<tr><td>{r.rule}</td>"
                   f"<td class='{cls}'>{r.status.value}</td>"
                   f"<td class='dim'>{r.detail}</td></tr>")
    return out


def _table(rows):
    return ("<table style='width:100%;border-collapse:collapse;font-size:11.5px'>"
            "<tr><th style='text-align:left'>rule</th><th style='text-align:left'>"
            "status</th><th style='text-align:left'>detail</th></tr>"
            + "".join(rows) + "</table>")


def _recent_legs(recent, want=9):
    """Confirmed causal pivots on the chart window at the coarsest scale that
    still yields enough structure; returns (pivots, waves)."""
    for pct in (0.06, 0.04, 0.03, 0.02):
        piv = [p for p in zigzag_causal(recent, pct=pct) if p.confirmed]
        if len(piv) >= want:
            break
    waves = pivots_to_waves(piv) if len(piv) >= 2 else []
    return piv, waves


def analyze_symbol_sow(symbol, bars, tf="1d", desc="", window=300):
    """SOW-method chart data + cards for `render_analysis_page`."""
    full = bars
    recent = bars[-window:] if len(bars) > window else bars
    last_t, last_close = recent[-1][0], recent[-1][4]
    line = [[b[0], b[4]] for b in recent]

    piv, legs = _recent_legs(recent)
    now = (last_t, last_close)

    # ---------------- step 3: impulse vs corrective, best PER TYPE ---------- #
    cands = label_and_validate(recent, degrees=(0.05, 0.10, 0.15), max_candidates=40)
    best = {}
    for c in cands:
        best.setdefault(c.count_type, c)
    def _cand_line(c):
        return (f"<span class='k'>{c.count_type}</span>: {c.hard_fails} rule-breaks, "
                f"{c.warns} warns, fib quality {c.fib_score:.0%} "
                f"(scale #{c.degree})")
    step3 = [
        _cand_line(best[k]) for k in ("IMPULSE", "CORRECTION") if k in best
    ] or ["No candidate window passes the hard rules on this timeframe."]
    step3.append("Discriminators (SOW deck p45): a corrective takes MORE time than "
                 "the move it corrects (except triangle/terminal/diametric); "
                 "impulses do NOT fit parallel channels. Candidates are shown per "
                 "type — violation counts are NOT comparable across types.")

    # ---------------- step 4: which corrective? (seeing wave b) ------------- #
    step4, table_rows, lines = [], [], []
    if len(legs) >= 3:
        A, B, C = legs[-3], legs[-2], legs[-1]
        t_res = correction_time_rules([A, B])
        b_retr = B.retr(A)
        fam = ("Diametric / Triangle favoured (b faster than a)"
               if B.days < A.days else
               "all corrective patterns possible; Zigzag or FLAT most likely "
               "(b slower than a)")
        step4 = [
            f"Last three legs a/b/c: a {A.days:.1f}d, b {B.days:.1f}d, "
            f"c {C.days:.1f}d; b retraces <span class='k'>{b_retr:.0%}</span> of a.",
            f"Instructor's diagnosis rule (Day-2 p9): <span class='k'>{fam}</span>.",
            ("b &lt; 61.8% of a → <span class='k'>zigzag family</span> "
             "(deck p32)" if b_retr < 0.618 else
             "b ≥ 61.8% of a → <span class='k'>flat family</span> (deck p34)"),
        ]
        table_rows += _rule_rows(t_res)
        table_rows += _rule_rows([retracement_logic(b_retr)])
        table_rows += _rule_rows([flat_b_band(A, B)])
        table_rows += _rule_rows([zigzag_c_check([A, B, C])])
        table_rows += _rule_rows([similarity_and_balance(A, C, context="a vs c")])
        table_rows += _rule_rows(validate_correction([A, B, C]))
    else:
        step4 = ["Fewer than 3 confirmed legs on this window — Status UNKNOWN."]

    if len(legs) >= 5:
        five = legs[-5:]
        table_rows += _rule_rows(validate_impulse(five))
        # instructor's impulse TIME rule (deck p19 r16): W2>=W1, W4>=W3 time
        for i, name in ((0, "W2 vs W1"), (2, "W4 vs W3")):
            tr = correction_time_rules([five[i], five[i + 1]])
            for r in tr:
                r.rule = f"impulse time rule ({name}): " + r.rule
            table_rows += _rule_rows(tr)
        table_rows += _rule_rows(triangle_subrules(five))
        table_rows += _rule_rows([bd_line_test(five),
                                  is_extracting_triangle(five),
                                  is_neutral_triangle(five),
                                  is_running_triangle(five)])
    if len(legs) >= 7:
        table_rows += _rule_rows(diametric_pair_checks(legs[-7:]))

    # ---------------- step 2/5: confirmation lines + chart overlays --------- #
    conf_rows = []
    if len(legs) >= 3:
        A, B, C = legs[-3], legs[-2], legs[-1]
        conf_rows += _rule_rows(zero_b_confirmation(A, B, C, *now))
        lines.append([A.start.t, A.start.price, last_t,
                      _line_at(A.start, B.end, last_t), "0-B line", "#f2b134"])
    if len(legs) >= 5:
        five = legs[-5:]
        conf_rows += _rule_rows(bd_confirmation(five, *now))
        b_, d_ = five[1], five[3]
        lines.append([b_.end.t, b_.end.price, last_t,
                      _line_at(b_.end, d_.end, last_t), "B-D line", "#3aa6ff"])
        w2p, w4p = five[1].end, five[3].end
        conf_rows += _rule_rows(two_four_confirmation(
            five[4], w2p, w4p, *now, uptrend=five[0].up))
        lines.append([w2p.t, w2p.price, last_t,
                      _line_at(w2p, w4p, last_t), "2-4 line", "#48d97a"])
    if len(legs) >= 7:
        conf_rows += _rule_rows(diametric_boundary_confirmation(legs[-7:], *now))
    step5 = [_table(conf_rows)] if conf_rows else [
        "Not enough confirmed legs to place confirmation lines."]
    step5.append("SOW two-stage discipline (deck p33-38): a pattern is over only "
                 "when its line breaks in ≤ the time of the final wave, then price "
                 "exceeds the b/W4 extreme. Lines are drawn on the chart above.")

    # ---------------- step 6: Ichimoku (SOW overlay; display-only) ---------- #
    top_i = max(range(len(piv)), key=lambda i: piv[i].price) if piv else 0
    top = piv[top_i] if piv else None
    pre = piv[:top_i] or piv
    launch = min(pre, key=lambda p: p.price) if pre else None
    if top and launch and top.price > launch.price:
        rng = top.price - launch.price
        zone = (round(top.price - 0.618 * rng, 2), round(top.price - 0.382 * rng, 2))
    else:
        zone = (round(last_close * 0.95, 2), round(last_close * 1.05, 2))
    post = [p.price for p in piv if top and p.t > top.t]
    bb = blue_box_zone(launch.price, top.price,
                       min(post) if post else last_close) if top and launch else None
    rep = score_reversal(symbol, full[-250:], zone, bullish=True,
                         blue_box=bb, use_ichimoku=True)
    ich = [s for s in rep.strands if "Ichimoku" in s.name]
    step6 = [(f"{'<span class=g>&#10003;</span>' if s.confirm else '<span class=dim>&#9675;</span>'} "
              f"<b>{s.name}</b>: {s.detail}") for s in rep.strands]
    step6.append(f"<b>Score {rep.score}/{rep.max_score}</b> — Ichimoku strand "
                 "included per SOW (settings 9/26/52; causal: the cloud at t was "
                 "displaced forward 26 bars ago; chikou unusable and excluded).")

    # ---------------- macro context + fib targets ---------------------------- #
    counts = wave_counts(full, max_alternates=2)
    primary = counts[0] if counts else None
    macro = [
        f"History: <span class='k'>{len(full)}</span> {tf} bars from {_fmt(full[0][0])}.",
        ("No dominant macro count." if not primary else
         f"Primary: <span class='k'>{primary.pattern}</span> @ {primary.degree_label}, "
         f"honest confidence <span class='k'>{primary.confidence:.0%}</span> "
         f"(covers {primary.coverage:.0%})."),
        "Top-down rule (deck p56-62): this count must nest inside the "
        "higher-timeframe count — read the coarser page first.",
    ]
    fibs = fib_retrace(top.price, launch.price) if top and launch else {}
    targets = [[round(v, 2), f"{r:.3f}  ${v:,.0f}", 0.85]
               for r, v in sorted(fibs.items())]

    # ---------------- step 7: execution notes -------------------------------- #
    tp = trade_plan(full)
    step7 = []
    if tp:
        tgt = "; ".join(f"{lab} ${p:,.2f}" for lab, p in tp.targets)
        rr_txt = ("meets" if tp.reward_risk and tp.reward_risk >= 2.0
                  else "BELOW") if tp.reward_risk else "unknown vs"
        step7 += [
            f"Direction: <span class='k'>{tp.direction.upper()}</span> "
            f"(confidence {tp.confidence:.0%} — low means WAIT).",
            f"Trigger: {tp.entry_trigger}; stop <span class='r'>${tp.stop_level:,.2f}</span>; "
            f"targets <span class='g'>{tgt or 'n/a'}</span>.",
            f"R:R {tp.reward_risk if tp.reward_risk is not None else 'n/a'} — "
            f"{rr_txt} the instructor's ≥1:2 gate (deck p68-69).",
        ]
    else:
        step7 += ["No actionable plan (no clean count) — per the method, do nothing."]
    step7 += [
        "Time cycles (Kaal Chakra, deck p77-81) are OUT of this repo by design — "
        "they arrive via the chakra_quant CycleSignal seam as the 7th strand.",
        "Only the validated wave-3 confirmation entry trades automatically; "
        "everything on this page is REF analysis (docs/WAVE3_RESULT.md).",
    ]

    tier = ("HIGH-CONFIDENCE reversal" if rep.score >= 4 else
            "BUILDING — not yet confirmed" if rep.score >= 2 else
            "structurally allowed only")
    labels = ["①", "②", "③", "④", "⑤", "Ⓐ", "Ⓑ", "Ⓒ"]
    pivots = [[p.t, round(p.price, 2), (labels[i] if i < len(labels) else ""),
               ("T" if top and p is top else p.kind)] for i, p in enumerate(piv[-7:])]
    pivots.append([last_t, round(last_close, 2), "now", "N"])

    mono = label_monowaves(piv) if len(piv) >= 4 else []
    m5 = sum(1 for _w, l in mono if l.startswith(":5"))
    m3 = sum(1 for _w, l in mono if l.startswith(":3"))
    step_count = [
        f"Monowave labels (count from the faster retracement, Day-2 p9 s5): "
        f"<span class='k'>{m5}</span> :5 / <span class='k'>{m3}</span> :3 "
        f"over {len(mono)} monowaves." if mono else
        "Insufficient pivots for monowave labelling.",
        _table(table_rows) if table_rows else "No doctrine checks applicable.",
    ]

    return {
        "symbol": symbol,
        "desc": desc or symbol,
        "subtitle": f"{desc or symbol} · {tf} · last {len(recent)} bars · SOW method",
        "headline": ("SOW: " + " vs ".join(
            f"{k.lower()} ({best[k].hard_fails}F/{best[k].warns}W)" if k in best
            else f"no valid {k.lower()} window"
            for k in ("IMPULSE", "CORRECTION"))
            + f" · macro {primary.pattern if primary else 'n/a'}"),
        "price": last_close,
        "change": f"confluence {rep.score}/{rep.max_score} · {tier}",
        "asof": _fmt(last_t),
        "line": line,
        "pivots": pivots,
        "targets": targets,
        "zone": list(zone),
        "lines": lines,
        "score": rep.score,
        "cards": [
            ("Step 1-3 — timeframe, channel, impulse-or-corrective", macro + step3),
            ("Step 4 — which corrective? (seeing wave b)", step4),
            ("Doctrine rule table (RULESET §A-§I on the recent legs)", step_count),
            ("Step 5 — confirmation lines (0-B / 2-4 / B-D, two-stage)", step5),
            ("Step 6 — Ichimoku Cloud (SOW overlay)", step6),
            ("Step 7 — execution notes (hourly/15m; R:R gate)", step7),
        ],
    }


def _line_at(p1, p2, t):
    """Price of the straight line through pivots p1,p2 at time t."""
    if p2.t == p1.t:
        return p2.price
    slope = (p2.price - p1.price) / (p2.t - p1.t)
    return p1.price + slope * (t - p1.t)
