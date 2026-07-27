# Ghost forward-test findings — why the signal has no edge

_Compiled 2026-06-13 from the TEST (Alpaca-enabled) session. Data: live Alpaca 15m
bars (sip, split-adjusted) for AVGO & MRVL, ~376 trading days (2024‑12 → 2026‑06‑12).
Method: causal ghost-feeding (`scripts/forward_test.py`); per-type/confidence
breakdown by `scripts/forward_diag.py`. Analysis only — not advice._

> **TL;DR.** On a large, multi-regime, look-ahead-free sample the forecast has **no
> directional edge** (next-candle 50–51% everywhere; the engine's own confidence is
> uninformative; invalidations outnumber hits). The root cause is structural, and it
> matches the four points raised in review: the tested signal **does not trade waves 3
> or 5**, its **direction is a mechanical reflex** (opposite the last completed leg),
> the **NeoWave content is only a time annotation**, and **~90% of signals are
> "trend-resume after a correction" fired with no confirmation** — i.e. effectively
> independent of the Elliott/NeoWave structure they are named for.

---

## 1. Method (what was measured)
- **Ghost feeding / causal:** at each candle `t` the forecast is built from bars `≤ t`
  only (`forecast_waves`, rolling `ROLL=400`), then the next `RESOLVE=32` candles are
  fed in to classify the outcome. `FORWARD` was widened (optional 3rd CLI arg) so the
  walk covers the **whole year**, not just the last 260 candles.
- **Outcome classes:** `STALE` (target already on the wrong side of price → unusable),
  `HIT` (target reached first), `INVALIDATED` (invalidation reached first), `OPEN`
  (neither within 32 bars), plus next-candle direction.
- **Two feeds per symbol:** `15m` = U.S. regular session (RTH, canonical, matches the
  engine's tuning); `15m_eh` = raw incl. extended hours.

## 2. Headline results
**Year (~376 trading days):**

| run | candles | STALE | usable (HIT/INVAL) | TARGET-HIT | next-candle DIR |
|---|---|---|---|---|---|
| AVGO 15m RTH | 9,344 | 16% | 1367 (558/809) | 41% | **50%** of 8,244 |
| MRVL 15m RTH | 9,345 | 27% | 1718 (755/963) | 44% | **51%** of 9,240 |
| AVGO 15m_eh | 23,367 | 9% | 1147 (439/708) | 38% | **51%** of 10,653 |
| MRVL 15m_eh | 22,903 | 18% | 2041 (891/1150) | 44% | **51%** of 16,803 |

**30-day pilot (late-May→June reversal window), for contrast:** STALE 45–86%,
target-hit 0–26%, dir 45–50%. The high stale there was the fast reversal lagging the
confirmed pivot — a regime effect, not a data problem (it falls to 9–27% over the year).

## 3. How a signal is actually generated (`wavelib/forecast.py`)
`forecast_from_count()` takes the primary top-down count and projects the **next** wave:

| current (completed) structure | forecast | direction | targets | code |
|---|---|---|---|---|
| 5-wave **IMPULSE/DIAGONAL** | "corrective A-B-C" | **opposes** the impulse | 38.2–61.8% retrace | L69–80 |
| 3-wave **CORRECTION** (ZIGZAG/FLAT/WXY) | "new impulse" | **opposes** last corrective leg (= resume prior trend) | 1.0–2.618× extension | L81–99 |
| **TRIANGLE** | "post-triangle thrust" | structure direction | 0.75–1.25× widest leg | L100–111 |

The direction line is literally:
```python
direction = "down" if last_up else "up"     # forecast.py:60  — next move opposes the last leg
```
The forward test evaluates this **raw** forecast (`forward_test.py:160` → `forecast_waves`).
It does **not** call `trade_plan()` (`forecast.py:194–255`), which is where the
confirmation-break trigger, the `score_reversal` confluence gate, and the R:R live.

## 4. Observation catalog (every finding, with evidence)

**O1 — Direction is a structural reflex, not a prediction.** It is fixed as "opposite
the last completed leg" (`forecast.py:60`); momentum/price action at `t` does not enter
the choice. *Evidence:* next-candle accuracy is identical whether the forecast agrees or
disagrees with the recent 20-bar trend — AVGO with-trend **49%** / against-trend **51%**;
MRVL **51% / 51%**. The direction carries zero information.

**O2 — It never trades waves 3 or 5.** The signal fires on **completion** of a structure
and projects the *next* leg; there is no path that says "an impulse is starting, position
for wave 3" or "ride wave 5." The classic Elliott edge (enter the 3rd, hold into the 5th)
is structurally absent. *Evidence:* `forecast_from_count` branches only on the *completed*
`pattern`; the dominant output is "new impulse after a correction," not "wave-3 in progress."

**O3 — ~90% of signals are "trend-resume after a correction"; the counter-trend branch is
100% dead.** *Evidence (year RTH):*

| forecast type | AVGO | MRVL |
|---|---|---|
| new-impulse (trend-resume) | 7,560 (92%) | 7,743 (84%) |
| corrective A-B-C (counter-trend) | 684 → **100% STALE** (0 HIT/0 INVAL) | 1,497 → **100% STALE** |

Every counter-trend forecast is discarded as stale (after an impulse completes, price has
already retraced past the projected zone), so it contributes nothing. All usable trades
come from the one "resume the trend after a pullback" branch.

**O4 — The engine's own confidence is uninformative.** *Evidence:* next-candle accuracy by
confidence bucket is flat at 47–53% for both names; the **highest-confidence bucket (≥70%)
resolves ZERO usable trades** (AVGO n=403, MRVL n=572 — all stale/open). Target-hit does
not rise with confidence (AVGO 39/35/48%; MRVL 63/28/40%). The model cannot tell its good
calls from its bad ones.

**O5 — Negative skew: invalidations beat hits, and faster.** *Evidence:* HIT < INVAL in
every run (AVGO RTH 558 vs 809; MRVL 755 vs 963). Median bars-to-resolution: INVALIDATED
**15** vs HIT **17–19** — stops are tagged before targets. Consistent with the known R:R<1
(targets sit closer than the structural stop).

**O6 — Most "usable" forecasts never pay inside the horizon.** *Evidence:* OPEN dominates
the resolved-eligible set (AVGO new-impulse OPEN 5,377 of 7,560 ≈ 71%). The Fib-extension
targets (1.0–2.618×) are too far to reach in 32 bars; even correct directional calls don't
resolve in time.

**O7 — The disciplined signal was never tested.** `trade_plan()` adds exactly the missing
pieces — entry only on a **confirmation break** of the last pivot, a **confluence** gate
(`score_reversal`), R:R, and a Neely time gate — but `forward_test.py` bypasses it and
tests the ungated projection. So the headline numbers describe a signal fired **every 15
minutes with no trigger**.

**O8 — NeoWave is present only as a time annotation, not a forecasting method.** The sole
NeoWave element in the forecast is the Similarity-&-Balance **time window** `[N/3, 3N]`
(`forecast.py:123–127`); it is printed, not used to select direction or filter entries.
There is no Rule of Neutrality, no monowave→polywave position logic, no logic-pre-
construction driving the signal.

**O9 — Momentum gates labelling, not the forecast.** The EWO momentum check
(`wavetree.momentum_lookup`) influences how wave 3 is *labelled inside the count*, but
`forecast_from_count` never consults momentum when choosing direction (ties to O1).

**O10 — Stale% is regime-driven, not a feed/data defect.** Over the year STALE is 9–27%
vs 45–86% in the 30-day reversal window; RTH-vs-EH stale is inconsistent across symbols, so
session structure is second-order. The earlier "all-stale" scare was a fast reversal
out-running the confirmed pivot.

## 5. The four structural gaps (review points, validated)
1. **No wave-3 / wave-5 signals.** ✔ Confirmed (O2). The model forecasts the leg *after* a
   completed structure; it has no "impulse-in-progress → trade the 3rd/5th" trigger.
2. **No genuine wave prediction.** ✔ Confirmed (O1, O4). The "prediction" is a deterministic
   reflex (opposite-last-leg + Fib levels) with zero demonstrated skill — direction and
   confidence both decouple from outcome.
3. **No proper NeoWave.** ✔ Confirmed (O8). NeoWave is a printed time band, not a structural
   driver — none of Neely's construction/neutrality logic gates the signal.
4. **Trades fire after corrections, independent of Elliott/NeoWave.** ✔ Confirmed (O3, O1).
   84–92% of signals are "new impulse after a correction," fired with no confirmation, and
   whether they agree with structure/trend is irrelevant to the result (50/50). The signal
   behaves like an untimed "buy-the-dip" reflex that happens to be *named* with wave labels.

## 6. What it does today vs. what a real EW/NeoWave trade needs
| dimension | today | needed |
|---|---|---|
| trigger | fires every candle on structure *completion* | identify an *incomplete* count at a wave-2/4 low, trigger on the break that confirms 3/5 started |
| direction | opposite last leg (reflex) | the impulse direction, momentum-confirmed (EWO) |
| which wave | the leg after completion (mostly corrections/early impulse) | the 3rd (and the 5th), the high-probability legs |
| gate | none (raw projection) | confirmation break + confluence ≥ N strands + R:R ≥ 1 (`trade_plan` exists, unused) |
| NeoWave | a printed time window | construction + neutrality + S&B used to *place* the wave and gate entries |
| target/horizon | far Fib extensions, 32-bar window | structure-based targets reachable in the test horizon |

## 7. Recommended experiments (priority order)
1. **Test the gated signal.** Point a forward test at `trade_plan()` (confirmation break +
   confluence + R:R) instead of raw `forecast_waves`, and re-run the year. Highest-value:
   it measures the discipline that was built but never evaluated.
2. **Make it a wave-3 entry.** Detect an incomplete impulse at a wave-2 low and trigger on
   the wave-1-high break (confirmation the 3rd has begun); add the wave-5 projection. Drop
   or de-weight the 100%-stale counter-trend branch.
3. **Re-couple direction to momentum** (EWO) and bring targets to a horizon-reachable
   distance (or lengthen `RESOLVE`) so R:R and the test window agree.
4. **Deepen NeoWave** from a time annotation to a construction/neutrality gate before
   re-testing.

## 8. Reproduce
```bash
python3 scripts/forward_test.py avgo 15m 100000     # year-long ghost test (RTH)
python3 scripts/forward_test.py mrvl 15m 100000
python3 scripts/forward_diag.py                     # the by-type / by-confidence tables above
```
Data: `data/live/{avgo,mrvl}_15m_2026-06.json` (RTH) and `_15m_eh_` (extended hours);
reports in `reports/FORWARD_TEST_*.md`; provenance in
`reports/FORWARD_TEST_ALPACA_NOTES_2026-06.md`.

## 9. Bottom line
The rebuild made the **counts** correct, but the **tradeable signal** is a mechanical,
untimed trend-resume reflex that is decoupled from the wave structure it is named for —
so a large, honest forward test shows it at coin-flip. The fix is not more data; it is to
make the *signal itself* trade the 3rd/5th wave on confirmation (route through `trade_plan`),
and to give NeoWave a structural role beyond the time window.
