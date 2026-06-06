# 00 — Research Index & Consolidated Build Roadmap

**Ewace_2026 / `wavelib`** — Elliott Wave + NeoWave research, June 2026.

This folder is the deep-research layer produced before the next coding phase. Four
agents researched the methodology from authoritative sources (Frost & Prechter,
Glenn Neely *Mastering Elliott Wave*, the ForexTalker / LiteFinance NeoWave series,
Investopedia / SMC) and audited the current engine module-by-module. This index
sequences their findings into one dependency-ordered roadmap.

> **Update (build complete):** the research pass below has now been *implemented*.
> Phases 0–4 of the roadmap are built and tested (Phase 0 F1/F3/F4; F2 deferred).
> The engine now has causal pivots, a Degree hierarchy, corrected classifiers, the
> NeoWave bottom-up constructor + logic, hardened confirmation strands with the typed
> `CycleSignal` seam, and the automation layer (auto-label, auto-degree, causal
> backtest, SVG charting). **90 unit tests pass** (`python3 -m unittest discover -s
> tests`), plus all module self-tests and `examples/01..04`. The chakra_quant bridge
> remains a documented seam only.

---

## Reading order

| # | Doc | Workstream | Audits |
|---|-----|-----------|--------|
| 1 | [`01_elliott_wave.md`](01_elliott_wave.md) | Classic Elliott Wave — hard rules, guidelines, corrections, diagonals, degree hierarchy, Fibonacci | `rules.py` §B/C/D |
| 2 | [`02_neowave_neely.md`](02_neowave_neely.md) | NeoWave (Neely) — monowave→polywave construction, S&B, channeling, terminals, complex-correction zoo. **Canonical** home for terminals & NeoWave channeling (01 cross-links here). | `rules.py` §E/F + `toolkit.py` |
| 3 | [`03_confirmation_strands.md`](03_confirmation_strands.md) | Reversal-confirmation strands + the **cycle-seam spec** (chakra_quant bridge) | `confluence.py` |
| 4 | [`04_automation_validation.md`](04_automation_validation.md) | Auto-labeling, auto-degree, causal backtest harness, programmatic charting | whole package |

---

## Current state in one picture

The engine is a faithful **first pass at a single, hand-picked degree**. Its weaknesses
cluster in three places:

1. **No degree / no bottom-up construction.** There is no `Degree` concept and no
   monowave→polywave→multiwave builder, so degree is *assumed*, never *computed*. This
   blocks auto-labeling (01 §3, 02 §3).
2. **Classifier thresholds diverge from canon** — a flat dead-zone (B 0.618–0.90
   silently mislabeled), triangle progression checked on alternating legs only, leading
   vs ending diagonal not distinguished, loose Fibonacci bands (01 §3).
3. **Confirmation strands are crude** — `momentum_divergence` and `choch` are effectively
   stubs (rolling max / global-min, not confirmed swing pivots); `channel_break` is an
   EMA9 proxy, not a trendline (03 §3). And the **backtest is look-ahead-unsafe**: ZigZag
   pivots are dated at the price extreme, not at the bar the reversal was *confirmed*
   (04 §3).

Fidelity tally across the audited functions: a handful **Full**, many **Heuristic**,
several **Stub**, and the architectural pieces (degree, monowave constructor,
`label_and_validate`, `backtest_reversals`) **Missing**.

---

## Consolidated build roadmap (dependency-ordered)

Each item cites its source doc/task. Build top-to-bottom: later phases depend on earlier
ones. **Discipline that applies throughout:** TDD with synthetic ground-truth first
(`visual-first-validation`), and **causal-only** — every signal at bar *t* uses data
≤ *t*, no `center=True`, no `shift(-N)`, right-aligned windows. This anticipates the
eventual `chakra_quant` D-013 bridge (see Cycle Seam below).

### Phase 0 — Foundations (causal timing, de-dup, degree)
- **F1. `Pivot.confirmed_t` + `zigzag_causal`** *(04-Item1 — CRITICAL prerequisite).* ✅ **DONE.**
  Run ZigZag front-to-back, recording the bar where the reversal is *confirmed*, not the
  back-dated extreme. Without this every backtest silently uses look-ahead data.
  → `toolkit.py:zigzag_causal` (detection-parity with `zigzag`, adds `confirmed_t`;
  final extreme provisional). Tests in `tests/test_foundations.py`.
- **F2. De-duplicate shared utilities** *(04-§3).* ⏸ **DEFERRED** (deliberate refactor, not a
  safe re-export). `similarity_and_balance`, `project_wave5`, terminal-retrace window exist
  twice but the copies have **diverged APIs** (`SBResult` vs `RuleResult`; different dict
  keys), so de-dup means choosing one API and updating the demos/examples — its own task.
- **F3. `Degree` enum + optional `degree` field on `Wave`/`Pivot`** *(01-Task4 — architectural).* ✅ **DONE.**
  Nine levels (Grand Supercycle→Subminuette) with `.abbr`/`.finer()`/`.coarser()`,
  backward-compatible (`Optional[Degree] = None`). → `rules.py:Degree`.
- **F4. Swing-pivot helper** *(03-P1, roadmap called it `zigzag_pivots`).* ✅ **DONE** as
  `toolkit.py:swing_pivots(series, n_left, n_right)` — N-bar confirmed fractal pivots over
  any `(t, value)` series, consumed by the confirmation strands (Phase 3) and the monowave
  constructor (Phase 2).

### Phase 1 — Classifier correctness (single-degree fidelity)  ✅ DONE
- **C1. Fix the flat dead-zone** *(01-Task1).* `ZIGZAG_B_MAX = 0.618`, `FLAT_B_MIN = 0.618`;
  replace C-wave length-ratio with a directional **endpoint** check (does C surpass A's
  extreme?) to separate expanded vs running flats. Removes the 0.618–0.90 misclassification.
- **C2. Fix the triangle check** *(01-Task3).* Test the full `a>b>c>d>e` progression (not
  just a,c,e); detect a genuinely flat boundary for *barrier*; emit a REF for wave-E
  overshoot of the a-c line; add the post-triangle thrust projection (≥75% of widest leg).
- **C3. Split leading vs ending diagonal** *(01-Task2).* `leading_diagonal_rules` (5-3-5-3-5,
  overlap common) vs `ending_diagonal_rules` (3-3-3-3-3, overlap expected) — they imply
  opposite "what's next" signals.
- **C4. Firm up Fibonacci thresholds** *(01-Task5 + §3).* zigzag B = 0.618; extension
  preferred ≥1.618; wave-3 preferred 1.618–2.618 (outer = WARN); add `w5=1.618×w1` and
  `w5=0.382×w3` to `project_wave5`.
- **C5. Base 0-2 channel test** *(01-Task6 / 02 channeling).* The 0-2 line (and wave-2
  endpoint correction via a 0-2 break) is absent; only 2-4 and 1-3 exist.

### Phase 2 — NeoWave construction & logic (the deepest gap)  ✅ DONE
- **N1. `label_monowaves` — Neely's seven retracement rules** *(02-Task1 — KEYSTONE).*
  Breakpoints at 38.2 / 61.8 / 100 / 161.8 / 261.8 %, conditions a–d, rollback endpoint
  correction, and structure labels (`:5`/`:3`/`:F3`/`:L5`/…). Unlocks all bottom-up degree.
- **N2. `group_polywaves`** *(02-Task2).* Sliding 3/5 window over labeled monowaves,
  applying hard-rule + S&B checks to assemble polywave candidates.
- **N3. Two-stage impulse confirmation timing** *(02-Task4).* A 2-4 break must occur in
  *less* time than wave 5 took to form; full retrace ≤ wave-5 build time. Directly fixes
  the AVGO false-confirmation (2-4 line ~$301 still unbroken).
- **N4. S&B on all adjacent corrective pairs** *(02-Task3)* — not just wave2 vs wave4.
- **N5. Terminal fidelity** *(02-Task5 + terminal rows).* Enforce 3-3-3-3-3 sub-structure
  and the wave-2 ≤ 61.8% retrace limit; **reframe the retrace window as a directional
  bias, not a price/time forecast** (the cause of the AVGO over-projection).
- **N6. Complete the complex-correction zoo** *(02-Tasks 6–9).* Neutral triangle
  (C longest, A≈E, 161.8% C limit), diametric time-similarity across all 7 legs,
  9-leg symmetrical, and a computed `x_wave_check` (the 61.8% rule, currently a REF stub).

### Phase 3 — Confirmation strand hardening  ✅ DONE
- **S1. Rewrite `momentum_divergence`** *(03-P1).* Paired confirmed swing pivots (regular
  + hidden), ≥50-bar guard, ≥3 RSI-point amplitude filter.
- **S2. Rewrite `choch`** *(03-P2).* Track structural trend direction; require body-close
  confirmation on N-bar pivots; distinguish **BOS** from **CHoCH**.
- **S3. `CycleSignal` payload + new `score_reversal` signature** *(03-P3).* See Cycle Seam.
- **S4. Harden the rest** *(03-P4/5/6).* 20-bar volume window + range filter; a real
  two-pivot **trendline** channel break (not EMA9); a minimum-bar guard in `score_reversal`.

### Phase 4 — Automation & validation (the "start coding further" target)  ✅ DONE
- **A1. Multi-scale pivot streams** *(04-Item2).* ATR-adaptive ZigZag at several multipliers
  feeding the degree hierarchy.
- **A2. `label_and_validate(bars, degrees, …) -> list[CandidateCount]`** *(04-Item3 / 02-Task10).*
  Enumerate candidate counts → R1/R2/R3 combinatorial pruning → validate against the
  existing `validate_impulse`/`validate_correction` → rank by `(hard_fails, warns, -fib_score)`.
  Removes the hand-picking bottleneck (CLAUDE.md TODO #1).
- **A3. Auto-degree loop** *(04-Item4).* Neely bottom-up: monowave→polywave→multiwave
  compaction assigns degree instead of assuming it.
- **A4. `backtest_reversals(bars, …) -> BacktestStats`** *(04-Item5).* Causal bar-by-bar
  replay calling `label_and_validate` on `bars[0..t]`, recording `ReversalEvent`s at
  score ≥ threshold, walking forward for outcome; hit-rate, profit factor, walk-forward
  efficiency over rolling IS/OOS splits. Turns the research tool into a falsifiable system.
- **A5. `render_chart(waves, projections)`** *(04-Item6).* Programmatic SVG to replace the
  hand-built `charts/*.html`.

---

## Cycle seam — the chakra_quant bridge (documented only)

The 7th confirmation strand is the agreed boundary between this repo's **"where"** layer
and `chakra_quant`'s Hurst/FLD **"when"** layer. Per the user's direction, this pass
**documents the seam only — no wiring, no import.** The contract (full spec in
[`03_confirmation_strands.md` §3.5](03_confirmation_strands.md)):

- A typed `CycleSignal` lives **in this repo** (`wavelib/confluence.py` or a new
  `wavelib/cycle_seam.py`): fields `aligned`, `cycle_period`, `phase`, `source`
  (+ optional `fld_value`, `confirmation_bars`). `score_reversal` gains
  `cycle_signal: Optional[CycleSignal] = None` alongside the legacy `cycle_aligned` bool.
- **Neither library imports the other.** `chakra_quant` produces a `CycleSignal`-shaped
  object from outside and the caller passes it in; an adapter translates names if they drift.
- **Causal-only is non-negotiable.** If `aligned` is ever set with future data the backtest
  is invalid; `source` records the algorithm (e.g. `"goertzel_40bar"`) so causality is
  auditable. This mirrors `chakra_quant`'s D-013.

Building **S3** (the typed seam) is the last step needed before real integration; the
integration itself is explicitly out of scope until the EW/NeoWave engine above is validated.

---

## Honest caveats (carried from all four docs)

- **Degree is the central subjectivity.** The engine can validate *a* count's internal
  consistency; it cannot prove the chosen degree is correct. Auto-degree (A3) narrows but
  does not eliminate this.
- **Sub-wave structure is data-limited.** Some rules (diagonal 5-3-5-3-5 vs 3-3-3-3-3,
  zigzag's 5-3-5) need sub-wave data the Wave-level input doesn't carry — a genuine
  data-availability gap, not just missing code.
- **Guidelines are statistical tendencies, not physics** — keep them WARN, never let them
  invalidate.
- **NeoWave terminals are often irregular** (AVGO's was expanding/irregular); terminal
  timing is a bias, not a number.
- **Automation invites overfitting** — combinatorial label search inflates multiple-testing
  risk; the backtest (A4) and walk-forward splits exist precisely to keep the system honest.

---

*Generated from the four workstream docs in this folder. Start at Phase 0.*
