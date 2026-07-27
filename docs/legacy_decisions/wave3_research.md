# Legacy decision — wave-3 confirmation entry

**Verdict: SALVAGE AS FLAGSHIP — validated, then made rule-faithful.**
(Salvage matrix P2 "experimental" → promoted after broad validation.)

Causal ghost-feed forward tests found positive expectancy on every symbol
tried: AVGO +0.167R/79 trades, MRVL +0.314R/119 (year, 15m), NVDA/AMD +0.4R
(9mo) — win rates 47–56% vs the ~36% random-walk threshold at that R:R. The
matrix's "sample too small" concern for the STRICT variant (3–7 trades/yr)
was confirmed and addressed by the 2026-07 operating-point sweep: pooled over
12 semis the crude entry holds (+0.30R/606 trades) and the rule-faithful
MANAGEMENT (scale-out, S&B time budget, E-10 window) is the main per-trade
improvement (+0.49R @ 25/yr/sym). No gated config met the ≥30 trades/yr bar,
so no gated profile ships as default.

**Disposition:** `ewave.signals.wave3.generate(bars, profile)` — the crude
and strict presets reproduce the originals exactly (pinned by anchor tests);
operating points live in configs/profiles.json.

Evidence: docs/WAVE3_RESULT.md; docs/RULESET.md §G-H; docs/research/OPERATING_POINT.md.
