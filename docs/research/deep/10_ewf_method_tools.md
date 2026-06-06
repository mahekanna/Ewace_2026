# EWF (ElliottWave-Forecast.com) — Method, Tools & Indicators: Research Harvest

**Date:** 2026-06-06
**Author:** Research agent (Ewace_2026)
**Status:** Reference — external methodology harvest, not binding spec

---

## 1. Scope & Method

### 1.1 What This Document Is

This document harvests the publicly accessible methodology of
**ElliottWave-Forecast.com (EWF)**, a subscription-based Elliott Wave forecasting
service founded in 2005 by Eric Morera. EWF serves ~78 world markets (FX majors,
equity indices, commodities, crypto) and has developed several proprietary extensions
on top of classical Elliott Wave theory that are worth understanding as reference
points for the Ewace_2026 engine.

The goal is to identify:
- What EWF does that goes *beyond* textbook Elliott / Prechter/Frost
- Which ideas are mechanically implementable in our deterministic engine
- Which ideas are genuinely discretionary/proprietary and cannot be replicated

### 1.2 Retrieval Method & Limitations

**Direct WebFetch on elliottwave-forecast.com returns HTTP 403** (anti-bot
protection). The PDF at
`https://elliottwave-forecast.com/wp-content/uploads/2014/11/eBookFFF.pdf`
also returned 403.

All content below was retrieved via **site-scoped web searches** (26 queries total).
Search summaries include paraphrased content from EWF pages; exact wording is
reproduced where unambiguous. The member-only areas (live charts, video rooms,
strategy-of-the-day) are inaccessible — this document covers only the public
educational content and blog posts.

Sources are cited inline by URL and compiled in §7.

---

## 2. EWF Methodology — Topic by Topic

### 2.1 Overview: EWF's System Components

EWF describes their full analytical system as comprising:

> "Elliott Wave Theory, cycles, sequences, time, distribution, correlations, and
> Fibonacci."

They explicitly state they do **not** use fundamental or sentiment analysis because
it "provides neither actionable trades nor ways to manage risk."

Their primary claim to differentiation over classical EWT:

1. **Swing-sequence counting** (3/7/11 corrective vs 5/9/13 impulsive) replaces
   pure 5-wave labeling as the primary trading trigger.
2. **Blue Box** — a proprietary Fibonacci-extension confluence zone used as a
   mechanical entry area.
3. **Right Side tag** — a visual directional stamp (green/red/black) that tells
   traders whether to buy dips or sell rallies at any given moment.
4. Integration of **High-Frequency Trading (HFT) dynamics** — the claim that
   modern algorithmic market participants consistently re-enter at recurring
   Fibonacci levels, making those levels "self-fulfilling" inflection points.
5. A **distribution / currency ranking** system (largely proprietary/opaque from
   public content).

Sources:
- https://elliottwave-forecast.com/elliottwave/the-elliott-wave-theory-and-high-frequency-trading/
- https://elliottwave-forecast.com/trading/market-nature-art-trading/
- https://elliottwave-forecast.com/ (homepage description)

---

### 2.2 The Blue Box — Definition, Ratios, and Usage

The Blue Box is EWF's most distinctive public concept. It is described consistently
across dozens of articles and is the core "high-probability trade setup" vehicle.

#### Definition

> "Blue Boxes are High-Frequency and High Probability / Low Risk areas based in a
> relationship of sequences, cycles and calculated using extensions."

More precisely: a Blue Box is drawn as a **price zone spanning the 100%–161.8%
Fibonacci extension** of a corrective move within a 3, 7, or 11 swing corrective
sequence. It marks where the correction is **statistically expected to end** and
the dominant trend to resume.

#### Why "High Frequency"?

EWF's rationale is that HFT algorithms also target these Fibonacci extension zones
to re-enter in the direction of the primary trend. Both buyers and sellers converge
at these levels — sellers taking profits from the prior move, buyers initiating new
positions — creating a natural inflection. The zone is therefore not a random pick
but an area where **institutional and algorithmic order flow clusters**.

#### Drawing the Blue Box

From multiple worked examples:

1. Identify the dominant trend direction (bullish or bearish sequence established).
2. Count the corrective swing structure — confirm it is in a 3, 7, or 11 corrective
   sequence (not a 5/9/13 impulsive one).
3. Measure the Fibonacci extension of leg A (or wave W) projected from the origin
   of leg B (or wave X):
   - **Lower boundary:** 100% extension (equal legs / A=C point)
   - **Upper boundary:** 161.8% extension (the "extreme" / invalidation boundary)
4. The resulting price band is the Blue Box (drawn as a shaded rectangle on the
   chart).

In a bullish Blue Box, the zone is **below** current price (buyers expected to enter
as price pulls back into it). In a bearish Blue Box, the zone is **above** current
price (sellers expected to enter on a bounce into it).

#### Invalidation Rule

If price **closes beyond the 161.8% extension** (the outer boundary of the Blue
Box), the trade setup is invalidated. This is the stop-loss anchor:

> "Invalidation for the long trades is break of 1.618 fib ext (the lower boundary
> of the Blue Box area)."

Position size is sized so that **maximum 2% of capital** is risked if the stop
(161.8% breach) is hit.

#### Trade Management Once Entered

> "Once bounce reaches 50 Fibs against the blue connector, positions are made
> risk-free and the stop loss is set at breakeven with partial profits booked."

The sequence is:
1. Enter at the top of the Blue Box (100% extension level) on the first touch.
2. Hold with stop below 161.8%.
3. When price bounces 50% of the Blue Box range, move stop to breakeven (risk-free).
4. Trail or scale out toward higher targets (next wave projection).

#### Blue Box Wins

EWF maintains a public "Blue Box Wins" tracker. Examples cited include:
- AMD: 25%+ rally from Blue Box entry
- Microsoft (MSFT): 27% gain since April entry
- Bitcoin: 50% gain from buying zone
- EURUSD: 6.5% since May buy entry

No aggregate win rate or statistical distribution is published publicly.

Sources:
- https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/
- https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/
- https://elliottwave-forecast.com/forex/cadjpy-elliott-wave-blue-box-buy-setup/
- https://elliottwave-forecast.com/trading/ibex-elliott-wave-buying-blue-box/
- https://elliottwave-forecast.com/stock-market/sp-500-spx-elliott-wave-buying/
- https://elliottwave-forecast.com/trading/dax-elliott-wave-buying-dips-blue-box/

---

### 2.3 Swing-Sequence Framework (3/7/11 vs 5/9/13)

This is EWF's primary structural innovation over classical Elliott Wave counting.

#### The Core Arithmetic

| Sequence type | Counts |
|---|---|
| Impulsive (trend) | 5, 9, 13, 17, 21… |
| Corrective (counter-trend) | 3, 7, 11, 15, 19… |

A "swing" is defined as a pivot-to-pivot move (each directional leg between a high
and low counts as one swing). The count includes *all* legs of any corrective
structure at the trading degree.

**Key insight:** The distinction between a 5-swing move (incomplete corrective) and
a 5-wave impulse is resolved by examining the *internal structure* of the largest
middle swing. If the biggest correction in the middle is "too large to be wave 4 of
an impulse," the sequence is corrective and therefore *incomplete* at 5 swings —
calling for one more leg to complete the 7-swing structure.

#### Incomplete Sequences as the Trading Edge

> "Elliott Wave Forecast relies on Swing Sequences rather than 5 wave moves to find
> their Trading Edge."

When 5 corrective swings are visible, EWF stamps the chart with a **Bullish
Sequence** (if trending up) or **Bearish Sequence** (if trending down) to indicate:
- The 6th swing pullback is expected → entry zone
- The 7th swing should complete the corrective cycle → target zone

This resolves a chronic ambiguity in classical EWT: whether a 3-wave move is a
complete zigzag (ABC) or just the first W of a double-three (WXY). EWF's answer is
to count swings and treat the 5-swing state as inherently incomplete.

#### Impulsive Sequence Completion

For impulsive sequences (5, 9, 13…):
- 5 swings up = possible wave 1 or A complete → look for 3-swing correction
- 9 swings up = possible wave 3 complete → look for wave 4 correction
- 13 swings up = possible wave 5 / larger impulse complete → potential reversal

EWF distinguishes these by checking whether the internal structure of each upswing
shows 5 sub-waves (impulsive) or 3 sub-waves (corrective).

#### Stamps on Charts

Public charts carry color stamps:
- **Green "Bullish Sequence"** = buy dips toward the next corrective swing
- **Red "Bearish Sequence"** = sell rallies toward the next corrective swing
- **Black** = right side is unclear, no directional bias

Sources:
- https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/
- https://elliottwave-forecast.com/stock-market/spx500-bullish-elliott-wave-sequence/
- https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/
- https://elliottwave-forecast.com/elliottwave/usdjpy-elliott-wave-double-three/

---

### 2.4 The "Right Side" Tag System

The Right Side concept is EWF's directional bias overlay — distinct from the wave
count itself.

> "When the chart shows the right side is higher in green, traders should only buy
> the dips and not try to sell pullbacks. Conversely, when the chart shows the right
> side is lower in red, traders should only attempt to sell rallies. If the right
> side tag is black in color, this means the right side is not clear."

The Right Side is determined by:
1. The larger-degree sequence stamp (Bullish or Bearish Sequence from §2.3).
2. The position within the multi-timeframe hierarchy (higher timeframe determines
   the Right Side for lower timeframe trading).

**Key rule:** Traders only enter Blue Box setups that are *aligned with* the Right
Side tag. A Blue Box appearing in a Bearish Sequence on the daily chart should not
be bought (it would be a counter-trend trade against the Right Side).

The Right Side can change when an instrument breaks its higher-degree invalidation
level.

> "Each time frame has its own right side and also its own invalidation level."

Sources:
- https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/
- https://elliottwave-forecast.com/trading/right-side-helps-survival-trading-world/
- https://elliottwave-forecast.com/forex/trading-eurgbp-with-right-side-system/

---

### 2.5 Fibonacci Ratios — Complete EWF Reference Table

EWF uses a specific set of Fibonacci ratios that extends beyond the standard
textbook set. The full reference:

#### Retracement Levels (corrections against prior wave)

| Level | Application |
|---|---|
| 23.6% | Wave 4 in strong trending markets; shallow corrections |
| 38.2% | Wave 4 in standard trends; wave 2 shallow retraces |
| 50.0% | Wave 2 and wave B standard retracement |
| 61.8% | Wave 2 and wave B standard retracement (golden ratio) |
| 76.4% | Wave 2 deeper retracement; wave X connector |
| 85.4% | Wave 2 maximum "normal" retracement before invalidation risk |

> "Wave 2 typically resides at 50%, 61.8%, 76.4%, or 85.4% of wave 1."

Stop placement for Wave 2 entries: beyond the **85.4% retracement** level.

#### Extension Levels (projection of next impulsive leg)

| Level | Application |
|---|---|
| 100% | Equal legs (A=C or W=Y) — the primary Blue Box lower boundary |
| 123.6% | Common C wave target in regular flats; typical W=Y projection |
| 161.8% | Wave 3 primary target (measured from wave 1); Blue Box upper boundary / stop |
| 200% | Wave 3 extended target |
| 261.8% | Wave 3 maximum extension in very strong trends |
| 323.6% | Wave 3 extreme extension |

Specific relationships:
- **Wave 3** = 161.8%, 200%, 261.8%, or 323.6% of Wave 1
- **Wave 5** = inverse 123.6–161.8% retracement of Wave 4, or equal to Wave 1, or
  61.8% of Wave 1+3 combined
- **Wave C in zigzag** = 100%–123.6% of Wave A (normal); 123.6%–161.8% (expanded)
- **Wave C exceeds 161.8% of A** = warning that count may be Wave 3 of an impulse,
  not a corrective C
- **Wave Y (in WXY double-three)** = 100%–123.6% of Wave W (typical); stop below
  161.8%

> "One of the most used Fibonacci key levels in Elliott wave analysis is 123.6%."

Sources:
- https://elliottwave-forecast.com/trading/fibonacci-retracement-and-fibonacci-extension/
- https://elliottwave-forecast.com/elliottwave/measure-fibonacci-extensions-elliott-wave-flat-corrections/
- https://elliottwave-forecast.com/elliottwave/importance-of-an-elliott-wave-zigzag-fibonacci-extension/
- https://elliottwave-forecast.com/trading/fibonacci-retracement-elliott-wave-guide/

---

### 2.6 RSI Divergence — EWF's Momentum Validation Protocol

RSI divergence is EWF's primary momentum confirmation tool, applied systematically
to validate or invalidate wave counts.

#### The Core Rules

1. **Impulse structures must end with RSI divergence** between Wave 5 and Wave 3.
   Specifically: price makes a new high in Wave 5 while RSI makes a *lower* high
   versus Wave 3. Absence of this divergence suggests the move is not yet complete
   or not an impulse.

2. **Corrective structures should end without RSI divergence.** This helps
   distinguish a corrective C wave (which need not show divergence) from a Wave 5
   (which should).

3. **Each impulsive subdivision should have internal RSI divergence:**
   > "Each impulsive subdivision (wave 1, wave 3 and wave 5) should have RSI
   > divergence in its internals."

4. **Leading Diagonal** — strong RSI divergence between Wave 3 and Wave 5 of
   the diagonal is the key identifier.

5. **Wave 5 validation test:** If a market makes a new high *without* momentum
   divergence on RSI, the prior high is unlikely to be a completed Wave 5. EWF
   uses this explicitly:
   > "When Nasdaq reached all-time highs without momentum divergence, with the RSI
   > showing its strongest momentum peak at the same time the Index made its all-time
   > high, it could be concluded that the previous all-time high was unlikely to be
   > wave V."

#### RSI as Structure Discriminator (Incomplete 7-Swing Test)

Beyond wave-5 detection, EWF uses RSI to determine whether a structure is a
complete 5-wave impulse or an incomplete 7-swing corrective:

> "RSI divergence is used to check if an instrument is in wave 5, and also to
> check if the structure is an incomplete 7 swing structure. Impulse structures
> should end with RSI divergence and corrective structures should end without
> RSI divergence."

RSI period: the standard 14-period RSI is the implied default; no proprietary
period is disclosed publicly.

Sources:
- https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/
- https://elliottwave-forecast.com/trading/elliott-wave-divergence-macd-rsi-fibonacci/
- https://elliottwave-forecast.com/elliottwave/what-is-the-relative-strength-index-rsi/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-indices-ending-5-waves-not/

---

### 2.7 Awesome Oscillator and MACD

EWF uses the Awesome Oscillator (AO) alongside RSI for momentum confirmation:

- **Strong AO expansion** during Wave 3 (both bullish histogram bars) confirms
  the impulse is in its strongest phase.
- **AO histogram weakening or negative divergence** signals Wave 5 approaching
  completion.
- **AO zero-line cross** after Wave 5 can confirm the impulse is over.

MACD is used similarly:
> "MACD, RSI, Fibonacci, ADX, and Stochastic are the indicators that work best
> with Elliott Wave analysis."

The Fractal Indicator is also mentioned as a secondary tool for identifying
wave turning points.

Sources:
- https://elliottwave-forecast.com/elliottwave/mastering-elliott-wave-pattern-recognition-in-trading/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-tools-and-indicators/

---

### 2.8 WXY Double-Three vs ABC — EWF's Preferred Count

EWF explicitly favors **WXY (Double Three)** labeling over **ABC (Zigzag)** as
the default interpretation of three-wave counter-trend moves.

#### Why WXY is Preferred

> "WXY (Double Three) pattern is more common than ABC (Zig-Zag), which is the
> reason why you don't see ABC labeling as often as WXY at EWF charts."

The argument:
- In a WXY, Wave W already subdivides in 3 waves, making it structurally impossible
  for the pattern to "become" a wave 3 of an impulse. The trader knows the first leg
  is corrective.
- In an ABC (zigzag), Wave A subdivides in 5 waves — identical to an impulsive
  Wave 1. There is more ambiguity about whether a 5-wave A is part of a correction
  or the start of an impulse.

> "WXY is a better corrective pattern to trade than ABC, as the pattern reduces the
> risk that the correction will become an impulse."

#### WXY Fibonacci Targets

- Wave Y ends at **100%–123.6%** of Wave W (measured from the end of Wave X)
  as the typical Blue Box target zone.
- Invalidation: Wave Y extends beyond **161.8%** of Wave W.

#### Connector Wave X

Wave X separates W from Y and can be *any* corrective structure: zigzag, flat,
triangle, double-three, or triple-three. X retraces 50%–85.4% of Wave W.

Triple Three (WXYXZ = 11-swing structure):
- Wave Z ends at 100%–123.6% of Wave W.
- The second X retraces Wave Y by 50%–85.4%.

Sources:
- https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/
- https://elliottwave-forecast.com/elliottwave/difference-wxy-abc-structure/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-pattern-double-structure/
- https://elliottwave-forecast.com/elliottwave/double-three-including-triangle-connector/

---

### 2.9 Wave Entry, Exit, and Stop-Loss Protocol

EWF's mechanical trading protocol, assembled from public articles:

#### Entry

**Standard corrective setup (Wave 2/B/X entry):**
1. Wait for a prior 1/A/W wave to complete (confirm 5 sub-waves or 3 sub-waves
   depending on label).
2. Measure the 50%–85.4% retracement zone of the prior swing for a Wave 2
   (or 50%–61.8% for a shallow Wave 4).
3. Enter long (or short) as price enters the retracement zone.

**Blue Box corrective sequence setup:**
1. Identify 3, 7, or 11 swing corrective count within a bullish/bearish sequence.
2. Measure the 100%–161.8% extension of the first corrective leg (the Blue Box).
3. Enter at the **100% level** (top of Blue Box for a bull trade, bottom for a bear
   trade).
4. Stop below/above the **161.8% extension**.

**WXY setup:**
> "A trader who wants to buy a corrective pattern WXY can try to buy wave Y at the
> 100% of wave W with stop loss below 161.8%."

#### Stop Loss

> "Stop losses should always be based on technical invalidation levels rather than
> random price distances."

Key invalidation anchors:
- Wave 2 trade: stop beyond 100% retracement of Wave 1 (rule: wave 2 cannot
  exceed wave 1's origin).
- Blue Box trade: stop beyond the 161.8% extension.
- Wave 4 trade: stop below Wave 1's high (no overlap rule).
- Risk capped at maximum **2% of capital** per trade.

#### Exit / Target

> "Target areas to exit a position is best to exit all of a position at the equal
> legs to 1.236% area Fibonacci extension area of the wave 1 or wave A measured
> against the high or low of the larger degree correction."

General target hierarchy:
1. First target: 123.6% extension of Wave 1 (from end of Wave 2)
2. Second target: 161.8% extension (Wave 3 typical)
3. Final target: Equal legs (100%) or 123.6% for the overall cycle completion

**Risk-free trigger:** Once price bounces 50% of the initial move from the Blue Box
entry, move stop to breakeven.

#### Timeframe Guidance

> "Elliott Wave theory is extremely hard to use for intraday trades, and much
> better accuracy is found by changing trades from 1–3 days to 5–60 days."

EWF recommends 4H, Daily, and Weekly timeframes for primary analysis.
Analysis is performed **top-down**: Weekly → Daily → 4H → 1H.

Sources:
- https://elliottwave-forecast.com/elliottwave/how-to-trade-forex-with-elliott-wave/
- https://elliottwave-forecast.com/elliottwave/how-to-trade-wave-2-or-b-wave-corrections-in-any-elliott-wave-cycle-or-degree/
- https://elliottwave-forecast.com/trading/stop-loss-trading-strategies/
- https://elliottwave-forecast.com/elliottwave/where-to-place-stop-losses-using-the-elliott-wave-principle/

---

### 2.10 Multi-Timeframe Approach and Wave Degree Labeling

EWF uses the standard Elliott Wave degree hierarchy but emphasizes top-down
analysis as the *only* valid approach:

> "Analysts recommend analyzing Elliott Wave charts from the higher time frame to
> the lower time frame (weekly → daily → 4 hour → 1 hour)."

Wave degrees and their typical timeframes at EWF:

| Degree | Typical Timeframe | Notation |
|---|---|---|
| Grand Supercycle | Monthly / multi-century | (I)(II)(III) |
| Supercycle | Monthly / multi-decade 40–70y | (I)(II) |
| Cycle | Monthly / multi-year | I II III |
| Primary | Weekly | ((I)) ((II)) |
| Intermediate | Daily | (I) (II) |
| Minor | 4H | I II |
| Minute | 1H | ((i)) ((ii)) |
| Minuette | 15m | (i) (ii) |

**Nesting:** EWF uses the term "nesting" to describe the fractal extension of an
impulse. A "quadruple nest" (e.g., wave ((3)) of III of (III) of Cycle III) signals
an extremely powerful continuation move — a key pattern EWF highlights for high-
conviction long setups.

**Degree consistency rule:** Once the higher timeframe is labeled, lower timeframe
waves must be consistent sub-divisions of those labels.

Sources:
- https://elliottwave-forecast.com/stock-market/spx-elliott-wave-weekly-inflection-area/
- https://elliottwave-forecast.com/video-blog/reading-elliott-wave-chart-seminar-2/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-theory/

---

### 2.11 Corrective Patterns — EWF's Full Taxonomy

EWF covers all standard corrective patterns with specific Fibonacci relationships:

#### Zigzag (ABC, 5-3-5) — 3 swings

- Wave B retraces 50%–61.8% of Wave A
- Wave C = 100%–123.6% of Wave A (normal); 123.6%–161.8% (expanded)
- Blue Box for the end of a zigzag: 100%–123.6% extension zone

If Wave C exceeds 161.8% of Wave A → structure may be a Wave 3 of an impulse, not
a correction. Major invalidation signal.

#### Flat Corrections (3-3-5) — 3 swings

Three sub-types:
1. **Regular Flat**: Wave B ends near start of Wave A; Wave C slightly beyond Wave
   A's end.
2. **Expanded / Irregular Flat**: Wave B extends beyond Wave A's origin to ~123.6%
   of A. Wave C ends beyond Wave A's low/high at 123.6%–161.8% of Wave A.
3. **Running Flat**: Wave C ends without reaching Wave A's extreme — a sign of
   strong underlying trend.

Fibonacci in flats:
- Regular flat: Wave C = 61.8%–100% of Wave A
- Expanded flat: Wave C = 123.6%–161.8% of Wave A

#### Double Three (WXY) — 7 swings

The EWF-preferred corrective label (see §2.8 above). The 7-swing structure is the
most common in modern markets per EWF.

#### Triple Three (WXYXZ) — 11 swings

Three corrective patterns connected by two X-wave connectors. Signals extended
sideways markets. The 11-swing count completes the triple three.

#### Triangles (3-3-3-3-3) — 5 swings

Types: Contracting, Ascending, Descending, Running, Expanding.

**Placement rule:** Triangles appear **only** in Wave 4, Wave B, or Wave X
positions — *never* in Wave 2, Wave 1, Wave 3, or Wave 5 (exception: ending
diagonal which is a special case of Wave 5).

**Running Triangle:** Wave B exceeds the origin of Wave A. A frequent trap —
traders mistake the B breakout for a new impulse.

Sources:
- https://elliottwave-forecast.com/trading/elliott-wave-corrective-waves/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-structure-triple-three-corrections/
- https://elliottwave-forecast.com/elliottwave/measure-fibonacci-extensions-elliott-wave-flat-corrections/
- https://elliottwave-forecast.com/trading/elliott-wave-triangle-patterns-ascending-descending-contracting/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-running-triangle-2/
- https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/

---

### 2.12 Impulsive Wave Rules — EWF's Complete Set

Standard rules (EWF reaffirms all classical rules):

1. Wave 2 never retraces more than 100% of Wave 1.
2. Wave 3 is **never the shortest** of Waves 1, 3, 5.
3. Wave 4 never overlaps into Wave 1's territory (exception: diagonal).

EWF's additional conventions:

4. **Wave 3 is the most common extension** — 90% of extensions occur in Wave 3.
5. **Wave 3 minimum** = 161.8% of Wave 1; typical range: 161.8%–261.8%.
6. **RSI divergence required** at Wave 5 vs. Wave 3 (see §2.6).
7. **Motive sequence redefinition:** EWF distinguishes between an "impulse" (strict
   5-wave structure with non-overlapping waves) and a "motive sequence" (which can
   include a leading diagonal as Wave 1 and still trend upward). They observe that
   in modern markets trends frequently unfold in 3-wave (corrective) structures
   moving in the direction of the dominant sequence.

#### Nesting (Nested Impulses)

A nested impulse occurs when Wave 1 of a larger degree itself contains a completed
5-wave structure, and Wave 2 corrects it, setting up Wave 3 of the larger degree.
When this nesting occurs at multiple degrees simultaneously, EWF labels it a
"quadruple nest" and treats it as an extremely bullish (or bearish) signal with
the highest continuation probability.

#### Ending Diagonal (Wave 5 / C)

- Subdivides 3-3-3-3-3 (unlike regular impulse: 5-3-5-3-5)
- Appears only in Wave 5 or Wave C positions
- Characterized by overlapping waves in a contracting wedge
- Signals trend exhaustion and probable sharp reversal
- Confirmed by strong RSI divergence between Wave 3 and Wave 5 sub-waves

#### Leading Diagonal (Wave 1 / A)

- Subdivides 5-3-5-3-5 or 3-3-3-3-3
- Appears in Wave 1 or Wave A positions
- Wave 1 and Wave 4 typically overlap
- Confirmed by RSI divergence between Wave 3 and Wave 5 within the diagonal
- Signals early-stage trend (often followed by a sharp Wave 2 correction)

Sources:
- https://elliottwave-forecast.com/elliottwave/impulsive-5-wave-structure-ground-rules/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/
- https://elliottwave-forecast.com/elliottwave/introduction-diagonals/
- https://elliottwave-forecast.com/elliottwave/never-break-3-rules-successful-elliott-wave-trader/
- https://elliottwave-forecast.com/elliottwave/elliott-wave-extensions/

---

### 2.13 Top 10 Tools — EWF's Public List (2026)

From their explicitly titled article:

1. **Fibonacci Retracement** — projecting corrections
2. **Fibonacci Extension** — projecting impulse targets; 1.618 especially for Wave 3
3. **RSI (Relative Strength Index)** — divergence at Wave 5; structure validation
4. **Elliott Wave Oscillator (EWO = MACD 5/34/5 on close)** — momentum confirmation
5. **Awesome Oscillator (AO)** — Wave 3 confirmation; Wave 5 divergence
6. **Blue Boxes** — high-probability reversal/continuation zone entries
7. **Fractal Indicator** — wave turning points
8. **MACD** — divergence and trend confirmation
9. **ADX** — trend strength; impulse vs. corrective context
10. **Stochastic** — overbought/oversold at wave extremes

Source:
- https://elliottwave-forecast.com/elliottwave/elliott-wave-tools-and-indicators/

---

### 2.14 Distribution and Correlation System (Partially Proprietary)

EWF references a "distribution system" and "currency ranking" as proprietary
additions:

> "The distribution is a system in which sequences need to keep in one direction
> not only in price, but also in momentum, with machines able to execute these
> decisions with high degrees of perfection."

> "EWF's top traders use trendlines in conjunction with the RSI indicator and
> heavily rely on the proprietary distribution system to forecast the end of a
> specific cycle."

> "We have observed the market over the years and added tools like cycles,
> distribution, correlations, ranking among currencies and sequences."

The public content does not reveal the specific mechanics of the distribution
system or the currency ranking algorithm. It appears to involve:
- Tracking RSI momentum across instruments simultaneously
- Ranking currencies by relative strength/weakness (a standard approach in forex)
- Using inter-market correlations (e.g., Oil/SPX correlation) to confirm directional
  bias

EWF also references "first-dimension" and "second-dimension" correlations:
- First dimension: two instruments moving in the same direction
- Second dimension: two instruments moving in opposite directions but their swings
  are still correlated in structure/time

Source:
- https://elliottwave-forecast.com/trading/market-nature-art-trading/
- https://elliottwave-forecast.com/commodities/oil-and-spx/

---

## 3. Which EWF Ideas Are Implementable in Our Engine

The Ewace_2026 engine operates on deterministic, causal rules applied to OHLCV
data. Below is an analysis of each EWF concept against our design constraints
(deterministic, no lookahead, pure stdlib/numpy-compatible, separation of
structure/measurement/confirmation).

### 3.1 Blue Box — Fibonacci Extension Confluence Zone (HIGH priority)

**Implementable: Yes, fully mechanical.**

The Blue Box is a straightforward Fibonacci extension computation:
1. Identify swing A (from pivot_high to pivot_low, or vice versa)
2. Identify swing B (the retracement)
3. Compute 100% extension = B + (A_magnitude) in the original A direction
4. Compute 161.8% extension = B + (1.618 × A_magnitude)
5. The Blue Box is the price range [100%, 161.8%] extension

Our `wavelib/toolkit.py` already has `project_wave5` (Fibonacci extension). The
Blue Box is essentially an extension zone off a corrective leg. We could add:

```python
def blue_box_zone(swing_a_start, swing_a_end, swing_b_end):
    """
    Returns (lower, upper) price bounds of the EWF Blue Box.
    For a bullish Blue Box (correction expected to end, price to rise):
      swing_a_start > swing_a_end (decline), swing_b_end > swing_a_end (bounce).
    lower = swing_b_end - 1.000 * abs(swing_a_end - swing_a_start)
    upper = swing_b_end - 1.618 * abs(swing_a_end - swing_a_start)
    """
    mag = abs(swing_a_end - swing_a_start)
    direction = 1 if swing_a_start > swing_a_end else -1
    lower = swing_b_end + direction * mag          # 100% extension
    upper = swing_b_end + direction * 1.618 * mag  # 161.8% extension
    return (min(lower, upper), max(lower, upper))
```

This maps directly onto our existing Fibonacci infrastructure. The Blue Box zone
can serve as a **zone-of-interest** output for `confluence.score_reversal()` —
specifically as a structural strand indicating the price is within a computed
reversal zone.

**Suggested integration point:** `wavelib/toolkit.py` — add `blue_box_zone()` as
a new measurement function alongside the existing `fibonacci_retracements()`.

### 3.2 Swing-Sequence Counting (3/7/11 vs 5/9/13) (HIGH priority)

**Implementable: Yes, with moderate complexity.**

Our `wavelib/rules.py` already performs ZigZag pivot detection and wave labeling.
The swing-sequence count is an abstraction layer *above* specific wave labels —
it counts alternating pivot legs regardless of whether they're part of an impulse
or corrective structure.

Proposed addition to `wavelib/automation.py`:

```python
def count_swing_sequence(pivots):
    """
    Count alternating swings from a list of (price, direction) pivot pairs.
    Returns (count, sequence_type) where sequence_type is 'impulsive' or 'corrective'.
    Impulsive: 5, 9, 13, 17...  Corrective: 3, 7, 11, 15...
    """
    n = len(pivots)
    if (n - 5) % 4 == 0:  # 5, 9, 13...
        return n, 'impulsive'
    elif (n - 3) % 4 == 0:  # 3, 7, 11...
        return n, 'corrective'
    else:
        return n, 'incomplete'
```

The "incomplete sequence" flag is the trading signal: if a corrective swing count
stands at 5 (odd for the series 3, 7, 11…), mark the instrument as having an
"incomplete sequence" calling for one more leg. This is a deterministic, causal
computation on our existing ZigZag pivot output.

**Suggested integration point:** Add `swing_sequence_count()` to `wavelib/automation.py`
and surface its output in `label_and_validate()` results. The incomplete-sequence
flag (swing_count = 5 corrective swings) maps onto our confluence framework as an
additional "structural readiness" strand.

### 3.3 RSI Divergence at Wave 5 (ALREADY PARTIALLY IMPLEMENTED)

**Implementable: Yes — we already have swing-pivot RSI divergence in `confluence.py`.**

EWF's specific Wave 5 RSI divergence rule is:
- Price makes a new high (Wave 5 > Wave 3 high) while RSI makes a *lower* high
  at Wave 5 vs. Wave 3.

Our `confluence.py` implements RSI divergence detection. The refinement needed is
to make it **wave-specific**: check divergence at the *labeled* Wave 5 vs. Wave 3
pivot rather than at any arbitrary swing pair.

EWF's additional rule — impulse ends with divergence, correction ends without —
is implementable as a boolean gate:
- If the last labeled structure is an impulse candidate AND RSI shows divergence at
  the terminal pivot → impulse-end signal confirmed.
- If the last labeled structure is a corrective candidate AND RSI does NOT show
  divergence → corrective-end signal confirmed.

**Suggested integration point:** Extend `confluence.py`'s existing RSI divergence
strand to be wave-label-aware. Pass the wave label context from `automation.py`
into `score_reversal()`.

### 3.4 Equal-Legs (100% Extension) as Default Corrective Target

**Implementable: Yes, trivial computation.**

Equal legs (A=C or W=Y) is the 100% Fibonacci extension — already within our
`fibonacci_retracements()` infrastructure. EWF elevates this to the *primary*
corrective target (center of the Blue Box zone).

In our engine: whenever we compute the end of a corrective leg, project equal legs
as a candidate completion zone. This is already partially done in `toolkit.py`
(`project_wave5` uses Fibonacci ratios). Explicitly naming the 100% extension as
an "equal-legs target" and including it as a reversal-zone output would align with
EWF's framework.

### 3.5 WXY Label Preference Over ABC

**Implementable: Partially — guidance for our labeling engine.**

EWF's preference for WXY over ABC has a mechanical justification: if the first
leg of a 3-swing correction has 3 internal sub-waves (making it a W), label the
whole correction as WXY. If the first leg has 5 sub-waves, it could be ABC or the
start of an impulse — more ambiguous.

Our `rules.py` already tracks internal sub-wave counts. We could add a heuristic:
- If 3-swing correction detected AND first leg has 3 sub-waves → label WXY,
  apply 100%–123.6% Y target extension.
- If 3-swing correction detected AND first leg has 5 sub-waves → label ABC,
  apply 100%–123.6% C target extension (same math, different semantic).

Both are low-risk additions since the Fibonacci math is identical. The labeling
distinction helps with communicating to the user which structure is more likely
to stay corrective.

### 3.6 Directional Sequence Stamp (Right Side Logic)

**Implementable: Yes, as a meta-state on top of the wave count.**

The Right Side tag is essentially:
- **Bullish stamp:** the instrument has completed an impulsive sequence up and is in
  a corrective pullback → bias is long.
- **Bearish stamp:** the instrument has completed an impulsive sequence down and is
  in a corrective bounce → bias is short.
- **Neutral:** sequence is ambiguous.

This is derivable from our existing `label_and_validate()` output. After labeling,
check whether the highest-confidence candidate shows an upward-trending impulsive
sequence (bullish stamp) or downward-trending one (bearish stamp).

**Suggested integration:** Add `directional_bias()` function to `automation.py`
that derives "bullish sequence / bearish sequence / unclear" from the current wave
count and degree hierarchy.

### 3.7 Connector Wave X Fibonacci Retracement (50%–85.4%)

**Implementable: Yes.**

When a WXY is identified, the X connector should retrace 50%–85.4% of Wave W.
This is a simple range check on the observed retracement of the X wave. Currently
our engine validates whether a correction stays within bounds; extending this to
explicitly flag when an X wave retracement is outside [50%, 85.4%] would improve
WXY identification accuracy.

---

## 4. What Is Genuinely Proprietary or Discretionary

The following EWF elements are **not implementable** in a purely mechanical engine,
or are opaque enough that they cannot be reproduced from public information:

### 4.1 Distribution System

The "distribution system" — described as tracking whether sequences maintain
directional consistency in both price and momentum — is not publicly specified
with enough precision to implement. The currency ranking system is also proprietary.
These appear to be proprietary overlays built from years of in-house research.

### 4.2 "High-Frequency Trading Integration" Claims

EWF's framing that their Blue Boxes correspond to where HFT algorithms cluster
orders is a marketing claim, not a specification. The Blue Box is computable
mechanically; the HFT alignment claim is unverifiable and unfalsifiable from
public data.

### 4.3 Aggregate Win Rate Statistics

EWF does not publish aggregate statistics on Blue Box win rates, drawdown periods,
or risk-adjusted returns. The "Blue Box Wins" page shows cherry-picked successful
examples. No independent third-party audit of their signal performance is publicly
available. Reviews on Trustpilot/ForexFactory include critics who note that wave
counts are frequently redrawn when they fail.

### 4.4 Degree of Discretion in Real-Time Labeling

Despite EWF's framing as "mechanical" and "objective," real-time wave labeling
involves substantial discretion:
- Choosing between ABC and WXY when the first leg is ambiguous
- Determining when a corrective sequence is "complete" vs. "extending"
- Selecting which of several valid wave counts to display as the "preferred"

The Right Side tag, while presented as objective, reflects the analyst's preferred
count — which can and does change when price action invalidates it. This is the
fundamental limitation of EWT applied to live markets.

### 4.5 Multi-Market Correlation System

EWF's use of inter-market correlations (Oil/SPX, currency pair rankings, etc.)
as a directional filter is described but not mechanically specified. The "second-
dimension correlation" (instruments moving in opposite directions with correlated
swings) concept would require a custom implementation not described in public
materials.

---

## 5. Gaps — Content Not Retrievable

The following topics were searched but returned insufficient detail:

1. **Exact EWO (Elliott Wave Oscillator) parameters** — the specific MACD settings
   (implied to be 5/34 close, the standard EWO) are not confirmed in public text.

2. **The eBookFFF.pdf content** — HTTP 403 blocked retrieval. The PDF title
   suggests it covers the FFF (Forex Forecast Framework) but content is unknown.

3. **Proprietary pivot system details** — mentioned repeatedly as one of EWF's
   core differentiators but never defined mechanically.

4. **Distribution system algorithm** — described qualitatively, never specified.

5. **Currency ranking mechanics** — qualitatively described as relative strength
   of currencies, not specified.

6. **Members-only tools** — live chart rooms, strategy-of-the-day, video updates,
   and the real-time signal service are behind a subscription paywall.

7. **Backtesting evidence** — no publicly available backtest reports, Sharpe
   ratios, drawdown statistics, or out-of-sample performance data exist for any
   EWF strategy. The Blue Box approach is presented via case studies only.

8. **Specific TradingView indicators** — EWF mentions TradingView as a platform
   but does not publish their proprietary indicators publicly.

---

## 6. Synthesis: Fit with Ewace_2026 Architecture

The Ewace_2026 engine's design separates **structure** (rules.py), **measurement**
(toolkit.py), and **confirmation** (confluence.py). EWF's methodology maps cleanly
onto this:

| EWF Concept | Ewace_2026 Layer | Status |
|---|---|---|
| Swing sequence count (3/7/11 vs 5/9/13) | `automation.py` | New function needed |
| Blue Box zone computation | `toolkit.py` | New function needed |
| Equal legs (100% extension) | `toolkit.py` | Already partially present |
| WXY vs ABC label preference | `rules.py` | Heuristic refinement |
| RSI divergence at labeled Wave 5 | `confluence.py` | Extend existing |
| Right Side / directional bias | `automation.py` | New function needed |
| X wave 50–85.4% retracement check | `rules.py` | Add validation rule |
| Fibonacci ratio table (full EWF set) | `toolkit.py` | Add constants |
| Corrective-ends-without-divergence gate | `confluence.py` | New gate |

The integration with `chakra_quant`'s cycle seam (`wavelib/cycle_seam.py`) maps to
EWF's "cycles and time" component — the 7th confluence strand (§2 of CLAUDE.md).

**Critical caution:** EWF's swing-sequence counting (§2.3) and the Blue Box (§2.2)
are mathematically simple but require a well-calibrated ZigZag pivot detector as
input. The quality of the pivot detection is the primary driver of whether these
rules add signal or noise. Our existing ZigZag in `toolkit.py` and the automation
layer's multi-scale approach are appropriate foundations.

---

## 7. Sources

All URLs harvested via site-scoped web searches. Direct page content not available
due to HTTP 403 anti-bot protection; summaries are derived from Google-indexed
previews.

- [Top 10 Essential Tools and Indicators for Mastering Elliott Wave Analysis in 2026](https://elliottwave-forecast.com/elliottwave/elliott-wave-tools-and-indicators/)
- [Elliott Wave Theory | Rules, Guidelines & Structures](https://elliottwave-forecast.com/elliott-wave-theory/)
- [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)
- [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)
- [The Right Side: Only Way to Survive in the Trading World](https://elliottwave-forecast.com/trading/right-side-helps-survival-trading-world/)
- [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)
- [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)
- [Fibonacci Retracement, Extension & Trading Strategies](https://elliottwave-forecast.com/trading/fibonacci-retracement-and-fibonacci-extension/)
- [Fibonacci Retracement in Elliott Wave Theory - Complete Trading Guide](https://elliottwave-forecast.com/trading/fibonacci-retracement-elliott-wave-guide/)
- [How to Measure Fibonacci Extensions in Elliott Wave Flat Corrections](https://elliottwave-forecast.com/elliottwave/measure-fibonacci-extensions-elliott-wave-flat-corrections/)
- [Importance of an Elliott Wave ZigZag Fibonacci Extension](https://elliottwave-forecast.com/elliottwave/importance-of-an-elliott-wave-zigzag-fibonacci-extension/)
- [How Momentum Indicator (RSI) is Used with Elliott Wave](https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/)
- [Elliott Wave Analysis with MACD, RSI & Fibonacci Divergence](https://elliottwave-forecast.com/trading/elliott-wave-divergence-macd-rsi-fibonacci/)
- [How to Trade Forex with Elliott Wave: The Complete Guide](https://elliottwave-forecast.com/elliottwave/how-to-trade-forex-with-elliott-wave/)
- [How to Trade Wave 2 or B Wave Corrections](https://elliottwave-forecast.com/elliottwave/how-to-trade-wave-2-or-b-wave-corrections-in-any-elliott-wave-cycle-or-degree/)
- [Best Stop Loss Strategies For Trading](https://elliottwave-forecast.com/trading/stop-loss-trading-strategies/)
- [Where to Place Stop Losses Using the Elliott Wave Principle](https://elliottwave-forecast.com/elliottwave/where-to-place-stop-losses-using-the-elliott-wave-principle/)
- [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)
- [ABC and WXY: difference between both structures](https://elliottwave-forecast.com/elliottwave/difference-wxy-abc-structure/)
- [Elliott Wave Pattern (Double Three WXY) Structure](https://elliottwave-forecast.com/elliottwave/elliott-wave-pattern-double-structure/)
- [Double Three with a Triangle in the Connector Wave](https://elliottwave-forecast.com/elliottwave/double-three-including-triangle-connector/):
- [Mastering Triple Three Corrections in Elliott Wave Theory](https://elliottwave-forecast.com/elliottwave/elliott-wave-structure-triple-three-corrections/)
- [Elliott Wave Corrective Waves: Zigzag, Flat, Triangle Patterns](https://elliottwave-forecast.com/trading/elliott-wave-corrective-waves/)
- [Three Types of Elliott Wave Flat Corrections](https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/)
- [Expanded / Irregular Flat Elliott Wave Structure](https://elliottwave-forecast.com/elliottwave/expanded-irregular-flat-elliott-wave-structure/)
- [Elliott Wave Triangle Structure](https://elliottwave-forecast.com/elliottwave/elliott-wave-triangle-structure/)
- [Running Triangle and how they are different to regular Triangles](https://elliottwave-forecast.com/elliottwave/running-triangle-and-how-they-are-different-to-regular-triangles/)
- [Elliott Wave Triangle Patterns: Ascending, Descending & Contracting](https://elliottwave-forecast.com/trading/elliott-wave-triangle-patterns-ascending-descending-contracting/)
- [Ending Diagonal in Elliott Wave – Pattern & Trading Guide](https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/)
- [Introduction to Diagonals - Part 1](https://elliottwave-forecast.com/elliottwave/introduction-diagonals/)
- [Introduction to Diagonals - Part 2](https://elliottwave-forecast.com/elliottwave/introduction-diagonals-part-2/)
- [Elliott Wave Diagonal Patterns Explained: Leading & Ending Diagonals](https://elliottwave-forecast.com/trading/leading-and-ending-diagonals/)
- [Elliott Wave Impulse Pattern: How to Identify the 5 Wave Structure](https://elliottwave-forecast.com/elliottwave/impulsive-5-wave-structure-ground-rules/)
- [Elliott Wave Extensions in a 5-Wave Move](https://elliottwave-forecast.com/elliottwave/elliott-wave-extensions/)
- [Never break these 3 rules to be a successful Elliott Wave Trader](https://elliottwave-forecast.com/elliottwave/never-break-3-rules-successful-elliott-wave-trader/)
- [Equal Legs: What does it mean?](https://elliottwave-forecast.com/elliottwave/equal-legs/)
- [Did you know what the meaning of term Equal Legs is?](https://elliottwave-forecast.com/elliottwave/equal-legs-elliotts-wave-theory/)
- [Elliott Wave Theory and High Frequency Trading](https://elliottwave-forecast.com/elliottwave/the-elliott-wave-theory-and-high-frequency-trading/)
- [High Frequency Trading: Has The Market Really Changed?](https://elliottwave-forecast.com/elliottwave/high-frequency-trading-has-the-market-really-changed/)
- [Market Nature And The Art Of Trading It](https://elliottwave-forecast.com/trading/market-nature-art-trading/)
- [Oil and SPX simple correlation using Elliott wave cycles](https://elliottwave-forecast.com/commodities/oil-and-spx/)
- [CADJPY Elliott Wave: Blue Box Buy Setup Explained](https://elliottwave-forecast.com/forex/cadjpy-elliott-wave-blue-box-buy-setup/)
- [S&P 500 (SPX) Elliott Wave: Buying the Dips in a Blue Box](https://elliottwave-forecast.com/stock-market/sp-500-spx-elliott-wave-buying/)
- [DAX Elliott Wave: Buying the Dips at the Blue Box Area](https://elliottwave-forecast.com/trading/dax-elliott-wave-buying-dips-blue-box/)
- [Microsoft (MSFT) Up 27% Since April Entry at the Blue Box Area](https://elliottwave-forecast.com/stock-market/microsoft-msft-april-entry-blue-box/)
- [AMD Delivers 25%+ Rally Off Our Blue Box Entry](https://elliottwave-forecast.com/stock-market/amd-delivers-25-rally-off-our-blue-box-entry/)
- [Bitcoin BTCUSD gained 50% from our buying zone](https://elliottwave-forecast.com/cryptos/btcusd-elliott-wave-buying-blue-box/)
- [Elliottwave-Forecast.com Official Thread - Forex Factory](https://www.forexfactory.com/thread/528784-elliottwave-forecastcom-official-thread-w-analysis-blogs)
- [Elliott Wave Forecast Reviews - Traders Union (4.6/5)](https://tradersunion.com/reviews/elliottwave-forecast-com/)

---

*Document generated 2026-06-06. Based on 26 web search queries against
elliottwave-forecast.com public content. Direct page access blocked (HTTP 403).
No commitment from Ewace_2026 to implement any EWF concept without passing
the engine's own validation gates.*
