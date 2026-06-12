# 03 — NEoWave FORECASTING and TRADING Method

**Status:** practitioner research — 2026-06-12
**Author:** agent research session (Ewace_2026)
**Scope:** How NEoWave *predicts and trades* the next wave — the forecasting and
trading layer that sits on top of the construction mechanics already documented in
`02_neowave_neely.md` and `deep/05_neowave_full_algorithm.md`.

Construction details (monowave labelling, compaction hierarchy, the seven retracement
rules, pattern-specific hard rules) are NOT repeated here. This document is the
*forecasting and trading* slice.

**Primary sources:**

| ID | Source | URL |
|----|--------|-----|
| MEW | Glenn Neely, *Mastering Elliott Wave* v2, Windsor Books, 1990 | https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp |
| NW-QA | neowave.com Q&A archive (direct Neely answers) | https://www.neowave.com/qow-archive.asp |
| NW-19 | QA-19 — Structure vs Behaviour | https://www.neowave.com/qow/qow-archive-19.asp |
| NW-22 | QA-22 — Confirming wave-5 end | https://www.neowave.com/qow/qow-archive-22.asp |
| NW-474 | QA-474 — Post-diametric behaviour | https://www.neowave.com/qow/qow-archive-474.asp |
| NW-1109 | QA-1109 — Two types of confirmation | https://www.neowave.com/qow/qow-archive-1109.asp |
| NW-1285 | QA-1285 — Why trading deviates from forecast | https://www.neowave.com/qow/qow-archive-1285.asp |
| NW-RRL | Rule of Reverse Logic | https://www.neowave.com/neowave-rules-of-reverse-logic.asp |
| NW-WHAT | What is NEoWave? | https://www.neowave.com/what-is-neowave.asp |
| NW-ANAL | What is NEoWave Analysis? | https://www.neowave.com/what-is-neo-wave-analysis.asp |
| NW-DIFF | NEoWave vs Elliott Wave | https://www.neowave.com/what-is-the-difference-between-neo-wave-and-elliott-wave.asp |
| LF-27 | LiteFinance Part 27 — Trading Strategy | https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/ |
| LF-16 | LiteFinance Part 16 — Extended Rules of Logic (Flats/Zigzags) | https://www.litefinance.org/blog/for-professionals/neowave-part-16-extended-rules-of-logic-for-zigzags-and-flat-corrections/ |
| LF-17 | LiteFinance Part 17 — Extended Rules of Logic (Complex Corrections) | https://www.litefinance.org/blog/for-professionals/neowave-part-17-extended-rules-of-logic-for-complex-corrections-exceptions-to-the-rules-2020-05-07 |
| LF-21 | LiteFinance Part 21 — Channeling and Fibonacci Relationships | https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships |
| FT-IL | ForexTalker — Impulse Rules of Logic | https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-price-impulses-the-rules-of-the-stretched-wave-equality-alternation-overlap-the-rules-of-logic/ |
| NW-3518 | QA-3518 — Supplemental Price and Time | https://www.neowave.com/qow/qow-archive-3518.asp |
| NW-17 | QA-17 — Wave-2 and wave-4 time in impulse | https://www.neowave.com/qow/qow-archive-17.asp |
| NW-RIVER | Neely River Trading Technology | https://www.neowave.com/NEELY-RIVER/ |

---

## 1. Why NEoWave Is Predictive Where Classical Elliott Is Descriptive

### 1.1 The Core Claim

Neely argues that orthodox Elliott Wave is **descriptive** — it tells you what probably
happened; it does not constrain what *must* happen next. Practitioners can always find a
valid label for any price action in retrospect. NEoWave claims to be **predictive**
because:

1. **Logical entailment.** Each identified pattern constrains the set of valid
   next-patterns to a narrow range. Post-pattern behaviour that falls outside that range
   falsifies the count. The count is therefore falsifiable — and falsifiable systems are
   predictive. [NW-WHAT]

2. **Self-defining price/time limits.** Every pattern in NEoWave carries hard limits on
   the time and price that subsequent patterns may consume. A smaller-degree pattern
   cannot take more time or price than a larger-degree pattern. This rule produces
   *advance time limits* on when a pattern can be expected to end. [NW-ANAL]

3. **Self-confirming post-pattern behaviour.** After a pattern ends, price must display
   specific post-pattern behaviour (direction, speed, magnitude) or the prior label is
   wrong. The wrongness is detectable, forcing the analyst to revise rather than
   rationalise. [NW-19]

4. **Logic flow through the count.** Neely's Rules of Logic specify, for each pattern
   type, what the next pattern must be and where it must end. Because these rules are
   violated by certain counts, the space of valid interpretations is genuinely narrow —
   often to one or two alternatives at most. [FT-IL]

### 1.2 EW vs NEoWave: The Practical Difference

| Attribute | Classical Elliott Wave | NEoWave |
|-----------|----------------------|---------|
| Pattern identification | Subjective; multiple valid counts typically coexist | Objective bottom-up construction; invalid counts are eliminated by structure labels + channeling |
| Post-pattern behaviour | Optional confirmation; not required | Mandatory; missing behaviour invalidates the count |
| Time forecasting | Informal / guidelines | Mandatory time limits per pattern + S&B time-similarity constraint |
| Count management | Analyst chooses "preferred" count | Rule of Reverse Logic — prefer the *least complete* count until evidence forces resolution |
| Trading signal | Interpretation-dependent; varies by analyst | Follows deterministic two-stage confirmation protocol |

[NW-DIFF, NW-ANAL]

### 1.3 The Three Logic Pillars

Neely's forecasting method rests on three pillars [NW-ANAL]:

1. **Logic:** *a strong correction must yield a powerful move.* The size and complexity
   of the prior correction encodes information about the minimum required size of what
   follows it.

2. **Self-defining limits:** *a smaller degree pattern cannot take more time and price
   than a larger degree pattern.* This produces an upper bound on how long any in-progress
   pattern can take before it must be reinterpreted as a higher-degree structure.

3. **Self-confirmation:** *strict requirements for post-pattern price behaviour determine
   whether prior structural analysis was correct.* If the market refuses to confirm, the
   label is changed — not the rules.

---

## 2. Enumerated Rules

Rules are numbered FR- (Forecasting), CC- (Completion/Confirmation), TR- (Trade).
Precision grades: **HARD** (explicit in MEW or Q&A as a rule); **FIRM** (consistently
stated across multiple sources but without an exact threshold); **GUIDELINE** (commonly
practised but explicitly framed as a tendency, not a rule).

---

### Part A — Completion and Confirmation Rules

---

**CC-1 (HARD): Two-Stage Impulse Completion Protocol**

An impulse pattern (trending or terminal) is confirmed complete only when both stages
have been satisfied. Until Stage 1 is met, the impulse is *in progress* regardless of
how extended wave 5 has become.

- **Stage 1 (mandatory):** After the presumed end of wave 5, price returns to the 2-4
  trendline in *less time than wave 5 took to form*. "Less time" means fewer bars,
  measured bar-for-bar against wave 5's duration. [NW-22, MEW Ch. 6]

- **Stage 2 (preferred/confirms larger degree):** The *entire price range* of wave 5 is
  retraced in *no more time than wave 5 took to form*. When Stage 2 is also satisfied,
  the analyst has confirmation that the next larger-degree move (not merely wave 5's
  retracement) has begun. Failing Stage 2 after Stage 1 suggests wave 5 was actually a
  much larger wave. [NW-22, NW-1109]

**Implementation note:** Both stages are timing constraints, not price-level tests alone.
The 2-4 line value at the time of the break is irrelevant if the timing is wrong.
Implemented in `two_four_confirmation()` but not yet invoked automatically on new bars.

---

**CC-2 (HARD): Type 1 vs Type 2 Pattern Confirmation**

Neely distinguishes two confirmation approaches [NW-1109]:

- **Type 1 (standard / book):** The two-stage 2-4 trendline protocol (CC-1). Used for
  historical analysis and for confirming that an *old pattern* has ended.

- **Type 2 (real-time trading):** Calculates the exact price-and-time point at which a
  *new larger-degree trend* will probably begin. More aggressive entry signal. Caveat:
  Type 2 generates false signals when the prior pattern has an expanding bias (expanding
  triangle, expanding diametric) because those patterns begin or end with an expanding
  phase that mimics the confirmation signal.

For automated analysis, Type 1 is the appropriate default. Type 2 should be flagged as
WARN when the prior pattern was an expanding variant.

---

**CC-3 (HARD): "Moves Further and Faster" Confirmation**

The general definition of pattern confirmation in NEoWave: *post-pattern price action
moves further and faster than the largest counter-trend wave of the prior pattern.*
This principle is universal across all pattern types (not just impulses). [NW-WHAT,
NW-RIVER]

When applied to real-time monitoring:
- Measure the largest counter-trend leg *within* the just-completed pattern (e.g., the
  deepest pull-back inside an impulse, or the widest leg of a triangle in the opposite
  direction).
- The first post-pattern move in the new direction must both exceed that counter-trend
  leg in *price* AND do so in *less time* than that counter-trend leg took to form.

This is the *universal* confirmation rule. The two-stage 2-4 protocol (CC-1) is the
specific implementation for trending/terminal impulses.

---

**CC-4 (HARD): Pre-constructive Filter — Pattern Is Not Started Until Conditions Are Met**

Before any pattern can be *claimed to have started*, the following must hold [MEW Ch. 3]:

1. **Complexity progression:** A corrective wave must be at least as complex as the
   motive wave it corrects. A simple monowave cannot correct a multiwave impulse.
2. **Wave-2 time rule (trending impulse):** Wave 2 must consume *at least as much time*
   as wave 1, and wave 4 must consume at least as much time as wave 3. [NW-17] These
   constraints mean a shallow, fast-completing candidate wave 2 is *not finished* — it
   is still in progress.
3. **Wave-2 time rule (terminal impulse):** The opposite applies — each corrective
   sub-wave in a terminal *may* be shorter in time than the preceding motive sub-wave.
4. **Upper time bound (trending impulse):** Wave 2 must not exceed 3× (300%) of wave 1
   in time, and wave 4 must not exceed 3× wave 3 in time. Exceeding this signals the
   pattern is not a standard impulse. [NW-17]

---

**CC-5 (HARD): Post-Correction Behaviour — Thrust Required**

After any *flat* or *zigzag* correction, a thrust in the direction of the preceding
trend is expected. The thrust should [MEW Ch. 6, LF-16]:

- **Direction:** opposite to the correction (resuming the prior trend).
- **Minimum magnitude:** the thrust must be *at least as large* as the correction itself
  in price (a thrust smaller than the correction suggests the correction is not over, or
  the degree is wrong).
- **Time limit:** the thrust should complete in *no more time* than the correction took
  to form.

Failure to see the thrust within the time window is a post-constructive FAIL: the
correction is mislabelled (incomplete, or of wrong type).

---

**CC-6 (HARD): Post-Triangle Thrust Rules**

After a contracting or neutral triangle completes, the post-triangle thrust satisfies
[NW-5161, MEW Ch. 5]:

- **Magnitude:** approximately equal to the longest leg of the triangle (wave a).
  This is the price target for the thrust.
- **Time limit:** the thrust *must complete* in no more time than the *shortest* triangle
  leg. If the thrust is still unfinished after this time window, the triangle was
  misidentified (or the analyst is tracking a different wave leg).
- **Direction:** in the direction of the trend that preceded the triangle. A triangle
  almost never occurs at the very beginning of a trend — it signals the penultimate leg
  before the final thrust (wave B or wave 4 are typical positions).

---

**CC-7 (HARD): Post-Diametric Behaviour**

After diametric wave g completes [NW-474]:

- **Immediate thrust:** a sharp move in the *opposite* direction to wave g, roughly equal
  to the *widest part* of the formation (the longest leg in price).
- **Speed test:** the post-g move must be *larger and faster* than any same-direction leg
  within the diametric. If it is not, the diametric is still in progress.
- **Degree test:** if the post-g wave is also *larger and faster* than waves B, D, and F
  (the counter-trend legs inside the diametric), the diametric ended a single leg of a
  *larger* formation. The larger pattern context (was it wave-A of a flat? wave-2 of an
  impulse? an x-wave?) determines the subsequent larger-degree projection.
- **Time:** no hard time limit (unlike triangles); expect the thrust to be sharp but no
  fixed duration rule is published.

---

**CC-8 (HARD): Post-Terminal Complete-Retrace Requirement**

After a terminal impulse completes [MEW Ch. 5, LF-20]:

- The *entire* terminal must eventually be retraced back to its origin price.
- Stage 1 (CC-1) confirms the terminal is over when the 2-4 line is broken in < wave-5
  time.
- The full retrace to origin is a *directional bias* not a timed guarantee. The retrace
  tends to begin fast (Stage 1 provides early confirmation) but the full origin retrace
  can extend well beyond Stage 2's timing window.

**Practical framing:** the origin price is the structural *target* for the retracement,
not a price to be reached within any fixed time window. Use the 1/4–1/2 build-time
window only as a monitoring bias — watch for the retrace accelerating in that window,
not for the origin to be reached within it.

---

**CC-9 (HARD): Behaviour Over Structure — The Falsification Rule**

> "No matter what you think of structure, if post-pattern behaviour is inconsistent
> with your labelling, your wave count is wrong." [NW-19]

This is not just a guideline — it is the primary error-correction mechanism of NEoWave.
When observed post-pattern behaviour violates any of CC-1 through CC-8:

1. The current label is **wrong**. It is not "unusual behaviour" — it is a falsified count.
2. The analyst must revise the label, not explain away the behaviour.
3. The most common cause: the pattern is *not yet complete* (incomplete correction,
   incomplete wave 5, misidentified endpoint).

In automated terms: if post-pattern behaviour fails any confirmation check, set the
`WaveNode.confirmation_status = Status.FAIL` and re-run pattern identification with
the final pivot point moved later.

---

### Part B — Next-Wave Direction, Price, and TIME Projection Rules

---

**FR-1 (HARD): Impulse Followed by Correction — Direction and Relative Size**

After a confirmed trending impulse (5-3-5-3-5) ends [MEW Ch. 6, FT-IL]:

- **Direction:** a correction in the *opposite* direction begins. It will be a
  3-wave corrective pattern (zigzag, flat, triangle) or a complex combination.
- **Retracement depth (wave 2 of next degree):** typically 38.2–61.8% of the impulse.
  The correction will not exceed 100% of the impulse (if it does, the prior label is
  wrong — the "impulse" was actually a corrective wave inside a larger structure).
- **If the impulse is wave 1 or wave 3 of a larger sequence:** the following wave must
  *not* completely retrace the impulse (> 100% retrace falsifies the impulse-labelling
  of this wave at the current degree).
- **If the impulse is wave 5:** the following wave is expected to retrace deeply (often
  38.2–61.8% of the *entire* prior 5-wave sequence at the next larger degree). The two
  stages of CC-1 govern the timing of this confirmation.

---

**FR-2 (HARD): Terminal Impulse — Immediate and Deep Opposite Correction**

After a confirmed terminal impulse ends [MEW Ch. 5, LF-20]:

- **Direction:** immediately reverses in the *opposite* direction.
- **Magnitude (HARD):** the correction must *completely retrace the entire terminal* back
  to the terminal's origin price. This is a hard NeoWave rule, not a guideline.
- **Speed:** the retrace begins faster than the terminal formed. Stage 1 (2-4 break in
  < wave-5 time) provides the entry-confirming early signal.
- **Implication:** a terminal in wave 5 position carries the most powerful reversal
  implication — the subsequent correction retraces not just the terminal but the entire
  larger impulse sequence (all 5 waves at the next degree).

---

**FR-3 (HARD): Post-Correction Impulse — Minimum Size from Prior Correction**

The impulse following a correction must satisfy a minimum size constraint keyed to the
nature of the prior correction [MEW Ch. 6, LF-17]:

| Prior correction type | Minimum required next impulse |
|----------------------|-------------------------------|
| Single zigzag or flat | Must be larger than the correction in price |
| Complex double three (W-X-Y) | Must be > 161.8% of the prior impulse of the same degree |
| Triangle | Must equal the *thrust* projection (≈ widest leg of triangle) |

**Logic:** "the post-effect after corrective patterns is usually more powerful than after
impulses." The more complex the correction, the larger the required follow-through. An
impulse that fails these minimum sizes is suspect — either the correction is not over, or
the degree is wrong.

---

**FR-4 (HARD): Pattern-Type Determines Degree Context of Next Move**

The position of the completed pattern within the larger structure determines whether the
next wave is a *continuation* (same trend degree) or a *termination* (trend reversal at
the current degree with continuation at the next larger degree).

Rules [MEW Ch. 4–6, NW-474]:

- **Pattern in wave 2 or wave 4 position:** the next wave is a motive wave (3 or 5) in
  the *same* direction as the prior motive waves. The target is the Fibonacci projection
  from the end of the corrective pattern.
- **Pattern in wave B position (within an A-B-C):** the next wave is wave C in the
  direction opposite to wave B. Wave C ≈ wave A (at minimum); may extend to 1.618× A.
- **Pattern in x-wave position (within a double/triple combination):** the next wave is
  the second (or third) corrective pattern of the complex combination, same-direction as
  the first corrective pattern.
- **Post-diametric thrust:** the move following the diametric ends the *larger pattern*
  that contains the diametric. The diametric is identified as a sub-leg of the larger
  structure, and the post-g thrust is the *terminal leg* of that larger structure.

---

**FR-5 (HARD): Fibonacci Price Targets for Next Wave**

Price targets for the next wave are derived from completed-wave measurements [MEW Ch. 5,
LF-21, LF-27]:

**For wave 3 of a trending impulse (measuring from wave 2 end):**

| Target | Calculation |
|--------|-------------|
| Minimum / conservative | 1.618 × wave 1 (measured from wave 2 end) |
| Standard extension | 2.618 × wave 1 |
| Strong extension | 4.236 × wave 1 |

**For wave 5 of a trending impulse (measuring from wave 4 end):**

| If wave 3 extended | Target |
|-------------------|--------|
| Wave 3 = extended | Wave 5 ≈ wave 1 (equality); secondary: 0.618 × wave 1 |
| Wave 1 = extended | Wave 5 ≈ wave 3 (equality); secondary: 0.618 × wave 3 |
| Wave 5 = extended | Project from wave 4 end: 1.618, 2.618, or 4.236 × wave 1 |

**For wave C of a correction (measuring from wave B end):**

| C-wave target | Condition |
|--------------|-----------|
| C ≈ A | Normal zigzag or regular flat |
| C = 1.618 × A | Extended zigzag or expanded flat |
| C = 0.618 × A | Running flat (C fails to reach A endpoint — WARN) |

**For post-triangle thrust:**
Thrust ≈ widest leg (wave a) measured from the e-wave endpoint in the thrust direction.

**For post-diametric thrust:**
Thrust ≈ widest leg of the formation from the g-wave endpoint.

---

**FR-6 (HARD): TIME Projection — Rule of Similarity and Balance**

This is the central mechanism by which NEoWave forecasts *when* a next wave completes
[MEW Ch. 4, NW-32, NW-78]:

- **Same-degree waves:** adjacent waves at the same degree must be within a **1/3–3×
  ratio** in both price AND time. This rule works in both directions:
  - *Forward (forecasting):* if the just-completed wave took N bars, the next same-degree
    wave must complete within the band [N/3, 3N] bars.
  - *Backward (validation):* if the current wave has already consumed > 3N bars, it is
    no longer the same degree as the prior wave — either it is a higher degree, or there
    is a hidden x-wave between them.

- **What this produces as a time forecast:**
  Given a completed wave of N bars, the *expected completion window* for the next
  same-degree wave is: **earliest possible** = entry + (N/3) bars; **latest possible** =
  entry + (3N) bars; **modal expectation** = entry + N bars (equality).

---

**FR-7 (HARD): Time Limits Within a Pattern — Sub-Wave Duration Constraints**

Each leg inside a pattern carries a hard upper time limit [NW-QA-search-similarity, MEW
Ch. 5]:

| Pattern | Hard time limit on last leg |
|---------|----------------------------|
| Flat / Zigzag | Wave C cannot consume > time(A) + time(B) combined |
| Triangle | Wave E cannot consume > time(B) + time(C) + time(D) combined |
| Diametric | Wave G cannot consume > time(D) + time(E) + time(F) combined |
| X-wave | Cannot consume more time than the entire prior correction (W) |
| Wave-b of Flat | Normally 2–4× time(A); suspicious if > 5–7× time(A) |

If an in-progress sub-wave is approaching these limits, the pattern is either nearing
completion or has been mislabelled.

---

**FR-8 (FIRM): Progress Labels and In-Pattern Direction**

Within a still-unfolding pattern, NEoWave uses progress labels to state the *current
structural position* and therefore the *immediate direction* of the next sub-wave
[LF-20, MEW Ch. 5]:

**Trending impulse — progress label implications:**

| Current position | Immediate direction |
|-----------------|---------------------|
| After wave 2 end | Wave 3 begins — motive direction, targets 1.618–4.236× wave 1 |
| After wave 3 end | Wave 4 correction begins — opposite direction, 38.2–61.8% retrace |
| After wave 4 end (wave 4 duration ≥ wave 3 duration confirmed) | Wave 5 begins — motive direction, targets wave-1 or 0.618× wave-1 |
| After wave 5 end + Stage 1 confirmed | Larger correction begins |

**Terminal impulse — additional rule:**
At the end of each sub-wave, the next sub-wave begins in the opposite direction and is
permitted to be shorter in time (unlike trending impulse where corrective sub-waves must
be ≥ motive sub-waves in time). The terminal signals exhaustion and ends with an immediate
reversal (FR-2).

**Triangle — progress label implications:**
Post-wave d, wave e begins in the direction of wave a. Once wave e is confirmed complete
by the thrust, the post-triangle move begins in the direction of the prior trend.

---

**FR-9 (FIRM): Rule of Reverse Logic — Prefer the Least-Complete Count**

When multiple wave counts are simultaneously valid [NW-RRL]:

> Select the count that requires the *most* additional price and time to resolve — the
> one with the *lowest completion fraction*.

**Completion fraction** = (price moved so far toward the pattern's projected terminal
price) / (full projected price range of the pattern).

**Algorithmic implementation:**

```python
completion_fraction = price_moved_so_far / projected_full_pattern_price_range
# Prefer: min(completion_fraction) across all valid candidate counts
```

**Forecasting implication:** if the count with the lowest completion fraction is a
triangle-in-progress (e.g. leg 4 of 5), the forecast is: more sideways consolidation,
then a thrust. The analyst does NOT call the pattern complete until the least-complete
valid count is eliminated by incoming price data.

**NeoWave claims this rule works 100% of the time when consistently applied.** [NW-RRL]

---

**FR-10 (FIRM): Post-Pattern Context — Was the Correction a Terminator or a Connector?**

After any corrective pattern completes, the analyst must classify its *contextual role*
[NW-474, MEW Ch. 4]:

1. **Terminator (wave 2, 4, B, or a leg of a triangle):** the correction *terminates*
   the prior motive wave and *connects* to the next motive wave of the *same* degree.
   The next move is a continuation of the trend at the current degree.

2. **Connector / x-wave:** the correction connects two larger corrective patterns.
   The next move is another corrective pattern, typically of the same direction as the
   first. The combined structure is a double or triple combination.

3. **Pattern-concluding correction (final leg of a larger pattern):** the correction is
   the *last leg* of a larger corrective structure (e.g., wave C of a flat, leg e of a
   triangle). After it ends, the move that follows is at the *next higher degree* — a
   completely different scale of pattern.

The post-pattern behaviour test (CC-3) distinguishes these roles: a move that is larger
and faster than any same-direction leg in the correction confirms the terminator or
pattern-concluding role; a smaller or slower move suggests the x-wave or connector role.

---

**FR-11 (HARD): Self-Defining Time Limit — Smaller Degree Cannot Take More Time**

A critical structural constraint for *real-time* count management [NW-ANAL]:

> A pattern at degree N cannot consume more time (or price) than a pattern at degree N+1.

In practice: if the in-progress candidate pattern is already consuming more time than
the prior pattern it is supposed to correct, either:
(a) the prior pattern was of higher degree than labelled, or
(b) the current pattern is of higher degree than assumed (it contains x-waves or has
    already subdivided into a complex combination).

This rule fires an automatic re-labelling signal: if `current_pattern.bars > prior_pattern.bars * 3.0`, the count must be revised.

---

### Part C — Trade Rules

---

**TR-1 (HARD): No Trade Until Stage 1 Confirmation**

The NEoWave method explicitly prohibits trading pattern completions on the identification
of the pattern alone. A trade is only initiated *after* Stage 1 confirmation is met
(CC-1). Before Stage 1, the pattern is a *candidate*, not a fact. [NW-22, NW-WHAT]

> Until Stage 1 fires, the trading panel shows: **NO TRADE — awaiting 2-4 line break.**

---

**TR-2 (HARD): Entry Confirmation — Two Consecutive Bars**

After Stage 1 is met, a trade entry requires an additional filter [LF-27]:

- **For a short trade after a completed upward impulse:** enter after the *second
  consecutive down bar* closes. Two consecutive closes in the new direction confirm the
  reversal has begun, not just a spike.
- **For a long trade after a completed downward correction:** enter after the *second
  consecutive up bar* closes.

Stop is set simultaneously with entry (TR-4). Entry on the bar close of the second
confirmation bar, not on anticipation of it.

---

**TR-3 (HARD): Neely River Separation — Forecasting ≠ Trading**

Neely explicitly separates the *forecasting layer* (NEoWave pattern analysis) from the
*trading layer* (Neely River). Trading is a three-prong process [NW-1285, NW-RIVER]:

1. **Trend prediction** — addressed by NEoWave: what is the likely direction and target.
2. **Entry timing** — addressed by Neely River: precise confirmation before entry.
3. **Position management** — addressed by Neely River: stop movement, scaling, exit.

The practical consequence for an automated engine: NEoWave analysis produces the
*forecast*; the trading execution layer must separately implement:
- The two-consecutive-bar filter (TR-2)
- Stop management (TR-4)
- Exit at Fibonacci target (TR-5)

Trading signals may deviate from the wave forecast when the trading layer's stops are
triggered before the price reaches the wave-theory target.

---

**TR-4 (HARD): Stop Placement — Logical Invalidation Level**

The stop is placed at the *logical invalidation level* of the count [LF-27, MEW Ch. 6]:

| Pattern type | Stop location |
|-------------|---------------|
| Terminal impulse — short trade | Above the terminal's peak (wave 5 peak). Reasoning: if price closes above the terminal peak, no reversal has begun; the terminal label is wrong. |
| Trending impulse complete — short trade | Above the wave-5 peak. |
| Trending impulse — long trade in wave 3 position | Below the wave-2 low. Reasoning: wave 2 cannot retrace > 100% of wave 1 in a valid impulse. |
| Correction (flat/zigzag) complete — long trade | Below wave C's low (the correction's endpoint). |
| Triangle complete — long trade | Below wave e's endpoint. |
| Any completed correction — long trade | Below the correction's full origin (point zero of the pattern). |

**The stop is not adjusted downward arbitrarily.** It is moved only when price has
advanced enough to make the stop a breakeven or better. Specifically: once price has
moved further than the largest counter-trend wave of the prior pattern (CC-3 confirmation
of full strength), the stop may be moved to breakeven or to protect a portion of profits.

---

**TR-5 (HARD): Fibonacci Price Targets as Exit Objectives**

Exit targets use the Fibonacci projection system (FR-5) applied to the *expected next
wave* [LF-27, LF-21]:

- **First target (partial exit):** the conservative Fibonacci level (e.g., 0.618× wave-1
  from wave-2 end for wave 3 of terminal retracement; or wave-a for wave-C of a flat).
- **Second target (full exit):** the 1.618× or equality level.
- **Channel-based alternative:** if the 2-4 channel's extension passes through a
  Fibonacci target, that confluence level is preferred as an exit.

A stop is moved to breakeven after the first target is reached. The position is held to
the second target unless post-pattern behaviour signals the next pattern is already
completing.

---

**TR-6 (HARD): Invalidation Levels — Count Must Be Abandoned If Violated**

Beyond the stop, certain price levels represent *count invalidations* — not just
trade stops but structural resets requiring full re-analysis [LF-27, MEW Ch. 5]:

| Invalidation event | Structural implication |
|-------------------|----------------------|
| Price closes above the terminal's *origin* (not just the peak) | The entire terminal label is wrong; re-label the entire sequence from the terminal's starting pivot |
| Wave 2 retraces > 100% of wave 1 (trending impulse) | The count is invalid; wave 1 must be relabelled as part of a correction |
| Wave 4 overlaps wave 1 (trending impulse) | The impulse is invalid; it is a terminal or a complex correction |
| Wave 3 is the shortest of waves 1, 3, 5 | The impulse is invalid |
| Post-terminal: price returns to wave-5's peak without first retracing to the 2-4 line | Terminal not confirmed; may still be in an extending wave 5 |

---

**TR-7 (FIRM): Middle-Pattern Management — Avoid Trading the Ambiguous Interior**

Neely explicitly cautions against trading in the *middle phase* of a developing pattern
[NW-1080 — implied from pattern complexity teaching]:

> The middle of a pattern is where multiple counts are most plausible and trading is
> most dangerous.

**Operational rule:** do not enter a new directional trade while:
- The pattern has not yet reached at least wave 3 or wave C equivalent (i.e., the
  post-midpoint portion).
- The Rule of Reverse Logic (FR-9) selects a count whose completion fraction is < 0.40
  (the pattern is less than 40% complete by price projection).

Wait for the pattern to reach late-stage development before trading it.

---

**TR-8 (FIRM): Position Sizing and Time Management**

Neely addresses risk control through time as well as price [NW-RIVER, implied from
three-prong process]:

- **Time-based exit:** if the expected next wave has not begun to materialize within the
  S&B time window (FR-6: [N/3, 3N] bars after entry), consider exiting on time alone
  even without the stop being hit. A wave that has consumed > 3× the expected time is
  likely a higher-degree structure that will dominate the position.

- **Risk per trade:** Neely River specifically addresses *unemotional* trade management.
  The implication for sizing: risk per trade should be defined *before* entry, fixed, and
  not adjusted based on the wave count's attractiveness. Wave-count confidence does not
  override position-sizing discipline.

---

## 3. The Full Forecasting Logic Flow

Integrating all rules above, the NEoWave forecasting decision path for a just-completed
pattern is:

```
1. Pattern identified (bottom-up construction, channeling passed).
        |
2. Rule of Reverse Logic (FR-9): is there a less-complete valid count?
        — If YES: prefer less-complete count; wait for more data.
        — If NO: proceed.
        |
3. Self-defining time limit check (FR-11): is pattern still within S&B time bounds?
        — If FAIL: count must be revised (pattern is higher degree or x-wave present).
        — If PASS: proceed.
        |
4. Post-pattern context (FR-10): is the pattern a terminator, connector, or concluding?
        — Determines whether next move is same-degree continuation, connector, or
          higher-degree reversal.
        |
5. Direction determination:
        — Trending impulse → correction opposite direction (FR-1).
        — Terminal impulse → immediate full retrace (FR-2).
        — Correction → impulse in prior trend direction (FR-3).
        — Triangle → thrust in prior trend direction (CC-6).
        — Diametric → sharp thrust in opposite direction to wave g (CC-7).
        |
6. Price target: Fibonacci projection from pattern endpoint (FR-5).
7. Time window: S&B window [N/3, 3N] bars from pattern endpoint (FR-6).
        |
8. Monitor for Stage 1 confirmation (CC-1):
        — 2-4 trendline break in < wave-5 time (or equivalent for other patterns).
        — Until Stage 1: NO TRADE (TR-1).
        |
9. Two-consecutive-bar entry filter (TR-2): count bars, wait for second close.
10. Entry: position in confirmed direction, stop at invalidation level (TR-4).
11. Manage: first target → move stop to breakeven (TR-5).
              second target → full exit or trail stop.
12. Time check: if N/3 bars elapsed without Stage 1, re-examine count.
               if 3N bars elapsed after entry without reaching target, time-based exit (TR-8).
```

---

## 4. Gap Analysis — What Our Engine Lacks

The following table maps each rule above to the current engine status in `wavelib/`. All
construction gaps (monowave labels, rollback, compaction) are already catalogued in
`11_neowave_techniques.md` — this table focuses exclusively on the *forecasting and
trading* layer.

| Rule | Engine Status | Gap Description |
|------|---------------|-----------------|
| **CC-1** Stage 1 / Stage 2 timing | `two_four_confirmation()` IMPL | Stage 1/2 are computable but not called automatically on new bars. Needs `ConfirmationQueue.update(bar)`. |
| **CC-2** Type 1 / Type 2 confirmation | MISSING | No classification of which confirmation type to use. No expanding-bias warning for Type 2. |
| **CC-3** "Moves further and faster" | MISSING | No measurement of largest counter-trend leg of prior pattern. Universal confirmation signal not implemented. |
| **CC-4** Pre-constructive filter | PARTIAL | `elliott_hard_rules()` checks W4/W1 overlap and W2 < 100%. Time rules (W2 ≥ W1, W4 ≥ W3 in bars; W2 ≤ 3×W1 time) missing. |
| **CC-5** Post-correction thrust | MISSING | No function checks for expected thrust after flat/zigzag completion. No time window monitoring. |
| **CC-6** Post-triangle thrust | MISSING | `triangle_thrust()` exists in `toolkit.py` for price target but no timing check (≤ shortest-leg duration). |
| **CC-7** Post-diametric behaviour | MISSING | No function implements the post-g speed/size test or degree-elevation test. |
| **CC-8** Post-terminal retrace | PARTIAL | `terminal_retrace_window()` computes time bias correctly. Framing issue: origin price should not be presented as timed forecast. |
| **CC-9** Behaviour over structure | MISSING | No mechanism updates a pattern's confirmation status when post-pattern behaviour fails. |
| **FR-1** Post-impulse correction direction/size | MISSING | No function projects correction direction or minimum/maximum retracement range from a completed impulse. |
| **FR-2** Post-terminal full retrace | PARTIAL | Full-retrace requirement is documented in `terminal_retrace_window()` but is framed as a bias window rather than a hard rule. |
| **FR-3** Post-correction impulse minimum size | MISSING | No function computes minimum required impulse size keyed to correction type (161.8% rule for double threes). |
| **FR-4** Pattern context (terminator / connector) | MISSING | Engine does not determine whether a pattern is in wave-2/4 position, wave-B position, or x-wave position. No contextual role assignment. |
| **FR-5** Fibonacci price targets | PARTIAL | `project_wave5()` in `toolkit.py` handles wave-5 targets. Wave-3 targets and post-correction targets (zigzag/flat) missing. |
| **FR-6** S&B time projection window | MISSING | The [N/3, 3N] window is computable from any completed wave but no function generates it. |
| **FR-7** Sub-wave duration limits | MISSING | Hard time limits (e.g., wave-C ≤ time(A)+time(B)) not checked during in-progress pattern monitoring. |
| **FR-8** Progress labels and in-pattern direction | MISSING | No progress-label system tracking "currently in wave-4, wave-5 next." |
| **FR-9** Rule of Reverse Logic | MISSING | No `completion_fraction` property on candidates; no `rank_by_reverse_logic()` function. |
| **FR-10** Post-pattern contextual role | MISSING | Same as FR-4: no contextual role assignment. |
| **FR-11** Self-defining time limit | MISSING | No auto-check that current pattern has not exceeded 3× prior pattern's time. |
| **TR-1** No trade until Stage 1 | MISSING | No trading gate implemented. |
| **TR-2** Two-consecutive-bar entry filter | MISSING | No stateful bar counter for confirmation bars. |
| **TR-3** Forecasting vs trading separation | STRUCTURAL | The engine is correctly analysis-only (`confluence.py` + `backtest.py` layer). The trading-params synthesis function `neowave_trade_params()` (see GAP-2 in `11_neowave_techniques.md`) is still MISSING. |
| **TR-4** Stop at logical invalidation | MISSING | Invalidation levels are implicit in `elliott_hard_rules()` but not surfaced as a `stop_price` output. |
| **TR-5** Fibonacci target exit | PARTIAL | `project_wave5()` handles one target. Multi-level target table (conservative + full extension) missing. |
| **TR-6** Hard invalidation levels | MISSING | No function computes and reports the full invalidation-level set per pattern. |
| **TR-7** Avoid mid-pattern trading | MISSING | No completion-fraction guard before trade-signal generation. |
| **TR-8** Time-based exit | MISSING | S&B time window [N/3, 3N] not generated; no time-expiry exit signal. |

### Priority Summary

Based on impact on forecasting correctness and user-facing value:

1. **CRITICAL:** FR-6 (S&B time projection window) + FR-7 (sub-wave time limits) —
   together these make the "when" forecast possible. Low implementation effort.

2. **CRITICAL:** CC-3 ("moves further and faster") — the universal confirmation signal
   that gates all other signals. Requires measuring the largest counter-trend leg inside
   each identified pattern.

3. **HIGH:** FR-5 completion (wave-3 targets, post-correction thrust targets) + TR-4/TR-6
   (stop and invalidation levels as output fields). These complete the trading-params
   output (GAP-2 in `11_neowave_techniques.md`).

4. **HIGH:** FR-9 (Rule of Reverse Logic) — completion fraction on WaveNode candidates.
   Stateful but straightforward once FR-5 targets are computed.

5. **MEDIUM:** CC-4 completion (W2/W4 time rules), CC-5/CC-6 (post-correction/triangle
   thrust), FR-8 (progress labels). These improve the confirmation layer.

6. **DEFERRED:** CC-7 (post-diametric), FR-3 (post-correction minimum), FR-10/FR-11
   (contextual role, self-defining limit). These require the full compaction hierarchy
   (Task 1–3 in `02_neowave_neely.md`) before they can be implemented reliably.

---

## 5. The 5 Most Important NEoWave Forecasting Rules

Ranked by their impact on prediction accuracy and by how uniquely they distinguish
NEoWave from classical Elliott Wave:

**Rule 1 — Two-Stage Timing Confirmation (CC-1)**
No pattern is complete until the 2-4 trendline is broken in *less time than wave 5 took
to form*. This single rule eliminates premature trading of unconfirmed patterns and is
the foundation of NEoWave's claim to objectivity. Without it, the analyst is still in
the realm of "this looks like it might be done."

**Rule 2 — Behaviour Over Structure (CC-9)**
Post-pattern price behaviour overrules structural labelling. If the market refuses to
confirm the label, the label is wrong. This makes NEoWave falsifiable: the count changes
when data contradicts it, not when the analyst loses confidence. A system that cannot
be falsified is not a prediction system.

**Rule 3 — Rule of Similarity and Balance for Time (FR-6)**
The [N/3, 3N] time window is NEoWave's *duration forecast*. Every completed wave of N
bars predicts that the next same-degree wave will complete within N/3 to 3N bars. This
is the mechanism behind the "when" forecast — entirely absent from classical Elliott
Wave. It applies recursively at every degree.

**Rule 4 — Rule of Reverse Logic (FR-9)**
When multiple counts are valid, prefer the *least complete* one. This prevents the
common failure of declaring patterns done prematurely. Neely claims it works 100% of
the time when applied consistently. It is also the rule that keeps analysts honest —
the least attractive count (the one that requires the most patience) is usually the
correct one.

**Rule 5 — Self-Defining Time Limits (FR-11 + FR-7)**
A pattern at degree N cannot consume more time or price than a pattern at degree N+1.
Individual sub-waves carry hard time limits (wave C ≤ time(A) + time(B), etc.). These
rules produce *real-time falsification signals* during pattern development — if an
in-progress wave is approaching a limit, the analyst knows the pattern must either
resolve imminently or be re-labelled as higher degree. Classical EW has no equivalent.

---

## Sources (cited URLs, in full)

- [neowave.com — What is NEoWave?](https://www.neowave.com/what-is-neowave.asp)
- [neowave.com — What is NEoWave Analysis?](https://www.neowave.com/what-is-neo-wave-analysis.asp)
- [neowave.com — NEoWave vs Elliott Wave](https://www.neowave.com/what-is-the-difference-between-neo-wave-and-elliott-wave.asp)
- [neowave.com — Mastering Elliott Wave Chapter 1 (free)](https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp)
- [neowave.com — Rule of Reverse Logic](https://www.neowave.com/neowave-rules-of-reverse-logic.asp)
- [neowave.com — Neely River Trading Technology](https://www.neowave.com/NEELY-RIVER/)
- [neowave.com QA-2 — Time limits for wave-b of a Flat](https://www.neowave.com/qow/qow-archive-2.asp)
- [neowave.com QA-17 — Can wave-2 take less time than wave-1?](https://www.neowave.com/qow/qow-archive-17.asp)
- [neowave.com QA-19 — Structure vs Behaviour](https://www.neowave.com/qow/qow-archive-19.asp)
- [neowave.com QA-22 — Confirming the end of wave-5](https://www.neowave.com/qow/qow-archive-22.asp)
- [neowave.com QA-32 — Does MEW cover all S&B applications?](https://www.neowave.com/qow/qow-archive-32.asp)
- [neowave.com QA-78 — S&B: price or time — both required?](https://www.neowave.com/qow/qow-archive-78.asp)
- [neowave.com QA-303 — 2-4 trendline placement](https://www.neowave.com/qow/qow-archive-303.asp)
- [neowave.com QA-474 — What happens after diametric wave-G?](https://www.neowave.com/qow/qow-archive-474.asp)
- [neowave.com QA-1006 — Extension rule: 161.8% requirement](https://www.neowave.com/qow/qow-archive-1006.asp)
- [neowave.com QA-1080 — Trading during middle phase of a pattern](https://www.neowave.com/qow/qow-archive-1080.asp)
- [neowave.com QA-1109 — Two types of confirmation](https://www.neowave.com/qow/qow-archive-1109.asp)
- [neowave.com QA-1285 — Why trading deviates from wave forecast](https://www.neowave.com/qow/qow-archive-1285.asp)
- [neowave.com QA-3518 — Supplemental Price and Time](https://www.neowave.com/qow/qow-archive-3518.asp)
- [neowave.com QA-3592 — Time limits for wave 2 and wave 4](https://www.neowave.com/qow/qow-archive-3592.asp)
- [neowave.com QA-5161 — Post-triangle thrust timing](https://www.neowave.com/qow/qow-archive-5161.asp)
- [neowave.com Stage 1 & Stage 2 Confirmation achieved (blog post)](https://www.neowave.com/tradingblog/blog.asp?bid=157)
- [neowave.com Elliott Wave Rules (blog post)](https://www.neowave.com/tradingblog/blog.asp?bid=71)
- [LiteFinance — NeoWave Part 16: Extended Rules of Logic for Zigzags and Flats](https://www.litefinance.org/blog/for-professionals/neowave-part-16-extended-rules-of-logic-for-zigzags-and-flat-corrections/)
- [LiteFinance — NeoWave Part 17: Extended Rules of Logic for Complex Corrections](https://www.litefinance.org/blog/for-professionals/neowave-part-17-extended-rules-of-logic-for-complex-corrections-exceptions-to-the-rules-2020-05-07)
- [LiteFinance — NeoWave Part 21: Channeling in Impulses and Fibonacci Relationships](https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships)
- [LiteFinance — NeoWave Part 27: Practical Trading Strategy](https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/)
- [ForexTalker — NeoWave Impulse Rules of Logic](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-price-impulses-the-rules-of-the-stretched-wave-equality-alternation-overlap-the-rules-of-logic/)
- [Scribd — NeoWave Part 12: Impulsions and Rules to Analyze Impulse Patterns](https://www.scribd.com/document/839672305/Part-12-Impulsions-and-the-Rules-to-Analyze-Impulse-Wave-Patterns-NeoWave-Theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 13: Corrections and Rules to Identify Them](https://www.scribd.com/document/839672297/Part-13-Corrections-Rules-to-identify-a-correction-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Patterns for Traders (Part 17)](https://www.scribd.com/document/502312113/17-Dear-friends)
- [Scribd — Real-Time Trading Using NeoWave Concepts, Glenn Neely](https://www.scribd.com/document/500258793/1)
- [ebrary.net — Triangle and Diametric patterns chapter](https://ebrary.net/299888/education/triangle)
- [Ewace_2026 repo — docs/research/02_neowave_neely.md](../02_neowave_neely.md)
- [Ewace_2026 repo — docs/research/deep/05_neowave_full_algorithm.md](../deep/05_neowave_full_algorithm.md)
- [Ewace_2026 repo — docs/research/deep/11_neowave_techniques.md](../deep/11_neowave_techniques.md)
