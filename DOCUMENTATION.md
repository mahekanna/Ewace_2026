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
- `data/avgo.py`, `data/mrvl.py` (auto-generated fixtures): `WEEKLY (t,h,l,c)`,
  `DAILY (t,o,h,l,c,v)`, `H4 (t,h,l,c)`, `H1 (t,o,h,l,c)`, `FRESH_4H_VOL (t,o,h,l,c,v)`.
  `data/mrvl.py` also carries the hand-curated `MACRO_PIVOTS [(date,price,kind)]` below a
  marker line that the generator preserves verbatim.
- `data/live/<slug>_<tf>_<tag>.json` (snapshots, `tf` ∈ 15m/1h/4h/1d/1w, `tag` = YYYY-MM):
  `{"symbol","interval","asof","bars":[{t,o,h,l,c,v}]}` — the contract every script under
  `scripts/` reads (see `docs/COLLAB_RUNBOOK.md`). The `2026-06` tag is the June-2026
  baseline (TradingView/Alpaca); `2026-11` was pulled with `data/fetch.py`.

### `data/fetch.py` — loader + refresher

```python
from data.fetch import load_bars
bars = load_bars("AVGO", "1d")              # newest snapshot tag -> [(t,o,h,l,c,v), ...]
bars, meta = load_bars("MRVL", "1w", tag="2026-11", with_meta=True)
```
Loading is stdlib-only. Fetching needs the optional `yfinance` extra:

```bash
pip install yfinance
python3 data/fetch.py                         # AVGO + MRVL -> data/live/*_{1d,1w,1h,4h}_<YYYY-MM>.json
python3 data/fetch.py AVGO MRVL --fixtures    # ...and regenerate data/avgo.py / data/mrvl.py
python3 data/fetch.py NVDA --tf 1d 1w --tag 2026-11
```
Conventions baked in: regular session only; split-adjusted but *not* dividend-adjusted
(`auto_adjust=False`, identical to Alpaca `adjustment=split` — the two agree to the cent);
daily bars stamped midnight ET; 4h bars built from 1h bars at 09:30/13:30 ET; weekly bars
built from daily bars (Mon–Fri, stamped Monday) because Yahoo's native weekly series is not
week-aligned for every ticker. Yahoo depth caps: 15m ≤ 60 days, 1h ≤ 730 days.

### Count continuation — the count held at every bar

`analyze_symbol` labels the end of the series. `wavelib/count_history.py` replays the
history causally (at bar *i* the engine sees `bars[:i]` only) and records, per bar, the
**anchored** count (`wave_counts` on the trailing window: pattern, degree, confidence,
labelled legs) and the **recent** validated candidate (`label_and_validate`). Runs of
identical labelling are compressed into `CountSegment`s with a transition tag — EXTEND
(same origin, legs advanced), RELABEL (pattern changed), SHIFT (same pattern, new anchor),
NEW/LOST. `render_count_history_page` emits a self-contained page: price line, a pattern
band per bar, a scrubber/play-head that redraws the as-of legs (only bars left of the head
were visible), and the segments table.

**Forecasting the next wave, tested.** Each time a new anchored count is adopted,
`forecast_from_count` (`wavelib/forecast.py`) projects the next wave from it with the
bars visible then — direction, Fibonacci targets (retracements after a 5, extensions /
Blue Box after a 3, thrust after a triangle), the void level, and the NeoWave time window
[N/3, 3N]. `grade_forecasts` then walks the bars that followed: **HIT** (nearest target
reached), **HIT_FULL** (farthest), **INVALIDATED** (void level crossed first, judged from
the side price was on at adoption — an impulse's void sits beyond its correction targets),
**EXPIRED** (nothing within 3N), **OPEN**. `forecast_scorecard` aggregates hit rates per
pattern; the page draws the projection at the play-head (targets, void, projected leg) and
reveals the outcome only after the play-head passes it; the ledger tab lists every
projection. On the 2026-11 daily replay the nearest-target hit rate is low (see
`reports/COUNT_HISTORY_2026-11.md`), consistent with the forecast backtest in
`reports/FORECAST_BACKTEST_2026-06.md`: the forecaster is a bias, not an edge.

```bash
python3 scripts/count_history.py AVGO MRVL --tag 2026-11 [--window 300] [--stride 1] [--start 2021-01-01]
# -> charts/<sym>_count_history_<tag>.html, reports/COUNT_HISTORY_<tag>.md (brief + scorecard + ledger + segments)
```

### What every count must obey (Nov 2026 audit — `docs/RULESET.md` §I)

Both counters (`wavetree.top_down_count` partition search and the bottom-up
`_build_level` grouping) enforce, for every labelled wave: R1/R2/R3; pivot kind matches
leg direction with alternating boundaries; a wave's end is its extreme (pivot AND bar
level; truncated fifth allowed with a haircut; triangles exempt); the NeoWave extension
(one of 1/3/5 ≥ 1.618× the next-longest); Similarity & Balance with at least one of
price/time in [⅓, 3×]; the 2-4 line unbroken by the interiors of waves 3 and 5; zigzag C
beyond A's end; regular flats with C ≈ A. Candidates are ranked by one score, confidence ×
coverage, with structures that end at the window end (the present) first — including
counts whose **final wave is still running** (`AnchoredCount.in_progress`), for which the
forecast is the completion of that wave. `wave_counts(..., present_first=False)` gives the
macro view (dominant structure). The ZigZag no longer loses a series' first extreme nor
confirms a reversal on the bar that set the extreme. `tests/test_rule_audit.py` is the
executable version of this list.

### The plain-language read — `wavelib/brief.py`

`decision_brief(symbol, bars, scorecard=..., adoption_t=...)` turns the current anchored
count + projection into something a non-specialist can use: **Where we are** (the count in
words), **What the engine expects next** (direction, first/far target, deadline), **What
confirms it / what kills it** (the trigger = a close beyond the pivot before the last leg;
the void = the count's invalidation; a protective reference beyond the last pivot; the
live confluence x/7), **How reliable is this kind of call** (the replay scorecard row for
that pattern, phrased as decent / coin-flip / weak), and **What to do**. It commits to one
stance — `NO READ`, `WAIT FOR CONFIRMATION`, `CONFIRMED BIAS`, `PLAYED OUT`, `STAND ASIDE` —
decided causally from the bars since the count was adopted (void crossed → stand aside;
first target reached → played out; past the deadline unconfirmed → expired; trigger
crossed → confirmed; else wait). The brief sits at the top of each count-history page with a
glossary, and `python3 scripts/brief.py` prints it / writes `reports/BRIEF_<tag>.md`.
It is a reading of structure, not advice on sizing or execution.

Run the full daily stack on a snapshot with
`python3 scripts/run_validation.py --tag 2026-11 --symbols AVGO MRVL` → writes
`reports/VALIDATION_<tag>.md` + `charts/<sym>_analysis_<tag>.html`. Hand-set reversal zones
apply only to the `2026-06` baseline; other tags derive the zone from the recent up-leg.

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
