# 04 — Practitioner Trading Rules & Risk Framework for Elliott / NeoWave

**Ewace_2026 / `wavelib`** — research layer, June 2026.  
**Scope:** how professionals convert a wave count into an actual trade — entries,
stops, targets, risk management, confirmation filters, and alternate-count discipline.
This document is **methodology and rules only**; it is not advice. All Fibonacci
levels and rules are cross-checked against Frost & Prechter *Elliott Wave Principle*
(New Classics Library, 9th ed.); Glenn Neely *Mastering Elliott Wave* (Windsor Books,
1990); ElliottWaveTrader.net practitioner material; EWI (elliottwave.com) channeling
guides; and multiple public EW trading education sources cited inline.

---

## Methodology

**Primary references:**

- Frost & Prechter, *Elliott Wave Principle: Key to Market Behavior* (1978, rev. 2005).
  Foundation of all hard rules, channeling, Fibonacci guideline tables.
  [EWI book page](https://www.elliottwave.com/books/elliott-wave-principle/)
- Glenn Neely, *Mastering Elliott Wave* (1990). NeoWave time-gate confirmation;
  2-4 trendline break timing rule; monowave retracement rules.
  [neowave.com](https://www.neowave.com/)
- ElliottWaveTrader (Avi Gilbert / Garrett Patten). Fibonacci cluster method —
  three or more independent Fibonacci projections overlapping in a tight band.
  [fibstrategy](https://www.elliottwavetrader.net/fibonacci-markets-and-stocks/strategy)
- EWI Channeling guide. 0-2 base channel; 2-4 trendline; wave-5 upper-channel
  projection.
  [elliottwave.com channeling](https://www.elliottwave.com/waveopedia/channeling/)
  [elliottwave.com channel article](https://www.elliottwave.com/articles/how-to-use-elliott-wave-channels-in-your-analysis/)
- ElliottWave Forecast (EWF). Fibonacci retracement tables per wave, confluence
  zones, multi-timeframe application.
  [ewf theory](https://elliottwave-forecast.com/elliott-wave-theory/)
- BullWaves / LiteFinance NeoWave series. Detailed correction rules, flat/zigzag
  classification, triangle entry/stop rules.
  [bullwaves corrections](https://bullwaves.org/complete-guide-elliott-wave-correction-patterns/)
  [litefinance neowave trading](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- StockCharts ChartSchool — EW guidelines applied, wave 2/4 retracement tables,
  channeling.
  [chartschool](https://chartschool.stockcharts.com/table-of-contents/market-analysis/elliott-wave-analysis-articles/guidelines-for-applying-elliott-wave-theory)
- FXOpen Fibonacci ratio reference.
  [fxopen fibonacci](https://fxopen.com/blog/en/fibonacci-ratios-to-use-with-the-elliott-theory/)
- SeeTheWaves RSI + EW.
  [seethewaves rsi](https://seethewaves.com/relative-strength-index-rsi-and-elliott-wave/)
- InnerCircleTrader (ICT). BOS/CHoCH framing mapped onto EW wave positions.
  [ict ew](https://innercircletrader.net/tutorials/elliot-wave-theory/)
- OpoFinance blog — RSI divergence confirmation rules.
  [opofinance rsi](https://blog.opofinance.com/en/elliott-wave-and-rsi/)
- ForexTrainingGroup — Fibonacci cluster construction.
  [fibclusters](https://forextraininggroup.com/using-fibonacci-clusters-to-increase-your-trading-odds/)
- NepseTrading — combining Fibonacci projections with EW.
  [nepsetrading](https://nepsetrading.com/blog/combining-fibonacci-with-elliott-waves-for-perfect-projections)
- Stocata Elliott Wave channel & price targets.
  [stocata](https://stocata.org/ta_en/elliott7.html)
- AlgoTrading Investment — channeling technique.
  [algotrading channeling](https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/)

**Approach:** Five parallel searches were run across hard-rule sources, Fibonacci
ratio tables, stop/invalidation doctrine, RSI/momentum confirmation integration,
and multi-timeframe / alternate-count risk management. Rules were triangulated
across at least two independent sources before inclusion. The tables below enumerate
every implementable rule; a final section maps each to what our engine currently
does or doesn't compute.

---

## Canonical Fibonacci Ratios Quick Reference

*(Source: Frost & Prechter; EWF; FXOpen; NepseTrading)*

| Wave | Type | Canonical ratio / depth | Notes |
|------|------|------------------------|-------|
| Wave 2 retrace | Retracement of W1 | 50 %, 61.8 %, 76.4 % | Typical. Deep = zigzag. 38.2 % shallow. Never ≥ 100 % |
| Wave 3 extension | Projection of W1 | 1.618 × W1 common; 2.618 × W1 extended; 4.236 extreme | W3 must not be shortest impulse |
| Wave 4 retrace | Retracement of W3 | 23.6 %, 38.2 % | Shallow by alternation; 50 % only in triangles; no W1 overlap |
| Wave 5 target | vs W1 or vs W1-W3 | Equal to W1 in price; or 61.8 % of net(W1→W3); or 0.382 × net(W1→W3) when W3 extended | Channel projection (2-4 line upper parallel) often best method |
| Wave B (zigzag) | Retrace of A | 38.2 %–61.8 % | B > 61.8 % of A → suspect flat |
| Wave B (flat) | Retrace of A | 61.8 %–100 %; expanded flat B ≈ 105–138 % of A | B > 100 % → expanded flat |
| Wave C (zigzag) | Extension of A | 100 % of A; 161.8 % of A extended | Always 5-wave internally |
| Wave C (flat) | Extension of A | 100 %–161.8 % of A | Check for new extreme |
| Triangle thrust | Post-triangle | 75 %–125 % of widest leg (leg A) | Swift, last leg before correction |

---

## Table A — Entry Rules by Wave Position

Each row: the wave being traded, the setup condition, and the exact trigger.

| # | Wave position | Setup condition | Entry trigger | Source(s) |
|---|---------------|-----------------|---------------|-----------|
| A-1 | End of W2 / start of W3 | W2 retraces 38.2–61.8 % of W1 and holds above W1 start | Break + close above W1 high; or limit buy in the 50–61.8 % Fib zone with momentum reversal candle | Frost & Prechter; EWF; EWI |
| A-2 | W3 continuation | W3 is underway (broke W1 high); a sub-wave-(ii) pulls back | Enter on break above sub-(i) high within the developing W3; stop below sub-(ii) low | EWF; ICT BOS framing |
| A-3 | End of W4 / start of W5 | W4 retraces 23.6–38.2 % of W3; does not overlap W1 high | Break + close above W3 high (after W4 is confirmed complete) | Frost & Prechter; StockCharts ChartSchool |
| A-4 | W5 fade (reversal short at top) | W5 approaches 1.0–1.618 × W1 or upper channel line; RSI bearish divergence; W5 volume < W3 volume | Break below W4 low (confirms W5 complete); ending diagonal: break below its lower boundary | EWF; Seethewaves RSI; StockCharts |
| A-5 | Wave C of ABC correction (long) | In a larger impulse uptrend; C reaches = A or 1.618 × A; momentum divergence on C swing | Momentum reversal confirmation (engulfing / RSI divergence + close above prior minor high) | Frost & Prechter; EWI; BullWaves |
| A-6 | Wave A of new correction (short) | Impulse complete (W5 confirmed); price breaks W4 low with body close | Limit/market short on break of W4 low; or on first bounce failure (bearish reversal candle at former W4) | EWF |
| A-7 | Post-triangle breakout (W4 triangle) | Triangle ABCDE complete; E within A-C channel; W5 thrust imminent | Break above wave D extreme; stop just beyond E extreme; target = 75–125 % of widest triangle leg from E | EWI triangles; BullWaves; Frost & Prechter |
| A-8 | Ending diagonal fade | 5th wave ends in an ending diagonal (3-3-3-3-3 overlapping); RSI divergence; volume contracting | Break below the lower diagonal boundary; stop above the 5th-wave extreme; target prior W4 zone or 61.8 % retrace of entire diagonal | StockCharts; EWF; StockPathShala ending-diagonal |
| A-9 | NeoWave 2-4 confirmation entry | After a suspected 5-wave move: 2-4 trendline is broken in less time than wave-5 took to form; entire wave-5 range retraced in less time than wave-5 build time | Enter in the direction of the *previous* impulse once both time conditions are confirmed; stop at wave-5 extreme | Neely *MEW*; LiteFinance NeoWave |

---

## Table B — Stop / Invalidation Rules

A structural stop = the price that voids the wave count. The stop is placed there (or 0.1–0.3 % beyond to avoid wick-stops), not at an arbitrary percentage.

| # | Trade | Structural invalidation (count void) | Stop placement | Notes |
|---|-------|--------------------------------------|----------------|-------|
| B-1 | Long W3 entry (end of W2) | Any close below W2 low (= start of W1) | 0.1–0.2 % below W2 low | A new low below W1 origin invalidates the entire impulse; exit immediately |
| B-2 | Long W3 continuation (sub-wave entry) | Sub-wave (ii) low exceeded | 0.1 % below sub-(ii) low | Tighter stop; count is still valid at the higher degree |
| B-3 | Long W5 entry (end of W4) | W4 overlaps W1 high (closes below W1 top in a non-diagonal) | 0.1 % below W4 low (= W1 top is the hard rule; stop just below W4 low is tighter and valid) | If W4 enters W1 territory the 5-wave structure is invalid (not a diagonal) |
| B-4 | Short W5 fade / reversal | Price closes and holds above W5 extreme | 0.1–0.2 % above the wave-5 extreme (the highest print of the impulse) | "Truncated W5" is rare but possible; stop must be beyond the absolute high |
| B-5 | Short wave A of ABC | Price surpasses the impulse origin (W1 start) to the upside | Above the origin of the preceding impulse | A move above the impulse start voids the corrective thesis |
| B-6 | Long wave C of ABC (corrective end) | Wave C closes below wave A start (voids flat/zigzag — price has extended beyond the expected correction range) | Below wave A start for a flat; below the ENTIRE correction start for any pattern | A new extreme beyond A start flags a larger-degree correction, not a simple ABC |
| B-7 | Post-triangle thrust long | Price re-enters and closes below wave E extreme (the triangle lower boundary) | Below wave E extreme | Post-thrust failure back inside the triangle voids the thrust reading |
| B-8 | Ending diagonal fade short | Price closes above the 5th-wave (diagonal) extreme | 0.1 % above the highest print of the diagonal | Even a throw-over (brief wick beyond the channel) can occur; require a *close* above to stop out |
| B-9 | NeoWave 2-4 confirmation | Wave-5 extreme (long direction: the starting low; short: the starting high) is exceeded before time conditions are met | At the wave-5 extreme; no entry if time gates not met | Never trade the label; wait for the NeoWave time confirmation; if time expires without confirmation, abort |
| B-10 | General alternation stop | W4 overlaps W1 in a presumed normal impulse | Reclassify as diagonal (if overlapping); otherwise treat all prior entries as stopped out | Diagonal entries have their own tighter invalidation |

---

## Table C — Target / Projection Rules

Partial exits lock in profit as each target is touched; the stop trails to breakeven after T1.

| # | Wave being targeted | Primary target (T1) | Extended target (T2) | Stretch target (T3) | Partial exit protocol |
|---|--------------------|--------------------|---------------------|--------------------|-----------------------|
| C-1 | Wave 3 | 1.618 × W1 measured from W2 low | 2.618 × W1 from W2 low | 4.236 × W1 (only in very extended W3) | Take 30–50 % off at T1; trail stop to breakeven after T1 hit |
| C-2 | Wave 5 (after W4 low entry) | Equal to W1 in price length | 61.8 % of net(W1→W3) added from W4 low | Upper 2-4 trendline parallel | Take 50 % off at T1; trail stop below each completed sub-wave |
| C-3 | Wave 5 via channel | Upper parallel of 2-4 trendline (draw line through W2 end / W4 end; parallel through W3 top) | If W3 steep: use W1 top as anchor for the parallel instead | — | Exit all remaining position on close back inside the channel (throwover complete) |
| C-4 | Wave C of flat/zigzag (long) | 100 % of wave A (equality) | 161.8 % of wave A | — | 50 % at 100 % A; 50 % at 161.8 % A |
| C-5 | Post-ABC reversal (new impulse long) | 23.6 %–38.2 % retrace of the A-B-C correction (first sub-wave of the new impulse) | 61.8 % retrace of the correction | 100 % retrace (back to the impulse's former peak) | Trail stop below each corrective pullback within the new impulse |
| C-6 | Post-triangle thrust | 75 % of widest triangle leg from E | 100 % of widest leg | 125 % of widest leg | Full exit at 100 % unless momentum is strong; beyond 125 % count as W5 extension |
| C-7 | W5 fade (short after impulse top) | Prior W4 zone (first target for corrective wave A) | 38.2 % retracement of entire W1–W5 impulse | 61.8 % retracement of entire impulse | Take 50 % at prior W4; hold rest for 61.8 % retrace if BOS structure confirms |
| C-8 | Fibonacci cluster zone | When ≥ 3 independent Fibonacci measurements (e.g. 0.618 × W1-W5 retrace, 1.0 × W-A, 1.618 × prior sub-wave) fall within 1–2 % of each other | The band itself is the target; enter at the near edge, exit at the far edge | — | The tighter the cluster, the higher the expected reaction; only trade 3+ level clusters |

---

## Table D — Confluence & Confirmation Rules

No structural label alone justifies a trade. Each rule here is an independent filter; more green lights = higher probability.

| # | Confirmation type | Green-light condition | Amber / caution | Red / abort |
|---|------------------|-----------------------|-----------------|-------------|
| D-1 | Fibonacci zone | Price is within the 38.2–61.8 % "golden zone" of the prior wave | Price is at a minor Fib (23.6 % or 76.4 %) only | Price is outside all expected Fib zones |
| D-2 | RSI divergence (regular bearish) | Higher price + lower RSI peak → confirms W5 or C completion for a fade entry | Divergence only on sub-daily timeframe, not the trade TF | No divergence at all at a suspected terminal wave |
| D-3 | RSI divergence (regular bullish) | Lower price + higher RSI trough → confirms W2 or W4 completion for a trend entry | Divergence moderate, RSI not yet turning up | RSI confirming the trend (no divergence) at a supposed reversal |
| D-4 | RSI trend-signal (motive wave) | RSI > 60 in an upward W3 (confirms impulse momentum) | RSI 50–60 (sluggish, may be corrective disguised as impulse) | RSI < 50 in a supposed W3 up — abort the impulse thesis |
| D-5 | Volume confirmation | W3 volume > W1 volume; W5 volume < W3 volume; volume spike on W-A of a correction | W5 volume ≈ W3 (ambiguous extension or failure) | W3 volume < W1 — impulse validity weak |
| D-6 | CHoCH (Change of Character) | A minor swing break *opposing* the dominant trend, body-close confirmed, on a confirmed N-bar swing pivot | BOS only (continuation swing-high/low break in trend direction) — not a reversal signal | Price makes a new extreme in the trend direction without CHoCH — the presumed terminal wave is not yet complete |
| D-7 | BOS (Break of Structure) | BOS in the direction of the trade (confirms wave-3 continuation or wave-C continuation) | BOS on a micro/noise swing, not a confirmed pivot | BOS opposing the trade direction — recount required |
| D-8 | Fibonacci cluster (price) | ≥ 3 independent Fibonacci measurements overlap within 1–2 % | 2 Fibonacci levels overlapping | Only 1 Fibonacci level — no cluster |
| D-9 | Fibonacci cluster (time) | Time ratio of the current wave to a prior wave = 0.618, 1.0, or 1.618 | Time ratio near but not at a canonical Fib | No time relationship |
| D-10 | Channel confirmation | Price is at / near a parallel trend channel boundary (0-2 base channel bottom for W2/W4 entries; 2-4 upper parallel for W5 targets) | Channel line is approximate (only 2 touches) | Price has pierced the channel deeply, not just touched |
| D-11 | NeoWave time gate | 2-4 trendline broken in < time(W5); full W5 range retraced in < time(W5) | Time close but slightly over | Time conditions exceeded — do not enter; wait for next setup |
| D-12 | Momentum candle / candlestick | Engulfing, hammer, pin bar, or outside bar at the confluence zone | Small-body candle only — ambiguous | No momentum candle at entry zone |
| D-13 | Multi-TF alignment | Same wave structure confirmed on 1 TF higher and the trade TF | Only visible on the trade TF | Higher-TF count contradicts the trade |
| D-14 | MACD histogram flip | Histogram crosses from negative to positive (bullish) or positive to negative (bearish) at the wave reversal zone | MACD line cross without histogram flip | MACD diverging further (deepening histograms) at the reversal zone |

**Minimum viable confluence for a live trade:** D-1 (Fib zone) + at least one of D-2/D-3 (momentum divergence) + at least one of D-6/D-7 (structure break). Three independent strands minimum. Five or more = high-conviction. A wave count label *alone* never suffices.

---

## Table E — Risk / Position Rules

| # | Rule | Condition → Action |
|---|------|--------------------|
| E-1 | Fixed-fraction risk | Max 1–2 % of total account equity risked per trade. Position size = (account × risk_pct) ÷ |entry − stop|. Scale down to 0.5 % when confidence is low (confluence < 3 strands). |
| E-2 | Minimum reward:risk | Do not enter if T1 target delivers < 2:1 R:R. The W3 entry from W2 low (50–61.8 % retrace) typically delivers 3:1 to 5:1 to the 1.618 extension. If R:R < 2:1, the stop is too wide or the target too close — do not trade. |
| E-3 | Primary + alternate count | Always maintain one alternate count. Define the price that flips the primary to the alternate before entering. Size the trade so that the flip price = your stop. If price hits the flip level, the count has changed — this is not bad luck, it is information. |
| E-4 | Asymmetric size by wave position | W3 entries (highest probability, widest structural support): full 1–2 % risk unit. W5 fades (trend fighting, higher false-positive rate): 0.5 % risk unit. Corrective-ABC entries (structure more ambiguous): 0.5 % risk unit. |
| E-5 | Stop trail after T1 | Once T1 is hit and 30–50 % of position is taken off, move the remaining stop to breakeven + slippage. Never let a T1-hit trade turn into a loss. |
| E-6 | Stop trail in wave 3 | Trail the stop below each completed sub-wave (ii), (iv) inside the developing W3. Each new sub-wave pullback that holds and turns becomes the new stop. |
| E-7 | No additions against the stop | Never add to a losing position. If price approaches the structural stop, reduce, do not increase. The stop is the count's voiding level — it is not negotiable. |
| E-8 | Alternate-count sizing | When primary and alternate counts are both plausible (ambiguous structure, low count confidence), halve the position. Run full size only when the structure is unambiguous (hard-rule pass, 5+ confluence strands). |
| E-9 | Degree-proportionate stop width | The stop must be set at the count's structural voiding level *for the degree being traded*. A Minute-degree entry in a Primary-degree wave gets a Minute-degree stop (e.g., below the Minute W2 low), not a Primary-degree stop, to keep R:R sensible. |
| E-10 | Time invalidation | Set a maximum bar count within which the entry trigger must fire. If the trigger has not fired within N bars = the prior corrective leg's duration (Neely's time gate), cancel the order. An expected W3 that does not materialize after the time budget is exhausted is a sign the count is wrong. |
| E-11 | Earnings / event blackout | Do not initiate new EW-based structural positions within 2 sessions of a major scheduled event (earnings, FOMC). The structural count is irrelevant to gap risk. Existing positions: tighten stop to the recent swing extreme. |
| E-12 | Post-5 wave holding | After a 5-wave impulse is complete, *do not* add to the trend. The corrective phase follows. Fade the 5th wave or stand aside; never buy the breakout of a completed wave 5. |

---

## Gap to Our Engine: What Is and Is Not Encoded

The table below maps each practitioner rule category to the current `wavelib` implementation status, identifying concrete gaps.

| Rule area | What the engine does today | Gap |
|-----------|---------------------------|-----|
| **Entry trigger** | `TradePlan.entry_trigger` = break above/below the last confirmed pivot (`forecast.py:144-183`). Covers A-1 (W2 end break), A-3 (W4 end break) in a generic way. | **A-4, A-8 (W5 fade / ending diagonal fade)** — no special logic for detecting "end of W5 + divergence → short entry." `TradePlan` always trades in the direction of `fc.next_wave`; it does not generate a counter-trend fade signal when the next wave is a correction. **A-7 (triangle thrust)** — triangle is detected and `triangle_thrust()` computes the price target, but no TradePlan is emitted for the thrust entry itself. **A-9 (NeoWave time gate)** — partially in place (`confirm_window_bars` is the prior leg's bar count), but the two-condition check (2-4 trendline break *time* < W5 time AND full-W5-retrace time < W5 time) is not implemented. |
| **Stop placement** | `TradePlan.stop_level` = 1 % beyond the last swing (`forecast.py:168-173`). | **Structural stop is not count-derived.** The stop should be at the count-voiding level: below W2 low for W3 entries, below W4 low (at W1 top) for W5 entries, above W5 extreme for fade entries (B-1 through B-8). The current 1 %-swing proxy is correct in many cases but is not derived from the invalidation level. |
| **Invalidation level** | `WaveForecast.invalidation` = first leg start (`forecast.py:61`); passed through to `TradePlan.invalidation`. Correct for an impulse (W1 start invalidates the count). | **Not wave-position-specific.** For a W4/W5 entry, the invalidation should be the W4/W1-overlap level, not the W1 origin. Corrective-entry invalidation (wave C end) is also not distinguished from impulse invalidation. |
| **Fibonacci targets** | `forecast_from_count` computes 0.382/0.5/0.618 retrace targets after an impulse, and 0.618×/1.0×/1.618× last-leg after a correction (`forecast.py:58-83`). | **W3 extension targets missing** (1.618, 2.618, 4.236 × W1 from W2 low). **W5 = W1 equality and 0.382/0.618 × net(W1-W3) missing** (the engine only uses channel projection implicitly via the last-leg multiples). **Fibonacci cluster not computed** — no logic to find zones where ≥ 3 independent Fibonacci measurements overlap (D-8, C-8). |
| **Channel projection** | `triangle_thrust()` in `rules.py` computes post-triangle targets. 2-4 trendline exists in `rules.py:channeling`. | **Upper-channel W5 target missing.** The practitioner's primary W5 projection method is to draw a parallel through W3 top off the 2-4 trendline; no function in the engine computes this and emits it as a TradePlan target. |
| **RSI divergence** | `momentum_divergence()` in `confluence.py` — hardened (Phase 3): swing-pivot RSI pairs, ≥50-bar guard, ≥3-RSI-point filter. Regular + hidden divergence. | **Not wave-position-aware.** The engine computes divergence generically; it does not specifically test "is this a bearish divergence on the 5th swing high?" (D-2, D-5). Connecting the divergence type to the wave label (W5 vs W3) and adjusting entry direction accordingly is missing. |
| **Volume confirmation** | `volume_capitulation()` in `confluence.py` — 20-bar window + wide-range filter (Phase 3). | **W3 > W1 volume comparison missing** (D-5). The current implementation detects spikes at reversal points; it does not compare W3 volume to W1 volume to confirm an impulse is genuine (vs a corrective disguised as a 3-wave structure). |
| **CHoCH / BOS** | `choch()` in `confluence.py` — swing-pivot based, body-close confirmed, BOS vs CHoCH distinguished (Phase 3). | **Good fidelity.** The main gap is that the output of `choch()` is a 0/1 confluence strand; the direction of the CHoCH (bullish vs bearish) is not passed back to `TradePlan` to filter out structurally-opposed entries. |
| **Multi-TF alignment** | Not implemented. `wave_counts()` operates on a single bar array. | **Fully absent.** There is no mechanism to check "does the 1-higher-TF count align with this trade?" (D-13). The entry is generated from the local count only. |
| **Alternate count** | Not implemented. `wave_counts(..., max_alternates=0)` is the default. | **Fully absent for TradePlan.** `wave_counts` can return alternates when `max_alternates > 0` but `TradePlan` / `trade_plan()` only uses `counts[0]`. E-3 (define the alternate and price that flips it before entering) is completely unimplemented. |
| **Position sizing / R:R** | Not implemented. The engine is "analysis tooling only" (CLAUDE.md). | **Intentionally absent** — out of scope per CLAUDE.md. However, E-2 (minimum 2:1 R:R gate) could be computed from `(T1_target − entry) / (entry − stop)` and emitted as a `TradePlan` field to let the caller filter. |
| **Fibonacci cluster detection** | Not implemented. | **Fully absent.** No function collects multiple independent Fibonacci projections and identifies where they overlap. This is the most cited high-value confluence tool in institutional EW practice. |
| **NeoWave time gate** | `TradePlan.confirm_window_bars` = prior-leg bar count (a proxy). | **Partial.** The two-condition Neely gate (2-4 trendline break in < W5 time AND full W5 retrace in < W5 time) is not checked. The single `confirm_window_bars` field is the intent, but the trigger logic is not executed. |
| **Ending diagonal detection + fade** | `ending_diagonal_rules()` in `rules.py` (Phase 1 C-3). The distinction from leading diagonal is implemented. | **TradePlan does not consume this.** When `wave_counts` identifies an ending diagonal as the completed pattern, `forecast_from_count` and `trade_plan()` treat it the same as any corrective/terminal pattern — they do not emit a fade-short plan with stop above the diagonal extreme (A-8, B-8). |
| **Minimum confluence gate for entry** | `score_reversal()` returns an integer strand count; `backtest_reversals` filters by `min_score`. | **TradePlan does not enforce a minimum score.** `trade_plan()` does not call `score_reversal()` internally; the caller must do this manually. A structural check — "only emit a TradePlan if confluence ≥ 3 strands" — is missing. |

---

## Summary: The 5 Highest-Impact Rules to Implement

Listed by expected gain in signal quality and risk-adjusted return, given the current engine gaps:

### 1. Fibonacci Extension Targets for W3 and W5 (C-1, C-2)
**Gap:** `forecast_from_count` computes only retrace targets after an impulse. W3 entries — the highest-probability, highest R:R setup — have no T1/T2/T3 targets.
**Fix:** Compute 1.618, 2.618 × W1 from W2 low (W3 targets); W1-equality and 0.382 × net(W1-W3) from W4 low (W5 targets); and emit them in `WaveForecast.targets`. One arithmetic function, enormous impact on usability.

### 2. Count-Derived Structural Stop (B-1 through B-4)
**Gap:** `TradePlan.stop_level` is 1 % beyond the last swing, not the count-voiding level. For a W3 entry the structural stop is W2 low; for a W5 entry it is W4 low (or W1 high). An oversized stop inflates risk; an undersized stop exits before the count is actually voided.
**Fix:** Branch `trade_plan()` on the wave label of the last completed wave: if we are entering into W3 (last completed = W2), stop = W2_low × 0.999; if entering into W5 (last completed = W4), stop = W4_low × 0.999; if fading after W5, stop = W5_high × 1.001. Pass the label out from `forecast_from_count`.

### 3. Fibonacci Cluster Detection (D-8, C-8)
**Gap:** The single highest-cited practitioner edge in institutional EW is the "price cluster" — when ≥ 3 independent Fibonacci projections from different swing pairs converge within 1–2 %. Our engine emits targets per-wave but never intersects them.
**Fix:** Add a `fib_cluster(projections, tolerance=0.02)` function in `toolkit.py` that collects all Fibonacci measurements (retrace of the impulse, extension of W1, equality of W-A, etc.) and returns clusters where ≥ 3 overlap. Emit the cluster as the primary target zone in `WaveForecast.targets`.

### 4. Alternate Count + Flip Price (E-3)
**Gap:** `trade_plan()` uses `counts[0]` only. No alternate count is carried forward. A trader following the output has no price level to watch for a count flip.
**Fix:** Re-enable `max_alternates=1` in `trade_plan()`; emit a `TradePlan.alt_invalidation` = the price level from `counts[1]` that contradicts `counts[0]`. Add a warning when the primary and alternate counts disagree on direction. This is a risk management field, not an additional signal.

### 5. Minimum Confluence Gate on TradePlan Emission (D-minimum, E-2)
**Gap:** `trade_plan()` emits a plan regardless of how many confirmation strands are satisfied. A W5-label on a 1-confluence-strand count is structurally no different from a W3-label on a 6-strand count, yet both generate a TradePlan.
**Fix:** Call `score_reversal(bars, ...)` inside `trade_plan()` and only emit the plan if `score >= min_confluence` (default 3). Expose `min_confluence` as a parameter. Emit the actual `score` in `TradePlan` so the caller sees "confidence 45%, score 3/7" and can filter further. This alone would eliminate most false-signal plans.

---

*Document generated 2026-06-12. Sources cited inline. This is methodology research — not trading advice.*
