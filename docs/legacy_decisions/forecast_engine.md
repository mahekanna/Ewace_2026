# Legacy decision — forecast engine (next-leg projection)

**Verdict: REFERENCE ONLY — never the trading engine.** (Salvage matrix P4.)

A year-long causal ghost-forward replay (AVGO+MRVL 15m, ~9,300 candles each)
showed the next-leg forecast DIRECTION is a coin flip (50–51% everywhere), the
engine's own confidence is uninformative (highest bucket resolved ZERO usable
trades), 84–92% of signals were an untimed "trend-resume" reflex, and the
counter-trend branch was 100% stale. Root cause: direction = mechanical
"opposite the last completed leg", decoupled from the wave structure.

**Disposition in the platform:** the projection machinery lives in
`ewave.signals.trade_plan` with a REF-only banner; `forecast_from_count`'s
direction never gates an automated entry (enforced by test). The trade-
management parts (confirmation trigger, structural stop, R:R, confluence
gate) were salvaged — they seeded the validated wave-3 entry.

Evidence: docs/FORWARD_GHOST_TEST_FINDINGS.md; reports/FORWARD_TEST_*.md.
