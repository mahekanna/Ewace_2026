# Multi-regime Deflated Sharpe report — reversal strategy (weekly)

_Generated 2026-06-06 by `scripts/run_multiregime.py`. Pooled across **25 instruments** spanning multiple asset classes and **1987-08 → 2026-06** of WEEKLY history (so the sample contains the 2000, 2008, 2020 and 2022 regimes). Triple-barrier exits (+pt/-sl/13-bar), net of 0.1% cost. Not investment advice._

**Buy-and-hold benchmark** (13-bar horizon): Sharpe **0.228** (42086 samples) — the bar the strategy must clear.

## Regime coverage (per instrument)
| instrument | symbol | weekly bars | from | to |
|---|---|---|---|---|
| AMAT | NASDAQ:AMAT | 2000 | 1988-02 | 2026-06 |
| AMD | NASDAQ:AMD | 2000 | 1988-02 | 2026-06 |
| ASML | NASDAQ:ASML | 1630 | 1995-03 | 2026-06 |
| AVGO | NASDAQ:AVGO | 879 | 2009-08 | 2026-06 |
| BTCUSDT | BINANCE:BTCUSDT | 460 | 2017-08 | 2026-06 |
| DJI | TVC:DJI | 2000 | 1988-02 | 2026-06 |
| ETHUSDT | BINANCE:ETHUSDT | 460 | 2017-08 | 2026-06 |
| EURUSD | FX:EURUSD | 2000 | 1988-02 | 2026-05 |
| GOLD | TVC:GOLD | 2000 | 1987-08 | 2026-05 |
| JNJ | NYSE:JNJ | 2000 | 1988-02 | 2026-06 |
| JPM | NYSE:JPM | 2000 | 1988-02 | 2026-06 |
| KO | NYSE:KO | 2000 | 1988-02 | 2026-06 |
| LRCX | NASDAQ:LRCX | 2000 | 1988-02 | 2026-06 |
| MRVL | NASDAQ:MRVL | 1354 | 2000-06 | 2026-06 |
| MU | NASDAQ:MU | 2000 | 1988-02 | 2026-06 |
| NDX | NASDAQ:NDX | 2000 | 1988-02 | 2026-06 |
| NVDA | NASDAQ:NVDA | 1429 | 1999-01 | 2026-06 |
| PG | NYSE:PG | 2000 | 1988-02 | 2026-06 |
| QCOM | NASDAQ:QCOM | 1800 | 1991-12 | 2026-06 |
| SMCI | NASDAQ:SMCI | 1002 | 2007-03 | 2026-06 |
| SPX | SP:SPX | 2000 | 1988-02 | 2026-06 |
| TSM | NYSE:TSM | 1496 | 1997-10 | 2026-06 |
| VIX | TVC:VIX | 1901 | 1990-01 | 2026-06 |
| WMT | NYSE:WMT | 2000 | 1988-02 | 2026-06 |
| XOM | NYSE:XOM | 2000 | 1988-02 | 2026-06 |

## Variants tried (each is a 'trial' logged to `registry/trials.jsonl`)
| score_thr | +pt / -sl | events | Sharpe | PSR vs buy&hold | CPCV 5%ile PF |
|---|---|---|---|---|---|
| 3 | 0.1/0.07 | 632 | 0.127 | 1% | 0.91 |
| 3 | 0.15/0.1 | 632 | 0.164 | 5% | 1.07 |
| 4 | 0.1/0.07 | 104 | 0.087 | 8% | 0.78 |
| 4 | 0.15/0.1 | 104 | 0.119 | 13% | 0.59 |

## Deflated verdict (vs buy-and-hold)
- Pooled decided events across all variants: **1472** (vs the handful per symbol on the daily report) — the multi-regime sample.
- Best variant: score_threshold=3, +pt/-sl=0.15/0.1 (Sharpe 0.164 vs buy&hold 0.228, 632 events).
- Beats buy-and-hold Sharpe: **False**; PSR vs buy&hold: **5%**.  (>=30-event variants only.)
- Variants tried this run: **4**; total in registry: **17**.
- **Deflated Sharpe (vs 0, corrected for 4 trials): 100%**.

> Verdict: **No edge over buy-and-hold even across regimes.** The best variant's Sharpe (0.164) does not beat the benchmark (0.228); PSR-vs-benchmark 5%. The honest result the multi-regime test exists to surface.
>
> CPCV 5th-pctile out-of-sample profit factor (table above) is the most robust single number — it purges/embargoes folds so adjacent overlapping weekly signals can't leak. This report is the regime-diversity answer to the daily DSR report's main caveat; remaining caveats: signals on different instruments are not fully independent (sector/beta correlation).
>
> Replay settings: labelling context capped at 300 bars and the timeline sampled every 2 bars for tractable runtime — both are causal (past-only) and, on weekly data where a reversal zone persists for several bars, do not materially change the decided-event set.
