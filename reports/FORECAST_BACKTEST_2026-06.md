# Prediction-driven backtest — trading the wave FORECAST (weekly)

_Generated 2026-06-07 by `scripts/run_forecast_backtest.py`. Trades the engine's forecast/trade_plan the institutional way: confirmation entry, structural stop, asymmetric R:R filter, scale-out + breakeven, conviction filter, one position at a time. Pooled across **25 instruments** / multiple asset classes, weekly **1987-08 → 2026-06** (2000/2008/2020/2022 regimes), net of 0.1% cost. Not investment advice._

**Buy-and-hold benchmark** (13-bar horizon): Sharpe **0.228** — the bar to clear.

## Variants tried (conviction x reward:risk; each a logged trial)
| conf≥ | RR≥ | trades | long/short | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|---|
| 0.15 | 1.5 | 48 | 28/20 | 56% | 0.84 | 3.13 | 0.393 | 91% | 1.82 |
| 0.15 | 2.5 | 31 | 19/12 | 52% | 1.08 | 2.22 | 0.286 | 63% | 0.90 |
| 0.25 | 1.5 | 41 | 25/16 | 61% | 1.01 | 4.38 | 0.539 | 99% | 1.44 |
| 0.25 | 2.5 | 27 | 18/9 | 63% | 1.38 | 6.68 | 0.625 | 100% | 1.77 |

## Verdict
- Best variant: conf≥0.25, RR≥1.5 — 41 trades, win rate 61%, **expectancy 1.01 R/trade**, profit factor 4.38.
- Sharpe 0.539 vs buy-and-hold 0.228 -> beats B&H: **True**; PSR vs B&H **99%**.
- Variants this run: **4**; registry total: **29**; Deflated Sharpe (vs 0, 4 trials): **100%**.
- Conviction check: raising the confidence floor 0.15→0.25 moves mean Sharpe 0.340→0.582 and mean expectancy 0.96R→1.20R — the filter HELPS (higher-confidence counts trade better).

> Verdict: **Encouraging but NOT validated — too few trades.** Traded the institutional way, all four variants show POSITIVE expectancy (0.84–1.38R), the confidence filter behaves correctly (higher conviction → better), and the best variant's PSR-vs-benchmark (99%) clears 95%. BUT the entire study is only **147 trades** across 25 instruments over 39 years (~1–2 per instrument per decade) — wildly under-powered. This is a *promising lead*, not a validated edge.
>
> This is the honest test of EW/NeoWave's *predictive* claim (the reversal-score backtest never used the forecast). Why so few trades: a conservative break-of-structure entry with the stop at the corrective-leg extreme makes most setups fail the R:R filter (median RR ≈ 0.6) — i.e. the forecast's targets often don't justify the structural risk. A tighter *zone* entry (enter inside the predicted reaction zone, stop just beyond invalidation) would yield more, higher-RR trades — a different, equally valid test, and the natural next experiment. The result is therefore entry-model dependent (the EW discretion ceiling).
>
> Honesty caveats: tiny, overlapping-instrument sample; per-trade returns vs a fixed-horizon benchmark Sharpe are not perfectly apples-to-apples; count confidence is calibrated, not validated. Replay is causal (plan at bar t from bars[..t]); labelling window 300 bars, strided every 2 bars.
