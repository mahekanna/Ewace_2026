# 01 — Classic Elliott Wave Theory: Rules, Guidelines, and wavelib Audit

**Scope:** Classic Elliott Wave per the Frost & Prechter lineage — impulse hard rules,
probabilistic guidelines, all correction pattern families, diagonals, the degree hierarchy,
and Fibonacci wave relationships. NeoWave (Neely) terminals, NeoWave-specific channeling,
and the Neely monowave/polywave construction are out of scope here; see `02_neowave_neely.md`
for those topics.

**Status:** Research reference document. Not investment advice.

---

## 1. Scope & Sources

This document covers:

1. The three inviolable hard rules for impulse waves and the structural logic behind each.
2. Probabilistic guidelines: extension, alternation, equality, depth bands, wave-3 Fibonacci,
   channeling, and wave personality.
3. All correction patterns: zigzag (5-3-5), flat family (3-3-5) with exact B- and C-wave
   proportion conditions, triangles (3-3-3-3-3), and combinations (double/triple three).
4. Diagonals: leading (wave 1/A) vs ending (wave 5/C), contracting vs expanding, sub-wave
   structures, legal wave 4/wave 1 overlap.
5. The degree hierarchy: all nine levels, notation conventions, and the gap in `wavelib`.
6. Fibonacci wave relationships: retracements (.382/.5/.618/.786) and extensions (1.272/1.618/
   2.618).

Cross-references:
- Ending-diagonal-as-NeoWave-terminal and the 2-4/1-3 NeoWave channeling construction order:
  see `02_neowave_neely.md`.
- `wavelib/rules.py` is audited in §3.

### Primary references

- Frost, A.J. & Prechter, R.R. *Elliott Wave Principle: Key to Market Behavior*, 10th ed.,
  New Classics Library, 2005. (Canonical primary source.)
  PDF via investmenttheory.org:
  https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf
- Elliott Wave International — Waveopedia (Flats, Diagonals, Triangles, Combinations,
  Channeling, Wave Personality):
  https://www.elliottwave.com/waveopedia/
- StockCharts ChartSchool — "Identifying Elliott Wave Patterns" and "Guidelines for Applying
  Elliott Wave Theory":
  https://chartschool.stockcharts.com/table-of-contents/market-analysis/elliott-wave-analysis-articles/identifying-elliott-wave-patterns
- Wikipedia — "Elliott Wave Principle":
  https://en.wikipedia.org/wiki/Elliott_wave_principle
- EW Forecast — "Elliott Wave Theory | Rules, Guidelines & Structures":
  https://elliottwave-forecast.com/elliott-wave-theory/
- EW Street — "Elliott Wave Theory: The Complete Guide (2026)":
  https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/
- EW Monitor — "Elliott Wave Theory: Everything You Need to Know":
  https://elliottwavemonitor.com/elliott-wave-theory/
- Bullwaves — "Simple Elliott Wave Correction Patterns":
  https://bullwaves.org/complete-guide-elliott-wave-correction-patterns/
- EWM Interactive — "Recognize the Leading Diagonal Pattern":
  https://ewminteractive.com/recognize-leading-diagonal-pattern
- FBS — "Double Three and Triple Three Patterns":
  https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns
- FBS — "Fibonacci Ratios and Impulse Waves":
  https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275
- Market Oracle — "Channeling Technique with Elliott Wave":
  https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/
- Forex Training Group — "Characteristics and Personalities of Elliott Waves":
  https://forextraininggroup.com/characteristics-and-personalities-of-elliott-waves/
- Banks & Bankers — "Flat Elliott Wave: Complete Beginner's Guide":
  https://banksandbankers.com/flat-elliott-wave-beginners-guide/
- EW Dynamics — "Comprehensive Guide to Elliott Wave Theory":
  https://elliottwavedynamics.com/comprehensive-guide-to-elliott-wave-theory/
- Price Action Help — "Elliott Wave Theory — Revised Rules and Guidelines":
  https://priceactionhelp.com/elliott-wave
- LitaFinance — "Prechter Wave Degrees and Alternation Guidelines":
  https://www.litefinance.org/blog/for-professionals/market-wave-theory-by-robert-prechter-part-2-wave-degrees-and-more-guidelines-of-wave-alternation/
- Elliott Wave Insight — "Elliott Wave Degrees & Labeling":
  https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/
- Yet Another EW Analysis Blog — "Wave Labels":
  https://yaewab.blogspot.com/p/wave-labels.html
- EBC — "How Do Ending Diagonals Fit Into Your Trading Strategy?":
  https://www.ebc.com/forex/how-do-ending-diagonals-fit-into-your-trading-strategy

---

## 2. Theory

### 2.1 The Three Inviolable Hard Rules

Every valid impulse wave (motive five-wave sequence in the direction of the one-larger-degree
trend) must satisfy all three rules. A single failure invalidates the label.
(Frost & Prechter, *Elliott Wave Principle*, Ch. 1;
https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf;
Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle)

#### Rule 1 — Wave 2 never retraces more than 100% of Wave 1

**Exact threshold:** The end of wave 2 must remain strictly above (in a bull impulse) or
below (in a bear impulse) the **origin** of wave 1 — i.e., wave 2 must not cross the
starting price of the entire impulse.

**Why this rule exists:** Wave 2 is a corrective retracement against the first directional
leg. If it erases all of wave 1 and penetrates its start, the sequence is no longer moving
net in the impulse direction; the entire five-wave construction collapses and the count must
be relabeled. The rule operationalises the minimum condition for calling the prior leg
"wave 1" at all: the subsequent counter-move must leave some net progress intact.
(EW Forecast https://elliottwave-forecast.com/elliott-wave-theory/;
Price Action Help https://priceactionhelp.com/elliott-wave)

**Typical depth:** Wave 2 most often retraces 50%–61.8% of wave 1 (Fibonacci .5 and .618
are the high-probability targets). Retracements of 76.4% or even 85.4% are seen but
uncommon. Anything approaching 99% is technically valid yet extremely rare; treat as a
warning flag that the count may be wrong.

#### Rule 2 — Wave 3 is never the shortest of waves 1, 3, and 5

**Exact threshold:** `length(wave 3) > length(wave 1)` OR `length(wave 3) > length(wave 5)`
— equivalently, wave 3 must not be shorter than *both* other motive waves simultaneously.
(Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle;
EW Street https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)

**Why this rule exists:** Wave 3 represents the heart of the trend — the phase where the
original thesis is recognised by the broadest participation and momentum is strongest. A
third wave shorter than both waves 1 and 5 would imply an irrational market structure:
the high-confidence, high-participation leg is also the weakest, contradicting the
psychological logic of mass herding. In practice wave 3 is almost always the *longest* of
the three motive legs, but the rule only forbids it from being the *shortest*.

Note: this rule applies exclusively to motive waves. In a diagonal (leading or ending),
wave 3 is only forbidden from being the shortest, not required to be the longest; the
contracting wedge shape naturally produces progressively shorter legs.

#### Rule 3 — Wave 4 does not enter the price territory of Wave 1

**Exact threshold (non-diagonal):** The extreme of wave 4 (its lowest point in a bull
impulse, highest in a bear) must not penetrate the extreme of wave 1 (its top in bull,
its bottom in bear). In a bull impulse: `low(wave 4) > high(wave 1)`.
(Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle;
EW Street https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)

**Why this rule exists:** The price territory of wave 1 represents the first zone of
contested ground; if wave 4 retreats into it, the structure looks like a trading range
rather than a progressive trend. The gap between the top of wave 1 and the bottom of
wave 4 (the "1-4 gap") is the visual fingerprint of a healthy impulse. Violation means
the move is either a diagonal or not an impulse at all. **Exception:** this rule is
explicitly suspended for diagonals (both leading and ending), where wave 4/wave 1 overlap
is not just permitted but expected (see §2.6).

---

### 2.2 Guidelines (Probabilistic — WARN Level, Never Invalidating)

Guidelines are tendencies observed across a large sample of wave sequences. No single
guideline violation invalidates a count; patterns are more complex and guidelines are best
used in combination.

#### Extension guideline

One, and typically only one, of the three motive waves (1, 3, or 5) extends — i.e., is
substantially longer than the other two. In equity markets, extension occurs most often in
wave 3; in commodity markets, extension in wave 5 is common; extension in wave 1 is the
rarest. An extended wave typically shows internal sub-division that is clearly visible at the
same degree — it looks like an impulse within an impulse.
(Frost & Prechter, Ch. 1; EW Monitor https://elliottwavemonitor.com/elliott-wave-theory/)

Typical magnitudes for an extended wave 3: 1.618×, 2.618×, and occasionally 3.618× the
length of wave 1 (Fibonacci extensions). A ratio ≥ 1.618 is the widely cited minimum for
calling a wave "extended."

When wave 3 is clearly extended (e.g., > 1.618× wave 1), waves 1 and 5 tend toward
equality or a .618 relationship to each other (see Equality guideline below).

#### Equality of non-extended motive waves

If one of the three motive waves extends, the remaining two tend toward price equality OR a
0.618 Fibonacci relationship to each other. This is one of Frost & Prechter's most cited
guidelines and is useful for projecting wave 5 after wave 4 completes.
Projected wave 5 = wave 4 end + length(wave 1) [equality], or + 0.618 × length(wave 3)
[Fibonacci fallback].
(Frost & Prechter, Ch. 1; EW Forecast https://elliottwave-forecast.com/elliott-wave-theory/)

#### Alternation guideline

Waves 2 and 4 tend to alternate in *form* and *depth*. If wave 2 is a sharp correction
(simple zigzag, deep), wave 4 will tend to be sideways (flat, combination, or triangle)
and shallow. Conversely, a shallow complex wave 2 suggests a sharp deep wave 4.
Alternation applies to price, time, severity, and structure.
(Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle;
EW Street https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)

Quantitative expression: the difference in retracement depths of wave 2 and wave 4 (each
measured against their prior motive leg) is typically > 15–20 percentage points. A
difference of < 10 pp is a weak alternation signal.

#### Depth bands

- **Wave 2:** Most commonly retraces 50%–61.8% of wave 1. A retracement of 38.2% is shallow
  but valid. Retracements of 76.4%–85.4% are deep but not rule violations. The key
  probability cluster is 0.5–0.618.
  (EW Dynamics https://elliottwavedynamics.com/comprehensive-guide-to-elliott-wave-theory/;
  FBS https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275)
- **Wave 4:** Most commonly retraces 23.6%–38.2% of wave 3, less often reaching 50%. Wave 4
  is characteristically shallower than wave 2, consistent with the alternation guideline.
  The 0.236 level (23.6%) is the shallowest common target; 0.382 is the median; 0.5 is the
  outer boundary under normal conditions.
  (EW Forecast https://elliottwave-forecast.com/elliott-wave-theory/)

#### Wave 3 Fibonacci to Wave 1

Wave 3 is most commonly 1.618× the length of wave 1. It can extend to 2.618× or 3.618×
in strongly trending markets. Ratios below 1.0× are unusual and should prompt re-labelling.
A ratio of 1.0× (equality) is an allowable lower bound in a non-extending wave 3 scenario.
(FBS https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275)

The `wavelib` guideline check currently uses a band of 1.3×–3.0× (`elliott_guidelines` line
145). The lower bound of 1.3× is reasonable as a WARN threshold but is a heuristic, not
canonical (the standard says 1.618× is the *typical* target; below 1.618× is possible but
unusual for an extending wave 3).

#### Channeling guideline (Frost & Prechter)

Frost & Prechter describe parallel channel lines as a primary wave-identification tool. Three
channels are used sequentially:
(Market Oracle / Algotrading-Investment
https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/;
Elliott Wave International https://www.elliottwave.com/waveopedia/channeling/)

1. **Base channel (0-2 line):** Draw through wave-0 origin and wave-2 end; place a parallel
   through the top of wave 1. Price holding above this lower line during wave 3 confirms the
   motive structure. A break below the lower line during wave 4 is a warning.
2. **Acceleration channel (1-3 line):** After wave 3, draw a line connecting tops of waves
   1 and 3; place a parallel through the bottom of wave 2. This channel forecasts the upper
   boundary for wave 5 (throw-over above it = blow-off exhaustion; fell short below it =
   truncated/weak fifth).
3. **Deceleration channel (2-4 line):** After wave 4, draw a line through the bottoms of
   waves 2 and 4; place a parallel through the top of wave 3. The upper parallel provides an
   alternative estimate of wave 5 target. This is the classic NeoWave construction-order
   channel; see `02_neowave_neely.md` for the NeoWave-specific channeling rules.

Note: `wavelib` implements `two_four_test` (2-4 line) and `throwover_test` (1-3 line) but
does NOT implement the base channel (0-2 line parallel through wave-1 top). That is a gap.

#### Wave personality and psychology

Personality descriptions (Frost & Prechter, Ch. 2;
Forex Training Group https://forextraininggroup.com/characteristics-and-personalities-of-elliott-waves/;
EW International https://www.elliottwave.com/waveopedia/wave-personality/):

| Wave | Personality / market psychology |
|------|--------------------------------|
| 1 | Tentative; difficult to identify in real time. Often looks like a normal bounce off a bottom. News is overwhelmingly negative; few buyers. Volume may or may not expand. |
| 2 | Fear and disbelief; feels like the decline is resuming. Sentiment turns bearish. Often a deep, sharp retracement. Rarely makes news; common re-entry opportunity in hindsight. |
| 3 | Strongest and longest impulse in most markets. Fundamentals improve; analysts upgrade; breadth and volume expand. "Wonders to behold" (Prechter). Least likely to be confused with anything else once underway. |
| 4 | Boringly sideways; investors "know" the trend is up but don't act. Often a flat, triangle, or combination. Less emotional than wave 2. Holds above wave 1 high (hard rule). |
| 5 | Emotionally frothy; breadth diverges (fewer stocks participating, just the big names). Volume often lower than wave 3. News is uniformly positive. Commonly produces divergences in momentum oscillators. Wave of "amateur enthusiasm." |
| A | Corrective sell-off; many still believe the prior trend will resume. Often mistaken for a normal pullback in the uptrend. Sub-divides 5-3 internally if part of a zigzag. |
| B | Counter-trend rally ("sucker rally"). Commonly produces false hope of trend resumption. Sub-divides in 3 waves. Especially treacherous in expanded flats where B exceeds prior high. |
| C | Devastating in bear markets; clearly impulsive in sub-structure (5 waves). Leaves little doubt the prior correction was more than a pullback. |

---

### 2.3 Correction Patterns

All corrections move against the one-larger-degree trend and are labelled with letters
(A, B, C or a through e for triangles, or W, X, Y, Z for combinations).

#### 2.3.1 Zigzag (5-3-5)

Structure: A (5-wave motive), B (3-wave correction), C (5-wave motive, same direction as A).

**Hard classification rules:**
- Wave A subdivides into 5 sub-waves.
- Wave B subdivides into 3 sub-waves.
- Wave B must NOT retrace more than **61.8%** of wave A. This is the principal classifier —
  a shallow B is the fingerprint of a zigzag.
  (EW Monitor https://elliottwavemonitor.com/elliott-wave-theory/;
  EW Street https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)
- Wave B cannot exceed the origin of wave A.
- Wave C must extend beyond the end of wave A (C reaches new corrective extreme).

**Proportions (guideline, not rule):**
- C is typically 61.8%–161.8% of A; equality (C = A) is common.
- Deep zigzags: C up to 200% of A has been observed.

**Double zigzag:** Two zigzags connected by an X-wave — labeled W, X, Y. Position: typically
wave 2 or wave 4. The overall correction looks "deeper" than a single zigzag.

#### 2.3.2 Flat Family (3-3-5)

All flats share a 3-3-5 internal structure: A and B each subdivide into 3 waves; C
subdivides into 5 waves. The key differentiator across subtypes is the **extent of wave B
relative to wave A** and the **extent of wave C relative to wave A**.

The minimum condition for any flat: wave B must retrace **more than 61.8%** of wave A (if
B retraces ≤ 61.8%, the pattern is a zigzag, not a flat).
(Banks & Bankers https://banksandbankers.com/flat-elliott-wave-beginners-guide/;
EW Forecast — Three Types of Flats
https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/)

Three subtypes:

**Regular flat:**
- B retraces approximately **90%–100%** of A (within the range 61.8%–100%).
- C extends to approximately the same level as the end of A; C ≈ 61.8%–100% of A.
- The overall correction ends near, but typically slightly beyond, the wave-A extreme.

**Expanded flat (also called irregular flat — the most common subtype):**
- B retraces **more than 100%** of A, typically **105%–138%** of A. The 138% level is a
  widely cited outer guideline (1.382 Fibonacci extension of A measured from the origin).
  (EW Forecast https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/)
- C extends **beyond** the end of A, typically reaching **105%–165%** of A.
- The C wave's minimum extension past the end of A distinguishes expanded from regular.
- Psychologically dangerous: B makes a new high (in a bear correction), giving the
  impression the prior trend has resumed before C drives a sharp new low.

**Running flat (rare):**
- B retraces **more than 100%** of A (like an expanded flat).
- But C **fails to reach** the end of wave A — C is truncated. The net displacement of the
  overall pattern is minimal; price "runs sideways" with a strong underlying trend.
- Running flats indicate extremely strong thrust in the prevailing trend direction; they
  appear most often within strong wave 3 sequences.
  (EW Monitor https://elliottwavemonitor.com/elliott-wave-theory/)

**Disambiguation table:**

| Subtype | B retraces A | C retraces (vs A) |
|---------|-------------|-------------------|
| Regular | 61.8%–100% | ≈ 61.8%–100% of A |
| Expanded | > 100% (typ. 105%–138%) | > 100% of A |
| Running | > 100% | < 100% of A (C truncated) |

#### 2.3.3 Triangles (3-3-3-3-3)

Structure: Five internal corrective legs labelled a, b, c, d, e, each subdividing in 3 waves.
Triangles are always corrective and appear in specific positions: wave 4, wave B, or the
final X-wave in a combination (always "penultimate" — they precede the final thrust of the
one-larger-degree structure).
(EW International — Triangles https://www.elliottwave.com/waveopedia/triangles/;
EW Forecast https://elliottwave-forecast.com/elliott-wave-theory/)

A contracting triangle is the most common. Each successive leg is shorter:
- a > b > c > d > e in absolute length.
- Two converging boundary lines: upper boundary (a-c line) and lower boundary (b-d line)
  converge to an apex.
- **Apex timing rule:** the apex of the converging lines often coincides with a turning point
  at the one-larger degree. The post-triangle thrust typically occurs when price is within
  the last 75% of the time to the apex.

**Barrier triangle:** One of the two boundary lines is horizontal (barrier), the other
converges. Can appear in wave 4 or wave B.

**Expanding triangle:** Each successive leg is *longer* than the prior — lines diverge. Less
common than contracting; more often appears in wave B.

**Thrust rule:** After any contracting or barrier triangle completes, there is a rapid thrust
in the direction of the one-larger-degree trend. The thrust is typically at least 75% and
no more than 125% of the widest leg (leg a) of the triangle.
(EW International Triangle article; Price Action Help https://priceactionhelp.com/elliott-wave)

**Wave E behavior:** Wave e commonly undershoots or overshoots the a-c boundary line —
overshoot slightly more common. This means a rigid "price must stay within the channel"
filter will incorrectly reject valid triangles.

#### 2.3.4 Combinations — Double Three and Triple Three

Combinations are horizontal corrections consisting of two or three simpler corrective
structures connected by X-waves.
(FBS https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns;
EW International https://www.elliottwave.com/waveopedia/combinations/)

**Double three (W-X-Y):**
- W: any simple corrective pattern (zigzag, flat, or triangle as the *final* component only).
  If W is the first component, it can be zigzag or flat; triangle is prohibited as W.
- X: any corrective pattern; most commonly a zigzag; must be smaller than W (guideline:
  X < 61.8% of W in price travel).
- Y: any corrective pattern including a triangle as the final component.
- The net travel of the whole W-X-Y is typically sideways relative to the prior trend.

**Triple three (W-X-Y-X-Z):**
- Three corrective structures connected by two X-waves.
- W, Y, and Z may each be a zigzag, flat, double three of lesser degree, or triangle.
- Triangle appears only as the *final* component (Z); it cannot be W or Y.
- There is never more than one zigzag in a combination.

**X-wave role and size:**
- X-waves connect the component corrections. The X-wave can be any corrective structure.
- Guideline: the net travel of one component relates to the next by equality or ×0.618.
  (EW Monitor https://elliottwavemonitor.com/elliott-wave-theory/)

---

### 2.4 Diagonals

Diagonals are five-wave motive structures that form a wedge shape. They are the only
five-wave motive patterns in which wave 4/wave 1 overlap is permitted (or, in ending
diagonals, expected).

Both types: the converging or diverging boundary lines (1-3 upper boundary, 2-4 lower
boundary) must form a clear wedge; legs must be in alternating directions.

#### 2.4.1 Ending Diagonal (wave 5 or wave C)

Position: exclusively in wave 5 of an impulse or wave C of a zigzag/flat. Signals trend
exhaustion — "too far, too fast" in the preceding move.
(EW International https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/;
EBC https://www.ebc.com/forex/how-do-ending-diagonals-fit-into-your-trading-strategy)

**Sub-wave structure: 3-3-3-3-3** (all five legs are each three-wave corrective moves).

**Overlap rule:** Wave 4 almost always moves *into* the price territory of wave 1
(overlap). This is the distinguishing characteristic vs a normal impulse.

**Size (contracting form, most common):** waves contract — wave 5 < wave 3 < wave 1 in
length. The boundary lines converge toward an apex that is not yet reached when wave 5
ends.

**Expanding form (rare):** waves expand — wave 5 > wave 3 > wave 1. Lines diverge.

**After completion:** a rapid, full retrace back to the origin of the entire diagonal
(i.e., the start of wave 5 or wave C) typically follows very quickly. See also
`02_neowave_neely.md` §[terminal retrace] for NeoWave's fast-retrace timing rules.

#### 2.4.2 Leading Diagonal (wave 1 or wave A)

Position: exclusively in wave 1 of an impulse or wave A of a zigzag. Signals that a new
trend has begun but in an unusual, uncertain form.
(EWM Interactive https://ewminteractive.com/recognize-leading-diagonal-pattern;
Market Bulls https://market-bulls.com/leading-diagonal-elliott-wave/)

**Sub-wave structure: 5-3-5-3-5** (contrast: ending diagonal uses 3-3-3-3-3). The
impulsive sub-structure within each motive leg confirms that the trend is genuine.

**Overlap rule:** Wave 4 typically (but not always mandatorily) overlaps wave 1. Overlap
is common but somewhat less consistent than in an ending diagonal.

**Size (contracting form, most common):** wave 1 > wave 3 > wave 5 in length. Lines
converge.

**Expanding form:** wave 1 < wave 3 < wave 5. Lines diverge. Less common.

**After completion:** the impulse continues — wave 2 will retrace deeply (often 61.8%–
78.6% of the leading diagonal), but does not break its origin. The leading diagonal is
followed by a full motive sequence of waves 2 through 5.

**Key distinctions from ending diagonal:**

| Feature | Leading diagonal | Ending diagonal |
|---------|-----------------|-----------------|
| Position | Wave 1 or A | Wave 5 or C |
| Sub-wave structure | 5-3-5-3-5 | 3-3-3-3-3 |
| Overlap (4 into 1) | Common, not always | Expected/mandatory |
| What follows | Continuation (impulse resumes) | Sharp full reversal |
| Signal | Uncertain start of new trend | Exhaustion, trend end |

---

### 2.5 Degree Hierarchy and Notation

Elliott identified nine degrees of waves, from largest (multi-century) to smallest
(minutes). The hierarchy is fractal: each degree is composed of waves of the next smaller
degree.
(Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle;
EW Insight https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/)

| # | Degree name | Typical duration | Motive labels | Corrective labels |
|---|-------------|-----------------|--------------|-------------------|
| 1 | Grand Supercycle | Multi-century | (I)(II)(III)(IV)(V) [circled Roman] | (A)(B)(C) [circled] |
| 2 | Supercycle | Multi-decade (40–70 yr) | I II III IV V [Roman] | A B C [Roman cap] |
| 3 | Cycle | 1 year to several decades | I II III IV V [Roman] | A B C [Roman cap, or same as Supercycle context] |
| 4 | Primary | Months to 2 years | (1)(2)(3)(4)(5) [circled Arabic] | (A)(B)(C) [circled] |
| 5 | Intermediate | Weeks to months | 1 2 3 4 5 [plain Arabic] | A B C [plain caps] |
| 6 | Minor | Days to weeks | 1 2 3 4 5 [plain Arabic, smaller] | a b c [plain lower] |
| 7 | Minute | Hours to days | i ii iii iv v [Roman lower] | a b c [Roman lower] |
| 8 | Minuette | Minutes to hours | i ii iii iv v [Roman lower] | a b c [Roman lower] |
| 9 | Subminuette | Sub-minute | (i)(ii)(iii)(iv)(v) [circled lower] | (a)(b)(c) [circled lower] |

**Practical notation note (Prechter / common usage):**
- In text, analysts often use parentheses and brackets to distinguish degrees: `(I)` >
  `[I]` > `I` > `(1)` > `[1]` > `1` > `(i)` > `[i]` > `i` from large to small.
- In `wavelib`, degree is entirely absent — waves are plain `Wave` objects with a string
  `label` field that can hold any text but carries no degree semantics.

**Critical architectural gap:** Without encoded degree, the engine cannot:
- Resolve which sub-wave sequences need to be validated at which scale.
- Enforce that a corrective structure at one degree is the correct size relative to its
  neighbours.
- Implement auto-labelling across multiple degrees simultaneously.
- Apply Neely's monowave/polywave/multiwave construction (see `02_neowave_neely.md`).

---

### 2.6 Fibonacci Wave Relationships

Elliott Wave analysis is inseparable from the Fibonacci number sequence. The ratio φ
(≈1.618) and its inverse (≈0.618) appear repeatedly as guideline targets.
(FBS https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275;
EW Dynamics https://elliottwavedynamics.com/comprehensive-guide-to-elliott-wave-theory/)

#### Retracement ratios

| Level | Calculation | Common use in EW |
|-------|-------------|-----------------|
| 0.236 | 1 − 0.764 | Shallow wave 4, not common |
| 0.382 | 1 − 0.618 | Wave 4 common target; shallow wave 2 |
| 0.500 | — | Wave 2 common target |
| 0.618 | 1/φ | Wave 2 most common target; B-wave zigzag maximum |
| 0.764 | √0.618 | Deep wave 2 |
| 0.786 | √0.618 ≈ 0.786 | Deep corrections; wave 2 near-limit |

#### Extension / projection ratios

| Level | Calculation | Common use in EW |
|-------|-------------|-----------------|
| 1.000 | — | Equality of waves (wave 5 = wave 1; wave C = wave A) |
| 1.272 | √φ | Wave 5 moderate extension |
| 1.618 | φ | Wave 3 typical extension; wave C expanded flat |
| 2.000 | — | Wave 3 moderate extension |
| 2.618 | φ² | Wave 3 strong extension |
| 3.618 | φ³ | Wave 3 extreme extension |
| 4.236 | φ⁴ | Wave 3 very extreme extension (rare) |

#### Summary of typical wave-by-wave targets

| Wave | Typical Fibonacci targets |
|------|--------------------------|
| Wave 2 | 0.500, 0.618 of wave 1 (deep: 0.764, 0.786) |
| Wave 3 | 1.618 × wave 1 (common); 2.618×, 3.618× (extended) |
| Wave 4 | 0.236 (shallow), 0.382 (median), 0.500 (outer) of wave 3 |
| Wave 5 | = wave 1 (equality, most common); 0.618 × wave 3; 1.618 × wave 1 (extended) |
| Zigzag C | = wave A; 0.618 × A, 1.618 × A |
| Flat B | 0.618–1.000 × A (regular); 1.000–1.382× A (expanded) |
| Flat C | 1.000–1.618 × A |

---

## 3. Current wavelib Audit

Audit target: `/home/user/Ewace_2026/wavelib/rules.py`. Sections B (impulse), C
(corrections), D (diagonals), plus the cross-cutting degree gap.

| Concept | Implemented? (file:func) | Fidelity | Gap note |
|---------|--------------------------|----------|----------|
| Hard rule R1: wave 2 < 100% of wave 1 | `rules.py:elliott_hard_rules` (line 97–99) | Full | Checks `w2.end.price > w1.start.price` (bull). Correct. |
| Hard rule R2: wave 3 not shortest | `rules.py:elliott_hard_rules` (line 101–104) | Full | Logic `not (w3 < w1 AND w3 < w5)` is the canonical definition. Correct. |
| Hard rule R3: wave 4/wave 1 no overlap | `rules.py:elliott_hard_rules` (line 105–109) | Full | `w4.end.price > w1.end.price` (bull). Correct. Note appended if diagonal. |
| Guideline: extension present | `rules.py:elliott_guidelines` (line 119–125) | Heuristic | Threshold: extended wave must be > 1.3× second. Canonical says ≥ 1.618× is the Fibonacci target; 1.3× is loose. The check does identify *which* wave extends, which is useful, but 1.3× will trigger PASS for patterns that are not truly "extended" by EW theory. |
| Guideline: equality of non-extended waves | `rules.py:elliott_guidelines` (line 127–131) | Heuristic | Uses `ratio > 0.6` (i.e., the two non-extended waves within 60% of each other). Canonical: equality or 0.618. The 0.6 threshold is close to canonical 0.618 but inverted direction; `min/max > 0.6` is a reasonable proxy. Could be tightened to 0.618 and add note that equality (≈ 1.0) is the primary target. |
| Guideline: alternation (depth, 2 vs 4) | `rules.py:elliott_guidelines` (line 133–137) | Heuristic | Only checks price depth difference > 0.15 (15 pp). Does NOT check for form alternation (sharp vs sideways) or time alternation. Canonical alternation is multidimensional. |
| Guideline: wave 2 depth 0.5–0.618 | `rules.py:elliott_guidelines` (line 139–140) | Heuristic | Band `0.45–0.75` coded. Canonical typical range is 0.5–0.618; the code's lower bound (0.45) and upper (0.75) are modestly wider. Not wrong, but 0.764–0.786 range is a real secondary cluster that is outside the coded band. |
| Guideline: wave 4 depth 0.236–0.382 | `rules.py:elliott_guidelines` (line 141–142) | Heuristic | Band `0.18–0.45` coded. Canonical typical is 0.236–0.382; the code's lower (0.18) is below 0.236 and upper (0.45) is above 0.382 but below 0.5. Reasonably loose but not unreasonable. |
| Guideline: wave 3 ≈ 1.618–2.618× wave 1 | `rules.py:elliott_guidelines` (line 144–146) | Heuristic | Band `1.3–3.0` coded. Lower bound (1.3×) is below the canonical 1.618× Fibonacci target. Upper bound (3.0×) misses the 3.618× level which appears in strongly extended third waves. Recommend: split into preferred (1.618–2.618, PASS) and outer (1.3–1.618 or 2.618–4.236, WARN). |
| Guideline: wave 5 projection | `rules.py:project_wave5` (line 150–155) | Heuristic | Returns `w5=w1` (equality) and `w5=0.618×w3`. Missing: `w5=1.618×w1` (extended fifth) and `w5=0.382×w3`. Only binary output; no ranking by probability. |
| Guideline: channeling (base channel) | Not implemented | Missing | The 0-2 base channel (parallel through wave-1 top) is absent. Only 2-4 and 1-3 tests exist. |
| Guideline: wave personality | Not implemented | Missing | No personality/psychology labels. Not automatable (text descriptions), but could be returned as REF strings alongside rule results. |
| Correction: zigzag classifier | `rules.py:classify_correction` (line 175–177) | Heuristic | Threshold: `b_retr <= 0.62`. Canonical rule is B ≤ 0.618 of A. The 0.62 is within rounding tolerance but should be precisely 0.618. More critically, the function does NOT verify that wave A sub-divides in 5 or that wave C sub-divides in 5 (that would require sub-wave data). Currently classifies by B-wave retracement only, which is correct as a heuristic given the Wave-level input. |
| Correction: flat (regular) | `rules.py:classify_correction` (line 178–191) | Heuristic | Threshold: `b_retr >= 0.9` enters flat branch. Canonical minimum for a flat is B > 0.618; the 0.9 threshold is effectively classifying only the upper portion of flats and misses regular flats where B is between 0.618 and 0.9. The "intermediate/complex" catch-all (line 189–191) covers 0.62–0.9, but this includes valid regular flats. See gap note below. |
| Correction: flat (expanded) | `rules.py:classify_correction` (line 181–183) | Heuristic | Detects `b_retr > 1.0 and c_vs_a > 1.0`. Canonical: B > 1.0 AND C > 1.0 of A. This is correct for the expanded case. However, missing: the canonical B minimum for expanded is typically 1.05; and C should extend *past the end of A*, not just be longer than A's absolute length — the current check compares `C.length / A.length` rather than checking whether C's endpoint surpasses A's endpoint (a directional check). |
| Correction: flat (running) | `rules.py:classify_correction` (line 184–186) | Heuristic | Detects `b_retr > 1.0 and c_vs_a <= 1.0`. Canonical running flat: B > 100% of A AND C fails to reach end of A. The `c_vs_a <= 1.0` length-ratio check is directionally correct, but again misses the endpoint check (should verify that C's endpoint does NOT surpass A's endpoint). |
| Correction: flat B/C threshold gap (0.62–0.9) | `rules.py:classify_correction` (line 189–191) | Missing | B retracement between 0.62 and 0.9 returns WARN as "intermediate/complex". But canonical theory places regular flat B in the 0.618–1.0 range, with 0.9 being typical, not the minimum. A B of 0.7–0.9 is a valid regular flat per Frost & Prechter. |
| Correction: triangle (contracting/expanding) | `rules.py:_classify_triangle` (line 194–209) | Heuristic | Checks `lens[0] > lens[2] > lens[4]` (every-other leg contracting). This checks only legs 1, 3, 5 (a, c, e) — not the full a > b > c > d > e ordering. A contracting triangle has all five legs progressively shorter, not just the odd ones. The current check will pass a triangle where b > a (as long as a > c > e), which is incorrect. |
| Correction: triangle (barrier) | `rules.py:_classify_triangle` (line 202–204) | Heuristic | Classified as default when not contracting or expanding. Barrier triangles have one flat boundary; the current code doesn't actually check for a flat boundary — it simply falls through. This is a stub/heuristic. |
| Correction: triangle wave E overshoot | Not implemented | Missing | Canonical: wave E commonly overshoots or undershoots the a-c boundary. No check exists. |
| Correction: triangle thrust projection | Not implemented | Missing | Canonical: post-triangle thrust ≥ 75% of widest leg. No projection function exists. |
| Correction: combination (W-X-Y) | `rules.py:classify_correction` (line 168–170) | Stub | Any non-3, non-5 leg count → "COMBINATION" REF. No sub-structure analysis. Canonical has specific rules for X-wave size (< 61.8% of W) and triangle-only-as-final. All REF, which is honest. |
| Diagonal: ending diagonal rules | `rules.py:diagonal_rules` (line 215–240) | Heuristic | Checks: overlap (correct), wave-3 not shortest (WARN not FAIL in diagonal, correct), contracting wedge (line 236–239). Does NOT verify sub-wave structure (3-3-3-3-3 for ending vs 5-3-5-3-5 for leading). Position parameter (`"leading"` vs `"ending"`) is accepted as string but NOT used to enforce different sub-wave structure rules. |
| Diagonal: leading vs ending distinction | `rules.py:diagonal_rules` (line 215) | Stub | `position` parameter passed in but structural differences (sub-wave count 5-3-5-3-5 vs 3-3-3-3-3, mandatory vs common overlap, valid position in sequence) are NOT enforced. Both paths run the same checks. This is the most significant structural gap in the diagonal code. |
| Diagonal: sub-wave structure (5-3-5-3-5 vs 3-3-3-3-3) | Not implemented | Missing | Requires access to sub-wave data. Not possible with the current Wave-level input. This is a genuine data-availability gap, not just a coding omission. |
| Diagonal: contracting vs expanding check | `rules.py:diagonal_rules` (line 236–239) | Heuristic | Only checks contracting (`w5 < w3 < w1`). No explicit expanding check (expanding is just the else case → WARN). Canonical expanding diagonals are valid but rarer; WARN is reasonable, but the code doesn't distinguish "expanding (valid)" from "neither contracting nor expanding (irregular)". |
| Wave degree hierarchy | Not implemented (anywhere) | Missing | No `Degree` enum, no `degree` field on `Wave` or `Pivot`, no multi-degree validation. The `label` string field carries free text. This is the most architecturally impactful gap. |
| Fibonacci ratio table | Partial (`project_wave5`, `fib_extension`, `fib_retrace` in toolkit) | Heuristic | Only equality and 0.618×wave3 projections for wave 5. Missing 1.618×wave1 extension projection and 0.382×wave3 shallow projection. |

**Summary of gap severity:**

| Severity | Concepts |
|----------|----------|
| Critical (architectural) | Degree hierarchy absent; sub-wave structure inaccessible to rule engine |
| High (classification errors possible) | Flat B 0.62–0.90 range misclassified; triangle legs checked on alternating subset only; leading vs ending diagonal not differentiated |
| Medium (thresholds off) | Zigzag B threshold 0.62 vs 0.618; extension threshold 1.3× vs 1.618×; wave3 ratio upper bound 3.0× misses 3.618× |
| Low (missing features) | Base channel (0-2 line); wave personality; triangle thrust projection; wave E overshoot check; expanded-flat endpoint check vs length-ratio check |

---

## 4. Build Roadmap

Items are ordered by impact and dependency. Items marked CAUSAL require care to avoid
forward-looking data (per D-013 in the sibling `chakra_quant` repo; `wavelib` itself
should follow the same principle: rules at pivot `t` use only data ≤ `t`).

### Task 1 — Fix flat classifier threshold gap (HIGH priority)

**File:** `rules.py:classify_correction`

Problem: the branch `b_retr >= 0.9` misses the canonical 0.618–0.9 range for regular flat.

Fix:
```python
# Proposed canonical thresholds
ZIGZAG_B_MAX = 0.618    # canonical; currently coded as 0.62
FLAT_B_MIN   = 0.618    # any flat requires B > 0.618 of A
REG_FLAT_MAX = 1.00     # regular: B within [0.618, 1.00]
EXP_FLAT_MIN = 1.00     # expanded: B > 1.00 of A
# Running flat: B > 1.00, BUT C endpoint does not surpass A endpoint (direction check)
```

Change the branch logic to:
```
b_retr <= 0.618  → ZIGZAG
b_retr > 0.618 and b_retr <= 1.00  → REGULAR FLAT (or FLAT variant)
b_retr > 1.00 and C endpoint > A endpoint  → EXPANDED FLAT
b_retr > 1.00 and C endpoint <= A endpoint  → RUNNING FLAT
0.618 < b_retr < FLAT_B_MIN  → should never occur with the above logic
```

The endpoint check for expanded vs running flat requires comparing `C.end.price` to
`A.end.price` in the motive direction — no lookahead concern (CAUSAL OK: both A and C are
already complete at classification time).

Write test: `test_classify_correction_flat.py` with edge cases at exactly 0.618, 0.90,
1.00, and 1.05 B-wave retracement values.

### Task 2 — Split leading vs ending diagonal into separate functions (HIGH priority)

**File:** `rules.py`

Problem: `diagonal_rules(w, position)` accepts a `position` string but enforces identical
checks for both leading and ending diagonals. The structural difference is material:

- Ending: 3-3-3-3-3; overlap expected (FAIL if absent without sub-wave check would be
  too strict since sub-waves are inaccessible, so WARN); position = wave 5 or wave C.
- Leading: 5-3-5-3-5 (sub-wave check inaccessible); overlap common but not always; position
  = wave 1 or wave A.

Proposed API:
```python
def ending_diagonal_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """wave 5 / wave C position. 3-3-3-3-3 (sub-structure REF). Overlap expected."""

def leading_diagonal_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """wave 1 / wave A position. 5-3-5-3-5 (sub-structure REF). Overlap common."""
```

Both functions should emit a REF result noting the sub-wave structure requirement that
cannot be machine-checked at this degree of resolution.

The `is_terminal` function in section F already implements a separate NeoWave terminal
check; these two functions would be the classic-EW equivalents.

CAUSAL note: no lookahead concern — diagonal classification uses only the five already-
complete wave endpoints.

### Task 3 — Fix triangle leg-progression check (HIGH priority)

**File:** `rules.py:_classify_triangle`

Problem: `contracting = lens[0] > lens[2] > lens[4]` only checks alternating legs (a, c, e).
Canonical contracting triangle: all five legs a > b > c > d > e.

Fix:
```python
contracting = all(lens[i] > lens[i+1] for i in range(4))  # a>b>c>d>e
expanding   = all(lens[i] < lens[i+1] for i in range(4))  # a<b<c<d<e
# barrier: check if one boundary is approximately flat (max deviation ≤ X%)
# wave E overshoot: emit REF noting e may over/undershoot a-c line
```

Add a threshold constant for barrier detection and emit a REF result noting wave E
overshoot probability. Add thrust projection:
```python
def triangle_thrust(widest_leg: float, base: float, direction: int) -> dict:
    """Project post-triangle thrust: 75%–125% of widest_leg from apex base."""
    return {"min": round(base + direction * 0.75 * widest_leg, 2),
            "max": round(base + direction * 1.25 * widest_leg, 2)}
```

CAUSAL: classification and projection use only completed wave data — OK.

### Task 4 — Add Degree enum and degree field to Wave/Pivot (ARCHITECTURAL)

**File:** `rules.py`

This is the largest single architectural change. The degree gap means multi-degree
validation (e.g., "is this wave 2 at the Intermediate degree consistent with the Minor
sub-waves?") is not possible.

Proposed minimal implementation:
```python
class Degree(Enum):
    GRAND_SUPERCYCLE = 1
    SUPERCYCLE       = 2
    CYCLE            = 3
    PRIMARY          = 4
    INTERMEDIATE     = 5
    MINOR            = 6
    MINUTE           = 7
    MINUETTE         = 8
    SUBMINUETTE      = 9

@dataclass
class Wave:
    start: Pivot
    end: Pivot
    label: str = ""
    degree: Optional[Degree] = None   # NEW
```

This is backward-compatible (degree=None = degree not assigned).

Downstream: `similarity_and_balance` can then check that two corrective waves being
compared are actually at the same degree. `validate_impulse` can enforce that wave 4's
endpoint is consistent with the degree-specific overlap rules.

Auto-degree assignment from ZigZag amplitude is the goal (see CLAUDE.md TODO item 4):
given a price-history ZigZag, assign degrees based on relative size via the Rule of
Proportion. This is inherently heuristic and subject to the degree ambiguity caveat in §5.

CAUSAL: degree assignment is based on completed wave endpoints — OK.

### Task 5 — Firm up Fibonacci guideline thresholds (MEDIUM priority)

**File:** `rules.py:elliott_guidelines`

Specific changes:
- Extension threshold: change `1.3 * second` → `1.618 * second` (canonical Fibonacci).
  Emit the softer WARN at 1.3× and PASS only at 1.618×+.
- Wave 3 ratio band: change `1.3 <= r3 <= 3.0` → add a second WARN tier:
  `1.618 <= r3 <= 3.618` = PASS, `1.3 <= r3 < 1.618` = WARN (short), `r3 > 3.618` = WARN
  (extremely extended, check for degree shift).
- Wave 5 projection: add `w5=1.618*w1` (extended fifth) and `w5=0.382*w3` (short fifth)
  to `project_wave5` return dict.
- Zigzag B threshold: tighten from `0.62` to `0.618` in `classify_correction`.

None of these changes involve future data (CAUSAL OK).

### Task 6 — Add base channel (0-2 line) test (LOW priority)

**File:** `rules.py`

Missing function:
```python
def base_channel_test(w0_origin: Pivot, w1_top: Pivot, w2_end: Pivot,
                      current_t: float, current_price: float,
                      uptrend: bool = True) -> RuleResult:
    """
    Base channel: line through w0_origin and w2_end; parallel through w1_top.
    Price holding above the lower line (w0-w2) during wave 3 confirms motive.
    A break below the lower line during wave 4 is a warning.
    """
```

CAUSAL: all pivots (w0, w1, w2) are already complete at time of check — OK.

### Task 7 — Tests for corrected classifiers

Write `tests/test_rules_corrections.py`:
- `test_zigzag_b618_boundary`: B = exactly 0.618 → ZIGZAG PASS.
- `test_flat_b_between_618_and_90`: B = 0.75 → REGULAR FLAT PASS (currently misclassified).
- `test_expanded_flat_endpoint_vs_length`: verify that endpoint check distinguishes expanded
  from regular when C is long but ends before A's extreme.
- `test_running_flat`: B = 1.1, C endpoint < A endpoint → RUNNING FLAT.
- `test_triangle_all_five_legs`: contracting with b > a → should NOT be contracting.
- `test_leading_vs_ending_diagonal_distinction`: same 5 waves should return different
  results under `leading_diagonal_rules` vs `ending_diagonal_rules`.

---

## 5. Open Questions / Subjectivity Caveats

### 5.1 Degree ambiguity — the central problem

Two experienced analysts looking at the same chart will often disagree on which degree a
wave belongs to. A sequence that looks like wave (3) of Primary to one analyst may be wave
((3)) of Intermediate to another. This is not a code problem; it is intrinsic to the theory.
(DOCUMENTATION.md §9; CLAUDE.md TODO item 4)

Implication for `wavelib`: the library currently sidesteps this by requiring the user to
hand-pick which pivots represent which wave degree. Any automated degree-assignment algorithm
(Task 4) will inherit this subjectivity and should express its confidence as a REF or WARN,
not a hard PASS.

### 5.2 Sub-wave structure is inaccessible at a single degree

The sub-wave structure rules (zigzag A in 5, B in 3; leading diagonal in 5-3-5-3-5;
ending diagonal in 3-3-3-3-3) require examining *the next smaller degree* of waves. At the
`Wave` level, this data is not present. Rules that require sub-wave structure must remain
REF until the library supports recursive multi-degree wave trees.

### 5.3 Guideline thresholds are statistical tendencies, not physics

Thresholds like "wave 2 retraces 61.8% of wave 1" are empirical observations across a
large sample. Individual waves deviate; the guidelines help identify the *most likely*
scenario. Any threshold encoded in `wavelib` is a heuristic approximation of a probability
distribution, not an exact cutoff. WARN is the correct status, not FAIL.

### 5.4 Flat subtype B-wave ambiguity

The distinction between a regular flat (B ≈ 90%–100%) and an expanded flat (B > 100%) is
clear in theory. In practice, market data near the 100% boundary can be classified either
way depending on measurement precision (intrabar vs closing-price pivots). The `wavelib`
ZigZag uses intrabar highs/lows, which tends to produce slightly larger B-wave measurements
than closing-price ZigZags; calibrate boundary thresholds accordingly.

### 5.5 Triangle wave E overshoot

Wave E of a triangle routinely slightly overshoots or undershoots the a-c boundary line.
Any automated triangle classifier that requires strict containment will reject valid
triangles. The recommended approach: apply a tolerance band (e.g., ±2% of wave A) around
the a-c line when checking wave E; emit REF rather than FAIL.

### 5.6 "X-wave" identity in combinations

Combinations are the most subjective of correction patterns. An analyst can almost always
find a plausible W-X-Y labelling for any sideways price action. The key discipline:
W and Y should each be clearly identifiable as a simpler pattern (zigzag, flat, or
triangle), and X should be visibly smaller than W. Without automated sub-pattern
classification, the `wavelib` REF status for combinations is the honest answer.

---

## Sources

- Frost, A.J. & Prechter, R.R. *Elliott Wave Principle*, 10th ed. PDF via Investment Theory:
  https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf
- Elliott Wave International Waveopedia (Flats, Triangles, Combinations, Channeling,
  Diagonals, Wave Personality):
  https://www.elliottwave.com/waveopedia/
- Wikipedia — "Elliott Wave Principle":
  https://en.wikipedia.org/wiki/Elliott_wave_principle
- StockCharts ChartSchool — "Identifying Elliott Wave Patterns":
  https://chartschool.stockcharts.com/table-of-contents/market-analysis/elliott-wave-analysis-articles/identifying-elliott-wave-patterns
- StockCharts ChartSchool — "Guidelines for Applying Elliott Wave Theory":
  https://chartschool.stockcharts.com/table-of-contents/market-analysis/elliott-wave-analysis-articles/guidelines-for-applying-elliott-wave-theory
- EW Forecast — "Elliott Wave Theory: Rules, Guidelines & Structures":
  https://elliottwave-forecast.com/elliott-wave-theory/
- EW Forecast — "Three Types of Elliott Wave Flats":
  https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/
- EW Forecast — "Ending Diagonal in Elliott Wave":
  https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/
- EW Street — "Elliott Wave Theory: The Complete Guide to Wave Analysis & Trading (2026)":
  https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/
- EW Monitor — "Elliott Wave Theory: Everything You Need To Know":
  https://elliottwavemonitor.com/elliott-wave-theory/
- Bullwaves — "Simple Elliott Wave Correction Patterns: Rules and Guidelines":
  https://bullwaves.org/complete-guide-elliott-wave-correction-patterns/
- EWM Interactive — "Recognize the Leading Diagonal Pattern":
  https://ewminteractive.com/recognize-leading-diagonal-pattern
- Market Bulls — "Leading Diagonal Elliott Wave Explained":
  https://market-bulls.com/leading-diagonal-elliott-wave/
- EBC Financial — "How Do Ending Diagonals Fit Into Your Trading Strategy?":
  https://www.ebc.com/forex/how-do-ending-diagonals-fit-into-your-trading-strategy
- EW Trader — "Ending Diagonal Triangle Elliott Wave Pattern":
  https://thepatternsite.com/EWDiagTriangle.html
- EW Trader — "Leading Diagonal Triangle Elliott Wave Pattern":
  https://thepatternsite.com/EWleadingTriangle.html
- FBS — "Double Three and Triple Three Patterns":
  https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns
- FBS — "Fibonacci Ratios and Impulse Waves in Elliott Wave Analysis":
  https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275
- EW International — "Elliott Wave Pattern Diagonals":
  https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/
- EW Dynamics — "Comprehensive Guide to Elliott Wave Theory":
  https://elliottwavedynamics.com/comprehensive-guide-to-elliott-wave-theory/
- Banks & Bankers — "Flat Elliott Wave Pattern: Complete Beginner's Guide":
  https://banksandbankers.com/flat-elliott-wave-beginners-guide/
- Price Action Help — "The Elliott Wave Theory — Revised Rules and Guidelines":
  https://priceactionhelp.com/elliott-wave
- Algotrading-Investment — "Channelling Technique with Elliott Wave":
  https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/
- Forex Training Group — "Characteristics and Personalities of Elliott Waves":
  https://forextraininggroup.com/characteristics-and-personalities-of-elliott-waves/
- EW Insight — "Elliott Wave Degrees & Labeling":
  https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/
- Yet Another EW Analysis Blog — "Wave Labels":
  https://yaewab.blogspot.com/p/wave-labels.html
- LiteFinance — "Prechter Wave Theory: Degrees and Alternation":
  https://www.litefinance.org/blog/for-professionals/market-wave-theory-by-robert-prechter-part-2-wave-degrees-and-more-guidelines-of-wave-alternation/
- Elliott Wave International — "Combinations":
  https://www.elliottwave.com/waveopedia/combinations/
- Elliott Wave International — "Triangles":
  https://www.elliottwave.com/waveopedia/triangles/
- Elliott Wave Monitor — "Leading and Ending Diagonal":
  https://elliottwavemonitor.com/leading-and-ending-diagonal/
- Medium / EW Monitors — "Elliott Wave Theory: Everything You Need to Know":
  https://medium.com/@ewmonitors/elliott-wave-theory-everything-you-need-to-know-3c038cc3971f
- Stokes Trades — "Elliott Wave Theory and Fibonacci Numbers":
  https://stokestrades.com/elliott-wave-theory/
- EW OTrader — "Elliott Wave and Fibonacci Retracements & Projections":
  https://ewotrader.com/education/elliott-wave-theory/elliott-wave-and-fibonacci/
