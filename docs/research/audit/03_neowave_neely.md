# 03 — NeoWave (Glenn Neely): Theory, Code Audit, and Mistake Table

**Status:** audit — 2026-06-09
**Auditor:** agent research session (Ewace_2026)
**Scope:** monowave construction, structure-label assignment (:5 / :3 / :F3 etc.),
Rule of Similarity & Balance, retracement rules 1–7, polywave grouping, and the
concrete causes of the observed behaviour (`:3` / `:sL3` dominance, S&B WARN,
NeoWave / Elliott label disagreement).

Cross-references: `docs/research/02_neowave_neely.md` (theory baseline),
`docs/research/deep/05_neowave_full_algorithm.md` (implementable spec),
`reports/WAVE_COUNTS_AVGO_MRVL.md` (observed output).

---

## 1. Theory (cited)

### 1.1 The Five Phases of NeoWave Construction

Neely's system is strictly bottom-up and must be executed in an invariant order
[MEW Ch. 1–4; LiteFinance intro; neowave.com — what is NeoWave]:

```
Phase 1  Chart standardisation  — uniform bar resolution; arithmetic scale
Phase 2  Monowave extraction    — pivots + rollback corrections + neutrality
Phase 3  Structure labelling    — 7 retracement rules → labels per monowave
Phase 4  Pattern construction   — sliding-window grouping into polywaves; compact upward
Phase 5  Confirmation logic     — channeling + post-constructive rules
```

Skipping or reordering any phase is not a permissible simplification; it produces
structurally mislabeled counts that cannot be repaired at a later stage.

### 1.2 Structure Label Glossary

[MEW Ch. 3; Scribd — NeoWave Part 2; neowave.com QA-25]

| Label | Mnemonic | Meaning |
|-------|----------|---------|
| `:5` | Five | Motive — part of a 5-wave impulse |
| `:3` | Three | Corrective — any standard 3-segment correction |
| `:F3` | First 3 | Corrective — first segment of a flat (B-wave of flat) |
| `:c3` | C-Three | Corrective — C-wave of a correction; completes a correction |
| `:L5` | Last 5 | Motive — final wave of a motive sequence (wave-5 position) |
| `:s5` | Strong 5 | Motive — strongest (extended) wave; wave-3 extension |
| `:sL3` | Strong-Last 3 | Corrective — powerful C-wave, often with throw-over; ends a correction |
| `:L3` | Last 3 | Corrective — last segment of complex correction or triangle |

**Key behavioural criterion for `:5` vs `:3`** [MEW Ch. 3; neowave.com QA-25]:
- `:5` — price covers *more distance per time unit* than the wave it is embedded in;
  the wave it is retraced by is fully retraced in *less* time than the wave itself.
- `:3` — price covers *less distance per time unit*; retracement is slow and/or the
  wave is internally complex on a lower timeframe.

### 1.3 The Seven Retracement Rules: Exact Table

For monowave m1, compute:

```
r21 = abs(m2.length) / abs(m1.length)    [next wave vs current]
r01 = abs(m0.length) / abs(m1.length)    [prior wave vs current]
overlap = m2's endpoint reaches into m0's price territory (Rule 3 vs 4 splitter)
```

[MEW Ch. 3; Scribd Parts 3–9; ForexTalker rollback+rules; LiteFinance Parts 3–11]

| Rule | r21 range | r01 sub-conditions | Primary candidate labels for m1 |
|------|-----------|-------------------|----------------------------------|
| 1 | r21 < 0.382 | r01 < 1.00 | `:s5` |
| | | 1.00 ≤ r01 ≤ 1.618 | `:s5` or `:5` |
| | | r01 > 1.618 | `:5` |
| 2 | 0.382 ≤ r21 < 0.618 | r01 < 0.618 | `:5` |
| | | 0.618 ≤ r01 < 1.00 | `:5` |
| | | 1.00 ≤ r01 ≤ 1.618 | `:5` or `:L5` |
| | | r01 > 1.618 | `:L5` |
| 3 | 0.618 ≤ r21 < 1.00, **no overlap** | r01 < 0.618 | `:3` or `:F3` |
| | | 0.618 ≤ r01 < 1.00 | `:3`, `:F3`, or `:5` (flag) |
| | | 1.00 ≤ r01 ≤ 1.618 | `:c3` or `:sL3` |
| | | r01 > 1.618 | `:c3` |
| 4 | 0.618 ≤ r21 < 1.00, **with overlap** | r01 < 0.618 | `:5` or `:c3` (check m3) |
| | | 0.618 ≤ r01 < 1.00 | `:c3` |
| | | 1.00 ≤ r01 ≤ 1.618 | `:L5` or `:5` |
| | | r01 > 1.618 | `:L5`, `:s5`, or `:sL3` |
| 5 | 1.00 ≤ r21 < 1.618 | r01 < 1.00 | `:3` or `:c3` |
| | | 1.00 ≤ r01 < 1.618 | `:3`, `:c3`, or `:F3` |
| | | r01 ≥ 1.618 | `:c3` or `:sL3` |
| 6 | 1.618 ≤ r21 < 2.618 | r01 < 1.00 | `:c3` |
| | | r01 ≥ 1.00 | `:c3` or `:F3` |
| 7 | r21 ≥ 2.618 | r01 < 1.00 | `:c3` or `x:c3` |
| | | 1.00 ≤ r01 < 2.618 | `:3` or `x:c3` |
| | | r01 ≥ 2.618 | `x:c3` (condition d — extreme x-wave) |

**Critical sub-rule within Rule 2** [ForexTalker — Rule 2 conditions]:
Rule 2 candidates should also check **m3**: if m3 > m2 and m3 moves in m1's direction,
`:5` is strongly preferred over `:L5`. If m3 ≤ m2 or m3 subdivides into 3 sub-moves,
lean toward `:L5`.

**Critical disambiguation inside Rule 3** [Scribd Part 5]:
`:F3` (first leg of a flat) requires that m3 ≈ m1 in length (within 40%). If m3 does
not approximately equal m1, `:F3` should not be assigned — default to `:3`.

**The Rule-3 / Rule-4 split** [Scribd Part 7]:
Rules 3 and 4 share the 0.618–1.00 r21 range. The separator is whether m2's endpoint
*enters m0's price territory* (overlap = True → Rule 4). Without this check, the
61.8–100% band is systematically mis-routed to Rule 3, which biases labels corrective.

### 1.4 Rule of Similarity & Balance

[MEW Ch. 4; neowave.com QA-32, QA-78; LiteFinance Part 18]

For any two adjacent waves at the **same degree**:

- **Price similarity:** smaller / larger ≥ 1/3 (band [1/3, 3×]).
- **Time similarity:** shorter / longer ≥ 1/3 (band [1/3, 3×]).
- **Complexity (tertiary):** fewer monowaves / more monowaves ≥ 1/3.

At least one of price OR time must be satisfied. If **both** are violated, the waves are
definitively different degrees and the count must be revised, or a hidden x-wave exists.
S&B is applied to *all adjacent corrective pairs at every pattern level* — not just
wave 2 vs wave 4 in a single impulse.

### 1.5 Rule of Proportion

[MEW Ch. 4; neowave.com QA-1006]

No sub-wave should exceed the size of its parent wave unless an extension is underway.
In a NeoWave **trending impulse**, the extended wave **must be ≥ 161.8%** of the
next-longest motive wave. This is a **hard rule** in NeoWave — if the ratio is < 161.8%,
there is no extension (not a WARN; structural implication is different).

### 1.6 Rollback Rules and Neutrality

[MEW Ch. 2; ForexTalker — rollback rules]

Three rollback situations (R1 near-miss; R2 one-bar spike; R3 flat cluster) must be
resolved on the pivot list *before* any structure labelling occurs. Rollback is not an
optional cleaning step — mislabeled endpoints contaminate every downstream ratio.

The Rule of Neutrality absorbs any monowave shorter than ~10% of its neighbours into
the adjacent larger monowave before labelling.

### 1.7 Polywave Compaction and Power Ratings

[MEW Ch. 4; LiteFinance Part 18; Scribd Part 2]

| Structure | Power rating |
|-----------|-------------|
| Monowave | 1 |
| 3- or 5-monowave polywave | 2 |
| 3- or 5-polywave multiwave | 3 |
| 3- or 5-multiwave macrowave | 4 |

Complexity equality (within 3×) is used in S&B tertiary checks, x-wave bounds, and
diametric time-similarity tests.

---

## 2. What the Code Does Now

### 2.1 `retracement_logic()` — rules.py:427, toolkit.py:314

Both implementations use a **3-band mapping**:

```python
# rules.py:427-437
if retr < 0.382:
    m = "prior=extended 3rd; you're in a 4th"
elif retr < 0.618:
    m = "prior=1st/5th; current=2nd/4th (normal)"
elif retr <= 1.0:
    m = "deep: prior=a-wave/1st; current=2nd/B/X (sharp)"
else:
    m = ">100%: NOT a retracement -> trend change / larger structure"
```

This always returns `Status.REF`. The function is display-only; it does **not** assign
structure labels to individual monowaves.

### 2.2 `monowave_candidates()` — rules.py:794–822

This is the core label-assignment function, called by `label_monowaves()`. It implements
a **5-band mapping**:

```python
# rules.py:808-819
if r < 0.382:                       # Rule 1
    cands = [":5"]
elif r < 0.618:                     # Rule 2
    cands = [":5", ":3"]
elif r <= 1.0:                      # Rule 3 / Rule 4
    cands = [":3", ":c3"] if overlaps_m0 else [":3", ":5"]
elif r <= 1.618:                    # Rule 5
    cands = [":3", ":L5"]
elif r <= 2.618:                    # Rule 6
    cands = [":3", ":sL3"]
else:                              # Rule 7
    cands = [":sL3", ":x"]
if m0r > 2.618 and ":sL3" not in cands:     # condition d only
    cands.append(":sL3")
```

The function returns a list; `label_monowaves()` (rules.py:788) always picks **index 0**
as the "primary candidate":

```python
# rules.py:788
core = monowave_candidates(m0, m1, m2)[0]
```

### 2.3 `similarity_and_balance()` — rules.py:409, toolkit.py:297

Both versions correctly implement the [1/3, 3×] band for **both** price and time.
However, application coverage differs:

- **`validate_impulse()`** (rules.py:853): applies S&B only to `w[1]` vs `w[3]`
  (wave 2 vs wave 4).
- **`validate_correction()`** (rules.py:867): for 3-wave corrections checks A vs C;
  for 5-leg corrections (triangle) checks all 4 adjacent pairs. This is closer to Neely.
- **`group_polywaves()`** (rules.py:825): for 3-leg groups checks only A vs C;
  for 5-leg impulse groups does NOT apply S&B at all (only `elliott_hard_rules`).

### 2.4 `label_monowaves()` — rules.py:762–791

Calls `monowave_candidates()` for each interior monowave (those with full m0/m2
context), picks the first candidate unconditionally, appends the retracement-rule
number, and returns the labelled list. Edge monowaves (first and last) get `:?`.

### 2.5 `group_polywaves()` — rules.py:825–847

Slides windows of size 3 and 5 over labelled monowaves. For size 3 calls
`classify_correction()` and checks S&B on legs 0 vs 2. For size 5 runs
`elliott_hard_rules()`. Does **not** use the structure labels produced by
`label_monowaves()` for grouping decisions — the labels are stored in the tuple
but not consulted.

### 2.6 `rule_of_proportion()` — rules.py:420–424

Always returns `Status.WARN` if child > parent, `Status.PASS` otherwise. Does not check
the 161.8% extension hard rule.

### 2.7 `is_terminal()` — rules.py:585–606

Checks wave-4/wave-1 overlap (correct) and contracting shape (correct). Reports wave-2
retracement and flags "> 61.8% atypical" but the rule-check status is `Status.PASS`
regardless of the wave-2 size — only the detail string differs:

```python
# rules.py:601
limit_note = "" if w2_retr <= 0.618 + 1e-9 else " (>61.8% - atypical for a terminal)"
return RuleResult("terminal impulsion", Status.PASS, ...)
```

### 2.8 Observed Output — `reports/WAVE_COUNTS_AVGO_MRVL.md`

AVGO 1W full-range (21 monowaves): 7 motive (`:5`) vs 12 corrective (`:3`, `:sL3`).
AVGO 4H full-range (24 monowaves): 6 motive (`:5`) vs 16 corrective.
MRVL 1W full-range (98 monowaves): 26 motive vs 70 corrective.

S&B WARNs appear on:
- AVGO 4H (time out of band 3.81×)
- AVGO 1H (price out of band 0.28×)
- MRVL 1W (price out of band 0.22×)

---

## 3. Mistake Table

| # | Neely requirement | Code behaviour | Location | Verdict | Severity | Effect on the count |
|---|-------------------|----------------|----------|---------|----------|---------------------|
| **M1** | Rule 2 (r21 0.382–0.618): primary label is `:5` unconditionally (motive) for all r01 sub-conditions up to the `:L5` boundary at r01 > 1.618 | `monowave_candidates()` returns `[":5", ":3"]` — `:3` is the second candidate; `label_monowaves()` picks index 0 (`:5`) which is correct. BUT: the caller in the wave-report pipeline picks the first candidate without ever checking r01 sub-conditions that would resolve `:5` to `:L5` when r01 > 1.618. For r01 values in the `:L5` zone, the label stays `:5` and is never promoted to `:L5`. | `rules.py:810–812`, `rules.py:788` | PARTIAL — primary label is correct for Rules 1 and 2; sub-condition disambiguation (`:L5` vs `:5`) is missing | MEDIUM | Motive waves near the end of a sequence are mislabeled `:5` instead of `:L5`; polywave grouper cannot distinguish "normal first wave" from "final motive wave," so polywave boundaries are wrong |
| **M2** | Rule 3 (r21 0.618–1.00, NO overlap): when r01 < 0.618, primary label is `:3` or `:F3` (corrective). When r01 between 0.618–1.00, label is AMBIGUOUS between `:3`, `:F3`, and `:5` (must check m3). This ambiguity must be preserved in the candidate set. | `monowave_candidates()` for no-overlap Rule 3 returns `[":3", ":5"]`. This **drops** `:F3` (first leg of a flat) entirely from the candidate set, regardless of r01 sub-conditions. Additionally, the overlap boolean `overlaps_m0` is computed as `m0lo <= m2.end.price <= m0hi` (rules.py:807) which tests whether m2.end is **inside** m0's range — Neely's Rule-4 overlap is whether m2.end has *crossed past* m0.start in the opposite direction from m1, not whether it falls within m0's band. | `rules.py:806–813` | WRONG — both the candidate set (`:F3` missing) and the overlap test (wrong direction) are wrong | HIGH | `:F3` is the essential corrective qualifier that marks "first leg of a flat." Its absence causes every flat B-wave to be labelled `:3` instead of `:F3`, which propagates to a flat having two `:3` legs at the same level. This inflates the corrective count and is the primary reason flat corrections are not identified bottom-up. The wrong overlap test causes mislabeled Rule-3 vs Rule-4 routing on a non-trivial subset of monowaves. |
| **M3** | Rule 5 (r21 1.00–1.618): m2 has exceeded m1 in the opposite direction. The primary label for m1 is `:3` or `:c3` (corrective) when r01 < 1.00. The key diagnostic is that m2 > m1 in the **opposite** direction — this confirms m1 ended a corrective sequence. `label_monowaves()` must select this label because it will be the *leading* candidate (index 0). | `monowave_candidates()` Rule-5 returns `[":3", ":L5"]` — `:L5` is listed as a second candidate for all r01 values, but Neely's Rule-5 table specifies `:L5` only when r01 ≥ 1.618 (condition c). For r01 < 1.00 the label should be `:3` or `:c3`, not `:3` or `:L5`. The `:L5` candidate in the Rule-5 band is incorrect for the most common r01 range (< 1.00). | `rules.py:814–815` | WRONG — `:L5` is offered as a Rule-5 candidate when it should not be for r01 < 1.00 | HIGH | `:L5` in Rule-5 territory is occasionally picked by callers that rank candidates differently. More importantly, `:c3` (C-wave of a correction — the label that *closes* a corrective sequence) is entirely absent from the Rule-5 candidate set, so the engine never identifies the end of an A-B-C pattern at the monowave level. Flat and zigzag C-waves are always labelled `:3` rather than `:c3`, making it impossible for the polywave grouper to recognise where corrections end. |
| **M4** | Rule 6 (r21 1.618–2.618): m2 is much larger than m1. Both r01 sub-conditions assign `:c3` as primary, with `:F3` possible when r01 ≥ 1.00. `:sL3` is **not** a Neely primary for Rule 6. | `monowave_candidates()` Rule-6 returns `[":3", ":sL3"]`. `:sL3` (Strong-Last 3 — powerful C-wave with throw-over) should appear in Rule 6 only when r01 ≥ 1.618 and specific internal characteristics of m1 and m2 are present. The code offers `:sL3` for all Rule-6 cases, while the correct primary is `:c3`. | `rules.py:816–817` | WRONG — incorrect primary and secondary labels for Rule 6 | MEDIUM | Every large counter-swing (m2 > 1.618× m1) gets labelled `:sL3` as its secondary candidate instead of `:c3`. Since the pipeline picks index 0 (`:3`), primary labelling is accidentally correct for Rule 6 — but the presence of `:sL3` in the candidate set can mislead any caller that inspects the full candidate list, and `:c3` is still missing. |
| **M5** | Rule 4 overlap test: m2 reaches into m0's price territory means m2.end has **crossed the starting price of m0** in the counter-m1 direction (e.g., in an upward m1, m2's endpoint goes below m0's start). This is a directional crossing, not a price-band containment. | The overlap test (`rules.py:806–807`) computes `m0lo <= m2.end.price <= m0hi` — containment within m0's high–low band. A move that overshoots m0.start but stays within m0's range (between m0.start and m0.end) is NOT an overlap in Neely's sense, but the code will flag it as one. Conversely, a move that crosses well past m0.start but falls outside the narrowly-computed `m0lo/m0hi` box (if m0 had internal gap or unusual structure) may be missed. | `rules.py:806–807` | WRONG — the overlap check is containment within m0's band, not directional crossing past m0.start | MEDIUM | Miscode of Rule 3 vs Rule 4 routing. Rule 4 (overlap) favours `:c3` and `:L5`; Rule 3 (no overlap) favours `:3` and `:5`. Mis-routing in the high-frequency 0.618–1.00 band causes systematic over-assignment of `:c3` when there is no true overlap, and under-assignment when there is. |
| **M6** | `label_monowaves()` always selects the first candidate from `monowave_candidates()`. Neely's algorithm requires preserving ALL candidates and resolving ambiguity using (a) the m3 check, (b) r01 sub-condition, and (c) backfill from subsequent monowaves. | `label_monowaves()` (rules.py:788): `core = monowave_candidates(m0, m1, m2)[0]`. No m3 is passed; r01 sub-conditions are not used to narrow the candidate set; ambiguous cases (Rule-3b: r01 0.618–1.00) are silently resolved to the first list element. | `rules.py:788–789` | INCOMPLETE — ambiguity collapse is premature and loses genuine label uncertainty | HIGH | For roughly 30–40% of monowaves (Rules 3b, 4a, 4d, 5b), the first candidate is not definitively correct without the m3 check. Premature selection biases corrective (`:3` or `:c3` is often index 0). This is the primary mechanical cause of the observed `:3`/`:sL3` dominance in the wave count output. |
| **M7** | S&B must be applied to ALL adjacent corrective pairs at every pattern level — including within corrections (A vs B vs C in a flat, legs of a triangle), and between adjacent motive sub-waves when checking degree consistency. | `validate_impulse()` (rules.py:862) applies S&B only to `w[1]` vs `w[3]` (wave 2 vs wave 4). `group_polywaves()` (rules.py:841) for 5-wave impulse groups does not apply S&B at all — only `elliott_hard_rules()` is called. The 3-wave group path does check A vs C, which is correct for one pair. | `rules.py:862`, `rules.py:843–846` | INCOMPLETE — S&B coverage is too narrow | MEDIUM | Degree misassignment goes undetected. A 5-wave sequence where waves 1 and 3 are 10× different in price passes through the polywave grouper unchallenged. The S&B WARNs in the report output (AVGO 4H 3.81×, AVGO 1H 0.28×, MRVL 1W 0.22×) are detectable but the engine does not use them to reject or flag those polywave candidates. |
| **M8** | `rule_of_proportion()` must FAIL (not WARN) when a wave claims to be extended but is < 161.8% of the next-longest motive wave. In NeoWave the 161.8% extension rule is hard, not a guideline. | `rule_of_proportion()` (rules.py:420–424) always returns `Status.WARN` when child > parent, never `Status.FAIL`. `elliott_guidelines()` (rules.py:166–175) also returns only `Status.WARN` for extension ratios < 1.618. | `rules.py:420–424`, `rules.py:166–175` | WRONG severity — WARN where NeoWave requires FAIL for a claimed trending impulse | LOW | A trending impulse that claims wave 3 is "extended" at only 1.4× wave 1 passes as valid. In Neely's framework this means there is NO extension (different structural implication — the impulse may actually be a terminal or have a non-extension structure). The FAIL gate would reject ~20% of false "extended" impulse claims. |
| **M9** | `is_terminal()`: wave-2 retracement > 61.8% of wave-1 is a **FAIL** (hard limit in terminals; neowave.com QA-1079). | `is_terminal()` (rules.py:601–606): the wave-2 limit violation appends "(>61.8% - atypical for a terminal)" to the detail string but the overall status is `Status.PASS`. `terminal_rules()` (rules.py:625–627) upgrades this to `Status.WARN` but not `Status.FAIL`. | `rules.py:601–606`, `rules.py:625–627` | WRONG — WARN/note where Neely requires FAIL | LOW-MEDIUM | A terminal with wave-2 retracing 80–90% of wave-1 passes as valid. This violates a distinguishing NeoWave hard rule (in a trending impulse, wave-2 may go to 99.9%; in a terminal, hard limit is 61.8%). The rule exists precisely to prevent terminals from being confused with trending impulses. |
| **M10** | Polywave grouper must consult the **structure labels** assigned by `label_monowaves()` to decide whether groups of 3 and 5 are structurally valid. Specifically: a 5-wave impulse should have motive labels (`:5`/`:s5`/`:L5`) on waves 1, 3, 5 and corrective labels (`:3`/`:F3`/`:c3`) on waves 2, 4. A 3-wave correction should have matching types on A and C. | `group_polywaves()` (rules.py:825–847) stores the structure label from `label_monowaves()` as a tuple element but **never reads it** when deciding whether a group is valid. The grouper uses `classify_correction()` and `elliott_hard_rules()` on raw `Wave` objects only. The entire point of the Phase 3 label assignment — to make Phase 4 structurally constrained — is bypassed. | `rules.py:825–847` | MISSING — labels exist in the tuple but are not used | HIGH | The bottom-up NeoWave discipline is entirely broken. Any 5 consecutive waves that pass the three Elliott hard rules become a polywave candidate regardless of whether their individual labels make structural sense. This produces polywave candidates that Neely would reject at Phase 3, inflating candidates and producing incorrect degree assignments. |

---

## 4. Concrete Fixes (function-level, implementable)

### Fix 1 — `monowave_candidates()`: correct Rule 3/4 overlap test

**File:** `rules.py:806–807`

**Current:**
```python
m0lo, m0hi = min(m0.start.price, m0.end.price), max(m0.start.price, m0.end.price)
overlaps_m0 = m0lo <= m2.end.price <= m0hi
```

**Required:** overlap means m2's endpoint has crossed *past* m0.start in the direction
opposite to m1. For an upward m1, this means m2 ends BELOW m0.start.price (m2 went
below where m0 started). For a downward m1, m2 ends ABOVE m0.start.price.

```python
if m1.up:
    overlaps_m0 = m2.end.price < m0.start.price   # m2 crossed below m0's origin
else:
    overlaps_m0 = m2.end.price > m0.start.price   # m2 crossed above m0's origin
```

### Fix 2 — `monowave_candidates()`: complete the candidate sets per rule

**File:** `rules.py:808–822`

Replace the 5-band table with the full 7-rule table from §1.3, passing r01 as a
parameter and using it for sub-condition routing. Minimum changes:

1. **Rule 2:** add r01-based routing to separate `:5` from `:L5`. When r01 > 1.618,
   primary becomes `:L5`, not `:5`:
   ```python
   elif r < 0.618:  # Rule 2
       if r01 > 1.618:
           cands = [":L5", ":5"]
       else:
           cands = [":5", ":L5"]
   ```

2. **Rule 3 (no overlap):** add `:F3` to the candidate set:
   ```python
   else:  # no-overlap Rule 3
       if r01 < 0.618:
           cands = [":3", ":F3"]
       elif r01 < 1.0:
           cands = [":3", ":F3", ":5"]   # flag ambiguity (Rule 3b)
       elif r01 <= 1.618:
           cands = [":c3", ":sL3"]
       else:
           cands = [":c3"]
   ```

3. **Rule 5:** replace `:L5` with `:c3` as the second candidate for r01 < 1.618:
   ```python
   elif r <= 1.618:  # Rule 5
       if r01 >= 1.618:
           cands = [":c3", ":sL3"]
       else:
           cands = [":3", ":c3"]   # NOT :L5
   ```

4. **Rule 6:** add `:F3` and `:c3` properly:
   ```python
   elif r <= 2.618:  # Rule 6
       if r01 >= 1.0:
           cands = [":c3", ":F3"]
       else:
           cands = [":c3"]
   ```

### Fix 3 — `label_monowaves()`: preserve ambiguity; use m3 to narrow

**File:** `rules.py:786–791`

Current code collapses to index 0 unconditionally. Instead:

1. Accept an optional `m3: Optional[Wave]` parameter.
2. For Rule 2 and Rule 3b (ambiguous cases), check m3:
   - If m3 is available and m3 > m2 and m3 moves in m1's direction → prefer `:5` over `:L5`, prefer `:5` over `:3`.
   - If m3 ≤ m2 or subdivides into 3 → prefer `:L5` over `:5`.
3. When ambiguity remains, keep the full candidate list and mark the label as `":5|:3"` (pipe-separated) rather than silently picking one.
4. The final monowave (no m2) gets `:?` (provisional) — this is already done correctly.

```python
def label_monowaves(pivots: Sequence[Pivot]) -> list[tuple[Wave, str]]:
    ...
    for i, m1 in enumerate(waves):
        m0 = waves[i - 1] if i - 1 >= 0 else None
        m2 = waves[i + 1] if i + 1 < n else None
        m3 = waves[i + 2] if i + 2 < n else None   # NEW: pass to candidates
        if m0 is None or m2 is None:
            out.append((m1, ":?"))
            continue
        cands = monowave_candidates(m0, m1, m2, m3=m3)   # pass m3
        core = cands[0] if len(cands) == 1 else "|".join(cands[:2])
        rule = _retracement_rule(m2.length / m1.length if m1.length else float("nan"))
        out.append((m1, f"{core}(R{rule})"))
```

### Fix 4 — `group_polywaves()`: use structure labels in grouping decisions

**File:** `rules.py:833–846`

After collecting `grp = waves[start:start + size]`, also read the labels from
`items[start:start + size]`:

```python
for size in (3, 5):
    for start in range(0, len(waves) - size + 1):
        grp = waves[start:start + size]
        labs = [lab for (_, lab) in items[start:start + size]]
        if size == 5:
            hard = elliott_hard_rules(grp)
            if any(h.status is Status.FAIL for h in hard):
                continue
            # NeoWave label check: motive labels on w1/w3/w5, corrective on w2/w4
            motive_ok = all(any(c in labs[i] for c in (":5", ":s5", ":L5")) for i in (0, 2, 4))
            corrective_ok = all(any(c in labs[i] for c in (":3", ":F3", ":c3", ":sL3")) for i in (1, 3))
            if not (motive_ok and corrective_ok):
                continue   # fails NeoWave structural constraint
            ...
```

For ambiguous labels (pipe-separated), treat as passing if ANY candidate satisfies
the required role.

### Fix 5 — `validate_impulse()`: extend S&B to all adjacent wave pairs

**File:** `rules.py:853–864`

Replace the single S&B call:
```python
# Current
res.append(similarity_and_balance(w[1], w[3], context="wave2 vs wave4"))

# Required
for i in range(len(w) - 1):
    res.append(similarity_and_balance(w[i], w[i+1], context=f"w{i+1} vs w{i+2}"))
```

Also apply S&B to all adjacent pairs in `group_polywaves()` for 5-wave candidates
(currently missing entirely — rules.py:843–846).

### Fix 6 — `is_terminal()` and `terminal_rules()`: enforce 61.8% limit as FAIL

**File:** `rules.py:585–636`

In `is_terminal()` (line 601): the wave-2 limit must be `Status.FAIL`, not a
status-neutral note, when wave-2 retraces > 61.8% of wave-1:

```python
# In is_terminal():
w2_limit_ok = w2_retr <= 0.618 + 1e-9
if not w2_limit_ok:
    return RuleResult("terminal impulsion", Status.FAIL,   # FAIL not PASS
                      f"wave2 retraces {w2_retr:.0%} of wave1 (>61.8% -> NOT a valid terminal)")
```

In `terminal_rules()` (line 625–627):
```python
res.append(RuleResult("terminal: wave2 <= 61.8% of wave1",
                      Status.FAIL if w2_retr > 0.618 + 1e-9 else Status.PASS,
                      f"wave2 retraces {w2_retr:.0%} of wave1"))
```

### Fix 7 — `rule_of_proportion()`: FAIL for claimed extension < 161.8%

**File:** `rules.py:420–424`

The function signature only receives a parent and child pair. The 161.8% check needs
to be in `validate_impulse()` where all three motive waves are available, not in
`rule_of_proportion()` itself. Add to `validate_impulse()` or `elliott_guidelines()`:

```python
# In elliott_guidelines(), replace the WARN-only extension check:
if ext_ratio >= 1.618:
    ext_st = Status.PASS
elif ext_ratio >= 1.3:
    ext_st = Status.WARN   # borderline; keep WARN for classical EW
else:
    # NeoWave hard rule: < 1.3x means no extension at all
    # Caller should treat this as FAIL if pattern claims to be a NeoWave trending impulse
    ext_st = Status.WARN   # upgrade to FAIL in a NeoWave-specific wrapper
```

Add a new `neowave_extension_check(w1, w3, w5)` function that returns `Status.FAIL`
when the claimed extension is < 161.8%:

```python
def neowave_extension_check(waves: Sequence[Wave]) -> RuleResult:
    """NeoWave hard rule: extended wave >= 161.8% of next-longest (QA-1006)."""
    if len(waves) != 5:
        return RuleResult("NW extension", Status.NA, "need 5 waves")
    w1, _, w3, _, w5 = waves
    lens = sorted([w1.length, w3.length, w5.length], reverse=True)
    ratio = lens[0] / lens[1] if lens[1] else float("nan")
    if ratio >= 1.618:
        return RuleResult("NW extension >=161.8%", Status.PASS, f"{ratio:.2f}x")
    return RuleResult("NW extension >=161.8%", Status.FAIL,
                      f"longest={ratio:.2f}x next: no valid NeoWave extension (need >=1.618)")
```

---

## 5. Root Cause Analysis: Why `:3`/`:sL3` Dominate and Why S&B Often WARNs

### 5.1 The `:3` Dominance

Three bugs compound to produce the corrective-label inflation:

1. **M6 (label collapse):** `label_monowaves()` always picks index 0. For Rules 3, 5,
   and 6, index 0 is `:3`. This means any monowave retraced by 61.8–100% of m2 (the
   most common real-market range) gets `:3` as its primary, regardless of whether m3
   and r01 indicate a motive sub-condition (Rule 3b ambiguity case).

2. **M3 (`:c3` missing from Rule 5):** The C-wave that closes an A-B-C sequence falls
   in Rule 5 or Rule 6 territory (m2 > m1 as the engine continues the larger trend).
   `:c3` is absent from the candidate set, so every sequence completion is `:3`.

3. **M2 (`:F3` missing from Rule 3):** Flat B-waves (the first leg of a flat) fall in
   Rule 3. Without `:F3` in the candidates, they are labelled `:3`, indistinguishable
   from any other corrective. The polywave grouper cannot detect the flat's internal
   structure.

### 5.2 The `:sL3` Dominance

`:sL3` appears in the Rule-6 candidate set for ALL r01 values, and in Rule-7. In a
strong uptrend, every downward correction that is small relative to the prior up-move
generates a very large m2 (the subsequent up-move) relative to m1 (the correction).
This puts many of those corrections in Rule-5/6 territory, which the code maps to
`[":3", ":sL3"]` — and `:sL3` appears in the candidates for a large proportion of the
strong-uptrend corrections, inflating its prevalence.

### 5.3 The NeoWave / Elliott Disagreement

The Elliott engine (`label_and_validate()`) uses `elliott_hard_rules()` and
`validate_impulse()` directly on pivots at the macro level. The NeoWave labels come
from `label_monowaves()` at the monowave level. There is no reconciliation step: the
monowave labels are not fed back into the macro-level Elliott analysis. Both engines
produce independent outputs from the same pivot stream, and there is no mechanism to
enforce that Elliott's wave-3 corresponds to a NeoWave `:5` at the monowave level.

### 5.4 The S&B WARNs

S&B WARNs on AVGO 4H (time 3.81×), AVGO 1H (price 0.28×), and MRVL 1W (price 0.22×)
are applied post-hoc to the most recent A vs C pair in the macro-level correction
identified by the Elliott engine. Because the macro-level degree is assumed (not
bottom-up computed), and because no S&B check is performed during polywave grouping (M7),
the same degree is assigned to waves of vastly different sizes. When size differences
are > 3×, S&B WARN is mathematically unavoidable given the assumed degree — it is a
symptom of the missing bottom-up degree assignment, not a wrong S&B threshold.

---

## 6. Priority Order for Fixes

| Priority | Fix | Rationale |
|----------|-----|-----------|
| P1 | Fix 3 (ambiguity preservation in `label_monowaves`) | Eliminates premature collapse; this is the root cause of the `:3` bias |
| P2 | Fix 2 (complete candidate sets per Rule) | Adds `:F3`, `:c3` to correct rule branches; makes flat/zigzag C-waves identifiable |
| P3 | Fix 1 (overlap test correction) | Correct Rule 3/4 routing; prevents systematic miscorrection in the 0.618–1.0 band |
| P4 | Fix 4 (use labels in polywave grouper) | Activates the bottom-up discipline that Phase 4 requires |
| P5 | Fix 5 (S&B coverage) | Correct degree-consistency checking; catches the observed 3.81× violations at the grouper stage |
| P6 | Fix 6 (terminal wave-2 FAIL) | Low effort; converts a misleading note to an enforcement signal |
| P7 | Fix 7 (extension hard rule) | Low effort; adds the NeoWave distinguishing FAIL gate |

---

## 7. Summary Table — Existing Correct Implementations

Not all NeoWave is wrong. The following are correctly implemented and should not be
changed without care:

| Component | File:Function | Status |
|-----------|--------------|--------|
| S&B 1/3–3× band (price AND time) | `rules.py:409`, `toolkit.py:297` | Correct |
| Retracement breakpoints (38.2/61.8/100/161.8/261.8%) | `rules.py:743–759` | Correct |
| Two-stage 2-4 confirmation (Stage 1 + Stage 2 timing) | `rules.py:464–490` | Correct |
| `confirm_completion()` causal per-bar monitor | `rules.py:509–545` | Correct |
| Diametric time-similarity (adjacent-leg 1/3–3× check) | `rules.py:664` | Correct |
| Neutral triangle (C longest, A≈E, C ≤ 261.8%×A) | `rules.py:704–719` | Correct |
| x-wave check (< 61.8% = small, 61.8–100% = WARN, > 100% = FAIL) | `rules.py:722–733` | Correct |
| Terminal overlap check | `rules.py:594–598` | Correct |
| Terminal contracting/expanding shape | `rules.py:599`, `rules.py:628–633` | Correct |
| Rollback rules (Phase 2) | NOT IMPLEMENTED | Missing |
| Rule of Neutrality | NOT IMPLEMENTED | Missing |
| 0-2 trendline construction | NOT IMPLEMENTED | Missing |

---

## Sources

- Glenn Neely, *Mastering Elliott Wave* v2, Windsor Books, 1990 [MEW]
- [neowave.com — Structure labels :F3 vs :5 (QA-25)](https://www.neowave.com/qow/qow-archive-25.asp)
- [neowave.com — S&B importance (QA-32)](https://www.neowave.com/qow/qow-archive-32.asp)
- [neowave.com — S&B: price or time? (QA-78)](https://www.neowave.com/qow/qow-archive-78.asp)
- [neowave.com — Extension ≥ 161.8% (QA-1006)](https://www.neowave.com/qow/qow-archive-1006.asp)
- [neowave.com — Wave-2 retrace limit terminal (QA-1079)](https://www.neowave.com/qow/qow-archive-1079.asp)
- [neowave.com — Neutral triangle (QA-8)](https://www.neowave.com/qow/qow-archive-8.asp)
- [neowave.com — Post-constructive behaviour (QA-19)](https://www.neowave.com/qow/qow-archive-19.asp)
- [LiteFinance — NeoWave intro](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- [LiteFinance — Complexity, Balance, Compaction (Part 18)](https://www.litefinance.org/blog/for-professionals/neowave-part-18-rules-of-complexity-and-balance-compaction-procedures-power-ratings/)
- [ForexTalker — Rollback rules + Rule 1](https://forextalker.com/neowave-wave-theory-by-glenn-neely-rollback-rules-and-the-first-rule-of-wavelength-relationships/)
- [ForexTalker — Rule 2 conditions](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-the-second-rule-for-the-ratio-of-wavelengths-and-conditions-for-its-implementation/)
- [ForexTalker — Conditions a, b, c, d for Rule 7](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-a-b-c-and-d-for-the-seventh-rule/)
- [Scribd — NeoWave Part 2 (Polywaves + Structure Labels)](https://www.scribd.com/document/690130352/Part-2-Basic-Info-on-Polywaves-and-Structure-Labels)
- [Scribd — NeoWave Part 5 (Retracement Rule 3)](https://www.scribd.com/document/502299837/5-The-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 7 (Retracement Rule 4)](https://www.scribd.com/document/502300644/7-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 9 (Rules 5 & 6)](https://www.scribd.com/document/502311042/9-NeoWave-theory-by-Glenn-Neely)
- `docs/research/02_neowave_neely.md` — prior audit baseline
- `docs/research/deep/05_neowave_full_algorithm.md` — implementable algorithm spec
- `reports/WAVE_COUNTS_AVGO_MRVL.md` — observed engine output (2026-06-09)
