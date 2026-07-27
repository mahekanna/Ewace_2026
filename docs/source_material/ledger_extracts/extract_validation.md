# Extract — ElliottWave_Research_Validation_Pack

Paths in SOURCE are relative to `ElliottWave_Research_Validation_Pack/` (inner pack root).

### [IMPULSE] motive-waves-five-wave-with-trend
- RULE: Motive waves are five-wave structures moving in the direction of the larger trend.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves)
- NOTES: Listed under "Confirmed concepts" as safe to convert into V1 automation specs.

### [IMPULSE] wave2-retrace-less-than-100pct
- RULE: Wave 2 retraces less than 100% of wave 1.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves)
- NOTES: Encoded in V1 yaml as `wave2_retrace_must_be_less_than_pct: 100` under profile `classic_elliott`.

### [IMPULSE] wave4-retrace-less-than-100pct-of-wave3
- RULE: Wave 4 retraces less than 100% of wave 3.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves)
- NOTES: Encoded as `wave4_retrace_must_be_less_than_pct_of_wave3: 100`.

### [IMPULSE] wave3-exceeds-wave1
- RULE: Wave 3 travels beyond wave 1 (`wave3_must_exceed_wave1_end: true`).
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves)

### [IMPULSE] wave3-never-shortest
- RULE: Wave 3 is never the shortest among waves 1, 3, and 5 (`wave3_must_not_be_shortest_among_1_3_5: true`).
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Motive waves)
- NOTES: Reaffirmed as RD-003 "Implement as hard rule in impulse validator", risk High.

### [IMPULSE] impulse-structure-5-3-5-3-5-no-overlap
- RULE: An impulse is a five-wave motive pattern with 5-3-5-3-5 internal structure; normal impulses should not have wave 4 overlap wave 1 (`normal_impulse_wave4_wave1_overlap_allowed: false`). Diagonal or terminal variants must be handled separately.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Impulse, §Hard rules for V1)

### [ZIGZAG] zigzag-structure-5-3-5
- RULE: Zigzag is a corrective pattern subdividing 5-3-5.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves)

### [FLAT] flat-structure-3-3-5
- RULE: Flat is a corrective pattern subdividing 3-3-5.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves)

### [TRIANGLE] triangle-structure-3-3-3-3-3
- RULE: Triangle is a corrective pattern subdividing 3-3-3-3-3.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves)

### [COMPLEX-X] combination-double-triple
- RULE: Combination = double/triple corrective structures (a primary corrective category alongside zigzag, flat, triangle).
- TYPE: guideline
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Corrective waves)

### [IMPULSE] soft-rules-alternation-fib-channeling
- RULE: Soft rules for scoring only: `alternation_between_wave2_and_wave4: score_only`, `fibonacci_relationships: score_only`, `channeling: score_or_annotation`.
- TYPE: guideline
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Soft rules for scoring)

### [IMPULSE] sow-strict-wave2-61.8
- RULE: SOW/NeoWave strict profile: wave 2 retracement limit `wave2_retrace_must_be_less_or_equal_pct: 61.8` (i.e. <=61.8% of wave 1). Must NOT overwrite the classical 100% profile — it is a separate profile `sow_neowave_strict`.
- TYPE: hard
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Conflict with SOW/NeoWave strict rules)
- NOTES: The SOW notes use stricter impulse rules; keeping both avoids forcing one interpretation across all modules.

### [AUTOMATION-SPEC] ruleprofile-system-first
- RULE: Implement a `RuleProfile` system before coding impulse/corrective validators.
- TYPE: process
- SOURCE: research_notes/R01_Elliott_Wave_Core_Rules.md (§Development decision)

### [PROCESS-METHOD] neowave-implement-gradually
- RULE: NeoWave-style analysis is more rule-dense and interpretive than basic Elliott Wave — it includes time, price, balance, similarity, touch-point, confirmation-line, monowave, and pattern-implication concepts — therefore NeoWave rules should be implemented gradually.
- TYPE: process
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Key point)

### [PROCESS-METHOD] neowave-source-priority
- RULE: Source priority for NeoWave: 1) user-provided SOW/NeoWave notes and converted Markdown pack; 2) official NEoWave material and QOW archive; 3) Glenn Neely's formal book/course material if manually available; 4) secondary internet summaries only as low-priority references.
- TYPE: process
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Source priority for NeoWave)

### [PROCESS-METHOD] neowave-archive-topics
- RULE: The official NEoWave archive publicly indexes: Rule of Similarity and Balance, monowave chart detail, wave 2 triangle possibility, Fibonacci measurement, extension importance, dividends/splits and wave structure, cash vs futures chart selection.
- TYPE: scope
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Confirmed research observation)
- NOTES: Supports the need for a dedicated `sow_neowave_strict` rule profile and separate advanced modules.

### [AUTOMATION-SPEC] neowave-v1-implement-now
- RULE: Implement now in V1: Mono-wave table; Price length and time length; Retracement/extension metrics; Similarity/balance score fields; Confirmation-line placeholders; Manual review flags.
- TYPE: process
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§V1 handling / Implement now)

### [SCOPE] neowave-do-not-automate-v1
- RULE: Do not fully automate in V1: Diametric; Neutral triangle; Extracting triangle; Complex corrective combinations; Advanced terminal impulse classification; Reverse logic; Full NeoWave degree resolution.
- TYPE: scope
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Do not fully automate in V1)

### [AUTOMATION-SPEC] neowave-rule-type-classification
- RULE: Engineering classification: Numeric retracement/extension → Implement; Time length comparisons → Implement as metric + rule profile; Similarity/balance → Implement as score/warning; Touch-point rules → Implement as visual/score first; Confirmation lines → Implement as annotation first; Advanced patterns → Manual-review or V2.
- TYPE: process
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification)

### [TIME] time-length-comparisons-as-metric
- RULE: Time length comparisons (NeoWave) are implemented as metric + rule profile in V1, not as standalone hard invalidations.
- TYPE: time
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification)

### [CONFIRMATION-LINES] confirmation-lines-annotation-first
- RULE: Confirmation lines: implement as annotation first (placeholders in V1). Touch-point rules: implement as visual/score first.
- TYPE: guideline
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Engineering classification, §Implement now)

### [PROCESS-METHOD] neowave-as-profiles-first
- RULE: NeoWave must be represented as stricter rule profiles and scoring/annotation modules first. Full advanced pattern automation should wait until the pivot and mono-wave engine are stable.
- TYPE: process
- SOURCE: research_notes/R02_NeoWave_Rules_Clarification.md (§Development decision)

### [FIB] fib-comparison-uses
- RULE: Fibonacci relationships are used to compare: corrective retracement against previous impulse; impulse wave relationships within a sequence; wave C against wave A; projected targets after confirmation.
- TYPE: fib
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Confirmed concepts)

### [FIB] common-retracement-zones
- RULE: Common retracement zones include 38.2%, 50%, and 61.8%.
- TYPE: fib
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Confirmed concepts)

### [FIB] fib-is-scoring-not-predictor
- RULE: Fibonacci should not be coded as a single hard predictor; it should be a measuring and scoring system.
- TYPE: guideline
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Engineering approach)

### [AUTOMATION-SPEC] wave-data-fields
- RULE: Each wave/mono-wave must expose: price_length, abs_price_length, time_length_bars, direction, start_price, end_price, start_time, end_time.
- TYPE: process
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Required data fields)

### [AUTOMATION-SPEC] required-ratio-functions
- RULE: Required ratio functions: retracement_pct(current_wave, previous_wave); extension_ratio(current_wave, reference_wave); time_ratio(current_wave, reference_wave); price_projection(start_point, reference_length, ratio).
- TYPE: process
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Required ratio functions)

### [FIB] supported-retracement-levels
- RULE: Retracement levels to support: 0.236, 0.382, 0.500, 0.618, 0.786, 1.000.
- TYPE: fib
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Fibonacci zones to support)

### [FIB] supported-extension-levels
- RULE: Extension levels to support: 1.000, 1.272, 1.414, 1.618, 2.000, 2.618.
- TYPE: fib
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Fibonacci zones to support)

### [FIB] fib-profile-weights
- RULE: Profile use: `classic_elliott: fib_relationships_required: false, fib_relationships_score_weight: 0.20`; `sow_neowave_strict: fib_relationships_required_for_confirmation: true, fib_relationships_score_weight: 0.30`.
- TYPE: fib
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Rule profile use)

### [SETUP-TRADE] fib-output-per-candidate
- RULE: For every detected pattern candidate, output: Primary fib retracement; Primary fib extension; Invalidation level; Target zone; Confidence impact.
- TYPE: setup
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Manual TradingView output)

### [FIB] fib-shared-utility-decision
- RULE: Build Fibonacci as a shared utility and scoring component, not as a standalone buy/sell engine.
- TYPE: process
- SOURCE: research_notes/R03_Fibonacci_Engineering_Rules.md (§Development decision)

### [VALIDATION] repainting-definition-and-risk
- RULE: Repainting = difference between behavior on historical bars and realtime bars. Pivots and higher-timeframe references are especially vulnerable to repainting.
- TYPE: validation
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Repainting risk)
- NOTES: Per TradingView documentation; critical for wave analysis.

### [INDICATORS] barstate-isconfirmed-behavior
- RULE: `barstate.isconfirmed` is true on historical bars and on the closing update of a realtime bar; it can help avoid using a still-forming realtime bar. Limitation: it does not work when used inside `request.security()`.
- TYPE: indicator
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§barstate.isconfirmed)

### [VALIDATION] htf-request-security-leak
- RULE: Higher-timeframe data requested through `request.security()` can leak future information if lookahead settings are misused; using lookahead without offsetting the expression makes historical results appear to know future values.
- TYPE: validation
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Higher-timeframe data)

### [VALIDATION] pine-helper-policy
- RULE: No Pine helper script may use future-leaking higher-timeframe logic. No Pine helper script may treat a realtime unconfirmed bar as a confirmed signal. No Pine helper script may claim non-repainting if it uses pivot confirmation that requires future bars without showing confirmation delay.
- TYPE: hard
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Pine helper policy)

### [PROCESS-METHOD] tv-output-language-policy
- RULE: TradingView outputs should use language like "Possible candidate / Confirmed after break / Invalid if level breaks / Manual review required" and avoid "Guaranteed wave count / Immediate buy/sell / Non-repainting prediction".
- TYPE: process
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Manual workflow policy)

### [AUTOMATION-SPEC] add-spec-13-no-lookahead
- RULE: Add `specs/13_no_lookahead_and_repainting_policy.md` as a required future spec.
- TYPE: process
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Required future spec)

### [INDICATORS] pine-confirmed-condition-concept
- RULE: Suggested Pine helper concept: `confirmed_condition = barstate.isconfirmed and condition`. For higher-timeframe usage, the final Pine helper must follow TradingView's non-repainting HTF guidance and must be reviewed separately.
- TYPE: indicator
- SOURCE: research_notes/R04_TradingView_Repainting_And_Alerts.md (§Suggested Pine helper rules)
- NOTES: Marked "Concept only, not final code".

### [DATA] alpaca-10yr-capability
- RULE: User tested Alpaca MCP with Claude and confirmed approximately 10 years of data availability including extended-hours data. Treat tested MCP behavior as the practical account-level capability while using official Alpaca docs as the API contract reference.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§User-confirmed capability)

### [DATA] alpaca-timeframes-and-pagination
- RULE: Alpaca single-symbol historical bars endpoint supports timeframes: 1-59 minutes; 1-23 hours; 1 day; 1 week; 1, 2, 3, 4, 6, or 12 months. The endpoint has pagination and requires checking `next_page_token`.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Officially relevant API behavior)

### [DATA] required-dataset-metadata
- RULE: Every cached dataset must include metadata: symbol, timeframe, source: alpaca, feed: iex|sip|other, adjustment_profile: raw|split|dividend|spin-off|all, session_profile: regular|extended|full, asof: YYYY-MM-DD or null, start: datetime, end: datetime, timezone: America/New_York, retrieved_at: datetime, mcp_server_version: optional.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Required metadata)

### [DATA] adjustment-policy-split-default
- RULE: Split discontinuities can distort wave counts, so: Default wave-analysis profile = split-adjusted; Raw data retained for execution/reference/latest price comparison; All-adjusted data = optional research profile. The system must clearly show which adjustment profile was used.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Adjustment policy)

### [DATA] session-policy-regular-default
- RULE: Default V1 wave analysis uses regular session only (`v1_default: session_profile: regular`). Extended-hours data must be stored separately because overnight/pre-market candles can create pivots that do not appear on regular-session TradingView charts. Optional profile: `session_profile: extended, use_case: gap/premarket/manual review`.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Session policy)

### [DATA] feed-policy-iex-vs-sip
- RULE: IEX is the no-subscription feed representing a single exchange; SIP is consolidated across US exchanges. The project must store `feed` explicitly to avoid mixing data quality profiles.
- TYPE: hard
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Feed policy)

### [DATA] alpaca-ingestion-decisions
- RULE: Development decisions: build Alpaca ingestion before Elliott rules; cache data as parquet; store metadata JSON beside each parquet file; follow pagination until complete; keep regular and extended sessions separate; keep raw and split-adjusted data distinguishable.
- TYPE: process
- SOURCE: research_notes/R05_Alpaca_Data_Behavior.md (§Development decisions)

### [VALIDATION] no-lookahead-core-rule
- RULE: The system must never enter, exit, score, or confirm a trade using data that was not available at that time.
- TYPE: hard
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Core rule)

### [VALIDATION] pivot-two-timestamps
- RULE: Every pivot has two timestamps: `pivot_time` = the actual turning candle; `confirmed_time` = first candle where the algorithm could know the pivot. A backtest may display the pivot marker at `pivot_time`, but any signal or trade action can only occur at or after `confirmed_time`.
- TYPE: hard
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Pivot timing rule)

### [VALIDATION] pivot-lifecycle-states
- RULE: Pivot lifecycle: candidate → confirmed → used_in_pattern; candidate → invalidated; confirmed → expired.
- TYPE: hard
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Pivot lifecycle)

### [VALIDATION] test-pivot-not-usable-before-confirmation
- RULE: Test 1: Given a swing high at bar 100 and confirmation occurs at bar 106, the backtest must not enter or exit using this pivot before bar 106.
- TYPE: validation
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 1)

### [VALIDATION] test-pattern-confirmation-is-max-pivot-confirmation
- RULE: Test 2: Given a zigzag candidate requiring pivots A, B, C, the pattern confirmation time is max(confirmed_time_A, confirmed_time_B, confirmed_time_C).
- TYPE: validation
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 2)

### [VALIDATION] test-no-future-bars-in-rolling
- RULE: Test 3: Indicators, pivots, waves, and pattern scores must use only bars <= current bar (no future-bar access in rolling calculations).
- TYPE: validation
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 3)

### [VALIDATION] test-annotation-vs-signal-separation
- RULE: Test 4: Chart may draw pivot at historical turning point; signal report must display confirmation delay.
- TYPE: validation
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Test 4)

### [VALIDATION] trade-log-required-fields
- RULE: Every trade log must include: signal_time, execution_time, latest_known_pivot_time, latest_known_pivot_confirmed_time, pattern_candidate_id, rule_profile, lookahead_audit_status.
- TYPE: hard
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Backtest output requirement)

### [VALIDATION] forbidden-lookahead-behaviors
- RULE: Forbidden: Entering at the pivot candle when pivot was confirmed later; Using centered rolling windows for signal decisions; Using final pattern labels to trade earlier candles; Using future higher-timeframe bar values; Using adjusted data for backtest but raw prices for execution without documenting it.
- TYPE: hard
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Forbidden behavior)

### [VALIDATION] test-file-before-backtests
- RULE: Create `test_no_lookahead.py` before implementing backtests.
- TYPE: process
- SOURCE: research_notes/R06_No_Lookahead_Backtesting_Policy.md (§Development decision)

### [SETUP-TRADE] output-is-study-plan-not-signals
- RULE: The system should output a manual chart-study plan, not blind buy/sell signals.
- TYPE: setup
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§Output principle)

### [AUTOMATION-SPEC] manual-output-required-sections
- RULE: Required output sections: Symbol; Timeframe; Session profile; Adjustment profile; Rule profile; Detected candidate pattern; Pattern confidence; Confirmed pivots; Candidate pivots; Invalidation level; Confirmation trigger; Fibonacci zone; Channel/line instruction; TradingView drawing steps; Manual review warnings; No-lookahead confirmation delay.
- TYPE: process
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§Required output sections)

### [ZIGZAG] example-zigzag-study-plan
- RULE: Example zigzag correction workflow (TSLA 1H, sow_neowave_strict): mark pivots 0, A, B; draw 0-B line; draw Fibonacci projection of A from B; watch C zone near 1.0x to 1.618x of A; do not treat C as complete until reversal/pivot confirmation.
- TYPE: setup
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§Example output)
- NOTES: Example lists confirmed pivots with pivot and confirmed timestamps (e.g. Pivot 0: 2026-04-01 10:00, confirmed 2026-04-01 13:00) and warning "Pivot C is not confirmed yet. Do not backtest entry at C pivot candle."

### [ZIGZAG] zigzag-bearish-invalidation
- RULE: Candidate invalid if price breaks above B before C completion in a bearish setup.
- TYPE: setup
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§Example output / Invalidation)

### [AUTOMATION-SPEC] tv-object-export-idea
- RULE: Future versions can export TradingView objects as JSON: {"lines": [], "labels": [], "fib_anchors": [], "notes": []}.
- TYPE: process
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§TradingView object export idea)

### [PROCESS-METHOD] manual-output-before-live
- RULE: Manual output should be implemented before live signals or automation.
- TYPE: process
- SOURCE: research_notes/R07_Manual_TradingView_Workflow.md (§Development decision)

### [AUTOMATION-SPEC] feasibility-monowave
- RULE: Mono-wave: difficulty Low, V1 status Implement — foundation for all patterns.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [ZIGZAG] feasibility-zigzag
- RULE: Zigzag: difficulty Medium, V1 status Implement — clear A-B-C structure; good first corrective module.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [FLAT] feasibility-flat
- RULE: Flat: difficulty Medium, V1 status Implement after zigzag — clear A-B-C 3-3-5 structure but variants require caution.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [IMPULSE] feasibility-basic-impulse
- RULE: Basic impulse: difficulty Medium/High, V1 status Implement after mono-wave metrics — requires internal structure and overlap/extension validation.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [TRIANGLE] feasibility-triangle
- RULE: Triangle: difficulty High, V1 status Candidate/manual review — easy to label too early; requires time and boundaries.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [TERMINAL] feasibility-terminal-diagonal
- RULE: Terminal impulse / diagonal: difficulty High, V1 status V2 or warning — needs exception handling for overlap.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [COMPLEX-X] feasibility-double-triple-combination
- RULE: Double/triple combination: difficulty High, V1 status V2 — requires reliable recognition of multiple sub-patterns.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [DIAMETRIC] feasibility-diametric
- RULE: Diametric: difficulty Very high, V1 status V2/manual review — NeoWave-specific and interpretive.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [TRIANGLE] feasibility-neutral-triangle
- RULE: Neutral triangle: difficulty Very high, V1 status V2/manual review — requires stricter NeoWave logic.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [TRIANGLE] feasibility-extracting-triangle
- RULE: Extracting triangle: difficulty Very high, V1 status V2/manual review — requires mature triangle engine.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [SCOPE] feasibility-full-degree-resolution
- RULE: Full degree resolution: difficulty Very high, status V3 — needs multi-timeframe hierarchy and human review.
- TYPE: scope
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Feasibility matrix)

### [PROCESS-METHOD] v1-pattern-order
- RULE: V1 pattern order: 1. Mono-wave table; 2. Zigzag candidate; 3. Flat candidate; 4. Basic impulse candidate; 5. Triangle annotation/manual-review.
- TYPE: process
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§V1 pattern order)

### [VALIDATION] confidence-policy-no-100pct
- RULE: No pattern should output 100% certainty. Use states: Candidate; Probable; Confirmed by rule profile; Manual review required; Invalidated.
- TYPE: hard
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Confidence policy)

### [PROCESS-METHOD] one-pattern-per-task-card
- RULE: Do not build all pattern modules at once. Use one pattern module per task card.
- TYPE: process
- SOURCE: research_notes/R08_Pattern_Automation_Feasibility.md (§Development decision)

### [PROCESS-METHOD] source-bibliography
- RULE: Canonical source list (accessed 2026-06-13): Elliott Wave International Waveopedia pages (Motive Waves, Impulse, Corrective Waves, Zigzags, Flats, Triangles, Fibonacci Relationships, Channeling, Alternation); NEoWave QOW Archive; TradingView Pine Script docs (Repainting, Bar States, Other Timeframes and Data); Alpaca Market Data docs (About Market Data API, Historical Stock Data, Historical Bars Single Symbol); user-provided pack (Brahmastra mentorship Day 5 notes, Sutra of Waves Day 1 and Day 2 notes, SOW Fibonacci May 2026 notes, SOW/Neo Wave training deck, converted Markdown pack, ElliottWave automation roadmap, agent prompt pack).
- TYPE: process
- SOURCE: research_notes/R09_Source_Bibliography.md (§all)

### [PROCESS-METHOD] research-pipeline-philosophy
- RULE: Build philosophy: Research source → verified rule → engineering interpretation → spec update → coding task. Never: Research source → direct coding agent context.
- TYPE: process
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§Final recommended build philosophy)
- NOTES: Research should be a controlled validation sprint; the project must not absorb unlimited EW/NeoWave/Fibonacci/TradingView/broker-data theory.

### [IMPULSE] master-pattern-structure-summary
- RULE: Stable classical structure: motive waves move with the larger trend in five waves; corrective waves are generally three-wave or variations; impulse is 5-3-5-3-5 with normally no overlap between wave 4 and wave 1; zigzag is A-B-C subdividing 5-3-5; flat is A-B-C subdividing 3-3-5; triangle is A-B-C-D-E subdividing 3-3-3-3-3.
- TYPE: hard
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§1. Classical Elliott Wave core rules are stable enough for V1)
- NOTES: Engineering decision: implement classical Elliott rules as formal rule profile `classic_elliott`.

### [IMPULSE] wave2-profile-split-100-vs-61.8
- RULE: `rule_profiles: classic_elliott: wave2_max_retrace_pct_of_wave1: 100; sow_neowave_strict: wave2_max_retrace_pct_of_wave1: 61.8`.
- TYPE: hard
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§2. SOW / NeoWave rules need a stricter and separate rule profile)
- NOTES: SOW/NeoWave course notes are stricter on retracement, time, confirmation lines, touch points, and pattern balance; do not merge blindly with classical Elliott Wave. Engineering decision: create profile `sow_neowave_strict`. Same split repeated in 02_SOURCE_QUALITY_POLICY.md (§Example conflict: Wave 2 retracement).

### [SCOPE] advanced-neowave-staged
- RULE: Diametric, neutral triangle, extracting triangle, terminal impulse, and complex corrections should not be implemented before data, pivot, mono-wave, and basic pattern validation are stable. Mark advanced NeoWave patterns as `manual_review` in V1 and implement as V2 modules.
- TYPE: scope
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§3. NeoWave advanced structures must be staged)

### [VALIDATION] tv-repainting-hard-risk
- RULE: TradingView realtime bars and historical bars can behave differently; higher-timeframe requests can repaint unless handled carefully; `barstate.isconfirmed` is useful on normal chart bars but does not work inside `request.security()`. Engineering decision: add `NO_LOOKAHEAD_AND_REPAINTING_POLICY.md` to main specs and tests.
- TYPE: hard
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§4. TradingView repainting is a hard risk)

### [DATA] alpaca-explicit-profiles-decision
- RULE: The system must not treat all bars as equal. Store `session_profile`, `adjustment_profile`, `feed`, `source`, and `asof` in metadata.
- TYPE: hard
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§5. Alpaca data must be stored with explicit session and adjustment profiles)

### [VALIDATION] backtest-uses-confirmation-time
- RULE: A swing pivot is only known after a reversal or confirmation rule; a backtest that enters at the pivot candle uses future information. Every pivot has `pivot_time` (actual market turning candle) and `confirmed_time` (first candle where algorithm could know the pivot). Trades and alerts can only use `confirmed_time`.
- TYPE: hard
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§6. Backtesting must use confirmation time, not pivot time)

### [AUTOMATION-SPEC] new-specs-to-add
- RULE: New documentation to add: specs/12_rule_profile_spec.md; specs/13_no_lookahead_and_repainting_policy.md; specs/14_data_adjustment_and_session_policy.md; specs/15_pattern_feasibility_matrix.md; specs/16_manual_tradingview_output_spec.md.
- TYPE: process
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§New documentation to add to the main project)
- NOTES: 04_DOC_UPDATE_MATRIX.md assigns priorities: specs 12 and 13 Critical; specs 14, 15, 16 High.

### [PROCESS-METHOD] v1-build-sequence
- RULE: Recommended V1 build sequence: 1. Alpaca Data Engine; 2. Data adjustment/session metadata; 3. Pivot Engine with candidate vs confirmed states; 4. MonoWave Engine; 5. Rule Profile Engine; 6. Zigzag Detector; 7. Flat Detector; 8. Impulse Detector; 9. TradingView Manual Annotation Output; 10. Backtest Harness with no-lookahead tests.
- TYPE: process
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§Recommended V1 build sequence after this research)

### [SCOPE] do-not-implement-in-v1
- RULE: Do not implement in V1: Live order placement; Options execution; ML wave prediction; Advanced NeoWave diametric/extracting/neutral triangle full automation; News/fundamentals integration; Auto wave count certainty claims.
- TYPE: scope
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§Do not implement in V1)

### [PROCESS-METHOD] final-control-rule
- RULE: If a new research item does not change a spec, test, or task card, it should remain in research notes only and must not enter coding context.
- TYPE: process
- SOURCE: 00_RESEARCH_VALIDATION_MASTER.md (§Final control rule)

### [SCOPE] allowed-research-areas
- RULE: Only research improving one of these areas is allowed in the current sprint: 1. Elliott Wave rule validation; 2. NeoWave/SOW rule clarification; 3. Fibonacci rule engineering; 4. TradingView repainting and manual annotation constraints; 5. Alpaca historical data behavior; 6. No-lookahead backtesting design; 7. Manual TradingView workflow output.
- TYPE: scope
- SOURCE: 01_RESEARCH_SCOPE_AND_POLICY.md (§Allowed research for current sprint)

### [SCOPE] postponed-research
- RULE: Postpone until V1 engine works: ML/DL wave prediction; Computer vision chart pattern detection; Options execution logic; Live broker order routing; Full discretionary NeoWave interpretation; Sentiment/news/fundamental scanners; Portfolio optimization; Auto-trading bots.
- TYPE: scope
- SOURCE: 01_RESEARCH_SCOPE_AND_POLICY.md (§Research that must be postponed)

### [PROCESS-METHOD] research-acceptance-test
- RULE: A research item is accepted only if it converts into at least one of: a spec change, a test case, a task card, a rule profile setting, a manual TradingView instruction, or a warning/limitation note. Otherwise it remains background reading and does not affect development.
- TYPE: process
- SOURCE: 01_RESEARCH_SCOPE_AND_POLICY.md (§Research acceptance test)

### [PROCESS-METHOD] llm-context-control
- RULE: Coding agents must not browse or interpret broad Elliott Wave theory. They receive only: 1. Shared system rules; 2. The relevant spec file; 3. The current task card; 4. The specific decision record related to that task.
- TYPE: process
- SOURCE: 01_RESEARCH_SCOPE_AND_POLICY.md (§Context-control rule for LLMs)
- NOTES: Repeated as the "Core rule" in README.md.

### [PROCESS-METHOD] research-item-format
- RULE: Every research item must follow the format: Topic; Source; Observed claim; Engineering interpretation; Decision; Affected files; Affected agents; Risk level; Implementation status.
- TYPE: process
- SOURCE: 01_RESEARCH_SCOPE_AND_POLICY.md (§Research sprint output format)

### [PROCESS-METHOD] source-ranking-tiers
- RULE: Source hierarchy: Tier 1 project source of truth (user-provided mentorship PDFs and converted Markdown pack; existing project roadmap and agent prompt pack; user-confirmed Alpaca MCP behavior); Tier 2 official documentation (TradingView Pine docs, Alpaca API docs, Elliott Wave International Waveopedia, NEoWave official archive); Tier 3 technical implementation references (Python packages, backtesting frameworks, exchange calendars); Tier 4 secondary commentary (blogs, YouTube, forums, generic trading education). Tier 4 sources must not create hard rules unless verified against Tier 1 or Tier 2.
- TYPE: process
- SOURCE: 02_SOURCE_QUALITY_POLICY.md (§Source ranking)

### [PROCESS-METHOD] source-conflict-handling
- RULE: When sources conflict: 1. Do not overwrite existing docs silently; 2. Create a decision record; 3. Decide whether the conflict should be handled by separate rule profiles; 4. Add tests for both profiles if both are supported.
- TYPE: process
- SOURCE: 02_SOURCE_QUALITY_POLICY.md (§Conflict handling)

### [IMPULSE] wave2-conflict-example
- RULE: Classical Elliott Wave sources commonly state wave 2 must not retrace 100% or more of wave 1; SOW/NeoWave course material uses a stricter 61.8% rule. Decision: `classic_elliott: wave2_max_retrace_pct_of_wave1: 100; sow_neowave_strict: wave2_max_retrace_pct_of_wave1: 61.8`.
- TYPE: hard
- SOURCE: 02_SOURCE_QUALITY_POLICY.md (§Example conflict: Wave 2 retracement)
- NOTES: "This avoids forcing one interpretation across all modules."

### [PROCESS-METHOD] citation-rule
- RULE: Every research note must include a Sources section with URLs and access date. Avoid copying long source text into the project; summarize and translate into engineering decisions.
- TYPE: process
- SOURCE: 02_SOURCE_QUALITY_POLICY.md (§Citation rule for docs)

### [AUTOMATION-SPEC] RD-001-rule-profiles
- RULE: RD-001: Add separate `classic_elliott`, `sow_neowave_strict`, and `research_experimental` profiles. Rule type Architecture, Accepted, affects `rules/` and `specs/12_rule_profile_spec.md`, risk High.
- TYPE: process
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [IMPULSE] RD-002-wave2-retracement
- RULE: RD-002: Classical profile uses `<100%`; SOW/NeoWave strict profile uses `<=61.8%` for wave 2 retracement. Hard/profile-specific, Accepted, impulse validator, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [IMPULSE] RD-003-wave3-not-shortest
- RULE: RD-003: Wave 3 not shortest — implement as hard rule in impulse validator. Accepted, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [TERMINAL] RD-004-wave4-overlap-exception
- RULE: RD-004: In `classic_elliott`, non-overlap of wave 4 with wave 1 is hard for normal impulse; allow exception only in diagonal/terminal module. Hard with exception, Accepted, impulse/terminal modules, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [IMPULSE] RD-005-alternation-soft
- RULE: RD-005: Treat alternation as guideline/score, not hard invalidation. Soft, Accepted, pattern scoring, risk Medium.
- TYPE: guideline
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [CONFIRMATION-LINES] RD-006-channeling-support-only
- RULE: RD-006: Use channeling as target/validation support, not initial pattern proof. Soft/visual, Accepted, chart annotation, risk Medium.
- TYPE: guideline
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [ZIGZAG] RD-007-zigzag-first-detector
- RULE: RD-007: Implement first corrective detector: A-B-C, 5-3-5 approximation, B retracement profile, C target zone. Pattern V1, Accepted, corrective detector, risk Medium.
- TYPE: setup
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [FLAT] RD-008-flat-after-zigzag
- RULE: RD-008: Implement flat after zigzag: A-B-C, 3-3-5 approximation, B near/beyond A start. Running flat must be warning/manual-review. Pattern V1, Accepted, risk Medium.
- TYPE: setup
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [TRIANGLE] RD-009-triangle-manual-review
- RULE: RD-009: Implement triangle as candidate/manual-review in V1; full triangle confirmation later. Manual-review, Accepted, triangle detector, risk High.
- TYPE: scope
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [DIAMETRIC] RD-010-advanced-neowave-v2
- RULE: RD-010: Diametric, neutral triangle, extracting triangle, and complex correction are V2 unless only annotated manually. Postpone, Accepted, NeoWave modules, risk High.
- TYPE: scope
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [VALIDATION] RD-011-pivot-timestamps
- RULE: RD-011: Every pivot must store `pivot_time` and `confirmed_time`. Backtests use only `confirmed_time`. Hard, Accepted, pivot engine/backtest, risk Critical.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [VALIDATION] RD-012-lifecycle-states
- RULE: RD-012: Pivots and patterns must have lifecycle states: `candidate`, `confirmed`, `invalidated`, `expired`. Hard, Accepted, all engines, risk Critical.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [VALIDATION] RD-013-htf-security-non-repainting
- RULE: RD-013: Pine helpers must avoid future-leaking `request.security()` patterns. Non-repainting HTF values require confirmed/offset logic. Hard, Accepted, Pine helpers, risk Critical.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [INDICATORS] RD-014-barstate-limitation
- RULE: RD-014: Do not rely on `barstate.isconfirmed` inside `request.security()`. Hard, Accepted, Pine helpers, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [DATA] RD-015-adjustment-profile
- RULE: RD-015: Store raw and adjusted variants or at least explicit `adjustment_profile`. Default analysis profile: split-adjusted; raw retained for execution/reference. Data policy, Accepted, data engine, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [DATA] RD-016-session-profile
- RULE: RD-016: Store `regular`, `extended`, and `full` session profiles separately. Default V1 pattern analysis: regular session. Data policy, Accepted, data engine, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [DATA] RD-017-pagination
- RULE: RD-017: Data fetcher must follow `next_page_token` until complete or capped. Hard, Accepted, data engine, risk High.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [DATA] RD-018-feed-metadata
- RULE: RD-018: Store `feed` in metadata; distinguish IEX vs SIP. Hard, Accepted, data engine, risk Medium.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [SETUP-TRADE] RD-019-manual-study-plan
- RULE: RD-019: Output should be a manual study plan, not a blind buy/sell signal. Product policy, Accepted, report/annotation engine, risk High.
- TYPE: setup
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [VALIDATION] RD-020-no-entry-before-confirmation
- RULE: RD-020: No strategy can enter at a pivot before the pivot is confirmed. Hard, Accepted, backtest engine, risk Critical.
- TYPE: hard
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§decision table)

### [PROCESS-METHOD] decision-states
- RULE: Decision states: Accepted = add to project specs/tasks; Deferred = keep in research notes, do not build now; Rejected = do not use; Needs Review = requires user or manual domain review.
- TYPE: process
- SOURCE: 03_RESEARCH_DECISION_LOG.md (§Decision states)
- NOTES: Coding agents should follow the decision log only when their task explicitly references it.

### [AUTOMATION-SPEC] doc-update-matrix-existing-files
- RULE: Existing docs to update: DEVELOPMENT_ROADMAP.md (add Research Validation Sprint before coding); LLM_WORKFLOW_RULES.md (coding agents cannot read broad research notes unless task-specific); specs/03_pivot_detection_spec.md (add pivot_time, confirmed_time, lifecycle states); specs/05_impulse_rules_spec.md (rule profile handling for wave 2 retracement conflict); specs/06_corrective_rules_spec.md (zigzag/flat/triangle V1/V2 status); specs/10_backtest_spec.md (confirmation-time-only trade policy); agents/A04_Pivot_Engine_Agent.md (no-lookahead confirmation contract); agents/A07_Rule_Engine_Agent.md (rule profile system); agents/A11_Backtest_Agent.md (mandatory lookahead audit); tasks/TASK_004_PIVOT_ENGINE.md (tests for candidate/confirmed pivot timestamps); tasks/TASK_010_BACKTEST_ENGINE.md (tests preventing pivot-time entries).
- TYPE: process
- SOURCE: 04_DOC_UPDATE_MATRIX.md (§Existing docs to update)

### [PROCESS-METHOD] research-agents-propose-only
- RULE: Files that must not be modified by research agents: src/, tests/, notebooks/. Research agents propose changes only; coding agents implement after the decision log is accepted.
- TYPE: process
- SOURCE: 04_DOC_UPDATE_MATRIX.md (§Files that should not be modified by research agents)

### [PROCESS-METHOD] v1-freeze-checklist
- RULE: Documentation freeze checklist before coding: PROJECT_CHARTER.md confirms V1 scope; DATA_CONTRACT.md includes Alpaca session/adjustment/feed metadata; PIVOT_DETECTION_SPEC.md includes pivot_time and confirmed_time; RULE_PROFILE_SPEC.md exists; NO_LOOKAHEAD_AND_REPAINTING_POLICY.md exists; PATTERN_FEASIBILITY_MATRIX.md exists; MANUAL_TRADINGVIEW_OUTPUT_SPEC.md exists; agent task cards mention allowed files and forbidden changes; backtest spec states that signals can only use data available at the signal time.
- TYPE: process
- SOURCE: 05_FREEZE_CRITERIA_V1.md (§Documentation freeze checklist)

### [SCOPE] v1-allowed-build-scope
- RULE: V1 allowed: Alpaca data ingestion; Data normalization/cache; Pivot detection; Mono-wave construction; Rule profiles; Zigzag candidate detection; Flat candidate detection; Basic impulse candidate detection; Manual TradingView output; No-lookahead backtest harness.
- TYPE: scope
- SOURCE: 05_FREEZE_CRITERIA_V1.md (§V1 build scope)

### [SCOPE] v1-not-allowed
- RULE: V1 not allowed: Live trading; Options execution; Advanced NeoWave full automation; ML prediction; News/fundamental scanner; Auto certainty labels.
- TYPE: scope
- SOURCE: 05_FREEZE_CRITERIA_V1.md (§V1 build scope)

### [PROCESS-METHOD] freeze-rule
- RULE: After freeze criteria are accepted, no new theory is allowed into V1 unless it fixes a bug, prevents lookahead bias, or clarifies an existing rule.
- TYPE: process
- SOURCE: 05_FREEZE_CRITERIA_V1.md (§Freeze rule)

### [PROCESS-METHOD] research-vs-coding-agent-separation
- RULE: Use research agents to verify and classify rules; use coding agents to implement frozen specs; do not mix them. Recommended agent sequence: 1. Elliott Rule Validation Agent; 2. NeoWave Clarification Agent; 3. Alpaca Data Research Agent; 4. TradingView Repainting Agent; 5. No-Lookahead Audit Agent; 6. Documentation Patch Agent; 7. Coding Agent.
- TYPE: process
- SOURCE: 06_AGENT_RESEARCH_PROMPTS.md (§Principle, §Recommended agent sequence)

### [PROCESS-METHOD] research-agent-output-format
- RULE: Every research agent must output: Findings; Accepted decisions; Deferred decisions; Rejected ideas; Affected docs; Affected tests; Risks; Next coding task.
- TYPE: process
- SOURCE: 06_AGENT_RESEARCH_PROMPTS.md (§Research agent output format)

### [PROCESS-METHOD] coding-agent-no-theory-decisions
- RULE: A coding agent must never decide a new Elliott Wave theory interpretation by itself; it must ask for a decision record update. Use prompt cards one at a time — do not give all prompt cards to one agent.
- TYPE: process
- SOURCE: 06_AGENT_RESEARCH_PROMPTS.md (§Coding agent rule, §Use prompt cards)

### [PROCESS-METHOD] pack-recommended-use-order
- RULE: Recommended use order: 1. Read 00_RESEARCH_VALIDATION_MASTER.md; 2. Read 03_RESEARCH_DECISION_LOG.md; 3. Apply doc_updates/UPDATE_01_SPECS_TO_MODIFY.md; 4. Add prompt cards only when needed; 5. Freeze Version 1 using 05_FREEZE_CRITERIA_V1.md; 6. Begin coding from data engine and pivot engine only.
- TYPE: process
- SOURCE: README.md (§Recommended use order)

### [PROCESS-METHOD] most-important-pack-decisions
- RULE: Most important decisions: use rule profiles `classic_elliott`, `sow_neowave_strict`, `research_experimental`; keep NeoWave advanced patterns as manual-review or V2 until data/pivot/monowave foundation is stable; treat TradingView repainting and no-lookahead as hard engineering constraints; store Alpaca data with explicit adjustment/session profiles; backtests must trigger at pivot confirmation time, not at the historical pivot candle.
- TYPE: process
- SOURCE: README.md (§Most important project decisions in this pack)

### [SCOPE] pack-disclaimer
- RULE: The pack is for research, software engineering, and manual chart-study workflow only. It is not financial advice, not a promise of profit, and not a live trading instruction system.
- TYPE: scope
- SOURCE: README.md (§Important disclaimer)

### [AUTOMATION-SPEC] rule-profile-spec-full-yaml
- RULE: `specs/12_rule_profile_spec.md` required content: `classic_elliott: wave2_max_retrace_pct: 100, wave3_not_shortest: hard, wave4_overlap_wave1: fail, alternation: score`; `sow_neowave_strict: wave2_max_retrace_pct: 61.8, wave3_not_shortest: hard, wave4_overlap_wave1: fail_except_terminal, wave2_time_vs_wave1: warn_or_fail_by_config, wave4_time_vs_wave3: warn_or_fail_by_config, alternation: score_required`; `research_experimental: allow_manual_override: true, strict_invalidations: false`.
- TYPE: hard
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md)

### [TIME] sow-time-rules-wave2-wave4
- RULE: In `sow_neowave_strict`: `wave2_time_vs_wave1: warn_or_fail_by_config` and `wave4_time_vs_wave3: warn_or_fail_by_config` (time-comparison rules configurable between warning and failure).
- TYPE: time
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md)

### [TERMINAL] wave4-overlap-fail-except-terminal
- RULE: `classic_elliott: wave4_overlap_wave1: fail`; `sow_neowave_strict: wave4_overlap_wave1: fail_except_terminal` — overlap of wave 4 into wave 1 fails validation except in the terminal-impulse case for the strict profile.
- TYPE: hard
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§1. Add specs/12_rule_profile_spec.md)

### [AUTOMATION-SPEC] no-lookahead-spec-contents
- RULE: `specs/13_no_lookahead_and_repainting_policy.md` must include: pivot_time vs confirmed_time; candidate vs confirmed states; TradingView repainting warning; request.security HTF rule; backtest signal timing; forbidden future access.
- TYPE: validation
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§2. Add specs/13_no_lookahead_and_repainting_policy.md)

### [AUTOMATION-SPEC] pivot-schema-fields
- RULE: Pivot spec fields: pivot_id: str; symbol: str; timeframe: str; pivot_time: datetime; confirmed_time: datetime; pivot_type: Literal['high','low']; price: float; confirmation_method: str; confirmation_bars: int; confirmation_price_move_pct: float | None; status: Literal['candidate','confirmed','invalidated','expired'].
- TYPE: hard
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§3. Update pivot spec)

### [AUTOMATION-SPEC] monowave-schema-fields
- RULE: Monowave spec fields: start_pivot_id; end_pivot_id; known_from_time = max(start.confirmed_time, end.confirmed_time); price_length; time_length; slope; retracement_vs_previous; extension_vs_previous.
- TYPE: hard
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§4. Update monowave spec)

### [AUTOMATION-SPEC] impulse-profile-aware-validators
- RULE: Impulse rules spec must add profile-aware validators: validate_wave2_retracement(profile); validate_wave3_not_shortest(profile); validate_wave4_overlap(profile); validate_alternation(profile); validate_time_rules(profile).
- TYPE: process
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§5. Update impulse rules spec)

### [VALIDATION] backtest-hard-test-known-from-time
- RULE: Backtest spec hard test: No trade can be generated using a pivot, monowave, or pattern before its known_from_time.
- TYPE: hard
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§6. Update backtest spec)

### [AUTOMATION-SPEC] manual-tv-output-spec-additions
- RULE: Manual TradingView output spec must include: confirmed_time; invalidation; confirmation trigger; manual chart drawing steps; warning if candidate relies on unconfirmed pivot.
- TYPE: process
- SOURCE: doc_updates/UPDATE_01_SPECS_TO_MODIFY.md (§7. Update manual TradingView output spec)

### [VALIDATION] agent-a04-pivot-contract
- RULE: A04 Pivot Engine Agent rule: "You must store both pivot_time and confirmed_time. You must not expose a pivot as usable for signals until confirmed_time."
- TYPE: hard
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A04 Pivot Engine Agent)

### [VALIDATION] agent-a05-monowave-known-from
- RULE: A05 MonoWave Engine Agent rule: "A mono-wave is only known when both endpoint pivots are confirmed. Use known_from_time = max(endpoint confirmed times)."
- TYPE: hard
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A05 MonoWave Engine Agent)

### [AUTOMATION-SPEC] agent-a07-rule-profiles
- RULE: A07 Rule Engine Agent rule: "Implement rule profiles. Do not hard-code one interpretation of Elliott Wave rules."
- TYPE: process
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A07 Rule Engine Agent)

### [PROCESS-METHOD] agent-a08-one-pattern-per-task
- RULE: A08 Pattern Agent rule: "Only implement one pattern per task. Advanced NeoWave patterns are manual-review unless a task specifically says otherwise."
- TYPE: process
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A08 Pattern Agent)

### [VALIDATION] agent-a11-backtest-fail-conditions
- RULE: A11 Backtest Agent rule: "Backtest must fail if any signal uses future data, centered windows, unconfirmed pivots, or final labels unavailable at that time."
- TYPE: hard
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A11 Backtest Agent)

### [SETUP-TRADE] agent-a14-tv-output-rules
- RULE: A14 TradingView Output Agent rule: "Output manual charting instructions, not direct trading orders. Every candidate must include invalidation and confirmation state."
- TYPE: setup
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§A14 TradingView Output Agent)

### [PROCESS-METHOD] shared-rule-research-not-specs
- RULE: Shared System Rules addition: "Research notes are not coding specs. Coding agents follow decision logs and specs only."
- TYPE: process
- SOURCE: doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md (§Shared System Rules update)

### [AUTOMATION-SPEC] task-r001-rule-profile-spec
- RULE: TASK_R001 (create specs/12_rule_profile_spec.md): allowed files only that spec; forbidden: no source code changes, no backtest changes, no pattern implementation. Done when `classic_elliott`, `sow_neowave_strict`, `research_experimental` are defined; wave 2 retracement conflict is documented; hard/soft/warning/manual-review rule statuses are defined.
- TYPE: process
- SOURCE: doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R001)

### [AUTOMATION-SPEC] task-r002-no-lookahead-policy
- RULE: TASK_R002 (create specs/13_no_lookahead_and_repainting_policy.md): done when pivot_time and confirmed_time are defined; backtest signal time policy is defined; TradingView repainting rules are documented; request.security() HTF warning is included.
- TYPE: process
- SOURCE: doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R002)

### [AUTOMATION-SPEC] task-r003-pivot-spec-patch
- RULE: TASK_R003 (patch pivot spec for candidate/confirmed lifecycle): done when pivot schema includes lifecycle fields; confirmation methods are listed; no-lookahead notes are included.
- TYPE: process
- SOURCE: doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R003)

### [VALIDATION] task-r004-backtest-audit
- RULE: TASK_R004 (patch backtest spec with strict no-lookahead audit): done when trade log includes `lookahead_audit_status`; tests for unconfirmed pivot usage are required; signal time uses `known_from_time`, not visual pivot time.
- TYPE: validation
- SOURCE: doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md (§TASK_R004)

### [PROCESS-METHOD] prompt-r01-ew-validation-agent
- RULE: Elliott Wave Rule Validation Agent: validate only core EW rules needed for software implementation; must not write code, implement a detector, propose trading signals, or add ML. Output: 1. Rules confirmed; 2. Rules conflicting with existing docs; 3. Whether conflict requires a rule profile; 4. Hard rules; 5. Soft/scoring rules; 6. Manual-review rules; 7. Specs to update; 8. Tests to add. Do not browse beyond official Elliott Wave references unless asked; do not overwrite SOW/NeoWave rules — separate them into profiles.
- TYPE: process
- SOURCE: prompt_cards/PROMPT_R01_EW_RULE_VALIDATION_AGENT.md (§prompt)

### [PROCESS-METHOD] prompt-r02-neowave-agent
- RULE: NeoWave/SOW Research Agent: classify SOW/NeoWave rules into implementation categories; must not code, must not simplify advanced NeoWave patterns into classical Elliott patterns, must not implement advanced patterns in V1. Output: implement-now rules; score-only rules; manual-review rules; V2 postponed rules; rule profile additions for `sow_neowave_strict`; agent/task impacts. If a NeoWave rule requires discretionary judgment, label it `manual_review` unless a numeric implementation is obvious.
- TYPE: process
- SOURCE: prompt_cards/PROMPT_R02_NEOWAVE_RESEARCH_AGENT.md (§prompt)

### [VALIDATION] prompt-r03-repaint-agent-hard-rule
- RULE: TradingView Repainting Audit Agent: only audit repainting and lookahead risk (no full Pine script, no trading signals). Output: repainting risks; HTF request.security rules; barstate.isconfirmed limitations; alert timing rules; manual TradingView warning text; tests or review checks needed. Hard rule: Any higher-timeframe series must be reviewed for future leakage before use in a published helper.
- TYPE: hard
- SOURCE: prompt_cards/PROMPT_R03_TRADINGVIEW_REPAINT_AGENT.md (§prompt)

### [DATA] prompt-r04-alpaca-agent-default-decision
- RULE: Alpaca Data Research Agent: convert Alpaca MCP/API behavior into a clean data contract (no EW logic, no pivots, no trading signals). Output: final bar schema; metadata schema; session profile rules; adjustment profile rules; pagination requirements; feed/asof requirements; data validation tests. Required decision: Default V1 wave analysis uses regular-session split-adjusted data unless user overrides it.
- TYPE: hard
- SOURCE: prompt_cards/PROMPT_R04_ALPACA_DATA_RESEARCH_AGENT.md (§prompt)

### [VALIDATION] prompt-r05-no-lookahead-agent-hard-rule
- RULE: No-Lookahead Audit Agent: prevent future-data leakage in pivots, monowaves, pattern detection, and backtests; must not implement a strategy, optimize parameters, or report performance metrics unless the audit passes. Output: all potential future-leak paths; required timestamp fields; required lifecycle states; unit tests to add; backtest rejection conditions; trade log audit fields. Hard rule: A trade can never occur at a pivot candle unless that pivot was already confirmed at that same candle by the selected confirmation method.
- TYPE: hard
- SOURCE: prompt_cards/PROMPT_R05_NO_LOOKAHEAD_AUDIT_AGENT.md (§prompt)

### [PROCESS-METHOD] templates-for-notes-decisions-patches
- RULE: Reusable templates: research note (Purpose; Sources reviewed; Findings table with Finding/Source/Confidence/Notes; Engineering interpretation; Decision recommendation Accepted/Deferred/Rejected/Needs Review; Affected docs; Tests to add; Risks; Final decision ID RD-XXX); decision record (Status; Context; Sources; Decision; Implementation impact Module/Spec/Task/Test; Alternatives considered; Risk Low/Medium/High/Critical; Review date); doc patch (Target file; Patch reason; Add section; Replace section; Tests affected; Agent affected).
- TYPE: process
- SOURCE: templates/TEMPLATE_RESEARCH_NOTE.md, templates/TEMPLATE_DECISION_RECORD.md, templates/TEMPLATE_DOC_PATCH.md (§all)

## FILES READ
- README.md
- FILE_INDEX.md
- 00_RESEARCH_VALIDATION_MASTER.md
- 01_RESEARCH_SCOPE_AND_POLICY.md
- 02_SOURCE_QUALITY_POLICY.md
- 03_RESEARCH_DECISION_LOG.md
- 04_DOC_UPDATE_MATRIX.md
- 05_FREEZE_CRITERIA_V1.md
- 06_AGENT_RESEARCH_PROMPTS.md
- research_notes/R01_Elliott_Wave_Core_Rules.md
- research_notes/R02_NeoWave_Rules_Clarification.md
- research_notes/R03_Fibonacci_Engineering_Rules.md
- research_notes/R04_TradingView_Repainting_And_Alerts.md
- research_notes/R05_Alpaca_Data_Behavior.md
- research_notes/R06_No_Lookahead_Backtesting_Policy.md
- research_notes/R07_Manual_TradingView_Workflow.md
- research_notes/R08_Pattern_Automation_Feasibility.md
- research_notes/R09_Source_Bibliography.md
- doc_updates/UPDATE_01_SPECS_TO_MODIFY.md
- doc_updates/UPDATE_02_AGENT_PACK_PATCH_NOTES.md
- doc_updates/UPDATE_03_TASK_CARDS_TO_ADD.md
- prompt_cards/PROMPT_R01_EW_RULE_VALIDATION_AGENT.md
- prompt_cards/PROMPT_R02_NEOWAVE_RESEARCH_AGENT.md
- prompt_cards/PROMPT_R03_TRADINGVIEW_REPAINT_AGENT.md
- prompt_cards/PROMPT_R04_ALPACA_DATA_RESEARCH_AGENT.md
- prompt_cards/PROMPT_R05_NO_LOOKAHEAD_AUDIT_AGENT.md
- templates/TEMPLATE_RESEARCH_NOTE.md
- templates/TEMPLATE_DECISION_RECORD.md
- templates/TEMPLATE_DOC_PATCH.md
