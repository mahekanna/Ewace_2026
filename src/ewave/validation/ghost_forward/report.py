"""
validation.ghost_forward.report — markdown summary of a ghost-forward run
(the kit's ghost_forward.py report format, as a library function).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .stability import Snapshot


def _dt(t):
    return datetime.fromtimestamp(t, tz=timezone.utc)


def render(symbol: str, interval: str, snaps: List[Snapshot], outcomes: List[dict],
           m: dict, roll: int, horizon: int, out_path: Optional[str] = None) -> str:
    n = len(snaps)
    counts = m["outcomes"]
    stale = counts.get("stale", 0)
    decided = counts.get("HIT", 0) + counts.get("INVALIDATED", 0)
    lines = [
        f"# Ghost forward test — {symbol} {interval}", "",
        f"_At each of {n} candles ({_dt(snaps[0].t):%Y-%m-%d %H:%M} → "
        f"{_dt(snaps[-1].t):%Y-%m-%d %H:%M}) the forecast is built from the prior "
        f"{roll} bars only; snapshots are frozen before the next {horizon} bars label "
        "the outcome. Causal; not advice._", "",
        "## Summary",
        f"- Forecasts: **{m['forecasts']}** of {n} steps"
        + (f" ({m['forecasts']/n:.1%} fire rate)" if n else ""),
        f"- STALE/unusable: {stale} — excluded from hit-rate.",
        f"- Usable resolved: **{decided}** (HIT {counts.get('HIT', 0)} / "
        f"INVALIDATED {counts.get('INVALIDATED', 0)}); OPEN {counts.get('OPEN', 0)}.",
        f"- **Target-hit among usable: "
        + (f"{m['target_hit_rate']:.0%}**" if m['target_hit_rate'] is not None else "n/a**"),
        f"- MFE/MAE (R): {m['avg_mfe_r']} / {m['avg_mae_r']}; "
        f"median bars-to-outcome {m['median_bars_to_outcome']}.",
        f"- Next-candle direction: "
        + (f"{m['next_candle_accuracy']:.0%} (coin-flip = 50%)."
           if m['next_candle_accuracy'] is not None else "n/a."),
        f"- Episodes {m['episodes']} (avg len {m['avg_episode_length']}); repaint rate "
        + (f"{m['repaint_rate']:.0%}." if m['repaint_rate'] is not None else "n/a "
           "(one-shot signal forecaster — see stability.py docstring)."),
        "",
        "## Fired signals",
        "| time | price | dir | kind | conf | target | invalid | outcome (bars) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    by_step = {r["step"]: r for r in outcomes}
    for s in snaps:
        if not s.has_forecast:
            continue
        r = by_step[s.step]
        lines.append(
            f"| {_dt(s.t):%Y-%m-%d %H:%M} | {s.price:,.2f} | {s.direction} "
            f"| {s.kind or '-'} | {s.confidence:.0%} | {s.target:,.2f} "
            f"| {s.invalidation:,.2f} | {r['outcome']}"
            + (f" ({r['bars_to_outcome']})" if r["outcome"] in ("HIT", "INVALIDATED") else "")
            + " |")
    text = "\n".join(lines) + "\n"
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(text)
    return text
