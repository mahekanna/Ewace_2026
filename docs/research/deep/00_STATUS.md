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
02 + 05) and it was implemented — the gap was *presentation*, now fixed. Doc 11's
remaining genuine gaps (next NeoWave work): Rule-3-vs-4 overlap + conditions a-d
in `monowave_candidates`; a trading-method synthesis panel (entry/stop/targets);
post-constructive confirmations as a stateful per-bar queue.

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

120 unit tests (`python3 -m unittest discover -s tests`), synthetic-ground-truth
first. Validation math, CPCV, diagonals, anchored counts, and the wave tree all
have deterministic tests.
