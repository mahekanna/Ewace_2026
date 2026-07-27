# Master audit — where the wave application went wrong, and how to fix it

_Synthesis of four parallel theory-grounded code audits (2026-06-09). Each child
doc has the cited theory, the code references, and the full mistake tables:_

- `01_elliott_impulse_correction.md` — impulse-vs-corrective scoring
- `02_degree_and_coverage.md` — degree hierarchy + the counting DP / coverage
- `03_neowave_neely.md` — NeoWave (Neely) monowave construction
- `04_pivots_and_fibonacci.md` — pivot/ZigZag detection + Fibonacci proportion

The user's hypothesis was correct: **the failure is in the application, not the
theory.** The bad counts (everything labelled corrective, 29–60% coverage, a
16-year move tagged "Minuette", 98 monowaves on MRVL 1W, NeoWave disagreeing with
Elliott) are not noise — they trace to a small set of foundational bugs that
cascade and reinforce each other.

---

## The linchpin: linear vs logarithmic price

**Every wave-proportion comparison in the engine uses linear price differences
(`abs(end.price - start.price)`). Elliott/NeoWave require LOGARITHMIC measurement
for any instrument whose range exceeds ~2× (Neely, neowave.com QA #11 & #38).**
AVGO spans 330×, MRVL 105×.

Concretely (Audit 04, M1): AVGO wave I vs wave III is **7.74× on a linear scale**
(matches no Fibonacci ratio → Fib-quality ≈ 0) but **1.10× on a log scale** (near
equality/extension → Fib-quality ≈ 1.0). On a linear scale the engine **cannot
see** that a real impulse has valid proportions, so impulses score ~0 and lose to
corrections at every degree. This single error is upstream of the "everything is
corrective" symptom. It touches `Wave.length` and everything built on it:
`_impulse_quality` (wavetree.py:44), `_fib_score` (automation.py:37),
`similarity_and_balance` (rules.py:412), `wave_ratio` (toolkit.py:264).

---

## Symptom → root cause map

| Observed symptom | Primary cause(s) |
|---|---|
| Every TF labelled corrective (ZIGZAG/FLAT/TRIANGLE/WXY), never IMPULSE | **Log error** (impulse Fib-quality ≈ 0) **×** scoring arithmetic (impulse bonus +0.5 too small; ZIGZAG base 0.80 too high) **×** scale-blindness |
| Primary count covers only 29–60% of the series | DP has **no coverage floor**; carries ungrouped singletons at score 0; picks locally-best root |
| 16-year move tagged "Minuette/Minute" | Degree computed on the **partial** node, not the full series; `anchored_degree` **hard-capped at INTERMEDIATE** (Primary/Cycle/Supercycle/GSC are dead code) |
| 98 "monowaves" on MRVL 1W | `adaptive_zigzag` scale list tops out at 0.30 → never reaches target on a 105×/25-yr series; fixed-% threshold is noise at $2 and Primary-degree at $400 |
| NeoWave disagrees with Elliott on the same swings | NeoWave **premature label collapse** (`monowave_candidates()[0]` without m3 / r01 sub-conditions); `:F3` missing; Rule-3/4 overlap test wrong; polywave grouper **ignores its own labels** |

---

## Root causes, ranked

| # | Root cause | Severity | Audit / location | Why it matters |
|---|---|---|---|---|
| **R1** | **Linear (not log) price** for all ratio/Fib/length comparisons | CRITICAL | 04 M1 — `rules.py:Wave.length`, wavetree:44, automation:37, toolkit:264 | Foundational; makes valid impulse proportions invisible → corrective bias everywhere |
| **R2** | Impulse loses to correction in DP scoring (bonus +0.5; ZIGZAG base 0.80 > impulse node ~0.70) | CRITICAL | 01 M1/M7 — `wavetree.py` `value()`/`_correction_quality` | Corrections out-score impulses node-for-node even before bonuses |
| **R3** | No full-range **coverage constraint** in the DP | CRITICAL | 02 M1 — `wavetree.py:wave_counts`, `_build_level` | Primary count describes a tidy sub-window; rest unlabelled |
| **R4** | Degree computed on the **partial** node + ladder capped at INTERMEDIATE | CRITICAL | 02 M2/M3 — `anchored_degree`, `_anchored_from` | A multi-year structure gets the smallest degree; 4 of 9 degrees unreachable |
| **R5** | Fixed-% ZigZag → degree-inconsistent pivots; scale-blind to Primary-degree moves; `adaptive_zigzag` list too short | HIGH | 04 M2/M3 + 01 M2 — `toolkit.py:zigzag_causal`, `wave_report.py` | Wrong pivots corrupt every downstream label; the full advance is never offered to the DP as one 5-wave group |
| **R6** | NeoWave premature label collapse + wrong candidate sets + polywave ignores labels | HIGH | 03 M6/M2/M10 — `rules.py` `label_monowaves`/`monowave_candidates`/`group_polywaves` | ~30–40% of monowaves forced corrective; flats indistinguishable from zigzags; Phase-3 labels have zero effect on Phase-4 grouping |
| **R7** | Two inconsistent Fib scoring fns in parallel (Gaussian `_fib_close` vs linear `_closeness`) | MED | 04 — wavetree vs automation | The two engines rank the same count differently |

---

## How they cascade (why fixing one isn't enough)

1. **R1 (log)** zeroes impulse Fibonacci quality → **R2** scoring then crowns
   corrections → "everything corrective".
2. **R5 (fixed-% zigzag)** never hands the DP a 5-node group spanning the full
   advance → even with R1/R2 fixed, the count can't *be* a Primary impulse, and the
   pivot set is degree-inconsistent (→ 98 monowaves, corrupted complexity counts).
3. **R3 (no coverage floor)** lets the DP keep a clean 30% sub-window → **R4**
   then measures degree on that fragment → "Minuette".
4. **R6** means even the NeoWave layer that *should* gate motive/corrective is
   inert and disagrees with Elliott.

These are coupled: a credible fix must address R1+R5 (foundation), then R2+R3+R4
(selection), then R6 (NeoWave), in that order.

---

## Fix plan (ordered by dependency; TDD — write the test first)

### Phase 1 — Foundation (measurement)
1. **Log lengths.** Add `Wave.log_length = abs(log(end.price/start.price))`; route
   all ratio/Fib/similarity/length comparisons through it (or a `use_log` flag set
   when series max/min > 2). Files: `rules.py` (`Wave`, `similarity_and_balance`),
   `wavetree.py` (`_impulse_quality`, `_correction_quality`, `_fib_close`),
   `automation.py` (`_fib_score`), `toolkit.py` (`wave_ratio`).
   _Test:_ a synthetic log-proportioned impulse must score Fib-quality ≈ 1.
2. **Volatility-scaled pivots.** Switch the count zigzag to ATR/log thresholds
   (`zigzag_causal(..., atr_n=…)`) so a swing means the same thing at $2 and $400;
   extend/repair the adaptive scale search (cap bug). Files: `toolkit.py`,
   `wave_report.py`/`wave_charts.py`. _Test:_ pivot count stable & degree-consistent
   across a 100× synthetic ramp.

### Phase 2 — Selection (impulse vs correction)
3. **Re-balance scoring:** IMPULSE bonus +0.5 → **+1.5**; `_correction_quality`
   ZIGZAG base 0.80 → **0.65**; add an `_alternating()`/hard-rule gate so corrective
   candidates face the same scrutiny as impulses. File: `wavetree.py`.
   _Test:_ a clean synthetic 5-wave impulse must out-rank any 3-wave parse of it.
4. **Coarser scales + more levels** so the full multi-decade advance is presented
   as a single 5-node group (add ~0.35/0.60 adaptive scales; `max_levels` 6→8–10).

### Phase 3 — Coverage & degree
5. **Coverage floor:** make the primary count span the series — gap penalty in the
   DP carry branch + a `min_coverage` requirement + a forced coarse full-range pass.
   File: `wavetree.py:wave_counts`/`_build_level`.
6. **Degree by relative magnitude across the FULL series**, and **extend the ladder**
   (Fibonacci-spaced thresholds → PRIMARY/CYCLE/SUPERCYCLE/GRAND_SUPERCYCLE reachable).
   File: `wavetree.py:anchored_degree`, `_anchored_from`.

### Phase 4 — NeoWave fidelity
7. **Carry candidates + apply m3/r01 sub-conditions** instead of `candidates[0]`;
   **add `:F3`** to Rule-3; **fix the Rule-3/4 overlap test** (crossing past
   `m0.start`, not band-containment); make **`group_polywaves` read the structure
   labels** (waves 1/3/5 must be motive, 2/4 corrective). File: `rules.py`.

### Cross-cutting
8. **Unify the two Fib scoring functions** (R7) so both engines agree.

---

## Validation plan (how we'll know it's fixed)

Re-run `scripts/wave_report.py AVGO MRVL` after each phase and check, against the
hand-read expectation:

- **Weekly count becomes a 5-wave IMPULSE at Primary/Cycle degree** (not a Minuette
  zigzag), with **coverage ≈ full series**.
- **MRVL 1W monowave count drops** from 98 to a degree-appropriate handful.
- **NeoWave `:5`/`:3` agree with Elliott** on the motive legs of the advance.
- Synthetic ground-truth tests (a known log-impulse, a known zigzag) label
  correctly and deterministically (per the repo's visual-first + TDD skills).

Only after the counts are theory-faithful does re-testing tradeability become
meaningful — the earlier "no edge" results were partly measuring a mis-applied
engine.
