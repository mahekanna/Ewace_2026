# Roadmap — making the engine instrument-agnostic and genuinely predictive

_Written 2026-08-19 after reading the full research corpus (`docs/research/**`,
`RULESET.md`, `FORWARD_GHOST_TEST_FINDINGS.md`) and auditing `wavelib/` against it.
Supersedes nothing; it sequences the work the corpus already identifies but has not
done. Analysis tooling only — not investment advice._

---

## 0. Correcting the record

An earlier session in this thread concluded "the method has no predictive edge, it is
already proven." **That was an overreach and this document retracts it.**

What the existing backtests actually falsified is narrower and very specific. Per
`FORWARD_GHOST_TEST_FINDINGS.md`, the signal every negative test measured was:

```python
direction = "down" if last_up else "up"     # forecast.py:60
```

— the next move is mechanically the *opposite of the last completed leg*. That signal:

- never trades wave 3 or wave 5 (O2) — the classic Elliott edge is structurally absent;
- fires on structure *completion*, every bar, with **no confirmation trigger** (O7);
- is 84–92% "trend-resume after a correction", with the counter-trend branch **100%
  stale** (O3) — an untimed buy-the-dip reflex wearing wave labels;
- consults momentum for *labelling* but never for *direction* (O9);
- uses NeoWave only as a printed time annotation, never as a structural gate (O8).

So the honest statement is: **an ungated, completion-triggered, opposite-last-leg
reflex has no edge — tested thoroughly, across five timeframes, 19,784 direction
trades, 25 instruments and multiple asset classes.** That is a real and valuable
negative result. It is *not* a test of Elliott Wave or NeoWave as practised, because
the disciplined layer was never in the signal path.

## 1. What the audit found is still missing

`wavelib` was rebuilt in June (log measurement, EWO momentum gate, top-down degree,
extensions/clusters — all verified present in code). The rebuild fixed the **counts**.
It did not build the **predictive layer**. Grepping `wavelib/` for the mechanisms that
`practitioner/03_neowave_forecasting.md` identifies as the source of NeoWave's
predictive claim:

| Rule | What it does | In code? |
|---|---|---|
| CC-1 two-stage 2-4 completion | the only sanctioned "pattern is over" test | present, **not wired to any signal** |
| CC-3 "moves further and faster" | the *universal* confirmation rule | **absent** |
| CC-4 pre-constructive filter | wave-2 time ≥ wave-1 time, ≤ 3× | **absent** |
| CC-5 post-correction thrust | thrust ≥ correction, in ≤ its time | **absent** |
| CC-9 behaviour-over-structure | falsify the count when behaviour disagrees | **absent** |
| FR-3 minimum next-impulse size | keyed to prior correction's complexity | **absent** |
| FR-7 sub-wave time caps | C ≤ time(A)+time(B), E ≤ B+C+D, … | **absent** |
| FR-9 Rule of Reverse Logic | prefer the least-complete valid count | **absent** |
| TR-1 no trade before Stage 1 | the entry prohibition | **absent** |
| TR-2 two-consecutive-bar filter | entry confirmation | **absent** |
| `trade_plan()` (confirmation + confluence + R:R) | built June 12 | present, **never backtested** |

Neely's predictiveness claim rests on exactly three pillars — *logical entailment*,
*self-defining price/time limits*, and *self-confirming post-pattern behaviour*. The
third pillar is entirely unimplemented and the second is only half-built (S&B exists;
the hard caps do not). **The predictive layer has never been tested because it has
never been built.**

## 2. Why the tool is not yet instrument-agnostic

`zigzag_causal` supports volatility-scaled thresholds (`atr_n`), but **every caller
defaults to `atr_n=None` and passes a hardcoded percentage**, tuned per timeframe:

```
TFS = [("1W", (0.05, 0.10, 0.18, 0.30)), ("1D", (0.04, 0.08, …)), …]   # wave_report.py
piv = zigzag_causal(bars, pct=0.02)                                     # wave3.py
```

A fixed 2% swing is noise on a $2 stock and a Primary-degree move on a $400 one; it
means something different again on EURUSD, gold and BTC. This is audit root-cause **R5**,
still open in every real code path. Until thresholds are volatility-relative, "works on
any instrument" is not true — the *test universe* is already multi-asset (25 instruments
since Stage 10), but the *engine* is tuned per instrument class.

---

# The plan

Six phases. Each has an explicit **gate** with kill criteria, because the corpus's
central discipline is refusing to certify an underpowered or data-mined result. Phases
1–3 are the predictive work; 4–6 depend on them passing.

## Phase 0 — Instrument-agnostic measurement _(prerequisite, ~1 week)_

Make volatility-scaled pivots the default, not an option.

- Route every caller through ATR/log thresholds; remove hardcoded `pct=` and the
  per-timeframe scale tuples. Degree should follow from *relative* magnitude, not an
  absolute percentage.
- Repair the adaptive scale search (audit R5 notes the cap bug: the list tops out at
  0.30 and never converges on a 105×/25-year series).

**Gate.** On a synthetic 100× ramp, pivot count and assigned degree must be stable
across the whole range. The same config, unchanged, must produce degree-consistent
counts on a $2 equity, a $400 equity, EURUSD, gold and BTCUSDT. Fail ⇒ do not proceed;
everything downstream inherits the pivots.

## Phase 1 — Wire the discipline that already exists _(cheapest real test, ~1 week)_

This is `FORWARD_GHOST_TEST_FINDINGS.md` recommendation #1, still not done, and it is
mostly wiring rather than new logic.

- Point the forward test at `trade_plan()` instead of raw `forecast_waves` — confirmation
  break + `score_reversal` confluence + R:R, all of which exist.
- Enforce **TR-1**: no trade until CC-1 Stage 1 fires. Wire the existing
  `two_four_confirmation` / `confirm_completion` into the signal path as a hard gate.
- Add **TR-2**: entry only on the second consecutive close in the new direction.
- Drop the counter-trend branch that is 100% stale, or re-anchor it to current price.

**Gate.** Powered sample (n ≥ 300 decided trades). Compare three arms: ungated reflex
(the known-dead baseline), gated, and buy-and-hold. Gated must beat *both*. This phase
is cheap and decisive: if wiring the discipline moves nothing, the discipline is not
where the edge lives, and Phase 2 gets prioritised over Phase 3.

## Phase 2 — Build the missing NeoWave predictive core _(the real work, ~3–4 weeks)_

Implement the third pillar — self-confirming post-pattern behaviour — and the hard time
limits. Each rule TDD'd against synthetic ground truth first, per the repo's convention.

1. **CC-3 moves-further-and-faster** — the universal confirmation. Post-pattern move must
   exceed the prior pattern's largest counter-trend leg in price *and* form in less time.
2. **CC-4 pre-constructive filter** — wave 2 ≥ time(wave 1) and ≤ 3×; same for wave 4 vs 3.
   A shallow fast "wave 2" is *not finished*. This alone should remove a class of
   premature wave-3 entries.
3. **CC-5 / FR-3 post-correction thrust** — minimum next-impulse size keyed to the
   correction's type and complexity (single vs W-X-Y vs triangle).
4. **FR-7 sub-wave time caps** — C ≤ time(A)+time(B); E ≤ B+C+D; G ≤ D+E+F; x-wave ≤ W.
5. **CC-9 falsification engine** — when post-pattern behaviour fails any check, mark the
   count FAIL and re-label with the terminal pivot moved later. This is the error-correction
   mechanism that makes the system falsifiable rather than rationalising.
6. **FR-9 Rule of Reverse Logic** — among valid counts prefer the least-complete.

**Gate.** Measure the *falsification rate*: how often does the engine retract a count
before price invalidates it? A predictive system should retract early and often. If
CC-9 never fires, the rules are not binding and the layer is decorative.

## Phase 3 — Power the rule-faithful wave-3 / wave-5 entry _(~2 weeks)_

`wave3_signal_strict` already implements RULESET §H faithfully — NeoWave `:5` motive
label on wave 1, golden-zone wave 2, R1, ≥3 confluence strands, R:R ≥ 2. It is the most
promising artifact in the repo and it has **10 trades across 2 symbols**. That is not
evidence of anything.

- Extend to wave-5 entries and to shorts (currently long-only).
- Run across the full multi-asset universe × all timeframes for n in the hundreds.
- **Mandatory control arm:** identical management (scale-out, breakeven trail) with
  randomised or direction-flipped entries. `FORECAST_BACKTEST_2026-06.md` established
  that near-target-plus-breakeven manufactures a high win rate *regardless of entry
  quality* — the strict signal uses exactly that management, so without a control its
  74% win rate proves nothing.

**Gate.** Beat the control **and** buy-and-hold, survive CPCV out-of-sample, survive
Deflated Sharpe at the honest trial count (registry is at 68 and rising). Fail ⇒ the
rule-faithful entry is dead too, and that is a publishable, decisive result.

## Phase 4 — Calibration and honest output _(~1 week)_

- **Calibration curve**: when the engine says 55%, does the count hold 55% of the time
  out-of-sample? Currently unmeasured, and `forward_diag` already shows confidence is
  *uninformative* (flat 47–53% across buckets; the ≥70% bucket resolves zero usable
  trades). Either recalibrate or stop reporting a number that carries no information.
- **Stop presenting a single "primary"** when a ranked alternate scores higher — the
  weekly AVGO count currently shows `primary IMPULSE 29%` beside `alternate ZIGZAG 56%`,
  which is the display contradicting itself. Carry alternates with their flip levels and
  promote on invalidation (CC-9 / EWI G3).

## Phase 5 — Cycle seam _(gated: only if Phase 3 passes)_

Hurst/FLD timing into the 7th confluence strand. `deep/00_STATUS.md` already gates this
RED and the reasoning is correct: there is no validated standalone edge for a "when"
layer to enhance. Do not open this until Phase 3 clears.

## Phase 6 — Production hardening _(gated: only after a validated signal)_

Typed `BarSeries` (provider, session, adjustment, tz, asof — the session/anchor
inconsistencies hit in August), immutable content-addressed snapshots, look-ahead
prefix-stability test in CI (already written ad hoc and passing: 1,472 checks, zero
violations), packaged install, scheduled ingest with validation alerting.

Deliberately last. Hardening the pipeline around an unvalidated signal buys the ability
to be wrong on a schedule.

---

## Honest expectations

Two independent designs — time-series direction (19,784 trades) and dollar-neutral
cross-sectional (202 rebalances) — found no information in the **composite forecast**.
That composite is a reflex, so those results do not condemn the method; but they also
do not encourage. The prior that Phases 1–3 find a durable edge should be *modest*, and
the plan is built so each phase can kill the hypothesis cheaply and publicly rather
than accumulating unfalsifiable machinery.

What is genuinely unexplored is real: the entire third pillar of NeoWave, the wired
confirmation gate, and a powered test of the rule-faithful entry. Those deserve to be
tried before anyone concludes the method does not work.

The corpus's own ceiling still stands and should be restated: a single deterministic
high-confidence count over long history is not achievable — degree anchoring and
real-time label ambiguity are intrinsically discretionary. The realistic best outcome
is a *selective, confirmation-gated, falsifiable* signal that trades rarely and knows
when it is wrong. Not an oracle.
