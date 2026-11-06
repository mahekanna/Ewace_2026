"""
brief.py — the plain-language read: what the engine thinks, what would confirm
it, what would prove it wrong, by when, and how often this kind of call has
worked before.  One bottom line.
===========================================================================
Everything else in wavelib speaks in labels (ZIGZAG, T1, void, EXTEND...).  This
module turns the current anchored count + its next-wave projection into a short
brief a non-specialist can act on as *analysis*: a directional bias with the
exact level that confirms it, the exact level that invalidates it, a time window,
a reliability figure from the causal replay (`count_history.forecast_scorecard`),
and an explicit stance — NO READ / WAIT FOR CONFIRMATION / CONFIRMED BIAS /
PLAYED OUT / STAND ASIDE.

Confirmation follows the NeoWave discipline of never acting on the label alone:
  * after a completed correction (A-B-C / W-X-Y / triangle) the expected impulse is
    confirmed only when price breaks the START of the last corrective leg (the B /
    X high or low, i.e. the pivot before the final leg);
  * after a completed impulse the expected correction is confirmed when price
    breaks the wave-4 extreme (start of wave 5).
The stop sits just beyond the last pivot; the void is the count's own invalidation.

Analysis tooling only — the stance is a reading of structure, not advice on
sizing or execution (out of scope for this repo).  Pure stdlib.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field

from .wavetree import wave_counts
from .forecast import forecast_from_count
from .confluence import score_reversal

_DEFAULT_SCALES = (0.04, 0.07, 0.12, 0.20)


def _d(t) -> str:
    return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc).strftime("%Y-%m-%d")


@dataclass
class Brief:
    symbol: str
    as_of: str
    price: float
    stance: str                    # NO READ | WAIT FOR CONFIRMATION | CONFIRMED BIAS | PLAYED OUT | STAND ASIDE
    bottom_line: str               # one sentence a non-specialist can act on
    direction: str = ""            # "up" | "down" | ""
    pattern: str = ""
    confidence: float = 0.0
    sections: list = field(default_factory=list)   # [(title, [plain sentences])]
    levels: dict = field(default_factory=dict)      # trigger/stop/void/t1/far/deadline
    reliability: dict | None = None                 # scorecard row for this pattern


def _reliability_phrase(row) -> str:
    if not row or not row.get("decided"):
        return ("no track record yet for this kind of call (run the bar-by-bar replay "
                "to get one)")
    hr = row["hit_rate"] or 0.0
    n = row["decided"]
    tier = ("a decent track record" if hr >= 0.5 and n >= 20
            else "roughly a coin flip" if hr >= 0.35
            else "a weak track record")
    return (f"{tier}: in this symbol's history, projections made from a completed "
            f"{row.get('pattern', 'count')} reached their first target {hr:.0%} of the time "
            f"({row['HIT'] + row['HIT_FULL']} of {n} decided), were proven wrong "
            f"{(row['inval_rate'] or 0):.0%} of the time"
            + (f", typically taking ~{row['median_bars_to_t1']} bars to get there"
               if row.get("median_bars_to_t1") else ""))


def decision_brief(symbol: str, bars, window: int = 300, scorecard: dict | None = None,
                   scales=_DEFAULT_SCALES, adoption_t: float | None = None) -> Brief:
    """Build the brief from the LAST bar.  `scorecard` is `forecast_scorecard(...)`
    output (per-pattern rows) from the replay; `adoption_t` is when the current
    count was first adopted (from the replay) so confirmation is judged causally
    from that bar — defaults to the last confirmed pivot of the count."""
    recent = bars[-window:] if len(bars) > window else bars
    price = recent[-1][4]
    as_of = _d(recent[-1][0])
    counts = wave_counts(recent, scales=scales, max_alternates=0)
    pc = counts[0] if counts else None
    fc = None
    if pc is not None and pc.labels:
        try:
            fc = forecast_from_count(pc, price, sequence_status="not evaluated")
        except Exception:
            fc = None

    if pc is None or not pc.labels or fc is None or not fc.targets:
        why = ("The engine could not settle on a wave count for the last "
               f"{len(recent)} bars, so it has no expectation for the next move.")
        return Brief(symbol, as_of, price, "NO READ",
                     "Nothing to act on: the structure is unclear. Wait for a clean swing to form.",
                     sections=[("Where we are", [why]),
                               ("What to do", ["Nothing. Check back after the next clear swing high or low."])])

    legs = [n for _l, n in pc.labels]
    last = legs[-1]
    running = bool(getattr(pc, "in_progress", False))
    up = fc.direction == "up"
    sgn = 1 if up else -1
    # --- levels -----------------------------------------------------------
    if running:
        # the final wave is underway: it is CONFIRMED once price exceeds the end of
        # the previous wave in the same direction (A's end for a running C, wave 3's
        # end for a running 5); the reference stop is just beyond the wave's origin
        same_dir = legs[-3] if len(legs) >= 3 else legs[0]
        trigger = same_dir.end.price
        stop = round(last.start.price * (0.99 if up else 1.01), 2)
    else:
        trigger = last.start.price               # break of the pivot BEFORE the final leg
        stop = round(last.end.price * (0.99 if up else 1.01), 2)
    void = fc.invalidation
    good = sorted((p for _lab, p in fc.targets if sgn * (p - price) > 0), key=lambda p: sgn * p)
    t1 = good[0] if good else None
    far = good[-1] if good else None
    cluster = fc.cluster[0][0] if fc.cluster else None
    adoption_t = adoption_t if adoption_t is not None else last.end.t
    deadline_t = adoption_t + fc.time_hi_days * 86400.0
    # --- status since adoption (causal: only bars after the adoption bar) ----
    after = [b for b in bars if b[0] > adoption_t]
    confirmed_t, voided_t, hit_t = None, None, None
    inv_below = void < price
    for b in after:
        t, h, l = b[0], b[2], b[3]
        if voided_t is None and ((inv_below and l <= void) or (not inv_below and h >= void)):
            voided_t = t
            break
        if confirmed_t is None and ((up and h > trigger) or (not up and l < trigger)):
            confirmed_t = t
        if t1 is not None and hit_t is None and ((up and h >= t1) or (not up and l <= t1)):
            hit_t = t
    trigger_already = (up and price > trigger) or (not up and price < trigger)
    if confirmed_t is None and trigger_already:
        confirmed_t = recent[-1][0]
    exhausted = t1 is None                       # price is already beyond every target
    expired = recent[-1][0] > deadline_t and confirmed_t is None and hit_t is None
    # --- reliability --------------------------------------------------------
    row = dict(scorecard.get(fc.pattern, {}), pattern=fc.pattern) if scorecard else None
    rel = _reliability_phrase(row)
    weak = bool(row and row.get("decided") and (row.get("hit_rate") or 0) < 0.4)
    # --- confluence at the target zone (independent confirmation strands) ---
    try:
        zone = (min(t1 or price, far or price), max(t1 or price, far or price))
        rep = score_reversal(symbol, bars[-250:], zone, bullish=up)
        confl, confl_max = rep.score, rep.max_score
    except Exception:
        confl, confl_max = 0, 7

    dirword = "UP" if up else "DOWN"
    above, below = ("above", "below") if up else ("below", "above")
    vside = "above" if void > price else "below"      # the void can sit on either side
    legs_txt = ", ".join(f"{lab} ended {_d(n.end.t)} at ${n.end.price:,.2f}"
                         for lab, n in (pc.labels[:-1] if running else pc.labels))
    last_lab = pc.labels[-1][0] if pc.labels else "?"
    where = [
        (f"On the last {len(recent)} daily bars the engine's best read is a {fc.pattern} whose "
         f"final wave {last_lab} is STILL RUNNING ({pc.degree_label} degree, {pc.confidence:.0%} "
         "confidence — low numbers are normal here; Elliott counts are interpretive)."
         if running else
         f"On the last {len(recent)} daily bars the engine's best read is a completed "
         f"{fc.pattern} ({pc.degree_label} degree) with {pc.confidence:.0%} confidence — "
         "low numbers are normal here; Elliott counts are interpretive."),
        f"Its legs: {legs_txt}" + (f"; wave {last_lab} running since {_d(last.start.t)} "
                                   f"(${last.start.price:,.2f}), now ${last.end.price:,.2f}." if running else "."),
        f"Price now: ${price:,.2f} ({as_of}).",
    ]
    expect = [
        f"Expected next: {fc.next_wave} — i.e. a move {dirword}.",
        ((f"Target: ${t1:,.2f}" if t1 == far else f"Target zone: first ${t1:,.2f}, then up to ${far:,.2f}")
         + (f"; the strongest Fibonacci overlap is ${cluster:,.2f}" if cluster else "") + "."
         if t1 else "No target in the expected direction from here (price already past them)."),
        "Targets are measured from the confirmed pivots, never from today's price; only the "
        f"levels still ahead of price are listed (the count was adopted {_d(adoption_t)}).",
        f"Time: the move should complete within ~{fc.time_lo_days:.0f}-{fc.time_hi_days:.0f} days "
        f"of {_d(adoption_t)} (by about {_d(deadline_t)}), measured against the prior "
        f"{(last.end.t - last.start.t) / 86400:.0f}-day wave"
        + (" — a long window, so this is a slow, position-scale read, not a short-term call"
           if fc.time_hi_days > 180 else "") + ".",
    ]
    pct = lambda a, b: abs(a - b) / b
    if trigger_already:
        prog = (f"Price is already {pct(price, trigger):.0%} {above} the trigger ${trigger:,.2f}, "
                "so the expected move is in progress"
                + (f"; {pct(t1, price):.0%} is left to the first target." if t1 else
                   "; it has already run past every projected target."))
    else:
        prog = (f"Price is {pct(price, trigger):.0%} away from the trigger ${trigger:,.2f}; "
                "nothing has been confirmed yet.")
    confirm = [
        (f"Confirmation: a daily close {above} ${trigger:,.2f} (the end of the previous wave in "
         "this direction) proves the running wave is genuine. Until then this is only a bias."
         if running else
         f"Confirmation: a daily close {above} ${trigger:,.2f} (the pivot before the last leg). "
         "Until then this is only a bias."),
        prog,
        f"Proven wrong: a move {vside} ${void:,.2f} voids the count — the expectation is cancelled.",
    ]
    if pct(stop, void) > 0.03:
        confirm.append(f"Nearer protective reference: just {below} the last pivot, ${stop:,.2f}.")
    confirm.append(
        f"Independent confirmation strands at the target zone right now: {confl}/{confl_max} "
        "(momentum divergence, MACD turn, volume climax, channel break, change of character, "
        "zone, cycle). Fewer than 4 means the label is NOT yet backed by price behaviour.")
    rr = (pct(t1, price) / max(pct(void, price), 1e-9)) if t1 else None
    if rr is not None:
        confirm.append(f"From here: {pct(t1, price):.0%} to the first target versus "
                       f"{pct(void, price):.0%} to the void level — reward-to-risk {rr:.1f} to 1.")

    # --- stance / bottom line ------------------------------------------------
    if voided_t:
        stance = "STAND ASIDE"
        bl = (f"The expected {dirword} move was proven wrong on {_d(voided_t)} "
              f"(price crossed ${void:,.2f}). Ignore this projection and wait for a new count.")
    elif exhausted:
        stance = "PLAYED OUT"
        bl = (f"Price (${price:,.2f}) has already moved past every level this count projected. "
              "The projection is exhausted — do not chase; wait for the next count to form.")
    elif hit_t:
        stance = "PLAYED OUT"
        bl = (f"The projection already reached its first target ${t1:,.2f} on {_d(hit_t)}. "
              "It is done — do not chase; wait for the next count to form.")
    elif expired:
        stance = "STAND ASIDE"
        bl = (f"Nothing happened within the time window (by {_d(deadline_t)}). "
              "The projection has expired; wait for a new count.")
    elif confirmed_t:
        stance = "CONFIRMED BIAS"
        bl = (f"{dirword} bias, confirmed on {_d(confirmed_t)} by the break {above} ${trigger:,.2f}. "
              + (f"Target ${t1:,.2f}" if t1 == far else f"Target zone ${t1:,.2f}-${far:,.2f}")
              + f"; the read is wrong {vside} ${void:,.2f}; "
              f"expect resolution by about {_d(deadline_t)}."
              + (" Reliability is weak for this kind of call, so treat it as a lean, not a conviction."
                 if weak else ""))
    else:
        stance = "WAIT FOR CONFIRMATION"
        bl = (f"Lean {dirword}, but do nothing yet: wait for a close {above} ${trigger:,.2f}. "
              f"If price goes {vside} ${void:,.2f} first, the read is wrong. "
              f"Window closes about {_d(deadline_t)}.")
    if confl < 4 and stance in ("CONFIRMED BIAS", "WAIT FOR CONFIRMATION"):
        bl += f" Only {confl}/{confl_max} independent strands agree — low conviction."

    if stance == "STAND ASIDE":
        what_to_do = ["Do nothing on this read. The next clean swing will produce a new count."]
    elif stance == "PLAYED OUT":
        what_to_do = ["Do nothing on this read; the move it called has happened.",
                      "A fresh count will form once price makes a new confirmed swing; check back then."]
    elif stance == "CONFIRMED BIAS":
        what_to_do = [
            f"Treat the structure as leaning {dirword} toward ${t1:,.2f}"
            + (f" (then ${far:,.2f})." if far != t1 else "."),
            f"The read is cancelled {vside} ${void:,.2f}."
            + (f" A nearer protective reference is ${stop:,.2f}." if pct(stop, void) > 0.03 else ""),
            f"If nothing happens by {_d(deadline_t)}, drop the read."]
    else:
        what_to_do = [
            f"Watch for a daily close {above} ${trigger:,.2f}. That is the only event that upgrades "
            "this from a bias to a confirmed read.",
            f"If price breaks {vside} ${void:,.2f} first, the count is void — forget it.",
            f"Re-check after {_d(deadline_t)}: an unconfirmed read past its window expires."]

    sections = [("Where we are", where), ("What the engine expects next", expect),
                ("What confirms it / what kills it", confirm),
                ("How reliable is this kind of call", [rel.capitalize() + "."]),
                ("What to do", what_to_do)]
    return Brief(symbol, as_of, price, stance, bl, fc.direction, fc.pattern, pc.confidence,
                 sections,
                 {"trigger": round(trigger, 2), "stop": stop, "void": round(void, 2),
                  "t1": t1, "far": far, "cluster": cluster, "deadline": _d(deadline_t),
                  "confirmed": _d(confirmed_t) if confirmed_t else None,
                  "voided": _d(voided_t) if voided_t else None,
                  "hit": _d(hit_t) if hit_t else None, "confluence": confl},
                 row)


GLOSSARY = [
    ("Count", "the engine's labelling of recent swings as Elliott waves (1-5 motive, A-B-C corrective, W-X-Y double correction, A-E triangle)."),
    ("Anchored count", "the committed count on the trailing 300 bars; 'recent candidate' is the cleanest small fragment, often older and less useful."),
    ("Confidence", "how well the structure obeys the rules and Fibonacci proportions; 20-50% is normal, it is not a probability of success."),
    ("Projection / forecast", "what should come next IF the count is right: direction, target levels, a void level and a time window."),
    ("T1 / far", "the nearest and farthest projected target in the expected direction."),
    ("Void (invalidation)", "the price that proves the count wrong; crossing it cancels the expectation."),
    ("Trigger (confirmation)", "the pivot before the last leg; a close beyond it is the first evidence the expected move has started. Never act on the label alone."),
    ("Time window", "NeoWave rule of thumb: the next wave takes between one third and three times the prior wave's duration."),
    ("Confluence x/7", "independent confirmation strands (momentum divergence, MACD turn, volume climax, channel break, change of character, zone, cycle). Below 4 = unconfirmed."),
    ("EXTEND / RELABEL / SHIFT", "how a held count changed: same origin with legs advanced / a different pattern / same pattern re-anchored elsewhere."),
    ("HIT / HIT_FULL / INVALIDATED / EXPIRED", "how a projection ended: nearest target reached / farthest reached / void crossed first / nothing within the time window."),
]


def brief_markdown(b: Brief) -> str:
    out = [f"## {b.symbol} — plain-language read as of {b.as_of} (${b.price:,.2f})", "",
           f"**Stance: {b.stance}.** {b.bottom_line}", ""]
    for title, lines in b.sections:
        out.append(f"**{title}**")
        out.extend(f"- {ln}" for ln in lines)
        out.append("")
    return "\n".join(out)


def brief_html(b: Brief) -> str:
    color = {"NO READ": "#7c8a91", "WAIT FOR CONFIRMATION": "#f2b134", "CONFIRMED BIAS": "#27e0c4",
             "PLAYED OUT": "#48d97a", "STAND ASIDE": "#ff5d57"}.get(b.stance, "#e8eef0")
    secs = "".join(
        f"<div class='bsec'><h3>{t}</h3><ul>" + "".join(f"<li>{ln}</li>" for ln in lines) + "</ul></div>"
        for t, lines in b.sections)
    return (f"<div class='card brief'><h2>Plain-language read — as of {b.as_of}, ${b.price:,.2f}</h2>"
            f"<div class='stance' style='color:{color}'>{b.stance}</div>"
            f"<p class='bl'>{b.bottom_line}</p><div class='bgrid'>{secs}</div></div>")


def glossary_html() -> str:
    return ("<div class='card'><h2>What the words mean</h2><ul>"
            + "".join(f"<li><b>{k}</b> — {v}</li>" for k, v in GLOSSARY) + "</ul></div>")


def glossary_markdown() -> str:
    return "### Glossary\n\n" + "\n".join(f"- **{k}** — {v}" for k, v in GLOSSARY) + "\n"
