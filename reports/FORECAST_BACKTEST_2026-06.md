# Prediction-driven backtest — trading the wave FORECAST

_Generated 2026-06-12 by `scripts/run_forecast_backtest.py`. Trades the engine's forecast the institutional way (confirmation entry, structural stop, asymmetric R:R, scale-out + breakeven, conviction filter, one position at a time). Two entry models x two timeframes; every cell is a registry-logged trial. Net of 0.1% cost. Not investment advice._

## 1W — 25 instruments, 1987-08→2026-06 (buy-and-hold 13-bar Sharpe **0.228**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 1421 | 16% | -0.64 | 0.23 | -0.549 | 0% | 0.15 |
| zone | 0.25 | 1014 | 19% | -0.57 | 0.27 | -0.482 | 0% | 0.18 |
| bos | 0.15 | 636 | 75% | 0.51 | 5.59 | 0.476 | 100% | 3.20 |
| bos | 0.25 | 460 | 74% | 0.48 | 5.40 | 0.478 | 100% | 3.31 |

- Zone-entry (powered, up to 1421 trades): expectancy -0.64R@conf0.15, -0.57R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 18994 signals): signed mean -0.27% vs buy-and-hold +5.28%, win 48%, Sharpe -0.013 — **does NOT beat always-long**.
## 1D — 26 instruments, 2006-07→2026-06 (buy-and-hold 40-bar Sharpe **0.220**)
| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |
|---|---|---|---|---|---|---|---|---|
| zone | 0.15 | 2200 | 17% | -0.61 | 0.23 | -0.584 | 0% | 0.17 |
| zone | 0.25 | 1801 | 19% | -0.58 | 0.25 | -0.544 | 0% | 0.18 |
| bos | 0.15 | 1009 | 77% | 0.55 | 5.13 | 0.563 | 100% | 3.66 |
| bos | 0.25 | 835 | 76% | 0.52 | 4.11 | 0.491 | 100% | 2.71 |

- Zone-entry (powered, up to 2200 trades): expectancy -0.61R@conf0.15, -0.58R@conf0.25 — **not positive** (the powered sample shows no edge).
- Direction skill (no stop/target, 15778 signals): signed mean +0.43% vs buy-and-hold +4.10%, win 52%, Sharpe +0.023 — **does NOT beat always-long**.

## Overall verdict — REBUILT engine (Phases 1-5), 1W + 1D

_(The auto-generated verdict below this block is templated and now stale; this
hand-written section is the accurate read of the rebuilt-engine re-test.)_

**What changed vs the pre-rebuild run** (`FORECAST_BACKTEST_prerebuild.md`): the
break-of-structure (BOS) model went from **31-48 trades (under-powered)** to
**460-1,009 trades** — the top-down counts produce far more, cleaner structures. And
the powered BOS rows are now POSITIVE: **74-77% win, +0.48 to +0.55 R, profit factor
4-5.6, CPCV out-of-sample PF 2.7-3.7, PSR-vs-B&H 100%.** The zone model stays
negative (-0.57 to -0.64 R).

**But this is NOT a demonstrated predictive edge — three honest reasons:**

1. **The mechanics-free DIRECTION test still fails.** Signing each forecast's
   horizon return by its predicted direction (no stops/targets/management):
   1W **-0.27%** (48% win) vs buy-and-hold **+5.28%**; 1D **+0.43%** (52% win) vs
   **+4.10%**. The forecast direction captures *less than passive long* — it has no
   directional skill. A strategy whose direction call is worse than "always long"
   cannot have a real predictive edge.

2. **The 75%-win / 0.5R / PF-5 profile is a trade-management signature, not skill.**
   With a near take-profit + move-to-breakeven and a wider structural stop, the
   probability of booking the close partial before the far stop is mechanically
   high (~barrier asymmetry) — a high win rate falls out *regardless of entry
   quality*. Expectancy, not win rate, is the test.

3. **The positive expectancy is most plausibly DRIFT capture.** On a secular-bull
   semis universe, "enter long on a confirmed up-break" rides the equity risk
   premium. The direction test (which is drift-aware, benchmarked to buy-and-hold)
   shows the forecast captures *less* of that drift than holding — so the BOS
   profit is the drift the management happens to harvest, minus the part the
   forecast's direction errors give back.

> **Verdict: the rebuild fixed the COUNTS, not the EDGE.** Correctly-applied
> EW/NeoWave now produces faithful impulse counts at the right degree (a real,
> verifiable improvement in analysis quality) — but trading the forecast still does
> not beat buy-and-hold: the direction call remains worse than passive long, and the
> powered positive expectancy is drift + barrier-asymmetry, not prediction. To claim
> otherwise we would need a control (random/flipped-direction BOS with identical
> management) to beat — and the direction test already implies it would not.
>
> This is the honest answer to the thread's question: applying the tools the
> professional way makes the ENGINE right; it does not, on this evidence, make the
> FORECAST tradeable.

---

_Auto-generated verdict (templated; superseded by the hand-written section above):_

- Trials this run: **8**; registry total: **65**.
- Highest Sharpe cell: 1d/bos/conf0.15 — 1009 trades, 0.55R, Sharpe 0.563.
- Direction skill: 1W 48% win, Sharpe -0.013; 1D 52% win, Sharpe +0.023 — neither beats always-long.
