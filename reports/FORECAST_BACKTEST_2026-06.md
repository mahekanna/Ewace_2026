# Prediction-driven backtest — trading the wave FORECAST

_Generated 2026-06-07 by `scripts/run_forecast_backtest.py`. Trades the engine's forecast the institutional way (confirmation entry, structural stop, asymmetric R:R, scale-out + breakeven, conviction filter, one position at a time). Two entry models x two timeframes; every cell is a registry-logged trial. Net of 0.1% cost. Not investment advice._

## 1W — 25 instruments, 1987-08→2026-06 (buy-and-hold 13-bar Sharpe **0.228**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 3338 | 16% | -0.72 | 0.10 | -0.853 | 0% | 0.07 |
| zone | 0.25 | 2049 | 19% | -0.67 | 0.12 | -0.790 | 0% | 0.08 |
| bos | 0.15 | 48 | 56% | 0.84 | 3.13 | 0.393 | 91% | 1.82 |
| bos | 0.25 | 41 | 61% | 1.01 | 4.38 | 0.539 | 99% | 1.44 |

- Zone-entry (powered, up to 3338 trades): expectancy -0.72R@conf0.15, -0.67R@conf0.25 — **not positive** (the powered sample shows no edge).
## 1D — 26 instruments, 2006-07→2026-06 (buy-and-hold 40-bar Sharpe **0.220**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 3919 | 20% | -0.66 | 0.14 | -0.788 | 0% | 0.11 |
| zone | 0.25 | 3108 | 22% | -0.63 | 0.16 | -0.749 | 0% | 0.12 |
| bos | 0.15 | 34 | 68% | 1.12 | 5.59 | 0.662 | 99% | 1.30 |
| bos | 0.25 | 31 | 68% | 1.11 | 5.49 | 0.668 | 99% | 1.80 |

- Zone-entry (powered, up to 3919 trades): expectancy -0.66R@conf0.15, -0.63R@conf0.25 — **not positive** (the powered sample shows no edge).

## Overall verdict
- Trials this run: **8** (2 timeframes x 2 entry models x 2 conviction floors); registry total: **37**.
- Highest Sharpe cell: 1d/bos/conf0.25 — 31 trades, 1.11R, Sharpe 0.668.

> Verdict: **No durable edge.** The break-of-structure model looked faintly positive only because it was tiny/under-powered; once the EWF zone-entry model produces a properly-powered sample (hundreds of trades), expectancy is **not positive** — the forecast's reaction zones are not reliably where price turns. Trading the prediction does not beat buy-and-hold on either the weekly or the daily timeframe.
>
> Reading guide: the **zone** rows are the powered test (many trades); the **bos** rows are the conservative/under-powered one. Expectancy in R is the desk metric; PSR-vs-benchmark + CPCV are the multiple-testing-robust gates. Caveats: overlapping-instrument correlation; per-trade vs fixed-horizon benchmark Sharpe are not perfectly apples-to-apples; count confidence is calibrated, not validated. Causal throughout; setup geometry cached per (timeframe, instrument); timelines strided for runtime.
