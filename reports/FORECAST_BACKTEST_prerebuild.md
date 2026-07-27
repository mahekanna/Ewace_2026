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
- Direction skill (no stop/target, 19784 signals): signed mean -0.82% vs buy-and-hold +5.28%, win 49%, Sharpe -0.036 — **does NOT beat always-long**.
## 1D — 26 instruments, 2006-07→2026-06 (buy-and-hold 40-bar Sharpe **0.220**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 3919 | 20% | -0.66 | 0.14 | -0.788 | 0% | 0.11 |
| zone | 0.25 | 3108 | 22% | -0.63 | 0.16 | -0.749 | 0% | 0.12 |
| bos | 0.15 | 34 | 68% | 1.12 | 5.59 | 0.662 | 99% | 1.30 |
| bos | 0.25 | 31 | 68% | 1.11 | 5.49 | 0.668 | 99% | 1.80 |

- Zone-entry (powered, up to 3919 trades): expectancy -0.66R@conf0.15, -0.63R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 15763 signals): signed mean +0.60% vs buy-and-hold +4.10%, win 52%, Sharpe +0.032 — **does NOT beat always-long**.
## 4H — 12 instruments, 2016-06→2026-06 (buy-and-hold 30-bar Sharpe **0.230**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 2144 | 25% | -0.56 | 0.19 | -0.678 | 0% | 0.16 |
| zone | 0.25 | 1939 | 27% | -0.54 | 0.21 | -0.643 | 0% | 0.17 |
| bos | 0.15 | 20 | 55% | 0.80 | 1.97 | 0.296 | 61% | 0.53 |
| bos | 0.25 | 18 | 56% | 0.89 | 2.06 | 0.313 | 63% | 0.65 |

- Zone-entry (powered, up to 2144 trades): expectancy -0.56R@conf0.15, -0.54R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 9172 signals): signed mean +0.69% vs buy-and-hold +2.74%, win 52%, Sharpe +0.056 — **does NOT beat always-long**.
## 1H — 12 instruments, 2023-07→2026-06 (buy-and-hold 48-bar Sharpe **0.186**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 1094 | 33% | -0.43 | 0.29 | -0.508 | 0% | 0.20 |
| zone | 0.25 | 1041 | 33% | -0.43 | 0.29 | -0.507 | 0% | 0.18 |
| bos | 0.15 | 12 | 58% | 0.58 | 0.91 | -0.038 | 23% | 0.31 |
| bos | 0.25 | 12 | 58% | 0.58 | 0.91 | -0.038 | 23% | 0.31 |

- Zone-entry (powered, up to 1094 trades): expectancy -0.43R@conf0.15, -0.43R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 5819 signals): signed mean +0.70% vs buy-and-hold +1.80%, win 53%, Sharpe +0.072 — **does NOT beat always-long**.
## 15M — 12 instruments, 2025-08→2026-06 (buy-and-hold 48-bar Sharpe **0.191**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 626 | 34% | -0.40 | 0.32 | -0.481 | 0% | 0.26 |
| zone | 0.25 | 610 | 34% | -0.40 | 0.31 | -0.487 | 0% | 0.24 |
| bos | 0.15 | 5 | 60% | 0.00 | 1.31 | 0.105 | 43% | n/a |
| bos | 0.25 | 5 | 60% | 0.00 | 1.31 | 0.105 | 43% | n/a |

- Zone-entry (powered, up to 626 trades): expectancy -0.40R@conf0.15, -0.40R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 5162 signals): signed mean +0.28% vs buy-and-hold +0.97%, win 52%, Sharpe +0.052 — **does NOT beat always-long**.

## Overall verdict
- Trials this run: **20** (5 timeframes x 2 entry models x 2 conviction floors); registry total: **57**.
- Highest Sharpe cell: 1d/bos/conf0.25 — 31 trades, 1.11R, Sharpe 0.668.
- Direction skill across timeframes: 1W 49% win, Sharpe -0.036; 1D 52% win, Sharpe +0.032; 4H 52% win, Sharpe +0.056; 1H 53% win, Sharpe +0.072; 15M 52% win, Sharpe +0.052 — marginally above a coin flip on intraday, but Sharpe is noise-level and none beats always-long.

> Verdict: **No durable edge — confirmed across all 5 timeframes (1W→15M).** Once the EWF zone-entry model produces a properly-powered sample (626–3,919 trades per timeframe), expectancy is NEGATIVE on every timeframe (−0.40 to −0.72 R) — the forecast's reaction zones are not reliably where price turns. The mechanics-free direction test edges just above a coin flip on intraday (52–53%) but its Sharpe is noise-level (~0.05) and never beats buy-and-hold on any timeframe; on weekly it is below 50%. The faintly-positive break-of-structure rows are all tiny samples (5–48 trades). Trading the wave prediction has no tradeable edge at any horizon tested.
>
> Reading guide: the **zone** rows are the powered test (many trades); the **bos** rows are the conservative/under-powered one. Expectancy in R is the desk metric; PSR-vs-benchmark + CPCV are the multiple-testing-robust gates. Caveats: overlapping-instrument correlation; per-trade vs fixed-horizon benchmark Sharpe are not perfectly apples-to-apples; count confidence is calibrated, not validated. Causal throughout; setup geometry cached per (timeframe, instrument); timelines strided for runtime.
