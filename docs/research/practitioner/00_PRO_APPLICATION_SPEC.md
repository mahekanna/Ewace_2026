# Professional application spec — how pros actually apply Elliott/NeoWave to forecast the next wave

_Synthesis of four practitioner-methodology research streams (2026-06-09). Child
docs hold the cited detail and full enumerated rule tables:_

- `01_ewi_professional_method.md` — EWI / Kennedy workflow (16 ID rules, 15 projection rules)
- `02_ewf_trading_method.md` — elliottwave-forecast.com Blue Box system (26 rules)
- `03_neowave_forecasting.md` — Neely's predictive/time method (9 CC + 11 FR + 8 TR rules)
- `04_trading_rules_risk.md` — cross-school entry/stop/target/risk (5 rule tables)

## The headline: four independent schools converge on five things our engine does NOT do

This is the core finding. EWI, EWF, NeoWave, and general practitioner doctrine were
researched separately, yet they **independently agree** on the same application
methods — and our engine implements **none** of them. Our engine does *pure
structural, bottom-up counting on linear price with retracement-only targets and no
gates*. That is not how any professional applies these tools.

| # | What every professional school does | What our engine does | The gap |
|---|---|---|---|
| **P1 MOMENTUM GATES WAVE IDENTITY** | EWI uses the Elliott Wave Oscillator (5-SMA−35-SMA): **highest reading = wave 3, zero-line pullback = wave 4, divergence = wave 5**. EWF uses the *same idea* via RSI: new extreme **without** divergence = wave 3 (continue), **with** divergence = wave 5 (fade). | Labels waves by price structure only; **no momentum gate at all** | The single biggest miss. Pros confirm "is this really wave 3?" with momentum; we never do, so sub-waves and B-waves get mislabelled |
| **P2 TOP-DOWN DEGREE ANCHORING** | Anchor the **highest** degree from the instrument's major historical turning points *first*, then drill down | Bottom-up from a fixed-% zigzag; degree **capped at Intermediate** (audit R4) | A 16-yr advance can't even be assigned Cycle/Primary degree |
| **P3 FORECAST TIME, NOT JUST PRICE** | NeoWave Similarity & Balance on **time**: next same-degree wave completes in **[N/3, 3N] bars**; self-defining sub-wave time limits | Forecasts price targets only | No "when," and no time-based falsification of a wrong count |
| **P4 PROJECT WITH EXTENSIONS + CONFLUENCE** | Next wave projected by Fibonacci **extensions** (W3 = 1.618/2.618×W1; EWF Blue Box = 100–161.8% extension of the first corrective leg) and **Fib clusters** (≥3 measurements overlapping = the target zone) + channel projection | Retracement-only targets; **no extension projection, no cluster detection** | We compute the wrong kind of target and never find confluence |
| **P5 TRADE ON CONFIRMATION + CONFLUENCE, CARRY ALTERNATES, FALSIFY** | Enter only on confirmation (EWF limit-touch of the Blue Box + RSI; NeoWave 2-4 break in < wave-5 time); every count carries a **structural invalidation** and a ranked **alternate** that is promoted on breach; **behaviour over structure** — price that fails to confirm *falsifies the label* | Emits trade plans with **no confluence check, no alternate, heuristic 1%-swing stop, no falsification** | We "predict" instead of "react"; a wrong count just silently persists |

Everything below operationalises these five.

---

## A. Counting workflow (replace bottom-up-only with the pro workflow)

1. **Log price always** for any instrument with >2× range (Neely; EWI treats it as
   non-negotiable). _(= audit R1.)_
2. **Top-down pass first:** find the highest-degree termini from all-history
   extremes; assign the macro degree; *then* subdivide. Bottom-up monowave
   construction is the *second* pass, constrained by the top-down frame. _(= audit R4.)_
3. **Volatility-scaled pivots** (ATR/log), not fixed-%, so a "swing" means the same
   thing at $2 and $400. _(= audit R5.)_
4. **Multi-timeframe alignment:** the operative count on TF must nest inside the
   one-higher-degree count on the higher TF.

## B. Wave-identification rules (add the MOMENTUM GATE — the key missing layer)

5. **Elliott Wave Oscillator** `EWO = SMA(close,5) − SMA(close,35)`. Gate:
   - Wave 3 candidate **must** carry the sequence's **highest |EWO|**; else it is
     not wave 3 (likely sub-wave iii or a B-wave). _(EWI I4 — "responsible for the
     majority of miscounted impulses.")_
   - Wave 4 candidate **should** see EWO return to/through the **zero line** (~94%
     of valid impulses); if not, it's a sub-wave (iv) of an extending 3. _(EWI I5.)_
   - Wave 5 **should** show **EWO/RSI divergence** vs wave 3. _(EWI / EWF.)_
6. **RSI-divergence mode switch** (EWF A8/C6): new price extreme **without**
   divergence ⇒ still wave 3 (don't fade); **with** divergence ⇒ wave 5 (fade,
   prepare next correction).
7. **Internal-structure check** before ABC vs WXY: zigzag (ABC) is valid only if
   leg A subdivides into **5**; if A is a 3, it's WXY/combination. _(EWI I9 — fixes
   the wrong target family.)_
8. **Re-balance impulse vs corrective scoring + alternation/channel gates** so a
   momentum-confirmed 5-wave impulse out-ranks a 3-wave parse. _(= audit R2.)_

## C. Next-wave projection rules (price + TIME + confluence)

9. **Extensions, by wave:** W3 = 1.618 / 2.618 × W1 (from W2 low); W5 = W1-equality
   or 0.382/0.618 × net(W1→W3) (from W4 low); C = A or 1.618 × A; triangle thrust.
   Retracements only for W2/W4/B (0.382–0.618 / 0.5–0.786). _(trading-rules C-1/C-2.)_
10. **Blue Box** zone = **100%–161.8% Fibonacci extension of the first corrective
    leg**, projected from the connector end; entry edge = the 100% "equal-legs"
    level. _(EWF A4.)_
11. **Fibonacci cluster** = collect all independent projections; a band where **≥3
    overlap** (±~2%) is the primary target. _(trading-rules D-8 — "the most cited
    institutional-EW edge, completely absent.")_
12. **Time projection** = Similarity & Balance on time: next same-degree wave in
    **[N/3, 3N] bars**; enforce sub-wave hard time caps (C ≤ time(A)+time(B);
    degree-N pattern ≤ time of degree N+1). _(NeoWave FR-6/FR-7/FR-11.)_
13. **Channel projection** (Kennedy's base→acceleration→deceleration channels) as a
    second, independent W5 target. _(EWI.)_

## D. Trading rules (react, don't predict)

14. **Entry by wave position:** buy **wave-2 pullback (0.5–0.618)** to ride wave 3;
    buy **wave-4 pullback** for wave 5; **fade end-of-5 / end-of-C** at the Fib
    cluster + momentum divergence. _(trading-rules Table A.)_
15. **Confirmation required:** EWF limit-touch of the Blue Box (+RSI); NeoWave
    **2-4 trendline break in less time than wave 5 took** (Stage 1), then a
    two-bar filter. **No trade before confirmation.** _(EWF / NeoWave CC-1.)_
16. **Count-derived structural stop** (not a 1% proxy): below W2 low for W3 entries;
    below W4 low for W5 entries; above the 5th's extreme for fades; **161.8%
    extension** for Blue-Box corrective entries (beyond it the move isn't corrective
    anymore). _(trading-rules B; EWF B3.)_
17. **Risk-free trigger:** at 50% of the connector wave, take partial + move stop to
    breakeven. _(EWF B4.)_

## E. Risk & count-management

18. **Confluence gate on every plan:** require `score_reversal ≥ N` (Fib cluster +
    channel + momentum + structure) before emitting a trade. _(trading-rules E-2.)_
19. **Carry a ranked alternate + its flip price;** promote the alternate the instant
    the preferred count's **structural invalidation** breaks. _(EWI G3; trading E-3.)_
20. **Behaviour over structure / Reverse Logic:** if price fails to confirm, the
    **label is falsified** — switch counts; and when several counts are valid prefer
    the **least-complete** one. _(NeoWave CC-9, FR-9.)_
21. **Fixed-fraction risk** sized off the structural stop; only take **asymmetric
    (≥2:1)** setups.

---

## How this maps onto the bug audit (the two studies converge)

| Practitioner requirement | Audit root cause it confirms | Engine change |
|---|---|---|
| Log price (A1) | R1 linear-price | log lengths everywhere |
| Top-down degree (A2) | R4 degree capped/partial | top-down anchor + unlock degree ladder |
| ATR pivots (A3) | R5 fixed-% zigzag | volatility-scaled zigzag |
| Momentum gate (B5/B6) | R2 impulse-loses + R6 label-collapse | **NEW: EWO/RSI gate on wave ID** |
| Extensions + clusters (C9–C11) | forecast = retracement-only | **NEW: extension + cluster projection** |
| Time projection (C12) | absent | **NEW: S&B time windows + caps** |
| Confluence gate + alternates + falsification (D15, E18–E20) | trade_plan emits ungated | **NEW: confirmation/confluence/alternate layer** |

The previous audit told us *what's broken in the code*; this spec tells us *how
professionals actually do it*. **They agree.** The rebuild therefore has two joined
halves: (1) fix the measurement/scoring/degree/coverage bugs (audit Phases 1–3), and
(2) add the professional application layer that was never there — **momentum-gated
wave ID, extension+cluster+time projection, and a confirmation/confluence/alternate
trading discipline**.

---

## Prioritised rebuild plan (audit + practitioner, merged)

- **Phase 1 — Measurement:** log lengths; ATR/log pivots. _(R1, R5 / A1, A3)_
- **Phase 2 — Identification:** EWO + RSI **momentum gate**; ABC-vs-WXY internal
  check; re-balanced impulse-vs-correction scoring. _(R2, R6 / B5–B8)_ — **this is
  the highest-leverage new work; it's how pros stop mislabelling wave 3.**
- **Phase 3 — Degree & coverage:** top-down anchoring; coverage floor; full degree
  ladder. _(R3, R4 / A2)_
- **Phase 4 — Projection:** Fibonacci **extensions** + **clusters** + **time
  windows** + channel targets. _(C9–C13)_
- **Phase 5 — Trading discipline:** confirmation gate, structural stops, confluence
  gate, ranked alternates + falsification, risk sizing. _(D, E)_

**Validation:** after Phase 2 the AVGO/MRVL weekly should finally read as a
**momentum-confirmed 5-wave impulse at Cycle/Primary degree**; after Phase 4 the
forecast should output an extension/cluster target zone **with a time window**;
after Phase 5 re-run the prediction backtest — only now is the trading test fair,
because only now is the engine applying the method the way professionals do.
