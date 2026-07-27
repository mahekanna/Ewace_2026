# Deep-research → implementation status

This folder (`05`–`08`) is the second, **methodology-first** research pass (the
first pass, `../01`–`04`, was scoped to auditing the original code). Below maps each
deep finding to what is now built in `wavelib`, what is deferred, and why.

| Deep doc | Recommendation | Status | Where |
|---|---|---|---|
| 07 auto-labeling | Single primary count + ranked alternates (not fragmented roots) | ✅ done | `wavetree.wave_counts`, `anchor_count` |
| 07 auto-labeling | Degree anchoring via Neely 13–55 monowave window | ✅ done | `wavetree.anchored_degree` |
| 07 auto-labeling | Gaussian-Fibonacci *calibrated* confidence | ⏳ partial | confidence is spread & honest (8–34%) via `_fib_close` tent kernel; Gaussian kernel deferred (re-calibration risk) |
| 06 diagonals/patterns | Diagonals in the tree (ending/leading, wedge, overlap) | ✅ done | `wavetree._diagonal_node` (degree≥2) |
| 06 diagonals/patterns | Impulse/diagonal/triangle disambiguation procedure | ✅ done | `rules.disambiguate_five` |
| 06 diagonals/patterns | Full Fib relationship tables, throw-over depth | ⏳ partial | core checks present; exhaustive tables deferred |
| 05 NeoWave full algo | Two-stage 2-4 timing confirmation | ✅ done (Phase 2) | `rules.two_four_confirmation` |
| 05 NeoWave full algo | Monowave **candidate** labels (carry >1, prune later) | ✅ done (additive) | `rules.monowave_candidates` |
| 05 NeoWave full algo | Rollback + full candidate-propagation into the constructor | ⛔ deferred | doc 05 §5 lists rollback thresholds as genuinely discretionary/unautomatable; full propagation is a large rework |
| 08 validation | PSR / MinTRL / Deflated Sharpe | ✅ done | `validation.py`; wired into `BacktestStats` |
| 08 validation | Trials registry (capture n_trials prospectively) | ✅ done | `validation.log_trial` / `registry/trials.jsonl` |
| 08 validation | CPCV falsification gate (purged/embargoed) | ✅ done | `validation.cpcv_splits`, `cpcv_profit_factor` |

## Stage 6 — EWF (elliottwave-forecast.com) integration (docs 09, 10)

A dedicated harvest of elliottwave-forecast.com (their server 403s automated
fetches, so search-sourced) produced docs `09`/`10`. Implemented:

| EWF idea | Status | Where |
|---|---|---|
| Blue Box (100–161.8% Fib-extension reaction zone) | ✅ done | `toolkit.blue_box_zone` |
| Swing-sequence count (3/7/11 corr, 5/9/13 motive) | ✅ done | `automation.swing_sequence` (in report) |
| Running triangle (wave-B beyond origin) | ✅ done | `rules.is_running_triangle` |
| ABC-vs-WXY discipline (5-3-5 vs 3-3-3) | ✅ done | `wavetree._correction_node` → `WXY` |
| Wave-label-aware RSI divergence | ✅ done | `confluence.divergence_at` |
| Members-only videos / seminar PDF / proprietary pivot algo | ⛔ inaccessible | 403 / paywall — noted in 09/10 |

Also completed (previously deferred): **Gaussian-Fibonacci calibration**
(`wavetree._fib_close` smooth kernel) and **CPCV wired into the per-symbol report**
(`backtest.reversal_returns` → `validation.cpcv_profit_factor`, with an honest
"needs ≥6 events" when under-powered).

## Stage 7 — realistic validation (doc 08)

| Item | Status | Where |
|---|---|---|
| Triple-barrier exits (+pt / -sl / time barrier) | ✅ done | `backtest._resolve_tb`, `reversal_returns(pt,sl,max_hold)` |
| Buy-and-hold benchmark Sharpe | ✅ done | `backtest.horizon_returns` |
| DSR report scored vs buy-and-hold, >=20-event headline | ✅ done | `scripts/run_dsr.py` → `reports/DSR_2026-06.md` |

**Result with realistic exits: no edge over buy-and-hold** (best 47-event variant
Sharpe 0.630 ≈ benchmark 0.633; DSR 1%). The apparent edge from the earlier toy
fixed-target model vanished — the harness now produces a trustworthy verdict and
correctly refuses to certify a data-mined result. Honest caveats remaining:
small/overlapping samples, single regime, no transaction costs.

## Stage 8 — next-wave forecasting + costs

| Item | Status | Where |
|---|---|---|
| Project the NEXT wave (direction, target zone, invalidation) | ✅ done | `forecast.forecast_waves` / `forecast_from_count` |
| Forecast shown on charts + in the report | ✅ done | `report_chart` card + target lines; `run_validation` line |
| Transaction costs in the backtest | ✅ done | `backtest._resolve_tb(cost=...)`; `run_dsr` uses 0.1% |

Forecasting is the first piece that *projects* rather than *labels*: from the recent
structure it states the expected next move with a bounded Fibonacci target zone and
invalidation, at honest (often 26-48%) confidence, and explicitly flags when a large
**unconfirmed** leg is in progress (so it doesn't over-claim). It is a probabilistic
zone, not a prediction.

## Stage 9 — NeoWave surfaced + universe expanded

| Item | Status | Where |
|---|---|---|
| Dedicated NeoWave-techniques research sweep (60 techniques, gaps) | ✅ done | `deep/11_neowave_techniques.md` |
| NeoWave shown in the analysis (it was implemented but invisible) | ✅ done | `report_chart._neowave_card` + report line |
| Watchlist 6 → **12** AI-semis (ARM/SMCI/QCOM/ASML/LRCX/AMAT) | ✅ done | `data/live/`, `run_validation` |

The NeoWave card surfaces monowave structure (:5/:3), Similarity & Balance, the
terminal/diagonal check, neutral/running-triangle flags, and the 2-4 timing
confirmation. Honest answer to "did we research NeoWave?": **yes, deeply** (docs
02 + 05) and it was implemented — the gap was *presentation*, now fixed.

### Stage 9b — doc 11's three remaining NeoWave gaps (now CLOSED)

| Gap (doc 11) | Status | Where |
|---|---|---|
| GAP-1 Rule-3-vs-4 overlap test + condition d in monowave labelling | ✅ done | `rules.monowave_candidates` (overlaps_m0 + m0r) now drives `rules.label_monowaves`' core label — fixes the old `retr>1 -> :5` motive over-labelling |
| GAP-2 trading-method synthesis panel (direction/entry/stop/invalidation/time-gated targets) | ✅ done | `forecast.TradePlan` / `forecast.trade_plan`; surfaced as the "Trading-method synthesis" report card |
| GAP-3 post-constructive confirmation as a stateful per-bar monitor | ✅ done | `rules.CompletionSignal` / `rules.confirm_completion` walks bars forward from wave-5 end, returns first-confirm bar or `pending`; surfaced in the NeoWave card when the count is an impulse |

GAP-1 makes labels Neely-correct: the 0.618-1.0 retrace band now splits into Rule 3
(no re-entry into m0 -> motive-or-first `:3/:5`) vs Rule 4 (re-entry -> c-wave
`:3/:c3`), so the constructor stops calling every deep extension a motive. GAP-2
turns a forecast into an honest, gated plan (low confidence = *wait*, the stop is
the structural invalidation, and confirmation is time-boxed to the prior leg's
build). GAP-3 is the real-time companion to the static `two_four_confirmation`: the
constructor proposes a complete impulse, the monitor waits for the market to
confirm it bar-by-bar with no look-ahead. All three are unit-tested (147 tests).

## Stage 10 — multi-regime validation (answers the daily report's main caveat)

The daily DSR report's biggest honesty caveat was *"single recent regime."* That is
now closed. `scripts/run_multiregime.py` pools the reversal strategy across **25
instruments** and multiple asset classes (12 semis, indices SPX/NDX/DJI/VIX,
defensive/energy sectors JPM/XOM/PG/JNJ/WMT/KO, EURUSD/GOLD, BTCUSDT/ETHUSDT) over
**weekly history 1987→2026** — so the sample now spans 2000, 2008, 2020 and 2022.

| metric | result |
|---|---|
| Pooled decided events (all variants) | **1,472** (vs a handful per symbol daily) |
| Buy-and-hold benchmark Sharpe (13-bar) | 0.228 (42,086 samples) |
| Best ≥30-event variant Sharpe | 0.164 (632 events) |
| Beats buy-and-hold | **No** (PSR vs benchmark **5%**) |
| CPCV 5th-pctile OOS profit factor | 0.59 – 1.07 (≈1.0 = no robust edge) |

**Verdict: no edge over buy-and-hold even across regimes.** This is the strongest
honesty result the project has produced: with a proper multi-decade, multi-asset
sample (1,472 events, not a handful) the reversal-confluence strategy still does not
beat passive holding. The harness refuses to certify a data-mined edge. (Report:
`reports/MULTIREGIME_2026-06.md`. Replay is bounded by a causal `label_lookback`
cap + `stride` for tractable runtime — both past-only.) This directly gates the
chakra_quant cycle integration: there is no validated standalone edge yet for the
"when" layer to enhance.

## Stage 11 — prediction-driven backtest (testing EW/NeoWave's *predictive* claim)

The multi-regime test (Stage 10) and all prior backtests traded a reversal SCORE
with fixed barriers — they never used the engine's wave FORECAST. `wavelib/
forecast_backtest.py` + `scripts/run_forecast_backtest.py` fix that: they trade
`forecast`/the count the institutional way — break-of-structure confirmation entry,
stop at the corrective-leg extreme (real structural risk), asymmetric R:R filter,
scale-out + move-to-breakeven, conviction filter, one position at a time, causal.

**A first run reported a fake edge (74% win / 14R / PF~50).** It was a bug, caught
because it was too good to be true: the stop had collapsed to a hard-coded 1%
(meaningless R, capped losses) and the same setup was re-entered every bar (fake
100% PSR). Both fixed (structural stop = leg depth; setup de-duplication). A second
(corrected) pass on a CONSERVATIVE break-of-structure entry looked *faintly*
positive — but on only ~147 trades, far too few to trust. So a second entry model
(EWF reaction-zone pullback) was added to get a properly-powered sample, run across
BOTH timeframes:

Powered verdict (weekly 1987→2026 + daily 2006→2026; `reports/FORECAST_BACKTEST_2026-06.md`):

| timeframe | entry | trades | win% | avg R | Sharpe | PSR vs B&H |
|---|---|---|---|---|---|---|
| 1W | zone (powered) | 2,049–3,338 | 16–19% | **−0.72 / −0.67** | −0.85 | 0% |
| 1W | bos (tiny) | 41–48 | 56–61% | +0.84 / +1.01 | 0.39–0.54 | 91–99% |
| 1D | zone (powered) | 3,108–3,919 | 20–22% | **−0.66 / −0.63** | −0.79 | 0% |
| 1D | bos (tiny) | 31–34 | 68% | +1.11 / +1.12 | 0.66 | 99% |

**Verdict: no durable edge.** The break-of-structure model looked positive only
because it was under-powered (31–48 trades); the moment the zone-entry model
produces a real sample (2,000–3,900 trades) on EITHER timeframe, expectancy is
clearly **negative** (−0.6 to −0.7 R, 16–22% win) — the forecast's predicted
reaction zones are *not* where price reliably turns. No configuration is both
powered and positive. Trading the prediction does not beat buy-and-hold on weekly
or daily. (Honest nuance: the zone stop is tight, which contributes to the low win
rate — results are entry/stop-model dependent, the EW discretion ceiling — but the
direction of the conclusion is unambiguous across the powered cells.)

**Decisive confirmation — the pure DIRECTION test** (`scripts/forecast_direction_test.py`,
no stop/target/management, just "enter next bar in the forecast direction, hold 13
weeks"): over **19,784** forecast-directed trades the signed mean is **−0.82%**
(Sharpe −0.04, **win rate 48.6%** — below a coin flip), versus buy-and-hold +5.28%.
This removes the entry/stop-model caveat entirely: the forecast direction itself
carries **no skill** — it is marginally *anti*-predictive. The negative backtest is
not an artifact of how trades were managed; the prediction has no directional edge
to begin with.

**Robustness across timeframes.** The forecast-driven test was then swept over
**five timeframes — 1W, 1D, 4H, 1H, 15M** (`reports/FORECAST_BACKTEST_2026-06.md`).
The zone-entry model is NEGATIVE on every one (−0.40 to −0.72 R, 626–3,919 trades
each); the per-timeframe direction test edges marginally above a coin flip on
intraday (52–53% win) but at noise-level Sharpe (~0.05) and never beats buy-and-hold
on any horizon (below 50% on weekly). The faint positive is confined to tiny
break-of-structure samples (5–48 trades). No tradeable edge at any horizon tested.

This confirms the cycle-integration gate is RED: across the reversal-score test
(Stage 10) and the prediction test on FIVE timeframes PLUS the mechanics-free
direction test, there is no standalone edge for the chakra_quant "when" layer to
enhance. The engine's honest role is *context* ("where a reversal is structurally
permitted"), not a standalone systematic predictor — exactly the ceiling the
research predicted.

## The honest ceiling

Both research passes converge on the same truth: a single, deterministic,
high-confidence Elliott/NeoWave count over long history is **not achievable** —
degree anchoring, rollback thresholds, and real-time label ambiguity are
intrinsically discretionary (doc 05 §5, doc 07 §5). The engine's job is therefore
to (a) commit to a **primary** count, (b) carry **ranked alternates**, (c) report
**calibrated confidence** that is low when the structure is genuinely ambiguous,
and (d) **refuse to claim edge** when the backtest is statistically underpowered.
All four behaviours are now in place; what remains (Gaussian calibration, full
candidate-propagation, exhaustive Fib tables) sharpens — but does not change — that
honest posture.

## Test coverage

147 unit tests (`python3 -m unittest discover -s tests`), synthetic-ground-truth
first. Validation math, CPCV, diagonals, anchored counts, the wave tree, the
monowave Rule-3-vs-4 overlap test, the trade-plan synthesizer, and the
post-constructive completion monitor all have deterministic tests.
