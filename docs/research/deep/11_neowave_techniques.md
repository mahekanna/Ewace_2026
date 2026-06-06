# 11 — NeoWave Techniques: Gap Analysis, Card Spec, and Priority Gaps

**Status:** research sweep — 2026-06-06
**Author:** agent research session (Ewace_2026)
**Scope:** Dedicated audit of every public NeoWave technique against the current
`wavelib` implementation. Focuses on GAPS and on how each technique should be
PRESENTED to the user, not on repeating what is already documented in `02_neowave_neely.md`
or `05_neowave_full_algorithm.md`.

---

## 1. Scope and Sources

This document was produced by:

1. Reading `docs/research/02_neowave_neely.md` (theory baseline + gap table),
   `docs/research/deep/05_neowave_full_algorithm.md` (implementable algorithm spec),
   and `wavelib/rules.py` in full (all NeoWave functions: `label_monowaves`,
   `monowave_candidates`, `similarity_and_balance`, `rule_of_proportion`,
   `retracement_logic`, `two_four_test`, `two_four_confirmation`, `throwover_test`,
   `base_channel_test`, `terminal_rules`, `is_terminal`, `terminal_retrace_window`,
   `is_neutral_triangle`, `is_running_triangle`, `classify_complex_correction`,
   `x_wave_check`, `group_polywaves`).

2. Web research across: neowave.com Q&A archive, LiteFinance 27-part NeoWave series,
   ForexTalker NeoWave series, Scribd NeoWave chapter PDFs, MTrading NeoWave overview,
   opofinance NeoWave trading, stockpathshala NeoWave rules, niftywaveindia blog.
   (ForexTalker and many downstream sites returned HTTP 403; content was captured
   via search-result summaries and prior session fetches in `02_neowave_neely.md`.)

**What is NOT duplicated here:** the theory narrative, individual rule tables, and
source URLs from `02_neowave_neely.md` and `05_neowave_full_algorithm.md`. Those
documents are the authoritative theory reference. This document is the TECHNIQUE-STATUS
and PRESENTATION layer: for each NeoWave technique, mark its implementation state and
specify what a user-facing output should show.

---

## 2. Technique-by-Technique Table

**Status codes:**
- `IMPL(func)` = fully implemented in the named function
- `PARTIAL(func)` = function exists but with known gaps
- `STUB(func)` = function present but returns placeholder / unconditional result
- `MISSING` = no implementation at all

| # | Technique | What It Is | Our Status | How to Surface |
|---|-----------|-----------|-----------|---------------|
| T01 | **Chart standardisation** | Uniform bar resolution, arithmetic price scale (not log), no missing bars, bar compaction for overlapping bars | MISSING | Pre-flight check panel: "Chart OK: uniform 4H bars, arithmetic scale" or WARNING if log-scale detected; flag missing bar count |
| T02 | **Rule of Neutrality** | Merge tiny monowaves (< ~10% of adjacent wave) into neighbours before labelling; prevents phantom pivots | MISSING | Show absorbed-pivot count in pre-flight: "Neutrality: 2 pivots absorbed" |
| T03 | **Rollback rules (R1/R2/R3)** | Correct monowave endpoints when price briefly overshoots a prior pivot (near-miss, one-bar spike, flat top) | MISSING | Mark each rollback-corrected pivot with a flag: "pivot @$385 rolled-back from $386.10" |
| T04 | **Monowave extraction** | ZigZag pivot detection with percentage-reversal threshold | PARTIAL(`toolkit.zigzag`) | Show pivot count and ZigZag threshold used: "23 pivots, threshold=3.0%" |
| T05 | **Structure labels :5/:3** | Assign motive/corrective core label using m0/m1 price-and-time comparison | PARTIAL(`label_monowaves`) | Show label string per monowave: "m1 → :5(R2), m2 → :3(R3)" |
| T06 | **Full 7-rule structure labels** | Complete sub-type labels (:F3/:c3/:L5/:s5/:sL3/:L3) from 7-rule decision tree with conditions a–d | PARTIAL(`monowave_candidates`) | Show candidate label set: "m3 → {:5, :L5} (ambiguous, Rule 2c)" |
| T07 | **Rule of Similarity & Balance — price** | Adjacent corrective waves: price ratio in [1/3, 3×] | PARTIAL(`similarity_and_balance`) | Show P-ratio and pass/fail: "S&B price: 1.42× (ok)" |
| T08 | **Rule of Similarity & Balance — time** | Adjacent corrective waves: time ratio in [1/3, 3×] | PARTIAL(`similarity_and_balance`) | Show T-ratio and pass/fail: "S&B time: 0.28× (WARN — different degree?)" |
| T09 | **S&B applied to ALL adjacent pairs** | S&B must run on every adjacent corrective pair, not just W2 vs W4 | PARTIAL (only W2/W4 and A/C; gaps in triangle legs) | In the output card, list all S&B checks with their pair labels |
| T10 | **Rule of Proportion** | Sub-wave ≤ parent wave; extended wave must be ≥ 161.8% of next-longest | PARTIAL(`rule_of_proportion`) | Show child/parent ratio: "Proportion: 0.73× (ok)" or "No valid extension (ratio 1.48× < 1.618): not a trending impulse" |
| T11 | **Retracement rules 1–4 (< 100%)** | Seven-rule decision tree, breakpoints at 38.2% / 61.8% / 100% | PARTIAL(`retracement_logic`, `monowave_candidates`) | Show rule triggered: "Rule 2: m2 retraces 54% of m1 → :5 (1st or 5th)" |
| T12 | **Retracement rules 5–7 (> 100%)** | Strong-reversal / extreme-reversal bands; conditions a–d on m0/m1 ratio | PARTIAL(`monowave_candidates`) | Show rule + condition: "Rule 6b → :c3 or :F3 (m0/m1=1.3×)" |
| T13 | **Rule 4 overlap variant** | Rule 3 vs Rule 4 split: Rule 4 applies when m2 retraces into m0's price territory | MISSING (code merges rules 3 & 4) | Show overlap flag: "Rule 4 (overlap detected): :c3" |
| T14 | **Conditions a–d sub-classification** | Four sub-conditions indexed by m0/m1 ratio, modifying structure label for Rules 5–7 | PARTIAL(`monowave_candidates`, missing m3 context) | Show condition letter: "Rule 5, condition b → :3 or :F3" |
| T15 | **Polywave grouping** | Sliding-window (size 3 or 5) over labelled monowaves; validate each group via correction/impulse rules + S&B | PARTIAL(`group_polywaves`) | Show candidate groups: "3 polywave candidates at degree 1" |
| T16 | **Compaction hierarchy** | Monowave → Polywave → Multiwave → Macrowave; assign compacted :5/:3 label at each level | MISSING (no multi-level WaveTree) | Show degree column: "Degree 0: monowave :3 | Degree 1: polywave :5" |
| T17 | **Power ratings (complexity)** | Integer complexity metric: monowave=1, polywave=2, multiwave=3, macrowave=4 | MISSING | Show power rating per wave segment: "W2 complexity=2 (polywave)" |
| T18 | **Channeling-FIRST order** | 0-2, 2-4, 1-3 trendlines built BEFORE pattern is named | PARTIAL (demo enforces order; `validate_impulse` does not require it) | Show channel-first badge: "Channeling checked before count assigned" |
| T19 | **0-2 base channel** | Line from pivot-0 through wave-2 end; corrects wave-2 endpoint if price violates and reverses | PARTIAL(`base_channel_test` as passive check; no active endpoint correction) | Show 0-2 line value at current bar: "0-2 line: $301.4 | Price: $385.7 → holding (motive intact)" |
| T20 | **2-4 trendline (static break)** | Line through endpoints of W2 and W4; break signals impulse nearing completion | IMPL(`two_four_test`) | Show line value + break status: "2-4 line: $301 | Price: $385.7 → NOT broken (impulse unconfirmed)" |
| T21 | **2-4 confirmation Stage 1 (timing)** | Break must occur in < W5-build-time after W5 peak | IMPL(`two_four_confirmation`) | Show timing gate: "Stage 1: line not yet broken (0 / 65 days)" |
| T22 | **2-4 confirmation Stage 2 (timing)** | Full W5 retrace to W5 origin within W5-build-time | IMPL(`two_four_confirmation`) | Show timing gate: "Stage 2: W5 origin $289.96 | Price $385.7 → not retraced" |
| T23 | **1-3 upper channel (throw-over/fell-short)** | Parallel to 2-4 line through W1 top; W5 relative position signals exhaustion type | IMPL(`throwover_test`) | Show flavour: "W5 THROW-OVER 1-3 line ($460) by $35 → blow-off exhaustion" |
| T24 | **Trending impulse hard rules (3)** | W2 < 100% W1; W3 ≠ shortest; W4/W1 no overlap | IMPL(`elliott_hard_rules`) | Show each rule: PASS/FAIL with values |
| T25 | **Extension hard rule (NeoWave)** | One motive wave ≥ 161.8% of next-longest; HARD in NeoWave, not just guideline | PARTIAL (treated as WARN in `elliott_guidelines`) | Flag if extension claimed without 161.8% ratio: "FAIL: W3 = 1.36× W1 — no valid extension; re-examine count" |
| T26 | **Wave-2 time rule** | W2 must consume ≥ W1 time (trending impulse); W4 must consume ≥ W3 time | MISSING | Show timing pair: "W2 bars: 14 | W1 bars: 10 → ok (W2 >= W1)" |
| T27 | **Alternation** | W2 and W4 should alternate in character (one sharp/deep, one sideways/shallow) | PARTIAL (checked in `elliott_guidelines` as WARN) | Show: "Alternation: W2=61% sharp, W4=23% sideways → alternating (ok)" |
| T28 | **Terminal: W4/W1 overlap** | Mandatory overlap; diagnostic feature of terminal vs trending | IMPL(`is_terminal`, `terminal_rules`) | Show: "Terminal: W4/W1 OVERLAP present (terminal confirmed)" |
| T29 | **Terminal: W2 ≤ 61.8% hard limit** | In terminal, W2 corrective sub-wave may not exceed 61.8% of W1 | IMPL(`terminal_rules`) | Show: "W2 retraces 34% of W1 (≤ 61.8%: ok)" or "WARN: 72% > 61.8%" |
| T30 | **Terminal: contracting vs expanding shape** | w1>w3>w5 (contracting) or w5>w3>w1 (expanding/irregular) | IMPL(`terminal_rules`) | Show: "Shape: CONTRACTING (textbook)" or "EXPANDING (rarer, WARN)" |
| T31 | **Terminal: 3-3-3-3-3 sub-structure** | All 5 sub-waves should be internally corrective | PARTIAL (REF stub; cannot check without structure labels) | Show: "Sub-structure: REF — requires monowave labels (Task 1 not complete)" |
| T32 | **Terminal retrace bias window** | Monitor window (1/4 to 1/2 build time) for retrace acceleration; origin is structural target | PARTIAL(`terminal_retrace_window`) | Show: "Retrace monitor: watch 2026-07-01 to 2026-09-01 | Target: $289.96 (structural bias, NOT timed forecast)" |
| T33 | **Zigzag: B ≤ 61.8% of A (hard)** | Hard limit in NeoWave (not guideline) | IMPL(`classify_correction`) | Show: "ZIGZAG: B retraces 54% of A (≤ 61.8% hard limit: ok)" |
| T34 | **Zigzag: C surpasses A** | C endpoint must exceed A endpoint (else truncated C, a WARN) | PARTIAL (checked in `classify_correction` as C/A ratio, not endpoint check) | Show: "C surpasses A end: yes (C $412 > A end $398)" |
| T35 | **Flat B ≥ 61.8% of A (hard lower bound)** | B in flat must retrace ≥ 61.8% of A; below → triangle leg or zigzag B | MISSING | Show: "Flat B: 83% of A (≥ 61.8%: ok)" |
| T36 | **Post-correction thrust** | After flat/zigzag, thrust proportional to correction size in ≤ correction time | MISSING | Show: "Post-correction: thrust expected ≥ $XX within ~N bars (monitor)" |
| T37 | **Contracting triangle: 5-leg a-b-c-d-e** | a>b>c>d>e; all legs corrective (3-3-3-3-3); converging trendlines | PARTIAL(`_classify_triangle`) | Show leg progression and sub-structure: "CONTRACTING TRIANGLE: a=47>b=38>c=29>d=22>e=14" |
| T38 | **Neutral triangle (NeoWave exclusive)** | C longest; A≈E (each ≥ 38.2% of C); C ≤ 161.8–261.8% of A | IMPL(`is_neutral_triangle`) | Show: "NEUTRAL TRIANGLE: C=1.43×A, A≈E (ratio 0.94) — ok" or WARN |
| T39 | **Running triangle (EWF extended)** | B exceeds wave-A origin; highest mislabel risk | IMPL(`is_running_triangle`) | Show: "RUNNING TRIANGLE: B breaks beyond A origin — mislabel risk, verify" |
| T40 | **Post-triangle thrust timing** | Thrust ≈ widest leg (wave a); completes in ≤ shortest leg time | MISSING | Show: "Post-triangle thrust target: $XX to $YY | Expected within ~N bars" |
| T41 | **Barrier triangle** | One trendline is horizontal (within 3% tolerance) | PARTIAL(`_classify_triangle`) | Show: "BARRIER TRIANGLE: a-c-e boundary flat (within 3%)" |
| T42 | **Diametric (7 legs): time similarity** | All 7 legs similar in TIME (S&B 1/3–3×); no x-waves | PARTIAL(`classify_complex_correction`) | Show time-ratio matrix: "Diametric time spread: max/min = 2.1× (ok < 3×)" |
| T43 | **Diametric: bowtie vs diamond** | Bowtie: legs expand to d then contract; Diamond: contract to d then expand | PARTIAL(`classify_complex_correction`) — uses mid=max/min heuristic instead of proper expand/contract test | Show: "DIAMETRIC BOWTIE: legs [d=longest]; time similar" |
| T44 | **Diametric: post-pattern thrust** | Sharp thrust after leg g, ≈ widest part of formation | MISSING | Show: "Post-diametric thrust target: $XX | Expect sharp move post-g" |
| T45 | **Symmetrical (9 legs)** | All 3 dimensions (price + time + complexity) similar within advancing group and within declining group; groups dissimilar to each other | PARTIAL(`classify_complex_correction`, 9-leg branch) | Show: "SYMMETRICAL (9 legs): adv p=0.91 t=0.87 | dec p=0.88 t=0.83 | cross-dissimilar: ok" |
| T46 | **x-wave size rule (61.8%)** | Small x-wave retraces < 61.8% of prior correction; > 100% is structural error | IMPL(`x_wave_check`) | Show: "x-wave: 45% of prior correction (small x-wave: ok)" |
| T47 | **x-wave complexity bounds** | x-wave power rating ≤ prior correction; ≥ least complex sub-wave of prior correction | MISSING | Show: "x-wave complexity: 1 (mono) vs prior correction 2 (poly) — ok" |
| T48 | **Pre-constructive rules** | Complexity progression, alternation requirement, extension rule, W4/W1 constraints, applied as a filter before any pattern name | PARTIAL (some in `elliott_hard_rules`, extension as WARN; no unified pre-constructive filter) | Show as a pre-check block: "Pre-constructive: complexity ok, alternation WARN, extension FAIL" |
| T49 | **Post-constructive: Stage 1/2 timing** | 2-4 line break in < W5 time (Stage 1); full W5 retrace in ≤ W5 time (Stage 2) | IMPL(`two_four_confirmation`) | See T21/T22 |
| T50 | **Post-constructive: post-correction thrust** | Thrust after flat/zigzag proportional to correction in ≤ correction duration | MISSING | Show: "Post-correction thrust: monitoring ($XX target, N-bar window)" |
| T51 | **Rule of Reverse Logic** | When counts conflict, prefer the count furthest from completion | MISSING | Show: "Reverse Logic: Pattern A is 42% complete; Pattern B is 78% complete → prefer Pattern A" |
| T52 | **Progress labels** | Position-tracking labels within patterns (e.g. "now in W3 of trending impulse (III)" or "now in B of flat correction") | MISSING | Show: "Current position: W4 of trending impulse; expect W5 next" |
| T53 | **Trading method: entry confirmation** | Trade entered after two consecutive bars in the new direction post-pattern; ALSO "post-pattern price moves further and faster than largest counter-trend wave of the prior pattern" | MISSING | Show: "Entry signal: 0 / 2 confirmation bars observed" |
| T54 | **Trading method: stop placement** | Stop above/below the pattern's origin (for terminals: origin = terminal start; for impulse: W2 origin) | MISSING | Show: "Stop: $289.96 (terminal origin)" |
| T55 | **Trading method: Fibonacci price targets** | W3 targets: 1.618×/2.618×/4.236×W1 from W2 end; W5 targets: W5=W1 or 0.618×W3 from W4 end; post-correction thrust ≈ prior correction size | PARTIAL(`project_wave5`) | Show target table: "W5 targets: $338 (=W1), $371 (=0.618×W3), $430 (=1.618×W1)" |
| T56 | **Trading method: time targets** | W4 must consume ≥ W3 time before W5 can be valid; retrace time rules for Stage 1/2 | PARTIAL (W5 timing in `two_four_confirmation`; W4 time rule missing) | Show: "W4 minimum duration: 12 bars (W3=12); currently 9 bars → W4 NOT complete yet" |
| T57 | **Trading method: invalidation level** | Count invalid if: W2 > 100% of W1 (trending), W2 > 61.8% of W1 (terminal), W4 overlaps W1 (trending), W3 shortest | PARTIAL (hard rules in `elliott_hard_rules`; invalidation framing missing) | Show: "Invalidation: price below $289.96 (terminal origin) negates terminal count" |
| T58 | **Degree notation** | Progress-label degree brackets: (i)(ii)... minor, ((i))((ii))... intermediate, (I)(II)... primary | MISSING (Degree enum exists but no progress-label notation output) | Show degree-annotated label: "Currently in wave ((3)) of Primary (III)" |
| T59 | **Extracting triangle** | Formerly a distinct type; Neely retired the term (QA-923); maps to neutral triangle with extended C | IMPL (subsumed by `is_neutral_triangle`) | No separate output needed; note in neutral-triangle output: "Extracting triangle category retired by Neely (now: neutral triangle)" |
| T60 | **Correction sub-type: strong/normal/weak B** | Flat B-wave classification: strong B > 100% of A; normal B 80–100%; weak B 61.8–80% | MISSING | Show: "Flat B: STRONG (B=114% of A) → expanded flat expected" |

---

## 3. NeoWave Analysis CARD Specification

A per-symbol "NeoWave Techniques" panel should display the following fields, derived
from functions already in `wavelib/rules.py`. Fields are grouped into sections.
Unavailable data (e.g. monowave labels not yet computed) should show "REF" or "N/A"
rather than an error.

### Section A: Pre-Flight

```
Pre-flight
  ZigZag threshold:    3.0%          (toolkit.zigzag parameter)
  Pivot count:         23            (len(pivots))
  Pivots absorbed:     0             (apply_neutrality output — currently MISSING)
  Rollback corrections: 0            (apply_rollback output — currently MISSING)
  Scale warning:       N/A           (chart standardisation — currently MISSING)
```

### Section B: Monowave Structure Labels

```
Monowave Labels   [last 5 visible]
  m(-4):  :5(R2)          (motive, rule 2)
  m(-3):  :3(R3)          (corrective, rule 3)
  m(-2):  :5|:3(R3)       (ambiguous — carry both)
  m(-1):  :3(R6)          (corrective, rule 6)
  m(0):   :?(R?)          (PROVISIONAL — m2 not yet confirmed)

  S&B (all adjacent corrective pairs): [list, see Section D]
```

### Section C: Pattern Identification

```
Pattern ID
  Candidate count:      2            (number of polywave candidates)
  Best match:           TERMINAL IMPULSE (5-wave, score=2 WARNs, 0 FAILs)
  Alt match:            TRENDING IMPULSE (score=1 FAIL — W4/W1 overlap)

  Pattern label:        Terminal impulsion (5-3-3-3-3)
  Degree confidence:    HEURISTIC
  Shape:                CONTRACTING (w1>w3>w5)
  Progress label:       w5 COMPLETE                    (from terminal_rules)
  Current wave pos:     Post-W5 (monitoring retrace)   (from post-constructive check)
```

### Section D: NeoWave Rules Output

```
NeoWave Rules
  S&B W2 vs W4:       price 1.07× ok | time 0.65× ok → PASS
  S&B A vs C:         price 1.24× ok | time 1.81× ok → PASS
  S&B W1 vs W3:       price 1.42× ok | time 0.51× ok → PASS    [currently missing]
  S&B W3 vs W5:       price 1.89× ok | time 0.31× WARN         [currently missing]
  Proportion (W3):    0.88× of parent → ok
  Extension:          W3=1.36×W1 → no valid extension (NeoWave hard rule WARN)
  Retracement logic:  W2 retraces 54% of W1 → Rule 2: 1st/5th context
  Alternation:        W2=34% deep, W4=23% shallow → alternating (PASS)
  W2 time rule:       W2=14 bars >= W1=10 bars → PASS           [currently missing]
```

### Section E: Terminal Checks

*(only when is_terminal returns PASS)*

```
Terminal Checks
  W4/W1 overlap:          YES → terminal confirmed
  W2 <= 61.8% of W1:      34% → PASS
  Shape:                  CONTRACTING (textbook)
  Sub-structure (:3 each): REF — requires monowave labels
  Retrace bias window:    Watch 2026-07-01 to 2026-09-01
  Full retrace target:    $289.96 (terminal origin — directional bias)
  Stage 1 trigger:        2-4 line @ $301 | Price $385.7 → NOT broken yet
  Stage 2 trigger:        W5 origin $289.96 | NOT yet retraced
```

### Section F: Channeling Panel

```
Channeling
  0-2 base line @ now:    $274.3 | Price $385.7 → holding (motive intact)
  2-4 trendline @ now:    $301.0 | Price $385.7 → NOT broken
  W5 vs 1-3 upper line:   W5=$495 | 1-3 line=$460 → THROW-OVER (blow-off)
  Confirmation Stage 1:   NOT MET (2-4 line unbroken)
  Confirmation Stage 2:   NOT MET (W5 not retraced)
```

### Section G: Complex Correction Panel

*(only when legs >= 5)*

```
Complex Correction
  Leg count:              5
  Triangle type:          CONTRACTING TRIANGLE
  Neutral triangle check: WARN (C not longest leg)
  Running triangle check: NA (B does not exceed A origin)
  Post-triangle thrust:   Target $XX to $YY (≈ widest leg); N-bar window   [MISSING]

  (If 7 legs:)
  Diametric:              BOWTIE | time spread 2.1× < 3× → PASS
  Post-diametric thrust:  Target $XX [MISSING]

  (If 9 legs:)
  Symmetrical:            adv p=0.91 t=0.87 | dec p=0.88 t=0.83 → PASS
```

### Section H: x-Wave Check

*(only when x-wave argument supplied)*

```
x-Wave
  x-wave size:    45% of prior correction (small x-wave: ok)
  x-wave complexity: REF (power ratings not yet computed)
```

### Section I: Trading Method Output

*(derived from pattern, current price, post-constructive status)*

```
Trading Method
  Trade direction:        NONE (impulse unconfirmed — Stage 1 not met)
  Confirmation needed:    2-4 line break AND 2 consecutive down bars
  Entry trigger:          2-4 line @ $301 breaks, then 2 down bars close below
  Stop level:             $289.96 (terminal origin)
  Invalidation:           Price closes above W5 peak $495 (no count change)
  W5 price targets:       $338 (W5=W1), $371 (W5=0.618×W3), $430 (W5=1.618×W1)
  Time targets:
    Stage 1 window:       < 65 bars post-peak (W5 build time)
    Stage 2 window:       < 65 bars post-Stage-1
  Rule of Reverse Logic:  [MISSING — needs completion_fraction per candidate count]
  Progress label context: Post-wave-5 of Primary (III) terminal — bias DOWN
```

---

## 4. Prioritized GAPS

The following techniques are not implemented and have meaningful analytical impact.
They are ranked by impact-on-user vs implementation effort.

### GAP-1 (CRITICAL): Rules 5–7 overlap detection (T13) and full conditions a–d sub-classification (T14)

**What is missing:** The code's `monowave_candidates()` handles Rules 1–7 in price bands
but does not implement the Rule 3 vs Rule 4 split (which depends on whether m2 retraces
into m0's price territory — an overlap test, not a price-ratio test). Rules 5–7 correctly
identify reversal candidates but do not apply sub-conditions a–d that depend on the
m0/m1 ratio. This means approximately 30–40% of monowaves in trending or extended
markets receive ambiguous labels that could be narrowed with the m0/m1 ratio test.

**Impact:** Every polywave grouping that contains a Rule-5 or Rule-6 monowave carries
extra label ambiguity. This directly inflates the number of candidate counts and reduces
the engine's discrimination power. The overlap test for Rule 4 is particularly important
because rules 3 and 4 have the same r21 range (0.618–1.00) but opposite structural
implications (Rule 3 → corrective; Rule 4 overlap → possibly motive).

**Implementation:** Add `overlap = m2_endpoint_in_m0_territory(m0, m1, m2)` flag to
`_apply_retracement_rules()`. Add `_rule4()` function with the 4a–4e conditions. Add
the m0r (m0/m1 ratio) branch in `_rule5()`, `_rule6()`, `_rule7()`.

**User surface:** "Rule 4 (overlap): :c3 | Rule 3 (no overlap): :3 or :F3 — DISTINCT
structural implications for adjacent polywave."

---

### GAP-2 (HIGH): Trading method panel (T53–T57): entry confirmation, stops, invalidation, time targets

**What is missing:** No function synthesises the pattern-identification output into
actionable trading parameters. The engine can identify a terminal and compute wave-5
targets (`project_wave5`) and retrace windows (`terminal_retrace_window`), but there
is no unified function that outputs:
- The two-consecutive-bar entry confirmation count
- The stop level anchored to pattern origin
- The invalidation price level
- The time-gated targets for Stage 1 and Stage 2

**Impact:** This is the main output a user sees. Without it, the engine produces a list
of rule results that requires manual synthesis. The NeoWave method is explicitly about
eliminating guesswork — the trading-method output is the delivery of that promise.

**Implementation:** New function `neowave_trade_params(pattern, current_t, current_price)
→ TradeParams`. Takes the best-candidate pattern (a `WaveNode`), the current observation,
and returns a `TradeParams` dataclass with all the fields in Section I of the card spec.
The two-consecutive-bar confirmation is stateful — it requires a counter incremented on
each new bar that closes in the confirmation direction.

**User surface:** Section I of the NeoWave card (see §3 above). Most visible improvement
to user output.

---

### GAP-3 (HIGH): Post-constructive rules as a stateful queue (T50–T52)

**What is missing:** Post-constructive checks (post-correction thrust, post-triangle
thrust, Rule of Reverse Logic) require subsequent price bars that do not exist at the
time the pattern is labelled. The engine has no mechanism to:
- Queue a "pending confirmation check" for a just-identified pattern
- Update the confirmation status on each new bar
- Apply the Rule of Reverse Logic across competing candidate counts

**Impact:** Without this, the engine cannot tell the user "your terminal pattern has
not been confirmed yet" (Stage 1 not met) from "your terminal pattern IS confirmed and
the retrace has begun." This distinction is the difference between a speculative position
and a confirmed reversal trade. The current `two_four_confirmation()` function computes
the answer correctly when called, but it is never called automatically as new bars arrive.

**Implementation:** A `ConfirmationQueue` class that holds pending `(pattern, rule_fn)`
pairs and a `.update(current_bar)` method that re-evaluates each pending check. The
`WaveNode` should gain a `confirmation_status: Status` field updated by the queue.
Rule of Reverse Logic: add `completion_fraction` property to `WaveNode` (fraction of
projected price range already moved) and a `rank_by_reverse_logic(candidates)` sorter.

**User surface:** "Stage 1: NOT MET (monitoring) / MET (retrace underway)" with bar
count and elapsed time shown in real time. The reverse-logic winner is flagged with
"Most preferred count (Rule of Reverse Logic): …"

---

### GAP-4 (MEDIUM): Rule of Neutrality + Rollback rules before labelling (T02, T03)

**What is missing:** Before structure labelling, Neely requires (a) the Rule of
Neutrality (absorb tiny monowaves < ~10% of adjacent) and (b) rollback rules (correct
endpoints of brief spike/near-miss pivots). Neither is implemented. The current ZigZag
in `toolkit.py` uses a percentage-reversal that roughly deduplicates nearby pivots but
does not implement Neely's specific rollback situations (R1 near-miss, R2 one-bar spike,
R3 flat top). Without rollback, monowave endpoints are systematically slightly wrong,
which corrupts the m2/m1 ratio used in all seven retracement rules.

**Impact:** Errors compound upward: wrong endpoints → wrong r21 ratios → wrong rule
application → wrong structure labels → wrong polywave grouping. For high-volatility
bars (AVGO had several 3–5% intraday spikes in 2026-Q2), rollback errors can shift
an m2/m1 ratio from 0.59 to 0.65, crossing the Rule 2/3 boundary.

**Implementation:** `apply_rollback(pivots)` and `apply_neutrality(pivots)` already
drafted in `05_neowave_full_algorithm.md §2.3.3 and §2.5.6`. Needs unit tests for the
three rollback situations (R1/R2/R3) and the neutrality threshold edge cases.

**User surface:** "Pre-flight: 2 pivots absorbed (neutrality), 1 rollback correction
(R2 one-bar spike @$386.10 → merged with $385.74 endpoint)."

---

### GAP-5 (MEDIUM): Post-triangle and post-diametric thrust targets (T40, T44)

**What is missing:** After identifying a completed triangle (contracting/neutral/barrier)
or diametric, the engine does not compute the post-pattern thrust target or timing window.
For triangles: thrust ≈ widest leg (leg a) from the e-wave endpoint; must complete in
≤ shortest leg duration. For diametrics: thrust ≈ widest part from g-wave endpoint;
typically sharp but no hard timing rule.

**Impact:** The thrust target is the primary TRADING signal after a triangle/diametric.
Without it, a user who identifies the pattern has no price objective.

**Implementation:** `triangle_thrust_target(legs, breakout_price, direction)` (extend
existing `triangle_thrust()`); add `timing_limit_bars = min(leg.days for leg in legs)`.
`diametric_thrust_target(legs, breakout_price, direction)` — new function returning
`{"target": ..., "note": "timing rule: qualitative only — expect sharp move"}`.

**User surface:** "Post-triangle thrust: $XX–$YY | Must complete within 14 bars" or
"Post-diametric thrust: target ~$XX (sharp, no hard timing limit)."

---

### GAP-6 (MEDIUM): Wave-2 and Wave-4 time rule for trending impulse (T26, T56)

**What is missing:** NeoWave states that in a trending impulse, Wave 2 must consume
at least as many bars as Wave 1, and Wave 4 must consume at least as many bars as Wave 3,
before the wave can be considered "complete." This is a TIMING hard rule, not a price
rule. It means that if a putative Wave 2 ends in 2 bars while Wave 1 took 10 bars,
the Wave 2 is NOT over — price is still in Wave 1 or the pivot is being mislabelled.

**Impact:** This catches early-reversal mislabelling. The AVGO weekly analysis is
immune (wave durations are multi-month) but it matters greatly on the 4-hour and hourly
timeframes where waves 2 and 4 are short.

**Implementation:** Add to `terminal_rules()` and `elliott_hard_rules()`: for trending
impulse, `w2.days >= w1.days` (FAIL if not), `w4.days >= w3.days` (FAIL if not). For
terminal impulse, these constraints are reversed (each corrective sub-wave CAN be
shorter — this is part of what makes it a terminal).

**User surface:** "W2 time rule: W2=8 bars vs W1=12 bars → FAIL (W2 not complete)."

---

### GAP-7 (LOWER): Flat B classification: strong/normal/weak (T60) + post-correction thrust (T36)

**What is missing:** The code classifies flats as regular/expanded/running by the
C-endpoint test but does not sub-classify the B-wave as strong (>100%), normal (80–100%),
or weak (61.8–80%). Neely uses this sub-classification to predict C's target range.
Additionally, the post-correction thrust rule (after any flat or zigzag, expect a thrust
≈ correction size within ≤ correction duration) is not implemented.

**Implementation:** Add to `classify_correction()` for the flat family: compute
`b_strength = "strong" if b_retr > 1.0 else "normal" if b_retr >= 0.80 else "weak"`;
return in detail string. Add `post_correction_thrust_target(correction_wave, direction)`
that returns `{"min": ..., "max": ..., "within_bars": correction.days}`.

**User surface:** "EXPANDED FLAT: B strong (114%); C target ~$XX; post-flat thrust
expected within ~20 bars."

---

### GAP-8 (LOWER): Compaction hierarchy and power ratings (T16, T17)

**What is missing:** The `WaveTree` class drafted in `05_neowave_full_algorithm.md §3.2`
is not yet implemented. Without it, the engine has no multi-level compaction — it
operates at a single degree level with hand-picked pivots. Power ratings (integer
complexity metric) are referenced by the x-wave check and S&B complexity check but
never computed.

**Impact:** This is the foundational bottom-up difference between classical EW practice
and NeoWave. However, it requires T01–T04 (chart standardisation, neutrality, rollback,
monowave labels) to be complete first. This is the highest-difficulty, highest-payoff
gap but is correctly placed last in the build order.

**User surface:** "Degree 0: monowave :3(R3) | Degree 1: polywave :5 (correction of
3 monowaves) | Degree 2: multiwave ZIGZAG."

---

## 5. Honest Caveats

### 5.1 Precision of Rollback Thresholds

Neely's rollback rules use words like "trivially small" and "barely exceeds." No
published numeric threshold exists. The `05_neowave_full_algorithm.md` uses ATR-relative
thresholds as a reasonable approximation, but any deployment should flag rollback-
corrected pivots as REF and allow the analyst to override.

### 5.2 Structure Label Ambiguity Is Irreducible for 30–40% of Monowaves

Rules 3–5 are genuinely ambiguous in real market data. The correct approach is to carry
multiple candidate labels forward and resolve them as later waves arrive. Any forced
single-label output for ambiguous monowaves is an overstatement of confidence and should
be flagged visually (e.g. ":5|:3" notation).

### 5.3 Trading Method Output Is Conditional on Pattern Confirmation

The trading-method panel (Section I of the card) must be clearly gated: if Stage 1
confirmation (2-4 line break) has not occurred, the panel should show "NO TRADE" rather
than optimistic entry guidance. Neely's method is explicit: trade signals follow
confirmed pattern completion, not pattern identification.

### 5.4 Degree Is Always Heuristic Above Monowave Level

The S&B rules constrain but rarely uniquely determine degree. The card should always
display `degree_confidence: HEURISTIC` and show all candidate degree assignments with
their S&B violation counts.

### 5.5 Symmetrical Pattern Detection is REF-Grade

The symmetrical (9-leg) pattern is the least specified in public sources (described in
QA-5 and QA-875 only). Any `SYMMETRICAL: PASS` result from `classify_complex_correction`
should display as `Status.WARN` to the user with a note: "Symmetrical detected — manual
confirmation required; pattern extremely rare."

### 5.6 Post-Constructive Checks Are Asynchronous

Stage 1 and Stage 2 confirmations can only be checked on bars that arrive after the
pattern completes. They cannot be precomputed. The card must update these fields on
each new bar automatically — a static snapshot analysis (like the current demo output)
will appear to stall at "Stage 1: not met" indefinitely.

### 5.7 The Terminal Retrace Is a Bias, Not a Forecast

The `terminal_retrace_window()` output should always include the warning string baked
into `05_neowave_full_algorithm.md §2.9`: the target price is the structural origin, not
a timed forecast. The AVGO over-projection case (documented in `02_neowave_neely.md §2.7`)
happened precisely because this distinction was not preserved in the presentation layer.

---

## Sources

- [Glenn Neely, *Mastering Elliott Wave* v2, Windsor Books, 1990 — Chapter 1 (free)](https://www.neowave.com/mastering-elliott-wave-chapter-1-glenn-neely.asp)
- [neowave.com — What is NeoWave?](https://www.neowave.com/what-is-neowave.asp)
- [neowave.com — How to trade without emotion (entry/stop/confirmation)](https://www.neowave.com/neely-river/how-to-trade-without-emotion-by-glenn-neely.asp)
- [neowave.com — Trading service overview](https://www.neowave.com/trading-strategies.asp)
- [neowave.com — Two confirmation types (QA-1109)](https://www.neowave.com/qow/qow-archive-1109.asp)
- [neowave.com — Diametric definition (QA-3)](https://www.neowave.com/qow/qow-archive-3.asp)
- [neowave.com — Symmetrical definition (QA-5)](https://www.neowave.com/qow/qow-archive-5.asp)
- [neowave.com — X-wave rules (QA-7)](https://www.neowave.com/qow/qow-archive-7.asp)
- [neowave.com — Neutral triangle (QA-8)](https://www.neowave.com/qow/qow-archive-8.asp)
- [neowave.com — Structure vs behaviour (QA-19)](https://www.neowave.com/qow/qow-archive-19.asp)
- [neowave.com — 2-4 line confirmation of W5 end (QA-22)](https://www.neowave.com/qow/qow-archive-22.asp)
- [neowave.com — S&B: both price AND time? (QA-78)](https://www.neowave.com/qow/qow-archive-78.asp)
- [neowave.com — Post-diametric thrust (QA-474)](https://www.neowave.com/qow/qow-archive-474.asp)
- [neowave.com — 0-2 channeling importance (QA-273)](https://www.neowave.com/qow/qow-archive-273.asp)
- [neowave.com — 2-4 trendline placement (QA-303)](https://www.neowave.com/qow/qow-archive-303.asp)
- [neowave.com — Extension ≥ 161.8% (QA-1006)](https://www.neowave.com/qow/qow-archive-1006.asp)
- [neowave.com — Wave-2 retrace limit in terminals (QA-1079)](https://www.neowave.com/qow/qow-archive-1079.asp)
- [neowave.com — Neutral triangle C limit (QA-3849)](https://www.neowave.com/qow/qow-archive-3849.asp)
- [neowave.com — Post-triangle thrust timing (QA-5161)](https://www.neowave.com/qow/qow-archive-5161.asp)
- [neowave.com — Rule of Reverse Logic](https://www.neowave.com/neowave-rules-of-reverse-logic.asp)
- [neowave.com — Stage 1 & Stage 2 Confirmation blog](https://www.neowave.com/tradingblog/blog.asp?bid=157)
- [LiteFinance — NeoWave intro (all 27 parts)](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- [LiteFinance — Part 18: Compaction, Power Ratings, Rules of Complexity](https://www.litefinance.org/blog/for-professionals/neowave-part-18-rules-of-complexity-and-balance-compaction-procedures-power-ratings/)
- [LiteFinance — Part 20: Progress labels in terminal impulses](https://www.litefinance.org/blog/for-professionals/neowave-part-20-application-of-progress-labels-to-terminal-impulses/)
- [LiteFinance — Part 21: Channeling in impulses, Fibonacci relationships](https://www.litefinance.org/blog/for-professionals/neowave-part-21-channeling-in-impulses-and-fibonacci-relationships/)
- [LiteFinance — Part 23: Progress labels in triangles](https://www.litefinance.org/blog/for-professionals/neowave-part-23-progress-labels-and-their-application-to-triangles/)
- [LiteFinance — Part 27: NeoWave trading strategy (practical application)](https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/)
- [ForexTalker — Basic NeoWave concepts and chart construction rules](https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/)
- [ForexTalker — Rollback rules + Rule 1](https://forextalker.com/neowave-wave-theory-by-glenn-neely-rollback-rules-and-the-first-rule-of-wavelength-relationships/)
- [ForexTalker — Rule 2 conditions a–d](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-the-second-rule-for-the-ratio-of-wavelengths-and-conditions-for-its-implementation/)
- [ForexTalker — Conditions b,c,d for Rule 6](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-b-c-and-d-for-the-sixth-rule/)
- [ForexTalker — Conditions a,b,c,d for Rule 7](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-a-b-c-and-d-for-the-seventh-rule/)
- [ForexTalker — Impulse rules of logic (stretched wave, equality, alternation, overlap)](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-price-impulses-the-rules-of-the-stretched-wave-equality-alternation-overlap-the-rules-of-logic/)
- [ForexTalker — Multiwave structure and notation](https://forextalker.com/neowave-wave-theory-by-glenn-neely-about-the-structure-of-multivolts-and-notation/)
- [Scribd — NeoWave Part 5: Retracement Rule 3](https://www.scribd.com/document/502299837/5-The-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 7: Retracement Rule 4](https://www.scribd.com/document/502300644/7-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 9: Retracement Rules 5 & 6](https://www.scribd.com/document/502311042/9-NeoWave-theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 12: Impulsions and Rules to Analyze Impulse Patterns](https://www.scribd.com/document/839672305/Part-12-Impulsions-and-the-Rules-to-Analyze-Impulse-Wave-Patterns-NeoWave-Theory-by-Glenn-Neely)
- [Scribd — NeoWave Part 13: Corrections + identification rules](https://www.scribd.com/document/839672297/Part-13-Corrections-Rules-to-identify-a-correction-NeoWave-theory-by-Glenn-Neely)
- [Scribd — Advanced NeoWave techniques (neorules PDF)](https://www.scribd.com/document/470292919/neorules)
- [ebrary.net — Triangle and Diametric chapter](https://ebrary.net/299888/education/triangle)
- [niftywaveindia.blogspot.com — 7-leg diametric patterns](http://niftywaveindia.blogspot.com/2018/12/technical-learnings-7-legged-diametric.html)
- [Ewace_2026 repo: docs/research/02_neowave_neely.md — theory baseline](docs/research/02_neowave_neely.md)
- [Ewace_2026 repo: docs/research/deep/05_neowave_full_algorithm.md — algorithm spec](docs/research/deep/05_neowave_full_algorithm.md)
