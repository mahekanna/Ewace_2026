# Legacy decision — ghost-forward validation kit

**Verdict: SALVAGE AS CORE INFRASTRUCTURE.** (Salvage matrix P1.)

Ghost-feeding (candle-by-candle causal replay with snapshot freeze before
outcome labeling) is the validation method that exposed both the forecast's
missing edge and the stale-anchor bug that backtests hid. It is the
platform's mandatory gate between "signal exists" and "signal is tradable".

**Disposition:** kit core moved to `ewave.validation.ghost_forward`
(`core.py` = the causal walk; `stability.py` = snapshot-freeze → outcome
labeling → stability/repaint/lag metrics; enforced: labeling an unfrozen
snapshot set raises). `ghost_forward_kit/` remains as thin shims so the
portable kit and any vendored copies keep working.

Evidence: ghost_forward_kit/docs/05_METHODOLOGY.md; docs/NO_LOOKAHEAD_POLICY.md §3.
