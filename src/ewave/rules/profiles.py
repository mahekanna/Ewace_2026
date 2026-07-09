"""
rules.profiles — named rule/operating-point profiles (configs/profiles.json).
=============================================================================
A Profile is the single tunable surface of the signal engine: the wave-3
confirmation entry's knobs (docs/RULESET.md), the confluence gate, and the
risk gate. The four shipped profiles span the empirically mapped space:

  experimental       the crude-but-proven skeleton (docs/WAVE3_RESULT.md)
  sow_neowave_soft   first sweep point between crude and strict
  sow_neowave_strict rule-faithful RULESET §H (pattern-ID + >=3 strands + R:R>=2)
  classic_elliott    classical posture (hard rules mandatory, guidelines WARN)

The research track (docs/FULL_AUTOMATION_ROADMAP.md) sweeps these knobs via
ghost-forward + backtest, selecting by DSR — never raw expectancy.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional

from .. import config


@dataclass(frozen=True)
class Profile:
    name: str
    # pivot scale
    zigzag_pct: float = 0.02
    # wave-2 retracement band (golden zone; deep_hi allowed as WARN-band)
    retr_lo: float = 0.382
    retr_hi: float = 0.786
    deep_hi: Optional[float] = None
    # setup size / stop
    min_w1_frac: float = 0.01
    stop_buf: float = 0.001
    # gates
    use_momentum: bool = True             # EWO expanding in trade direction
    require_pattern_id: bool = False      # W1 must carry a NeoWave :5 motive label
    min_confluence_strands: int = 0       # Table D: a label alone never trades
    min_rr: float = 0.0                   # E-2: minimum reward:risk to T1
    # time logic
    entry_window_w2_mult: int = 0         # E-10: break within N x W2 duration (0 = off)
    sb_time_budget_w1_mult: int = 0       # S&B: max hold = N x W1 duration (0 = off)
    time_stop_bars: int = 0               # legacy fixed bar stop (0 = off)
    # management
    scale_out: bool = False               # C-1/E-5: 50% at T1, stop->breakeven

    def wave3_kwargs(self) -> dict:
        """Kwargs for the wave-3 signal generator (ewave.signals.wave3.generate)."""
        return {
            "pct": self.zigzag_pct,
            "retr_lo": self.retr_lo,
            "retr_hi": self.retr_hi,
            "deep_hi": self.deep_hi,
            "min_w1_frac": self.min_w1_frac,
            "buf": self.stop_buf,
            "use_momentum": self.use_momentum,
            "require_pattern_id": self.require_pattern_id,
            "conf_min": self.min_confluence_strands,
            "min_rr": self.min_rr,
            "entry_window_w2_mult": self.entry_window_w2_mult,
        }


def load_profiles(base_dir: Optional[str] = None) -> dict:
    """All profiles from configs/profiles.json (or .yaml) as {name: Profile}."""
    raw = config.load("profiles", base_dir=base_dir)
    known = {f.name for f in fields(Profile)} - {"name"}
    out = {}
    for name, knobs in raw.items():
        if name.startswith("_"):
            continue
        unknown = set(knobs) - known - {"_doc"}
        if unknown:
            raise config.ConfigError(
                f"profile '{name}': unknown knobs {sorted(unknown)} "
                f"(known: {sorted(known)})")
        out[name] = Profile(name=name,
                            **{k: v for k, v in knobs.items() if k in known})
    return out


def get_profile(name: str, base_dir: Optional[str] = None) -> Profile:
    profiles = load_profiles(base_dir)
    if name not in profiles:
        raise config.ConfigError(
            f"unknown profile '{name}' (have: {', '.join(sorted(profiles))})")
    return profiles[name]
