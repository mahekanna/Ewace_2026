# 02 — NeoWave (Glenn Neely) Methodology
### Canonical reference for `wavelib` NeoWave fidelity

**Status:** research baseline — 2026-06-05  
**Cross-references:** doc 01 (Elliott Wave fundamentals), `wavelib/rules.py`, `wavelib/toolkit.py`

---

## 1. Scope & Sources

This document is the canonical place for NeoWave theory as it applies to the `Ewace_2026`
engine. It covers:

- The bottom-up construction hierarchy (monowave → polywave → multiwave → macrowave)
- Construction order: channeling FIRST, then structure
- Rule of Similarity & Balance (price AND time; the 1/3–3× band)
- Retracement logic: Neely's seven retracement rules, their Fibonacci breakpoints, and
  the six conditions (a–d) attached to later rules
- Channeling specifics: 0-2 / 2-4 / 1-3 lines; throw-over and fell-short; impulse
  confirmation sequence
- Terminal impulsions: contracting and expanding/irregular; the fast-full-retrace
  expectation and its TIMING rule; why the engine's `terminal_retrace_window` over-
  projects on AVGO
- The complex-correction zoo done properly: diametric (7 legs a–g; bowtie/diamond),
  symmetrical (9 legs), neutral triangle, x-wave constraints
- Post-constructive rules of logic (Rule of Reverse Logic)
- An audit of `wavelib/rules.py` and `wavelib/toolkit.py` against this theory
- A concrete build roadmap with causal-only flags

**Primary sources consulted:**

| Source | Coverage |
|---|---|
| Glenn Neely, *Mastering Elliott Wave* (v2, 1990) | Full canonical text; cited throughout |
| neowave.com Q&A archive | Hundreds of clarifying Q&As from Neely himself |
| LiteFinance 27-part NeoWave series (litefinance.org) | Systematic worked-example coverage of every rule set |
| ForexTalker NeoWave series (forextalker.com) | Detailed coverage of conditions a–d and rollback rules |
| ebrary.net — Triangle & Diametric chapter | Diametric/symmetrical pattern reference |
| wavesstrategy.com — NeoWave vs Elliott Wave | Terminal/trending impulse comparison |
| niftywaveindia.blogspot.com — Diametric patterns | Pattern shape examples |

All inline citations point to the URLs listed in § Sources.

---

## 2. Theory

### 2.1 Bottom-Up Construction Hierarchy

NeoWave is **emphatically bottom-up**. Before any pattern label can be trusted, the analyst
must work from the smallest observable unit upward. This order is both a methodology and
a correctness guarantee — skipping levels produces mislabeled degrees and wrong pattern
calls. [[LiteFinance intro]](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/),
[[neowave.com — what is NeoWave]](https://www.neowave.com/what-is-neowave.asp)

#### Level 1 — Monowave
A **monowave** is the most primitive unit: a single directional price movement that begins
and ends at a change in direction. On a properly constructed chart, each monowave has
a unique start pivot and end pivot with no intervening reversal that exceeds the threshold
used for chart construction. The analyst assigns each monowave a **structure label**
(`:5`, `:3`, `:F3`, `:c3`, `:L5`, `:s5`, `:sL3`, `:L3`) based on the seven retracement
rules applied to neighbouring monowaves (m−2, m−1, m0, m1, m2, m3 in Neely's notation).
[[neowave.com — structure labels]](https://www.neowave.com/qow/qow-archive-25.asp),
[[LiteFinance part 3 — retracement rule 1]](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)

**Key structural distinction** (not in `wavelib`):

- `:5` labels (motive) — completely retrace the **prior** monowave faster than it took to
  form; cover more price per time unit; followed by a `:3`-labelled wave of less violence.
- `:3` labels (corrective) — retrace no more than 61.8 % of a prior monowave; consume
  equal or greater time than the prior monowave; exhibit equal or greater complexity.

The structure label is what allows the engine to determine, from the *bottom up*, whether
a given monowave is part of a motive or corrective series — before any pattern is named.

#### Level 2 — Polywave
A **polywave** is a group of 3 or 5 monowaves that, taken together, form a standard
Elliott corrective (3 monowaves) or impulsive (5 monowaves) pattern. Polywaves are
identified by locating groups of adjacent monowaves that:
  1. Satisfy the appropriate retracement rules within the group.
  2. Pass the Rule of Similarity & Balance (§2.3).
  3. Can be given a single structure label that compacts the group for the next level up.

[[neowave.com — compaction]](https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp),
[[LiteFinance — compaction procedures]](https://www.litefinance.org/blog/for-professionals/neowave-part-18-rules-of-complexity-and-balance-compaction-procedures-power-ratings/)

#### Level 3 — Multiwave
A **multiwave** is a group of 3 or 5 polywaves that form a standard Elliott pattern at
the next higher degree. The compaction process repeats: the entire polywave is treated as
a single structure unit, assigned its own label (`:3` or `:5`), and becomes an input to the
multiwave analysis. [[neowave.com — analysis methodology]](https://www.neowave.com/what-is-neo-wave-analysis.asp)

#### Level 4 — Macrowave
A **macrowave** is a group of 3 or 5 multiwaves. The same compaction logic applies again.
The hierarchy is explicitly fractal — the rule sets that govern monowaves govern every
higher level identically. [[LiteFinance intro]](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)

**The engine entirely lacks this hierarchy.** It begins at what would be the polywave or
multiwave level (hand-picked pivots), assuming the degree is already known. This is the
single largest theoretical gap — see § 3.

---

### 2.2 Construction Order: Channeling FIRST

This is one of Neely's most explicit inversions of classic Elliott practice. In orthodox
Elliott Wave, you identify the count and then draw channels to confirm it. **In NeoWave,
you construct and evaluate channels before trusting the count.**

The logic: channel behaviour is an independent, observable fact about price. If a
candidate count's implied channels are violated by price (e.g., wave 3 breaks below the
0-2 trendline, or wave 5 never even approaches the 1-3 upper channel), that is evidence
against the count — obtainable without having committed to a label first.
[[neowave.com — channeling importance]](https://www.neowave.com/qow/qow-archive-273.asp),
[[LiteFinance — channeling in impulses]](https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships/)

#### The Four Channeling Steps (impulse)

**Step 1 — 0-2 trendline.**  
Draw a line from the origin of wave 1 (pivot 0) through the end of wave 2. This line
helps locate the true end of wave 2. A *clean* 0-2 line means wave 2 ends exactly on or
near this line, or wave 2 finishes *after and higher than* the last touch. If price breaks
the 0-2 line immediately after what is assumed to be the wave-2 low, the wave-2 end must
be moved later. No segment of a valid wave 3 should break the 0-2 trendline significantly
downward (in a bull impulse).
[[neowave.com — 0-2 trendline]](https://www.neowave.com/qow/qow-archive-273.asp)

**Step 2 — 2-4 trendline.**  
Draw a line through the ends of wave 2 and wave 4 (across their *endpoints*, not their
intrawave extremes). This is the **most important confirmation line** in NeoWave:

- No part of wave 3 should break the 2-4 line (this hard rule is unique to NeoWave;
  classical EW does not mandate it).
- No point of wave 5 can break the 2-4 line.
- Impulse pattern **confirmed complete** only when price decisively penetrates the 2-4
  line in **less time than wave 5 took to form** (Stage 1 confirmation).
- Stage 2 confirmation: wave 5 entirely retraced in no more time than it took wave 5 to
  form.
[[neowave.com — 2-4 trendline placement]](https://www.neowave.com/qow/qow-archive-303.asp),
[[neowave.com — confirming wave 5 end]](https://www.neowave.com/qow/qow-archive-22.asp)

**Step 3 — 1-3 upper channel.**  
Draw a line parallel to the 2-4 line, anchored at the top of wave 1 (for an uptrend). A
second parallel line through the top of wave 3 defines the upper boundary. Wave 5 is
expected to terminate near this upper channel, but its actual behaviour reveals the
impulse character:

- **Throw-over:** wave 5 peak exceeds the 1-3 line — blow-off exhaustion, often with
  widening spread; sharp reversal expected.
- **Fell short / truncated 5th:** wave 5 peak fails to reach the 1-3 line — weakness,
  often a truncated wave 5, also signals exhaustion but of a different flavour (wave 3
  already consumed all the energy).

**Step 4 — Confirming the channel.**  
After the pattern completes, the 2-4 break timing rule (Step 2, Stage 1 and Stage 2) is
the hard confirmation signal that the motive sequence is done and a corrective phase has
begun.

> **Note for the engine:** The engine (`two_four_test`, `throwover_test`) performs Steps 2
> and 3 but does NOT enforce the timing rule for 2-4 penetration. The `two_four_test`
> function returns WARN/PASS depending on whether the line is *currently broken* — a
> static snapshot — rather than whether it was broken in less time than wave 5 took to
> form. This is a fidelity gap.

---

### 2.3 Rule of Similarity & Balance (S&B)

The Rule of Similarity & Balance is Neely's primary mechanism for **degree assignment**.
It is not just a plausibility check — it is how you determine whether two adjacent waves
belong to the same degree. Any wave count that violates it is "destined to fail."
[[neowave.com — S&B importance]](https://www.neowave.com/qow/qow-archive-32.asp)

**Exact definition:**

> For two adjacent waves to be considered the same degree:
>
> - **Price Similarity:** the smaller of the two must be no less than **1/3 (≈ 33 %)** the
>   vertical price coverage of the larger.  The upper bound is therefore **3×** the smaller.
>   Band: [1/3, 3×].
>
> - **Time Similarity:** the shorter-duration wave must be no less than **1/3** the time
>   consumed by the longer. Band: [1/3, 3×].
>
> - **Complexity Similarity (tertiary):** the less complex group must contain at least
>   **1/3** the monowave count of the more complex group. A pattern that exceeds 3×
>   the price/time/complexity of a same-degree candidate is definitionally a higher degree.

[[neowave.com — both required or just one?]](https://www.neowave.com/qow/qow-archive-78.asp)

**Critical nuance (missed by the engine):**  
For degree confirmation, at least *one* element (price OR time) must be satisfied.
However, for a pattern to be considered *well-formed* at the same degree, both should
ideally be in band. A violation of price similarity that is rescued only by time similarity
is a warning of a complex or hidden structure. A violation of *both* means the waves are
definitively different degrees and the count must be revised.

**What a violation implies:**
1. Adjacent waves are different degrees (most common cause).
2. There is a hidden x-wave between them that, once identified, restores balance.
3. The pattern is part of a complex correction (diametric or symmetrical) where
   non-adjacent legs are compared, not adjacent ones.

The code's `similarity_and_balance()` in both `rules.py` (Section E) and `toolkit.py`
(§ 3) correctly implements the 1/3–3× price AND time check with those exact bounds.
However, it is applied only to wave2 vs wave4 inside `validate_impulse()` — one pair.
Full Neely practice applies S&B to *every adjacent corrective pair*, including within
corrections (A vs C, legs of a triangle, etc.).

---

### 2.4 Rule of Proportion

> A child wave (subwave) should not exceed the size of the parent wave it belongs to.
> Specifically, no subwave should be longer in price (or time) than the full parent leg
> unless an extension is unfolding (which must be the longest wave, ≥ 161.8 % of the
> next longest motive wave).

[[neowave.com — extension required ≥ 161.8 %]](https://www.neowave.com/qow/qow-archive-1006.asp)

**Rule of Extension** (hard rule in NeoWave, guideline in classical EW): In a trending
impulse, the extended wave *must* be at least 161.8 % of the next-longest motive wave.
This is a **hard** rule in NeoWave, not a preference. The code treats it only as a
guideline (WARN) — that is appropriate for a classical EW check but should be upgraded to
FAIL if the pattern claims to be a NeoWave trending impulse.

---

### 2.5 Retracement Logic: The Seven Rules

Neely encodes wave identity in a decision-tree of seven retracement rules. The rules take
**m0** (the wave immediately before m1), **m1** (the current wave being labelled), **m2**
(the following wave), and sometimes **m3** as inputs.

The breakpoints are the Fibonacci retracement levels of m1 by m2:

| Rule | m2 / m1 ratio (retrace of m1) | What it signals about m1 |
|------|-------------------------------|--------------------------|
| Rule 1 | m2 < 38.2 % of m1 | m1 = extended 3rd wave; m2 = wave 4 (shallow 4th after an extension) |
| Rule 2 | 38.2 % ≤ m2 < 61.8 % of m1 | m1 = 1st or 5th wave; m2 = standard 2nd or 4th; depends on conditions a, b |
| Rule 3 | 61.8 % ≤ m2 ≤ 100 % of m1 | m1 = a-wave or 1st; m2 = sharp 2nd / B / X; has conditions a, b, c |
| Rule 4 | 61.8 % ≤ m2 ≤ 100 % (extended) | Overlap/subdivide variant; conditions c, d, e |
| Rule 5 | 100 % < m2 ≤ 161.8 % of m1 | m2 is NOT a retracement → trend change or larger structure; condition a applies if m0 < 100 % of m1 |
| Rule 6 | 161.8 % < m2 ≤ 261.8 % of m1 | Strong trend reversal; condition a: m0 < 100 % of m1 |
| Rule 7 | m2 > 261.8 % of m1 | Extreme reversal; possible x-wave or missing wave; condition d: m0 > 261.8 % of m1 |

[[Scribd — retracement rule 4]](https://www.scribd.com/document/502300644/7-NeoWave-theory-by-Glenn-Neely),
[[Scribd — rules 5 & 6]](https://www.scribd.com/document/502311042/9-NeoWave-theory-by-Glenn-Neely),
[[Scribd — rule 3]](https://www.scribd.com/document/502299837/5-The-NeoWave-theory-by-Glenn-Neely),
[[ForexTalker — conditions a–d for rule 7]](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-a-b-c-and-d-for-the-seventh-rule/),
[[ForexTalker — rule 2 conditions]](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-the-second-rule-for-the-ratio-of-wavelengths-and-conditions-for-its-implementation/)

#### Conditions a–d (attached to Rules 5–7)

Each higher-numbered rule carries sub-conditions that subdivide based on the **m0/m1
ratio** (the wave *before* m1 vs m1) and the internal complexity of m2:

- **Condition a:** m0 < 100 % of m1; m2's subwave count ≤ 3 monowaves → labels pointing
  toward the end of a corrective sequence or an x-wave.
- **Condition b:** m0 between 100 % and 161.8 % of m1; m2 ≤ 3 monowaves or is multi-wave
  → labels pointing toward the centre of a complex correction.
- **Condition c:** m0 between 161.8 % and 261.8 % of m1 → m1 is likely a corrective
  segment inside a larger complex correction.
- **Condition d:** m0 > 261.8 % of m1 → m1 is almost certainly the last segment of a
  trending impulse or a small x-wave in a multi-x complex combination.

[[ForexTalker — rollback rules & rule 1]](https://forextalker.com/neowave-wave-theory-by-glenn-neely-rollback-rules-and-the-first-rule-of-wavelength-relationships/)

#### Rollback Rules

Before applying the retracement rules, Neely specifies **rollback rules** that adjust the
monowave endpoint if price briefly exceeds a prior pivot before reversing. These are
applied *immediately after* monowave endpoint detection, prior to any structural labelling.
Their purpose is to prevent false pivot boundaries from contaminating all downstream
analysis. The engine has no rollback logic — the ZigZag detector (`toolkit.zigzag`)
uses a simple percentage-reversal that roughly approximates this but does not implement
the exact one-time-unit rollback specification.

#### Current Code vs Neely's Tables

`rules.py:retracement_logic()` and `toolkit.py:retracement_logic()` both implement a
simplified 3-band version:

```
< 38.2 %  →  extended 3rd / in a 4th
38.2–61.8 %  →  1st or 5th / normal 2nd or 4th
61.8–100 %  →  sharp 2nd / B / X
> 100 %   →  trend change / larger structure
```

Neely's actual system has **seven** breakpoints (at 38.2 %, 61.8 %, 100 %, 161.8 %,
261.8 %) with conditions a–d that pivot on the m0/m1 ratio and m2 internal structure.
The code's 3-band simplification is correct for the most commonly encountered range
(38.2–100 %) but silently misclassifies waves that fall in Rules 5–7 territory (deep
reversals, large x-waves, post-extension resets). The function is marked `REF` (reference)
rather than `PASS/FAIL`, which is honest but means no machine enforcement exists.

---

### 2.6 Channeling: Full Specification

*(Summarises § 2.2 and adds specifics not covered there.)*

**0-2 trendline application:**  
The most important early use of the 0-2 line is locating the true end of wave 2. If price
breaks the 0-2 line and then fails to continue, the assumed wave-2 endpoint is wrong and
must be revised rightward. This is an active channel-based *correction* to the pivot
labelling — not a passive confirmation check.

**2-4 trendline placement:**  
Neely is explicit that the 2-4 line should pass through the **end** of waves 2 and 4 (the
corrective endpoints), NOT through the most extreme intrawave points. The engine's
`two_four_test()` connects `w2` and `w4` as `Pivot` objects, which are endpoints — this is
correct for the function signature, but the caller must pass the endpoint pivots, not the
absolute highs/lows.
[[neowave.com — 2-4 trendline placement]](https://www.neowave.com/qow/qow-archive-303.asp)

**The two-stage confirmation sequence (hard timing rules):**

| Stage | Condition | Interpretation |
|-------|-----------|----------------|
| Stage 1 | Price returns to 2-4 trendline in **< time of wave 5** | Primary impulse is over |
| Stage 2 | All of wave 5 is retraced in **≤ time of wave 5** | Confirmed end, next larger degree move begins |

These are **timing constraints**, not just price level tests. The engine lacks both.

**Impulse-complete vs impulse-in-progress:**  
Until the 2-4 line is broken on the timing schedule above, the impulse is *not confirmed
complete* even if wave 5 has extended far beyond its projection. AVGO ($495 top on
2026-06-03, 2-4 line ~$301, still unbroken as of 2026-06-05) is an exact illustration:
confluence = 1/7 because structural completion is not yet confirmed.
[[neowave.com — pre-break confirmation]](https://www.neowave.com/qow/qow-archive-108.asp)

---

### 2.7 Terminal Impulsions

A **terminal impulsion** (called an *ending diagonal* in classical EW) is a 5-wave motive
sequence where each sub-wave is corrective (3-3-3-3-3 structure), and wave 4 overlaps
wave 1. It appears at the end of a trend — in the 5th-wave position of a larger impulse,
in the C-wave of a flat or zigzag, or occasionally as the entire 5th wave of a very
extended pattern.

[[tradingfinder.com — terminal vs trending impulse]](https://tradingfinder.com/education/forex/impulse-waves/),
[[neowave.com — wave-2 and wave-4 timing in terminals]](https://www.neowave.com/qow/qow-archive-3782.asp)

#### Distinguishing Features vs a Trending Impulse

| Feature | Trending Impulse | Terminal Impulsion |
|---------|-----------------|-------------------|
| Sub-wave structure | 5-3-5-3-5 | 3-3-3-3-3 |
| Wave 4 / wave 1 overlap | Never | Always |
| Wave 2 duration vs wave 1 | Must be ≥ wave 1 | IS allowed < wave 1 |
| Wave 4 duration vs wave 3 | Must be ≥ wave 3 | IS allowed < wave 3 |
| Extreme alternation (waves 2 & 4) | Rare | Common ("extreme alternation") |
| Contracting shape | No requirement | Typical; waves contract w5 < w3 < w1 |
| Expanding shape | Only with 3rd-extension | Less common but valid |

**Shape subtypes:**

- **Contracting terminal:** each motive wave is shorter than the previous (w1 > w3 > w5);
  the two boundary trendlines converge. This is the classic "ending wedge." Most common.
- **Expanding/irregular terminal:** waves expand (w5 > w3 > w1); trendlines diverge.
  Less common; often called an "irregular" terminal.

#### The Fast-Full-Retrace Expectation

Once a terminal is complete, Neely specifies:

> The entire terminal must be **completely retraced** back to its origin, and this retrace
> should occur in **less time than the terminal took to build**.

The exact timing language from Neely is framed as a *bias* rather than a mechanistic
guarantee. It reads in practice: if the pattern took *N* bars to form, expect the retrace
to complete in roughly *N/4 to N/2* bars. The most common completion zone is the **1/4 to
1/2 build-time range**, with 1/3 as the modal expectation.
[[neowave.com — terminal retrace timing]](https://www.neowave.com/qow-search.asp?dowhat=searchqow&searchterms=terminal),
[[LiteFinance — terminal impulse progress labels]](https://www.litefinance.org/blog/for-professionals/neowave-part-20-application-of-progress-labels-to-terminal-impulses/)

#### Why `terminal_retrace_window` Over-Projected on AVGO

The engine's `terminal_retrace_window(build_days, top_t)` in both `rules.py` and
`toolkit.py` computes:

```
retrace_complete_date = top_t + build_days × frac × 86400   for frac ∈ {0.25, 0.33, 0.5}
```

This gives **time targets** for *when the retrace should finish*. It says **nothing about
price depth**. The engine's demo output labelled the target as "retrace-to-$290" — that
price target comes from the terminal origin ($289.96), which is theoretically correct
(the origin is the full-retrace target) — but the engine treated it as a near-term
expected price, whereas Neely frames the origin as a **directional bias** ("the retrace
*should eventually* reach the origin") without specifying that it must do so in the same
fraction of build time.

The practical source of the over-projection: the AVGO terminal (4h) had `build_days ≈ 64`
(from 2026-03-30 to 2026-06-03). The 1/4-build-time window (`≈ 16 days`) would fall in
mid-June 2026. At that point, price was $385, not $290. Neely's actual expectation is
that **eventually** the origin is reached, not that the first 25 % of build time produces
a full retrace. The retrace **starts fast** (the 2-4 trendline break is Stage 1 signal)
but the full origin retrace can take considerably longer, especially when the 2-4 line
itself is not yet broken.

**Correct implementation**: the timing rule should be presented as a *window for
monitoring*, not a *price projection*. The 1/4–1/2 build time is when to watch for
evidence of the retrace accelerating. The origin price ($290 for AVGO) is the structural
*target* but carries no timing guarantee until the 2-4 line break provides Stage 1
confirmation.

#### Terminal Wave-2 Retrace Limit

A specific NeoWave constraint not in the code: in a terminal impulse, wave 2 is allowed
to retrace **up to 61.8 %** of wave 1 (not more, unlike a trending impulse where up to
99.9 % is allowed). This limits the size of the corrective sub-waves inside a terminal.
[[neowave.com — wave 2 retrace limit]](https://www.neowave.com/qow/qow-archive-1079.asp)

---

### 2.8 Complex Corrections: The Full Zoo

#### 2.8.1 Standard Corrections (3 legs)

Already documented in `wavelib/rules.py § C`. The key NeoWave refinements:

- **Zigzag (5-3-5):** B retraces ≤ ~61.8 % of A; C must surpass the end of A. The B-wave
  limit is a **hard** constraint in NeoWave (not a guideline). C should normally equal A
  or extend 1.618 × A.

- **Flat (3-3-5):** Regular flat: B ≈ A (80–100 %); C ≈ A. Expanded flat: B > A; C > A
  (often 1.618 × A). Running flat: B > A; C fails to reach the end of A (truncated C).

- **Post-pattern behaviour of corrections:** After any flat or zigzag, a thrust proportional
  to the correction's size is expected. Failing to see this thrust is a post-constructive
  clue that the label was wrong.

#### 2.8.2 Triangles (5 legs: a-b-c-d-e)

Triangles have each leg as a corrective (3-3-3-3-3 internally). Neely distinguishes:

- **Contracting triangle:** a > b > c > d > e in length; trendlines converge. Most common.
  Appears as wave 4, wave B, or wave X.
- **Expanding triangle:** a < b < c < d < e; trendlines diverge. Rarer.
- **Neutral triangle (NeoWave unique):** wave C is the *longest* leg; waves A and E tend
  toward equality (each is at least 38.2 %, typically 61.8–72 %, of C); the upper bound
  for C is 161.8 % of A (under volatile conditions up to 261.8 %). Channeling employs
  parallel lines through b-d ends, with a parallel through the end of wave a.
  [[neowave.com — neutral triangle]](https://www.neowave.com/qow/qow-archive-8.asp),
  [[neowave.com — neutral triangle C limit]](https://www.neowave.com/qow/qow-archive-3849.asp)
- **Barrier triangle:** one boundary is essentially horizontal; price "barriers" against it.
- **Post-triangle thrust:** the thrust out of any contracting or neutral triangle is
  approximately equal to the widest part of the triangle (wave a). The thrust typically
  completes in less time than the shortest triangle leg. There is a time limit:
  the post-pattern thrust should complete in no more time than the longest triangle leg.
  [[neowave.com — post-triangle thrust timing]](https://www.neowave.com/qow/qow-archive-5161.asp)

> **Note:** "Extracting triangle" was a term Neely used historically but later retired.
> He found it was not sufficiently precise. The underlying pattern is now described under
> the neutral triangle category with the wave-C extension.
> [[neowave.com — extracting triangle retired]](https://www.neowave.com/qow/qow-archive-923.asp)

#### 2.8.3 Diametric Formations (7 legs: a-b-c-d-e-f-g) — NeoWave Exclusive

The **diametric** is a 7-legged formation that does NOT involve any x-wave. It was
discovered by Neely circa 1992 (not in *Mastering Elliott Wave*). The defining character:
all seven legs are similar in **time** (and complexity), though not necessarily in price.
[[neowave.com — diametric definition]](https://www.neowave.com/qow/qow-archive-3.asp),
[[ebrary.net — triangle & diametric]](https://ebrary.net/299888/education/triangle)

**Two visual sub-shapes:**

| Sub-shape | Pattern of leg lengths | Visual shape |
|-----------|----------------------|--------------|
| Bowtie diametric | legs a, b, c, d expand; legs e, f, g contract | Hourglass / bowtie |
| Diamond diametric | legs a, b, c, d contract; legs e, f, g expand | Diamond shape |

The key: leg d is the pivot. In a bowtie, legs grow to d then shrink. In a diamond,
legs shrink to d then grow. Time similarity (not price equality) is the diagnostic test.

**Post-pattern:** after wave g completes, a thrust occurs in the opposite direction
roughly equal to the widest part of the pattern. The thrust is usually sharp.
[[neowave.com — post-diametric behaviour]](https://www.neowave.com/qow/qow-archive-474.asp)

#### 2.8.4 Symmetrical Formations (9 legs) — NeoWave Exclusive

The **symmetrical** is a 9-legged formation discovered by Neely circa 2001. It also does
NOT involve x-waves. It is the rarest of the advanced patterns.
[[neowave.com — symmetrical definition]](https://www.neowave.com/qow/qow-archive-5.asp)

Distinguishing features:
- Most legs possess similar **time, price, and complexity** (all three, unlike diametrics
  which require only time similarity).
- Advancing legs are similar to each other in price; declining legs are similar to each
  other in price — but the advancing and declining groups are *not* similar to each other
  (unlike the diametric where all legs are similar in time).
- Generally unfolds between parallel or near-parallel lines, with possible mild expansion
  or contraction throughout.

**Diagnostic trigger:** the more similarity in all three dimensions (price, time,
complexity) across adjacent waves, the higher the probability of a symmetrical. If
only time + complexity match, lean toward diametric. If only complexity, lean toward
triangle.
[[neowave.com — comparative identification]](https://www.neowave.com/qow/qow-archive-875.asp)

#### 2.8.5 X-Waves in Complex Combinations

An **x-wave** connects two corrective patterns in a complex (double or triple) combination.
Specific rules:
[[neowave.com — x-wave rules]](https://www.neowave.com/qow/qow-archive-7.asp),
[[neowave.com — x-wave complexity]](https://www.neowave.com/qow/qow-archive-94.asp)

1. **Size:** In a standard double/triple combination (W-X-Y, W-X-Y-X-Z), the x-wave is
   "small" — it retraces **less than 61.8 %** of the prior correction. In a "complex
   corrective rally" where the x-wave is large, it may retrace *more* than 61.8 % but
   this creates a distinctly different corrective character.

2. **Complexity upper bound:** x-wave complexity must be **no more complex** than the
   entire previous correction (W). It will typically be 1/3 to 2/3 the complexity of
   the preceding correction.

3. **Complexity lower bound:** x-wave complexity must be **no less complex** than the
   *least complex wave* of the preceding same-degree correction.

4. **x-wave cannot introduce a new degree:** it must be clearly smaller in both price and
   time than the corrections it connects.

**The engine's `x_wave_check()` returns `Status.REF` unconditionally** — a pure reference
stub with no computed logic. The 61.8 % retracement rule is checkable and should be
implemented.

---

### 2.9 Post-Constructive Rules of Logic

After constructing a pattern, NeoWave requires observing specific **post-pattern
behaviour** to confirm the label. This is what Neely calls Chapter 6's
"Post-Constructive Rules of Logic" — distinct from the construction rules themselves.
[[neowave.com — what is NeoWave]](https://www.neowave.com/what-is-neowave.asp),
[[neowave.com — Rule of Reverse Logic]](https://www.neowave.com/neowave-rules-of-reverse-logic.asp)

The two-stage impulse confirmation (§ 2.6) is a post-constructive rule. Additional:

- **Rule of Reverse Logic:** When multiple wave counts are plausible, select the count
  closest to the centre of its development — the one that requires the *most* additional
  time to resolve. This reduces the tendency to prematurely conclude patterns.

- **Behaviour-over-structure principle:** "No matter what you think of structure, if
  post-pattern behaviour is inconsistent with your labelling, your wave count is wrong."
  [[neowave.com — structure vs behaviour]](https://www.neowave.com/qow/qow-archive-19.asp)

The engine lacks all post-constructive checks. It validates *within* the proposed count
but does not test whether subsequent price behaviour has confirmed or invalidated it.

---

## 3. Current `wavelib` Audit

### Gap Table

| Concept | Implemented? (file:func) | Fidelity | Gap Note |
|---------|--------------------------|----------|----------|
| Monowave detection | `toolkit.py:zigzag` | heuristic | Percentage-reversal ZigZag approximates monowave boundaries but lacks rollback rules and structure-label assignment (`:5`/`:3`/`:F3` etc). No endpoint correction mechanism |
| Monowave structure labels | — | MISSING | The `:5`/`:3`/`:c3`/`:F3`/`:L5`/`:s5`/`:sL3`/`:L3` system is entirely absent. Without it, polywave grouping is impossible |
| Polywave construction | — | MISSING | Engine begins at hand-picked pivot level (multiwave degree). No grouping of 3 or 5 monowaves into polywaves |
| Multiwave construction | — | MISSING | No hierarchical compaction step. Degree is assumed, never computed |
| Macrowave construction | — | MISSING | Same — entirely top-down, not bottom-up |
| Compaction process | — | MISSING | No Structure Series generation; no multi-level label propagation |
| Rule of Similarity & Balance | `rules.py:similarity_and_balance`, `toolkit.py:similarity_and_balance` | heuristic | Correct 1/3–3× band for price AND time. Applied only to wave2 vs wave4 in `validate_impulse`; should be applied to ALL adjacent corrective pairs |
| S&B degree-assignment logic | — | MISSING | S&B is used as a plausibility check, not as the primary mechanism for confirming same-degree status |
| Rule of Proportion | `rules.py:rule_of_proportion` | stub | Checks child ≤ parent (WARN if child > parent), but does not enforce the hard 161.8 % extension rule |
| Rule of Extension (≥ 161.8 %) | `rules.py:elliott_guidelines` as WARN | heuristic | Treated as guideline; in NeoWave it is a hard rule that, if violated, means there is no extension (different structural implication) |
| Retracement logic (full 7 rules) | `rules.py:retracement_logic`, `toolkit.py:retracement_logic` | partial | Implements the correct three core bands (< 38.2 %, 38.2–61.8 %, 61.8–100 %, > 100 %) but omits Rules 5–7 (161.8 %, 261.8 % breakpoints) and all conditions a–d that depend on m0/m1 ratio. Status is REF, which is honest |
| Rollback rules | — | MISSING | The ZigZag percentage-reversal does not implement Neely's rollback corrections to monowave endpoints |
| Channeling: 0-2 trendline | — | MISSING | No 0-2 line construction or enforcement; no wave-2 endpoint correction via 0-2 break |
| Channeling: 2-4 trendline | `rules.py:two_four_test` | partial | Computes line value and detects break. Lacks the critical two-stage timing rule: break must occur in less time than wave 5 took to form |
| Channeling: 1-3 upper line | `rules.py:throwover_test` | heuristic | Correctly identifies throw-over vs fell-short. Status is REF (correct — genuinely requires visual confirmation). Volume context (heavy volume → throw-over) not checked |
| Channeling-first order | enforced in demo (`_demo`) | partial | The demo correctly runs channeling before trusting the count. But `validate_impulse` does not enforce or require channeling to run first; it can be called without it |
| Terminal impulsion detection | `rules.py:is_terminal`, `toolkit.py:is_terminal` | partial | Correctly checks wave4/wave1 overlap and contracting shape. Misses: (1) 3-3-3-3-3 sub-structure requirement (only overlap is checked); (2) wave-2 retrace ≤ 61.8 % of wave-1 limit; (3) expanding terminal shape detection is noted but not validated separately |
| Terminal retrace timing window | `rules.py:terminal_retrace_window`, `toolkit.py:terminal_retrace_projection` | partial | Computes correct 1/4–1/2 build-time windows. Does NOT frame them correctly as bias windows — the functions imply a price target that over-projects on AVGO. Should explicitly label this as a directional bias, not a price forecast. Timing rule that retrace should occur faster than build time is present but framing is misleading |
| Terminal wave-2 retrace limit | — | MISSING | No check that each corrective sub-wave of a terminal is ≤ 61.8 % of the prior motive sub-wave |
| Complex correction: triangle | `rules.py:_classify_triangle` | heuristic | Detects contracting/expanding/barrier by leg-length progression. Does not check 3-3-3-3-3 sub-structure or post-triangle thrust timing rules. No neutral triangle detection (wave-C longest; A≈E) |
| Neutral triangle | — | MISSING | No detection of wave-C as longest leg, no A≈E equality check, no 161.8 % C limit check |
| Complex correction: diametric | `rules.py:classify_complex_correction` (7-leg branch) | heuristic | 7-leg symmetry ratio test and expand-then-contract check approximate the bowtie/diamond distinction, but do not apply Neely's actual construction rules (time similarity across all 7 legs; discovery date: 1992, post-MEW). No minimum time-similarity threshold enforced |
| Complex correction: symmetrical | — | MISSING | 9-leg symmetrical pattern entirely absent. The code's `classify_complex_correction` returns PASS for 7 legs, REF for 8+ — a 9-leg symmetrical would return REF without identification |
| x-wave check | `rules.py:x_wave_check` | stub (REF) | Unconditional REF; no computation. The 61.8 % retrace rule for small x-waves is checkable and should be implemented |
| Post-constructive rules of logic | — | MISSING | No post-pattern behaviour checks. No Rule of Reverse Logic. No two-stage impulse confirmation sequence |
| Degree assignment | — | MISSING | Degree is assumed. No monowave-count-based complexity comparison; no automatic S&B-based degree computation |

---

## 4. Build Roadmap

Tasks are ordered by dependency. The monowave constructor is the keystone that unlocks
auto-labeling (CLAUDE.md TODO #1 and #4). Each task is marked **CAUSAL-ONLY** where
applicable — all indicators and rules must use only data at or before bar `t`.

---

### Task 1 — Monowave Constructor with Structure Labels (KEYSTONE)

**Dependency:** none (foundational)  
**Function signature:**
```python
def label_monowaves(pivots: list[Pivot]) -> list[tuple[Wave, str]]:
    """
    Given a list of Pivot objects (already extracted by zigzag), assign each
    Wave a structure label from the set {':5', ':3', ':F3', ':c3', ':L5',
    ':s5', ':sL3', ':L3'} by applying Neely's seven retracement rules.

    Returns a list of (Wave, structure_label) pairs.
    CAUSAL-ONLY: each label depends only on m(-2)..m3 — all observable.
    No future data is required; the label for m1 uses m2 which has already
    formed by the time labelling occurs.
    """
```

**Implementation notes:**
- Apply rollback rules to pivot endpoints before labelling.
- Implement all seven retracement rules with exact Fibonacci breakpoints:
  38.2 %, 61.8 %, 100 %, 161.8 %, 261.8 %.
- Conditions a–d for Rules 5–7 depend on the m0/m1 ratio — include a lookup table.
- Initial implementation may return a set of candidate labels rather than a single label
  (ambiguity is real and Neely acknowledges it) — flag ambiguity with `|` notation, e.g.
  `":5|:F3"`.
- **CAUSAL-ONLY:** the label for wave m1 requires m2 to have *completed* — this is a
  one-bar lookahead on the most recent incomplete wave. In live use, the last pivot's label
  is provisional until m2 confirms. Mark last label as `Status.WARN` ("provisional").

**Tests:**
- Known AVGO weekly pivots: verify wave (I) gets `:5`, wave (II) gets `:3` or `:F3`.
- Verify that the 38.2 % and 61.8 % breakpoints trigger the correct rule branch.
- Test rollback rule: a pivot that overshoots by one bar should be corrected.

---

### Task 2 — Polywave Grouper

**Dependency:** Task 1 (needs structure labels)  
**Function signature:**
```python
def group_polywaves(
    labelled_monowaves: list[tuple[Wave, str]]
) -> list[list[tuple[Wave, str]]]:
    """
    Scan the labelled monowave list and identify groups of 3 or 5 consecutive
    monowaves that satisfy both:
      (a) internal retracement rules for the group (standard impulse or correction)
      (b) Rule of Similarity & Balance for the group's corrective pairs

    Returns a list of candidate polywave groups. Each group is a slice of the
    input list. Groups may overlap (multiple candidates at a given start pivot).
    """
```

**Implementation notes:**
- Use a sliding window of sizes 3 and 5.
- For a 3-wave group: apply `classify_correction` to assess if A-B-C rules are met.
- For a 5-wave group: apply `elliott_hard_rules` to assess if 1-2-3-4-5 rules are met.
- Apply S&B to all corrective pairs within the group.
- Groups that pass become "polywave candidates" and are carried forward.

**Tests:**
- Verify AVGO (I)-(II)-(III) internal 5-wave group passes as a polywave candidate.
- Verify that inserting a wave that violates S&B causes the group to be rejected.

---

### Task 3 — S&B Upgrade (All Adjacent Corrective Pairs)

**Dependency:** none (improves existing)  
**Change to `validate_impulse`:**
```python
# Current: applies S&B only to wave2 vs wave4
res.append(similarity_and_balance(w[1], w[3]))

# Required: apply to all corrective pairs and all adjacent waves within corrections
for i in range(len(w) - 1):
    res.append(similarity_and_balance(w[i], w[i+1], context=f"w{i+1}_vs_w{i+2}"))
```

**Also add** to `validate_correction`: S&B check between legs A and C (zigzag/flat) and
between all five triangle legs.

---

### Task 4 — Two-Stage Impulse Confirmation (Timing Rules)

**Dependency:** none (improves existing `two_four_test`)  
**New function signature:**
```python
def two_four_confirmation(
    w5: Wave,
    w2: Pivot,
    w4: Pivot,
    current_t: float,
    current_price: float,
    uptrend: bool = True,
) -> list[RuleResult]:
    """
    Stage 1: Is price at or beyond the 2-4 line? If yes, did the break
             occur in less time than w5.days?
    Stage 2: Has the entire w5 price range been retraced? If yes, did that
             happen in ≤ w5.days?
    Returns two RuleResult objects, one per stage.
    CAUSAL-ONLY: uses only data already observed (current_t, current_price).
    """
```

**Tests:**
- AVGO: 2-4 line ~$301, current price $385.74 — Stage 1 should FAIL (line not broken).
- Construct a synthetic completed impulse and verify both stages PASS.

---

### Task 5 — Terminal Sub-Structure and Wave-2 Retrace Limit

**Dependency:** none (improves `is_terminal`)  
**Additions to `is_terminal`:**
1. Check wave-2 retracement of wave-1 ≤ 61.8 % (hard rule unique to terminals).
2. Report contracting vs expanding shape separately.
3. Add note that sub-waves should each be corrective (`:3`-type) — reference check
   until Task 1 provides structure labels.

---

### Task 6 — Neutral Triangle Detection

**Dependency:** none (new pattern in `classify_correction`)  
**Signature:**
```python
def is_neutral_triangle(legs: Sequence[Wave]) -> RuleResult:
    """
    NeoWave neutral triangle: 5 legs where leg C is the longest;
    legs A and E tend toward equality (each ≥ 38.2 % of C, typically 61.8–72 % of C);
    C ≤ 161.8 % of A (up to 261.8 % in volatile conditions).
    Channeling: parallel lines through ends of b & d, with parallel through end of a.
    """
```

---

### Task 7 — Diametric Pattern: Time-Similarity Enforcement

**Dependency:** none (improves `classify_complex_correction`)  
**Change:** Replace the current symmetry-ratio and expand-then-contract heuristic with a
proper time-similarity check across all seven legs. Each pair of adjacent legs should
pass an S&B time check (≤ 3× ratio). Add bowtie vs diamond classification by testing
whether leg d is the local maximum or minimum of leg lengths.

---

### Task 8 — Symmetrical Formation (9 legs)

**Dependency:** none (new case in `classify_complex_correction`)  
**Add a 9-leg branch** that checks: advancing legs are time/price/complexity similar to
each other; declining legs are similar to each other; the two groups are NOT similar
to each other. Return specific `Status.PASS` with "SYMMETRICAL (9 legs)" label rather
than the current REF fallback for n ≥ 8.

---

### Task 9 — x-Wave Check Computation

**Dependency:** none (improves `x_wave_check`)  
**Change:** Implement the 61.8 % retrace rule as a computable check. Return PASS if the
x-wave retraces < 61.8 % of the prior correction (small x-wave), WARN if 61.8–100 %
(large x-wave — note in detail), FAIL if > 100 % (not an x-wave; structural error).

---

### Task 10 — `label_and_validate(bars)` Auto-Labeling Entry Point

**Dependency:** Tasks 1 and 2  
**Signature:**
```python
def label_and_validate(
    bars: list[tuple],
    pct: float = 0.05,
    max_degree: int = 3,
) -> list[dict]:
    """
    Full bottom-up pipeline:
    1. zigzag(bars, pct) → pivots
    2. label_monowaves(pivots) → labelled monowaves
    3. group_polywaves(labelled) → polywave candidates
    4. For each polywave candidate, run validate_impulse / validate_correction
    5. Return scored candidates sorted by fidelity (fewest FAILs/WARNs)

    CAUSAL-ONLY: all computations use data ≤ bar t. The provisional label
    on the last incomplete wave is flagged WARN.
    """
```

This is the keystone deliverable that removes the manual pivot-picking step and enables
the backtest harness (CLAUDE.md TODO #5).

---

## 5. Open Questions / Subjectivity Caveats

1. **Degree is the hardest problem.** Even with the full monowave construction pipeline,
   the assignment of the first "anchor" degree is a human choice. Neely's S&B provides
   a *consistency* test (once anchored, everything cascades) but does not eliminate the
   initial anchor subjectivity. Automated systems can test multiple anchors and score
   them, but cannot collapse the space to one answer without additional priors.

2. **Rollback rule micro-thresholds.** The rollback rules require detecting whether a
   monowave's endpoint "overshoots by one time unit" — the definition of a time unit
   is chart-scale-dependent. On weekly data, one time unit = one week. On 4h data, four
   hours. This means the rollback logic must be parameterised by timeframe, complicating
   the implementation.

3. **Irregular terminals are underspecified.** Neely discusses expanding/irregular
   terminals but provides fewer examples than for contracting terminals. The exact rules
   for when an expanding terminal is valid vs when it is simply an error in labelling are
   not as clean. The engine's `is_terminal` should flag expanding terminals as
   `Status.WARN` rather than `Status.PASS` until sub-structure is confirmed.

4. **Diametric time-similarity threshold.** Neely says "similar" but does not give an
   exact maximum deviation between adjacent diametric legs for the time similarity test.
   The 1/3–3× S&B band is the implied default, but neowave.com Q&A #875 confirms that
   deviations are allowed without specifying a hard ceiling. Implementation should use
   the S&B band as a soft constraint (WARN not FAIL for a diametric).
   [[neowave.com — diametric time deviation]](https://www.neowave.com/qow/qow-archive-875.asp)

5. **Conditions a–d ambiguity.** For a given monowave, Rules 5–7 with their conditions
   a–d may yield *multiple* plausible structure labels. Neely's book uses a decision-tree
   that narrows to one label, but many practitioners find the tree branches depend on
   whether subsequent waves have formed. In an automated context, carrying a set of
   candidate labels forward (rather than forcing a single one) and resolving ambiguity
   when more data arrives is the honest approach.

6. **Post-constructive rules require historical data.** The two-stage impulse
   confirmation requires watching price *after* the proposed wave 5 — the timing rules
   are retrospective confirmations, not forward projections. In a real-time engine, the
   confirmation status of any completed count changes each new bar. This argues for a
   `confirm_status: Status` field on `Wave` objects that can be updated.

7. **Symmetrical patterns are extremely rare.** Neely found his first one around 2001.
   The code should treat a 9-leg detection as a `Status.WARN` ("possible symmetrical —
   manual confirmation required") rather than a `Status.PASS`, given the limited
   precedent for automated detection.

---

## Sources

- [Neo Wave Theory: How to Trade Using It — LiteFinance](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- [LiteFinance — Part 18: Complexity, Balance, Compaction](https://www.litefinance.org/blog/for-professionals/neowave-part-18-rules-of-complexity-and-balance-compaction-procedures-power-ratings/)
- [LiteFinance — Part 20: Terminal Impulse Progress Labels](https://www.litefinance.org/blog/for-professionals/neowave-part-20-application-of-progress-labels-to-terminal-impulses/)
- [LiteFinance — Part 21: Channeling in Impulses and Fibonacci Relationships](https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships/)
- [LiteFinance — Part 27: Trading Strategy Based on NeoWave](https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/)
- [Glenn Neely — Mastering Elliott Wave (Chapter 1, neowave.com)](https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp)
- [neowave.com — What is NeoWave?](https://www.neowave.com/what-is-neowave.asp)
- [neowave.com — What is NEoWave Analysis?](https://www.neowave.com/what-is-neo-wave-analysis.asp)
- [neowave.com Q&A #3 — What is a NEoWave Diametric Formation?](https://www.neowave.com/qow/qow-archive-3.asp)
- [neowave.com Q&A #5 — What is a NEoWave Symmetrical Formation?](https://www.neowave.com/qow/qow-archive-5.asp)
- [neowave.com Q&A #7 — X-wave application rules](https://www.neowave.com/qow/qow-archive-7.asp)
- [neowave.com Q&A #8 — What is a NEoWave Neutral Triangle?](https://www.neowave.com/qow/qow-archive-8.asp)
- [neowave.com Q&A #13 — Identifying degrees in wave formations](https://www.neowave.com/qow/qow-archive-13.asp)
- [neowave.com Q&A #19 — Structure vs behaviour in NeoWave](https://www.neowave.com/qow/qow-archive-19.asp)
- [neowave.com Q&A #22 — Confirming the end of wave 5](https://www.neowave.com/qow/qow-archive-22.asp)
- [neowave.com Q&A #24 — Classifying triangle types](https://www.neowave.com/qow/qow-archive-24.asp)
- [neowave.com Q&A #25 — Differentiating :F3 from :5](https://www.neowave.com/qow/qow-archive-25.asp)
- [neowave.com Q&A #32 — Does MEW cover all S&B applications?](https://www.neowave.com/qow/qow-archive-32.asp)
- [neowave.com Q&A #78 — S&B: both price and time required?](https://www.neowave.com/qow/qow-archive-78.asp)
- [neowave.com Q&A #94 — X-wave and pattern complexity](https://www.neowave.com/qow/qow-archive-94.asp)
- [neowave.com Q&A #108 — Pre-break terminal confirmation](https://www.neowave.com/qow/qow-archive-108.asp)
- [neowave.com Q&A #273 — Importance of channeling](https://www.neowave.com/qow/qow-archive-273.asp)
- [neowave.com Q&A #303 — 2-4 trendline placement](https://www.neowave.com/qow/qow-archive-303.asp)
- [neowave.com Q&A #474 — Post-diametric behaviour](https://www.neowave.com/qow/qow-archive-474.asp)
- [neowave.com Q&A #509 — Early triangle identification clues](https://www.neowave.com/qow/qow-archive-509.asp)
- [neowave.com Q&A #875 — Diametric time deviation](https://www.neowave.com/qow/qow-archive-875.asp)
- [neowave.com Q&A #923 — Extracting triangle retired](https://www.neowave.com/qow/qow-archive-923.asp)
- [neowave.com Q&A #1006 — Extension rule: 161.8 % requirement](https://www.neowave.com/qow/qow-archive-1006.asp)
- [neowave.com Q&A #1079 — Wave-2 retrace limit in NeoWave](https://www.neowave.com/qow/qow-archive-1079.asp)
- [neowave.com Q&A #2346 — Where to find diametric and symmetrical info](https://www.neowave.com/qow/qow-archive-2346.asp)
- [neowave.com Q&A #3782 — Terminal: wave-2 and wave-4 timing](https://www.neowave.com/qow/qow-archive-3782.asp)
- [neowave.com Q&A #3849 — Neutral triangle wave-C limit](https://www.neowave.com/qow/qow-archive-3849.asp)
- [neowave.com Q&A #3976 — Rule of Reverse Logic](https://www.neowave.com/qow/qow-archive-3976.asp)
- [neowave.com Q&A #5161 — Post-triangle thrust time limit](https://www.neowave.com/qow/qow-archive-5161.asp)
- [neowave.com — Rule of Reverse Logic explained](https://www.neowave.com/neowave-rules-of-reverse-logic.asp)
- [ForexTalker — Basic NeoWave concepts and principles](https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/)
- [ForexTalker — Rollback rules and first wavelength rule](https://forextalker.com/neowave-wave-theory-by-glenn-neely-rollback-rules-and-the-first-rule-of-wavelength-relationships/)
- [ForexTalker — Rule 2: conditions for its implementation](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-the-second-rule-for-the-ratio-of-wavelengths-and-conditions-for-its-implementation/)
- [ForexTalker — Conditions a, b, c, d for Rule 7](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-a-b-c-and-d-for-the-seventh-rule/)
- [Scribd — NeoWave Retracement Rule 3](https://www.scribd.com/document/502299837/5-The-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Retracement Rule 4](https://www.scribd.com/document/502300644/7-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Retracement Rules 5 & 6](https://www.scribd.com/document/502311042/9-NeoWave-theory-by-Glenn-Neely)
- [Scribd — Part 13: Corrections and identification rules](https://www.scribd.com/document/839672297/Part-13-Corrections-Rules-to-identify-a-correction-NeoWave-theory-by-Glenn-Neely)
- [Scribd — Part 20: Terminal Impulse progress labels](https://www.scribd.com/document/839672300/Part-20-Application-of-Progress-Labels-to-Terminal-Impulses-Progress-Labels-in-Terminal-Impulses)
- [ebrary.net — Triangle and Diametric pattern chapter](https://ebrary.net/299888/education/triangle)
- [tradingfinder.com — Terminal vs Trending Impulse](https://tradingfinder.com/education/forex/impulse-waves/)
- [wavesstrategy.com — What is NeoWave, difference from Elliott Wave](https://www.wavesstrategy.com/what-is-neo-wave-difference-between-elliott-wave-neo-wave-2)
- [Studocu — NW2 NeoWave Theory: Polywaves & Structures](https://www.studocu.com/row/document/sri-lanka-institute-of-marketing/digital-marketing/nw2-neo-wave/98941243)
- [niftywaveindia.blogspot.com — 7-legged Diametric patterns](http://niftywaveindia.blogspot.com/2018/12/technical-learnings-7-legged-diametric.html)
