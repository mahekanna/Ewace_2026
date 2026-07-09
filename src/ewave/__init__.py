"""
ewave — Elliott Wave / NeoWave full-automation research platform.
=================================================================
Pipeline: data → causal pivots → mono-waves → rules → candidates → signals →
ghost-forward validation → backtest → risk → paper trading.

Design ground rules (docs/ARCHITECTURE.md, docs/NO_LOOKAHEAD_POLICY.md):
- Pure-stdlib core; optional extras only behind import guards in adapters/reporting.
- Causality is non-negotiable: a pivot exists at `t` but is USABLE only at its
  `confirmed_t`; every signal carries `signal_time` = the bar that made it visible.
- Detection ≠ signal ≠ risk ≠ execution ≠ reporting — separate modules, testable alone.
- The flagship signal is the wave-3 confirmation entry (empirically validated:
  docs/WAVE3_RESULT.md); the next-leg forecast direction is REF/reference-only
  (disproven: docs/FORWARD_GHOST_TEST_FINDINGS.md).

The legacy `wavelib` package remains importable as a thin shim over these modules.
"""

__version__ = "0.3.0"
