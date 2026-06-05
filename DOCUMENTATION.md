# DOCUMENTATION — `wavelib` Elliott / NeoWave Research Engine

Version 0.1.0 · pure-stdlib Python 3.9+ · no third-party dependencies.

---

## Table of contents
1. Philosophy & design
2. Install / run
3. Architecture & data flow
4. Module reference (`rules`, `toolkit`, `confluence`)
5. Data format & the `data/` package
6. Worked AVGO / MRVL example (the session's findings)
7. Extension guide (where to add research)
8. Theory notes (what each rule encodes)
9. Known limitations & honest caveats

---

## 1. Philosophy & design

A wave label is a **hypothesis about structure**; it tells you *where* a reversal is
structurally permitted, never *whether* one is occurring. This library therefore
separates three concerns:

- **Structure** (`rules`): is a given sequence a valid Elliott impulse / correction /
  diagonal / NeoWave terminal? Does it pass the hard rules and the channeling tests?
- **Measurement** (`toolkit`): ZigZag pivots from raw OHLC, Fibonacci relationships,
  terminal-retrace timing, wave-5 projection.
- **Confirmation** (`confluence`): independent reversal evidence — momentum
  divergence, MACD, volume climax, market-structure CHoCH, channel break — combined
  into a score. **Only act when the score is high AND the label permits.**

The guiding rule: methods must fail *independently*. A reversal you can only see in
the wave count is not confirmed.

---

## 2. Install / run

No install needed (stdlib only).

```bash
# run the built-in self-tests
python3 wavelib/rules.py
python3 wavelib/toolkit.py

# run the examples
cd examples
python3 01_validate_avgo.py
python3 02_confluence_score.py
python3 03_zigzag_pipeline.py
```

As a library:

```python
from wavelib import zigzag, pivots_to_waves, validate_impulse, report
bars = [(t, o, h, l, c), ...]          # unix t
pivots = zigzag(bars, pct=0.05)
waves  = pivots_to_waves(pivots[-6:])  # last 5 legs
print(report(validate_impulse(waves)))
```

`requirements.txt` lists only optional extras (matplotlib/pandas) you may add for
your own research; the core engine needs none.

---

## 3. Architecture & data flow

```
            raw OHLC(+V)                 (t,o,h,l,c[,v])
                 │
                 ▼
        toolkit.zigzag(pct)              → list[Pivot]   (the wave skeleton)
                 │
                 ▼
     toolkit.pivots_to_waves()           → list[Wave]    (directional legs)
                 │
       ┌─────────┴───────────┐
       ▼                     ▼
 rules.validate_impulse   rules.validate_correction
   • hard rules             • zigzag/flat/triangle ID
   • guidelines             • retracement logic
   • S&B + terminal         • complex-correction zoo
   • channeling             
       │
       ▼
   rules.report()  → PASS/FAIL/WARN/REF verdict
       │
       ▼
 confluence.score_reversal(bars, zone)   → ConfluenceReport (0–7 score)
   • Fib zone   • divergence   • MACD   • volume   • channel   • CHoCH
   • (+ external Hurst/FLD cycle slot)
```

Canonical `Pivot`/`Wave` live in `rules.py`; `toolkit.py` imports them in package
context and falls back to local copies when run standalone.

---

## 4. Module reference

### 4.1 `wavelib.rules`

**Data structures**
- `Pivot(t, price, kind)` — `kind` ∈ {"H","L"}; `.date` property.
- `Wave(start, end, label="")` — `.length .signed .days .up .retr(other)`.
- `Status` enum: PASS / FAIL / WARN / NA / REF.
- `RuleResult(rule, status, detail)`.

**Elliott — impulse**
- `elliott_hard_rules(waves5)` → the 3 inviolable rules (R1 wave2<100%, R2 wave3 not
  shortest, R3 wave4/wave1 no overlap). Any FAIL ⇒ labeling is wrong.
- `elliott_guidelines(waves5)` → extension, equality, alternation, depth bands,
  wave3 fib ratio (WARN-level, probabilistic).
- `project_wave5(w1_len, w3_len, w4_end, prior_high)` → `{w5=w1, w5=0.618*w3,
  truncation_risk}`.

**Elliott — corrections**
- `classify_correction(waves)` → ZIGZAG / FLAT(regular/expanded/running) / TRIANGLE
  (3 or 5 legs) / combination.
- `diagonal_rules(waves5, position)` → leading/ending diagonal checks.

**NeoWave**
- `similarity_and_balance(a, b, lo=1/3, hi=3.0)` → price AND time band check.
- `rule_of_proportion(parent, child)`.
- `retracement_logic(retr)` → depth → implied prior-wave identity (REF).
- `is_terminal(waves5)` → terminal impulsion (wave4/wave1 overlap; contracting flag).
- `terminal_retrace_window(build_days, top_t)` → fast-full-retrace completion dates.
- `classify_complex_correction(legs)` → 5=triangle, 7=diametric/symmetrical, 8+=multi-X.

**Channeling (computed)**
- `line_value(p1, p2, t_query)` → trendline value at a time.
- `two_four_test(w2, w4, t_now, price_now, uptrend)` → is the 2-4 line broken?
  (impulse confirmed-complete only on a decisive break).
- `throwover_test(w1_top, w3_top, w5_peak, peak_t, uptrend)` → THROW-OVER vs
  FELL-SHORT of the 1-3 channel.

**Engines**
- `validate_impulse(waves, diagonal=False)` → all applicable impulse rules + S&B + terminal.
- `validate_correction(waves)` → classification + retracement logic + complex check.
- `report(results, title="")` → formatted string with a VALID/INVALID verdict
  (INVALID iff any hard-rule FAIL).

### 4.2 `wavelib.toolkit`

- `zigzag(bars, pct=0.10)` → `list[Pivot]`. Percentage-reversal on intrabar
  highs/lows; seed branch avoids dual-update corruption; collapses consecutive
  same-kind pivots keeping the extreme.
- `pivots_to_waves(pivots, labels=None)` → `list[Wave]`.
- `fib_extension(w1_len, base, ratios)` / `fib_retrace(high, low, ratios)`.
- `wave_ratio(a, b)`.
- (also standalone copies of S&B / terminal projection / wave5 for offline use.)

### 4.3 `wavelib.confluence`

- Indicators: `rsi(closes, n=14)`, `ema(vals, n)`, `macd(closes,12,26,9)`.
- Strands (each returns a `Strand(name, confirm, detail)`):
  `in_zone`, `momentum_divergence`, `macd_turn`, `volume_capitulation`,
  `channel_break`, `choch`.
- `classify_swing_sequence(pivot_prices)` → impulsive(5) vs corrective(3) guess.
- `score_reversal(symbol, bars, zone, bullish=True, cycle_aligned=False)` →
  `ConfluenceReport` with `.score` / `.max_score` (7) and a verdict tier:
  ≥4 HIGH-CONFIDENCE, 2–3 BUILDING, ≤1 STRUCTURALLY-ALLOWED-ONLY.

---

## 5. Data format & the `data/` package

- `zigzag` and chart pipelines expect bars as `(t, o, h, l, c)`, `t` in unix seconds.
- `score_reversal` expects `(t, o, h, l, c, v)` (volume required for the volume strand).
- `data/avgo.py`: `WEEKLY (t,h,l,c)`, `H4 (t,o,h,l,c)`, `H1 (t,o,h,l,c)`,
  `FRESH_4H_VOL (t,o,h,l,c,v)`.
- `data/mrvl.py`: `FRESH_4H_VOL (t,o,h,l,c,v)`, `MACRO_PIVOTS [(date,price,kind)]`.

To refresh, pull new OHLCV from your data source (this session used TVremix MCP:
exchange-prefixed `NASDAQ:AVGO`, `get_ohlcv` with `summary:False`) and overwrite the
arrays, keeping the tuple shape.

---

## 6. Worked example — the session's AVGO / MRVL findings

**AVGO** (as of Jun 5 2026, price $385.74):
- Primary (I) 41.51→251.88, (II)→138.10, (III)→495.00 (two Fib projections within ~$1 of $495).
- Top = expanding/irregular terminal impulsion (4h). Wave ⑤ **fell short** of the $560 1-3 channel (weak fifth).
- 2-4 line ~$301 **unbroken** → completion not yet channel-confirmed.
- Decline $495→$385 is **A-B-C corrective** into the $358–410 (IV) zone. Invalidation $251.88.
- Wave (V) projection: $500–510 (truncation risk) to $540–620 (if (IV) shallow).
- Reversal confluence: **1/7** — allowed, not confirmed.

**MRVL** (price $263.47):
- (I) 33.75→127.48, (II)→47.09 (85.8% — edge), (III)→324.20 (+589%; ((3)) 4.5× extended → S&B-stretched).
- Top = extending impulse (not terminal) → normal correction; threw **over** the $223 channel (blow-off).
- Pulled back $324→$263 into the $229–266 ((4)) zone. Reversal confluence **1/7**.

---

## 7. Extension guide (where to add research)

High-value next steps (left as hooks):

1. **`label_and_validate(bars)`** — auto-segment ZigZag pivots into candidate
   impulses/corrections, run every degree, and return the best-scoring count. Today
   you hand-pick which 5 legs to validate.
2. **Hurst / FLD / PSK cycle slot** — `score_reversal(..., cycle_aligned=True)` already
   reserves the 7th strand. Wire your CMA-bandpass / FLD model so "where" (Elliott)
   meets "when" (cycles).
3. **More confluence bars** — the RSI/divergence strand needs >14 bars; feed 50–100.
4. **Auto-degree labeling** — encode Neely's monowave→polywave→multiwave construction
   so degrees are assigned, not assumed (this is the biggest open subjectivity).
5. **Backtest harness** — replay historical bars, score reversals, measure hit-rate of
   score≥4 zones vs invalidations.
6. **Charting** — the `charts/*.html` are hand-built SVG; consider a `render_chart(waves,
   projections)` that emits them programmatically.

---

## 8. Theory notes (what the rules encode)

- **Elliott hard rules**: the only inviolable constraints; everything else is a guideline.
- **Channeling first (NeoWave)**: price behaviour vs the 0-2 / 2-4 / 1-3 lines helps
  *identify* structure, not just confirm it — run it before trusting a count.
- **Similarity & Balance**: adjacent corrective waves relate in price AND time within
  ~1/3–3×; violations flag a mislabeling or a hidden complex structure.
- **Terminal impulsion**: 5 legs each a three, wave4 overlaps wave1, ideally
  contracting; fully + rapidly retraced to its origin once complete.
- **Truncation**: a deep 4th caps the 5th near the prior high — a failed/marginal new high.

---

## 9. Known limitations & honest caveats

- **Degree is subjective.** The library validates *a* count's internal consistency; it
  does not prove the chosen degree is the correct one. Reasonable analysts label the
  same price action differently (see the ArtavestPro comparison in README).
- **Channeling beyond the 2-4 / 1-3 lines is `REF`** (converging-triangle boundaries,
  complex containment) — needs the full leg set and discretion.
- **Complex-correction subtypes** (diametric/neutral/extracting) are heuristic, not
  the exact Neely construction.
- **The terminal-retrace timing rule over-projected depth** on AVGO ($290 vs the actual
  shallow $385). Treat terminal targets as a *bias*, not a number — and lean on the
  confluence score for confirmation.
- **Not investment advice.** This is research tooling.
