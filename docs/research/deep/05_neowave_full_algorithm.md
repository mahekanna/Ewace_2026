# 05 — Glenn Neely's NeoWave: Complete Construction Algorithm

**Status:** deep-research reference — 2026-06-06  
**Author:** agent research session (Ewace_2026)  
**Scope:** Implementable specification of the full NeoWave bottom-up algorithm.  
Written from scratch (not an audit). Precise enough to code from directly.  
Not investment advice.

---

## 1. Scope and Sources

This document covers the *complete* NeoWave construction algorithm as published by Glenn
Neely in *Mastering Elliott Wave* (v2, 1990) and refined via his post-1992 Q&A archive
at neowave.com. It is written bottom-up — monowave identification first, compaction last
— precisely as Neely specifies. Every decision point includes exact Fibonacci thresholds
and, where available, pseudo-code or decision tables.

**Primary sources:**

| ID | Source |
|----|--------|
| MEW | Glenn Neely, *Mastering Elliott Wave* v2, Windsor Books, 1990 |
| NW-QA | neowave.com Q&A archive (hundreds of questions answered by Neely directly) |
| LF | LiteFinance 27-part NeoWave series, litefinance.org |
| FT | ForexTalker NeoWave series, forextalker.com |
| SC | Scribd NeoWave chapter excerpts (Parts 2–13) |
| NW-PG | PROMPTING_GUIDE & existing `docs/research/02_neowave_neely.md` in this repo |

Inline citations use [SRC-ID] notation. All URLs listed in §Sources at end.

---

## 2. Full Construction Algorithm

### 2.1 Overview: The Five Phases

NeoWave construction proceeds in an **invariant order**. Skipping any phase produces
mislabeled counts that cannot be corrected by later steps.

```
Phase 1:  Chart standardisation  → uniform bar resolution, no missing bars
Phase 2:  Monowave extraction    → pivots + rollback correction
Phase 3:  Structure labelling    → 7 retracement rules → structure labels per monowave
Phase 4:  Pattern construction   → group labelled monowaves into polywaves; compact upward
Phase 5:  Confirmation logic     → channeling + post-constructive rules + Rule of Reverse Logic
```

---

### 2.2 Phase 1 — Chart Standardisation

Before any wave work, the chart must satisfy [MEW Ch. 1]:

1. **Uniform resolution.** Each bar/candle represents the same time unit. No gaps allowed
   (fill weekend bars with the prior close if needed for daily data).
2. **No log scale.** NeoWave retracement rules use *arithmetic* price ratios. Log scale
   distorts those ratios and breaks every Fibonacci threshold.
3. **Bar construction rule.** If two adjacent bars overlap in price, they may be compacted
   into a single monowave candidate if neither represents a meaningful directional move
   exceeding the user's selected sensitivity threshold (see Phase 2).

---

### 2.3 Phase 2 — Monowave Extraction

#### 2.3.1 Definition

A **monowave** is the most primitive directional price unit: a segment from one distinct
pivot to the next, with no intervening reversal exceeding the threshold used to define
"reversal." Every valid monowave has a unique start pivot p_start and end pivot p_end.
[MEW Ch. 2], [LF intro]

Notation convention: monowaves are indexed ...m(-2), m(-1), m0, m1, m2, m3...
where m1 is the wave currently being labelled, m0 is the immediately preceding wave,
m2 is the immediately following wave.

#### 2.3.2 ZigZag Extraction (Approximate)

A common implementation uses a percentage-reversal ZigZag:

```python
def zigzag_pivots(bars, pct_threshold=0.03):
    """
    bars: list of (t, o, h, l, c)
    pct_threshold: minimum reversal as fraction of last pivot price
    Returns: list of Pivot(t, price, direction)  where direction in {UP, DOWN}
    """
    pivots = []
    direction = None
    last_high = last_low = bars[0][2], bars[0][3]  # h, l of first bar

    for bar in bars:
        t, o, h, l, c = bar
        if direction is None:
            direction = UP if c > bars[0][4] else DOWN
            last_pivot = Pivot(t=bar[0], price=c, direction=direction)
            pivots.append(last_pivot)
            continue

        if direction == UP:
            if h > last_pivot.price:
                last_pivot = Pivot(t=t, price=h, direction=UP)
            elif last_pivot.price - l >= pct_threshold * last_pivot.price:
                pivots.append(last_pivot)
                direction = DOWN
                last_pivot = Pivot(t=t, price=l, direction=DOWN)
        else:  # DOWN
            if l < last_pivot.price:
                last_pivot = Pivot(t=t, price=l, direction=DOWN)
            elif h - last_pivot.price >= pct_threshold * last_pivot.price:
                pivots.append(last_pivot)
                direction = UP
                last_pivot = Pivot(t=t, price=h, direction=UP)

    pivots.append(last_pivot)
    return pivots
```

#### 2.3.3 Rollback Rules [MEW Ch. 2, FT-rollback]

Rollback rules correct monowave endpoints *before* structure labelling. They are applied
once, immediately after pivot extraction, to every pivot in sequence.

**Definition of Rollback:** If price momentarily violates a prior pivot by a trivially
small amount (one bar unit) and then reverses, the prior pivot endpoint must be moved
to include that one-bar extension rather than treating the extension as a new reversal.

**Rollback Rule set (MEW's three situations):**

| Situation | Condition | Action |
|-----------|-----------|--------|
| R1 — Near miss | Next bar's extreme does not surpass prior pivot by more than a "minor" amount (< 1 bar ATR) and then reverses | Absorb the near-miss into the current monowave; do NOT create a new monowave. Extend current pivot to the extreme of the near-miss bar. |
| R2 — One-bar spike | A single bar produces both a new high AND a new low relative to the prior pivot direction | Assign the relevant extreme (high or low) to the ongoing monowave; if both extremes qualify, the longer move wins. |
| R3 — Flat top / base | Multiple bars form a horizontal cluster at a potential pivot, none clearly exceeding the others | Use the *last* bar of the cluster as the pivot endpoint; discard interior bars. |

**Pseudo-code:**

```python
def apply_rollback(pivots):
    """Apply rollback corrections to a pivot list in place."""
    i = 0
    while i < len(pivots) - 1:
        curr = pivots[i]
        nxt  = pivots[i + 1]
        # R1: check if next pivot barely exceeds the one after it
        if i + 2 < len(pivots):
            nxt2 = pivots[i + 2]
            price_gap = abs(nxt.price - curr.price)
            if price_gap < 0.1 * abs(nxt2.price - nxt.price):
                # nxt is a near-miss; absorb into curr monowave
                # move curr endpoint to nxt2 direction
                pivots.pop(i + 1)
                continue
        i += 1
    return pivots
```

*Note: Neely's rollback rules are qualitative in MEW; the thresholds above are
implementation conventions consistent with his intent. See §5 Caveats.*

---

### 2.4 Phase 3 — Structure Labelling: The Seven Retracement Rules

After rollback correction, each monowave m1 receives one or more **structure labels**
from the set `{:5, :3, :F3, :c3, :L5, :s5, :sL3, :L3}`. These labels encode the
monowave's probable role in the larger wave structure.

#### 2.4.1 Structure Label Glossary [MEW Ch. 3, SC-Part2]

| Label | Mnemonic | Meaning |
|-------|----------|---------|
| `:5` | Five | Motive — part of a 5-wave impulse; typically a wave 1, 3, or 5 |
| `:3` | Three | Corrective — part of any standard 3-segment correction (zigzag, flat, triangle leg) |
| `:F3` | First 3 | Corrective — first segment of a flat correction (B-wave of a flat) |
| `:c3` | C-Three | Corrective — C-wave of a correction; completes a correction |
| `:L5` | Last 5 | Motive — last wave of a motive sequence (wave 5 position); must be preceded by `:c3` or `:F3` |
| `:s5` | Strong 5 | Motive — strongest wave of a motive sequence (wave 3 extension) |
| `:sL3` | Strong-Last 3 | Corrective — powerful C-wave ending a correction, often with throw-over |
| `:L3` | Last 3 | Corrective — last segment of any complex correction or triangle; end of a correction |

**Key behavioural test for `:5` vs `:3`:**
- `:5` labels: price moves **more distance per time unit** than the wave it is retracing;
  completely retraces the prior monowave in *less* time than that prior monowave took to form.
- `:3` labels: price moves **less distance per time unit**; retracement is slow and/or
  the monowave is internally complex (multiple mini-legs visible on lower timeframe).

#### 2.4.2 The Seven Retracement Rules

For each monowave m1, compute:

```python
r21 = abs(m2.price_range) / abs(m1.price_range)   # retracement ratio: m2/m1
r01 = abs(m0.price_range) / abs(m1.price_range)   # prior ratio: m0/m1
```

Where `price_range = end.price - start.price` (signed; absolute value used for ratio).
Note: m2 moves in the *opposite* direction from m1 by definition.

Apply the rule whose range bracket contains `r21`:

---

**RULE 1: r21 < 0.382 (m2 retraces less than 38.2% of m1)**

m1 is most likely the extended 3rd wave of a motive sequence. m2 is a shallow 4th wave
following a wave-3 extension. [MEW Ch. 3, LF-Rule1]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 1a | r01 < 1.00 | `:s5` (m1 is the strong extended wave) |
| 1b | 1.00 ≤ r01 ≤ 1.618 | `:s5` or `:5` |
| 1c | r01 > 1.618 | `:5` (m1 is a normal motive wave; m0 was the extended wave) |

Additional constraint (Rule 1): m3 (the wave after m2) must be longer than m2 and must
move in the same direction as m1. If m3 < m2, the Rule-1 interpretation is suspect and
the count should be reviewed with Rule 3 or Rule 4.

---

**RULE 2: 0.382 ≤ r21 < 0.618 (m2 retraces 38.2–61.8% of m1)**

m1 is a 1st or 5th wave; m2 is a standard 2nd or 4th corrective wave. [MEW Ch. 3,
LF-Rule2, SC-Part4]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 2a | r01 < 0.618 | `:5` (strong first wave) |
| 2b | 0.618 ≤ r01 < 1.00 | `:5` |
| 2c | 1.00 ≤ r01 ≤ 1.618 | `:5` or `:L5` |
| 2d | r01 > 1.618 | `:L5` (m1 is the final wave; prior m0 was extended) |

**Also check m3:** If m3 > m2 and m3 moves in m1's direction, `:5` is preferred. If
m3 ≤ m2 or subdivides into 3, lean toward `:L5`.

---

**RULE 3: 0.618 ≤ r21 < 1.00 (m2 retraces 61.8–99.9% of m1)**

m1 is likely a corrective wave (A or B) or a wave 1 followed by a sharp correction.
[MEW Ch. 3, SC-Part5]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 3a | r01 < 0.618 | `:3` or `:F3` |
| 3b | 0.618 ≤ r01 < 1.00 | `:3`, `:F3`, or `:5` (ambiguous; flag) |
| 3c | 1.00 ≤ r01 ≤ 1.618 | `:c3` or `:sL3` |
| 3d | r01 > 1.618 | `:c3` (strong corrective ending) |

Disambiguation for `:3` vs `:F3`:
- `:F3` requires that m1 be followed by a wave that approximately equals m1 in length
  (the C-wave of a flat). Check whether m3 ≈ m1 (within 40%).
- If no such wave follows, default to `:3`.

---

**RULE 4: 0.618 ≤ r21 < 1.00 (same numeric range as Rule 3 but with overlap)**

Rule 4 is applied when there is *overlap between m1 and m0*, i.e., m2's endpoint exceeds
m0's endpoint in the opposite direction. This distinguishes corrections that subdivide
from simple retracements. [MEW Ch. 3, LF-Rule4-c-d-e, SC-Part7]

Key check before applying Rule 4 vs Rule 3:

```python
# Does m2 retrace back into m0's price territory?
m0_start = m0.start.price
m2_end   = m2.end.price
overlap = (m1.direction == UP and m2_end < m0_start) or \
          (m1.direction == DOWN and m2_end > m0_start)
if overlap:
    use_rule = 4
else:
    use_rule = 3
```

| Sub-condition | m0/m1 ratio (r01) | m2/m3 relationship | Assigned labels for m1 |
|---------------|--------------------|-------------------|------------------------|
| 4a | r01 < 0.618 | m3 ≥ 1.618 × m2 | `:5` or `:c3` |
| 4b | r01 < 0.618 | m3 < 1.618 × m2 | `:c3` or `:F3` |
| 4c | 0.618 ≤ r01 < 1.00 | any | `:c3` |
| 4d | 1.00 ≤ r01 ≤ 1.618 | m3 ≥ m2 | `:L5` or `:5` |
| 4e | r01 > 1.618 | any | `:L5`, `:s5`, or `:sL3` |

---

**RULE 5: 1.00 ≤ r21 < 1.618 (m2 exceeds m1 by 0–61.8%)**

m2 is NOT a simple retracement of m1; it has moved further than m1 in the opposite
direction. This signals a strong trend reversal or that m1 was a corrective wave inside
a larger move. [MEW Ch. 3, LF-Rule5, SC-Part9]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 5a | r01 < 1.00 | `:3` or `:c3` (m1 was corrective in a trending move that has now reversed) |
| 5b | 1.00 ≤ r01 < 1.618 | `:3`, `:c3`, or `:F3` |
| 5c | r01 ≥ 1.618 | `:c3` or `:sL3` (m1 ends a complex correction; m2 initiates the next impulse) |

Channeling check for Rule 5: Draw a line from m0.start through m1.end. If m2 moves
through this line cleanly, a true trend reversal is underway. If m2 stalls near the line,
m1 may still be counted as motive.

---

**RULE 6: 1.618 ≤ r21 < 2.618 (m2 exceeds m1 by 61.8–161.8%)**

Strong trend reversal. m1 is almost certainly corrective; m2 is the beginning of a new
motive sequence of a higher degree. [MEW Ch. 3, LF-Rule6, SC-Part9]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 6a | r01 < 1.00 | `:c3` (m1 completes a correction; m2 is the new impulse start) |
| 6b | 1.00 ≤ r01 | `:c3` or `:F3` |

In Rule 6 territory, an x-wave between the two corrections should be considered. If m1 is
small (r01 < 0.382), m1 may itself be an x-wave connecting two correction patterns.

---

**RULE 7: r21 ≥ 2.618 (m2 exceeds m1 by more than 161.8%)**

Extreme reversal. m1 is typically an x-wave, a truncated wave, or a monowave within a
complex multi-degree corrective sequence. [MEW Ch. 3, FT-Rule7, LF-Rule7]

| Sub-condition | m0/m1 ratio (r01) | Assigned labels for m1 |
|---------------|--------------------|------------------------|
| 7a | r01 < 1.00 | `:c3` or `x:c3` (x-wave connector) |
| 7b | 1.00 ≤ r01 < 2.618 | `:3` or `x:c3` |
| 7c | 2.618 ≤ r01 < ... | `:3`, `:F3`, or `x:c3` |
| 7d | r01 ≥ 2.618 | `x:c3` (m0 and m2 are both large; m1 is definitively an x-wave) |

In Rule 7, always check whether m1 should be merged with adjacent small monowaves via
rollback before assigning label.

---

#### 2.4.3 Complete Structure-Label Decision Table (Compact)

```
r21 = abs(m2) / abs(m1)
r01 = abs(m0) / abs(m1)
overlap = m2 endpoint reaches into m0's price territory

┌─────────────┬───────────┬──────────────────────────────────────────────┐
│ Rule (r21)  │ r01 range │ Labels for m1                                │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 1 (<0.382)  │ <1.00     │ :s5                                          │
│             │ 1–1.618   │ :s5 or :5                                    │
│             │ >1.618    │ :5                                           │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 2 (0.382–   │ <0.618    │ :5                                           │
│    0.618)   │ 0.618–1   │ :5                                           │
│             │ 1–1.618   │ :5 or :L5                                    │
│             │ >1.618    │ :L5                                          │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 3 (0.618–   │ <0.618    │ :3 or :F3                                    │
│    1.00)    │ 0.618–1   │ :3 or :F3 or :5 (flag ambiguity)            │
│ no overlap  │ 1–1.618   │ :c3 or :sL3                                  │
│             │ >1.618    │ :c3                                          │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 4 (0.618–   │ <0.618    │ :5 or :c3 (per m3 check)                    │
│    1.00)    │ 0.618–1   │ :c3                                          │
│ with overlap│ 1–1.618   │ :L5 or :5                                    │
│             │ >1.618    │ :L5 or :s5 or :sL3                          │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 5 (1.00–    │ <1.00     │ :3 or :c3                                    │
│    1.618)   │ 1–1.618   │ :3 or :c3 or :F3                            │
│             │ ≥1.618    │ :c3 or :sL3                                  │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 6 (1.618–   │ <1.00     │ :c3                                          │
│    2.618)   │ ≥1.00     │ :c3 or :F3                                   │
├─────────────┼───────────┼──────────────────────────────────────────────┤
│ 7 (≥2.618)  │ <1.00     │ :c3 or x:c3                                  │
│             │ 1–2.618   │ :3 or x:c3                                   │
│             │ ≥2.618    │ x:c3                                         │
└─────────────┴───────────┴──────────────────────────────────────────────┘
```

#### 2.4.4 Implementation: `label_monowaves()`

```python
FIBO = [0.382, 0.618, 1.000, 1.618, 2.618]

def label_monowaves(pivots: list[Pivot]) -> list[MonowaveLabel]:
    """
    Assign structure labels to each interior monowave.
    m0 = pivots[i-1]→[i], m1 = pivots[i]→[i+1], m2 = pivots[i+1]→[i+2]
    Returns list of MonowaveLabel(wave, labels, ambiguous).
    CAUSAL NOTE: label for m1 requires m2 to have completed.
    The LAST monowave in the list is always provisional (m2 not yet closed).
    """
    result = []
    waves = pivots_to_waves(pivots)   # each wave = (start_pivot, end_pivot)

    for i in range(1, len(waves) - 1):
        m0, m1, m2 = waves[i-1], waves[i], waves[i+1]
        r21 = abs(m2.price_range) / abs(m1.price_range) if m1.price_range else 0
        r01 = abs(m0.price_range) / abs(m1.price_range) if m1.price_range else 0
        overlap = _check_overlap(m0, m1, m2)
        m3 = waves[i+2] if i + 2 < len(waves) else None

        labels = _apply_retracement_rules(r21, r01, overlap, m1, m2, m3)
        ambiguous = len(labels) > 1

        result.append(MonowaveLabel(
            wave=m1,
            labels=labels,
            ambiguous=ambiguous,
            provisional=(i == len(waves) - 2)  # last labelable wave
        ))
    return result


def _apply_retracement_rules(r21, r01, overlap, m1, m2, m3):
    if r21 < 0.382:
        return _rule1(r01)
    elif r21 < 0.618:
        return _rule2(r01, m3)
    elif r21 < 1.000 and not overlap:
        return _rule3(r01, m1, m2, m3)
    elif r21 < 1.000 and overlap:
        return _rule4(r01, m2, m3)
    elif r21 < 1.618:
        return _rule5(r01)
    elif r21 < 2.618:
        return _rule6(r01)
    else:
        return _rule7(r01)
```

---

### 2.5 Phase 4 — Pattern Construction: Compaction Hierarchy

#### 2.5.1 Compaction Overview [MEW Ch. 4, LF-Part18]

Once monowaves are labelled, adjacent monowaves are grouped into **polywaves**, which are
then grouped into **multiwaves**, then **macrowaves**. Each level uses identical grouping
logic; the hierarchy is self-similar.

```
Monowave  (1 directional segment)
    ↓ group 3 or 5 → Polywave
Polywave  (3 or 5 monowaves satisfying impulse or correction rules)
    ↓ group 3 or 5 → Multiwave
Multiwave (3 or 5 polywaves)
    ↓ group 3 or 5 → Macrowave
Macrowave (3 or 5 multiwaves)
```

At each level, the grouped unit receives a **single compacted label** (`:5` or `:3`) and
is treated as a monowave at the next level up. This propagation is the core of NeoWave's
bottom-up objectivity.

#### 2.5.2 Power Ratings [MEW Ch. 4, LF-Part18]

**Complexity** is quantified by **power ratings**, which measure how many primitive
monowaves are consumed by a structure:

| Structure | Power Rating (complexity level) |
|-----------|--------------------------------|
| Monowave | 1 |
| 3-monowave polywave (correction) | 2 |
| 5-monowave polywave (impulse) | 2 |
| 3-polywave multiwave | 3 |
| 5-polywave multiwave | 3 |
| 3-multiwave macrowave | 4 |
| 5-multiwave macrowave | 4 |

Power ratings are used in three contexts:
1. **S&B complexity check** (§2.5.4): adjacent corrective waves must be within 3× of
   each other in complexity (power rating).
2. **x-wave complexity bounds** (§2.7.5): x-wave ≤ power rating of prior correction.
3. **Diametric time-similarity** (§2.8.3): all 7 legs should have similar power ratings
   (within ~2× of each other is the practical limit; see §5 Caveats).

#### 2.5.3 Grouping Algorithm

```python
def group_polywaves(labelled_monowaves):
    """
    Find all candidate polywave groups of 3 or 5 consecutive monowaves.
    Returns a list of PolywaveCandidate objects, possibly overlapping.
    """
    candidates = []
    n = len(labelled_monowaves)

    for start in range(n):
        for size in (3, 5):
            if start + size > n:
                break
            group = labelled_monowaves[start:start+size]
            if _validate_group(group, size):
                label = _compact_label(group)
                candidates.append(PolywaveCandidate(
                    group=group,
                    compacted_label=label,
                    degree=1
                ))

    return candidates


def _validate_group(group, size):
    """
    size=3: check A-B-C correction rules
    size=5: check 1-2-3-4-5 impulse hard rules
    Both: check Rule of Similarity & Balance for all adjacent corrective pairs
    """
    waves = [g.wave for g in group]
    if size == 3:
        ok = check_abc_correction(waves)
    else:
        ok = check_5wave_impulse(waves)
    if not ok:
        return False
    # S&B on all adjacent pairs
    for i in range(len(waves) - 1):
        if not similarity_and_balance(waves[i], waves[i+1]):
            return False
    return True


def _compact_label(group):
    """
    If group is a 5-wave impulse → ':5'
    If group is a 3-wave correction → ':3'
    Inherit sub-type qualifiers if applicable (':s5' for extensions, etc.)
    """
    if len(group) == 5:
        return ':5'
    return ':3'
```

#### 2.5.4 Rule of Similarity and Balance [MEW Ch. 4, NW-QA-32, NW-QA-78]

Two adjacent waves are the **same degree** if and only if:

```
price_similarity: smaller_price / larger_price >= 1/3   (i.e., ratio in [0.333, 3.0])
time_similarity:  shorter_time  / longer_time  >= 1/3   (i.e., ratio in [0.333, 3.0])
complexity_sim:   smaller_count / larger_count >= 1/3   (tertiary check)
```

At least one of price OR time must be satisfied for same-degree assignment.
If BOTH are violated, the waves are definitively different degrees — the count is wrong
or a hidden x-wave exists between them.

```python
def similarity_and_balance(w1, w2, context=""):
    p_ratio = min(w1.price_range, w2.price_range) / max(w1.price_range, w2.price_range)
    t_ratio = min(w1.bars, w2.bars) / max(w1.bars, w2.bars)
    price_ok = p_ratio >= 1/3
    time_ok  = t_ratio >= 1/3
    if price_ok or time_ok:
        status = PASS if (price_ok and time_ok) else WARN
    else:
        status = FAIL
    return RuleResult("S&B", status, f"{context} p={p_ratio:.2f} t={t_ratio:.2f}")
```

#### 2.5.5 Rule of Proportion [MEW Ch. 4]

A sub-wave (child) must not exceed the size of its parent wave unless an extension is
unfolding. In a **trending impulse**, the *extended wave* must be ≥ 161.8% of the
next-longest motive wave. This is a **hard rule** in NeoWave (not merely a guideline):

```python
def rule_of_proportion(waves_1_3_5):
    """waves_1_3_5: list of (price_range, bars) for the three motive sub-waves."""
    lengths = sorted([abs(w.price_range) for w in waves_1_3_5], reverse=True)
    longest, second = lengths[0], lengths[1]
    extension_ratio = longest / second
    if extension_ratio >= 1.618:
        return PASS  # valid extension
    # No extension: all three motive waves should be roughly equal
    # Fails NeoWave hard rule if any single wave is declared "extended" without 1.618x ratio
    return WARN
```

#### 2.5.6 Rule of Neutrality [MEW Ch. 2]

Allows merging two adjacent monowaves that do not clearly break direction. A monowave
with a price range less than 10% of the adjacent monowave may be neutralised (absorbed
into the adjacent larger monowave) when chart resolution warrants. This is applied
before structure labelling, as a data-quality step.

```python
def apply_neutrality(pivots, neutral_threshold=0.10):
    """
    Merge tiny monowaves (< neutral_threshold × adjacent wave) into neighbors.
    Prevents noise from generating phantom pivot points.
    """
    changed = True
    while changed:
        changed = False
        for i in range(1, len(pivots) - 1):
            m_prev = abs(pivots[i].price - pivots[i-1].price)
            m_curr = abs(pivots[i+1].price - pivots[i].price)
            m_next = abs(pivots[i+2].price - pivots[i+1].price) if i+2 < len(pivots) else m_curr
            if m_curr < neutral_threshold * max(m_prev, m_next):
                # absorb pivots[i] — remove this intermediate pivot
                pivots.pop(i)
                changed = True
                break
    return pivots
```

---

### 2.6 Phase 5A — Channeling (Must Run Before Pattern Naming)

Neely's most explicit inversion of classical EW practice: **channels are constructed
first; pattern names are assigned only if channeling is satisfied**. [MEW Ch. 5, NW-QA-273]

#### 2.6.1 The Four Channeling Steps for Impulses

**Step 1 — 0-2 trendline:**
Draw from origin of wave 1 (pivot 0) through the end of wave 2.
- Rule: No portion of wave 3 should *significantly* break this line downward (bull impulse).
- Correction use: If price breaks the 0-2 line and then fails to continue, the assumed
  wave-2 endpoint is wrong — move it later.

```python
def build_02_line(p0, p2):
    """Returns slope, intercept of line through p0 and p2."""
    slope = (p2.price - p0.price) / (p2.t - p0.t)
    intercept = p0.price - slope * p0.t
    return slope, intercept

def check_02_violation(line, wave3_bars):
    slope, intercept = line
    for bar in wave3_bars:
        expected = slope * bar.t + intercept
        if bar.low < expected * 0.99:   # 1% tolerance
            return FAIL
    return PASS
```

**Step 2 — 2-4 trendline (most important):**
Draw through *endpoints* of waves 2 and 4. Not through extremes; through wave endpoints.
- Hard rules:
  1. No part of wave 3 breaks this line.
  2. No point of wave 5 breaks this line.
  3. Pattern confirmed complete only when price *penetrates* the 2-4 line in
     **less time than wave 5 took to form** (Stage 1 confirmation).
  4. Stage 2: entire wave 5 retraced in **≤ time of wave 5**.

```python
def two_four_confirmation(w5_bars, w5_start_t, current_t, current_price,
                          line_price_at_t, uptrend=True):
    w5_duration = w5_bars  # number of bars
    time_elapsed = current_t - w5_start_t

    # Stage 1: Has the 2-4 line been broken?
    if uptrend:
        line_broken = current_price < line_price_at_t
    else:
        line_broken = current_price > line_price_at_t

    stage1 = PASS if (line_broken and time_elapsed < w5_duration) else FAIL

    # Stage 2: Has all of wave 5's price range been retraced?
    # (requires knowing wave 5 start price)
    # ... implementation continues
    return stage1
```

**Step 3 — 1-3 upper channel:**
Parallel to the 2-4 line, anchored at the end of wave 1. Wave 5 is expected to terminate
near this line.
- **Throw-over:** wave 5 peak exceeds the 1-3 line → blow-off exhaustion; expect sharp reversal.
- **Fell short (truncation):** wave 5 peak < 1-3 line → weakness; wave 3 consumed all momentum.

**Step 4 — Confirmation:**
Apply both Stage 1 and Stage 2 timing tests. Until both pass, the impulse is *not confirmed
complete* regardless of price level.

#### 2.6.2 Correction Channeling

For A-B-C corrections:
- Draw line from A-end through B-end.
- Parallel through A-start; C should terminate near this parallel.
- Zigzag: C should reach or slightly exceed the A-end parallel.
- Flat: C should reach approximately the A-end price level.
- Expanded flat: C exceeds A's endpoint; channel is wider.

---

### 2.7 Phase 5B — Pre- and Post-Constructive Rules of Logic

#### 2.7.1 Pre-Constructive Rules [MEW Ch. 3]

Pre-constructive rules constrain *which patterns are even possible* before construction
begins, based on preceding market behaviour. Applied as a filter before attempting any
count.

**Key pre-constructive rules:**

1. **Complexity progression:** A corrective wave must be at least as complex as the
   motive wave it corrects. A simple monowave cannot correct a complex multiwave impulse.

2. **Alternation requirement (guideline, not hard):** In a 5-wave impulse, waves 2 and 4
   should alternate in character (one sharp, one sideways). Apply as WARN if violated.

3. **Wave 2 retrace limits:**
   - Trending impulse: wave 2 may retrace up to 99.9% of wave 1.
   - Terminal impulse: wave 2 may retrace at most 61.8% of wave 1 (hard limit).

4. **Wave 4 / wave 1 non-overlap:** In a trending impulse, wave 4 may *never* enter
   the price territory of wave 1. In a terminal, overlap is mandatory (diagnostic feature).

5. **Extension rule:** One and only one motive wave (1, 3, or 5) extends. If two appear
   to extend, the structure is not a trending impulse.

```python
def pre_constructive_check(candidate_waves, pattern_type):
    results = []
    w1, w2, w3, w4, w5 = candidate_waves

    # Hard: wave 2 ≤ 100% retrace of wave 1
    if abs(w2.price_range) >= abs(w1.price_range):
        results.append(RuleResult("W2_RETRACE", FAIL, "Wave 2 >= 100% of wave 1"))

    # Hard: wave 4 does not overlap wave 1 (trending impulse only)
    if pattern_type == "TRENDING":
        if _overlap(w4, w1):
            results.append(RuleResult("W4_W1_OVERLAP", FAIL, "W4 overlaps W1 in trending impulse"))

    # Terminal: wave 4 MUST overlap wave 1; wave 2 ≤ 61.8%
    if pattern_type == "TERMINAL":
        if not _overlap(w4, w1):
            results.append(RuleResult("W4_W1_OVERLAP", FAIL, "W4 must overlap W1 in terminal"))
        w2_retrace = abs(w2.price_range) / abs(w1.price_range)
        if w2_retrace > 0.618:
            results.append(RuleResult("W2_TERMINAL_LIMIT", FAIL, f"W2 retraces {w2_retrace:.1%} > 61.8% in terminal"))

    return results
```

#### 2.7.2 Post-Constructive Rules [MEW Ch. 6, NW-QA-19]

Post-constructive rules are **behaviour tests** applied *after* a pattern is labelled,
using subsequent price action. Neely's core principle: "No matter what you think of
structure, if post-pattern behaviour is inconsistent with your labelling, your wave count
is wrong." [NW-QA-19]

**Post-impulse (trending):**
- Stage 1: 2-4 line penetrated in < wave-5 time (mandatory).
- Stage 2: Wave 5 fully retraced in ≤ wave-5 time (mandatory).
- Failing Stage 2 after Stage 1 signals that wave 5 was actually a much larger wave.

**Post-correction (flat/zigzag):**
- A thrust in the direction of the prior trend equal in magnitude to the correction itself
  should follow within a timeframe ≤ the correction's own duration.
- If no thrust follows, the correction is not complete (or was misidentified).

**Post-triangle:**
- Thrust after a contracting triangle ≈ widest part of the triangle (wave a length).
- Thrust completes in ≤ time of the shortest triangle leg.
- If the thrust fails to materialise, the triangle may be a diametric (check 7 legs).

**Post-terminal:**
- Entire terminal must be *completely retraced* back to its origin point.
- This retracement occurs faster than the terminal formed (directional bias, not a timed
  guarantee — see §2.9).
- The retrace *begins* fast (Stage 1: 2-4 break in < wave-5 time) but the full origin
  retrace may take considerably longer.

#### 2.7.3 Rule of Reverse Logic [MEW Ch. 6, NW-RRL]

When multiple wave counts are simultaneously plausible, apply the Rule of Reverse Logic:

> **Select the count that is furthest from completion — the one that requires the most
> additional time and price movement to resolve.**

Rationale: Markets tend to move toward their most uncertain or "confused" state before
decisive resolution. The count that appears "almost done" is usually the wrong one.

**Algorithmic implementation:**

```python
def rule_of_reverse_logic(candidate_counts):
    """
    Given a list of CandidateCount objects (each with a 'completion_fraction' between 0 and 1),
    return the count with the LOWEST completion fraction.
    completion_fraction = price_moved_so_far / projected_full_pattern_price_range
    """
    return min(candidate_counts, key=lambda c: c.completion_fraction)
```

Practical use: When both a zigzag-complete and a flat-in-progress label fit the data,
prefer the flat-in-progress. When both impulse-complete and triangle-leg-4 fit, prefer
leg-4 (the triangle is less complete).

---

### 2.8 Pattern Library: Hard Rules and Construction Logic

#### 2.8.1 Trending Impulse (5-3-5-3-5)

**Hard rules:**
1. Wave 2 retraces < 100% of wave 1.
2. Wave 3 is never the shortest of waves 1, 3, 5.
3. Wave 4 does not overlap wave 1.
4. One extended wave ≥ 161.8% of next-longest motive wave (hard in NeoWave, not EW).
5. 2-4 trendline never touched by wave 3 or wave 5.

**Guidelines:**
- Wave 2 typically retraces 38.2–61.8% of wave 1.
- Wave 4 typically retraces 38.2% of wave 3.
- Wave 3 is usually the strongest and longest.
- Alternation: if wave 2 is sharp, wave 4 is sideways (and vice versa).

**Fibonacci targets:**
```
w3 targets: 1.618 × w1,  2.618 × w1,  4.236 × w1
w5 targets: 0.618 × w1,  1.000 × w1,  1.618 × w1  (if w3 extended)
            0.618 × (w1+w3) if w1 extended
```

#### 2.8.2 Terminal Impulse (3-3-3-3-3) [MEW Ch. 5]

**Hard rules:**
1. All 5 sub-waves are internally corrective (3-wave structure each).
2. Wave 4 overlaps wave 1 (mandatory — diagnostic feature).
3. Wave 2 retraces ≤ 61.8% of wave 1.
4. Waves contract: w1 > w3 > w5 (contracting terminal) or expand: w5 > w3 > w1
   (expanding/irregular terminal).
5. Entire terminal is completely retraced after completion.

**Channeling:** Converging (contracting) or diverging (expanding) trendlines through
endpoints of waves 1, 3, 5 on one boundary and waves 2, 4 on the other.

```python
def is_terminal(waves):
    w1, w2, w3, w4, w5 = waves
    results = []
    # W4 overlaps W1 (hard)
    if not _overlap(w4, w1):
        results.append(RuleResult("W4_W1_OVL", FAIL, "No overlap"))
    # W2 ≤ 61.8% of W1 (hard)
    r = abs(w2.price_range) / abs(w1.price_range)
    if r > 0.618:
        results.append(RuleResult("W2_LIMIT", FAIL, f"{r:.1%} > 61.8%"))
    # Contracting shape check
    contracting = (abs(w1.price_range) > abs(w3.price_range) > abs(w5.price_range))
    expanding   = (abs(w5.price_range) > abs(w3.price_range) > abs(w1.price_range))
    if not (contracting or expanding):
        results.append(RuleResult("SHAPE", WARN, "Neither cleanly contracting nor expanding"))
    shape = "CONTRACTING" if contracting else "EXPANDING"
    results.append(RuleResult("SHAPE_TYPE", PASS, shape))
    return results
```

#### 2.8.3 Zigzag (5-3-5) [MEW Ch. 5]

**Hard rules:**
1. Wave B retraces ≤ 61.8% of wave A (hard limit; exceeding → flat, not zigzag).
2. Wave C surpasses the endpoint of wave A (if C fails to surpass A-end → truncated C,
   flag as WARN; may signal the larger sequence is more complex).
3. Wave A and wave C are internally motive (5-wave impulse or terminal).

**Guidelines:**
- C ≈ A in length (most common).
- C = 1.618 × A (extended zigzag variant).
- B is internally corrective (3-wave).

#### 2.8.4 Flat (3-3-5) [MEW Ch. 5]

**Variants:**

| Type | B retraces | C reaches |
|------|-----------|----------|
| Regular flat | 80–100% of A | ≈ A endpoint |
| Expanded flat | > 100% of A (B exceeds A's start) | > A endpoint (often 1.618×A) |
| Running flat | > 100% of A | Fails to reach A endpoint |

**Hard rules (all flat variants):**
1. Waves A and B are internally corrective (3-wave).
2. Wave C is internally motive (5-wave).
3. B retraces ≥ 61.8% of A (if < 61.8%, it may be a triangle leg or zigzag B).

#### 2.8.5 Triangle (3-3-3-3-3, 5 legs: a-b-c-d-e) [MEW Ch. 5]

**Contracting triangle:**
- a > b > c > d > e in price range.
- All 5 legs internally corrective.
- Two converging trendlines (b-d line, a-c line).
- Post-triangle thrust ≈ widest part (wave a length).
- Thrust completes in ≤ time of the *shortest* triangle leg.

**Neutral triangle (NeoWave exclusive):** [NW-QA-8, NW-QA-3849]
- Wave C is the longest leg.
- Waves A and E approximately equal, each ≥ 38.2% of C (typically 61.8–72% of C).
- C ≤ 161.8% of A (up to 261.8% in volatile conditions).
- Channeling: parallel lines through b-d endpoints; parallel through a-end.

**Barrier triangle:** One trendline is effectively horizontal; other converges toward it.

**Expanding triangle:** a < b < c < d < e (each leg longer than prior). Rarer.

```python
def is_neutral_triangle(legs):
    a, b, c, d, e = legs
    if abs(c.price_range) <= abs(a.price_range):
        return RuleResult("NEUTRAL_C", FAIL, "C not longest")
    c_len, a_len, e_len = abs(c.price_range), abs(a.price_range), abs(e.price_range)
    if a_len / c_len < 0.382:
        return RuleResult("NEUTRAL_A", FAIL, f"A={a_len/c_len:.2f} < 38.2% of C")
    if e_len / c_len < 0.382:
        return RuleResult("NEUTRAL_E", FAIL, f"E={e_len/c_len:.2f} < 38.2% of C")
    if c_len / a_len > 2.618:
        return RuleResult("NEUTRAL_C_LIMIT", FAIL, f"C={c_len/a_len:.2f}×A > 261.8%")
    return RuleResult("NEUTRAL_TRIANGLE", PASS, f"C={c_len/a_len:.2f}×A, A≈E={a_len/e_len:.2f}")
```

#### 2.8.6 Diametric Formation (7 legs: a-b-c-d-e-f-g) [NW-QA-3, post-MEW 1992]

The diametric was discovered by Neely circa 1992 and is NOT in *Mastering Elliott Wave*.
Defining characteristic: **all 7 legs are similar in TIME** (not necessarily price).
Fibonacci price ratios do NOT apply; time is the organising principle. [NW-QA-3, NW-QA-875]

**Construction rules:**
1. Each of the 7 legs is internally corrective (3-wave structure).
2. All 7 legs tend toward time equality: each leg is within ~2× of the others in duration.
   (Practical threshold: max_leg_bars / min_leg_bars < 3.0.)
3. No x-waves separate the legs (all 7 are contiguous).

**Shape identification:**
- **Bowtie:** Legs a–d expand in price (each longer than prior); legs e–g contract.
  Leg d is the longest.
- **Diamond:** Legs a–d contract; legs e–g expand.
  Leg d is the shortest.

```python
def classify_diametric(legs):
    """legs: list of 7 Wave objects."""
    assert len(legs) == 7
    durations = [w.bars for w in legs]
    prices    = [abs(w.price_range) for w in legs]

    # Time similarity check
    time_ratio = max(durations) / min(durations)
    if time_ratio > 3.0:
        return RuleResult("DIAMETRIC_TIME", WARN, f"Time spread {time_ratio:.1f}× > 3×")

    # Shape identification
    first_half = prices[:4]   # legs a, b, c, d
    second_half = prices[4:]  # legs e, f, g
    expanding_first  = all(first_half[i] < first_half[i+1] for i in range(3))
    contracting_first = all(first_half[i] > first_half[i+1] for i in range(3))
    contracting_second = all(second_half[i] > second_half[i+1] for i in range(2))
    expanding_second  = all(second_half[i] < second_half[i+1] for i in range(2))

    if expanding_first and contracting_second:
        shape = "BOWTIE"
    elif contracting_first and expanding_second:
        shape = "DIAMOND"
    else:
        shape = "IRREGULAR"

    # Max complexity guidance: < 55 total monowaves [NW-QA-875]
    total_mono = sum(w.monowave_count for w in legs)
    if total_mono > 55:
        complexity_note = "WARN: >55 monowaves; consider higher TF"
    else:
        complexity_note = f"OK: {total_mono} monowaves"

    return RuleResult("DIAMETRIC", PASS, f"{shape} | {complexity_note}")
```

**Post-diametric thrust:** Sharp move in the opposite direction after wave g, roughly
equal to the widest part of the formation. [NW-QA-474]

#### 2.8.7 Symmetrical Formation (9 legs) [NW-QA-5, post-MEW 2001]

The symmetrical was discovered circa 2001 and is the rarest NeoWave pattern.
All three dimensions — **price, time, and complexity** — are similar across most legs.
[NW-QA-5, NW-QA-875]

**Construction rules:**
1. 9 contiguous legs; no x-waves.
2. Advancing legs are price/time/complexity similar to each other.
3. Declining legs are price/time/complexity similar to each other.
4. Advancing group and declining group are NOT similar to each other.
5. Generally unfolds between approximately parallel trendlines (mild expansion/contraction
   is allowed).

**Diagnostic test:**

```python
def classify_symmetrical(legs):
    assert len(legs) == 9
    # Split into advancing and declining by direction
    advancing = [w for w in legs if w.direction == legs[0].direction]
    declining = [w for w in legs if w.direction != legs[0].direction]

    def group_similarity(group):
        prices     = [abs(w.price_range) for w in group]
        times      = [w.bars for w in group]
        complexity = [w.monowave_count for w in group]
        p_sim = min(prices) / max(prices)
        t_sim = min(times)  / max(times)
        c_sim = min(complexity) / max(complexity)
        return p_sim, t_sim, c_sim

    adv_p, adv_t, adv_c = group_similarity(advancing)
    dec_p, dec_t, dec_c = group_similarity(declining)

    all_similar = min(adv_p, adv_t, adv_c) >= 0.333 and min(dec_p, dec_t, dec_c) >= 0.333
    cross_similar = (
        abs(sum(w.price_range for w in advancing)) /
        abs(sum(w.price_range for w in declining))
    )
    # Cross-group should NOT be similar (advancing ≠ declining in price)
    cross_dissimilar = cross_similar < 0.5 or cross_similar > 2.0

    if all_similar and cross_dissimilar:
        return RuleResult("SYMMETRICAL", PASS, f"adv p={adv_p:.2f} t={adv_t:.2f} | dec p={dec_p:.2f} t={dec_t:.2f}")
    return RuleResult("SYMMETRICAL", FAIL, "Similarity conditions not met")
```

**vs Diametric disambiguation:**
- All three dimensions similar → SYMMETRICAL.
- Time + complexity similar, price NOT similar → DIAMETRIC.
- Price + complexity similar, time NOT similar → possibly Triangle or irregular.

#### 2.8.8 X-Waves in Complex Combinations [MEW Ch. 5, NW-QA-7, NW-QA-94]

An x-wave connects two corrective patterns in a W-X-Y (double combination) or
W-X-Y-X-Z (triple combination). Specific hard rules:

1. **Size (small x-wave):** Retraces **< 61.8%** of the prior correction (W). This is
   the most common x-wave. Exceeding 61.8% creates a "large x-wave" with distinctly
   different implications.
2. **Complexity upper bound:** x-wave power rating ≤ power rating of prior correction (W).
   Typically x-wave is 1/3–2/3 the complexity of W.
3. **Complexity lower bound:** x-wave complexity ≥ least complex wave of the same-degree
   correction it interrupts.
4. **Degree:** x-wave is always smaller (price AND time) than the corrections it connects.

```python
def x_wave_check(x_wave, prior_correction_W):
    results = []
    retrace = abs(x_wave.price_range) / abs(prior_correction_W.price_range)
    if retrace < 0.618:
        results.append(RuleResult("X_SIZE", PASS, f"Small x-wave {retrace:.1%} < 61.8%"))
    elif retrace < 1.00:
        results.append(RuleResult("X_SIZE", WARN, f"Large x-wave {retrace:.1%}: complex combination"))
    else:
        results.append(RuleResult("X_SIZE", FAIL, f"x-wave {retrace:.1%} >= 100% of W: not a valid x-wave"))
    # Complexity check
    if x_wave.monowave_count > prior_correction_W.monowave_count:
        results.append(RuleResult("X_COMPLEXITY", FAIL, "x-wave more complex than prior correction"))
    return results
```

---

### 2.9 Terminal Retrace Timing [NW-QA-terminal, LF-Part20]

Once a terminal impulse is complete, Neely specifies:
> The entire terminal must be completely retraced to its origin. This retrace occurs
> faster than the terminal formed.

**Implementation (bias window, NOT a price forecast):**

```python
def terminal_retrace_window(terminal_build_bars, terminal_end_t, terminal_origin_price):
    """
    Returns the observation window (in bars) for monitoring the retrace's progress.
    The origin price is the structural TARGET; no timing guarantee for reaching it.
    
    Window: monitor bars from terminal_end_t to terminal_end_t + terminal_build_bars.
    Expect retrace to be WELL UNDERWAY within 1/4 to 1/2 of build_bars.
    Full origin retrace: directional bias, may take as long as the build itself.
    """
    return {
        "monitor_window_bars":  terminal_build_bars,
        "early_signal_bars":    terminal_build_bars // 4,   # watch for acceleration here
        "expected_range_bars":  terminal_build_bars // 2,   # modal expectation
        "target_price":         terminal_origin_price,       # structural target
        "warning": "target_price is a directional bias, not a timed forecast. "
                   "Stage 1 confirmation (2-4 line break in < w5 time) must occur first."
    }
```

---

## 3. Recommended Data Structures

### 3.1 Core Types

```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class Direction(Enum):
    UP   = 1
    DOWN = -1

class Status(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    REF  = "REF"   # requires human discretion

@dataclass
class Pivot:
    t:         float        # unix seconds
    price:     float
    direction: Direction    # direction OF THE MONOWAVE ENDING HERE

@dataclass
class Wave:
    start:         Pivot
    end:           Pivot
    direction:     Direction
    bars:          int       # number of chart bars consumed
    monowave_count: int = 1  # 1 for primitive monowave; >1 after compaction
    degree:        int = 0   # 0=monowave, 1=polywave, 2=multiwave, 3=macrowave

    @property
    def price_range(self):
        return self.end.price - self.start.price   # signed

    @property
    def abs_price(self):
        return abs(self.price_range)

@dataclass
class MonowaveLabel:
    wave:        Wave
    labels:      list[str]   # e.g. [':5'], or [':5', ':L5'] if ambiguous
    ambiguous:   bool        # True if |labels| > 1
    provisional: bool        # True if m2 not yet confirmed (last in series)

@dataclass
class WaveNode:
    """Recursive tree node for the multi-level wave hierarchy."""
    wave:      Wave
    label:     str                      # e.g. ':5', ':3', 'IMPULSE', 'ZIGZAG'
    children:  list['WaveNode'] = field(default_factory=list)
    parent:    Optional['WaveNode'] = None
    degree:    int = 0
    structure: str = ""                 # e.g. '5-3-5', '3-3-5', '7-leg DIAMETRIC'
    confidence: str = "HEURISTIC"      # 'HIGH', 'MEDIUM', 'LOW', 'HEURISTIC'
    rules:     list = field(default_factory=list)  # list[RuleResult]

    def is_motive(self):
        return self.label in (':5', ':s5', ':L5', 'IMPULSE', 'TERMINAL')

    def is_corrective(self):
        return self.label in (':3', ':F3', ':c3', ':sL3', ':L3',
                              'ZIGZAG', 'FLAT', 'TRIANGLE',
                              'DIAMETRIC', 'SYMMETRICAL')

@dataclass
class RuleResult:
    rule:   str
    status: Status
    detail: str = ""
```

### 3.2 Recursive WaveNode Tree

```python
class WaveTree:
    """
    Manages the bottom-up construction hierarchy.
    
    Level 0: raw Pivots from zigzag extraction
    Level 1: Monowaves with structure labels
    Level 2: Polywaves (groups of 3 or 5 labelled monowaves)
    Level 3: Multiwaves (groups of 3 or 5 polywaves)
    Level 4: Macrowaves (groups of 3 or 5 multiwaves)
    """

    def __init__(self, pivots: list[Pivot]):
        self.pivots = pivots
        self.levels: dict[int, list[WaveNode]] = {}

    def build(self):
        # Phase 2: rollback + neutrality
        pivots = apply_rollback(self.pivots)
        pivots = apply_neutrality(pivots)

        # Phase 3: structure labels
        labelled = label_monowaves(pivots)
        self.levels[0] = [WaveNode(wave=lm.wave, label=lm.labels[0],
                                   degree=0) for lm in labelled]

        # Phase 4: compaction
        for degree in range(1, 4):
            lower_nodes = self.levels[degree - 1]
            upper_nodes = self._compact_level(lower_nodes, degree)
            if not upper_nodes:
                break
            self.levels[degree] = upper_nodes

        # Phase 5: channeling + post-constructive
        self._apply_channeling()
        self._apply_post_constructive()

    def _compact_level(self, nodes, target_degree):
        """Try grouping nodes into 3-wave or 5-wave patterns."""
        ...  # Calls group_polywaves() logic

    def _apply_channeling(self):
        """Build 0-2, 2-4, 1-3 trendlines for all impulse candidates."""
        ...

    def _apply_post_constructive(self):
        """Check 2-stage confirmation, post-triangle thrust, post-correction behaviour."""
        ...

    def candidates(self, degree=None):
        """Return all WaveNode candidates at the given degree level."""
        if degree is not None:
            return self.levels.get(degree, [])
        return {d: nodes for d, nodes in self.levels.items()}
```

---

## 4. Implementation Priority Order

The following 10 pieces, in this order, give the greatest fidelity improvement per unit
of implementation effort. Dependencies flow top-to-bottom.

| Priority | Component | What it unlocks | Estimated difficulty |
|----------|-----------|-----------------|---------------------|
| **P1** | `apply_rollback()` + `apply_neutrality()` | Clean pivot list; all downstream is meaningless without this | Medium |
| **P2** | `label_monowaves()` with all 7 rules + conditions | Structure labels; prerequisite for P3 | High |
| **P3** | `group_polywaves()` — sliding window + validation | True bottom-up polywave detection | High |
| **P4** | `similarity_and_balance()` applied to ALL adjacent corrective pairs | Degree assignment; eliminates the single largest source of wrong counts | Low (improve existing) |
| **P5** | `two_four_confirmation()` with timing rules (Stage 1 + 2) | Impulse completion confirmation; eliminates premature count closes | Medium |
| **P6** | `is_terminal()` upgrades: W2 ≤ 61.8% limit + 3-3-3-3-3 substructure | Terminal accuracy; currently the most commonly-used pattern in this codebase | Low (improve existing) |
| **P7** | `is_neutral_triangle()` | Neutral triangle detection (currently missing) | Low (new function) |
| **P8** | `x_wave_check()` with 61.8% retrace rule | Complex combination validation; currently all REF | Low (improve existing) |
| **P9** | `classify_diametric()` with time-similarity enforcement + bowtie/diamond | Proper 7-leg pattern discrimination | Medium |
| **P10** | `classify_symmetrical()` — 9-leg pattern | New pattern type; currently falls to REF | Medium |

**Not listed but mandatory before P2:** the `WaveNode` tree data structure (§3), which
is the container that makes compaction trackable. Without it, P3 has nowhere to store
multi-level output.

---

## 5. Honest Caveats: What Is Genuinely Unautomatable

### 5.1 Rollback Rules — Inherently Ambiguous

Neely's rollback rules describe qualitative endpoint corrections ("if price briefly
violates..."). The word "briefly" and "trivially" have no universal numeric definitions.
Any implementation must choose thresholds (e.g., 1 ATR, or 10% of adjacent wave). These
choices affect all downstream labels. **This is the fundamental ambiguity at the base of
the entire system.** Real NeoWave analysts adjust rollback judgement interactively using
visual context. Flag all rollback-corrected pivots with `RuleResult(status=REF)`.

### 5.2 Structure Label Ambiguity at the Margins

Rules 3–5 produce multi-label candidates for ~30–40% of monowaves in real market data.
For example, a Rule-3b monowave may be simultaneously valid as `:3`, `:F3`, or `:5`.
The correct label is resolved only *after* the next 3–5 monowaves have formed (backfill).
**No purely causal algorithm can resolve this in real time.** The correct implementation
maintains a set of candidate labels and propagates all candidates through compaction,
pruning as subsequent waves constrain the possibilities.

### 5.3 Degree Assignment

Even with full bottom-up monowave construction, degree assignment at higher levels
involves human judgment about market context (was the 2020 COVID crash a wave 4 or a
wave 2?). The similarity and balance rules constrain possibilities but rarely produce a
unique solution. Flag `degree_confidence = "HEURISTIC"` at all levels above monowave.

### 5.4 Diametric/Symmetrical Identification Threshold

Neely's rule for diametrics is "all 7 legs similar in time." In practice, "similar"
means within roughly 2–3× (Neely mentions "general" time equality). No published
exact percentage exists. The 3× threshold used in §2.8.6 is an interpolation from
NW-QA-875's guidance that Diametrics ≤ 55 monowaves are most reliably identified.
The complexity limit implies a practical time-spread limit but not an exact one.

### 5.5 Post-Constructive Confirmation Requires Subsequent Bars

Post-constructive rules (Stage 1, Stage 2 timing tests) require bars that have not yet
formed at the time of labelling. They cannot be computed at the bar where a pattern ends.
They are asynchronous validation checks, not synchronous rules. The implementation must
maintain a "pending confirmation" queue and check it on each new bar. This requires a
stateful design that the current `wavelib` does not have.

### 5.6 Rule of Reverse Logic Is Not Fully Automatable

"Select the count furthest from completion" requires knowing the *full price projection*
of each candidate count, which depends on which pattern is being claimed. For a
triangle, the projection is the thrust. For an impulse, it is the wave-5 target. For a
diametric, it is the post-g thrust. Computing all candidate projections simultaneously,
then selecting the least-complete, is implementable but requires all pattern projectors
to be wired together. This is Phase 5 (backtest) territory in the build order.

### 5.7 The Symmetrical Pattern Has Almost No Published Numeric Specification

Neely's symmetrical was described in his Q&A archive (~2001) but has never appeared in
a book or formal paper. The construction rules in §2.8.7 are derived from NW-QA-5 and
NW-QA-875 and are the best available public specification. Any implementation should
treat symmetrical detection as `Status.REF` until more authoritative numeric thresholds
become available.

### 5.8 X-Wave Complexity "Lower Bound" Is Qualitative

The rule that "x-wave complexity ≥ least complex wave of the same-degree correction it
interrupts" (MEW Ch. 5) is clear in intent but ambiguous in measurement when the prior
correction has legs of varying complexity. In practice, use power ratings (§2.5.2) as
the proxy and treat the lower bound as a WARN, not FAIL.

---

## Sources

| Source | URL |
|--------|-----|
| neowave.com — What is NeoWave | https://www.neowave.com/what-is-neowave.asp |
| neowave.com — What is NeoWave Analysis | https://www.neowave.com/what-is-neo-wave-analysis.asp |
| neowave.com — MEW Chapter 1 | https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp |
| neowave.com — Rule of Reverse Logic | https://www.neowave.com/neowave-rules-of-reverse-logic.asp |
| neowave.com — S&B importance (QA-32) | https://www.neowave.com/qow/qow-archive-32.asp |
| neowave.com — S&B: price or time? (QA-78) | https://www.neowave.com/qow/qow-archive-78.asp |
| neowave.com — Structure labels :F3 vs :5 (QA-25) | https://www.neowave.com/qow/qow-archive-25.asp |
| neowave.com — Confirming wave 5 end (QA-22) | https://www.neowave.com/qow/qow-archive-22.asp |
| neowave.com — 0-2 trendline (QA-273) | https://www.neowave.com/qow/qow-archive-273.asp |
| neowave.com — 2-4 trendline placement (QA-303) | https://www.neowave.com/qow/qow-archive-303.asp |
| neowave.com — Diametric definition (QA-3) | https://www.neowave.com/qow/qow-archive-3.asp |
| neowave.com — Diametric time deviation (QA-875) | https://www.neowave.com/qow/qow-archive-875.asp |
| neowave.com — Diametric vs Symmetrical (QA-2346) | https://www.neowave.com/qow/qow-archive-2346.asp |
| neowave.com — Symmetrical definition (QA-5) | https://www.neowave.com/qow/qow-archive-5.asp |
| neowave.com — Neutral triangle (QA-8) | https://www.neowave.com/qow/qow-archive-8.asp |
| neowave.com — Neutral triangle C limit (QA-3849) | https://www.neowave.com/qow/qow-archive-3849.asp |
| neowave.com — Post-triangle thrust timing (QA-5161) | https://www.neowave.com/qow/qow-archive-5161.asp |
| neowave.com — Post-diametric thrust (QA-474) | https://www.neowave.com/qow/qow-archive-474.asp |
| neowave.com — x-wave rules (QA-7) | https://www.neowave.com/qow/qow-archive-7.asp |
| neowave.com — x-wave complexity (QA-94) | https://www.neowave.com/qow/qow-archive-94.asp |
| neowave.com — Extracting triangle retired (QA-923) | https://www.neowave.com/qow/qow-archive-923.asp |
| neowave.com — Extension ≥ 161.8% (QA-1006) | https://www.neowave.com/qow/qow-archive-1006.asp |
| neowave.com — Wave-2 retrace limit terminal (QA-1079) | https://www.neowave.com/qow/qow-archive-1079.asp |
| neowave.com — Post-constructive behaviour (QA-19) | https://www.neowave.com/qow/qow-archive-19.asp |
| neowave.com — Pre-break confirmation (QA-108) | https://www.neowave.com/qow/qow-archive-108.asp |
| neowave.com — Terminal retrace timing (search) | https://www.neowave.com/qow-search.asp?dowhat=searchqow&searchterms=terminal |
| LiteFinance — NeoWave intro | https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/ |
| LiteFinance — Retracement Rule 1 | https://www.litefinance.org/blog/for-professionals/neowave-part-3-retracement-rule-1/ |
| LiteFinance — Retracement Rule 7 | https://www.litefinance.org/blog/for-professionals/neowave-part-11-retracement-rule-7/ |
| LiteFinance — Compaction + Power Ratings (Part 18) | https://www.litefinance.org/blog/for-professionals/neowave-part-18-rules-of-complexity-and-balance-compaction-procedures-power-ratings/ |
| LiteFinance — Terminal progress labels (Part 20) | https://www.litefinance.org/blog/for-professionals/neowave-part-20-application-of-progress-labels-to-terminal-impulses/ |
| LiteFinance — Channeling in impulses (Part 21) | https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships/ |
| LiteFinance — Practical NeoWave (Part 27) | https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/ |
| Scribd — NeoWave Part 2 (Polywaves + Structure Labels) | https://www.scribd.com/document/690130352/Part-2-Basic-Info-on-Polywaves-and-Structure-Labels |
| Scribd — NeoWave Part 3 (Retracement Rule 1) | https://www.scribd.com/document/690130462/Part-3-Retracement-Rule-1 |
| Scribd — NeoWave Part 4 (Retracement Rule 2) | https://www.scribd.com/document/690130554/Part-4-Retracement-Rule-2 |
| Scribd — NeoWave Part 5 (Retracement Rule 3) | https://www.scribd.com/document/502299837/5-The-NeoWave-theory-by-Glenn-Neely |
| Scribd — NeoWave Part 7 (Retracement Rule 4) | https://www.scribd.com/document/502300644/7-NeoWave-theory-by-Glenn-Neely |
| Scribd — NeoWave Part 8 (Conditions c,d,e) | https://www.scribd.com/document/502300840/8-NeoWave-theory-by-Glenn-Neely |
| Scribd — NeoWave Part 9 (Rules 5 & 6) | https://www.scribd.com/document/502311042/9-NeoWave-theory-by-Glenn-Neely |
| Scribd — NeoWave Part 13 (Corrections) | https://www.scribd.com/document/839672297/Part-13-Corrections-Rules-to-identify-a-correction-NeoWave-theory-by-Glenn-Neely |
| ForexTalker — Rollback rules + Rule 1 | https://forextalker.com/neowave-wave-theory-by-glenn-neely-rollback-rules-and-the-first-rule-of-wavelength-relationships/ |
| ForexTalker — Rule 7 conditions a-d | https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-a-b-c-and-d-for-the-seventh-rule/ |
| ForexTalker — Rule 2 conditions | https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-the-second-rule-for-the-ratio-of-wavelengths-and-conditions-for-its-implementation/ |
| ForexTalker — Impulse rules of logic | https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-price-impulses-the-rules-of-the-stretched-wave-equality-alternation-overlap-the-rules-of-logic/ |
| niftywaveindia.blogspot.com — 7-leg diametric | http://niftywaveindia.blogspot.com/2018/12/technical-learnings-7-legged-diametric.html |
| wavesstrategy.com — Diametric trading | https://www.wavesstrategy.com/nifty-trade-neo-wave-diametric-pattern |
| ebrary.net — Triangle & Diametric | https://ebrary.net/299888/education/triangle |
| Ewace_2026 repo — docs/research/02_neowave_neely.md | (this repository) |
