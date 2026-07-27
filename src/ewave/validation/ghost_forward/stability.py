"""
validation.ghost_forward.stability — snapshot freeze → outcome labeling → metrics.
==================================================================================
The two-pass discipline (docs/NO_LOOKAHEAD_POLICY.md §3):

  Pass A (causal): walk the series; at each candle hand the forecaster only
    prior bars; persist a SNAPSHOT row of exactly what was visible. The
    snapshot file is written before pass B ever looks at a future bar.
  Pass B (labeling): for each frozen snapshot, ghost-feed the next `horizon`
    bars to label the outcome (HIT/INVALIDATED/OPEN/stale), MFE/MAE in R
    multiples, and bars-to-outcome. Refuses to run on an unfrozen snapshot set.

Metrics (automation spec §10): counts per outcome, target-hit / invalidation
rates among usable calls, average MFE/MAE (R), median bars-to-outcome,
episode stability (standing-call forecasters), repaint rate, next-candle
directional accuracy. For ONE-SHOT signal forecasters (e.g. the wave-3
confirmation entry, which fires only on its trigger candle) episodes are
1-step by design — read MFE/MAE/hit-rate, not episode stability, for those.
"""
from __future__ import annotations

import json
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from .core import _norm, resolve


@dataclass
class Snapshot:
    step: int
    t: float
    price: float
    direction: Optional[str] = None
    target: Optional[float] = None
    invalidation: Optional[float] = None
    confidence: Optional[float] = None
    kind: Optional[str] = None
    note: str = ""
    # provenance (Ghost_Forward_Validation_Spec §10)
    profile: str = ""
    config_hash: str = ""
    setup_confirmed_t: Optional[float] = None   # when the setup became knowable

    @property
    def has_forecast(self) -> bool:
        return self.direction is not None


def snapshot_pass(bars, forecaster, roll: int = 400, forward="all",
                  horizon: int = 32, out_path=None, profile: str = "",
                  config_hash: str = "") -> List[Snapshot]:
    """Pass A: causal walk, snapshot every step; optionally persist (freeze)."""
    n = len(bars)
    fwd = n if forward in ("all", None) else int(forward)
    start = max(roll, n - fwd)
    snaps: List[Snapshot] = []
    for step, t in enumerate(range(start, n - horizon)):
        window = bars[max(0, t + 1 - roll):t + 1]
        fc = _norm(forecaster(window))
        row = Snapshot(step=step, t=bars[t][0], price=bars[t][4],
                       profile=profile, config_hash=config_hash)
        if fc is not None:
            row.direction, row.target = fc.direction, fc.target
            row.invalidation, row.confidence = fc.invalidation, fc.confidence
            row.kind, row.note = fc.kind, fc.note
            if fc.meta:
                row.setup_confirmed_t = fc.meta.get("setup_confirmed_t")
        snaps.append(row)
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            for s in snaps:
                f.write(json.dumps(asdict(s)) + "\n")
    return snaps


def outcome_pass(bars, snaps: List[Snapshot], roll: int = 400, forward="all",
                 horizon: int = 32, frozen: bool = False,
                 out_path=None) -> List[dict]:
    """Pass B: label each FROZEN snapshot using only bars after its step.

    `frozen=True` asserts pass A persisted first — labeling an unfrozen set is
    a policy violation and raises."""
    if not frozen:
        raise RuntimeError(
            "outcome_pass on an unfrozen snapshot set — persist snapshots first "
            "(docs/NO_LOOKAHEAD_POLICY.md §3 snapshot-freeze)")
    n = len(bars)
    fwd = n if forward in ("all", None) else int(forward)
    start = max(roll, n - fwd)
    out: List[dict] = []
    for s in snaps:
        t = start + s.step
        row = {"step": s.step, "t": s.t, "outcome": "no-forecast",
               "bars_to_outcome": 0, "mfe_r": None, "mae_r": None,
               "next_up": (bars[t + 1][4] >= bars[t][4]) if t + 1 < n else None}
        if s.has_forecast:
            fc = type("F", (), {"direction": s.direction, "target": s.target,
                                "invalidation": s.invalidation})()
            future = bars[t + 1:t + 1 + horizon]
            outcome, nbar = resolve(fc, future, s.price)
            row["outcome"], row["bars_to_outcome"] = outcome, nbar
            risk = abs(s.price - s.invalidation)
            if risk > 0 and future:
                if s.direction == "up":
                    mfe = max(b[2] for b in future) - s.price
                    mae = s.price - min(b[3] for b in future)
                else:
                    mfe = s.price - min(b[3] for b in future)
                    mae = max(b[2] for b in future) - s.price
                row["mfe_r"] = round(mfe / risk, 3)
                row["mae_r"] = round(mae / risk, 3)
        out.append(row)
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            for r in out:
                f.write(json.dumps(r) + "\n")
    return out


def _episodes(snaps: List[Snapshot]) -> List[dict]:
    """Group consecutive same-call snapshots into episodes (standing-call
    forecasters). A call is 'the same' if direction+kind match and the target
    moved < 1%."""
    eps: List[dict] = []
    cur = None
    for s in snaps:
        if not s.has_forecast:
            if cur:
                cur["ended_by"] = "vanished"
                eps.append(cur)
                cur = None
            continue
        same = (cur and cur["direction"] == s.direction and cur["kind"] == s.kind
                and cur["target"] and s.target
                and abs(s.target - cur["target"]) <= 0.01 * abs(cur["target"]))
        if same:
            cur["length"] += 1
            cur["target"] = s.target
            cur["conf_last"] = s.confidence
        else:
            if cur:
                cur["ended_by"] = "revised"
                eps.append(cur)
            cur = {"start_step": s.step, "direction": s.direction, "kind": s.kind,
                   "target": s.target, "length": 1, "ended_by": None,
                   "conf_first": s.confidence, "conf_last": s.confidence}
    if cur:
        cur["ended_by"] = "series_end"
        eps.append(cur)
    # spec six-state mapping (Ghost_Forward_Validation_Spec §13):
    #   series_end -> stable ; revised -> reclassified ; vanished -> disappeared
    #   upgraded/downgraded from confidence drift within the episode
    for e in eps:
        if e["ended_by"] == "series_end":
            e["state"] = "stable"
        elif e["ended_by"] == "revised":
            e["state"] = "reclassified"
        else:
            e["state"] = "disappeared"
        c0, c1 = e.get("conf_first"), e.get("conf_last")
        if c0 is not None and c1 is not None and e["state"] == "stable":
            if c1 > c0 + 1e-9:
                e["state"] = "upgraded"
            elif c1 < c0 - 1e-9:
                e["state"] = "downgraded"
    return eps


def metrics(snaps: List[Snapshot], outcomes: List[dict]) -> dict:
    n = len(snaps)
    with_fc = [s for s in snaps if s.has_forecast]
    counts = {}
    for r in outcomes:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    decided = counts.get("HIT", 0) + counts.get("INVALIDATED", 0)
    mfes = [r["mfe_r"] for r in outcomes if r["mfe_r"] is not None]
    maes = [r["mae_r"] for r in outcomes if r["mae_r"] is not None]
    nbars = [r["bars_to_outcome"] for r in outcomes
             if r["outcome"] in ("HIT", "INVALIDATED")]
    dir_pairs = [(s, r) for s, r in zip(snaps, outcomes)
                 if s.has_forecast and r["next_up"] is not None]
    eps = _episodes(snaps)
    ended = [e for e in eps if e["ended_by"] != "series_end"]
    return {
        "steps": n,
        "forecasts": len(with_fc),
        "outcomes": counts,
        "target_hit_rate": round(counts.get("HIT", 0) / decided, 4) if decided else None,
        "invalidation_rate": round(counts.get("INVALIDATED", 0) / decided, 4) if decided else None,
        "avg_mfe_r": round(sum(mfes) / len(mfes), 3) if mfes else None,
        "avg_mae_r": round(sum(maes) / len(maes), 3) if maes else None,
        "median_bars_to_outcome": statistics.median(nbars) if nbars else None,
        "next_candle_accuracy": round(
            sum(1 for s, r in dir_pairs if (s.direction == "up") == r["next_up"])
            / len(dir_pairs), 4) if dir_pairs else None,
        "episodes": len(eps),
        "avg_episode_length": round(sum(e["length"] for e in eps) / len(eps), 2) if eps else None,
        "repaint_rate": round(sum(1 for e in ended if e["ended_by"] == "vanished")
                              / len(ended), 4) if ended else None,
        "stability_states": {st: sum(1 for e in eps if e.get("state") == st)
                             for st in ("stable", "upgraded", "downgraded",
                                        "reclassified", "disappeared")},
        "repaint_level": _repaint_level(snaps, eps, ended),
        **_lag_metrics(snaps),
    }


def _repaint_level(snaps: List[Snapshot], eps, ended) -> str:
    """Spec §14 five-level classification. CRITICAL = a snapshot timestamp
    moved backward — structurally impossible in this engine (asserted); the
    remaining levels grade the vanish rate of ended episodes."""
    ts = [s.t for s in snaps]
    assert ts == sorted(ts), "CRITICAL repaint: snapshot timestamps not monotonic"
    if not ended:
        return "NONE"
    rate = sum(1 for e in ended if e["ended_by"] == "vanished") / len(ended)
    if rate == 0:
        return "NONE"
    if rate < 0.10:
        return "LOW"
    if rate < 0.30:
        return "MEDIUM"
    return "HIGH"


def _lag_metrics(snaps: List[Snapshot]) -> dict:
    """Signal-lag metrics (spec §12 late_signal_*): bars/seconds between the
    setup becoming knowable (setup_confirmed_t) and the signal firing."""
    lags = [s.t - s.setup_confirmed_t for s in snaps
            if s.has_forecast and s.setup_confirmed_t]
    if not lags:
        return {"late_signal_rate": None, "avg_signal_lag_secs": None}
    late = sum(1 for x in lags if x > 0)
    return {"late_signal_rate": round(late / len(lags), 4),
            "avg_signal_lag_secs": round(sum(lags) / len(lags), 1)}


def run(bars, forecaster, roll: int = 400, forward="all", horizon: int = 32,
        out_dir: Optional[str] = None) -> dict:
    """Full snapshot-freeze → outcome-label → metrics pipeline."""
    snap_path = Path(out_dir) / "snapshots.jsonl" if out_dir else None
    out_path = Path(out_dir) / "outcomes.jsonl" if out_dir else None
    snaps = snapshot_pass(bars, forecaster, roll, forward, horizon, snap_path)
    # pass A completed (and persisted when out_dir given) before any future
    # bar is read — the snapshot set is frozen by construction here
    outcomes = outcome_pass(bars, snaps, roll, forward, horizon,
                            frozen=True, out_path=out_path)
    m = metrics(snaps, outcomes)
    if out_dir:
        with open(Path(out_dir) / "metrics.json", "w") as f:
            json.dump(m, f, indent=1)
    return m
