# Phases 0–2 results — measurement fixed, edge not yet found

_Generated 2026-08-19 by `scripts/phase1_gate.py`. 26 instruments, daily, causal,
one position at a time. Pre-registered gates; results recorded as they came out.
Analysis tooling only — not investment advice._

## Phase 0 — instrument-agnostic measurement: **PASS**

The engine tuned pivot thresholds per instrument and per timeframe. Measured, one
config (`pct=0.05`) gave pivot densities per 1000 bars of 5.5 on EURUSD and 941 on
VIX — a **171x spread**. A 5x volatility shift inside one series moved density 12–44x.
"Degree" therefore meant something different on every instrument, and every
downstream label inherited it.

ATR-relative thresholds fix it:

| test | before | after |
|---|---|---|
| cross-instrument spread (18 symbols, 8 asset classes) | 171.2x | **1.3x** |
| 5x regime shift inside one series | 44x | **1.06x** |
| 100x price ramp, decile spread | 6.0x | **1.9x** |

Downstream, unprompted: AVGO daily confidence 55% → **69%** on the same structure,
and the weekly primary/alternate contradiction disappeared (was primary IMPULSE 29%
beside alternate ZIGZAG 56%; now 46% over 32%). GOLD and BTCUSDT now produce valid
Cycle/Primary impulse counts; EURUSD produces structure at all.

This phase is a real, verified win and it is done.

## Phases 1–2 — the trading layer: **FAIL (gate not met)**

Four arms over identical proposals and identical trade mechanics, so differences
are attributable to the gating alone.

| arm | n | expectancy | t | win% | PF |
|---|---|---|---|---|---|
| UNGATED — the signal every prior backtest measured | 2657 | **−0.746R** | −1.47 | 50.1% | 0.30 |
| GATED — CC-1 + confirmation break + TR-2 + confluence≥3 + R:R≥2 | 173 | **+0.003R** | +0.02 | 31.2% | 1.00 |
| FALSIFIED — GATED + CC-9 behaviour-over-structure | 112 | **−0.237R** | −2.11 | 30.4% | 0.61 |
| MOMENTUM — GATED with momentum-coupled direction | 74 | **+0.094R** | +0.33 | 32.4% | 1.15 |
| buy-and-hold, same span | 26 | +2145% total | | | |

### What this establishes

**Discipline is worth a great deal, and is not sufficient.** Wiring the gates that
already existed but were never enforced moved expectancy from −0.746R to break-even
— the largest single effect measured in this project. It confirms
`FORWARD_GHOST_TEST_FINDINGS` O7: the "no edge" verdict was measured on an ungated
signal. But the gated arm lands *at* zero, not above it.

**Direction is the binding constraint, as predicted.** Replacing the
opposite-the-last-leg reflex (`forecast.py:60`) with a momentum-coupled direction —
the `PRO_APPLICATION_SPEC` P1 gap, "the single biggest miss" — is the only change
that produced a positive expectancy (+0.094R, PF 1.15). Direction, not filtering,
is where the remaining signal lives.

**CC-9 as implemented is harmful.** Adding behaviour-over-structure falsification
made results *worse* (−0.237R, t=−2.11): it discards 35% of setups and the survivors
underperform the full set, so the structural filters (CC-4 time ratios, FR-7 caps)
are removing better trades than they keep. Either the thresholds are wrong for this
data or the rules bite on something other than trade quality. Recorded as a negative
result, not tuned away.

_A bug worth recording:_ the first CC-9 wiring discarded **99%** of setups. CC-3 and
CC-5 judge a *completed* post-pattern move; applying them at entry asks an
in-progress thrust to already exceed the correction it follows, which is incoherent.
`falsify_count` now separates the structural family (valid at entry) from the
behavioural family (needs a finished move).

### Why the gate still fails

n. The gates are selective enough that 26 instruments × ~2500 bars — roughly 65,000
bar-level decisions — yield only 74 momentum-arm trades. At that size a +0.094R
expectancy carries t=+0.33 and means nothing. Nothing here is statistically
significant, and no result in this table should be traded on.

**This is now a data problem, not a logic problem.** The chain
−0.746 → +0.003 → +0.094 is monotone and each step matches what the research
predicted, which is encouraging — and it is exactly the shape a promising-looking
overfit also has. Distinguishing them needs roughly an order of magnitude more
decisions: more instruments, more timeframes, walk-forward splits, and a
randomised-entry control (per `FORECAST_BACKTEST_2026-06`, the scale-out plus
breakeven management manufactures win rates regardless of entry quality).

## Honest status

There is **no working predictive system** here. What exists after this pass:

- a measurement layer that is genuinely instrument-agnostic and verified as such
- a disciplined signal that has stopped losing but does not yet win
- one identified lever (momentum-coupled direction) with the right sign and no power
- one identified dead end (CC-9 structural filtering as implemented)
- buy-and-hold still far ahead of every arm

## Next

1. **Power the momentum arm.** Extend to all timeframes and a wider universe until
   n ≥ 500, with walk-forward splits and the randomised-entry control. This decides
   whether +0.094R is signal or noise, and it is the only question worth asking next.
2. **Diagnose CC-9** — which of CC-4 / FR-7 is doing the damage, on what setups.
3. Leave the cycle seam (Phase 5) closed. The gate for it is still red.
