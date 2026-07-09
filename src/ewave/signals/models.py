"""
signals.models — the structured Signal object (automation spec §9).
===================================================================
A Signal is frozen the moment it becomes visible: `signal_time` is the bar
that made it knowable, `visible_bars_until` the last bar it was built from
(identical here — signals fire ON the confirmation candle), and it is
persisted BEFORE any outcome is evaluated (docs/NO_LOOKAHEAD_POLICY.md §3).
Sizing fields stay None until the risk engine approves (separation of
concerns: a signal proposes, risk disposes).
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class SignalStatus(Enum):
    CANDIDATE = "candidate"       # setup visible, trigger not yet fired
    CONFIRMED = "confirmed"       # trigger fired (wave-3 signals are born here)
    ENTERED = "entered"           # order filled
    EXITED = "exited"             # closed at target/stop/management
    INVALIDATED = "invalidated"   # invalidation level hit before entry
    EXPIRED = "expired"           # entry window elapsed without a fill


@dataclass
class Signal:
    symbol: str
    timeframe: str
    signal_time: float            # bar time when the signal became visible
    pattern_type: str             # e.g. "wave3_impulse"
    direction: str                # "long" | "short"
    entry_trigger: str            # e.g. "break_close_beyond_w1_extreme"
    entry_price: float
    stop_price: float
    targets: List[Tuple[str, float]]   # [(label, price), ...] T1 first
    invalidation_level: float     # count-voiding level (== structural stop)
    source_profile: str
    visible_bars_until: float = 0.0    # last bar the signal was built from
    status: SignalStatus = SignalStatus.CONFIRMED
    # decomposed confidence (each component independently auditable)
    reward_risk: float = 0.0           # to T1
    confluence_strands: int = 0        # Table D strands satisfied
    momentum: float = 0.0              # EWO at signal
    w2_retracement: float = 0.0        # pullback depth (fraction of W1)
    tree_confidence: Optional[float] = None   # patterns.tree context (D5)
    stability_score: Optional[float] = None   # filled by ghost-forward later
    setup_confirmed_t: Optional[float] = None  # when the setup became knowable (lag metric)
    # risk-engine outputs (None until approved)
    position_size: Optional[float] = None
    risk_amount: Optional[float] = None
    note: str = ""
    engine_version: str = ""
    signal_id: str = ""

    def __post_init__(self):
        if not self.visible_bars_until:
            self.visible_bars_until = self.signal_time
        if not self.engine_version:
            from .. import __version__
            self.engine_version = __version__
        if not self.signal_id:
            key = (f"{self.symbol}|{self.timeframe}|{int(self.signal_time)}|"
                   f"{self.pattern_type}|{self.direction}|{self.source_profile}")
            self.signal_id = hashlib.sha1(key.encode()).hexdigest()[:12]

    @property
    def target_1(self) -> Optional[float]:
        return self.targets[0][1] if self.targets else None

    @property
    def target_2(self) -> Optional[float]:
        return self.targets[1][1] if len(self.targets) > 1 else None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        d["targets"] = [list(t) for t in self.targets]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Signal":
        d = dict(d)
        d["status"] = SignalStatus(d.get("status", "confirmed"))
        d["targets"] = [tuple(t) for t in d.get("targets", [])]
        return cls(**d)


def from_wave3(sig, *, profile, symbol: str, timeframe: str,
               tree_confidence: Optional[float] = None) -> Signal:
    """Adapt a Wave3Signal (signals.wave3) into the platform Signal object."""
    return Signal(
        symbol=symbol.upper(), timeframe=timeframe,
        signal_time=sig.entry_t,
        pattern_type="wave3_impulse", direction=sig.direction,
        entry_trigger="break_close_beyond_w1_extreme",
        entry_price=sig.entry, stop_price=sig.stop,
        targets=list(sig.targets),
        invalidation_level=sig.stop,
        source_profile=profile.name,
        reward_risk=sig.reward_risk,
        confluence_strands=sig.strands,
        momentum=sig.ewo,
        w2_retracement=sig.retr,
        tree_confidence=tree_confidence,
        setup_confirmed_t=getattr(sig, "setup_confirmed_t", 0.0) or None,
        note=sig.note,
    )
