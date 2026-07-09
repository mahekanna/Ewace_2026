"""
reporting.tradingview — manual TradingView notes from Signal objects.
=====================================================================
One report FORMAT among several (docs/ARCHITECTURE.md D6): TradingView is
optional verification, not the destination. Notes state levels a human can
mark and verify; they never bark blind buy/sell commands, and forming/
unstable candidates carry a warning.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from ..signals.models import Signal, SignalStatus


def note(sig: Signal) -> str:
    t = datetime.fromtimestamp(sig.signal_time, timezone.utc)
    lines = [
        f"Symbol: {sig.symbol}",
        f"Timeframe: {sig.timeframe}",
        f"Detected candidate: {sig.pattern_type} ({sig.direction})",
        f"Candidate status: {sig.status.value}",
        f"Visible at: {t:%Y-%m-%d %H:%M} UTC",
        f"Entry trigger: {sig.entry_trigger} @ {sig.entry_price}",
        f"Invalidation level: {sig.invalidation_level}",
        f"Targets: " + ", ".join(f"{lab} {price}" for lab, price in sig.targets),
        f"Planned R:R (to T1): {sig.reward_risk}",
        f"Confluence strands: {sig.confluence_strands}/7"
        + (f"  |  tree confidence: {sig.tree_confidence}"
           if sig.tree_confidence is not None else ""),
        f"Profile: {sig.source_profile}  |  signal id: {sig.signal_id}",
        "",
        "Manual TradingView steps:",
        "1. Mark the wave-2 extreme (the invalidation level above).",
        "2. Mark the wave-1 extreme (the entry-trigger level).",
        f"3. Draw the Fib extension of wave 1 from the wave-2 extreme "
        f"(T1 = 1.618x at {sig.target_1}" +
        (f", T2 = 2.618x at {sig.target_2})." if sig.target_2 else ")."),
        "4. Verify momentum/volume/structure independently — a label alone "
        "never trades (RULESET Table D).",
        "5. Do not enter before the confirmation break; the count is void "
        "beyond the invalidation level.",
    ]
    if sig.status is SignalStatus.CANDIDATE:
        lines.insert(5, "WARNING: candidate is FORMING — levels may revise "
                        "until the trigger fires.")
    return "\n".join(lines)


def notes_markdown(signals: List[Signal], title: str = "TradingView notes") -> str:
    if not signals:
        return f"# {title}\n\n_No signals._\n"
    blocks = [f"# {title}", ""]
    for s in signals:
        blocks += ["```", note(s), "```", ""]
    return "\n".join(blocks)
