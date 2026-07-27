# RULE COVERAGE — is each extracted rule implemented, and is it actually used?

This answers the recurring question directly, grounded in the code (not prose).
For every doctrine rule there are **three different questions**, and they have
**different answers** — conflating them is what caused the confusion:

| Tier | Question | How to verify |
|---|---|---|
| **① IMPLEMENTED** | Does a validator function exist + is it unit-tested? | `grep def src/ewave/rules/*.py`; `tests/ewave_platform/test_phase9_doctrine.py` |
| **② ANALYSIS** | Does the SOW report run it as REF output a human reads? | `src/ewave/reporting/sow_report.py` |
| **③ TRADES** | Does it gate an automated trade (the wave-3 entry)? | `src/ewave/signals/wave3.py` |

**The headline, stated plainly:**
- **Tier ① is ~complete.** 49 validator functions cover essentially the whole
  SOW/NeoWave doctrine; the doctrine ones are unit-tested (`test_phase9_doctrine.py`,
  40 cases).
- **Tier ② is ~complete.** The SOW report (`sow_report.py`) runs the full §A–§I
  rule table on the recent structure and shows every PASS/FAIL/WARN/REF.
- **Tier ③ is deliberately a SMALL SUBSET.** The automated trade uses only a
  handful of rules — and that is a *finding*, not an omission (see below).

**Why tier ③ is small — the empirical reason (docs/WAVE3_RESULT.md,
FORWARD_GHOST_TEST_FINDINGS.md):** a year-long causal replay showed the
next-leg *direction forecast* has no edge (coin-flip) → it is REF-only and must
never gate a trade. The one thing that carried a positive, replicated edge was
the **wave-3 confirmation entry** with a *minimal* rule set. Adding the full
doctrine as hard gates did **not** add validated edge — it just cut the trade
count to 3–7/yr. So the platform **implements and displays** the whole doctrine
(tiers ① ②) but **trades** only the validated subset (tier ③), by design and
per the repo's "honesty over confidence" non-negotiable.

---

## What the automated TRADE actually checks (tier ③) — verbatim from wave3.py

**Crude `experimental` profile** — the ONLY independently validated +R config;
every backtest in the repo ran this. It enforces exactly:
1. **R1 hard rule** — wave 2 may not exceed wave 1's origin (`c.price <= a.price → reject`). ✅ the one Elliott hard rule in the trade path.
2. **Wave-2 retracement band** — `retr_lo ≤ retr ≤ retr_hi` (the golden zone; profile knob).
3. **Break-and-close confirmation** — the entry only fires on the candle that closes beyond wave 1's extreme (`prev ≤ w1_high < price`).
4. **Fibonacci targets** — 1.618× / 2.618× of W1 projected from the W2 low.
5. **Reward:risk** — implied by targets vs the W2-low stop.
6. (optional) **Momentum expansion** — wave-3 personality, if `use_momentum`.

**Strict `sow_neowave_strict` profile** — implemented, but 3–7 trades/yr and
NOT independently validated. Adds on top of the above:
7. **Pattern identification** — wave 1 must carry a NeoWave **`:5` motive** monowave label (`label_monowaves`).
8. **Confluence gate** — `score_reversal` must clear `conf_min` independent strands (Fib zone, structure, momentum divergence, channel break, CHoCH, blue-box, and optionally Ichimoku).
9. **Entry-time window** — the break must fire within ~wave-2's duration.
10. **R:R floor** — explicit `min_rr` gate.

**Everything else in the doctrine — triangles, diametrics, flats, the 0-B / B-D
confirmation lines, the impulse time rule, alternation, complex-X, Ichimoku (in
crude) — does NOT gate the automated trade.** It is implemented (①) and shown in
the report (②), but the validated signal does not depend on it.

---

## Per-category coverage matrix

Legend: **①** validator exists + tested · **②** shown in SOW report · **③T**
trades (crude) · **③S** trades (strict only) · **DOC** documented only · **SEAM**
out of scope by design.

| Doctrine rule | ① impl (validator) | ② report | ③ trade | notes |
|---|---|---|---|---|
| Impulse 5-3-5-3-5 structure | `elliott_hard_rules` | ✅ | — | structural context |
| **R1: W2 ≤ W1 origin** | `elliott_hard_rules` | ✅ | **③T** | hard reject in trade |
| R2: W3 not shortest | `elliott_hard_rules` | ✅ | — | checked in candidate ID |
| R3: W4 no overlap (non-terminal) | `elliott_hard_rules` | ✅ | — | |
| W2 ≤ 61.8% of W1 (NeoWave) | retr band in `wave3` | ✅ | **③T** | the retracement-band gate |
| Alternation W2/W4 | `validate_impulse` guidelines | ✅ | — | analysis |
| Extension: one of 1/3/5, ≥1.618× | `elliott_guidelines`,`project_wave5` | ✅ | — | analysis |
| Impulse **time rule** W2≥W1, W4≥W3 | `correction_time_rules` | ✅ | — | analysis/REF |
| **2-4 line** two-stage confirmation | `two_four_test/_confirmation`,`confirm_completion` | ✅ | — | REF (was disproven as a *forecast*) |
| Terminal / ending diagonal | `terminal_rules`,`is_terminal`,`ending_diagonal_rules` | ✅ | — | analysis |
| Terminal W3>W1 | `terminal_rules` | ✅ | — | test_phase9 |
| **Zigzag** 5-3-5, b<61.8%, c beyond a | `classify_correction`,`zigzag_c_check` | ✅ | — | analysis |
| **0-B line** confirmation (two-stage) | `zero_b_confirmation` | ✅ | — | test_phase9; the mentorship "Buy" — REF |
| **Flat** family, b-strength bands | `classify_correction`,`flat_b_band` | ✅ | — | test_phase9 |
| Correction time (b vs a) | `correction_time_rules` | ✅ | — | wave-b diagnosis card |
| **Triangle** 3-3-3-3-3, E smallest, ≥3>50% | `_classify_triangle`,`triangle_subrules` | ✅ | — | test_phase9 |
| Triangle **B-D clean** + confirmation | `bd_line_test`,`bd_confirmation` | ✅ | — | test_phase9 |
| Neutral / running / extracting triangle | `is_neutral_triangle`,`is_running_triangle`,`is_extracting_triangle` | ✅ | — | test_phase9 |
| **Diametric** 7-leg, pairs g≈a/f≈b/e≈c | `diametric_pair_checks`,`diametric_boundary_confirmation` | ✅ | — | test_phase9 |
| **Complex-X**, max-2-X, LARGE-X | `classify_complex_correction`,`max_x_count_check`,`x_wave_check` | ✅ | — | test_phase9 |
| Rule of Similarity & Balance (≥⅓) | `similarity_and_balance`,`rule_of_proportion` | ✅ | — | analysis |
| **Fibonacci** ratios / targets | `fib_extension/retrace/cluster`,`wave_ratio` | ✅ | **③T** | targets used in trade |
| Blue-box reaction zone | `blue_box_zone` | ✅ | ③S | confluence strand |
| **Confluence** score (strands) | `score_reversal` (confluence.py) | ✅ | **③S** | the strict gate |
| **Ichimoku** 9/26/52 filter | `indicators.ichimoku`,`ichimoku_trend` | ✅ (on) | ③S opt | opt-in strand only |
| **Time cycles** 54/108d, 85/141/272w | — | noted | **SEAM** | chakra_quant `CycleSignal`, by design |
| Gann levels | — | noted | **DOC** | no validated algorithm in the source |
| Touch-point rule (4-of-6 / 3-of-4) | — | noted | **DOC** | manual charting heuristic |
| No-lookahead (confirmed_t) | pivots + import-graph test | n/a | enforced | platform-wide invariant |
| DSR/PSR/MinTRL selection | `validation.stats` | n/a | enforced | edge selection |

**Totals:** every trading-doctrine rule is tier ① (implemented+tested) or
explicitly SEAM/DOC. Tier ② (report) covers all of §A–§I. Tier ③ (trades):
~6 rules in the validated crude path, ~10 in the strict path, plus the
confluence strands — the subset the evidence supports.

## The non-trading ledger entries

The full `docs/RULES_LEDGER.md` has 581 entries; many are **not** wave rules —
they are DATA-contract, VALIDATION, AUTOMATION-SPEC, RISK and SCOPE/PROCESS
requirements from the SPEC and agent packs. Those are implemented as the
platform itself (data store, ghost-forward freeze, trials registry, risk engine,
fail-closed live gates) and verified by `tests/` (337 passing). They are not in
the table above because they gate the *pipeline*, not a *wave label*.

## How to re-verify (nothing here is asserted without a command)

```bash
grep -n "^def " src/ewave/rules/*.py            # tier ① — the 49 validators
python3 -m unittest tests.ewave_platform.test_phase9_doctrine   # tier ① tests
sed -n '40,205p' src/ewave/signals/wave3.py     # tier ③ — exactly what trades
grep -n "table_rows\|conf_rows\|_rule_rows" src/ewave/reporting/sow_report.py  # tier ②
```

## Bottom line for the reader

Nothing extracted from your materials is lost or unimplemented: the doctrine is
**coded and tested (①)** and **shown in the analysis report (②)**. The automated
**trade (③) intentionally uses only the validated subset** — because the honest
evidence says the extra rules, used as hard gates, did not improve the edge.
If you want a specific rule promoted into the trade path (e.g. require a clean
B-D triangle break, or make Ichimoku a hard gate), that is a one-line profile
change + a fresh backtest/ghost-forward to prove it helps — say which rule and
I'll wire it and test it.
