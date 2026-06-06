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
