# 06 — Full Elliott/NeoWave Pattern Catalog: Construction Rules, Diagonals, Fibonacci, and Disambiguation

**Scope:** Deep implementable reference for the full Elliott Wave + NeoWave pattern catalog.
Written from scratch with inline citations. Precise enough to code from. Not investment advice.

**Date:** 2026-06-06  
**Intended audience:** The recursive wave-tree engine in `wavelib/rules.py` and `wavelib/automation.py`.

---

## 1. Scope and Sources

This document covers every major Elliott Wave and NeoWave pattern in machine-checkable
detail. Each pattern entry provides:

1. **Hard rules** — violations invalidate the label (FAIL in `RuleResult`).
2. **Guidelines** — probabilistic; violations are WARN, not FAIL.
3. **Sub-wave structure** — the exact internal count.
4. **Fibonacci relationships** — primary and secondary ratio targets.
5. **Disambiguation criteria** — how to distinguish this pattern from look-alikes.
6. **Pseudo-code** — implementable logic for a recursive validator.
7. **Post-pattern implication** — what each pattern forecasts for the next move.

Patterns covered, in order:
- §2: Impulse (5-wave motive)
- §3: Leading Diagonal (wave 1 / wave A)
- §4: Ending Diagonal (wave 5 / wave C) — *primary new addition*
- §5: Expanding Diagonal (contracting vs expanding variants)
- §6: Disambiguation decision tree (Impulse vs Diagonal vs Triangle)
- §7: Zigzag (5-3-5) and Double/Triple Zigzag
- §8: Flat (3-3-5) — Regular / Expanded / Running
- §9: Triangle (3-3-3-3-3) — Contracting / Barrier / Expanding / Running
- §10: Combinations — Double Three (W-X-Y) and Triple Three (W-X-Y-X-Z)
- §11: NeoWave Extensions — Terminal, Diametric (7-leg), Symmetrical (9-leg)
- §12: Fibonacci Relationship Table (complete reference)
- §13: Implementation Priority List
- §14: Caveats and honesty flags

---

## 2. Impulse (Five-Wave Motive)

### 2.1 Definition and Position

An impulse is a five-wave motive structure labeled 1-2-3-4-5 that progresses in the
direction of the trend at one-larger degree. Waves 1, 3, and 5 are themselves motive
(impulse or diagonal); waves 2 and 4 are corrective.

Impulses appear: as the complete numbered sequence of any motive trend; as waves 1, 3,
and 5 within a larger impulse; as waves A and C of a zigzag.

Source: Frost & Prechter, *Elliott Wave Principle*, 10th ed., Ch. 1;
archive.org: https://archive.org/details/elliottwaveprinc0000fros

### 2.2 The Three Inviolable Hard Rules

These are absolute. A single violation invalidates the impulse label and forces
recount. (Wikipedia: https://en.wikipedia.org/wiki/Elliott_wave_principle)

#### Rule 1 — Wave 2 never retraces 100% or more of Wave 1

```
# Upward impulse
assert w2.end.price > w1.start.price  # w2 end strictly above w1 origin
# Downward impulse
assert w2.end.price < w1.start.price
```

Rationale: If wave 2 erases all of wave 1, no net progress occurred; the impulse
count collapses and must be reclassified.

Invalidation level: the exact origin price of wave 1.

#### Rule 2 — Wave 3 is never the shortest of waves 1, 3, and 5

```
len1 = abs(w1.end.price - w1.start.price)
len3 = abs(w3.end.price - w3.start.price)
len5 = abs(w5.end.price - w5.start.price)

# FAIL if wave 3 is shorter than BOTH wave 1 AND wave 5
assert not (len3 < len1 and len3 < len5)
```

Note: wave 3 may be shorter than wave 1 but must not be shorter than wave 5 (and
vice versa). Only if it is the absolute minimum of all three is the count invalid.
Source: EW Forecast: https://elliottwave-forecast.com/elliott-wave-theory/

#### Rule 3 — Wave 4 does not enter Wave 1 price territory

```
# Upward impulse: wave 4 low must stay above wave 1 high
assert w4.end.price > w1.end.price
# Downward impulse: wave 4 high must stay below wave 1 low
assert w4.end.price < w1.end.price
```

The sole exception is a diagonal formation (see §3 and §4), where wave 4 overlap
with wave 1 is expected and not a violation.

Invalidation level: the extreme endpoint of wave 1 (not the origin — the end of
wave 1).

### 2.3 Extension Rules

Only one of waves 1, 3, or 5 extends (becomes markedly longer than the other two).
In practice: ~90% of extensions occur in wave 3; wave 5 extensions are the next
most common; wave 1 extensions are the rarest.
Source: EW Forecast extensions: https://elliottwave-forecast.com/elliottwave/elliott-wave-extensions/

**Wave 3 extended (most common):**
- Wave 3 ≥ 1.618 × wave 1 (often 1.618–2.618, sometimes larger).
- When wave 3 extends, waves 1 and 5 tend toward equality (the Guideline of Equality).
- If equality fails, the 0.618 relationship is the next most probable (wave 5 = 0.618 × wave 1).

**Wave 5 extended:**
- Wave 3 must be longer than wave 1 (otherwise Rule 2 fails).
- Wave 5 commonly extends to 1.618 × the net distance of wave 1 through wave 3
  (measured from wave 4's endpoint).
- Wave 5 extension often accompanies strong momentum and a final throw-over of the
  channel.

**Wave 1 extended (rare):**
- Waves 3 and 5 tend to be relatively equal in price and time.
- The net distance from the end of wave 3 to the end of wave 5 often equals 0.618 of wave 1.

```python
def check_extension(len1, len3, len5):
    """Returns which wave is extended, or None."""
    ratios = {1: len1, 3: len3, 5: len5}
    longest = max(ratios, key=ratios.get)
    second = sorted(ratios.values())[-2]
    if second == 0:
        return None
    ratio = ratios[longest] / second
    if ratio >= 1.618:
        return longest  # extended wave
    return None  # no clear extension (guideline warn, not fail)
```

### 2.4 Alternation Guideline

If wave 2 is a sharp correction (zigzag or double zigzag), wave 4 will usually be
a sideways correction (flat, triangle, double three). And vice versa.

**Sharp corrections** (wave 2 typical): zigzag, double/triple zigzag. Steep angle,
B-wave retracement < 61.8% of A.

**Sideways corrections** (wave 4 typical): flat, triangle, double/triple three.
Roughly horizontal, often include a new price extreme beyond the orthodox end of the
prior motive wave.

```python
def check_alternation(w2_pattern: str, w4_pattern: str) -> bool:
    SHARP = {"zigzag", "double_zigzag", "triple_zigzag"}
    SIDEWAYS = {"flat", "expanded_flat", "running_flat",
                "contracting_triangle", "barrier_triangle",
                "expanding_triangle", "double_three", "triple_three"}
    w2_sharp = w2_pattern in SHARP
    w4_sharp = w4_pattern in SHARP
    return w2_sharp != w4_sharp  # True = alternation present
```

Note: In a diagonal, waves 2 and 4 are both typically zigzags — no alternation expected.

### 2.5 Depth Guidelines

| Wave | Typical retracement | Common Fibonacci levels |
|------|---------------------|------------------------|
| Wave 2 of prior Wave 1 | 50–78.6% | 0.500, 0.618, 0.786 |
| Wave 4 of prior Wave 3 | 23.6–50% | 0.236, 0.382, 0.500 |

Wave 2 is typically deeper than wave 4. A wave 2 retracement > 78.6% that has not
yet crossed the wave 1 origin is still valid but raises concern about degree.

### 2.6 Wave Equality Guideline

When wave 3 is extended, the Guideline of Equality states:
- Wave 5 price length ≈ wave 1 price length (primary target), OR
- Wave 5 = 0.618 × wave 1 (secondary target).

```python
def wave5_equality_targets(w4_end, w1_len, w3_len):
    primary   = w4_end + w1_len          # wave 5 = wave 1
    secondary = w4_end + 0.618 * w1_len  # wave 5 = 0.618 × wave 1
    extended  = w4_end + 1.618 * w1_len  # extended fifth
    return {"equality": primary, "0.618_of_w1": secondary, "extended": extended}
```

### 2.7 Channeling Technique

Three successive channel constructions (applied as each wave completes):

**Base channel** (after wave 2 completes):
- Lower line: through wave 0 origin and wave 2 end.
- Upper parallel: through wave 1 top.
- Price holding above lower line during wave 3 confirms motive count.

**Acceleration channel** (after wave 4 completes):
- Lower line: through wave 2 end and wave 4 end.
- Upper parallel: through wave 3 top.
- Wave 5 target = upper parallel at the time of wave 4's end projected forward.

**Final channel** (after wave 5 completes):
- Lines through wave 1 top and wave 3 top; parallel through wave 2 bottom.
- Wave 5 ending: ideally meets or slightly breaches upper line (throw-over), or falls
  short (weak/truncated fifth).

Source: EWI Channeling: https://www.elliottwave.com/waveopedia/channeling/
EW Forecast channeling: https://elliottwave-forecast.com/trading/elliott-wave-channeling-trendlines-guide/

### 2.8 Impulse Pseudo-Code Summary

```python
def validate_impulse(w1, w2, w3, w4, w5) -> list[RuleResult]:
    results = []
    up = w1.end.price > w1.start.price

    # HARD RULES (any FAIL => invalid)
    # R1: wave 2 doesn't retrace past wave 1 start
    r1 = (w2.end.price > w1.start.price) if up else (w2.end.price < w1.start.price)
    results.append(RuleResult("R1 w2<100%w1", FAIL if not r1 else PASS, ...))

    # R2: wave 3 not shortest of 1, 3, 5
    l1, l3, l5 = abs_len(w1), abs_len(w3), abs_len(w5)
    r2 = not (l3 < l1 and l3 < l5)
    results.append(RuleResult("R2 w3 not shortest", FAIL if not r2 else PASS, ...))

    # R3: wave 4 doesn't overlap wave 1 territory
    r3 = (w4.end.price > w1.end.price) if up else (w4.end.price < w1.end.price)
    results.append(RuleResult("R3 w4/w1 no overlap", FAIL if not r3 else PASS, ...))

    # GUIDELINES (violations => WARN)
    results += check_extension_guideline(l1, l3, l5)
    results += check_alternation_guideline(w2_pattern, w4_pattern)
    results += check_depth_guideline(w2, w1, w3, w4)
    results += check_equality_guideline(l1, l3, l5, extended_wave)
    return results
```

---

## 3. Leading Diagonal (Wave 1 or Wave A)

### 3.1 Definition and Position

A leading diagonal appears **only** at the start of a trend:
- As wave 1 of an impulse (the sub-waves then unfold as 2-3-4-5 above it).
- As wave A of a zigzag correction.

It is the rarest of all motive patterns and signals a less-vigorous new trend.

### 3.2 Sub-Wave Structure: 5-3-5-3-5

The internal structure of a leading diagonal is **5-3-5-3-5**:
- Waves 1, 3, and 5 of the diagonal are themselves impulses (or occasionally
  smaller leading diagonals) — they subdivide into five waves.
- Waves 2 and 4 are zigzags (3-wave structures).

This distinguishes the leading diagonal from the ending diagonal (see §4), whose
internal structure is 3-3-3-3-3.

Sources:
- EW International Diagonals: https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/
- EW Monitor diagonal guide: https://elliottwavemonitor.com/leading-and-ending-diagonal/
- EW Forecast intro to diagonals: https://elliottwave-forecast.com/elliottwave/introduction-diagonals/

### 3.3 Hard Rules for Leading Diagonal (Contracting)

```
HARD RULES (any violation => label invalid):

1. wave 2 endpoint does NOT exceed wave 1 start.
   (same as impulse Rule 1 — wave 2 cannot retrace 100%+ of wave 1)

2. wave 3 endpoint MUST exceed wave 1 endpoint.
   (price advances beyond wave 1's extreme)

3. wave 4 endpoint MUST NOT exceed wave 2 endpoint.
   (wave 4 does not cross the start of wave 3)

4. wave 5 endpoint MUST exceed wave 3 endpoint.
   (price advances beyond wave 3's extreme — diagonal makes net progress)

5. wave 3 is never the shortest among waves 1, 3, 5.
   (same Rule 2 logic as impulse)

6. CONTRACTING: wave 3 < wave 1; wave 4 > wave 2; wave 5 < wave 3.
   (wedge tightens toward apex)
   For the contracting variant only — expanding variant has opposite size ordering.
```

### 3.4 Overlap of Wave 4 and Wave 1

In a leading diagonal, **wave 4 almost always overlaps with the price territory of
wave 1**. This is the canonical diagnostic signal: if wave 4's endpoint penetrates
into the price range covered by wave 1, it is NOT an impulse; it is a diagonal.

However: wave 4 must not go below (in an upward diagonal) the END of wave 2. If
price crosses the end of wave 2, the diagonal label is invalid.

```python
# Upward leading diagonal overlap test
def w4_overlap_w1(w1, w2, w4, up=True):
    # overlap: w4 end enters w1's price range
    overlap_present = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    # invalidation: w4 end crosses w2 end
    beyond_w2 = (w4.end.price < w2.end.price) if up else (w4.end.price > w2.end.price)
    return overlap_present, beyond_w2
```

### 3.5 Trendline Convergence Test

In a contracting leading diagonal:
- Draw line L1 through wave 1 end and wave 3 end.
- Draw line L2 through wave 2 end and wave 4 end.
- L1 and L2 must CONVERGE (slope toward each other going forward in time).
- Wave 5 ends near, at, or slightly beyond L1.

```python
def trendlines_converge(p1_end, p3_end, p2_end, p4_end):
    """Returns True if the 1-3 and 2-4 trendlines converge (contracting diagonal)."""
    # slope of L1 (in price/bar)
    slope_13 = (p3_end.price - p1_end.price) / (p3_end.t - p1_end.t)
    # slope of L2
    slope_24 = (p4_end.price - p2_end.price) / (p4_end.t - p2_end.t)
    # For upward diagonal: L1 has positive slope; L2 has positive but smaller slope
    # Convergence means L1 slope > L2 slope (lines closing gap)
    return slope_13 > slope_24  # upward case; invert for downward
```

### 3.6 Fibonacci Relationships (Leading Diagonal)

| Relationship | Primary ratio | Secondary ratio |
|---|---|---|
| Wave 2 retraces Wave 1 | 0.618 (deep) | 0.786 |
| Wave 4 retraces Wave 3 | 0.618 | 0.786 |
| Wave 3 vs Wave 1 (size) | 0.618 (shorter) | 0.786 |
| Wave 5 vs Wave 3 (size) | 0.618 (shorter) | 0.786 |
| Wave 5 projections | 0.618 × wave 3 from wave 4 end | = wave 1 |

Both corrective waves (2 and 4) in a leading diagonal typically retrace **0.66 to 0.81**
of their preceding motive wave — deeper than typical impulse corrections.

### 3.7 Post-Pattern Implication

The wave AFTER a leading diagonal is almost always a deep retracement:
- When in wave 1 position: wave 2 typically retraces 61.8–78.6% of the entire diagonal.
- The deep wave 2 pullback is followed by a powerful wave 3 — the leading diagonal
  signals initial accumulation before the main trend.

```python
# After confirming a leading diagonal at wave 1 position:
w2_target_61 = diag_end - 0.618 * diag_length  # upward case
w2_target_786 = diag_end - 0.786 * diag_length  # deeper target
```

Source: EWM Interactive: https://ewminteractive.com/recognize-leading-diagonal-pattern
EW Forecast: https://elliottwave-forecast.com/elliottwave/introduction-diagonals/

---

## 4. Ending Diagonal (Wave 5 or Wave C)

### 4.1 Definition and Position

An ending diagonal appears **only** at the termination of a larger trend:
- As wave 5 of an impulse (the final push exhausting the trend).
- As wave C of a flat or zigzag correction.

It signals exhaustion, not momentum. The pattern is more common than the leading
diagonal. After an ending diagonal completes, the market almost always reverses
sharply and rapidly retraces the entire diagonal, often returning to its origin.

### 4.2 Sub-Wave Structure: 3-3-3-3-3

The internal structure of an ending diagonal is **3-3-3-3-3**: every sub-wave (1
through 5) subdivides as a three-wave corrective structure (typically zigzags). No
motive sub-wave is an impulse. This is the defining hard rule that separates the
ending diagonal from all other five-wave patterns.

Sources:
- EW International Diagonals: https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/
- EW Forecast ending diagonal: https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/
- Stock Path Shala ending diagonal: https://stockpathshala.com/elliott-wave-ending-diagonal/

### 4.3 Hard Rules for Ending Diagonal (Contracting)

```
HARD RULES:

1. Wave 2 endpoint does NOT exceed wave 1 start.
   (retrace of wave 1 ≤ 100%; same as impulse R1)

2. Wave 3 endpoint MUST exceed wave 1 endpoint.
   (diagonal makes net directional progress on wave 3)

3. Wave 4 endpoint DOES NOT exceed wave 2 endpoint.
   (wave 4 does not cross wave 2's end; unlike impulse, it CAN overlap wave 1)

4. Wave 5 endpoint MUST exceed wave 3 endpoint.
   (final advance, even if marginal)

5. Wave 3 is never the shortest of waves 1, 3, 5.
   (NB: wave 3 is often shorter than wave 1 in an ending diagonal, but must
    be longer than wave 5 in a contracting variant)

6. CONTRACTING (most common):
   wave 1 > wave 3 > wave 5 (each motive wave shorter than previous)
   wave 4 > wave 2          (each corrective wave longer than previous)

7. Sub-wave structure 3-3-3-3-3:
   Every leg subdivides as a three (zigzag, flat, or small triangle).
   A leg that subdivides as a five (impulse) INVALIDATES the ending-diagonal label.
   (Cannot be machine-checked without sub-degree data; flag as REF)
```

### 4.4 Wave 4 / Wave 1 Overlap — Key Diagnostic

In an ending diagonal, **wave 4 almost always overlaps wave 1**. The overlap is the
single most important diagnostic flag separating an ending diagonal from an impulse.

Absence of overlap in a pattern that otherwise looks like a diagonal is unusual and
warrants WARN status (possibly a leading diagonal in wave 5 position, which can occur).

Invalidation of the overlap: wave 4 must NOT cross the end of wave 2. If it does,
the count is invalid (same rule as the leading diagonal).

```python
def ending_diagonal_overlap_check(w1, w2, w4, up=True):
    # Expected: w4 end overlaps w1 territory
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    # Invalidation: w4 end crosses w2 end (too deep)
    beyond_w2 = (w4.end.price < w2.end.price) if up else (w4.end.price > w2.end.price)
    if beyond_w2:
        return FAIL, "wave 4 crossed wave 2 end — ending diagonal invalidated"
    if not overlap:
        return WARN, "no w4/w1 overlap — atypical for ending diagonal"
    return PASS, "w4/w1 overlap confirmed"
```

### 4.5 Trendline Convergence (Contracting Ending Diagonal)

- Draw line L1 through the endpoints of wave 1 and wave 3.
- Draw line L2 through the endpoints of wave 2 and wave 4.
- Both lines converge toward an apex (wedge shape).
- The 1-3 line forms the upper boundary (in an upward diagonal).
- The 2-4 line forms the lower boundary.
- Wave 5 typically ends near the L1 upper boundary; it may slightly exceed it (throw-over).

```python
def check_wedge_convergence(w1e, w3e, w2e, w4e):
    """
    Contracting: slope of 1-3 line > slope of 2-4 line (for upward diagonal).
    Expanding: slope of 1-3 line < slope of 2-4 line.
    """
    slope_13 = (w3e.price - w1e.price) / max(w3e.t - w1e.t, 1)
    slope_24 = (w4e.price - w2e.price) / max(w4e.t - w2e.t, 1)
    contracting = slope_13 > slope_24
    return contracting
```

### 4.6 Throw-Over

A throw-over is a brief breach of the L1 (1-3) trendline by wave 5 before the reversal.
It is common (but not required) in ending diagonals and indicates final exhaustion.

Identification: wave 5 peak briefly exceeds the L1 line value at the same timestamp,
then reverses rapidly.

```python
def detect_throwover(w1e, w3e, w5_peak, w5_peak_t, up=True):
    l1_at_peak = line_value(w1e, w3e, w5_peak_t)
    throwover = (w5_peak > l1_at_peak) if up else (w5_peak < l1_at_peak)
    return throwover, l1_at_peak
```

Post throw-over behavior: reversal expected to carry price back to at minimum the
origin of wave 5, and often back to the origin of the entire ending diagonal.
Source: EWI Throw-Over: https://www.elliottwave.com/waveopedia/throw-over/
EW Forecast: https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/

### 4.7 Fibonacci Relationships (Ending Diagonal)

| Relationship | Primary ratio | Secondary ratio |
|---|---|---|
| Wave 2 retraces Wave 1 | 0.618–0.786 | 0.500 |
| Wave 4 retraces Wave 3 | 0.618–0.786 | 0.500 |
| Wave 3 vs Wave 1 (size) | 0.618 (smaller) | 0.786 |
| Wave 5 vs Wave 3 (size) | 0.618 (smallest) | 0.382 |
| Post-pattern retrace target | back to diagonal origin | wave 5 origin (minimum) |

Each corrective wave (2 and 4) typically retraces **0.66 to 0.81** of the preceding
motive wave (same as leading diagonal, deeper than normal impulse corrections).

Source: EW Forecast intro diagonals:
https://elliottwave-forecast.com/elliottwave/introduction-diagonals/

### 4.8 Post-Pattern Implication

After an ending diagonal completes, the subsequent move:
- Retraces the entire diagonal very rapidly (faster than the diagonal itself took to form).
- Minimum target: origin of wave 5 of the diagonal.
- Common target: origin of the entire diagonal (wave 1 start).
- The retrace is faster than any same-direction sub-wave within the diagonal.

This is the NeoWave **terminal impulse** rule: fast, full retrace expected within
the time frame of the diagonal's construction.

```python
def ending_diagonal_reversal_targets(diag_origin, diag_wave5_start, diag_end, up=True):
    delta = 1 if up else -1
    return {
        "minimum": diag_wave5_start,          # retrace to wave 5 origin
        "primary": diag_origin,               # retrace to diagonal start
        "overshoot": diag_origin - delta * abs(diag_end - diag_origin) * 0.236,
    }
```

### 4.9 Ending Diagonal Full Pseudo-Code

```python
def validate_ending_diagonal(w1, w2, w3, w4, w5) -> list[RuleResult]:
    results = []
    up = w1.end.price > w1.start.price
    l1 = abs_len(w1); l3 = abs_len(w3); l5 = abs_len(w5)
    l2 = abs_len(w2); l4 = abs_len(w4)

    # HARD RULE 1: w2 does not cross w1 start
    r1 = (w2.end.price > w1.start.price) if up else (w2.end.price < w1.start.price)
    results.append(RuleResult("ED-R1 w2<100%w1", FAIL if not r1 else PASS, ...))

    # HARD RULE 2: w3 exceeds w1 end
    r2 = (w3.end.price > w1.end.price) if up else (w3.end.price < w1.end.price)
    results.append(RuleResult("ED-R2 w3 exceeds w1 end", FAIL if not r2 else PASS, ...))

    # HARD RULE 3: w4 does not cross w2 end
    r3_ok = not ((w4.end.price < w2.end.price) if up else (w4.end.price > w2.end.price))
    results.append(RuleResult("ED-R3 w4 not past w2 end", FAIL if not r3_ok else PASS, ...))

    # HARD RULE 4: w5 exceeds w3 end
    r4 = (w5.end.price > w3.end.price) if up else (w5.end.price < w3.end.price)
    results.append(RuleResult("ED-R4 w5 exceeds w3 end", FAIL if not r4 else PASS, ...))

    # HARD RULE 5: w3 not shortest of motive waves
    r5 = not (l3 < l1 and l3 < l5)
    results.append(RuleResult("ED-R5 w3 not shortest", FAIL if not r5 else PASS, ...))

    # HARD RULE 6: Contracting size ordering
    contracting = (l1 > l3 > l5) and (l4 > l2)
    expanding = (l1 < l3 < l5) and (l4 < l2)
    if not (contracting or expanding):
        results.append(RuleResult("ED-R6 wedge sizing", WARN, "neither contracting nor expanding"))
    else:
        kind = "contracting" if contracting else "expanding"
        results.append(RuleResult("ED-R6 wedge sizing", PASS, kind))

    # GUIDELINE: w4/w1 overlap (expected, warn if absent)
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    results.append(RuleResult("ED-G w4/w1 overlap", PASS if overlap else WARN, ...))

    # GUIDELINE: trendline convergence (contracting case)
    if contracting:
        converging = check_wedge_convergence(w1.end, w3.end, w2.end, w4.end)
        results.append(RuleResult("ED-G trendlines converge", PASS if converging else WARN, ...))

    # GUIDELINE: throw-over check
    throwover, l1_at_w5 = detect_throwover(w1.end, w3.end, w5.end.price, w5.end.t, up)
    results.append(RuleResult("ED-G throw-over", PASS if throwover else WARN,
                              f"1-3 line at w5 peak: {l1_at_w5:.2f}"))

    # REF: 3-3-3-3-3 sub-structure (needs sub-degree data)
    results.append(RuleResult("ED-R sub-structure 3-3-3-3-3", REF,
                              "each leg must subdivide as a 3; verify with sub-degree pivots"))

    # FIBONACCI guidelines
    d2 = l2 / l1; d4 = l4 / l3
    results.append(RuleResult("ED-G w2 depth 0.618-0.786", WARN if not 0.60<=d2<=0.81 else PASS,
                              f"w2 retraces {d2:.0%} of w1"))
    results.append(RuleResult("ED-G w4 depth 0.618-0.786", WARN if not 0.60<=d4<=0.81 else PASS,
                              f"w4 retraces {d4:.0%} of w3"))

    return results
```

---

## 5. Expanding Diagonal

### 5.1 Contracting vs Expanding — Key Differences

Both leading and ending diagonals come in contracting and expanding variants. The
contracting variant (wedge that narrows) is far more common.

**Contracting diagonal:**
- Motive waves: 1 > 3 > 5 (each shorter).
- Corrective waves: 2 < 4 (each longer).
- Trendlines converge toward an apex.
- Most common form for both leading and ending diagonals.

**Expanding diagonal:**
- Motive waves: 1 < 3 < 5 (each longer — the reverse).
- Corrective waves: 2 > 4 (each shorter).
- Trendlines diverge away from each other.
- Rarer; typically appears in the leading position (wave 1/A) with 5-3-5-3-5 structure;
  occasionally as an ending diagonal in wave 5.

Source: EW International Diagonals: https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/
WaveTrack: https://www.wavetrack.com/tutorials/elliott-wave-expanding-diagonal-patterns.html

### 5.2 Hard Rules for Expanding Diagonal

```
For EXPANDING LEADING diagonal (upward):

1. wave 3 longer than wave 1:     l3 > l1
2. wave 5 longer than wave 3:     l5 > l3
3. wave 4 shorter than wave 2:    l4 < l2

For EXPANDING ENDING diagonal:
   Same size ordering.
   Wave 4 still must not cross wave 2 endpoint.
   Sub-structure: 3-3-3-3-3 (ending) or 5-3-5-3-5 (leading).
```

### 5.3 Trendline Divergence Test

```python
def trendlines_diverge(w1e, w3e, w2e, w4e):
    slope_13 = (w3e.price - w1e.price) / max(w3e.t - w1e.t, 1)
    slope_24 = (w4e.price - w2e.price) / max(w4e.t - w2e.t, 1)
    # For upward expanding diagonal: slope of 1-3 (upper) > slope of 2-4 (lower)
    # and the gap between them is growing
    diverging = slope_13 < slope_24  # opposite of converging
    return diverging
```

---

## 6. Disambiguation Decision Tree: Impulse vs Diagonal vs Triangle

This is the core algorithm needed in a recursive wave-tree engine. Given a 5-wave
candidate structure, determine what it is.

### 6.1 Decision Tree

```
INPUT: [w1, w2, w3, w4, w5] — 5 consecutive waves in trend direction

STEP 1: Check wave 4 / wave 1 overlap
────────────────────────────────────
  overlap = (w4.end.price < w1.end.price)  # for upward trend

  IF no overlap:
    → Candidate is an IMPULSE (or count is wrong)
    → Apply impulse hard rules (§2.2)
    → If all 3 hard rules pass → IMPULSE (confirmed)
    → If any hard rule fails → invalid count; try other counts

  IF overlap present:
    → Candidate is a DIAGONAL (leading or ending)
    → Proceed to Step 2

STEP 2: Determine Leading vs Ending Diagonal
────────────────────────────────────────────
  Check the POSITION of this 5-wave structure in the higher degree:
  
  IF this structure is in wave 1 or wave A position:
    → Candidate is LEADING DIAGONAL
    → Expect sub-structure 5-3-5-3-5 (REF: verify with sub-degree)
    → Deep wave-2/wave-B retracement follows (0.618–0.786 of diagonal)
  
  IF this structure is in wave 5 or wave C position:
    → Candidate is ENDING DIAGONAL
    → Expect sub-structure 3-3-3-3-3 (REF: verify with sub-degree)
    → Fast, sharp reversal follows (back to diagonal origin)
  
  IF position unknown/ambiguous:
    → Check sub-structure (§6.2) as the distinguishing test

STEP 3: Contracting vs Expanding
──────────────────────────────────
  l1=abs_len(w1), l3=abs_len(w3), l5=abs_len(w5)
  l2=abs_len(w2), l4=abs_len(w4)
  
  contracting = (l1 > l3 > l5) AND (l4 > l2)
  expanding   = (l1 < l3 < l5) AND (l4 < l2)
  
  IF contracting: trendlines converge → CONTRACTING diagonal
  IF expanding:   trendlines diverge  → EXPANDING diagonal
  IF neither:     WARN (irregular; possible but uncommon)
```

### 6.2 Triangle vs Diagonal Disambiguation

Both a triangle and an ending diagonal are 5-wave structures with wave 4 entering
wave 1 territory. The key differences:

| Feature | Triangle (3-3-3-3-3) | Ending Diagonal (3-3-3-3-3) |
|---|---|---|
| **Net price progress** | None — sideways; consolidation | Yes — moves in trend direction |
| **Position** | Wave 4, B, X (corrective position) | Wave 5 or C (motive-terminal position) |
| **Thrust after** | Fast thrust equal to widest leg | Sharp reversal back to origin |
| **Wave labeling** | A-B-C-D-E | 1-2-3-4-5 |
| **Wave B often** | Can exceed wave A start (running) | Cannot — hard rule |
| **Trendlines** | A-C line and B-D line (not 1-3 / 2-4) | 1-3 and 2-4 lines |
| **5th leg (E/5)** | Often falls short of A-C line | Often meets/exceeds 1-3 line |

```python
def diagonal_vs_triangle(candidates: list[Wave], position: str) -> str:
    """
    position: "corrective" (wave 4 / B / X) or "motive_terminal" (wave 5 / C)
    """
    net_progress = abs(candidates[-1].end.price - candidates[0].start.price)
    span = max(w.end.price for w in candidates) - min(w.start.price for w in candidates)
    sideways_ratio = net_progress / span if span else 0

    if position == "corrective":
        # Triangles appear in corrective positions; net sideways movement
        if sideways_ratio < 0.30:
            return "TRIANGLE"          # strongly sideways
        else:
            return "DIAGONAL (unusual corrective position — verify)"
    elif position == "motive_terminal":
        if sideways_ratio > 0.40:
            return "ENDING_DIAGONAL"   # net directional progress
        else:
            return "TRIANGLE (unexpected in wave 5 — recheck position)"
    return "AMBIGUOUS"
```

### 6.3 Impulse vs Leading Diagonal (wave 1 position)

Both appear in wave 1 or wave A. Distinguishing features:

| Feature | Impulse in wave 1 | Leading Diagonal in wave 1 |
|---|---|---|
| **Wave 4 / wave 1 overlap** | None (hard rule) | Almost always present |
| **Wedge shape** | Not required | Yes — trendlines converge |
| **Internal wave 1** | Impulse (5 sub-waves) | Impulse (5 sub-waves) — same |
| **Internal wave 2** | Any correction | Zigzag (3 sub-waves) |
| **Wave 2 retracement** | 50–78.6% | 61.8–78.6% (deeper, typical) |
| **Following wave 2** | Normal depth | Typically very deep (78.6%) |
| **Wave 3** | Often the longest | Often shorter than wave 1 |

```python
def impulse_vs_leading_diagonal(w1, w2, w3, w4, w5, up=True):
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    l1, l3, l5 = abs_len(w1), abs_len(w3), abs_len(w5)
    contracting = (l1 > l3 > l5)

    if not overlap:
        return "IMPULSE_CANDIDATE"   # no overlap → must be impulse
    if overlap and contracting:
        return "LEADING_DIAGONAL"    # overlap + contracting wedge → diagonal
    if overlap and not contracting:
        return "WARN: overlap present but not contracting — expanding diagonal or count error"
```

---

## 7. Zigzag (5-3-5) and Double/Triple Zigzag

### 7.1 Single Zigzag

A zigzag is the sharpest corrective pattern, labeled A-B-C.

**Sub-wave structure: 5-3-5**
- Wave A: impulse or leading diagonal (5 sub-waves)
- Wave B: any three-wave corrective (3 sub-waves)
- Wave C: impulse or ending diagonal (5 sub-waves)

**Hard rules:**
```
1. Wave B must NOT retrace more than 100% of wave A.
   (B endpoint must not cross A's start)

2. Wave B retraces less than 61.8% of wave A.
   (This is the DEFINING threshold separating zigzag from flat; see §8)

3. Wave C must exceed the endpoint of wave A.
   (C carries price beyond A's extreme; otherwise a running flat, not a zigzag)
```

```python
def validate_zigzag(wA, wB, wC) -> list[RuleResult]:
    b_retr = abs_len(wB) / abs_len(wA)
    a_down = wA.end.price < wA.start.price

    # Hard Rule 1: B doesn't cross A start
    r1 = (wB.end.price > wA.start.price) if a_down else (wB.end.price < wA.start.price)

    # Hard Rule 2: B < 61.8% of A (the zigzag/flat split)
    r2 = b_retr <= 0.618

    # Hard Rule 3: C exceeds A end
    r3 = (wC.end.price < wA.end.price) if a_down else (wC.end.price > wA.end.price)
```

**Fibonacci guidelines:**
- B retraces 38.2–61.8% of A (most common: ~50%)
- C ≈ 100% of A (equality, the primary target)
- C = 61.8% of A (secondary target; truncated zigzag)
- C = 161.8% of A (extended C-wave)

Source: EW International Zigzags: https://www.elliottwave.com/waveopedia/zigzags/
EWO Trader zigzag: https://ewotrader.com/blog/elliott-wave/zig-zag-elliott-wave-theory/

### 7.2 Double Zigzag (W-X-Y where W=zigzag, Y=zigzag)

A double zigzag links two zigzags with a connecting X-wave. It is the most common
combination pattern and appears most frequently in wave 2 or wave B positions.

**Structure: W (5-3-5) — X (any 3) — Y (5-3-5)**

**Hard rules for double zigzag:**
```
1. Wave W must be a zigzag.
2. Wave X must be smaller than wave W in price (X < W).
3. Wave X must retrace at least 20% of wave W.
4. Wave Y must be a zigzag.
5. Wave Y must be ≥ wave X in price.
6. Wave C of W cannot be a failure (truncated C that doesn't exceed A endpoint is
   a "C failure" — permitted only in unusual circumstances; WARN if present).
7. Wave X cannot be an ending triangle (triangles are not valid X-waves in most contexts).
```

Source: EW International Combinations: https://www.elliottwave.com/waveopedia/combinations/
EW Monitor double/triple: https://medium.com/@ewmonitors/elliott-wave-theory-everything-you-need-to-know-3c038cc3971f

### 7.3 Triple Zigzag (W-X-Y-X-Z)

Three zigzags linked by two X-waves. Relatively rare. Same rules as double zigzag
applied recursively. Final wave Z must be a zigzag.

---

## 8. Flat (3-3-5) — Regular, Expanded, Running

### 8.1 Common Characteristics

A flat correction is labeled A-B-C with sub-structure **3-3-5**:
- Wave A: any three-wave structure
- Wave B: any three-wave structure (B retraces more of A than in a zigzag)
- Wave C: impulse or ending diagonal (5 sub-waves)

The **defining characteristic of a flat vs zigzag** is the B-wave:
- B retraces > 61.8% of A → flat family
- B retraces ≤ 61.8% of A → zigzag

### 8.2 Regular Flat

```
B retraces approximately 90–100% of A (typically 0.818–1.000 of A).
C extends approximately 100% of A from B's endpoint (C ≈ A in length).
C ends near A's endpoint (does not significantly exceed it).
```

**Fibonacci relationships:**
- B ≈ 0.900–1.000 × A (deep but not exceeding A start)
- C ≈ 1.000 × B (equal to B length; C ends near A endpoint)
- C/A ≈ 1.000 (equality between C and A)

### 8.3 Expanded Flat (most common variant)

```
B exceeds wave A's starting point (B > 100% of A).
Typical B range: 105%–138% of A.
C extends significantly beyond A's endpoint in A's direction.
Typical C range: 1.382–1.618 × A (or even longer).
```

**Hard rules:**
```
1. B > 100% of A (B endpoint crosses A start — the key expanded flat signature).
2. C must exceed A's endpoint (C is longer than A and pushes past it).
```

**Fibonacci relationships:**
- B ≈ 1.236–1.382 × A (primary); 1.000–1.618 (full range)
- C ≈ 1.000 × A (minimum); 1.618 × A (typical extended C)
- C ≈ 1.618 × B is a common target

Source: EW International Flats: https://www.elliottwave.com/waveopedia/flats/
Trading Literacy: https://tradingliteracy.com/flat-correction-elliott-wave/

### 8.4 Running Flat (rare)

```
B exceeds wave A's starting point (B > 100% of A — same signature as expanded flat).
C FAILS to reach A's endpoint (C < A in directional extent).
C falls short in A's direction — it runs out of momentum before completing.
```

**Diagnostic:** The key distinction from expanded flat:
- Expanded flat: C exceeds A endpoint (C pushes past it).
- Running flat: C does NOT reach A endpoint (C falls short).

```python
def classify_flat_subtype(wA, wB, wC):
    a_down = wA.end.price < wA.start.price
    b_retr = abs_len(wB) / abs_len(wA)
    c_beyond_a = (wC.end.price < wA.end.price) if a_down else (wC.end.price > wA.end.price)
    b_beyond_a_start = (wB.end.price > wA.start.price) if a_down else (wB.end.price < wA.start.price)

    if b_retr <= 0.618:
        return "ZIGZAG"  # not a flat
    if b_retr <= 1.00:
        return "REGULAR_FLAT"      # B < A start, C ≈ A endpoint
    # B > 100%: expanded or running based on whether C clears A's endpoint
    if c_beyond_a:
        return "EXPANDED_FLAT"     # B > A start, C exceeds A end
    return "RUNNING_FLAT"          # B > A start, C falls short of A end
```

**Fibonacci relationships (running flat):**
- B ≈ 1.000–1.236 × A
- C ≈ 0.618–0.786 × A (truncated C — short of A endpoint)

Source: Bulkowski running flat: https://thepatternsite.com/EWRunning.html

### 8.5 Post-Flat Implications

After a regular flat: trend resumes with moderate force.
After an expanded flat: powerful trend resumption (the expanded flat represents a
strong holding action by the main trend; the C-wave exhaustion is followed by a swift
resumption).
After a running flat: the strongest subsequent trend signal — the correction was so
brief and shallow that the main trend is exceptionally powerful.

---

## 9. Triangle (3-3-3-3-3) — Four Variants

### 9.1 Common Structure

All triangles are five-wave corrective patterns labeled **A-B-C-D-E**, where each leg
subdivides as a three-wave structure. Triangles appear in:
- Wave 4 of an impulse (most common — wave 5 follows directly).
- Wave B of a flat or zigzag (uncommon).
- Wave X of a combination correction.
- Wave Y or Z of a combination (as the final element — "combinations end with flat or triangle").

The two trendlines used for triangles:
- **A-C line** (connects endpoints of waves A and C).
- **B-D line** (connects endpoints of waves B and D).

Source: EW International Triangles: https://www.elliottwave.com/waveopedia/triangles/
EW Forecast contracting triangle: https://elliottwave-forecast.com/elliott-wave-theory/

### 9.2 Contracting Triangle

The most common variant. Both trendlines converge.

**Hard rules:**
```
1. Wave C never moves beyond wave A's endpoint.
2. Wave D never moves beyond wave B's endpoint.
3. Wave E never moves beyond wave C's endpoint.
4. Wave B may exceed wave A's start (running triangle — see §9.5), but the
   standard contracting triangle does not include this.
5. Sub-wave structure: each of A, B, C, D, E subdivides as a three.
```

**Fibonacci relationships:**
- B ≈ 0.618 × A
- C ≈ 0.618 × B
- D ≈ 0.618 × C
- E ≈ 0.618 × D
(Each leg approximately 0.618 of the preceding same-direction leg.)

```python
def validate_contracting_triangle(wA, wB, wC, wD, wE):
    lens = [abs_len(w) for w in [wA, wB, wC, wD, wE]]
    # Hard rules: each leg does not exceed the previous same-direction leg
    a_down = wA.end.price < wA.start.price
    r1 = (wC.end.price > wA.end.price) if a_down else (wC.end.price < wA.end.price)
    r2 = (wD.end.price > wB.end.price) if not a_down else (wD.end.price < wB.end.price)
    r3 = (wE.end.price > wC.end.price) if a_down else (wE.end.price < wC.end.price)
    # Size contracting
    r4 = all(lens[i] > lens[i+1] for i in range(4))
    return [r1, r2, r3, r4]  # all must be True
```

### 9.3 Barrier Triangle

Same as contracting triangle except one of the two trendlines is approximately
horizontal (the "barrier"):
- If B-D line is horizontal: the triangle breaks upward (the horizontal line is on
  the side the next wave will exceed).
- If A-C line is horizontal: the triangle breaks downward.

```python
def is_barrier_triangle(side_a_c, side_b_d, tol=0.03):
    """Check if one trendline is approximately flat."""
    def nearly_flat(prices):
        mean = sum(prices) / len(prices)
        return mean != 0 and (max(prices) - min(prices)) <= tol * abs(mean)
    return nearly_flat(side_a_c) or nearly_flat(side_b_d)
```

### 9.4 Expanding Triangle

Trendlines diverge. Each leg is longer than the prior same-direction leg.

**Hard rules:**
```
1. Wave C moves beyond wave A's endpoint (C is longer than A).
2. Wave D moves beyond wave B's endpoint (D is longer than B).
3. Wave E moves beyond wave C's endpoint (E is longest of A/C/E).
4. Size ordering: A < B < C < D < E (each leg longer than prior).
```

**Fibonacci relationships:**
- B, C, D typically retrace 105–125% of the preceding sub-wave.

Source: EW International triangles: https://www.elliottwave.com/waveopedia/triangles/

### 9.5 Running Triangle

Wave B exceeds the origin of wave A (goes further than A's start). All other
contracting triangle rules still apply.

```
B exceeds A start → running triangle (not a violation — it identifies the subtype)
C must still not exceed A endpoint
D must still not exceed B endpoint
E must still not exceed C endpoint
```

This pattern indicates a very strong trend — wave B overshoots because the underlying
trend is too powerful to allow a full corrective structure.
Source: EW Forecast running triangle: https://elliottwave-forecast.com/elliottwave/running-triangle-and-how-they-are-different-to-regular-triangles/
Bulkowski running triangle: https://thepatternsite.com/EWTriangleRunning.html

### 9.6 Post-Triangle Thrust

After a triangle completes at wave E, the subsequent thrust (the wave that follows):
- Minimum: travels approximately the distance of wave A (the widest leg) from the
  apex/breakout point.
- Common: travels 75–125% of the widest leg.
- Maximum: can extend to 125%+ in strong markets.

```python
def triangle_thrust_targets(widest_leg_len, breakout_price, direction=1):
    return {
        "minimum": breakout_price + direction * 0.75 * widest_leg_len,
        "primary":  breakout_price + direction * widest_leg_len,
        "extended": breakout_price + direction * 1.25 * widest_leg_len,
    }
```

Source: Frost & Prechter, triangle thrust; EW Markets Waves:
https://www.marketswaves.com/education/elliott-wave-principle-chapter-12

---

## 10. Combinations: Double Three (W-X-Y) and Triple Three (W-X-Y-X-Z)

### 10.1 Definition

Combinations are sequences of two or three individual corrective patterns linked by
X-waves. They appear most commonly in wave 4, wave B, and wave X positions.
They are called "sideways" corrections because their net price movement is relatively
contained compared to the individual component patterns.

Source: EW International Combinations: https://www.elliottwave.com/waveopedia/combinations/
FBS double/triple three: https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns

### 10.2 Double Three (W-X-Y)

**Structure:** W — X — Y

| Component | Valid patterns | Notes |
|---|---|---|
| Wave W | Zigzag, flat, triangle | Cannot be a triangle in W position in most interpretations |
| Wave X | Zigzag (most common), flat, triangle | Cannot be an ending triangle (ET) |
| Wave Y | Zigzag, flat, triangle | Combinations end with flat or triangle |

**Hard rules:**
```
1. Wave X must be smaller than wave W in price extent.
2. Wave X must retrace at least 20% of wave W.
3. Wave X retraces typically 50–61.8% of wave W (guideline).
4. Wave Y must be ≥ wave X in price.
5. The overall combination should not make significant net progress
   (it is a sideways/horizontal correction).
6. No two adjacent components can be of the same type
   (e.g., W=zigzag and Y=zigzag is a "double zigzag" not a "double three").
```

```python
def validate_double_three(wW, wX, wY, w_type: str, x_type: str, y_type: str):
    # Size rules
    x_price = abs_len(wX)
    w_price = abs_len(wW)
    y_price = abs_len(wY)

    r1 = x_price < w_price               # X smaller than W
    r2 = x_price >= 0.20 * w_price       # X retraces at least 20% of W
    r3 = y_price >= x_price               # Y >= X

    # X-wave type restriction (no ending triangle as X)
    r4 = x_type != "ending_triangle"

    # Same-type restriction (prevents two identical patterns)
    r5 = not (w_type == y_type == "zigzag")  # double zigzag is separate label
    return [r1, r2, r3, r4, r5]
```

### 10.3 Triple Three (W-X-Y-X-Z)

Three corrective patterns connected by two X-waves. Each intermediate X-wave follows
the same rules as the X in a double three. The final pattern (Z) is most commonly
a flat or triangle.

**Pattern type constraints:**
- W: any correction except triangle (some sources allow triangle in W)
- X1: same X-wave rules as double three
- Y: any correction
- X2: same X-wave rules
- Z: flat or triangle (combinations must END with a flat or triangle)

### 10.4 X-Wave Detailed Rules

The X-wave is a connecting corrective wave that links two corrective components. It
moves against the direction of the primary correction (i.e., in the direction of the
main trend), creating the "zigzag" appearance between the major correction components.

```
X-wave rules:
1. Any corrective structure is valid (zigzag most common; flat second most common).
2. X must be SMALLER in price than the preceding corrective component (W or Y).
3. X retraces 50–61.8% of W (primary guideline); range 20%–80%.
4. An ending triangle (5-wave contracting triangle at the end of a larger pattern)
   is generally not valid as an X-wave.
5. Time: X typically takes less time than W.
```

Source: EW Forecast double three:
https://elliottwave-forecast.com/elliottwave/elliott-wave-structure-triple-three-corrections/

---

## 11. NeoWave Extensions: Terminal, Diametric, Symmetrical

### 11.1 NeoWave Terminal Impulse

The NeoWave "terminal impulse" is the equivalent of the Elliott Wave ending diagonal,
but with additional constraints derived from Neely's construction procedure.

**Key differences from standard ending diagonal:**
1. The sub-structure 3-3-3-3-3 is strictly enforced.
2. Wave 2 retraces ≥ 61.8% of wave 1 (Neely sets a floor).
3. The fast-full-retrace expectation has a **timing rule**: the post-terminal reversal
   must retrace the terminal in less time than the terminal itself took to form.
4. If wave 2 retraces > 61.8% of wave 1, the pattern may be a terminal regardless of
   the overlapping wave 4.
5. Channeling uses the **2-4 line** (lower boundary) and the **1-3 line** (upper boundary);
   both confirmed by the end of wave 4.

**Post-terminal fast retrace:**
```python
def terminal_retrace_check(terminal_start_t, terminal_end_t, retrace_end_t, retrace_start_price,
                            current_price, terminal_origin_price, up=True):
    terminal_duration = terminal_end_t - terminal_start_t
    retrace_duration = retrace_end_t - terminal_end_t
    # Price: has the retrace reached the terminal's origin?
    fully_retraced = (current_price <= terminal_origin_price) if up else (current_price >= terminal_origin_price)
    # Time: was the retrace faster than the terminal?
    fast = retrace_duration < terminal_duration
    return fully_retraced and fast  # both required for confirmation
```

Source: Neely, *Mastering Elliott Wave* v2, Ch. 5–6;
NeoWave company: https://www.neowave.com/

### 11.2 NeoWave Diametric Formation (7 legs)

A Diametric is a 7-legged formation labeled **a-b-c-d-e-f-g** that does NOT use an
X-wave connector. It is a NeoWave-specific pattern with no direct Elliott Wave equivalent.

**Hard rules:**
```
1. Exactly 7 legs labeled a through g.
2. No X-wave connector (all 7 legs are directly adjacent).
3. Time similarity is the norm (waves tend toward equality in time, not price).
4. Does NOT exhibit Fibonacci price or time relationships.
```

**Two shapes:**
- **Bowtie** (expansion then contraction): legs a–d expand in price, legs e–g contract.
- **Diamond** (contraction then expansion): legs a–d contract, legs e–g expand.

**Post-pattern implication:**
The wave immediately after wave G will be larger and faster than any same-direction leg
within the Diametric.

Source: NeoWave Q&A: https://www.neowave.com/qow/qow-archive-3.asp
WavesStrategy: https://www.wavesstrategy.com/blog/elliottwave-neowave

```python
def validate_diametric(legs: list[Wave]) -> list[RuleResult]:
    if len(legs) != 7:
        return [RuleResult("diametric", NA, f"need 7 legs, got {len(legs)}")]
    results = []
    lens = [abs_len(w) for w in legs]
    # Time similarity (the core NeoWave rule)
    times = [w.days for w in legs]
    t_ratio = max(times) / min(times) if min(times) > 0 else float("nan")
    results.append(RuleResult("diametric time similarity", PASS if t_ratio <= 3.0 else WARN,
                              f"max/min time ratio {t_ratio:.2f} (should be < 3×)"))
    # Detect bowtie vs diamond
    expanding_first = all(lens[i] < lens[i+1] for i in range(3))  # a<b<c<d
    contracting_last = all(lens[i] > lens[i+1] for i in range(3, 6))  # e>f>g
    contracting_first = all(lens[i] > lens[i+1] for i in range(3))  # a>b>c>d
    expanding_last = all(lens[i] < lens[i+1] for i in range(3, 6))  # e<f<g
    if expanding_first and contracting_last:
        shape = "bowtie (expand then contract)"
    elif contracting_first and expanding_last:
        shape = "diamond (contract then expand)"
    else:
        shape = "irregular (WARN)"
    results.append(RuleResult("diametric shape", WARN if "irregular" in shape else PASS, shape))
    return results
```

### 11.3 NeoWave Symmetrical Formation (9 legs)

A Symmetrical is a 9-legged formation where most waves have similar time, price, and
complexity. It is one degree larger than a Diametric in complexity. Like the Diametric,
it does NOT use X-wave connectors and does NOT exhibit Fibonacci relationships.

```
9 legs labeled a through i.
Most waves approach equality in time, price, and structural complexity.
No X-waves.
No Fibonacci price/time relationships.
Post-pattern: move after the formation is large and fast.
```

Source: NeoWave Q&A Symmetrical: https://www.neowave.com/qow/qow-archive-5.asp

---

## 12. Fibonacci Relationship Reference Table

### 12.1 Core Fibonacci Ratios Used in Wave Analysis

| Level | Decimal | Derivation |
|---|---|---|
| 0.236 | 23.6% | φ⁻³ ≈ 0.2361 |
| 0.382 | 38.2% | φ⁻² ≈ 0.3820 |
| 0.500 | 50.0% | arithmetic midpoint |
| 0.618 | 61.8% | φ⁻¹ (the golden ratio reciprocal) |
| 0.786 | 78.6% | √0.618 |
| 1.000 | 100% | equality |
| 1.272 | 127.2% | √1.618 |
| 1.382 | 138.2% | 1 + 0.382 |
| 1.618 | 161.8% | φ (the golden ratio) |
| 2.000 | 200% | double |
| 2.618 | 261.8% | φ² |
| 3.618 | 361.8% | φ³ |
| 4.236 | 423.6% | φ⁴ |

### 12.2 Impulse Wave Fibonacci Relationships

| Wave | Type | Primary ratio | Secondary ratio | Tertiary |
|---|---|---|---|---|
| Wave 2 retr. Wave 1 | Retracement | 0.618 | 0.786 | 0.500 |
| Wave 3 / Wave 1 (if extended) | Extension | 1.618 | 2.618 | 3.618 |
| Wave 4 retr. Wave 3 | Retracement | 0.382 | 0.500 | 0.236 |
| Wave 5 = Wave 1 (W3 extended) | Equality | 1.000 | 0.618 of W1 | — |
| Wave 5 extension target | Extension | W4 end + 1.618×W1 | W4 end + 1.000×W1 | — |
| Wave 5 (W1 extended) | Fibonacci proj | 0.618 × (W1 through W3) from W4 | — | — |

### 12.3 Diagonal Wave Fibonacci Relationships

| Pattern | Wave relationship | Primary ratio | Secondary |
|---|---|---|---|
| Ending diagonal | W2 retr. W1 | 0.618–0.786 | 0.500 |
| Ending diagonal | W4 retr. W3 | 0.618–0.786 | 0.500 |
| Ending diagonal | W3/W1 size | 0.618 (shorter) | 0.786 |
| Ending diagonal | W5/W3 size | 0.618 (shortest) | 0.382 |
| Leading diagonal | W2 retr. W1 | 0.618–0.786 | 0.786–1.000 |
| Leading diagonal | W4 retr. W3 | 0.618–0.786 | 0.786 |
| Post-lead. diag. W2 | Retr. full diagonal | 0.618 | 0.786 |

### 12.4 Corrective Wave Fibonacci Relationships

| Pattern | Wave relationship | Primary | Secondary | Tertiary |
|---|---|---|---|---|
| Zigzag B retr. A | Retracement | 0.500 | 0.382 | 0.618 (limit) |
| Zigzag C / A | Extension | 1.000 (equality) | 0.618 | 1.618 |
| Regular flat B retr. A | Retracement | 0.900–1.000 | 0.818 | — |
| Regular flat C / B | Extension | 1.000 (equality) | — | — |
| Expanded flat B / A | Extension | 1.236–1.382 | 1.000 | 1.618 |
| Expanded flat C / A | Extension | 1.618 | 1.382 | 2.618 |
| Running flat B / A | Extension | 1.000–1.236 | — | — |
| Running flat C / A | Truncated | 0.618–0.786 | — | — |
| Contracting triangle each leg | Ratio to prior same | 0.618 | — | — |
| Expanding triangle each leg | Ratio to prior same | 1.000–1.236 | — | — |
| Double three X retr. W | Retracement | 0.618 | 0.500 | 0.382 |
| Combination Y / W | Ratio | 1.000 (equality) | 0.618 | 1.618 |

### 12.5 Machine-Checkable Fibonacci Tolerance

For automated validation, use ±0.05 (5%) tolerance around each ratio:

```python
FIB_RATIOS = [0.236, 0.382, 0.500, 0.618, 0.786, 1.000,
              1.272, 1.382, 1.618, 2.618, 3.618]
FIB_TOLERANCE = 0.05  # ±5% of the measured distance

def nearest_fib(ratio: float) -> tuple[float, float]:
    """Returns (nearest_fib, distance_from_fib)."""
    closest = min(FIB_RATIOS, key=lambda f: abs(ratio - f))
    return closest, abs(ratio - closest)

def is_near_fib(ratio: float, tol=FIB_TOLERANCE) -> bool:
    _, dist = nearest_fib(ratio)
    return dist <= tol
```

---

## 13. Implementation Priority List for Recursive Wave-Tree Engine

Priority ranking for patterns not yet fully validated in `wavelib/rules.py` and
`wavelib/automation.py`:

### Priority 1 — Ending Diagonal (immediate)

**Why first:** Most frequent gap in the current engine. Ending diagonals appear at
the end of every significant move and are the primary signal for reversal setups.
AVGO and MRVL both show potential ending-diagonal structures.

**Implementation steps:**
1. Add `validate_ending_diagonal(w1,w2,w3,w4,w5)` to `rules.py` using the
   pseudo-code in §4.9 above.
2. Add `check_wedge_convergence()` and `detect_throwover()` helper functions.
3. Add `ending_diagonal_reversal_targets()` to `toolkit.py`.
4. Add test cases with synthetic data: (a) clean contracting ED, (b) ED with
   throw-over, (c) ED with no overlap (should WARN), (d) ED where w4 crosses w2 (FAIL).
5. Wire into `automation.py` `label_and_validate()` as a candidate pattern when
   wave 4/wave 1 overlap is detected in a 5-wave structure.

### Priority 2 — Leading Diagonal (high priority)

**Why second:** Leading diagonals are the signal for powerful 3rd-wave setups. The
deep wave-2 pullback following a leading diagonal is a high-probability entry point.

**Implementation steps:**
1. Extend `leading_diagonal_rules()` in `rules.py` to include Fibonacci checks for
   wave 2 and wave 4 retracement depths (0.618–0.786).
2. Add `leading_diagonal_wave2_targets()` to `toolkit.py`.
3. Add sub-structure verification flag (currently REF; remain REF until sub-degree
   pivot data is available).
4. Test: (a) clean 5-3-5-3-5 leading diagonal, (b) expanding variant, (c) no-overlap
   case (should return WARN not FAIL for the overlap check).

### Priority 3 — Expanding Diagonal (medium priority)

**Why third:** The current `_diagonal_common()` function emits WARN for non-contracting
diagonals. The expanding variant needs explicit validation rules.

**Implementation steps:**
1. Add `expanding_diagonal_rules()` that checks l1 < l3 < l5 and l4 < l2.
2. Add `trendlines_diverge()` test.
3. Wire into the disambiguation decision tree.

### Priority 4 — Zigzag Sub-structure Verification

**Why:** The engine classifies zigzags by B-wave depth only. The 5-3-5 sub-structure
is currently REF. Add sub-degree checking when pivots are available.

### Priority 5 — Flat Subtype Fibonacci Validation

**Why:** Current classification is correct for subtype but doesn't validate Fibonacci
targets for C-wave. Add C-wave target generation to `toolkit.py`.

### Priority 6 — Double/Triple Zigzag (W-X-Y)

**Why:** The combination classifier currently emits REF for multi-leg counts. Add
explicit W-X-Y validator with X-wave size constraints.

### Priority 7 — NeoWave Diametric (7-leg)

**Why:** Out of scope until the primary 5-wave patterns are fully validated, but the
7-leg structure appears in markets. Add as a candidate when a 7-wave structure is
detected that doesn't match any 3+3+3 combination.

### Priority 8 — NeoWave Symmetrical (9-leg)

**Why:** Lowest priority. Very rare. Add only after Diametric is validated.

---

## 14. Caveats and Honesty Flags

1. **Sub-wave verification (the core limitation):** The engine works on sequences of
   pivots at a single degree. Rules for sub-structure (3-3-3-3-3 vs 5-3-5-3-5) cannot
   be machine-checked without sub-degree pivot data. All sub-structure checks are flagged
   as `REF` and require human or multi-degree verification. This is an honest limitation,
   not a design flaw.

2. **Fibonacci ratios are guidelines, not hard rules:** The wave structure rules (hard
   rules) are absolute; the Fibonacci ratio relationships are probabilistic. A pattern
   that satisfies all hard rules but none of the Fibonacci guidelines is still a VALID
   pattern — the count is not wrong, just atypical. Never FAIL a count on Fibonacci
   grounds alone.

3. **Alternation is a guideline:** The expectation that wave 2 and wave 4 will alternate
   in form applies in roughly 70–80% of cases. It is a strong WARN signal, not a FAIL.

4. **Throw-over is an empirical observation, not a rule:** The presence or absence of a
   throw-over does not validate or invalidate an ending diagonal. It is a signal of the
   pattern's completeness (throw-over = likely complete; fall-short = possibly still
   building or truncated 5th).

5. **Contracting diagonal is standard; expanding is rare:** The expanding variant of
   both leading and ending diagonals is significantly rarer. If an expanding diagonal
   is identified, apply additional skepticism and verify with time analysis.

6. **Wave degrees are HEURISTIC:** The Neely bottom-up degree assignment in
   `automation.py assign_degrees_neely()` carries `degree_confidence="HEURISTIC"`.
   Pattern identification across degrees is reliable only when the degree assignment
   itself is reliable. For AVGO and MRVL at H4/weekly timeframes, degree confidence
   is medium.

7. **"Triangle vs. Diagonal" in wave 4:** This is the hardest real-world disambiguation.
   The decision tree in §6 provides the correct algorithm. The key check: does the
   5-wave structure make net directional progress, or is it sideways? Net progress ≥
   40% of total price range → diagonal candidate. Sideways ≤ 30% → triangle candidate.

8. **NeoWave Diametric and Symmetrical lack Fibonacci relationships:** Unlike all
   standard Elliott Wave patterns (which are expected to exhibit Fibonacci price
   relationships), Diametrics and Symmetricals are defined by TIME equality, not price
   Fibonacci. Searching for Fibonacci targets in these patterns is a category error.

9. **Combination patterns can be nested:** A double three can itself be a leg of a
   larger triple three. The recursive nature of the pattern catalog is the source of
   both its power and its ambiguity. The engine should cap recursion depth to avoid
   over-counting.

10. **The AVGO and MRVL terminal over-projection warning (from DOCUMENTATION §9):**
    The `terminal_retrace_window` in `toolkit.py` over-projects timing because it
    assumes the retrace will be "as fast as the terminal built." In practice, the
    retrace often takes longer while still qualifying as a terminal reversal. Use the
    price target (back to diagonal origin) as the primary confirmation, not the timing
    target.

---

## Sources

| # | Source | URL |
|---|---|---|
| 1 | Frost & Prechter, *Elliott Wave Principle*, 10th ed., via Archive.org | https://archive.org/details/elliottwaveprinc0000fros |
| 2 | EW International — Waveopedia: Diagonals | https://www.elliottwave.com/waveopedia/elliott-wave-pattern-diagonals/ |
| 3 | EW International — Waveopedia: Flats | https://www.elliottwave.com/waveopedia/flats/ |
| 4 | EW International — Waveopedia: Triangles | https://www.elliottwave.com/waveopedia/triangles/ |
| 5 | EW International — Waveopedia: Zigzags | https://www.elliottwave.com/waveopedia/zigzags/ |
| 6 | EW International — Waveopedia: Combinations | https://www.elliottwave.com/waveopedia/combinations/ |
| 7 | EW International — Throw-Over definition | https://www.elliottwave.com/waveopedia/throw-over/ |
| 8 | EW International — Channeling | https://www.elliottwave.com/waveopedia/channeling/ |
| 9 | EW International — Fibonacci Relationships | https://www.elliottwave.com/waveopedia/fibonacci-relationships/ |
| 10 | EW Forecast — Elliott Wave Theory: Rules, Guidelines & Structures | https://elliottwave-forecast.com/elliott-wave-theory/ |
| 11 | EW Forecast — Ending Diagonal | https://elliottwave-forecast.com/elliottwave/elliott-wave-theory-ending-diagonal/ |
| 12 | EW Forecast — Introduction to Diagonals | https://elliottwave-forecast.com/elliottwave/introduction-diagonals/ |
| 13 | EW Forecast — Elliott Wave Extensions | https://elliottwave-forecast.com/elliottwave/elliott-wave-extensions/ |
| 14 | EW Forecast — Running Triangle | https://elliottwave-forecast.com/elliottwave/running-triangle-and-how-they-are-different-to-regular-triangles/ |
| 15 | EW Forecast — Triple Three Corrections | https://elliottwave-forecast.com/elliottwave/elliott-wave-structure-triple-three-corrections/ |
| 16 | EW Forecast — Fibonacci Retracement Guide | https://elliottwave-forecast.com/trading/fibonacci-retracement-elliott-wave-guide/ |
| 17 | EW Forecast — Channeling and Trendlines | https://elliottwave-forecast.com/trading/elliott-wave-channeling-trendlines-guide/ |
| 18 | Wikipedia — Elliott Wave Principle | https://en.wikipedia.org/wiki/Elliott_wave_principle |
| 19 | Elliott Wave Monitor — Leading and Ending Diagonal | https://elliottwavemonitor.com/leading-and-ending-diagonal/ |
| 20 | EWM Interactive — Recognize Leading Diagonal | https://ewminteractive.com/recognize-leading-diagonal-pattern |
| 21 | Stock Path Shala — Ending Diagonal | https://stockpathshala.com/elliott-wave-ending-diagonal/ |
| 22 | Stock Path Shala — Leading Diagonal | https://stockpathshala.com/elliott-wave-leading-diagonal/ |
| 23 | FBS — Ending Diagonal Pattern | https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/ending-diagonal-pattern |
| 24 | FBS — Leading Diagonal Pattern | https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/leading-diagonal-pattern |
| 25 | FBS — Fibonacci Ratios and Impulse Waves | https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/fibonacci-ratios-and-impulse-waves |
| 26 | FBS — Zigzag and Flat Patterns | https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/zig-zag-and-flat-patterns-in-trading |
| 27 | FBS — Double/Triple Three | https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns |
| 28 | FBS EU — Alternation Guideline | https://fbs.com/analytics/guidebooks/guidelines-of-alternation-274 |
| 29 | EW International — Alternation | https://www.elliottwave.com/waveopedia/alternation/ |
| 30 | EW International — Equality | https://www.elliottwave.com/waveopedia/equality/ |
| 31 | Headway — Elliott Wave Diagonal Waves | https://hw.online/education/elliott-wave-theory-diagonal-waves/ |
| 32 | EBC Financial Group — Ending Diagonals | https://www.ebc.com/forex/how-do-ending-diagonals-fit-into-your-trading-strategy |
| 33 | Market Bulls — Ending Diagonal | https://market-bulls.com/ending-diagonal-elliott-wave/ |
| 34 | Trading Literacy — Flat Correction | https://tradingliteracy.com/flat-correction-elliott-wave/ |
| 35 | Bulkowski — Running Flat | https://thepatternsite.com/EWRunning.html |
| 36 | Bulkowski — Running Triangle | https://thepatternsite.com/EWTriangleRunning.html |
| 37 | Bulkowski — Double Zigzag | https://thepatternsite.com/EWDoubleZigzag.html |
| 38 | Bulkowski — Leading Triangle (Leading Diagonal) | https://thepatternsite.com/EWleadingTriangle.html |
| 39 | WaveTrack — Expanding Diagonal | https://www.wavetrack.com/tutorials/elliott-wave-expanding-diagonal-patterns.html |
| 40 | Afraid to Trade — Ending/Leading Diagonal Definitions | https://blog.afraidtotrade.com/ending-diagonal-leading-diagonal-and-wedge-definitions-sp500/ |
| 41 | Elliott Wave Trading — Diagonal Triangles | https://elliott-wave-trading.com/education/diagonal-triangles |
| 42 | Glenn Neely, *Mastering Elliott Wave* v2, via NEoWave.com | https://www.neowave.com/product-book.asp |
| 43 | NEoWave Q&A — Diametric Formation | https://www.neowave.com/qow/qow-archive-3.asp |
| 44 | NEoWave Q&A — Symmetrical Formation | https://www.neowave.com/qow/qow-archive-5.asp |
| 45 | NEoWave Q&A — Post-Diametric Behavior | https://www.neowave.com/qow/qow-archive-474.asp |
| 46 | NEoWave Q&A — Triangle vs Non-Triangle | https://www.neowave.com/qow/qow-archive-98.asp |
| 47 | WavesStrategy — NeoWave Diametric | https://www.wavesstrategy.com/blog/elliottwave-neowave |
| 48 | NeoWave Chart — EW vs NeoWave Differences | https://neowavechart.com/2025/08/19/elliottwave-vs-neowave/ |
| 49 | LuxAlgo — Elliott Wave Theory Rules Simplified | https://www.luxalgo.com/blog/elliott-wave-theory-pattern-rules-simplified/ |
| 50 | BabyPips — 3 Cardinal Rules | https://www.babypips.com/learn/forex/the-3-cardinal-rules-and-some-guidelines |
| 51 | CWCount — Elliott Wave Rules | https://cwcount.com/education/elliott-wave-principle-rules/ |
| 52 | CWCount — Elliott Wave Invalidation | https://cwcount.com/blog/elliott-wave-invalidation-example/ |
| 53 | Markets Waves — EWP Chapter 1.2 | https://www.marketswaves.com/education/elliott-wave-principle-chapter-12 |
| 54 | EWO Trader — Zigzag | https://ewotrader.com/blog/elliott-wave/zig-zag-elliott-wave-theory/ |
| 55 | Algotrading Investment — Channeling Technique | https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/ |
| 56 | EW Medium (@ewmonitors) — Everything You Need to Know | https://medium.com/@ewmonitors/elliott-wave-theory-everything-you-need-to-know-3c038cc3971f |
| 57 | FBS Australia — Double Three / Triple Three | https://fbsaustralia.com/en/analytics/guidebooks/double-three-and-triple-three-patterns-372 |
| 58 | Forex Wave Expert — Double/Triple Three | https://forexwaveexpert.com/double-three-and-triple-three-patterns/ |
| 59 | Vantage Markets — EW Theory Guide | https://www.vantagemarkets.com/academy/elliott-wave-theory-guide/ |
| 60 | Rare Metal Blog — What Invalidates an Elliott Wave | https://www.raremetalblog.com/what-invalidates-an-elliott-wave/ |
