# RULES LEDGER — every rule, setup & explanation from the shared docs

_Single canonical registry so nothing from any shared document is lost._ Assembled by `scripts/build_rules_ledger.py` from agent extractions of the full bundle (SOW instructor materials, the md/TradingView-playbook pack, the research-validation pack, the automation SPEC + agent-prompt packs, and the legacy/audit packs) merged with the page-cited PDF notes in `docs/research/sow_deep_read/`. Exact-duplicate rules are merged (sources unioned); near-duplicates are kept because they usually carry different specific numbers.

**394 distinct rule entries** across 20 categories. Where a rule is enforced in code, the RULESET section / validator is named in `docs/research/SOW_METHOD.md` (compliance matrix) and drawn in `docs/atlas/SOW_PATTERN_ATLAS.html`.

## Contents

- **IMP** — Impulse (motive) waves (32)
- **TRM** — Terminal impulse / ending diagonal (13)
- **ZZ** — Zigzag corrections (12)
- **FLT** — Flat corrections (9)
- **TRI** — Triangles (contracting / expanding / neutral / extracting) (19)
- **DIA** — Diametric & symmetrical formations (8)
- **CX** — Complex corrections & X-waves (11)
- **CNF** — Confirmation lines & two-stage confirmation (9)
- **FIB** — Fibonacci relationships (24)
- **TIM** — Wave time rules (7)
- **CYC** — Time cycles (Kaal Chakra / Hurst) (1)
- **ICH** — Ichimoku Cloud (4)
- **IND** — Other indicators (5)
- **SET** — Trade setups & execution (12)
- **RSK** — Risk & money management (4)
- **MTH** — Analysis method & order of operations (79)
- **DAT** — Data contract & preparation (35)
- **VAL** — Validation, backtesting & selection (54)
- **AUT** — Automation / engineering specs (38)
- **SCP** — Scope, exclusions & policy (18)


## IMP · Impulse (motive) waves

### IMP-01 — five-segment 5-3-5-3-5 structure
- **Rule:** An impulse is a five-segment trend structure, generally 5-3-5-3-5 internally; waves 1, 3, 5 thrust in the impulse direction, waves 2 and 4 correct waves 1 and 3 respectively.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules) · mdpack
- **Notes:** Same statement in 01_WAVE_RULES_REFERENCE.md §Impulse rule sheet and training deck p.17 (rules 1-2).

### IMP-02 — wave 2 retracement limit 61.8%
- **Rule:** Wave 2 should not retrace more than 61.8% of wave 1 (NeoWave rule set used in these notes). Deck wording: "End point of Wave 2 cannot retrace more than 61.8% of wave 1."
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 17 rule 3) · mdpack

### IMP-03 — wave 3 never the shortest
- **Rule:** Wave 3 cannot be "the" shortest of waves 1, 3, and 5.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also deck Page 17 rule 4 · mdpack

### IMP-04 — rule of overlap
- **Rule:** Wave 4 should not enter the price area covered by wave 2, except in a terminal impulse / diagonal — Rule of Overlap.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also deck Page 17 rule 5 · mdpack
- **Notes:** Composite notes add: if overlap appears, consider terminal/diagonal or relabel (Brahmastra_Mentorship_Day_5_6_EW_Composite.md Page 2).

### IMP-05 — rule of alternation
- **Rule:** Waves 2 and 4 should alternate in price, time, severity, intricacy, construction (pattern type) — Rule of Alternation.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 18 rule 6 · mdpack

### IMP-06 — extension rule — only one extends
- **Rule:** Only one among waves 1, 3, or 5 can extend (normally extends) — Extension rule.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 18 rule 10 · mdpack

### IMP-07 — extended wave >= 1.618x next longest
- **Rule:** The extended wave should be at least 1.618 times the next longest impulse wave — Extension rule.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 11 · mdpack

### IMP-08 — rule of equality
- **Rule:** The two unextended impulse waves tend toward equality — Rule of Equality.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 12 · mdpack

### IMP-09 — fifth-wave failure
- **Rule:** A fifth-wave (5th) failure is possible, especially when wave 3 is already an extended wave.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 13 · mdpack

### IMP-10 — 0-2 line rule
- **Rule:** No part of wave 1 or wave 3 should break the 0-2 line.
- **Type:** hard
- **Source:** 01_WAVE_RULES_REFERENCE.md (§Impulse rule sheet); deck Page 18 rule 7 · mdpack
- **Notes:** 0-2 line drawn from start of wave 1 (point 0) through end of wave 2; invalid examples show breaks or poor placement (Sutra_of_Waves_Day_1_Notes2.md Page 5).

### IMP-11 — 2-4 line integrity (Neely confirmation rule)
- **Rule:** No part of wave 3 or wave 5 should break the 2-4 line, except in terminal impulse — Neely's Confirmation Rule.
- **Type:** hard
- **Source:** 01_WAVE_RULES_REFERENCE.md (§Impulse rule sheet); deck Page 18 rule 8 · mdpack

### IMP-12 — Neely touch-point rule for impulse (4 of 6)
- **Rule:** Only 4 (out of possible 6) touch-points should touch the two opposing trend lines — Neely's Touch Point Rule.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 19 rule 14) · mdpack

### IMP-13 — common impulse invalidations
- **Rule:** Invalidate the impulse when: wave 2 fully destroys wave 1 beyond the allowed retracement rule; wave 3 is the shortest impulse wave; wave 4 overlaps wave 2 in a normal impulse; wave 5 does not confirm and the 2-4 line remains intact for too long.
- **Type:** validation
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Common invalidations) · mdpack

### IMP-14 — wave 2 cannot retrace beyond completion of wave 1
- **Rule:** Wave 2 should not retrace beyond completion (origin) of wave 1.
- **Type:** hard
- **Source:** 04_source_page_conversions/Brahmastra_Mentorship_Day_5_6_EW_Composite.md (§Page 2) · mdpack
- **Notes:** Composite examples show wave sequences, failures, and a similarity indicator (image-based).

### IMP-15 — alternation worked example
- **Rule:** Alternation example: compare wave 2 and wave 4 by retracement, price, time, pattern, and complexity; wave 2 retracement shown near 61.8% of wave 1; wave 4 retracement example around 38.2% of wave 1+3.
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 6) · mdpack

### IMP-16 — impulse structure rules
- **Rule:** 1-2-3-4-5; internal structure approximation 5-3-5-3-5; Waves 1, 3, and 5 move in impulse direction; Waves 2 and 4 correct waves 1 and 3; Wave 2 cannot retrace more than 61.8% of Wave 1; Wave 3 cannot be the shortest among 1, 3, and 5; Wave 4 should not overlap Wave 1 except terminal impulse; Wave 2 and Wave 4 should alternate; only one of 1, 3, or 5 should extend; extended wave should be at least 1.618x of the next longest.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Impulse Structure) · specs
- **Notes:** Implement impulse only after corrective modules and mono-wave engine are stable.

### IMP-17 — impulse validator checks
- **Rule:** 1. Evaluate five mono-waves as 1-2-3-4-5. 2. Check Wave 2 retracement <= 61.8%. 3. Check Wave 3 is not shortest. 4. Check Wave 4 overlap rule. 5. Check extension and equality rules. 6. Return structured rule results and score.
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Codex / Claude Prompt) · specs

### IMP-18 — motive-waves-five-wave-with-trend
- **Rule:** Motive waves are five-wave structures moving in the direction of the larger trend.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves) · validation
- **Notes:** Listed under "Confirmed concepts" as safe to convert into V1 automation specs.

### IMP-19 — wave2-retrace-less-than-100pct
- **Rule:** Wave 2 retraces less than 100% of wave 1.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves) · validation
- **Notes:** Encoded in V1 yaml as `wave2_retrace_must_be_less_than_pct: 100` under profile `classic_elliott`.

### IMP-20 — wave4-retrace-less-than-100pct-of-wave3
- **Rule:** Wave 4 retraces less than 100% of wave 3.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves) · validation
- **Notes:** Encoded as `wave4_retrace_must_be_less_than_pct_of_wave3: 100`.

### IMP-21 — wave3-exceeds-wave1
- **Rule:** Wave 3 travels beyond wave 1 (`wave3_must_exceed_wave1_end: true`).
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves) · validation

### IMP-22 — wave3-never-shortest
- **Rule:** Wave 3 is never the shortest among waves 1, 3, and 5 (`wave3_must_not_be_shortest_among_1_3_5: true`).
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves) · validation
- **Notes:** Reaffirmed as RD-003 "Implement as hard rule in impulse validator", risk High.

### IMP-23 — impulse-structure-5-3-5-3-5-no-overlap
- **Rule:** An impulse is a five-wave motive pattern with 5-3-5-3-5 internal structure; normal impulses should not have wave 4 overlap wave 1 (`normal_impulse_wave4_wave1_overlap_allowed: false`). Diagonal or terminal variants must be handled separately.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Impulse, §Hard rules for V1) · validation

### IMP-24 — soft-rules-alternation-fib-channeling
- **Rule:** Soft rules for scoring only: `alternation_between_wave2_and_wave4: score_only`, `fibonacci_relationships: score_only`, `channeling: score_or_annotation`.
- **Type:** guideline
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Soft rules for scoring) · validation

### IMP-25 — sow-strict-wave2-61.8
- **Rule:** SOW/NeoWave strict profile: wave 2 retracement limit `wave2_retrace_must_be_less_or_equal_pct: 61.8` (i.e. <=61.8% of wave 1). Must NOT overwrite the classical 100% profile — it is a separate profile `sow_neowave_strict`.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Conflict with SOW/NeoWave strict rules) · validation
- **Notes:** The SOW notes use stricter impulse rules; keeping both avoids forcing one interpretation across all modules.

### IMP-26 — feasibility-basic-impulse
- **Rule:** Basic impulse: difficulty Medium/High, V1 status Implement after mono-wave metrics — requires internal structure and overlap/extension validation.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### IMP-27 — master-pattern-structure-summary
- **Rule:** Stable classical structure: motive waves move with the larger trend in five waves; corrective waves are generally three-wave or variations; impulse is 5-3-5-3-5 with normally no overlap between wave 4 and wave 1; zigzag is A-B-C subdividing 5-3-5; flat is A-B-C subdividing 3-3-5; triangle is A-B-C-D-E subdividing 3-3-3-3-3.
- **Type:** hard
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§1. Classical Elliott Wave core rules are stable enough for V1) · validation
- **Notes:** Engineering decision: implement classical Elliott rules as formal rule profile `classic_elliott`.

### IMP-28 — wave2-profile-split-100-vs-61.8
- **Rule:** `rule_profiles: classic_elliott: wave2_max_retrace_pct_of_wave1: 100; sow_neowave_strict: wave2_max_retrace_pct_of_wave1: 61.8`.
- **Type:** hard
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§2. SOW / NeoWave rules need a stricter and separate rule profile) · validation
- **Notes:** SOW/NeoWave course notes are stricter on retracement, time, confirmation lines, touch points, and pattern balance; do not merge blindly with classical Elliott Wave. Engineering decision: create profile `sow_neowave_strict`. Same split repeated in 02_SOURCE_QUALITY_POLICY.md (§Example conflict: Wave 2 retracement).

### IMP-29 — wave2-conflict-example
- **Rule:** Classical Elliott Wave sources commonly state wave 2 must not retrace 100% or more of wave 1; SOW/NeoWave course material uses a stricter 61.8% rule. Decision: `classic_elliott: wave2_max_retrace_pct_of_wave1: 100; sow_neowave_strict: wave2_max_retrace_pct_of_wave1: 61.8`.
- **Type:** hard
- **Source:** 02_SOURCE_QUALITY_POLICY.md (§Example conflict: Wave 2 retracement) · validation
- **Notes:** "This avoids forcing one interpretation across all modules."

### IMP-30 — RD-002-wave2-retracement
- **Rule:** RD-002: Classical profile uses `<100%`; SOW/NeoWave strict profile uses `<=61.8%` for wave 2 retracement. Hard/profile-specific, Accepted, impulse validator, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### IMP-31 — RD-003-wave3-not-shortest
- **Rule:** RD-003: Wave 3 not shortest — implement as hard rule in impulse validator. Accepted, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### IMP-32 — RD-005-alternation-soft
- **Rule:** RD-005: Treat alternation as guideline/score, not hard invalidation. Soft, Accepted, pattern scoring, risk Medium.
- **Type:** guideline
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## TRM · Terminal impulse / ending diagonal

### TRM-01 — terminal impulse location
- **Rule:** Terminal impulse / ending diagonal appears mainly (Day 1 notes: can form only) in wave 5 or wave C.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5) · mdpack

### TRM-02 — terminal internal structure 3-3-3-3-3
- **Rule:** Terminal impulse internal form is corrective-looking, commonly 3-3-3-3-3, and the structure often forms a wedge.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal) · mdpack

### TRM-03 — wave 4 overlap allowed
- **Rule:** In a terminal impulse, wave 4 may enter the area of wave 1 (overlap allowed).
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); Day 1 Notes Page 5 · mdpack

### TRM-04 — wave 2 may retrace more than 61.8%
- **Rule:** In a terminal impulse, wave 2 can retrace more deeply than a normal impulse — Day 1 notes: wave 2 can retrace more than 61.8% of wave 1.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal) · mdpack

### TRM-05 — wave 3 must still exceed wave 1
- **Rule:** In a terminal impulse, wave 3 should still move beyond wave 1.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); Day 1 Notes Page 5 · mdpack

### TRM-06 — time rules relaxed in terminal
- **Rule:** Time rules are less strict for terminal impulse; Day 1 notes: "Time rule is not necessary in this special structure."
- **Type:** time
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 01_WAVE_RULES_REFERENCE.md (§Terminal impulse rule sheet) · mdpack

### TRM-07 — treat terminal as confirmation-required setup
- **Rule:** Treat terminal impulse as a terminal setup: wait for confirmation, because reversals can be sharp; confirmation is required — do not pre-empt terminal reversal.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 01_WAVE_RULES_REFERENCE.md (§Terminal impulse rule sheet) · mdpack

### TRM-08 — terminal TradingView workflow
- **Rule:** 1) draw wedge boundaries through waves 1-3 and 2-4; 2) check internal legs look corrective not clean impulses; 3) wait for a decisive wedge/2-4 break before acting; 4) invalidation is usually a failed wedge break or continuation beyond the terminal count.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal / TradingView workflow) · mdpack

### TRM-09 — 3rd extension terminal exists
- **Rule:** A "3rd extension terminal" variant is presented in the deck (page heading only; rule content is in the page image).
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 53) · mdpack
- **Notes:** Image carries the pattern definition; unreadable in text extraction.

### TRM-10 — terminal impulse exception flag
- **Rule:** Wave 4 overlap of Wave 1 is allowed only for terminal impulse; the impulse validator must mark the terminal exception separately ("Do not implement terminal impulse yet except as an exception flag").
- **Type:** guideline
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Impulse Structure / Forbidden) · specs

### TRM-11 — feasibility-terminal-diagonal
- **Rule:** Terminal impulse / diagonal: difficulty High, V1 status V2 or warning — needs exception handling for overlap.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### TRM-12 — RD-004-wave4-overlap-exception
- **Rule:** RD-004: In `classic_elliott`, non-overlap of wave 4 with wave 1 is hard for normal impulse; allow exception only in diagonal/terminal module. Hard with exception, Accepted, impulse/terminal modules, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### TRM-13 — wave4-overlap-fail-except-terminal
- **Rule:** `classic_elliott: wave4_overlap_wave1: fail`; `sow_neowave_strict: wave4_overlap_wave1: fail_except_terminal` — overlap of wave 4 into wave 1 fails validation except in the terminal-impulse case for the strict profile.
- **Type:** hard
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md) · validation


## ZZ · Zigzag corrections

### ZZ-01 — zigzag structure 5-3-5
- **Rule:** A zigzag is a sharp corrective pattern: A-B-C, internally 5-3-5 (3 segments).
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32 · mdpack

### ZZ-02 — B less than 61.8% of A
- **Rule:** Zigzag wave B should be less than 61.8% of A; it can be very shallow — deck: "B could be even 1% of A."
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Pages 32-33 · mdpack
- **Notes:** Day 2 Notes Page 2 words it as "B wave should be less than or equal to 61.8% of A."

### ZZ-03 — C must move beyond end of A
- **Rule:** Zigzag wave C should move beyond the end of A.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32 · mdpack

### ZZ-04 — Neely touch-point rule for zigzag (3 of 4)
- **Rule:** Only 3 (out of possible 4) touch points should touch the parallel trend lines/channel — Neely's Touch Point rule.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules) · mdpack

### ZZ-05 — only three basic standard correctives
- **Rule:** There are only 3 basic types of standard correctives: 1) Zigzag (5-3-5), 2) Flat (3-3-5), 3) Triangle (3-3-3-3-3).
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 31) · mdpack

### ZZ-06 — zigzag structure rules
- **Rule:** A-B-C; internal structure approximation 5-3-5; B retracement: less than 61.8% of A; C should move beyond end of A; Wave B should take same or more time than A; 0-B line break confirms completion.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 6 Zigzag Structure) · specs
- **Notes:** Candidate input = three mono-waves (A = wave 1, B = wave 2, C = wave 3). Output: Possible Zigzag, confidence score, rule results, invalidation level, confirmation line, TradingView drawing instruction.

### ZZ-07 — zigzag module implementation checks
- **Rule:** 1. Evaluate three mono-waves as A-B-C. 2. Check B < 61.8% of A. 3. Check C beyond A. 4. Check time rule for B vs A. 5. Return structured rule results and score. 6. Generate manual TradingView note.
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 6 Codex / Claude Prompt) · specs
- **Notes:** Zigzag is Pattern Module 1 — implemented first; Flat/Triangle/Impulse forbidden in that task.

### ZZ-08 — zigzag-structure-5-3-5
- **Rule:** Zigzag is a corrective pattern subdividing 5-3-5.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves) · validation

### ZZ-09 — example-zigzag-study-plan
- **Rule:** Example zigzag correction workflow (TSLA 1H, sow_neowave_strict): mark pivots 0, A, B; draw 0-B line; draw Fibonacci projection of A from B; watch C zone near 1.0x to 1.618x of A; do not treat C as complete until reversal/pivot confirmation.
- **Type:** setup
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§Example output) · validation
- **Notes:** Example lists confirmed pivots with pivot and confirmed timestamps (e.g. Pivot 0: 2026-04-01 10:00, confirmed 2026-04-01 13:00) and warning "Pivot C is not confirmed yet. Do not backtest entry at C pivot candle."

### ZZ-10 — zigzag-bearish-invalidation
- **Rule:** Candidate invalid if price breaks above B before C completion in a bearish setup.
- **Type:** setup
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§Example output / Invalidation) · validation

### ZZ-11 — feasibility-zigzag
- **Rule:** Zigzag: difficulty Medium, V1 status Implement — clear A-B-C structure; good first corrective module.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### ZZ-12 — RD-007-zigzag-first-detector
- **Rule:** RD-007: Implement first corrective detector: A-B-C, 5-3-5 approximation, B retracement profile, C target zone. Pattern V1, Accepted, corrective detector, risk Medium.
- **Type:** setup
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## FLT · Flat corrections

### FLT-01 — flat structure 3-3-5
- **Rule:** A flat is a sideways or broad correction: A-B-C, internally 3-3-5.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34 · mdpack

### FLT-02 — B more than 61.8% of A
- **Rule:** In a flat, B should be (retrace) more than 61.8% of A.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34 · mdpack

### FLT-03 — Neely touch-point rule for flat (3 of 4)
- **Rule:** Only 3 (out of possible 4) touch points should touch the parallel trend lines/channel — Neely's Touch Point rule (flat).
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 35); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules) · mdpack

### FLT-04 — flat variants
- **Rule:** Variants: Regular flat — B retraces about 61.8% to 100% of A, often weak B. Irregular / expanded flat — B exceeds the start of A (B > 100% of A, strong B); C can be strong. C-failure flat — C fails to move beyond A, often shows underlying strength in the opposite direction. Running flat — B is strong and C is shallow; continuation risk is high. Day 2 notes also show a double-failure flat.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules / Flat variants to watch); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 3) · mdpack

### FLT-05 — flat structure rules
- **Rule:** A-B-C; internal structure approximation 3-3-5; B retracement: more than 61.8% of A; C relates to A price-wise or A+B time-wise; 0-B line break confirms completion; Wave B should take same or more time than A.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 7 Flat Structure) · specs

### FLT-06 — flat variants
- **Rule:** Variants: Regular Flat, Irregular Flat, Running Flat, C Failure Flat, Double Failure Flat. Detector must classify broad variant when possible and return warning when ambiguous.
- **Type:** guideline
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 7 Flat Variants / Acceptance Criteria) · specs

### FLT-07 — flat-structure-3-3-5
- **Rule:** Flat is a corrective pattern subdividing 3-3-5.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves) · validation

### FLT-08 — feasibility-flat
- **Rule:** Flat: difficulty Medium, V1 status Implement after zigzag — clear A-B-C 3-3-5 structure but variants require caution.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### FLT-09 — RD-008-flat-after-zigzag
- **Rule:** RD-008: Implement flat after zigzag: A-B-C, 3-3-5 approximation, B near/beyond A start. Running flat must be warning/manual-review. Pattern V1, Accepted, risk Medium.
- **Type:** setup
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## TRI · Triangles (contracting / expanding / neutral / extracting)

### TRI-01 — triangle structure 3-3-3-3-3
- **Rule:** A triangle is a five-leg corrective pattern A-B-C-D-E, internally 3-3-3-3-3; each segment/leg is a complete corrective.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); deck Page 36 · mdpack

### TRI-02 — triangle cannot form in wave 2
- **Rule:** A standard triangle should not / cannot form in wave 2, except special terminal contexts (terminal impulse).
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4) · mdpack

### TRI-03 — triangle drift and leg sizes
- **Rule:** A triangle can drift upward or downward; A does not have to be the largest leg; E must be (should usually be) the smallest.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 36); 01_WAVE_RULES_REFERENCE.md (§Triangle rule sheet) · mdpack

### TRI-04 — retracement depth of legs
- **Rule:** At least 3 segments/legs should correct more than 50% of the previous segment.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules) · mdpack

### TRI-05 — Neely touch-point rule for triangle (4 of 6)
- **Rule:** Only 4 (out of possible 6) touch points should touch the two opposing trend lines — Neely's Touch Point Rule (triangle).
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37) · mdpack

### TRI-06 — B-D baseline must be clean
- **Rule:** B-D is the base line and it should be clean; no part of wave C or E should prematurely break the B-D trendline.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4) · mdpack

### TRI-07 — opposite boundary line selection
- **Rule:** Draw the A-C line when C is shorter than B; draw the C-E line on the other side when C is bigger than B.
- **Type:** process
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules) · mdpack

### TRI-08 — widest-leg relationship 100%-125%
- **Rule:** Widest leg relationship noted around 100% to 125% (of the adjacent leg) in the triangle sketches.
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4) · mdpack
- **Notes:** From handwritten sketch; irregular triangle variations also shown on the same page image.

### TRI-09 — triangle TradingView workflow
- **Rule:** 1) mark A-B-C-D-E; 2) draw the B-D line first; 3) draw the opposite boundary using A-C or C-E depending on leg size; 4) do not trade inside the triangle unless doing short-term range trading; 5) wait for B-D break confirmation; 6) the first move after the triangle break is often the tradeable move.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules / TradingView workflow) · mdpack

### TRI-10 — extracting triangle behavior
- **Rule:** Extracting triangle shows alternating expansion/contraction behavior; label A-B-C-D-E; watch whether one side expands while the other contracts; the final E leg often appears small relative to earlier legs; trade only after boundary confirmation, not while internal legs are forming.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Extracting and neutral triangles / Extracting triangle) · mdpack
- **Notes:** Day 2 Notes Page 5 schematic gives: e < c < a and d > b.

### TRI-11 — neutral triangle characteristics
- **Rule:** A neutral triangle differs from a simple contracting triangle: wave C can be the longest wave in the direction of the trend (the most powerful or longest internal leg); D can be the longest leg against the trend; confirmation still comes from the boundary break. Use it when normal triangle proportions do not fit but the five-leg corrective logic remains valid.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Extracting and neutral triangles / Neutral triangle) · mdpack
- **Notes:** Also headed "NUETRAL TRIANGLE" on deck Page 52 (image-based) and sketched in Day 2 Notes Page 5 ("C often powerful").

### TRI-12 — expanding triangle fingerprint
- **Rule:** Expanding triangle shows spikes at extremes ("EXPANDING TRIANGLE (SPIKES AT EXTREMES)").
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 72) · mdpack
- **Notes:** Heading only; details are in the page image.

### TRI-13 — limiting vs non-limiting triangles
- **Rule:** Pattern implication categories distinguish Limiting Triangle from Non-limiting Triangle (each completed pattern implies extent of the next action).
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 46) · mdpack

### TRI-14 — triangle structure rules
- **Rule:** A-B-C-D-E; internal structure approximation 3-3-3-3-3; each segment is corrective; triangle can drift upward or downward; E should often be smallest; at least three segments should retrace more than 50% of previous segment; B-D line is the base line and should be clean; triangle is confirmed when B-D line breaks in equal or lesser time than E.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 9 Triangle Structure) · specs
- **Notes:** Acceptance: evaluate five mono-waves as triangle candidate; produce trendline instructions; identify B-D confirmation line.

### TRI-15 — triangle-structure-3-3-3-3-3
- **Rule:** Triangle is a corrective pattern subdividing 3-3-3-3-3.
- **Type:** hard
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves) · validation

### TRI-16 — feasibility-triangle
- **Rule:** Triangle: difficulty High, V1 status Candidate/manual review — easy to label too early; requires time and boundaries.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### TRI-17 — feasibility-neutral-triangle
- **Rule:** Neutral triangle: difficulty Very high, V1 status V2/manual review — requires stricter NeoWave logic.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### TRI-18 — feasibility-extracting-triangle
- **Rule:** Extracting triangle: difficulty Very high, V1 status V2/manual review — requires mature triangle engine.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### TRI-19 — RD-009-triangle-manual-review
- **Rule:** RD-009: Implement triangle as candidate/manual-review in V1; full triangle confirmation later. Manual-review, Accepted, triangle detector, risk High.
- **Type:** scope
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## DIA · Diametric & symmetrical formations

### DIA-01 — seven-leg structure
- **Rule:** A diametric is a seven-leg corrective structure A-B-C-D-E-F-G, internally 3-3-3-3-3-3-3 (each leg corrective), often described as a bow-tie, diamond, or running diametric; it can also run in the direction of the larger trend.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern); 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet) · mdpack

### DIA-02 — paired-leg relationships G~A, F~B, E~C
- **Rule:** G approximately relates to A; F approximately relates to B; E approximately relates to C — by price or time. Fibo-system note: G≈A or G≈61.8%A; F≈B by price or time; E≈C by price or time.
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1) · mdpack
- **Notes:** Day 2 Notes Page 6 shows g≈a, f≈b, e≈c on sketches.

### DIA-03 — do not force triangle when seven legs visible
- **Rule:** Do not force a five-leg triangle (ABCDE) label if seven legs are clearly visible.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow); 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet) · mdpack

### DIA-04 — diametric confirmation after G
- **Rule:** Wait for G completion and a boundary break for confirmation; confirmation after G is more important than predicting G early.
- **Type:** hard
- **Source:** 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow) · mdpack

### DIA-05 — diametric TradingView workflow
- **Rule:** 1) mark seven legs A through G; 2) draw boundaries around the shape; 3) check whether the pattern is symmetrical in price or time; 4) do not force a five-leg triangle label; 5) wait for G completion and a boundary break.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow) · mdpack

### DIA-06 — diametric Fibonacci relationships
- **Rule:** G often relates to A; F often relates to B; E often relates to C.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Diametric) · specs

### DIA-07 — feasibility-diametric
- **Rule:** Diametric: difficulty Very high, V1 status V2/manual review — NeoWave-specific and interpretive.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### DIA-08 — RD-010-advanced-neowave-v2
- **Rule:** RD-010: Diametric, neutral triangle, extracting triangle, and complex correction are V2 unless only annotated manually. Postpone, Accepted, NeoWave modules, risk High.
- **Type:** scope
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## CX · Complex corrections & X-waves

### CX-01 — zigzag C ending on channel warns of complex correction
- **Rule:** If C ends exactly on the parallel channel (and confirmation is weak), development of a complex corrective involving an "x" wave is possible.
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules) · mdpack

### CX-02 — flat C ending on channel warns of X-wave combination
- **Rule:** If flat C ends on the parallel channel (and confirmation is weak), development of a complex corrective involving an "x" wave / X-wave combination is possible.
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 35); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules) · mdpack

### CX-03 — complex correction forms
- **Rule:** Complex corrections connect two or three corrective patterns using X waves. Forms: W-X-Y, W-X-Y-X-Z, double zigzag, triple zigzag, zigzag-X-flat, zigzag-X-flat-X-triangle.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 7) · mdpack

### CX-04 — maximum two X waves
- **Rule:** Maximum allowed: two X waves in a complex correction.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); Day 2 Notes Page 7; 01_WAVE_RULES_REFERENCE.md · mdpack

### CX-05 — X-wave nature
- **Rule:** X can be a mono-wave or a corrective pattern; X connects still-corrective patterns/structures.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 01_WAVE_RULES_REFERENCE.md (§Complex correction rule sheet) · mdpack

### CX-06 — large X wave means relabel
- **Rule:** If X becomes unusually large, reassess the degree and count. Example threshold: if X exceeds/becomes greater than 1.618 times W, the structure is no longer a small connector — reassess degree and relabel.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 8) · mdpack

### CX-07 — failed ABC confirmation is the first clue
- **Rule:** A failed ABC confirmation is often the first clue that a complex correction is forming; if a supposed correction keeps extending without confirmation, avoid forcing a completed pattern.
- **Type:** guideline
- **Source:** 01_WAVE_RULES_REFERENCE.md (§Complex correction rule sheet); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections) · mdpack

### CX-08 — complex correction TradingView workflow
- **Rule:** 1) first try to label a simple ABC; 2) if confirmation fails, mark the next connector as X; 3) start the next corrective pattern after X; 4) use the same confirmation-line rules for each component pattern; 5) avoid trading the middle of W-X-Y unless a lower timeframe setup is independently clear.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections / TradingView workflow) · mdpack

### CX-09 — advanced NeoWave pattern set and order
- **Rule:** Advanced patterns: Terminal Impulse, Diametric, Complex Correction, Double Combination, Triple Combination, Neutral Triangle, Extracting Triangle, Running Diametric. Implement as separate modules, not mixed into core impulse/corrective modules. Recommended order: 1. Terminal impulse 2. Diametric 3. Complex correction with X-wave 4. Neutral triangle 5. Extracting triangle 6. Double / triple combinations. Only begin after the core engine is stable.
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 10 Advanced NeoWave Patterns) · specs

### CX-10 — combination-double-triple
- **Rule:** Combination = double/triple corrective structures (a primary corrective category alongside zigzag, flat, triangle).
- **Type:** guideline
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves) · validation

### CX-11 — feasibility-double-triple-combination
- **Rule:** Double/triple combination: difficulty High, V1 status V2 — requires reliable recognition of multiple sub-patterns.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation


## CNF · Confirmation lines & two-stage confirmation

### CNF-01 — impulse confirmation: 2-4 line break within wave-5 time
- **Rule:** After wave 5, the 2-4 line should be cut/broken in equal or lesser time than wave 5 took — Neely's Rule of Confirmation.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 15; 01_WAVE_RULES_REFERENCE.md · mdpack

### CNF-02 — zigzag 0-B confirmation
- **Rule:** The 0-B line should be broken in equal or lesser time period than that of C — Neely's Rule of Confirmation for zigzag.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules) · mdpack
- **Notes:** Day 2 Notes Page 2: first-stage confirmation = break of 0-B trendline within the required time window; notes mention <=10 days as an example for stage timing.

### CNF-03 — flat 0-B confirmation
- **Rule:** In a flat, the 0-B line should be broken in equal or lesser time period than that of C — Neely's Rule of Confirmation.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 34); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules) · mdpack

### CNF-04 — triangle B-D confirmation
- **Rule:** Triangle is over/complete when the B-D line gets broken in equal or lesser time period than that of wave E — Neely's Rule of Confirmation.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules) · mdpack

### CNF-05 — two-stage confirmation — stage 1 structure lines
- **Rule:** Stage 1 structure-line confirmation: impulse — break of 2-4 line after wave 5; zigzag/flat — break of 0-B line after C; triangle — break of B-D line after E; diametric — break of boundary after G; complex correction — confirmation of the final component pattern.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Two-stage confirmation / Stage 1); 02_PATTERN_DECISION_TREE.md (§Step 7); 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Confirmation lines) · mdpack

### CNF-06 — two-stage confirmation — stage 2 price action
- **Rule:** Stage 2: after the structure-line break, price should also move beyond the nearest important swing level; hold above/below the broken line on retest when possible; align with Ichimoku direction if using the cloud filter; show acceptable reward/risk from the entry zone.
- **Type:** hard
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Two-stage confirmation / Stage 2) · mdpack
- **Notes:** Day 1 Notes Page 4: stage 1 is line-break confirmation (2-4 trendline with time window); stage 2 is price/action confirmation beyond the next level. Deck Page 38 heading "2 STAGE CONFIRMATION" (details in image).

### CNF-07 — never trade before the correct line breaks
- **Rule:** Never treat a count as tradeable until the correct confirmation line is broken.
- **Type:** hard
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 7 - Confirm before trade) · mdpack

### CNF-08 — confirmation-lines-annotation-first
- **Rule:** Confirmation lines: implement as annotation first (placeholders in V1). Touch-point rules: implement as visual/score first.
- **Type:** guideline
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification, §Implement now) · validation

### CNF-09 — RD-006-channeling-support-only
- **Rule:** RD-006: Use channeling as target/validation support, not initial pattern proof. Soft/visual, Accepted, chart annotation, risk Medium.
- **Type:** guideline
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## FIB · Fibonacci relationships

### FIB-01 — internal and external Fibonacci relationships in impulse
- **Rule:** Internal and external Fibonacci relationships are usually present among the segments of an impulse.
- **Type:** fib
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 18 rule 9) · mdpack

### FIB-02 — zigzag C relation to A
- **Rule:** C usually relates to A price-wise, or to the total of A+B time-wise, usually by equality or Fibonacci ratio; commonly C = A, C = 0.618A, or C = 1.618A depending on market behavior/structure.
- **Type:** fib
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 32); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules) · mdpack
- **Notes:** Day 1 Notes Page 7 adds a sketch where C ≈ 38.2% of A, plus C = A, and C = 1.618A for an elongated zigzag.

### FIB-03 — flat C relation to A or A+B
- **Rule:** In a flat, C usually relates to A price-wise, or to the total of A+B time-wise, usually by equality or Fibonacci ratio.
- **Type:** fib
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 34); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules) · mdpack

### FIB-04 — Fibonacci as validation filter, not signal
- **Rule:** Use Fibonacci as a validation filter, not as a trade signal by itself.
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation) · mdpack

### FIB-05 — impulse Fibonacci behavior
- **Rule:** Wave 3 often extends 1.618 or 2.618 of wave 1 (wave 3 usually the extended wave); wave 5 and wave 1 tend toward equality (often equality when wave 3 extends); wave 2 should not exceed 61.8% of wave 1; wave 4 and wave 2 often relate by Fibonacci.
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1) · mdpack
- **Notes:** Day 1 Notes2 Page 3 example: 3 = 161.8 (% of 1) and 5 ≈ 1; distinguishes subdivided vs extended portions.

### FIB-06 — zigzag Fibonacci behavior
- **Rule:** B <= 61.8% of A. C can equal A, be 0.618 of A, or extend to 1.618 of A (C≈A, C=0.618A, or C=1.618A).
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1) · mdpack

### FIB-07 — flat Fibonacci behavior
- **Rule:** B >= 61.8% of A; B can equal A or extend near 138.2% of A (B=A or B≈138.2% of A; quick sheet: near equality or 1.382x).
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1); 01_WAVE_RULES_REFERENCE.md (§Fibonacci quick sheet) · mdpack

### FIB-08 — triangle Fibonacci behavior
- **Rule:** Three legs (several legs) often show Fibonacci relationships with the prior leg; measure each leg and compare retracement percentages.
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1) · mdpack

### FIB-09 — X-wave Fibonacci behavior
- **Rule:** X should often be less than 61.8% of the prior pattern; a very large X requires relabeling (measure W and compare X).
- **Type:** fib
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1) · mdpack

### FIB-10 — Fibonacci series and golden ratio
- **Rule:** Fibonacci series 1,1,2,3,5,8,13,21,34,55,89,144…; the Golden Ratio = 1.618; golden rectangle and spiral underpin the wave principle.
- **Type:** fib
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 12) · mdpack

### FIB-11 — Fibonacci measurement definitions
- **Rule:** Retracement = correction length / prior impulse length. Extension = current wave length / comparison wave length. Equality = current wave approximately equal to comparison wave. Time ratio = current wave duration / comparison wave duration.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Required Calculations) · specs

### FIB-12 — important Fibonacci ratios
- **Rule:** Important ratios: 0.382, 0.500, 0.618, 1.000, 1.382, 1.618, 2.000, 2.618.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Important Ratios) · specs

### FIB-13 — impulse Fibonacci relationships
- **Rule:** Wave 3 often extends 1.618x or 2.618x Wave 1; extended wave should be at least 1.618x of next longest; two unextended waves tend toward equality.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage in Later Pattern Rules — Impulse) · specs

### FIB-14 — zigzag Fibonacci relationships
- **Rule:** B should be less than 61.8% of A; C often equals A or extends 1.618x A.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Zigzag) · specs

### FIB-15 — flat Fibonacci relationships
- **Rule:** B should be more than 61.8% of A; C often relates to A or A+B.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Flat) · specs

### FIB-16 — triangle Fibonacci relationships
- **Rule:** Internal legs are corrective; multiple legs often retrace more than 50% of previous leg.
- **Type:** fib
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Triangle) · specs

### FIB-17 — Fibonacci engine acceptance criteria
- **Rule:** Calculates all common price ratios; calculates time ratios; supports tolerance bands; returns structured measurements; measurements reusable by pattern modules; tests pass.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Acceptance Criteria) · specs

### FIB-18 — fib-comparison-uses
- **Rule:** Fibonacci relationships are used to compare: corrective retracement against previous impulse; impulse wave relationships within a sequence; wave C against wave A; projected targets after confirmation.
- **Type:** fib
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Confirmed concepts) · validation

### FIB-19 — common-retracement-zones
- **Rule:** Common retracement zones include 38.2%, 50%, and 61.8%.
- **Type:** fib
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Confirmed concepts) · validation

### FIB-20 — fib-is-scoring-not-predictor
- **Rule:** Fibonacci should not be coded as a single hard predictor; it should be a measuring and scoring system.
- **Type:** guideline
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Engineering approach) · validation

### FIB-21 — supported-retracement-levels
- **Rule:** Retracement levels to support: 0.236, 0.382, 0.500, 0.618, 0.786, 1.000.
- **Type:** fib
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Fibonacci zones to support) · validation

### FIB-22 — supported-extension-levels
- **Rule:** Extension levels to support: 1.000, 1.272, 1.414, 1.618, 2.000, 2.618.
- **Type:** fib
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Fibonacci zones to support) · validation

### FIB-23 — fib-profile-weights
- **Rule:** Profile use: `classic_elliott: fib_relationships_required: false, fib_relationships_score_weight: 0.20`; `sow_neowave_strict: fib_relationships_required_for_confirmation: true, fib_relationships_score_weight: 0.30`.
- **Type:** fib
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Rule profile use) · validation

### FIB-24 — fib-shared-utility-decision
- **Rule:** Build Fibonacci as a shared utility and scoring component, not as a standalone buy/sell engine.
- **Type:** process
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Development decision) · validation


## TIM · Wave time rules

### TIM-01 — corrective waves take same or more time than preceding impulse wave
- **Rule:** Corrective wave should take more time than preceding impulse: wave 2 should take same or more time than wave 1; wave 4 should take same or more time than wave 3.
- **Type:** time
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 19 rule 16) · mdpack
- **Notes:** Day 1 Notes2 Page 4: if wave 2 is too fast (less time than wave 1), the count is not valid under these notes.

### TIM-02 — zigzag B time >= A time
- **Rule:** Wave B should take the same or more time than wave A in a zigzag.
- **Type:** time
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32 · mdpack
- **Notes:** Day 1 Notes Page 7 states "B should take more time than A."

### TIM-03 — flat B time >= A time
- **Rule:** In a flat, wave B should take the same or more time than wave A.
- **Type:** time
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34 · mdpack
- **Notes:** Day 2 Notes Page 3 repeats: "in a flat, B should take more time than A."

### TIM-04 — corrective consumes more time than the move it corrects — exceptions
- **Rule:** Corrective usually consumes more time than the move it is correcting, EXCEPT in Triangles, Terminals, Diametric and Symmetrical.
- **Type:** time
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45) · mdpack

### TIM-05 — B-wave time heuristic for corrective family selection
- **Rule:** In corrective patterns inspect wave B timing: if B takes LESS time than A, diametric/triangle are more likely; if B takes MORE time than A, all corrections are possible, with zigzag or flat more likely.
- **Type:** time
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 9) · mdpack

### TIM-06 — time-length-comparisons-as-metric
- **Rule:** Time length comparisons (NeoWave) are implemented as metric + rule profile in V1, not as standalone hard invalidations.
- **Type:** time
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification) · validation

### TIM-07 — sow-time-rules-wave2-wave4
- **Rule:** In `sow_neowave_strict`: `wave2_time_vs_wave1: warn_or_fail_by_config` and `wave4_time_vs_wave3: warn_or_fail_by_config` (time-comparison rules configurable between warning and failure).
- **Type:** time
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md) · validation


## CYC · Time cycles (Kaal Chakra / Hurst)

### CYC-01 — time cycles as turn-window evidence
- **Rule:** Time cycles are used as supporting evidence for a turn window ("Are time cycles supporting a turn window?" in the signal checklist; "time cycles" is a Signal component in the trading cycle framework). Deck shows "Nifty Time Cycles", "Nifty Cycles", and a "Nifty 55 Days Cycles" chart — a 55-day cycle length on Nifty.
- **Type:** time
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Pages 61, 77, 78); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Signal checklist) · mdpack
- **Notes:** Cycle charts are image-based; only the 55-day figure is readable from the page title. Course context: "Kaal Chakra (Master of Cycles)" is the companion time-cycles course (deck Page 84).


## ICH · Ichimoku Cloud

### ICH-01 — Ichimoku default formulas
- **Rule:** Conversion line / Tenkan-sen = (9-period high + 9-period low) / 2; Base line / Kijun-sen = (26-period high + 26-period low) / 2; Leading Span A = (Conversion Line + Base Line) / 2; Leading Span B = (52-period high + 52-period low) / 2; Lagging Span / Chikou = close plotted 26 periods back. Default settings 9/26/52.
- **Type:** indicator
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter) · mdpack

### ICH-02 — Ichimoku long/short trade filter
- **Rule:** Long filter: price above cloud; Tenkan and Kijun rising or aligned upward; cloud supportive or turning supportive; wave pattern completed and confirmed. Short filter: price below cloud; Tenkan and Kijun falling or aligned downward; cloud resistive or turning bearish; wave pattern completed and confirmed.
- **Type:** indicator
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter) · mdpack

### ICH-03 — Ichimoku is not a standalone trigger
- **Rule:** Do not take a long simply because price is above the cloud — the wave count still needs confirmation; do not use Ichimoku as the only trigger.
- **Type:** indicator
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter; §Common mistakes to avoid) · mdpack

### ICH-04 — Ichimoku trade-setup condition from deck
- **Rule:** Ichimoku is an all-in-one indicator (support, resistance, trend direction, entry points, momentum). For any trade setup both the base line (Kijun-sen) and conversion line (Tenkan-sen) should move together in the same direction and the stock must be trading above or below the cloud.
- **Type:** indicator
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 49) · mdpack


## IND · Other indicators

### IND-01 — divergence and volume as supporting evidence
- **Rule:** Momentum divergence (RSI/momentum) is used only as supporting evidence at an important wave end; volume profile/volume behavior and options/positioning data should agree with the count before trading.
- **Type:** indicator
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView setup; §Signal checklist) · mdpack

### IND-02 — Prompt 003 — ATR pivot detector requirements
- **Rule:** 1. ATR must be computed only from past/current bars. 2. Pivot confirmation must occur only after ATR reversal is visible. 3. Every pivot must include confirmed_index and confirmed_t. 4. Include tests for no-lookahead behavior. New file: ewauto/pivots/atr_reversal.py; do not rewrite percent_reversal.py or fractal.py; no trading logic.
- **Type:** hard
- **Source:** BX/prompts/003_CODEX_ADD_ATR_PIVOT_DETECTOR.md (§Requirements) · specs

### IND-03 — barstate-isconfirmed-behavior
- **Rule:** `barstate.isconfirmed` is true on historical bars and on the closing update of a realtime bar; it can help avoid using a still-forming realtime bar. Limitation: it does not work when used inside `request.security()`.
- **Type:** indicator
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§barstate.isconfirmed) · validation

### IND-04 — pine-confirmed-condition-concept
- **Rule:** Suggested Pine helper concept: `confirmed_condition = barstate.isconfirmed and condition`. For higher-timeframe usage, the final Pine helper must follow TradingView's non-repainting HTF guidance and must be reviewed separately.
- **Type:** indicator
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Suggested Pine helper rules) · validation
- **Notes:** Marked "Concept only, not final code".

### IND-05 — RD-014-barstate-limitation
- **Rule:** RD-014: Do not rely on `barstate.isconfirmed` inside `request.security()`. Hard, Accepted, Pine helpers, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation


## SET · Trade setups & execution

### SET-01 — pre-trade signal checklist
- **Rule:** Ask before trading: completed pattern or only guessed pattern? divergence at an important wave end? time cycles supporting a turn window? volume profile/volume behavior agrees with count? options data or positioning supports the expected move? 15-minute or hourly chart giving a tradeable entry and stop? reward clearly larger than risk?
- **Type:** setup
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Market-context filter before wave count / Signal checklist) · mdpack

### SET-02 — long entry model
- **Rule:** Long setup: 1) higher timeframe count suggests correction complete or impulse continuation; 2) pattern confirmation line breaks; 3) price above or reclaiming Ichimoku cloud; 4) Tenkan/Kijun slope supports the move; 5) lower timeframe gives a pullback or breakout entry; 6) stop under the invalidation pivot or broken confirmation line; 7) target at the next Fibonacci projection, channel boundary, or prior wave level.
- **Type:** setup
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Practical entry model / Long setup) · mdpack

### SET-03 — short entry model
- **Rule:** Short setup: 1) higher timeframe count suggests upside pattern complete or bearish continuation; 2) confirmation line breaks down; 3) price below or losing the cloud; 4) Tenkan/Kijun slope supports downside; 5) lower timeframe gives a retest or breakdown entry; 6) stop above invalidation pivot or broken confirmation line; 7) target at next Fibonacci projection, channel boundary, or prior wave level.
- **Type:** setup
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Practical entry model / Short setup) · mdpack

### SET-04 — quick-reference trade filter
- **Rule:** Long: pattern confirmed + price above/reclaiming cloud + Tenkan/Kijun supportive. Short: pattern confirmed + price below/losing cloud + Tenkan/Kijun supportive.
- **Type:** setup
- **Source:** 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Trade filter) · mdpack

### SET-05 — trading cycle: context vs signal separation
- **Rule:** Separate Context from Signal. Context = market environment, Midcap/Nifty ratio, leadership/relative sector outperformance, scanner-based stock selection. Signal = pattern, divergence, time cycles, Elliott Wave, volume profile, options data, 15-minute chart execution, stop-loss, target, and reward:risk. For investing use weekly, daily, and hourly charts.
- **Type:** setup
- **Source:** 04_source_page_conversions/Brahmastra_Mentorship_Day_5_Trading_Cycle.md (§Page 1) · mdpack

### SET-06 — Phase 5 — TradingView workflow output DoD
- **Rule:** Produce manual chart instructions. DoD: Markdown note per candidate; invalidation / confirmation levels; wave IDs and timestamps.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 5) · specs

### SET-07 — manual TradingView note template
- **Rule:** Early output is a manual interpretation note containing: Symbol, Timeframe, Session, Detected structure, Current candidate, Confidence (e.g., 72%), key pivots with timestamps and prices, rule results (PASS/WARNING/UNKNOWN lines), TradingView action steps (mark pivot A, mark pivot B, draw 0-B trendline, watch for break of 0-B line, add Fibonacci projection from A to B to estimate C zone, use Ichimoku only as a trend filter), and invalidation statement. "This is better than directly producing buy/sell signals."
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§7 Manual TradingView Output Design) · specs

### SET-08 — invalidation discipline
- **Rule:** "If price violates the candidate structure before confirmation, discard the count."
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§7 Manual TradingView Output Design — Invalidation) · specs

### SET-09 — fib-output-per-candidate
- **Rule:** For every detected pattern candidate, output: Primary fib retracement; Primary fib extension; Invalidation level; Target zone; Confidence impact.
- **Type:** setup
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Manual TradingView output) · validation

### SET-10 — output-is-study-plan-not-signals
- **Rule:** The system should output a manual chart-study plan, not blind buy/sell signals.
- **Type:** setup
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§Output principle) · validation

### SET-11 — RD-019-manual-study-plan
- **Rule:** RD-019: Output should be a manual study plan, not a blind buy/sell signal. Product policy, Accepted, report/annotation engine, risk High.
- **Type:** setup
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### SET-12 — agent-a14-tv-output-rules
- **Rule:** A14 TradingView Output Agent rule: "Output manual charting instructions, not direct trading orders. Every candidate must include invalidation and confirmation state."
- **Type:** setup
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A14 TradingView Output Agent) · validation


## RSK · Risk & money management

### RSK-01 — never-skip list
- **Rule:** Never skip: invalidation price; stop location; reward/risk; alternate count; post-trade review.
- **Type:** risk
- **Source:** 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Never skip) · mdpack

### RSK-02 — live trade plan fields
- **Rule:** Before a trade record: direction (long/short), entry trigger, entry price, stop price, first target, second target, invalidation reason, confirmation line, Ichimoku condition, risk amount, reward/risk.
- **Type:** risk
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 4 - Live trade plan) · mdpack

### RSK-03 — before-entry checklist
- **Rule:** Before entry, all must be checked: higher timeframe count is valid; confirmation line has broken; entry timeframe agrees; stop is logical, not random; target is based on Fib/channel/wave level; news/event risk checked; position size is within risk rule; alternate count written down.
- **Type:** risk
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 4 - Live trade plan / Before entry checklist) · mdpack

### RSK-04 — backtest stage 3 — trading rules metrics
- **Rule:** Only after stages 1–2, test trading rules: entry trigger, stop invalidation, target zones, time stop, risk-reward, win rate, profit factor, max drawdown, expectancy.
- **Type:** risk
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 3) · specs


## MTH · Analysis method & order of operations

### MTH-01 — master manual workflow order
- **Rule:** Workflow order: 1) market context before counting waves; 2) mark swing highs/lows on higher timeframe; 3) classify structure as impulse, standard corrective, complex corrective, triangle, or diametric; 4) validate the count using price, time, Fibonacci, channels, and confirmation-line rules; 5) drop to lower timeframe only after the higher-timeframe map is acceptable; 6) use Ichimoku Cloud as trend/trade filter, not as replacement for wave validation; 7) trade only when risk, invalidation, and confirmation are clear.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§How to use this pack) · mdpack

### MTH-02 — TradingView chart layout
- **Rule:** Standard layout per instrument: price chart (candles/bars; log scale for long-term indices/stocks when the move is very large), Fib Retracement (validate wave 2, B wave, pullbacks), Fib Extension / Trend-Based Fib Extension (project wave 3, wave 5, C; anchor on 0-1-2 or A-B-C), Trend Line for 0-2, 2-4, 0-B, B-D lines, Parallel Channel (impulse/corrective/zigzag/flat/diametric boundaries), Date Range / Bar Count for time validation, Ichimoku Cloud with default 9/26/52, optional RSI/momentum only as supporting evidence.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView setup) · mdpack

### MTH-03 — global and inter-market context checklist
- **Rule:** Before counting a stock/index check: U.S. indices (DJIA, S&P 500, Nasdaq); Europe/Asia (FTSE, DAX, Nikkei, Hang Seng/Shanghai); currency and rates (DXY, USDINR, bond yields); commodities (gold, silver, copper, crude); breadth (midcap/smallcap vs benchmark); sector leadership (sectors outperforming the index); stock selection prefers clean structure, liquidity, relative strength.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Market-context filter before wave count / Global and inter-market checklist) · mdpack

### MTH-04 — core wave notation and mono-wave definition
- **Rule:** Impulse waves 1-2-3-4-5; corrective A-B-C; triangle A-B-C-D-E; diametric A-B-C-D-E-F-G; complex corrections W-X-Y or W-X-Y-X-Z. The mono-wave is the smallest marked swing unit: one directional move between two meaningful pivots.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Core wave notation) · mdpack

### MTH-05 — TradingView steps for an impulse
- **Rule:** 1) mark 0,1,2,3,4,5 pivots; 2) Fib Retracement on wave 1 to check wave 2; 3) Trend-Based Fib Extension from 0->1->2 to check wave 3 extension; 4) draw 0-2 line, internal price action should not violate count logic; 5) draw 2-4 line, confirmation after wave 5 requires its break; 6) compare waves 2 and 4 for alternation; 7) drop to 15-minute/hourly only after larger timeframe count acceptable.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView steps for an impulse) · mdpack

### MTH-06 — zigzag TradingView workflow
- **Rule:** 1) mark A,B,C against the prior trend; 2) Fib A to check B < 61.8%; 3) project C from B using A length; 4) draw the 0-B trendline; 5) after C completes wait for a break of 0-B in equal or less time than C; 6) if no confirmation, relabel as evolving correction.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules / TradingView workflow) · mdpack

### MTH-07 — ten-step manual chart routine
- **Rule:** 1) Context: index trend, sector leadership, global risk, bond/currency/commodity backdrop; 2) Weekly chart: identify the largest visible structure; 3) Daily chart: refine active wave and pattern; 4) Hourly chart: find confirmation line and invalidation; 5) 15-minute chart: entry only after larger chart is clear; 6) Label every count with text labels; 7) Measure with Fib, Price Range, Date Range; 8) Confirm: do not trade until the right confirmation line breaks; 9) Risk: write entry, stop, target, invalidation reason before trade; 10) Review: after market close save chart screenshots and update count.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Manual chart routine) · mdpack

### MTH-08 — common mistakes to avoid
- **Rule:** Avoid: forcing an impulse when the move is a corrective channel; calling every sideways move a triangle (many are flats or complex corrections); ignoring time rules and only using price retracement; acting before 0-B, 2-4, or B-D confirmation; mixing degrees (weekly and 15-minute counts must not carry the same degree labels); reusing old labels after invalidation instead of relabeling from scratch; using Ichimoku as the only trigger; ignoring sector/index context.
- **Type:** guideline
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Common mistakes to avoid) · mdpack

### MTH-09 — chart labelling conventions
- **Rule:** Use consistent text labels: 0,1,2,3,4,5 for impulse; A,B,C for standard correction; A,B,C,D,E for triangle; A,B,C,D,E,F,G for diametric; W,X,Y,X,Z for complex correction; "Alt:" for alternate count; "Invalid below/above:" for invalidation price; "Confirmed when:" next to the trendline that must break.
- **Type:** process
- **Source:** 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Minimum TradingView template labels) · mdpack

### MTH-10 — pattern families table
- **Rule:** Impulse 1-2-3-4-5 (5-3-5-3-5) directional trend move; Terminal impulse 1-2-3-4-5 (3-3-3-3-3) ending diagonal; Zigzag A-B-C (5-3-5) sharp correction; Flat A-B-C (3-3-5) sideways correction; Triangle A-B-C-D-E (3-3-3-3-3) contracting/expanding/neutral consolidation; Diametric A-B-C-D-E-F-G (3-3-3-3-3-3-3) seven-legged corrective; Complex correction W-X-Y or W-X-Y-X-Z combination of corrective patterns.
- **Type:** guideline
- **Source:** 01_WAVE_RULES_REFERENCE.md (§Pattern families) · mdpack

### MTH-11 — decision tree step 1 — directional vs corrective
- **Rule:** Ask: is price moving strongly in one direction with shallow pauses, or overlapping, slow, sideways, and channeled? If directional, test impulse rules first; if overlapping, test corrective patterns first.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 1) · mdpack

### MTH-12 — decision tree step 2 — impulse candidacy
- **Rule:** Candidate impulse if: you can mark 1-2-3-4-5; wave 2 is acceptable; wave 3 is not shortest; wave 4 does not overlap wave 2; one of 1/3/5 is extended; 2-4 confirmation is possible after wave 5. Reject impulse if: too much overlap; everything is inside a channel; wave 3 is weak/shortest; wave 4 overlaps wave 2 with no terminal impulse context.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 2) · mdpack

### MTH-13 — decision tree step 3 — zigzag vs flat
- **Rule:** Choose zigzag when: A looks like a five-wave move; B is less than 61.8% of A; C moves beyond A; structure is sharp. Choose flat when: A looks corrective; B retraces more than 61.8% of A; B may return near or beyond the start of A; C is a five-wave move; structure is sideways or broad.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 3) · mdpack

### MTH-14 — decision tree step 4 — triangle test
- **Rule:** Candidate triangle when: A-B-C-D-E visible; each leg corrective; B-D line clean; E smaller or terminal-looking; break of B-D confirms completion. Reject triangle when: there are seven clear legs; B-D line is repeatedly violated before E; one leg acts like a strong impulse instead of corrective movement.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 4) · mdpack

### MTH-15 — decision tree step 5 — diametric test
- **Rule:** Candidate diametric when: A-B-C-D-E-F-G visible; pattern resembles bow-tie, diamond, or running shape; paired leg relationships observable (G~A, F~B, E~C); triangle rules do not fit.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 5) · mdpack

### MTH-16 — decision tree step 6 — mark X and continue
- **Rule:** Candidate complex correction when: a simple ABC appears complete but confirmation does not happen; price starts another corrective sequence; the connector wave is likely X; the structure becomes W-X-Y or W-X-Y-X-Z.
- **Type:** process
- **Source:** 02_PATTERN_DECISION_TREE.md (§Step 6) · mdpack

### MTH-17 — timeframe cascade
- **Rule:** Higher timeframe first: Weekly -> Daily -> Hourly -> 15-minute.
- **Type:** process
- **Source:** 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Higher timeframe first) · mdpack
- **Notes:** Day 2 Notes Page 9 and the Day 5 Trading Cycle also use weekly/daily/hourly (15-minute for execution); for investing use weekly, daily, hourly charts.

### MTH-18 — pattern fingerprints quick reference
- **Rule:** Impulse: 5 waves, trend, one extension, wave 3 not shortest. Terminal: wedge, overlap allowed, usually at wave 5 or C. Zigzag: sharp ABC, B < 61.8% of A, C beyond A. Flat: sideways ABC, B > 61.8% of A. Triangle: ABCDE, corrective legs, clean B-D line. Diametric: seven legs ABCDEFG, bow-tie/diamond/running look. Complex: W-X-Y or W-X-Y-X-Z after simple ABC fails to confirm.
- **Type:** guideline
- **Source:** 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Pattern fingerprints) · mdpack

### MTH-19 — higher-timeframe wave map worksheet
- **Rule:** Record per instrument/timeframe/date: main trend (bullish/bearish/sideways), market context (risk-on/risk-off/mixed), sector context (leader/laggard/neutral); primary count with pattern type, labels marked, confirmation line, invalidation level, target zone, alternate count; and per-leg measurements of price length, time length, Fib relation, pass/fail (legs 1/A through G).
- **Type:** process
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 1 - Higher timeframe wave map) · mdpack

### MTH-20 — post-trade review questions
- **Rule:** After each trade record: result (win/loss/breakeven); was the count correct; did the confirmation line work; was entry early, late, or ideal; was stop logical; did I ignore invalidation; what should be relabeled now; chart screenshot saved (yes/no).
- **Type:** process
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 5 - Post-trade review) · mdpack

### MTH-21 — impulse/corrective application principles
- **Rule:** Impulse can be upwards or downwards; corrective can be upwards or downwards, going opposite to the move it is correcting; use wave charts plotting high and low of the period in chronological order; mono-wave is the basic unit of analysis; wave analysis has an explanation for each and every part of the chart for any time frame.
- **Type:** process
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44) · mdpack

### MTH-22 — rule of similarity and balance
- **Rule:** Rule of Similarity & Balance: the smaller of two adjacent waves of the same degree should be at least 1/3rd of the other, price-wise or time-wise.
- **Type:** hard
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44) · mdpack

### MTH-23 — pattern power transfer
- **Rule:** Each completed pattern implies and transfers a specific amount of "Power" to future market action; each completed pattern always implies the extent of the next action (categories: Impulse, Standard Corrective, Limiting Triangle, Non-limiting Triangle, Complex Corrective).
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45; §Page 46 PATTERN IMPLICATIONS) · mdpack

### MTH-24 — subdivision and channeling character
- **Rule:** Corrective is usually properly sub-divided while an impulse may look like a mono-wave; each impulse and corrective is part of a bigger wave, which is part of a still bigger wave (fractality); an impulse would usually NOT get channeled into parallel trend lines.
- **Type:** guideline
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45) · mdpack

### MTH-25 — Day 2 manual analysis steps
- **Rule:** Start from weekly/daily/hourly/15-minute; draw channel; try to identify impulse or corrective; apply the B-time heuristic; plot Ichimoku cloud; go to hourly/15-minute for the trade.
- **Type:** process
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 9) · mdpack

### MTH-26 — channelling technique (image-only)
- **Rule:** A "CHANELLING TECHNIQUE" section exists (deck Page 27) — the technique details are only in the page image and could not be read from text.
- **Type:** process
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 27) · mdpack
- **Notes:** Practical channel rules that ARE textual elsewhere: impulses usually do not channel in parallel lines (deck p.45); zigzag/flat 3-of-4 touch-point channel rules; C ending on channel warns of complex correction.

### MTH-27 — one Codex task prompt at a time
- **Rule:** Do not ask Codex to build everything at once; use one task prompt at a time from prompts/ and docs/codex/, starting with prompts/001_CODEX_CONNECT_ALPACA_MCP.md, then proceed through docs/roadmap/PHASED_BUILD_ROADMAP.md.
- **Type:** process
- **Source:** BX/README.md (§Recommended Codex workflow) · specs

### MTH-28 — design principles 4–5 — one pattern at a time, limited context
- **Rule:** "One pattern at a time: do not implement all NeoWave patterns in one task." and "Codex gets limited context: each coding task should load only relevant specs and files."
- **Type:** process
- **Source:** BX/docs/ARCHITECTURE.md (§Design principles) · specs

### MTH-29 — use bundle as active repo; legacy as reference only
- **Rule:** Use ElliottWave_Automation_Project_Bundle/ as the new clean base project; keep legacy/ (previous repo), research_validation/ (research decision docs), elliotwave_md_pack/ (source theory and manual TradingView notes) as references only. Do not build from the legacy repo directly.
- **Type:** process
- **Source:** BX/docs/START_HERE.md (§Use this bundle as the active repository) · specs

### MTH-30 — legacy migration rule
- **Rule:** "Legacy idea → new spec → new test → clean implementation → accepted module".
- **Type:** process
- **Source:** BX/docs/START_HERE.md (§Do not build from the legacy repo directly) · specs

### MTH-31 — first 5 steps
- **Rule:** 1. Create a GitHub repo from this bundle. 2. Run pytest and confirm all tests pass. 3. Connect Alpaca MCP server through ewauto/data/adapters/alpaca_mcp_adapter.py. 4. Fetch one symbol and save canonical bars. 5. Run ghost-forward validation and inspect the CSV outputs.
- **Type:** process
- **Source:** BX/docs/START_HERE.md (§First 5 steps) · specs

### MTH-32 — Task 1 context restriction
- **Rule:** Give Codex only these files for Task 1: README.md, pyproject.toml, ewauto/data/schema.py, ewauto/data/adapters/base.py, ewauto/data/adapters/alpaca_mcp_adapter.py, ewauto/data/cache.py, tests/test_schema.py, prompts/001_CODEX_CONNECT_ALPACA_MCP.md. "Do not give it all Elliott Wave docs while connecting Alpaca. That prevents drift."
- **Type:** process
- **Source:** BX/docs/START_HERE.md (§What Codex should see first) · specs

### MTH-33 — never give Codex the full theory library
- **Rule:** "Never give Codex the full theory library for a coding task. Use one task card, one agent role, and a small file set."
- **Type:** process
- **Source:** BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Never give Codex the full theory library) · specs

### MTH-34 — required prompt structure
- **Rule:** Every prompt must contain: Role, Task, Allowed files, Forbidden files, Input contract, Output contract, Tests required, Definition of done.
- **Type:** process
- **Source:** BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Required prompt structure) · specs

### MTH-35 — forbidden Codex behavior
- **Rule:** Forbidden: implementing trading execution without request; adding ML before labeled data exists; mixing classical Elliott and NeoWave rules without profile separation; removing confirmed_index / confirmed_t; backdating signals; rewriting unrelated modules.
- **Type:** hard
- **Source:** BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Forbidden Codex behavior) · specs

### MTH-36 — pull request acceptance rule
- **Rule:** A change is accepted only if: pytest passes; no-lookahead tests pass; module docstring explains the design; new behavior has tests; README or docs updated when interface changes.
- **Type:** process
- **Source:** BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Pull request acceptance rule) · specs

### MTH-37 — Phase 0 — repo setup DoD
- **Rule:** Phase 0 definition of done: `pip install -e '.[dev]'`, pytest passes, README commands work.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 0) · specs

### MTH-38 — Phase 6 — legacy salvage rule
- **Rule:** Migrate only proven pieces from the old repo: "Legacy idea → new spec → new tests → clean implementation". Do not copy large legacy files directly into production modules.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 6) · specs

### MTH-39 — Phase 7 — advanced patterns one at a time
- **Rule:** Add one pattern at a time: Triangle, Terminal impulse, Diametric, Neutral triangle, Extracting triangle, Complex correction. Each pattern must include tests and ghost-forward output.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 7) · specs

### MTH-40 — Prompt 005 — legacy salvage process
- **Rule:** Process: 1. Summarize the legacy idea. 2. Identify whether it fits the new architecture. 3. Write or update a spec. 4. Add tests. 5. Implement cleanly in the new module. Acceptance: Legacy idea → new spec → new tests → clean implementation → pytest passes.
- **Type:** process
- **Source:** BX/prompts/005_CODEX_LEGACY_SALVAGE.md (§Process / Acceptance rule) · specs

### MTH-41 — Prompt 005 — legacy salvage prohibitions
- **Rule:** Do not copy entire legacy modules blindly. Do not import from legacy code in production modules. Do not migrate symbol-specific logic. Do not migrate old forecast logic unless it passes ghost-forward validation.
- **Type:** hard
- **Source:** BX/prompts/005_CODEX_LEGACY_SALVAGE.md (§Forbidden behavior) · specs

### MTH-42 — three-layer knowledge architecture
- **Rule:** Layer 1 — Knowledge Base (raw markdown conversions, handwritten notes, source PDFs, diagrams, rules, examples). Layer 2 — Engineering Specifications (clean, simplified, machine-readable specs derived from the knowledge base). Layer 3 — Code Implementation. "The LLM should normally work from Layer 2, not from all raw documents."
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§1 Executive Summary) · specs
- **Notes:** Risks of handing full doc set to LLM: mixing discretionary theory with engineering; building all patterns at once; hallucinating rules; combining detection/signal/backtest/auto-trading into one unstable module; losing focus.

### MTH-43 — core build sequence
- **Rule:** Build in this sequence: Bars → Pivots → Mono-waves → Rule checks → Candidate patterns → Scores → Chart annotations → Backtest → Dashboard. Do NOT begin with "Detect every Elliott Wave / NeoWave pattern automatically" — too broad, will fail.
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§2 Core Development Philosophy) · specs
- **Notes:** Foundation order: 1. Clean historical data. 2. Stable pivot detection. 3. Mono-wave construction. 4. Rule validation. 5. Pattern candidates. 6. Manual TradingView interpretation.

### MTH-44 — keep raw documents separate
- **Rule:** The markdown pack goes under docs_source/original_markdown_pack/. Codex/Claude should NOT read every source document for every task; every development task should point to one or two specific specs (e.g., use only specs/03_pivot_detection_spec.md + specs/01_data_contract.md; do not read or modify docs_source/, patterns/, backtest/, dashboard/).
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§5 Important Rule: Keep Raw Documents Separate) · specs

### MTH-45 — Phase 0 — project freeze and scope control
- **Rule:** Create PROJECT_CHARTER.md, DEVELOPMENT_ROADMAP.md, LLM_WORKFLOW_RULES.md, specs/00_system_scope.md. Acceptance: project scope clearly defined; non-scope clearly defined; LLM workflow rules exist; development phases locked; the project does not contain auto-trading logic yet.
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§6 Phase 0) · specs

### MTH-46 — mono-wave concept — measurable unit, no labels
- **Rule:** "A mono-wave is the basic measurable unit of wave analysis. It is not yet an Elliott Wave label. It is only a directional segment between two confirmed pivots." Do not label a segment as Wave 1, Wave 2, Wave A, Wave B, or Wave C in this phase — first calculate facts, not opinions.
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Mono-Wave Concept / Important Rule) · specs
- **Notes:** Example measurements only: "This wave is UP. It moved 8.4%. It took 27 bars. It retraced 52% of the previous wave. It extended 1.61x the previous comparable wave."

### MTH-47 — LLM workflow rules and task template
- **Rule:** Never give the prompt "Read all documents and build the Elliott Wave automation system." Every task must include: Task name, Scope, Allowed files, Forbidden files, Input contract, Output contract, Tests required, Definition of done. Template includes: "Do not add trading logic unless explicitly requested. Do not refactor unrelated modules."
- **Type:** process
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§11 LLM Workflow Rules) · specs

### MTH-48 — neowave-implement-gradually
- **Rule:** NeoWave-style analysis is more rule-dense and interpretive than basic Elliott Wave — it includes time, price, balance, similarity, touch-point, confirmation-line, monowave, and pattern-implication concepts — therefore NeoWave rules should be implemented gradually.
- **Type:** process
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Key point) · validation

### MTH-49 — neowave-source-priority
- **Rule:** Source priority for NeoWave: 1) user-provided SOW/NeoWave notes and converted Markdown pack; 2) official NEoWave material and QOW archive; 3) Glenn Neely's formal book/course material if manually available; 4) secondary internet summaries only as low-priority references.
- **Type:** process
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Source priority for NeoWave) · validation

### MTH-50 — neowave-archive-topics
- **Rule:** The official NEoWave archive publicly indexes: Rule of Similarity and Balance, monowave chart detail, wave 2 triangle possibility, Fibonacci measurement, extension importance, dividends/splits and wave structure, cash vs futures chart selection.
- **Type:** scope
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Confirmed research observation) · validation
- **Notes:** Supports the need for a dedicated `sow_neowave_strict` rule profile and separate advanced modules.

### MTH-51 — neowave-as-profiles-first
- **Rule:** NeoWave must be represented as stricter rule profiles and scoring/annotation modules first. Full advanced pattern automation should wait until the pivot and mono-wave engine are stable.
- **Type:** process
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Development decision) · validation

### MTH-52 — tv-output-language-policy
- **Rule:** TradingView outputs should use language like "Possible candidate / Confirmed after break / Invalid if level breaks / Manual review required" and avoid "Guaranteed wave count / Immediate buy/sell / Non-repainting prediction".
- **Type:** process
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Manual workflow policy) · validation

### MTH-53 — manual-output-before-live
- **Rule:** Manual output should be implemented before live signals or automation.
- **Type:** process
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§Development decision) · validation

### MTH-54 — v1-pattern-order
- **Rule:** V1 pattern order: 1. Mono-wave table; 2. Zigzag candidate; 3. Flat candidate; 4. Basic impulse candidate; 5. Triangle annotation/manual-review.
- **Type:** process
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§V1 pattern order) · validation

### MTH-55 — one-pattern-per-task-card
- **Rule:** Do not build all pattern modules at once. Use one pattern module per task card.
- **Type:** process
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Development decision) · validation

### MTH-56 — source-bibliography
- **Rule:** Canonical source list (accessed 2026-06-13): Elliott Wave International Waveopedia pages (Motive Waves, Impulse, Corrective Waves, Zigzags, Flats, Triangles, Fibonacci Relationships, Channeling, Alternation); NEoWave QOW Archive; TradingView Pine Script docs (Repainting, Bar States, Other Timeframes and Data); Alpaca Market Data docs (About Market Data API, Historical Stock Data, Historical Bars Single Symbol); user-provided pack (Brahmastra mentorship Day 5 notes, Sutra of Waves Day 1 and Day 2 notes, SOW Fibonacci May 2026 notes, SOW/Neo Wave training deck, converted Markdown pack, ElliottWave automation roadmap, agent prompt pack).
- **Type:** process
- **Source:** research_notes/R09_Source_Bibliography.md (§all) · validation

### MTH-57 — research-pipeline-philosophy
- **Rule:** Build philosophy: Research source → verified rule → engineering interpretation → spec update → coding task. Never: Research source → direct coding agent context.
- **Type:** process
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§Final recommended build philosophy) · validation
- **Notes:** Research should be a controlled validation sprint; the project must not absorb unlimited EW/NeoWave/Fibonacci/TradingView/broker-data theory.

### MTH-58 — v1-build-sequence
- **Rule:** Recommended V1 build sequence: 1. Alpaca Data Engine; 2. Data adjustment/session metadata; 3. Pivot Engine with candidate vs confirmed states; 4. MonoWave Engine; 5. Rule Profile Engine; 6. Zigzag Detector; 7. Flat Detector; 8. Impulse Detector; 9. TradingView Manual Annotation Output; 10. Backtest Harness with no-lookahead tests.
- **Type:** process
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§Recommended V1 build sequence after this research) · validation

### MTH-59 — final-control-rule
- **Rule:** If a new research item does not change a spec, test, or task card, it should remain in research notes only and must not enter coding context.
- **Type:** process
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§Final control rule) · validation

### MTH-60 — research-acceptance-test
- **Rule:** A research item is accepted only if it converts into at least one of: a spec change, a test case, a task card, a rule profile setting, a manual TradingView instruction, or a warning/limitation note. Otherwise it remains background reading and does not affect development.
- **Type:** process
- **Source:** 01_RESEARCH_SCOPE_AND_POLICY.md (§Research acceptance test) · validation

### MTH-61 — llm-context-control
- **Rule:** Coding agents must not browse or interpret broad Elliott Wave theory. They receive only: 1. Shared system rules; 2. The relevant spec file; 3. The current task card; 4. The specific decision record related to that task.
- **Type:** process
- **Source:** 01_RESEARCH_SCOPE_AND_POLICY.md (§Context-control rule for LLMs) · validation
- **Notes:** Repeated as the "Core rule" in README.md.

### MTH-62 — research-item-format
- **Rule:** Every research item must follow the format: Topic; Source; Observed claim; Engineering interpretation; Decision; Affected files; Affected agents; Risk level; Implementation status.
- **Type:** process
- **Source:** 01_RESEARCH_SCOPE_AND_POLICY.md (§Research sprint output format) · validation

### MTH-63 — source-ranking-tiers
- **Rule:** Source hierarchy: Tier 1 project source of truth (user-provided mentorship PDFs and converted Markdown pack; existing project roadmap and agent prompt pack; user-confirmed Alpaca MCP behavior); Tier 2 official documentation (TradingView Pine docs, Alpaca API docs, Elliott Wave International Waveopedia, NEoWave official archive); Tier 3 technical implementation references (Python packages, backtesting frameworks, exchange calendars); Tier 4 secondary commentary (blogs, YouTube, forums, generic trading education). Tier 4 sources must not create hard rules unless verified against Tier 1 or Tier 2.
- **Type:** process
- **Source:** 02_SOURCE_QUALITY_POLICY.md (§Source ranking) · validation

### MTH-64 — source-conflict-handling
- **Rule:** When sources conflict: 1. Do not overwrite existing docs silently; 2. Create a decision record; 3. Decide whether the conflict should be handled by separate rule profiles; 4. Add tests for both profiles if both are supported.
- **Type:** process
- **Source:** 02_SOURCE_QUALITY_POLICY.md (§Conflict handling) · validation

### MTH-65 — citation-rule
- **Rule:** Every research note must include a Sources section with URLs and access date. Avoid copying long source text into the project; summarize and translate into engineering decisions.
- **Type:** process
- **Source:** 02_SOURCE_QUALITY_POLICY.md (§Citation rule for docs) · validation

### MTH-66 — decision-states
- **Rule:** Decision states: Accepted = add to project specs/tasks; Deferred = keep in research notes, do not build now; Rejected = do not use; Needs Review = requires user or manual domain review.
- **Type:** process
- **Source:** 03_RESEARCH_DECISION_LOG.md (§Decision states) · validation
- **Notes:** Coding agents should follow the decision log only when their task explicitly references it.

### MTH-67 — research-agents-propose-only
- **Rule:** Files that must not be modified by research agents: src/, tests/, notebooks/. Research agents propose changes only; coding agents implement after the decision log is accepted.
- **Type:** process
- **Source:** 04_DOC_UPDATE_MATRIX.md (§Files that should not be modified by research agents) · validation

### MTH-68 — v1-freeze-checklist
- **Rule:** Documentation freeze checklist before coding: PROJECT_CHARTER.md confirms V1 scope; DATA_CONTRACT.md includes Alpaca session/adjustment/feed metadata; PIVOT_DETECTION_SPEC.md includes pivot_time and confirmed_time; RULE_PROFILE_SPEC.md exists; NO_LOOKAHEAD_AND_REPAINTING_POLICY.md exists; PATTERN_FEASIBILITY_MATRIX.md exists; MANUAL_TRADINGVIEW_OUTPUT_SPEC.md exists; agent task cards mention allowed files and forbidden changes; backtest spec states that signals can only use data available at the signal time.
- **Type:** process
- **Source:** 05_FREEZE_CRITERIA_V1.md (§Documentation freeze checklist) · validation

### MTH-69 — freeze-rule
- **Rule:** After freeze criteria are accepted, no new theory is allowed into V1 unless it fixes a bug, prevents lookahead bias, or clarifies an existing rule.
- **Type:** process
- **Source:** 05_FREEZE_CRITERIA_V1.md (§Freeze rule) · validation

### MTH-70 — research-vs-coding-agent-separation
- **Rule:** Use research agents to verify and classify rules; use coding agents to implement frozen specs; do not mix them. Recommended agent sequence: 1. Elliott Rule Validation Agent; 2. NeoWave Clarification Agent; 3. Alpaca Data Research Agent; 4. TradingView Repainting Agent; 5. No-Lookahead Audit Agent; 6. Documentation Patch Agent; 7. Coding Agent.
- **Type:** process
- **Source:** 06_AGENT_RESEARCH_PROMPTS.md (§Principle, §Recommended agent sequence) · validation

### MTH-71 — research-agent-output-format
- **Rule:** Every research agent must output: Findings; Accepted decisions; Deferred decisions; Rejected ideas; Affected docs; Affected tests; Risks; Next coding task.
- **Type:** process
- **Source:** 06_AGENT_RESEARCH_PROMPTS.md (§Research agent output format) · validation

### MTH-72 — coding-agent-no-theory-decisions
- **Rule:** A coding agent must never decide a new Elliott Wave theory interpretation by itself; it must ask for a decision record update. Use prompt cards one at a time — do not give all prompt cards to one agent.
- **Type:** process
- **Source:** 06_AGENT_RESEARCH_PROMPTS.md (§Coding agent rule, §Use prompt cards) · validation

### MTH-73 — pack-recommended-use-order
- **Rule:** Recommended use order: 1. Read 00_RESEARCH_VALIDATION_MASTER.md; 2. Read 03_RESEARCH_DECISION_LOG.md; 3. Apply doc_updates/UPDATE_01_SPECS_TO_MODIFY.md; 4. Add prompt cards only when needed; 5. Freeze Version 1 using 05_FREEZE_CRITERIA_V1.md; 6. Begin coding from data engine and pivot engine only.
- **Type:** process
- **Source:** README.md (§Recommended use order) · validation

### MTH-74 — most-important-pack-decisions
- **Rule:** Most important decisions: use rule profiles `classic_elliott`, `sow_neowave_strict`, `research_experimental`; keep NeoWave advanced patterns as manual-review or V2 until data/pivot/monowave foundation is stable; treat TradingView repainting and no-lookahead as hard engineering constraints; store Alpaca data with explicit adjustment/session profiles; backtests must trigger at pivot confirmation time, not at the historical pivot candle.
- **Type:** process
- **Source:** README.md (§Most important project decisions in this pack) · validation

### MTH-75 — agent-a08-one-pattern-per-task
- **Rule:** A08 Pattern Agent rule: "Only implement one pattern per task. Advanced NeoWave patterns are manual-review unless a task specifically says otherwise."
- **Type:** process
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A08 Pattern Agent) · validation

### MTH-76 — shared-rule-research-not-specs
- **Rule:** Shared System Rules addition: "Research notes are not coding specs. Coding agents follow decision logs and specs only."
- **Type:** process
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§Shared System Rules update) · validation

### MTH-77 — prompt-r01-ew-validation-agent
- **Rule:** Elliott Wave Rule Validation Agent: validate only core EW rules needed for software implementation; must not write code, implement a detector, propose trading signals, or add ML. Output: 1. Rules confirmed; 2. Rules conflicting with existing docs; 3. Whether conflict requires a rule profile; 4. Hard rules; 5. Soft/scoring rules; 6. Manual-review rules; 7. Specs to update; 8. Tests to add. Do not browse beyond official Elliott Wave references unless asked; do not overwrite SOW/NeoWave rules — separate them into profiles.
- **Type:** process
- **Source:** prompt_cards/PROMPT_R01_EW_RULE_VALIDATION_AGENT.md (§prompt) · validation

### MTH-78 — prompt-r02-neowave-agent
- **Rule:** NeoWave/SOW Research Agent: classify SOW/NeoWave rules into implementation categories; must not code, must not simplify advanced NeoWave patterns into classical Elliott patterns, must not implement advanced patterns in V1. Output: implement-now rules; score-only rules; manual-review rules; V2 postponed rules; rule profile additions for `sow_neowave_strict`; agent/task impacts. If a NeoWave rule requires discretionary judgment, label it `manual_review` unless a numeric implementation is obvious.
- **Type:** process
- **Source:** prompt_cards/PROMPT_R02_NEOWAVE_RESEARCH_AGENT.md (§prompt) · validation

### MTH-79 — templates-for-notes-decisions-patches
- **Rule:** Reusable templates: research note (Purpose; Sources reviewed; Findings table with Finding/Source/Confidence/Notes; Engineering interpretation; Decision recommendation Accepted/Deferred/Rejected/Needs Review; Affected docs; Tests to add; Risks; Final decision ID RD-XXX); decision record (Status; Context; Sources; Decision; Implementation impact Module/Spec/Task/Test; Alternatives considered; Risk Low/Medium/High/Critical; Review date); doc patch (Target file; Patch reason; Add section; Replace section; Tests affected; Agent affected).
- **Type:** process
- **Source:** templates/TEMPLATE_RESEARCH_NOTE.md, templates/TEMPLATE_DECISION_RECORD.md, templates/TEMPLATE_DOC_PATCH.md (§all) · validation


## DAT · Data contract & preparation

### DAT-01 — wave chart plotting convention
- **Rule:** Use wave charts plotting the high and low of the period in chronological order (basic price-vs-time wave chart; example labels 0-1-2-3-4-5 followed by A-B-C).
- **Type:** process
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44); 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 2) · mdpack

### DAT-02 — image-only pages that may carry unread rules
- **Rule:** Numerous deck pages are image-only ("Visual/chart example") with headings but no extractable rule text: pp.13-15, 20-26 (impulse examples), 27 (Channelling Technique), 28 (Alternation), 29 (Extensions), 30 (Terminal Impulse), 38 (2 Stage Confirmation), 39-43 (Double/Tripple Combination), 47-48 (Diametric), 50-51 (Ichimoku charts), 52 (Neutral Triangle), 53 (3rd Extension Terminal), 54-55 (Extracting Triangle), 56-76 (market counts and examples incl. 72 Expanding Triangle), 77-79 (time cycles), 85, 88. Page 58 and 91 contain garbled OCR. Any rules drawn only in these images are NOT captured in this ledger.
- **Type:** scope
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§various pages) · mdpack
- **Notes:** Similarly all pages of the Day 1/Day 2/Brahmastra notes are handwritten images; their .md interpretations were extracted above but the underlying sketches may contain additional detail.

### DAT-03 — CSV column contract (canonical or abbreviated)
- **Rule:** CSV columns can be either canonical `timestamp,open,high,low,close,volume` or common API abbreviations `t,o,h,l,c,v`.
- **Type:** hard
- **Source:** BX/README.md (§Validate a CSV) · specs
- **Notes:** Validated via `ewauto validate-csv path/to/TSLA_1D.csv --symbol TSLA --timeframe 1D`.

### DAT-04 — data-lake independence via adapters
- **Rule:** "The active code should not depend directly on a specific data lake layout. Use adapters and canonical schema."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§intro) · specs

### DAT-05 — canonical bars — required and optional columns
- **Rule:** Required columns: timestamp, open, high, low, close, volume. Optional columns: vwap, symbol, timeframe, session_type, source.
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Canonical bars) · specs

### DAT-06 — recommended data lake layout
- **Rule:** data_lake/ layout: raw/alpaca/SYMBOL/TIMEFRAME/*.json; normalized/bars/SYMBOL/SYMBOL_TIMEFRAME_full.parquet; features/pivots/ and features/monowaves/; validation/ghost_forward/.
- **Type:** setup
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Recommended data lake layout) · specs

### DAT-07 — data lake rule 1 — raw data immutable
- **Rule:** "Raw data is immutable."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules) · specs

### DAT-08 — data lake rule 2 — normalized reproducible from raw
- **Rule:** "Normalized bars are reproducible from raw data."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules) · specs

### DAT-09 — data lake rule 3 — feature outputs carry config metadata
- **Rule:** "Feature outputs must include config metadata."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules) · specs

### DAT-10 — data lake rule 5 — version historical validation results
- **Rule:** "Never overwrite historical validation results without versioning."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules) · specs

### DAT-11 — Phase 1 — Alpaca MCP data connection DoD
- **Rule:** Fetch 10 years of bars for one symbol; normalize into canonical schema; save parquet cache; reload parquet and pass validate_bars. Files: ewauto/data/adapters/alpaca_mcp_adapter.py, ewauto/data/schema.py, ewauto/data/cache.py.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 1) · specs

### DAT-12 — Phase 8 — data lake integration timing
- **Rule:** Connect the package to the broader data lake only after the schema stabilizes.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 8) · specs

### DAT-13 — SPEC 001 — required column types
- **Rule:** Required: timestamp (UTC-aware datetime), open (float), high (float), low (float), close (float), volume (numeric >= 0). Optional: vwap, symbol, timeframe, session_type, source. Purpose: all data sources produce the same canonical OHLCV schema so the wave engine never depends on provider-specific quirks.
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_001_DATA_CONTRACT.md (§Required columns / Optional columns) · specs

### DAT-14 — SPEC 001 — validation rules
- **Rule:** timestamp sorted ascending; timestamp unique; high >= open, close, low; low <= open, close, high; no nulls in required columns; volume >= 0. Implementation: ewauto/data/schema.py.
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_001_DATA_CONTRACT.md (§Validation rules) · specs

### DAT-15 — SPEC 002 — required pivot fields
- **Rule:** Pivot fields: index, t, price, kind: H/L, confirmed_index, confirmed_t, source, meta. Purpose: detect swing pivots without lookahead.
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Required pivot fields) · specs

### DAT-16 — Prompt 001 — Alpaca MCP adapter requirements
- **Rule:** Adapter must: return canonical bars; support extended-hours flag; support adjusted/raw behavior if exposed by MCP; preserve UTC timestamps; pass schema validation; not store secrets. Forbidden: implementing Elliott Wave logic; modifying pivot/wave/rules/pattern/ghost-forward modules; adding API keys or secrets; removing normalize_bars or validate_bars.
- **Type:** hard
- **Source:** BX/prompts/001_CODEX_CONNECT_ALPACA_MCP.md (§Requirements / Forbidden changes) · specs
- **Notes:** DoD: pytest passes; fetch one symbol from Alpaca MCP; save parquet cache; reload parquet cache; validate_bars passes; README command snippet updated if needed.

### DAT-17 — Phase 1 — bar data contract
- **Rule:** Every bar must normalize to: symbol (string), timestamp (timezone-aware datetime), open/high/low/close (float), volume (float), vwap (float optional), timeframe (string), session_type (regular | extended | full), source (alpaca), adjusted (true | false optional).
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Data Contract) · specs

### DAT-18 — Phase 1 — required data capabilities
- **Rule:** Fetch historical bars for one symbol; support daily, hourly, 15m, 5m, and 1m where available; support extended-hours filtering; cache data locally as parquet; validate missing candles; validate duplicate timestamps; validate timezone consistency; export sample CSV for manual inspection.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Required Capabilities) · specs

### DAT-19 — session handling — regular/extended/full
- **Rule:** The system must explicitly support: regular = only regular market session; extended = premarket + postmarket only if separated; full = regular + extended combined. "For U.S. equities, session handling matters because Elliott Wave pivots can differ when extended-hours candles are included."
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Session Handling) · specs

### DAT-20 — Phase 1 — acceptance criteria
- **Rule:** Can fetch 10 years of daily data for a symbol; can fetch intraday data for supported periods; can store and reload parquet files; can label each bar with session_type; no duplicate timestamps; no missing schema columns; all timestamps timezone-aware; unit tests pass.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Acceptance Criteria) · specs

### DAT-21 — Phase 2 — pivot record schema
- **Rule:** Pivot record: symbol, timeframe, pivot_id, pivot_time, pivot_price, pivot_type (HIGH | LOW), source_bar_index, confirmation_time, confirmation_bar_index, confirmation_lag_bars, method, parameters.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Pivot Record Schema) · specs

### DAT-22 — Phase 3 — mono-wave schema
- **Rule:** Mono-wave record: symbol, timeframe, wave_id, start_pivot_id, end_pivot_id, start_time, end_time, start_price, end_price, direction (UP | DOWN), price_length, time_length_bars, time_length_seconds, percent_change, slope, retracement_vs_previous, extension_vs_previous, price_ratio_vs_previous, time_ratio_vs_previous, confirmation_time.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Mono-Wave Schema) · specs

### DAT-23 — alpaca-10yr-capability
- **Rule:** User tested Alpaca MCP with Claude and confirmed approximately 10 years of data availability including extended-hours data. Treat tested MCP behavior as the practical account-level capability while using official Alpaca docs as the API contract reference.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§User-confirmed capability) · validation

### DAT-24 — alpaca-timeframes-and-pagination
- **Rule:** Alpaca single-symbol historical bars endpoint supports timeframes: 1-59 minutes; 1-23 hours; 1 day; 1 week; 1, 2, 3, 4, 6, or 12 months. The endpoint has pagination and requires checking `next_page_token`.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Officially relevant API behavior) · validation

### DAT-25 — required-dataset-metadata
- **Rule:** Every cached dataset must include metadata: symbol, timeframe, source: alpaca, feed: iex|sip|other, adjustment_profile: raw|split|dividend|spin-off|all, session_profile: regular|extended|full, asof: YYYY-MM-DD or null, start: datetime, end: datetime, timezone: America/New_York, retrieved_at: datetime, mcp_server_version: optional.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Required metadata) · validation

### DAT-26 — adjustment-policy-split-default
- **Rule:** Split discontinuities can distort wave counts, so: Default wave-analysis profile = split-adjusted; Raw data retained for execution/reference/latest price comparison; All-adjusted data = optional research profile. The system must clearly show which adjustment profile was used.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Adjustment policy) · validation

### DAT-27 — session-policy-regular-default
- **Rule:** Default V1 wave analysis uses regular session only (`v1_default: session_profile: regular`). Extended-hours data must be stored separately because overnight/pre-market candles can create pivots that do not appear on regular-session TradingView charts. Optional profile: `session_profile: extended, use_case: gap/premarket/manual review`.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Session policy) · validation

### DAT-28 — feed-policy-iex-vs-sip
- **Rule:** IEX is the no-subscription feed representing a single exchange; SIP is consolidated across US exchanges. The project must store `feed` explicitly to avoid mixing data quality profiles.
- **Type:** hard
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Feed policy) · validation

### DAT-29 — alpaca-ingestion-decisions
- **Rule:** Development decisions: build Alpaca ingestion before Elliott rules; cache data as parquet; store metadata JSON beside each parquet file; follow pagination until complete; keep regular and extended sessions separate; keep raw and split-adjusted data distinguishable.
- **Type:** process
- **Source:** research_notes/R05_Alpaca_Data_Behavior.md (§Development decisions) · validation

### DAT-30 — alpaca-explicit-profiles-decision
- **Rule:** The system must not treat all bars as equal. Store `session_profile`, `adjustment_profile`, `feed`, `source`, and `asof` in metadata.
- **Type:** hard
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§5. Alpaca data must be stored with explicit session and adjustment profiles) · validation

### DAT-31 — RD-015-adjustment-profile
- **Rule:** RD-015: Store raw and adjusted variants or at least explicit `adjustment_profile`. Default analysis profile: split-adjusted; raw retained for execution/reference. Data policy, Accepted, data engine, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### DAT-32 — RD-016-session-profile
- **Rule:** RD-016: Store `regular`, `extended`, and `full` session profiles separately. Default V1 pattern analysis: regular session. Data policy, Accepted, data engine, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### DAT-33 — RD-017-pagination
- **Rule:** RD-017: Data fetcher must follow `next_page_token` until complete or capped. Hard, Accepted, data engine, risk High.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### DAT-34 — RD-018-feed-metadata
- **Rule:** RD-018: Store `feed` in metadata; distinguish IEX vs SIP. Hard, Accepted, data engine, risk Medium.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### DAT-35 — prompt-r04-alpaca-agent-default-decision
- **Rule:** Alpaca Data Research Agent: convert Alpaca MCP/API behavior into a clean data contract (no EW logic, no pivots, no trading signals). Output: final bar schema; metadata schema; session profile rules; adjustment profile rules; pagination requirements; feed/asof requirements; data validation tests. Required decision: Default V1 wave analysis uses regular-session split-adjusted data unless user overrides it.
- **Type:** hard
- **Source:** prompt_cards/PROMPT_R04_ALPACA_DATA_RESEARCH_AGENT.md (§prompt) · validation


## VAL · Validation, backtesting & selection

### VAL-01 — impulse validation checklist
- **Rule:** Checks (pass/fail): 5 waves visible; internal structure acceptable; wave 2 <= 61.8% of wave 1; wave 3 not shortest; wave 4 no overlap with wave 2; alternation between wave 2 and 4; extension only one of 1/3/5; extended wave >= 1.618x next longest; 2-4 line drawn; 2-4 line broken in acceptable time; Ichimoku agrees; risk/reward acceptable.
- **Type:** validation
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 2 - Impulse validation) · mdpack

### VAL-02 — corrective validation matrix
- **Rule:** Legs: zigzag 3, flat 3, triangle 5, diametric 7. Internal structure: 5-3-5 / 3-3-5 / 3-3-3-3-3 / corrective legs. B depth: zigzag <61.8% A, flat >61.8% A, triangle n/a, diametric n/a. Confirmation line: 0-B / 0-B / B-D / boundary after G. Time rule: zigzag and flat B >= A with 0-B break <= C; triangle B-D break <= E; diametric compare paired legs. Complex-correction risk flags: zigzag/flat if C ends at channel; triangle if B-D not clean; diametric if seven legs continue.
- **Type:** validation
- **Source:** 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 3 - Corrective validation) · mdpack

### VAL-03 — ghost-forward CSV run defaults
- **Rule:** Ghost-forward validation on CSV uses `ewauto ghost-forward-csv ... --reversal-pct 3.0 --warmup-bars 100 --horizon-bars 50`; outputs `outputs/reports/<SYMBOL>_<TF>_ghost_forward_signals.csv` and `outputs/reports/<SYMBOL>_<TF>_ghost_forward_outcomes.csv`.
- **Type:** validation
- **Source:** BX/README.md (§Run ghost-forward validation on CSV) · specs
- **Notes:** Example parameters: reversal 3.0%, 100 warmup bars, 50-bar outcome horizon.

### VAL-04 — most important rule — pivot candle vs signal candle
- **Rule:** Never confuse the pivot candle with the signal candle: "Pivot happened at index 100. Pivot confirmed at index 105. Signal can start at 105 only, not 100."
- **Type:** hard
- **Source:** BX/README.md (§Most important rule) · specs
- **Notes:** "The whole project is built around this no-lookahead principle."

### VAL-05 — design principle 1 — no lookahead
- **Rule:** "No lookahead: every pivot and signal must have a confirmation index."
- **Type:** hard
- **Source:** BX/docs/ARCHITECTURE.md (§Design principles) · specs

### VAL-06 — data lake rule 4 — snapshots carry timestamp + visible boundary
- **Rule:** "Ghost-forward snapshots must include signal timestamp and visible-bar boundary."
- **Type:** hard
- **Source:** BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules) · specs

### VAL-07 — ghost forward validation — definition
- **Rule:** Ghost Forward Validation is a candle-by-candle historical replay where the engine receives only past and current bars, generates live-visible wave candidates, records every candidate state, and later evaluates the outcome using future bars only after the signal snapshot has been frozen.
- **Type:** validation
- **Source:** BX/docs/GHOST_FORWARD_VALIDATION.md (§intro) · specs

### VAL-08 — ghost forward vs backtest question
- **Rule:** Normal backtesting asks "Did the completed historical pattern work?"; ghost-forward asks "At each historical candle, what would the engine have seen in real time?" — more appropriate for Elliott Wave and NeoWave because patterns evolve gradually.
- **Type:** validation
- **Source:** BX/docs/GHOST_FORWARD_VALIDATION.md (§Why this matters) · specs

### VAL-09 — snapshot fields (bundle)
- **Rule:** Snapshot fields: symbol, timeframe, signal_index, signal_time, visible_bars_until, candidate_id, pattern, status, confidence, expected_direction, invalidation_level, confirmation_level, wave_ids.
- **Type:** hard
- **Source:** BX/docs/GHOST_FORWARD_VALIDATION.md (§Snapshot fields) · specs

### VAL-10 — outcome fields (bundle)
- **Rule:** Outcome fields: max_favorable_excursion, max_adverse_excursion, hit_confirmation, hit_invalidation, bars_to_confirmation, bars_to_invalidation.
- **Type:** hard
- **Source:** BX/docs/GHOST_FORWARD_VALIDATION.md (§Outcome fields) · specs

### VAL-11 — non-negotiable — never backdate ghost-forward signal
- **Rule:** "Ghost-forward validation must never move a signal backward to the pivot candle."
- **Type:** hard
- **Source:** BX/docs/GHOST_FORWARD_VALIDATION.md (§Non-negotiable rule) · specs

### VAL-12 — no-lookahead core law
- **Rule:** "A module is invalid if it uses future bars to create a signal at an earlier timestamp."
- **Type:** hard
- **Source:** BX/docs/NO_LOOKAHEAD_POLICY.md (§Core law) · specs
- **Notes:** The policy file "is mandatory for every agent and Codex task."

### VAL-13 — pivot rule — three indices
- **Rule:** "Pivot index = where the swing actually occurred. Confirmed index = when the algorithm had enough evidence to know the pivot existed. Signal index = confirmed index or later." A pivot that occurs at candle 100 and is confirmed at candle 105 can only affect signals from candle 105 onward.
- **Type:** hard
- **Source:** BX/docs/NO_LOOKAHEAD_POLICY.md (§Pivot rule) · specs

### VAL-14 — forbidden lookahead behaviors
- **Rule:** Forbidden: backdating signals to the pivot candle; using completed future structures to label real-time candidates; optimizing pivots using full-chart hindsight; generating PnL from unconfirmed pivots; treating TradingView repainting labels as valid trade-time signals.
- **Type:** hard
- **Source:** BX/docs/NO_LOOKAHEAD_POLICY.md (§Forbidden behavior) · specs

### VAL-15 — required tests for every pivot detector
- **Rule:** Every pivot detector must pass: `confirmed_index >= pivot_index`, `confirmed_t >= pivot_t`, and a prefix-stability test.
- **Type:** validation
- **Source:** BX/docs/NO_LOOKAHEAD_POLICY.md (§Required tests) · specs

### VAL-16 — required tests for every replay engine
- **Rule:** Every replay engine must pass: visible data at t = `bars[:t+1]`; `signal_time` = current candle time; outcome labels use future only after snapshot is frozen.
- **Type:** validation
- **Source:** BX/docs/NO_LOOKAHEAD_POLICY.md (§Required tests) · specs

### VAL-17 — Phase 2 — pivot engine hardening DoD
- **Rule:** Goal: compare percent-reversal, fractal, and later ATR pivots. DoD: confirmed_index test passes; prefix-stability test passes; pivot CSV export exists; chart debug output exists.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 2) · specs

### VAL-18 — Phase 4 — ghost-forward validation DoD
- **Rule:** Prove candidates are visible in real time. DoD: ghost_forward_signals.csv; ghost_forward_outcomes.csv; summary metrics; no backdated signal timestamps.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 4) · specs

### VAL-19 — SPEC 002 — mandatory pivot invariant
- **Rule:** `confirmed_index >= index` and `confirmed_t >= t`.
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Mandatory invariant) · specs

### VAL-20 — SPEC 004 — ghost forward replay process
- **Rule:** For candle t: visible = bars[:t+1]; pivots = detect(visible); monowaves = build(pivots confirmed by t); candidates = scan(monowaves); snapshot = freeze candidate at t. Later: label outcome using bars after t.
- **Type:** validation
- **Source:** BX/docs/specs/SPEC_004_GHOST_FORWARD.md (§Process) · specs

### VAL-21 — SPEC 004 — forbidden ghost-forward behaviors
- **Rule:** Do not let outcome labeling affect the snapshot. Do not move signal time back to the pivot candle. Do not use full-history pivots during replay.
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_004_GHOST_FORWARD.md (§Forbidden) · specs

### VAL-22 — Prompt 002 — pivot engine hardening tests
- **Rule:** Required tests: `confirmed_index >= index`; `confirmed_t >= t`; prefix-stability test; `min_bars_between` respected. Forbidden: adding trading signals; adding Elliott pattern rules; removing confirmed_index or confirmed_t; backdating signal timestamps.
- **Type:** validation
- **Source:** BX/prompts/002_CODEX_HARDEN_PIVOT_ENGINE.md (§Required tests / Forbidden changes) · specs
- **Notes:** DoD: pytest passes; pivot outputs are deterministic; pivot detector config is documented.

### VAL-23 — Prompt 004 — extended ghost-forward reports
- **Rule:** Add: ghost_forward_summary.md generator; candidate stability report; late signal rate metric; repaint-like disappearance metric. Forbidden: altering pivot confirmation semantics; adding live trading; letting outcome labels influence signal snapshots.
- **Type:** validation
- **Source:** BX/prompts/004_CODEX_EXTEND_GHOST_FORWARD_REPORTS.md (§Requirements / Forbidden changes) · specs
- **Notes:** DoD: pytest passes; sample CSV run produces signals, outcomes, and summary markdown.

### VAL-24 — Phase 2 — pivot no-lookahead rule
- **Rule:** A pivot is confirmed only after enough future bars or reversal movement occurred. Store pivot_time = actual swing point time; confirmation_time = time when the system could know the pivot was confirmed. "Backtests must use `confirmation_time`, not `pivot_time`, for decisions."
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 No-Lookahead Rule) · specs

### VAL-25 — backtest stage 1 — mechanics
- **Rule:** Do not backtest final trading strategies too early. Stage 1 validates mechanics: data availability, pivot confirmation lag, no-lookahead enforcement, pattern frequency, pattern completion behavior.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 1) · specs

### VAL-26 — backtest stage 2 — pattern implication
- **Rule:** Stage 2 validates pattern implication: After Zigzag completion, did price move as expected? After 0-B line break, did follow-through occur? After impulse count completion, did correction begin? After triangle breakout, did directional continuation occur?
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 2) · specs

### VAL-27 — no-lookahead core rule + example
- **Rule:** "A signal, pattern, pivot, or confirmation can only be used after the bar where it becomes knowable." Example: swing high at 10:00 confirmed at 10:45 → pivot_time = 10:00, confirmation_time = 10:45; for backtesting "Do not allow any trade or pattern decision before 10:45."
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§10 No-Lookahead Rules) · specs
- **Notes:** Required test tests/test_no_lookahead.py "must remain active throughout the project."

### VAL-28 — repainting-definition-and-risk
- **Rule:** Repainting = difference between behavior on historical bars and realtime bars. Pivots and higher-timeframe references are especially vulnerable to repainting.
- **Type:** validation
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Repainting risk) · validation
- **Notes:** Per TradingView documentation; critical for wave analysis.

### VAL-29 — htf-request-security-leak
- **Rule:** Higher-timeframe data requested through `request.security()` can leak future information if lookahead settings are misused; using lookahead without offsetting the expression makes historical results appear to know future values.
- **Type:** validation
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Higher-timeframe data) · validation

### VAL-30 — pine-helper-policy
- **Rule:** No Pine helper script may use future-leaking higher-timeframe logic. No Pine helper script may treat a realtime unconfirmed bar as a confirmed signal. No Pine helper script may claim non-repainting if it uses pivot confirmation that requires future bars without showing confirmation delay.
- **Type:** hard
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Pine helper policy) · validation

### VAL-31 — no-lookahead-core-rule
- **Rule:** The system must never enter, exit, score, or confirm a trade using data that was not available at that time.
- **Type:** hard
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Core rule) · validation

### VAL-32 — pivot-two-timestamps
- **Rule:** Every pivot has two timestamps: `pivot_time` = the actual turning candle; `confirmed_time` = first candle where the algorithm could know the pivot. A backtest may display the pivot marker at `pivot_time`, but any signal or trade action can only occur at or after `confirmed_time`.
- **Type:** hard
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Pivot timing rule) · validation

### VAL-33 — pivot-lifecycle-states
- **Rule:** Pivot lifecycle: candidate → confirmed → used_in_pattern; candidate → invalidated; confirmed → expired.
- **Type:** hard
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Pivot lifecycle) · validation

### VAL-34 — test-pivot-not-usable-before-confirmation
- **Rule:** Test 1: Given a swing high at bar 100 and confirmation occurs at bar 106, the backtest must not enter or exit using this pivot before bar 106.
- **Type:** validation
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 1) · validation

### VAL-35 — test-pattern-confirmation-is-max-pivot-confirmation
- **Rule:** Test 2: Given a zigzag candidate requiring pivots A, B, C, the pattern confirmation time is max(confirmed_time_A, confirmed_time_B, confirmed_time_C).
- **Type:** validation
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 2) · validation

### VAL-36 — test-no-future-bars-in-rolling
- **Rule:** Test 3: Indicators, pivots, waves, and pattern scores must use only bars <= current bar (no future-bar access in rolling calculations).
- **Type:** validation
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 3) · validation

### VAL-37 — test-annotation-vs-signal-separation
- **Rule:** Test 4: Chart may draw pivot at historical turning point; signal report must display confirmation delay.
- **Type:** validation
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 4) · validation

### VAL-38 — trade-log-required-fields
- **Rule:** Every trade log must include: signal_time, execution_time, latest_known_pivot_time, latest_known_pivot_confirmed_time, pattern_candidate_id, rule_profile, lookahead_audit_status.
- **Type:** hard
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Backtest output requirement) · validation

### VAL-39 — forbidden-lookahead-behaviors
- **Rule:** Forbidden: Entering at the pivot candle when pivot was confirmed later; Using centered rolling windows for signal decisions; Using final pattern labels to trade earlier candles; Using future higher-timeframe bar values; Using adjusted data for backtest but raw prices for execution without documenting it.
- **Type:** hard
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Forbidden behavior) · validation

### VAL-40 — test-file-before-backtests
- **Rule:** Create `test_no_lookahead.py` before implementing backtests.
- **Type:** process
- **Source:** research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Development decision) · validation

### VAL-41 — confidence-policy-no-100pct
- **Rule:** No pattern should output 100% certainty. Use states: Candidate; Probable; Confirmed by rule profile; Manual review required; Invalidated.
- **Type:** hard
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Confidence policy) · validation

### VAL-42 — tv-repainting-hard-risk
- **Rule:** TradingView realtime bars and historical bars can behave differently; higher-timeframe requests can repaint unless handled carefully; `barstate.isconfirmed` is useful on normal chart bars but does not work inside `request.security()`. Engineering decision: add `NO_LOOKAHEAD_AND_REPAINTING_POLICY.md` to main specs and tests.
- **Type:** hard
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§4. TradingView repainting is a hard risk) · validation

### VAL-43 — backtest-uses-confirmation-time
- **Rule:** A swing pivot is only known after a reversal or confirmation rule; a backtest that enters at the pivot candle uses future information. Every pivot has `pivot_time` (actual market turning candle) and `confirmed_time` (first candle where algorithm could know the pivot). Trades and alerts can only use `confirmed_time`.
- **Type:** hard
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§6. Backtesting must use confirmation time, not pivot time) · validation

### VAL-44 — RD-011-pivot-timestamps
- **Rule:** RD-011: Every pivot must store `pivot_time` and `confirmed_time`. Backtests use only `confirmed_time`. Hard, Accepted, pivot engine/backtest, risk Critical.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### VAL-45 — RD-012-lifecycle-states
- **Rule:** RD-012: Pivots and patterns must have lifecycle states: `candidate`, `confirmed`, `invalidated`, `expired`. Hard, Accepted, all engines, risk Critical.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### VAL-46 — RD-013-htf-security-non-repainting
- **Rule:** RD-013: Pine helpers must avoid future-leaking `request.security()` patterns. Non-repainting HTF values require confirmed/offset logic. Hard, Accepted, Pine helpers, risk Critical.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### VAL-47 — RD-020-no-entry-before-confirmation
- **Rule:** RD-020: No strategy can enter at a pivot before the pivot is confirmed. Hard, Accepted, backtest engine, risk Critical.
- **Type:** hard
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### VAL-48 — backtest-hard-test-known-from-time
- **Rule:** Backtest spec hard test: No trade can be generated using a pivot, monowave, or pattern before its known_from_time.
- **Type:** hard
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§6. Update backtest spec) · validation

### VAL-49 — agent-a04-pivot-contract
- **Rule:** A04 Pivot Engine Agent rule: "You must store both pivot_time and confirmed_time. You must not expose a pivot as usable for signals until confirmed_time."
- **Type:** hard
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A04 Pivot Engine Agent) · validation

### VAL-50 — agent-a05-monowave-known-from
- **Rule:** A05 MonoWave Engine Agent rule: "A mono-wave is only known when both endpoint pivots are confirmed. Use known_from_time = max(endpoint confirmed times)."
- **Type:** hard
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A05 MonoWave Engine Agent) · validation

### VAL-51 — agent-a11-backtest-fail-conditions
- **Rule:** A11 Backtest Agent rule: "Backtest must fail if any signal uses future data, centered windows, unconfirmed pivots, or final labels unavailable at that time."
- **Type:** hard
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A11 Backtest Agent) · validation

### VAL-52 — task-r004-backtest-audit
- **Rule:** TASK_R004 (patch backtest spec with strict no-lookahead audit): done when trade log includes `lookahead_audit_status`; tests for unconfirmed pivot usage are required; signal time uses `known_from_time`, not visual pivot time.
- **Type:** validation
- **Source:** doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R004) · validation

### VAL-53 — prompt-r03-repaint-agent-hard-rule
- **Rule:** TradingView Repainting Audit Agent: only audit repainting and lookahead risk (no full Pine script, no trading signals). Output: repainting risks; HTF request.security rules; barstate.isconfirmed limitations; alert timing rules; manual TradingView warning text; tests or review checks needed. Hard rule: Any higher-timeframe series must be reviewed for future leakage before use in a published helper.
- **Type:** hard
- **Source:** prompt_cards/PROMPT_R03_TRADINGVIEW_REPAINT_AGENT.md (§prompt) · validation

### VAL-54 — prompt-r05-no-lookahead-agent-hard-rule
- **Rule:** No-Lookahead Audit Agent: prevent future-data leakage in pivots, monowaves, pattern detection, and backtests; must not implement a strategy, optimize parameters, or report performance metrics unless the audit passes. Output: all potential future-leak paths; required timestamp fields; required lifecycle states; unit tests to add; backtest rejection conditions; trade log audit fields. Hard rule: A trade can never occur at a pivot candle unless that pivot was already confirmed at that same candle by the selected confirmation method.
- **Type:** hard
- **Source:** prompt_cards/PROMPT_R05_NO_LOOKAHEAD_AUDIT_AGENT.md (§prompt) · validation


## AUT · Automation / engineering specs

### AUT-01 — bundle pipeline order
- **Rule:** The system pipeline is: Bars → Pivots → Mono-waves → Rule validators → Pattern candidates → Ghost-forward validation → TradingView notes.
- **Type:** process
- **Source:** BX/README.md (§What is included) · specs
- **Notes:** v0.1 engineering base built around Alpaca MCP data source, TradingView manual workflow, and Ghost Forward Validation.

### AUT-02 — architecture pipeline stages
- **Rule:** Pipeline: Alpaca MCP / CSV / Data Lake → Data Adapter → Canonical Bar Schema → Parquet Cache → Pivot Detector → Mono-wave Builder → Rule Validators → Pattern Candidate Scanner → Ghost Forward Replay → Outcome Labeling → TradingView Manual Notes / Reports.
- **Type:** process
- **Source:** BX/docs/ARCHITECTURE.md (§Pipeline) · specs

### AUT-03 — package map (ewauto)
- **Rule:** Package layout: ewauto/data (schema.py, cache.py, sessions.py, adapters/{base,csv_adapter,alpaca_mcp_adapter}.py), ewauto/pivots (models.py, percent_reversal.py, fractal.py), ewauto/waves/monowave.py, ewauto/rules ({result,fibonacci,impulse,corrective}.py), ewauto/patterns/candidates.py, ewauto/validation/ghost_forward ({snapshot,replay_engine,outcome_labeler,metrics}.py), ewauto/charts/tradingview_notes.py.
- **Type:** setup
- **Source:** BX/docs/ARCHITECTURE.md (§Package map) · specs

### AUT-04 — design principle 3 — explicit rule statuses
- **Rule:** "Rules are explicit: every rule returns PASS, FAIL, WARN, or UNKNOWN."
- **Type:** hard
- **Source:** BX/docs/ARCHITECTURE.md (§Design principles) · specs

### AUT-05 — bundle file inventory
- **Rule:** Bundle contains root (README.md, pyproject.toml, requirements.txt, configs/default.yml), 22 code files under ewauto/, 6 test files (test_schema, test_percent_pivots, test_fractal_pivots, test_monowaves, test_rules, test_ghost_forward), and 5 prompt files (001–005).
- **Type:** setup
- **Source:** BX/docs/BUNDLE_FILE_INDEX.md (§Root/Code/Tests/Prompts) · specs

### AUT-06 — Phase 3 — mono-wave and rule engine DoD
- **Rule:** Convert pivots to mono-waves and validate zigzag/flat/impulse candidates. DoD: wave table export; rule-result JSON export; candidate scanner returns interpretable results.
- **Type:** process
- **Source:** BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 3) · specs

### AUT-07 — SPEC 002 — implemented and future detectors
- **Rule:** Implemented: PercentReversalPivotDetector, FractalPivotDetector. Future: ATR reversal pivots, volume-confirmed pivots, multi-timeframe pivots.
- **Type:** setup
- **Source:** BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Implemented detectors / Future detectors) · specs

### AUT-08 — SPEC 003 — rule statuses
- **Rule:** Rule statuses: PASS, FAIL, WARN, UNKNOWN. Rationale: "Elliott Wave and NeoWave are not purely binary. Some rules are hard invalidations, while others are warning signs or manual-review criteria."
- **Type:** hard
- **Source:** BX/docs/specs/SPEC_003_RULE_ENGINE.md (§Rule statuses / Why this matters) · specs

### AUT-09 — SPEC 003 — implemented and future validators
- **Rule:** Implemented validators: validate_zigzag, validate_flat, validate_impulse. Future validators: triangle, terminal impulse, diametric, neutral triangle, extracting triangle, complex correction.
- **Type:** setup
- **Source:** BX/docs/specs/SPEC_003_RULE_ENGINE.md (§Implemented validators / Future validators) · specs

### AUT-10 — recommended repository structure
- **Rule:** Repo `elliotwave-automation/` with README.md, PROJECT_CHARTER.md, DEVELOPMENT_ROADMAP.md, LLM_WORKFLOW_RULES.md; docs_source/ (original_markdown_pack, handwritten_notes, pdf_conversions, source_images); specs/00–12 (system_scope, data_contract, bar_schema, pivot_detection, monowave, impulse_rules, corrective_rules, fibonacci_rules, ichimoku_filter, pattern_scoring, backtest, output_chart, tradingview_manual_output); src/ (data, pivots, waves, rules, patterns, scoring, backtest, charts, reports, utils); tests/ incl. test_no_lookahead.py; notebooks/; config/ (symbols.yaml, timeframes.yaml, pivot_profiles.yaml, session_profiles.yaml); outputs/ (data_cache, charts, backtests, reports, logs).
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§4 Recommended Repository Structure) · specs

### AUT-11 — Phase 2 — required pivot modes
- **Rule:** Start with three modes: Mode 1 percentage reversal pivots; Mode 2 ATR-based pivots; Mode 3 fractal swing pivots. For the first working version prioritize: "Percentage reversal + minimum bar distance".
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Required Pivot Modes) · specs
- **Notes:** "Elliott Wave automation depends on pivots. If the pivot engine is unstable, every wave count will be unstable."

### AUT-12 — Phase 2 — pivot acceptance criteria
- **Rule:** Detects alternating HIGH and LOW pivots; does not create duplicate consecutive highs or lows; stores pivot time and confirmation time separately; supports parameter profiles; can plot pivots on a chart; no-lookahead tests pass.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Acceptance Criteria) · specs

### AUT-13 — Phase 3 — mono-wave acceptance criteria
- **Rule:** Can convert pivot table to mono-wave table; calculates price length and time length; calculates retracement and extension ratios; does not assign Elliott labels yet; tests pass. Mono-wave table must be deterministic.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Acceptance Criteria / DoD) · specs

### AUT-14 — Phase 4 — rule result schema
- **Rule:** Every rule check returns: {"rule_id": "wave_2_retrace_limit", "status": "PASS | FAIL | WARNING | UNKNOWN", "confidence": 0.0, "details": "Human-readable explanation", "measured_value": 0.618, "expected_value": "<= 0.618"}.
- **Type:** hard
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 4 Rule Result Schema) · specs
- **Notes:** Why not binary only: Elliott Wave / NeoWave is interpretive — some rules mandatory, some guidelines, some context-dependent; hence PASS/FAIL/WARNING/UNKNOWN.

### AUT-15 — Phase 4 — rule engine acceptance criteria
- **Rule:** Rule engine can run a list of validators; each validator returns structured output; pattern modules can reuse this engine; rule results can be converted into pattern score; scoring works deterministically; tests pass.
- **Type:** validation
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§Phase 4 Acceptance Criteria) · specs

### AUT-16 — chart output requirements per phase
- **Rule:** Phase 1 chart: candles only, optional session shading. Phase 2: candles + pivot markers, HIGH/LOW pivots labeled, confirmation lag visible in debug mode. Phase 3: candles + pivots + mono-wave lines, each mono-wave numbered internally as M1, M2, M3... Phase 6+: candles + pattern candidate labels, A-B-C or 1-2-3-4-5 labels, rule score box, invalidation level, confirmation trendline.
- **Type:** setup
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§8 Chart Output Requirements) · specs

### AUT-17 — ruleprofile-system-first
- **Rule:** Implement a `RuleProfile` system before coding impulse/corrective validators.
- **Type:** process
- **Source:** research_notes/R01_Elliott_Wave_Core_Rules.md (§Development decision) · validation

### AUT-18 — neowave-v1-implement-now
- **Rule:** Implement now in V1: Mono-wave table; Price length and time length; Retracement/extension metrics; Similarity/balance score fields; Confirmation-line placeholders; Manual review flags.
- **Type:** process
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§V1 handling / Implement now) · validation

### AUT-19 — neowave-rule-type-classification
- **Rule:** Engineering classification: Numeric retracement/extension → Implement; Time length comparisons → Implement as metric + rule profile; Similarity/balance → Implement as score/warning; Touch-point rules → Implement as visual/score first; Confirmation lines → Implement as annotation first; Advanced patterns → Manual-review or V2.
- **Type:** process
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification) · validation

### AUT-20 — wave-data-fields
- **Rule:** Each wave/mono-wave must expose: price_length, abs_price_length, time_length_bars, direction, start_price, end_price, start_time, end_time.
- **Type:** process
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Required data fields) · validation

### AUT-21 — required-ratio-functions
- **Rule:** Required ratio functions: retracement_pct(current_wave, previous_wave); extension_ratio(current_wave, reference_wave); time_ratio(current_wave, reference_wave); price_projection(start_point, reference_length, ratio).
- **Type:** process
- **Source:** research_notes/R03_Fibonacci_Engineering_Rules.md (§Required ratio functions) · validation

### AUT-22 — add-spec-13-no-lookahead
- **Rule:** Add `specs/13_no_lookahead_and_repainting_policy.md` as a required future spec.
- **Type:** process
- **Source:** research_notes/R04_TradingView_Repainting_And_Alerts.md (§Required future spec) · validation

### AUT-23 — manual-output-required-sections
- **Rule:** Required output sections: Symbol; Timeframe; Session profile; Adjustment profile; Rule profile; Detected candidate pattern; Pattern confidence; Confirmed pivots; Candidate pivots; Invalidation level; Confirmation trigger; Fibonacci zone; Channel/line instruction; TradingView drawing steps; Manual review warnings; No-lookahead confirmation delay.
- **Type:** process
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§Required output sections) · validation

### AUT-24 — tv-object-export-idea
- **Rule:** Future versions can export TradingView objects as JSON: {"lines": [], "labels": [], "fib_anchors": [], "notes": []}.
- **Type:** process
- **Source:** research_notes/R07_Manual_TradingView_Workflow.md (§TradingView object export idea) · validation

### AUT-25 — feasibility-monowave
- **Rule:** Mono-wave: difficulty Low, V1 status Implement — foundation for all patterns.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### AUT-26 — new-specs-to-add
- **Rule:** New documentation to add: specs/12_rule_profile_spec.md; specs/13_no_lookahead_and_repainting_policy.md; specs/14_data_adjustment_and_session_policy.md; specs/15_pattern_feasibility_matrix.md; specs/16_manual_tradingview_output_spec.md.
- **Type:** process
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§New documentation to add to the main project) · validation
- **Notes:** 04_DOC_UPDATE_MATRIX.md assigns priorities: specs 12 and 13 Critical; specs 14, 15, 16 High.

### AUT-27 — RD-001-rule-profiles
- **Rule:** RD-001: Add separate `classic_elliott`, `sow_neowave_strict`, and `research_experimental` profiles. Rule type Architecture, Accepted, affects `rules/` and `specs/12_rule_profile_spec.md`, risk High.
- **Type:** process
- **Source:** 03_RESEARCH_DECISION_LOG.md (§decision table) · validation

### AUT-28 — doc-update-matrix-existing-files
- **Rule:** Existing docs to update: DEVELOPMENT_ROADMAP.md (add Research Validation Sprint before coding); LLM_WORKFLOW_RULES.md (coding agents cannot read broad research notes unless task-specific); specs/03_pivot_detection_spec.md (add pivot_time, confirmed_time, lifecycle states); specs/05_impulse_rules_spec.md (rule profile handling for wave 2 retracement conflict); specs/06_corrective_rules_spec.md (zigzag/flat/triangle V1/V2 status); specs/10_backtest_spec.md (confirmation-time-only trade policy); agents/A04_Pivot_Engine_Agent.md (no-lookahead confirmation contract); agents/A07_Rule_Engine_Agent.md (rule profile system); agents/A11_Backtest_Agent.md (mandatory lookahead audit); tasks/TASK_004_PIVOT_ENGINE.md (tests for candidate/confirmed pivot timestamps); tasks/TASK_010_BACKTEST_ENGINE.md (tests preventing pivot-time entries).
- **Type:** process
- **Source:** 04_DOC_UPDATE_MATRIX.md (§Existing docs to update) · validation

### AUT-29 — rule-profile-spec-full-yaml
- **Rule:** `specs/12_rule_profile_spec.md` required content: `classic_elliott: wave2_max_retrace_pct: 100, wave3_not_shortest: hard, wave4_overlap_wave1: fail, alternation: score`; `sow_neowave_strict: wave2_max_retrace_pct: 61.8, wave3_not_shortest: hard, wave4_overlap_wave1: fail_except_terminal, wave2_time_vs_wave1: warn_or_fail_by_config, wave4_time_vs_wave3: warn_or_fail_by_config, alternation: score_required`; `research_experimental: allow_manual_override: true, strict_invalidations: false`.
- **Type:** hard
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md) · validation

### AUT-30 — no-lookahead-spec-contents
- **Rule:** `specs/13_no_lookahead_and_repainting_policy.md` must include: pivot_time vs confirmed_time; candidate vs confirmed states; TradingView repainting warning; request.security HTF rule; backtest signal timing; forbidden future access.
- **Type:** validation
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§2. Add specs/13_no_lookahead_and_repainting_policy.md) · validation

### AUT-31 — pivot-schema-fields
- **Rule:** Pivot spec fields: pivot_id: str; symbol: str; timeframe: str; pivot_time: datetime; confirmed_time: datetime; pivot_type: Literal['high','low']; price: float; confirmation_method: str; confirmation_bars: int; confirmation_price_move_pct: float | None; status: Literal['candidate','confirmed','invalidated','expired'].
- **Type:** hard
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§3. Update pivot spec) · validation

### AUT-32 — monowave-schema-fields
- **Rule:** Monowave spec fields: start_pivot_id; end_pivot_id; known_from_time = max(start.confirmed_time, end.confirmed_time); price_length; time_length; slope; retracement_vs_previous; extension_vs_previous.
- **Type:** hard
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§4. Update monowave spec) · validation

### AUT-33 — impulse-profile-aware-validators
- **Rule:** Impulse rules spec must add profile-aware validators: validate_wave2_retracement(profile); validate_wave3_not_shortest(profile); validate_wave4_overlap(profile); validate_alternation(profile); validate_time_rules(profile).
- **Type:** process
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§5. Update impulse rules spec) · validation

### AUT-34 — manual-tv-output-spec-additions
- **Rule:** Manual TradingView output spec must include: confirmed_time; invalidation; confirmation trigger; manual chart drawing steps; warning if candidate relies on unconfirmed pivot.
- **Type:** process
- **Source:** doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§7. Update manual TradingView output spec) · validation

### AUT-35 — agent-a07-rule-profiles
- **Rule:** A07 Rule Engine Agent rule: "Implement rule profiles. Do not hard-code one interpretation of Elliott Wave rules."
- **Type:** process
- **Source:** doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A07 Rule Engine Agent) · validation

### AUT-36 — task-r001-rule-profile-spec
- **Rule:** TASK_R001 (create specs/12_rule_profile_spec.md): allowed files only that spec; forbidden: no source code changes, no backtest changes, no pattern implementation. Done when `classic_elliott`, `sow_neowave_strict`, `research_experimental` are defined; wave 2 retracement conflict is documented; hard/soft/warning/manual-review rule statuses are defined.
- **Type:** process
- **Source:** doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R001) · validation

### AUT-37 — task-r002-no-lookahead-policy
- **Rule:** TASK_R002 (create specs/13_no_lookahead_and_repainting_policy.md): done when pivot_time and confirmed_time are defined; backtest signal time policy is defined; TradingView repainting rules are documented; request.security() HTF warning is included.
- **Type:** process
- **Source:** doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R002) · validation

### AUT-38 — task-r003-pivot-spec-patch
- **Rule:** TASK_R003 (patch pivot spec for candidate/confirmed lifecycle): done when pivot schema includes lifecycle fields; confirmation methods are listed; no-lookahead notes are included.
- **Type:** process
- **Source:** doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R003) · validation


## SCP · Scope, exclusions & policy

### SCP-01 — NeoWave additions over classic Elliott
- **Rule:** NeoWave additions include: diametric, extracting triangle, two-stage confirmation, neutral triangle, and more (stricter) impulse rules. Impulse is 5 waves; corrective pattern is 3 waves; corrective types: Zigzag 5-3-5, Flat 3-3-5, Triangle 3-3-3-3-3, Diametric 7 legs.
- **Type:** scope
- **Source:** 04_source_page_conversions/Brahmastra_Mentorship_Day_5_6_EW_Composite.md (§Page 1) · mdpack

### SCP-02 — pack purpose and disclaimer
- **Rule:** The pack is for educational use only — a charting and review framework, not investment advice or guaranteed outcomes; converted notes are cleaned/reorganized from image-based handwritten PDFs rather than blind OCR; source page images are included so nothing important is lost.
- **Type:** scope
- **Source:** README.md (§Notes on conversion quality); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (header) · mdpack

### SCP-03 — source attribution
- **Rule:** Source material: "Neo Wave with Ichimoku Cloud" — Ashish Kyal Trading Gurukul / Waves Strategy Advisors (SEBI Registration No. INH000001097); course content covers Elliott Wave basics, impulsive extensions and terminal pattern, corrective zigzag/flat/triangle, application principles, pattern implications, evolving structures (diametric, extracting/neutral triangle), and Ichimoku Cloud.
- **Type:** scope
- **Source:** 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Pages 1, 2, 10) · mdpack

### SCP-04 — duplicate source file
- **Rule:** Sutra_of_Waves_Day_2_Notes_DUPLICATE.pdf is byte-for-byte identical to Sutra_of_Waves_Day_2_Notes.pdf; use Sutra_of_Waves_Day_2_Notes.md and its assets.
- **Type:** scope
- **Source:** 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes_DUPLICATE.md · mdpack

### SCP-05 — bundle is not an auto-trading bot
- **Rule:** The bundle "is **not** an auto-trading bot"; it is a disciplined project scaffold so Codex/Claude can refine one module at a time without getting confused by the full Elliott Wave document library.
- **Type:** scope
- **Source:** BX/README.md (§intro) · specs

### SCP-06 — design principle 2 — detection is not trading
- **Rule:** "Detection is not trading: wave candidates are research objects, not orders."
- **Type:** scope
- **Source:** BX/docs/ARCHITECTURE.md (§Design principles) · specs

### SCP-07 — bundle v0.1.0 status — implemented vs not implemented
- **Rule:** v0.1.0 scaffold, 11 tests passing at generation time. Implemented: data schema, CSV adapter, Alpaca MCP adapter interface, parquet cache, session helper, percent reversal pivots, fractal pivots, mono-wave builder, rule result model, zigzag/flat/impulse validators, pattern scanner, ghost-forward replay, outcome labeler, TradingView note generator, CLI. Not implemented: real Alpaca MCP wiring, ATR pivot detector, triangle/terminal/diametric/advanced NeoWave patterns, chart HTML output, data lake connector, dashboard, paper trading, live trading.
- **Type:** scope
- **Source:** BX/docs/PROJECT_STATUS.md (§Implemented now / Not implemented yet) · specs
- **Notes:** Missing pieces require local environment: Alpaca MCP function names, data lake paths, repo conventions, broker/data credentials, preferred chart output.

### SCP-08 — Version 1 scope
- **Rule:** V1 scope: fetch Alpaca historical data; normalize OHLCV bars; support regular/extended/full session data; resample into useful timeframes; detect swing pivots; create mono-wave table; apply Elliott/NeoWave rule validators; detect limited pattern candidates; generate chart annotations; export TradingView manual notes; run simple historical validation. V1 focuses on manual TradingView support, not auto-trading.
- **Type:** scope
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§3 What Version 1 Must Do) · specs

### SCP-09 — Version 1 non-scope
- **Rule:** No live order placement; no options execution; no short selling automation; no full discretionary NeoWave interpretation; no black-box ML prediction; no automatic final buy/sell recommendations in early phases; no all-pattern detection in one release; no strategy optimization before data and rules are stable.
- **Type:** scope
- **Source:** SM/ElliottWave_Automation_Development_Plan.md (§3 Version 1 Non-Scope) · specs

### SCP-10 — neowave-do-not-automate-v1
- **Rule:** Do not fully automate in V1: Diametric; Neutral triangle; Extracting triangle; Complex corrective combinations; Advanced terminal impulse classification; Reverse logic; Full NeoWave degree resolution.
- **Type:** scope
- **Source:** research_notes/R02_NeoWave_Rules_Clarification.md (§Do not fully automate in V1) · validation

### SCP-11 — feasibility-full-degree-resolution
- **Rule:** Full degree resolution: difficulty Very high, status V3 — needs multi-timeframe hierarchy and human review.
- **Type:** scope
- **Source:** research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix) · validation

### SCP-12 — advanced-neowave-staged
- **Rule:** Diametric, neutral triangle, extracting triangle, terminal impulse, and complex corrections should not be implemented before data, pivot, mono-wave, and basic pattern validation are stable. Mark advanced NeoWave patterns as `manual_review` in V1 and implement as V2 modules.
- **Type:** scope
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§3. NeoWave advanced structures must be staged) · validation

### SCP-13 — do-not-implement-in-v1
- **Rule:** Do not implement in V1: Live order placement; Options execution; ML wave prediction; Advanced NeoWave diametric/extracting/neutral triangle full automation; News/fundamentals integration; Auto wave count certainty claims.
- **Type:** scope
- **Source:** 00_RESEARCH_VALIDATION_MASTER.md (§Do not implement in V1) · validation

### SCP-14 — allowed-research-areas
- **Rule:** Only research improving one of these areas is allowed in the current sprint: 1. Elliott Wave rule validation; 2. NeoWave/SOW rule clarification; 3. Fibonacci rule engineering; 4. TradingView repainting and manual annotation constraints; 5. Alpaca historical data behavior; 6. No-lookahead backtesting design; 7. Manual TradingView workflow output.
- **Type:** scope
- **Source:** 01_RESEARCH_SCOPE_AND_POLICY.md (§Allowed research for current sprint) · validation

### SCP-15 — postponed-research
- **Rule:** Postpone until V1 engine works: ML/DL wave prediction; Computer vision chart pattern detection; Options execution logic; Live broker order routing; Full discretionary NeoWave interpretation; Sentiment/news/fundamental scanners; Portfolio optimization; Auto-trading bots.
- **Type:** scope
- **Source:** 01_RESEARCH_SCOPE_AND_POLICY.md (§Research that must be postponed) · validation

### SCP-16 — v1-allowed-build-scope
- **Rule:** V1 allowed: Alpaca data ingestion; Data normalization/cache; Pivot detection; Mono-wave construction; Rule profiles; Zigzag candidate detection; Flat candidate detection; Basic impulse candidate detection; Manual TradingView output; No-lookahead backtest harness.
- **Type:** scope
- **Source:** 05_FREEZE_CRITERIA_V1.md (§V1 build scope) · validation

### SCP-17 — v1-not-allowed
- **Rule:** V1 not allowed: Live trading; Options execution; Advanced NeoWave full automation; ML prediction; News/fundamental scanner; Auto certainty labels.
- **Type:** scope
- **Source:** 05_FREEZE_CRITERIA_V1.md (§V1 build scope) · validation

### SCP-18 — pack-disclaimer
- **Rule:** The pack is for research, software engineering, and manual chart-study workflow only. It is not financial advice, not a promise of profit, and not a live trading instruction system.
- **Type:** scope
- **Source:** README.md (§Important disclaimer) · validation

