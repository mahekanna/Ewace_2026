"""
pivots.models — the pivot contract + visibility helpers.
========================================================
`Pivot` itself lives in `ewave.rules.result` (single owner, D7); this module
adds the causal-visibility helpers every consumer should go through.
"""
from __future__ import annotations

from typing import List, Optional

from ..rules.result import Pivot, Wave


def visible(pivots: List[Pivot], now_t: float) -> List[Pivot]:
    """Only pivots KNOWABLE at `now_t`: confirmed, with confirmed_t <= now_t.
    This is the gate every signal/pattern path must pass pivots through
    (docs/NO_LOOKAHEAD_POLICY.md §1)."""
    return [p for p in pivots
            if p.confirmed_t is not None and p.confirmed_t <= now_t]


def provisional_last(pivots: List[Pivot]) -> Optional[Pivot]:
    """The still-forming final extreme (confirmed_t=None), if present."""
    if pivots and pivots[-1].confirmed_t is None:
        return pivots[-1]
    return None


def pivots_to_waves(pivots: List[Pivot], labels: Optional[List[str]] = None) -> List[Wave]:
    """Consecutive pivots -> Wave segments (optionally labelled)."""
    waves = [Wave(pivots[i], pivots[i + 1]) for i in range(len(pivots) - 1)]
    if labels:
        for w, lab in zip(waves, labels):
            w.label = lab
    return waves
