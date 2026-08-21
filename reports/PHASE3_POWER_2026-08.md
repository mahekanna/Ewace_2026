# Phase 3 — powered test of the direction call: **FAIL**

_Generated 2026-08-21 by `scripts/phase3_power.py`. 27 symbols x 5 timeframes,
causal, paired permutation test. Pre-registered gate. Not investment advice._

## The test design, and why it changed

The daily-only run produced 74 trades and a tempting +0.094R. It was rightly
objected that Elliott Wave is not an indicator that fires constantly — measured,
the gated signal takes **0.36 trades per instrument-year**, about one Primary-degree
setup every three years per symbol. Demanding n>=300 from 26 daily series was a
badly designed test, not evidence against the method.

So the design changed in two ways, neither of which loosens a gate:

1. **Breadth, not frequency.** Pool every (symbol, timeframe). In a fractal method a
   Minor-degree wave 3 on 4H is a legitimate instance of the same rules as a
   Primary-degree one on the weekly. This lifted the sample from 74 to **418**.

2. **A paired permutation test** instead of a t-test against zero. Every setup the
   signal takes gets a control twin: same entry bar, same |risk|, same R:R geometry,
   direction flipped. This isolates the only thing in question — does the DIRECTION
   call carry skill — and controls for the artifact `FORECAST_BACKTEST_2026-06`
   identified, that scale-out plus breakeven manufactures win rates regardless of
   entry quality. At low n a paired design is also far more powerful than testing a
   mean against zero.

## Result — n = 418

| | mean R | win% |
|---|---|---|
| signal | **−0.0550R** | 34.9% |
| direction-flipped control | **+0.1368R** | 44.5% |
| paired difference | **−0.1918R** | |

Setups by timeframe: 1W 30 · 1D 76 · 4H 95 · 1H 110 · 15M 107.

**Permutation test, 2000 draws: p = 0.9345.** Pre-registered gate (p < 0.05):
**FAIL.**

## What this establishes

**The signal is beaten by its own mirror.** 93% of random direction assignments over
the identical setups scored better than the actual direction call. This is the
properly-powered version of the test, on the design the method's selectivity
demands, and it is unambiguous: the direction call carries no skill.

**The +0.094R on n=74 was noise.** Exactly as flagged when it was reported. A
four-fold larger sample moved it from +0.094R to −0.055R and reversed the sign. This
is the clearest illustration in the project of why the underpowered result was not
allowed to stand as a finding.

**Momentum coupling did not rescue it.** The direction tested here is the
momentum-gated one (`PRO_APPLICATION_SPEC` P1), not the opposite-last-leg reflex. So
the failure is not merely "the reflex is bad" — replacing the reflex with the
professional momentum rule still yields no directional skill.

**Do not read the control as an inverse edge.** The flipped arm's +0.137R most
plausibly reflects long-drift capture on a secular-bull universe rather than genuine
inverse skill — the same confound the cross-sectional test was built to strip out.
The paired comparison stands regardless of that interpretation: the signal does not
beat its own mirror.

## Standing state of the project

| phase | result |
|---|---|
| 0 — instrument-agnostic measurement | **PASS**, verified (171x → 1.3x cross-instrument; regime 44x → 1.06x) |
| 1 — wire the existing discipline | large effect (−0.746R → +0.003R) but lands at zero |
| 2 — CC-9 falsification | **negative** — filtering made results worse (−0.237R) |
| 3 — powered direction test | **FAIL**, p = 0.93 at n = 418 |

## What is and is not falsified

Falsified, at proper power: **this engine's directional call — reflex and
momentum-coupled alike — does not predict.** Three independent designs now agree
(time-series direction over 19,784 trades; dollar-neutral cross-sectional over 202
rebalances; paired permutation over 418 setups).

Not falsified: the measurement layer (Phase 0 is a real, independent improvement);
Elliott/NeoWave as a *descriptive* framework for where a reversal is structurally
permitted; and direction rules materially different from the two tested here.

The corpus's own ceiling, written before any of this, still reads correctly: the
engine's honest role is **context**, not standalone prediction. Phases 1–3 tested
that ceiling properly rather than assuming it, and did not break through it.

## Recommendation

Stop trying to make the direction call predictive by adding layers to it. Three
properly-powered designs have now failed, the last one decisively. Any further work
on prediction should start from a materially different information source — the
cycle/timing seam is the only orthogonal one in the roadmap — and should not begin
until someone is willing to accept the same falsification standard used here.

The defensible product today is the analysis tool: an instrument-agnostic engine
that produces degree-appropriate counts with honest, ambiguity-aware confidence.
