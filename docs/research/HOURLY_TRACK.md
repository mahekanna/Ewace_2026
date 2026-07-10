# HOURLY_TRACK — wave-3 entry on the 1h timeframe (fresh data, 2026-07-10)

**Question** (FULL_AUTOMATION_ROADMAP open item): is there an operating point with
**≥30 trades/yr/symbol** and a DSR-supported edge? The 15m sweep found none. This track
tests the crude `experimental` profile on the **1h timeframe**, using the fresh
single-source TradingView series (2025-12-10 → 2026-07-09, ~0.58yr, RTH, 12 semis).

## Backtest (trials #119-#130, registry/trials.jsonl)

| sym | trades | exp (R) | win | PF | maxDD (R) |
|---|---|---|---|---|---|
| AMD  | 22 | +0.84 | 68% | 3.59 | 2.0 |
| SMCI | 28 | +0.80 | 61% | 2.98 | 4.1 |
| AMAT | 17 | +0.56 | 53% | 2.17 | 5.1 |
| MU   | 26 | +0.52 | 54% | 2.12 | 4.5 |
| MRVL | 25 | +0.50 | 56% | 2.13 | 3.1 |
| ARM  | 20 | +0.46 | 55% | 2.02 | 3.0 |
| QCOM | 20 | +0.24 | 45% | 1.45 | 5.1 |
| AVGO | 14 | +0.19 | 43% | 1.37 | 3.2 |
| TSM  | 17 | +0.18 | 41% | 1.30 | 2.8 |
| LRCX | 25 | +0.14 | 40% | 1.23 | 4.3 |
| NVDA | 15 | −0.09 | 27% | 0.86 | 4.1 |
| ASML | 13 | −0.14 | 31% | 0.80 | 7.1 |

**Pooled (all 12, no selection):** 242 trades · **+0.399R** expectancy · win 49.6% ·
PF 1.79 · **34.9 trades/yr/symbol** · per-trade Sharpe 0.272 (skew +0.23, kurt 1.34).

## Ghost-forward (snapshot-freeze walk, 568 steps/symbol, horizon 32)

Signal counts match the backtest scale (15-30/symbol). Hit-rates vary widely:
SMCI 0.76, AMD 0.58, AVGO/ARM 0.50 … AMAT 0.21, ASML 0.14 — the edge is NOT uniform;
it concentrates in the momentum names of this window.

## Selection statistics (ewave.validation.stats)

- **PSR** (pooled vs SR=0): **~1.00**; **MinTRL 36** trades (we have 242) — the pooled
  sample alone is statistically sufficient.
- **Family DSR** (12 hourly trials, sr_var 0.046): **0.086**.
- **Registry-wide DSR** (130 lifetime trials, sr_var 0.283): **0.000**.

## Honest verdict

1. **The trade-rate criterion is met for the first time**: 34.9 trades/yr/symbol ≥ 30
   (the 15m sweep never exceeded ~25 gated).
2. **PSR is strong but the window is weak evidence**: 0.58 years, one regime — a
   trending semis tape (AMD/SMCI/MU rallies). The year-long 15m validation produced
   +0.17-0.31R; +0.40R pooled here is plausibly regime-flattered.
3. **DSR does not yet support promotion.** Low family DSR reflects the large
   cross-symbol dispersion (ASML/NVDA negative while SMCI/AMD huge); registry-wide DSR
   is punished by 130 lifetime trials. Per policy (CLAUDE.md: select by DSR + MinTRL,
   never raw expectancy) the hourly profile stays **research, not production**.
4. **What would settle it**: extend the 1h history to ≥2.5 years/symbol (5000 bars via
   `ewave fetch-data` on a network-open machine, or chunked MCP pulls), re-run this
   exact pair of commands (they are one-liners; every run auto-logs a trial), and
   require family DSR > 0.95 across the longer, multi-regime sample. A CPCV pass
   (`ewave.validation.stats.cpcv_splits`) over the extended sample is the final gate.

## Reproduce

```bash
ewave backtest      --symbols AVGO,MRVL,NVDA,AMD,TSM,QCOM,ASML,LRCX,MU,ARM,SMCI,AMAT --tf 1h --profile experimental
ewave ghost-forward --symbols AVGO,MRVL,NVDA,AMD,TSM,QCOM,ASML,LRCX,MU,ARM,SMCI,AMAT --tf 1h --profile experimental --roll 400 --horizon 32 --csv
```

Artifacts: `outputs/backtests/<sym>_1h_experimental/` (trades/equity/metrics) and
`outputs/ghost_forward/<sym>_1h_experimental/` (snapshots/outcomes/metrics/summary).
