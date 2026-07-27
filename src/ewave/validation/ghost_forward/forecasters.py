"""
validation.ghost_forward.forecasters — expose ewave signal generators as
gf-contract callables (`forecast(bars) -> Forecast | None`), so any profile can
be ghost-forward tested: `ewave ghost-forward --profile sow_neowave_soft`.

This is also the RESEARCH-track harness (docs/FULL_AUTOMATION_ROADMAP.md): the
wave-3 operating-point sweep = this adapter over a grid of profile knobs, every
run logged to registry/trials.jsonl, selection by DSR.
"""
from __future__ import annotations

from ...rules.profiles import Profile
from ...signals import wave3
from .core import Forecast


def wave3_forecaster(profile: Profile):
    """Causal one-shot forecaster: fires only on the wave-3 confirmation candle.
    Confidence = confluence strands /7 when gated, else a flat 0.5 (the crude
    skeleton deliberately reports no self-confidence — docs/RULESET.md §G)."""
    def forecast(bars):
        sigs = wave3.generate(bars, profile)
        if not sigs:
            return None
        s = sigs[0]
        return Forecast(
            direction="up" if s.direction == "long" else "down",
            target=s.target_1,
            invalidation=s.stop_price,
            confidence=(s.confluence_strands / 7.0
                        if profile.min_confluence_strands else 0.5),
            kind=f"wave3-{profile.name}",
            note=s.note,
            meta={"setup_confirmed_t": getattr(s, "setup_confirmed_t", 0.0) or None})
    return forecast
