# Ledger extract — elliotwave_md_pack

### [PROCESS-METHOD] master manual workflow order
- RULE: Workflow order: 1) market context before counting waves; 2) mark swing highs/lows on higher timeframe; 3) classify structure as impulse, standard corrective, complex corrective, triangle, or diametric; 4) validate the count using price, time, Fibonacci, channels, and confirmation-line rules; 5) drop to lower timeframe only after the higher-timeframe map is acceptable; 6) use Ichimoku Cloud as trend/trade filter, not as replacement for wave validation; 7) trade only when risk, invalidation, and confirmation are clear.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§How to use this pack)

### [PROCESS-METHOD] TradingView chart layout
- RULE: Standard layout per instrument: price chart (candles/bars; log scale for long-term indices/stocks when the move is very large), Fib Retracement (validate wave 2, B wave, pullbacks), Fib Extension / Trend-Based Fib Extension (project wave 3, wave 5, C; anchor on 0-1-2 or A-B-C), Trend Line for 0-2, 2-4, 0-B, B-D lines, Parallel Channel (impulse/corrective/zigzag/flat/diametric boundaries), Date Range / Bar Count for time validation, Ichimoku Cloud with default 9/26/52, optional RSI/momentum only as supporting evidence.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView setup)

### [PROCESS-METHOD] global and inter-market context checklist
- RULE: Before counting a stock/index check: U.S. indices (DJIA, S&P 500, Nasdaq); Europe/Asia (FTSE, DAX, Nikkei, Hang Seng/Shanghai); currency and rates (DXY, USDINR, bond yields); commodities (gold, silver, copper, crude); breadth (midcap/smallcap vs benchmark); sector leadership (sectors outperforming the index); stock selection prefers clean structure, liquidity, relative strength.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Market-context filter before wave count / Global and inter-market checklist)

### [SETUP-TRADE] pre-trade signal checklist
- RULE: Ask before trading: completed pattern or only guessed pattern? divergence at an important wave end? time cycles supporting a turn window? volume profile/volume behavior agrees with count? options data or positioning supports the expected move? 15-minute or hourly chart giving a tradeable entry and stop? reward clearly larger than risk?
- TYPE: setup
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Market-context filter before wave count / Signal checklist)

### [PROCESS-METHOD] core wave notation and mono-wave definition
- RULE: Impulse waves 1-2-3-4-5; corrective A-B-C; triangle A-B-C-D-E; diametric A-B-C-D-E-F-G; complex corrections W-X-Y or W-X-Y-X-Z. The mono-wave is the smallest marked swing unit: one directional move between two meaningful pivots.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Core wave notation)

### [IMPULSE] five-segment 5-3-5-3-5 structure
- RULE: An impulse is a five-segment trend structure, generally 5-3-5-3-5 internally; waves 1, 3, 5 thrust in the impulse direction, waves 2 and 4 correct waves 1 and 3 respectively.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules)
- NOTES: Same statement in 01_WAVE_RULES_REFERENCE.md §Impulse rule sheet and training deck p.17 (rules 1-2).

### [IMPULSE] wave 2 retracement limit 61.8%
- RULE: Wave 2 should not retrace more than 61.8% of wave 1 (NeoWave rule set used in these notes). Deck wording: "End point of Wave 2 cannot retrace more than 61.8% of wave 1."
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 17 rule 3)

### [IMPULSE] wave 3 never the shortest
- RULE: Wave 3 cannot be "the" shortest of waves 1, 3, and 5.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also deck Page 17 rule 4

### [IMPULSE] rule of overlap
- RULE: Wave 4 should not enter the price area covered by wave 2, except in a terminal impulse / diagonal — Rule of Overlap.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); also deck Page 17 rule 5
- NOTES: Composite notes add: if overlap appears, consider terminal/diagonal or relabel (Brahmastra_Mentorship_Day_5_6_EW_Composite.md Page 2).

### [IMPULSE] rule of alternation
- RULE: Waves 2 and 4 should alternate in price, time, severity, intricacy, construction (pattern type) — Rule of Alternation.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 18 rule 6

### [IMPULSE] extension rule — only one extends
- RULE: Only one among waves 1, 3, or 5 can extend (normally extends) — Extension rule.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 18 rule 10

### [IMPULSE] extended wave >= 1.618x next longest
- RULE: The extended wave should be at least 1.618 times the next longest impulse wave — Extension rule.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 11

### [IMPULSE] rule of equality
- RULE: The two unextended impulse waves tend toward equality — Rule of Equality.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 12

### [IMPULSE] fifth-wave failure
- RULE: A fifth-wave (5th) failure is possible, especially when wave 3 is already an extended wave.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 13

### [IMPULSE] 0-2 line rule
- RULE: No part of wave 1 or wave 3 should break the 0-2 line.
- TYPE: hard
- SOURCE: 01_WAVE_RULES_REFERENCE.md (§Impulse rule sheet); deck Page 18 rule 7
- NOTES: 0-2 line drawn from start of wave 1 (point 0) through end of wave 2; invalid examples show breaks or poor placement (Sutra_of_Waves_Day_1_Notes2.md Page 5).

### [IMPULSE] 2-4 line integrity (Neely confirmation rule)
- RULE: No part of wave 3 or wave 5 should break the 2-4 line, except in terminal impulse — Neely's Confirmation Rule.
- TYPE: hard
- SOURCE: 01_WAVE_RULES_REFERENCE.md (§Impulse rule sheet); deck Page 18 rule 8

### [FIB] internal and external Fibonacci relationships in impulse
- RULE: Internal and external Fibonacci relationships are usually present among the segments of an impulse.
- TYPE: fib
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 18 rule 9)

### [IMPULSE] Neely touch-point rule for impulse (4 of 6)
- RULE: Only 4 (out of possible 6) touch-points should touch the two opposing trend lines — Neely's Touch Point Rule.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 19 rule 14)

### [CONFIRMATION-LINES] impulse confirmation: 2-4 line break within wave-5 time
- RULE: After wave 5, the 2-4 line should be cut/broken in equal or lesser time than wave 5 took — Neely's Rule of Confirmation.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Impulse rules); deck Page 19 rule 15; 01_WAVE_RULES_REFERENCE.md

### [TIME] corrective waves take same or more time than preceding impulse wave
- RULE: Corrective wave should take more time than preceding impulse: wave 2 should take same or more time than wave 1; wave 4 should take same or more time than wave 3.
- TYPE: time
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 19 rule 16)
- NOTES: Day 1 Notes2 Page 4: if wave 2 is too fast (less time than wave 1), the count is not valid under these notes.

### [PROCESS-METHOD] TradingView steps for an impulse
- RULE: 1) mark 0,1,2,3,4,5 pivots; 2) Fib Retracement on wave 1 to check wave 2; 3) Trend-Based Fib Extension from 0->1->2 to check wave 3 extension; 4) draw 0-2 line, internal price action should not violate count logic; 5) draw 2-4 line, confirmation after wave 5 requires its break; 6) compare waves 2 and 4 for alternation; 7) drop to 15-minute/hourly only after larger timeframe count acceptable.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView steps for an impulse)

### [IMPULSE] common impulse invalidations
- RULE: Invalidate the impulse when: wave 2 fully destroys wave 1 beyond the allowed retracement rule; wave 3 is the shortest impulse wave; wave 4 overlaps wave 2 in a normal impulse; wave 5 does not confirm and the 2-4 line remains intact for too long.
- TYPE: validation
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Common invalidations)

### [IMPULSE] wave 2 cannot retrace beyond completion of wave 1
- RULE: Wave 2 should not retrace beyond completion (origin) of wave 1.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Brahmastra_Mentorship_Day_5_6_EW_Composite.md (§Page 2)
- NOTES: Composite examples show wave sequences, failures, and a similarity indicator (image-based).

### [TERMINAL] terminal impulse location
- RULE: Terminal impulse / ending diagonal appears mainly (Day 1 notes: can form only) in wave 5 or wave C.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5)

### [TERMINAL] terminal internal structure 3-3-3-3-3
- RULE: Terminal impulse internal form is corrective-looking, commonly 3-3-3-3-3, and the structure often forms a wedge.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal)

### [TERMINAL] wave 4 overlap allowed
- RULE: In a terminal impulse, wave 4 may enter the area of wave 1 (overlap allowed).
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); Day 1 Notes Page 5

### [TERMINAL] wave 2 may retrace more than 61.8%
- RULE: In a terminal impulse, wave 2 can retrace more deeply than a normal impulse — Day 1 notes: wave 2 can retrace more than 61.8% of wave 1.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal)

### [TERMINAL] wave 3 must still exceed wave 1
- RULE: In a terminal impulse, wave 3 should still move beyond wave 1.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); Day 1 Notes Page 5

### [TERMINAL] time rules relaxed in terminal
- RULE: Time rules are less strict for terminal impulse; Day 1 notes: "Time rule is not necessary in this special structure."
- TYPE: time
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 5); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 01_WAVE_RULES_REFERENCE.md (§Terminal impulse rule sheet)

### [TERMINAL] treat terminal as confirmation-required setup
- RULE: Treat terminal impulse as a terminal setup: wait for confirmation, because reversals can be sharp; confirmation is required — do not pre-empt terminal reversal.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal); 01_WAVE_RULES_REFERENCE.md (§Terminal impulse rule sheet)

### [TERMINAL] terminal TradingView workflow
- RULE: 1) draw wedge boundaries through waves 1-3 and 2-4; 2) check internal legs look corrective not clean impulses; 3) wait for a decisive wedge/2-4 break before acting; 4) invalidation is usually a failed wedge break or continuation beyond the terminal count.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Terminal impulse / ending diagonal / TradingView workflow)

### [TERMINAL] 3rd extension terminal exists
- RULE: A "3rd extension terminal" variant is presented in the deck (page heading only; rule content is in the page image).
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 53)
- NOTES: Image carries the pattern definition; unreadable in text extraction.

### [ZIGZAG] zigzag structure 5-3-5
- RULE: A zigzag is a sharp corrective pattern: A-B-C, internally 5-3-5 (3 segments).
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32

### [ZIGZAG] B less than 61.8% of A
- RULE: Zigzag wave B should be less than 61.8% of A; it can be very shallow — deck: "B could be even 1% of A."
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Pages 32-33
- NOTES: Day 2 Notes Page 2 words it as "B wave should be less than or equal to 61.8% of A."

### [ZIGZAG] C must move beyond end of A
- RULE: Zigzag wave C should move beyond the end of A.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32

### [FIB] zigzag C relation to A
- RULE: C usually relates to A price-wise, or to the total of A+B time-wise, usually by equality or Fibonacci ratio; commonly C = A, C = 0.618A, or C = 1.618A depending on market behavior/structure.
- TYPE: fib
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 32); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules)
- NOTES: Day 1 Notes Page 7 adds a sketch where C ≈ 38.2% of A, plus C = A, and C = 1.618A for an elongated zigzag.

### [TIME] zigzag B time >= A time
- RULE: Wave B should take the same or more time than wave A in a zigzag.
- TYPE: time
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules); deck Page 32
- NOTES: Day 1 Notes Page 7 states "B should take more time than A."

### [CONFIRMATION-LINES] zigzag 0-B confirmation
- RULE: The 0-B line should be broken in equal or lesser time period than that of C — Neely's Rule of Confirmation for zigzag.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules)
- NOTES: Day 2 Notes Page 2: first-stage confirmation = break of 0-B trendline within the required time window; notes mention <=10 days as an example for stage timing.

### [ZIGZAG] Neely touch-point rule for zigzag (3 of 4)
- RULE: Only 3 (out of possible 4) touch points should touch the parallel trend lines/channel — Neely's Touch Point rule.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules)

### [COMPLEX-X] zigzag C ending on channel warns of complex correction
- RULE: If C ends exactly on the parallel channel (and confirmation is weak), development of a complex corrective involving an "x" wave is possible.
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 33); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules)

### [PROCESS-METHOD] zigzag TradingView workflow
- RULE: 1) mark A,B,C against the prior trend; 2) Fib A to check B < 61.8%; 3) project C from B using A length; 4) draw the 0-B trendline; 5) after C completes wait for a break of 0-B in equal or less time than C; 6) if no confirmation, relabel as evolving correction.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Zigzag rules / TradingView workflow)

### [FLAT] flat structure 3-3-5
- RULE: A flat is a sideways or broad correction: A-B-C, internally 3-3-5.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34

### [FLAT] B more than 61.8% of A
- RULE: In a flat, B should be (retrace) more than 61.8% of A.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34

### [TIME] flat B time >= A time
- RULE: In a flat, wave B should take the same or more time than wave A.
- TYPE: time
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules); deck Page 34
- NOTES: Day 2 Notes Page 3 repeats: "in a flat, B should take more time than A."

### [FIB] flat C relation to A or A+B
- RULE: In a flat, C usually relates to A price-wise, or to the total of A+B time-wise, usually by equality or Fibonacci ratio.
- TYPE: fib
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 34); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules)

### [CONFIRMATION-LINES] flat 0-B confirmation
- RULE: In a flat, the 0-B line should be broken in equal or lesser time period than that of C — Neely's Rule of Confirmation.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 34); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules)

### [FLAT] Neely touch-point rule for flat (3 of 4)
- RULE: Only 3 (out of possible 4) touch points should touch the parallel trend lines/channel — Neely's Touch Point rule (flat).
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 35); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules)

### [COMPLEX-X] flat C ending on channel warns of X-wave combination
- RULE: If flat C ends on the parallel channel (and confirmation is weak), development of a complex corrective involving an "x" wave / X-wave combination is possible.
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 35); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules)

### [FLAT] flat variants
- RULE: Variants: Regular flat — B retraces about 61.8% to 100% of A, often weak B. Irregular / expanded flat — B exceeds the start of A (B > 100% of A, strong B); C can be strong. C-failure flat — C fails to move beyond A, often shows underlying strength in the opposite direction. Running flat — B is strong and C is shallow; continuation risk is high. Day 2 notes also show a double-failure flat.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Flat rules / Flat variants to watch); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 3)

### [TRIANGLE] triangle structure 3-3-3-3-3
- RULE: A triangle is a five-leg corrective pattern A-B-C-D-E, internally 3-3-3-3-3; each segment/leg is a complete corrective.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); deck Page 36

### [TRIANGLE] triangle cannot form in wave 2
- RULE: A standard triangle should not / cannot form in wave 2, except special terminal contexts (terminal impulse).
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4)

### [TRIANGLE] triangle drift and leg sizes
- RULE: A triangle can drift upward or downward; A does not have to be the largest leg; E must be (should usually be) the smallest.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 36); 01_WAVE_RULES_REFERENCE.md (§Triangle rule sheet)

### [TRIANGLE] retracement depth of legs
- RULE: At least 3 segments/legs should correct more than 50% of the previous segment.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules)

### [TRIANGLE] Neely touch-point rule for triangle (4 of 6)
- RULE: Only 4 (out of possible 6) touch points should touch the two opposing trend lines — Neely's Touch Point Rule (triangle).
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37)

### [TRIANGLE] B-D baseline must be clean
- RULE: B-D is the base line and it should be clean; no part of wave C or E should prematurely break the B-D trendline.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4)

### [TRIANGLE] opposite boundary line selection
- RULE: Draw the A-C line when C is shorter than B; draw the C-E line on the other side when C is bigger than B.
- TYPE: process
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules)

### [CONFIRMATION-LINES] triangle B-D confirmation
- RULE: Triangle is over/complete when the B-D line gets broken in equal or lesser time period than that of wave E — Neely's Rule of Confirmation.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 37); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules)

### [TRIANGLE] widest-leg relationship 100%-125%
- RULE: Widest leg relationship noted around 100% to 125% (of the adjacent leg) in the triangle sketches.
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 4)
- NOTES: From handwritten sketch; irregular triangle variations also shown on the same page image.

### [TRIANGLE] triangle TradingView workflow
- RULE: 1) mark A-B-C-D-E; 2) draw the B-D line first; 3) draw the opposite boundary using A-C or C-E depending on leg size; 4) do not trade inside the triangle unless doing short-term range trading; 5) wait for B-D break confirmation; 6) the first move after the triangle break is often the tradeable move.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Triangle rules / TradingView workflow)

### [TRIANGLE] extracting triangle behavior
- RULE: Extracting triangle shows alternating expansion/contraction behavior; label A-B-C-D-E; watch whether one side expands while the other contracts; the final E leg often appears small relative to earlier legs; trade only after boundary confirmation, not while internal legs are forming.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Extracting and neutral triangles / Extracting triangle)
- NOTES: Day 2 Notes Page 5 schematic gives: e < c < a and d > b.

### [TRIANGLE] neutral triangle characteristics
- RULE: A neutral triangle differs from a simple contracting triangle: wave C can be the longest wave in the direction of the trend (the most powerful or longest internal leg); D can be the longest leg against the trend; confirmation still comes from the boundary break. Use it when normal triangle proportions do not fit but the five-leg corrective logic remains valid.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Extracting and neutral triangles / Neutral triangle)
- NOTES: Also headed "NUETRAL TRIANGLE" on deck Page 52 (image-based) and sketched in Day 2 Notes Page 5 ("C often powerful").

### [TRIANGLE] expanding triangle fingerprint
- RULE: Expanding triangle shows spikes at extremes ("EXPANDING TRIANGLE (SPIKES AT EXTREMES)").
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 72)
- NOTES: Heading only; details are in the page image.

### [TRIANGLE] limiting vs non-limiting triangles
- RULE: Pattern implication categories distinguish Limiting Triangle from Non-limiting Triangle (each completed pattern implies extent of the next action).
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 46)

### [DIAMETRIC] seven-leg structure
- RULE: A diametric is a seven-leg corrective structure A-B-C-D-E-F-G, internally 3-3-3-3-3-3-3 (each leg corrective), often described as a bow-tie, diamond, or running diametric; it can also run in the direction of the larger trend.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern); 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet)

### [DIAMETRIC] paired-leg relationships G~A, F~B, E~C
- RULE: G approximately relates to A; F approximately relates to B; E approximately relates to C — by price or time. Fibo-system note: G≈A or G≈61.8%A; F≈B by price or time; E≈C by price or time.
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1)
- NOTES: Day 2 Notes Page 6 shows g≈a, f≈b, e≈c on sketches.

### [DIAMETRIC] do not force triangle when seven legs visible
- RULE: Do not force a five-leg triangle (ABCDE) label if seven legs are clearly visible.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow); 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet)

### [DIAMETRIC] diametric confirmation after G
- RULE: Wait for G completion and a boundary break for confirmation; confirmation after G is more important than predicting G early.
- TYPE: hard
- SOURCE: 01_WAVE_RULES_REFERENCE.md (§Diametric rule sheet); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow)

### [DIAMETRIC] diametric TradingView workflow
- RULE: 1) mark seven legs A through G; 2) draw boundaries around the shape; 3) check whether the pattern is symmetrical in price or time; 4) do not force a five-leg triangle label; 5) wait for G completion and a boundary break.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Diametric pattern / TradingView workflow)

### [COMPLEX-X] complex correction forms
- RULE: Complex corrections connect two or three corrective patterns using X waves. Forms: W-X-Y, W-X-Y-X-Z, double zigzag, triple zigzag, zigzag-X-flat, zigzag-X-flat-X-triangle.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 7)

### [COMPLEX-X] maximum two X waves
- RULE: Maximum allowed: two X waves in a complex correction.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); Day 2 Notes Page 7; 01_WAVE_RULES_REFERENCE.md

### [COMPLEX-X] X-wave nature
- RULE: X can be a mono-wave or a corrective pattern; X connects still-corrective patterns/structures.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 01_WAVE_RULES_REFERENCE.md (§Complex correction rule sheet)

### [COMPLEX-X] large X wave means relabel
- RULE: If X becomes unusually large, reassess the degree and count. Example threshold: if X exceeds/becomes greater than 1.618 times W, the structure is no longer a small connector — reassess degree and relabel.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections); 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 8)

### [COMPLEX-X] failed ABC confirmation is the first clue
- RULE: A failed ABC confirmation is often the first clue that a complex correction is forming; if a supposed correction keeps extending without confirmation, avoid forcing a completed pattern.
- TYPE: guideline
- SOURCE: 01_WAVE_RULES_REFERENCE.md (§Complex correction rule sheet); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections)

### [COMPLEX-X] complex correction TradingView workflow
- RULE: 1) first try to label a simple ABC; 2) if confirmation fails, mark the next connector as X; 3) start the next corrective pattern after X; 4) use the same confirmation-line rules for each component pattern; 5) avoid trading the middle of W-X-Y unless a lower timeframe setup is independently clear.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Complex corrections / TradingView workflow)

### [FIB] Fibonacci as validation filter, not signal
- RULE: Use Fibonacci as a validation filter, not as a trade signal by itself.
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation)

### [FIB] impulse Fibonacci behavior
- RULE: Wave 3 often extends 1.618 or 2.618 of wave 1 (wave 3 usually the extended wave); wave 5 and wave 1 tend toward equality (often equality when wave 3 extends); wave 2 should not exceed 61.8% of wave 1; wave 4 and wave 2 often relate by Fibonacci.
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1)
- NOTES: Day 1 Notes2 Page 3 example: 3 = 161.8 (% of 1) and 5 ≈ 1; distinguishes subdivided vs extended portions.

### [FIB] zigzag Fibonacci behavior
- RULE: B <= 61.8% of A. C can equal A, be 0.618 of A, or extend to 1.618 of A (C≈A, C=0.618A, or C=1.618A).
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1)

### [FIB] flat Fibonacci behavior
- RULE: B >= 61.8% of A; B can equal A or extend near 138.2% of A (B=A or B≈138.2% of A; quick sheet: near equality or 1.382x).
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1); 01_WAVE_RULES_REFERENCE.md (§Fibonacci quick sheet)

### [FIB] triangle Fibonacci behavior
- RULE: Three legs (several legs) often show Fibonacci relationships with the prior leg; measure each leg and compare retracement percentages.
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1)

### [FIB] X-wave Fibonacci behavior
- RULE: X should often be less than 61.8% of the prior pattern; a very large X requires relabeling (measure W and compare X).
- TYPE: fib
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Fibonacci system for manual validation); 04_source_page_conversions/Day_2_SOW_Fibo_System.md (§Page 1)

### [FIB] Fibonacci series and golden ratio
- RULE: Fibonacci series 1,1,2,3,5,8,13,21,34,55,89,144…; the Golden Ratio = 1.618; golden rectangle and spiral underpin the wave principle.
- TYPE: fib
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 12)

### [CONFIRMATION-LINES] two-stage confirmation — stage 1 structure lines
- RULE: Stage 1 structure-line confirmation: impulse — break of 2-4 line after wave 5; zigzag/flat — break of 0-B line after C; triangle — break of B-D line after E; diametric — break of boundary after G; complex correction — confirmation of the final component pattern.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Two-stage confirmation / Stage 1); 02_PATTERN_DECISION_TREE.md (§Step 7); 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Confirmation lines)

### [CONFIRMATION-LINES] two-stage confirmation — stage 2 price action
- RULE: Stage 2: after the structure-line break, price should also move beyond the nearest important swing level; hold above/below the broken line on retest when possible; align with Ichimoku direction if using the cloud filter; show acceptable reward/risk from the entry zone.
- TYPE: hard
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Two-stage confirmation / Stage 2)
- NOTES: Day 1 Notes Page 4: stage 1 is line-break confirmation (2-4 trendline with time window); stage 2 is price/action confirmation beyond the next level. Deck Page 38 heading "2 STAGE CONFIRMATION" (details in image).

### [CONFIRMATION-LINES] never trade before the correct line breaks
- RULE: Never treat a count as tradeable until the correct confirmation line is broken.
- TYPE: hard
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 7 - Confirm before trade)

### [ICHIMOKU] Ichimoku default formulas
- RULE: Conversion line / Tenkan-sen = (9-period high + 9-period low) / 2; Base line / Kijun-sen = (26-period high + 26-period low) / 2; Leading Span A = (Conversion Line + Base Line) / 2; Leading Span B = (52-period high + 52-period low) / 2; Lagging Span / Chikou = close plotted 26 periods back. Default settings 9/26/52.
- TYPE: indicator
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter)

### [ICHIMOKU] Ichimoku long/short trade filter
- RULE: Long filter: price above cloud; Tenkan and Kijun rising or aligned upward; cloud supportive or turning supportive; wave pattern completed and confirmed. Short filter: price below cloud; Tenkan and Kijun falling or aligned downward; cloud resistive or turning bearish; wave pattern completed and confirmed.
- TYPE: indicator
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter)

### [ICHIMOKU] Ichimoku is not a standalone trigger
- RULE: Do not take a long simply because price is above the cloud — the wave count still needs confirmation; do not use Ichimoku as the only trigger.
- TYPE: indicator
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Ichimoku Cloud as trade filter; §Common mistakes to avoid)

### [ICHIMOKU] Ichimoku trade-setup condition from deck
- RULE: Ichimoku is an all-in-one indicator (support, resistance, trend direction, entry points, momentum). For any trade setup both the base line (Kijun-sen) and conversion line (Tenkan-sen) should move together in the same direction and the stock must be trading above or below the cloud.
- TYPE: indicator
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 49)

### [SETUP-TRADE] long entry model
- RULE: Long setup: 1) higher timeframe count suggests correction complete or impulse continuation; 2) pattern confirmation line breaks; 3) price above or reclaiming Ichimoku cloud; 4) Tenkan/Kijun slope supports the move; 5) lower timeframe gives a pullback or breakout entry; 6) stop under the invalidation pivot or broken confirmation line; 7) target at the next Fibonacci projection, channel boundary, or prior wave level.
- TYPE: setup
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Practical entry model / Long setup)

### [SETUP-TRADE] short entry model
- RULE: Short setup: 1) higher timeframe count suggests upside pattern complete or bearish continuation; 2) confirmation line breaks down; 3) price below or losing the cloud; 4) Tenkan/Kijun slope supports downside; 5) lower timeframe gives a retest or breakdown entry; 6) stop above invalidation pivot or broken confirmation line; 7) target at next Fibonacci projection, channel boundary, or prior wave level.
- TYPE: setup
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Practical entry model / Short setup)

### [PROCESS-METHOD] ten-step manual chart routine
- RULE: 1) Context: index trend, sector leadership, global risk, bond/currency/commodity backdrop; 2) Weekly chart: identify the largest visible structure; 3) Daily chart: refine active wave and pattern; 4) Hourly chart: find confirmation line and invalidation; 5) 15-minute chart: entry only after larger chart is clear; 6) Label every count with text labels; 7) Measure with Fib, Price Range, Date Range; 8) Confirm: do not trade until the right confirmation line breaks; 9) Risk: write entry, stop, target, invalidation reason before trade; 10) Review: after market close save chart screenshots and update count.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Manual chart routine)

### [PROCESS-METHOD] common mistakes to avoid
- RULE: Avoid: forcing an impulse when the move is a corrective channel; calling every sideways move a triangle (many are flats or complex corrections); ignoring time rules and only using price retracement; acting before 0-B, 2-4, or B-D confirmation; mixing degrees (weekly and 15-minute counts must not carry the same degree labels); reusing old labels after invalidation instead of relabeling from scratch; using Ichimoku as the only trigger; ignoring sector/index context.
- TYPE: guideline
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Common mistakes to avoid)

### [PROCESS-METHOD] chart labelling conventions
- RULE: Use consistent text labels: 0,1,2,3,4,5 for impulse; A,B,C for standard correction; A,B,C,D,E for triangle; A,B,C,D,E,F,G for diametric; W,X,Y,X,Z for complex correction; "Alt:" for alternate count; "Invalid below/above:" for invalidation price; "Confirmed when:" next to the trendline that must break.
- TYPE: process
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Minimum TradingView template labels)

### [PROCESS-METHOD] pattern families table
- RULE: Impulse 1-2-3-4-5 (5-3-5-3-5) directional trend move; Terminal impulse 1-2-3-4-5 (3-3-3-3-3) ending diagonal; Zigzag A-B-C (5-3-5) sharp correction; Flat A-B-C (3-3-5) sideways correction; Triangle A-B-C-D-E (3-3-3-3-3) contracting/expanding/neutral consolidation; Diametric A-B-C-D-E-F-G (3-3-3-3-3-3-3) seven-legged corrective; Complex correction W-X-Y or W-X-Y-X-Z combination of corrective patterns.
- TYPE: guideline
- SOURCE: 01_WAVE_RULES_REFERENCE.md (§Pattern families)

### [ZIGZAG] only three basic standard correctives
- RULE: There are only 3 basic types of standard correctives: 1) Zigzag (5-3-5), 2) Flat (3-3-5), 3) Triangle (3-3-3-3-3).
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 31)

### [PROCESS-METHOD] decision tree step 1 — directional vs corrective
- RULE: Ask: is price moving strongly in one direction with shallow pauses, or overlapping, slow, sideways, and channeled? If directional, test impulse rules first; if overlapping, test corrective patterns first.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 1)

### [PROCESS-METHOD] decision tree step 2 — impulse candidacy
- RULE: Candidate impulse if: you can mark 1-2-3-4-5; wave 2 is acceptable; wave 3 is not shortest; wave 4 does not overlap wave 2; one of 1/3/5 is extended; 2-4 confirmation is possible after wave 5. Reject impulse if: too much overlap; everything is inside a channel; wave 3 is weak/shortest; wave 4 overlaps wave 2 with no terminal impulse context.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 2)

### [PROCESS-METHOD] decision tree step 3 — zigzag vs flat
- RULE: Choose zigzag when: A looks like a five-wave move; B is less than 61.8% of A; C moves beyond A; structure is sharp. Choose flat when: A looks corrective; B retraces more than 61.8% of A; B may return near or beyond the start of A; C is a five-wave move; structure is sideways or broad.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 3)

### [PROCESS-METHOD] decision tree step 4 — triangle test
- RULE: Candidate triangle when: A-B-C-D-E visible; each leg corrective; B-D line clean; E smaller or terminal-looking; break of B-D confirms completion. Reject triangle when: there are seven clear legs; B-D line is repeatedly violated before E; one leg acts like a strong impulse instead of corrective movement.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 4)

### [PROCESS-METHOD] decision tree step 5 — diametric test
- RULE: Candidate diametric when: A-B-C-D-E-F-G visible; pattern resembles bow-tie, diamond, or running shape; paired leg relationships observable (G~A, F~B, E~C); triangle rules do not fit.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 5)

### [PROCESS-METHOD] decision tree step 6 — mark X and continue
- RULE: Candidate complex correction when: a simple ABC appears complete but confirmation does not happen; price starts another corrective sequence; the connector wave is likely X; the structure becomes W-X-Y or W-X-Y-X-Z.
- TYPE: process
- SOURCE: 02_PATTERN_DECISION_TREE.md (§Step 6)

### [PROCESS-METHOD] timeframe cascade
- RULE: Higher timeframe first: Weekly -> Daily -> Hourly -> 15-minute.
- TYPE: process
- SOURCE: 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Higher timeframe first)
- NOTES: Day 2 Notes Page 9 and the Day 5 Trading Cycle also use weekly/daily/hourly (15-minute for execution); for investing use weekly, daily, hourly charts.

### [PROCESS-METHOD] pattern fingerprints quick reference
- RULE: Impulse: 5 waves, trend, one extension, wave 3 not shortest. Terminal: wedge, overlap allowed, usually at wave 5 or C. Zigzag: sharp ABC, B < 61.8% of A, C beyond A. Flat: sideways ABC, B > 61.8% of A. Triangle: ABCDE, corrective legs, clean B-D line. Diametric: seven legs ABCDEFG, bow-tie/diamond/running look. Complex: W-X-Y or W-X-Y-X-Z after simple ABC fails to confirm.
- TYPE: guideline
- SOURCE: 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Pattern fingerprints)

### [SETUP-TRADE] quick-reference trade filter
- RULE: Long: pattern confirmed + price above/reclaiming cloud + Tenkan/Kijun supportive. Short: pattern confirmed + price below/losing cloud + Tenkan/Kijun supportive.
- TYPE: setup
- SOURCE: 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Trade filter)

### [RISK] never-skip list
- RULE: Never skip: invalidation price; stop location; reward/risk; alternate count; post-trade review.
- TYPE: risk
- SOURCE: 05_tradingview_worksheets/One_Page_Quick_Reference.md (§Never skip)

### [VALIDATION] impulse validation checklist
- RULE: Checks (pass/fail): 5 waves visible; internal structure acceptable; wave 2 <= 61.8% of wave 1; wave 3 not shortest; wave 4 no overlap with wave 2; alternation between wave 2 and 4; extension only one of 1/3/5; extended wave >= 1.618x next longest; 2-4 line drawn; 2-4 line broken in acceptable time; Ichimoku agrees; risk/reward acceptable.
- TYPE: validation
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 2 - Impulse validation)

### [VALIDATION] corrective validation matrix
- RULE: Legs: zigzag 3, flat 3, triangle 5, diametric 7. Internal structure: 5-3-5 / 3-3-5 / 3-3-3-3-3 / corrective legs. B depth: zigzag <61.8% A, flat >61.8% A, triangle n/a, diametric n/a. Confirmation line: 0-B / 0-B / B-D / boundary after G. Time rule: zigzag and flat B >= A with 0-B break <= C; triangle B-D break <= E; diametric compare paired legs. Complex-correction risk flags: zigzag/flat if C ends at channel; triangle if B-D not clean; diametric if seven legs continue.
- TYPE: validation
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 3 - Corrective validation)

### [PROCESS-METHOD] higher-timeframe wave map worksheet
- RULE: Record per instrument/timeframe/date: main trend (bullish/bearish/sideways), market context (risk-on/risk-off/mixed), sector context (leader/laggard/neutral); primary count with pattern type, labels marked, confirmation line, invalidation level, target zone, alternate count; and per-leg measurements of price length, time length, Fib relation, pass/fail (legs 1/A through G).
- TYPE: process
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 1 - Higher timeframe wave map)

### [RISK] live trade plan fields
- RULE: Before a trade record: direction (long/short), entry trigger, entry price, stop price, first target, second target, invalidation reason, confirmation line, Ichimoku condition, risk amount, reward/risk.
- TYPE: risk
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 4 - Live trade plan)

### [RISK] before-entry checklist
- RULE: Before entry, all must be checked: higher timeframe count is valid; confirmation line has broken; entry timeframe agrees; stop is logical, not random; target is based on Fib/channel/wave level; news/event risk checked; position size is within risk rule; alternate count written down.
- TYPE: risk
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 4 - Live trade plan / Before entry checklist)

### [PROCESS-METHOD] post-trade review questions
- RULE: After each trade record: result (win/loss/breakeven); was the count correct; did the confirmation line work; was entry early, late, or ideal; was stop logical; did I ignore invalidation; what should be relabeled now; chart screenshot saved (yes/no).
- TYPE: process
- SOURCE: 05_tradingview_worksheets/TradingView_Manual_Worksheets.md (§Worksheet 5 - Post-trade review)

### [PROCESS-METHOD] impulse/corrective application principles
- RULE: Impulse can be upwards or downwards; corrective can be upwards or downwards, going opposite to the move it is correcting; use wave charts plotting high and low of the period in chronological order; mono-wave is the basic unit of analysis; wave analysis has an explanation for each and every part of the chart for any time frame.
- TYPE: process
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44)

### [PROCESS-METHOD] rule of similarity and balance
- RULE: Rule of Similarity & Balance: the smaller of two adjacent waves of the same degree should be at least 1/3rd of the other, price-wise or time-wise.
- TYPE: hard
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44)

### [PROCESS-METHOD] pattern power transfer
- RULE: Each completed pattern implies and transfers a specific amount of "Power" to future market action; each completed pattern always implies the extent of the next action (categories: Impulse, Standard Corrective, Limiting Triangle, Non-limiting Triangle, Complex Corrective).
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45; §Page 46 PATTERN IMPLICATIONS)

### [TIME] corrective consumes more time than the move it corrects — exceptions
- RULE: Corrective usually consumes more time than the move it is correcting, EXCEPT in Triangles, Terminals, Diametric and Symmetrical.
- TYPE: time
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45)

### [PROCESS-METHOD] subdivision and channeling character
- RULE: Corrective is usually properly sub-divided while an impulse may look like a mono-wave; each impulse and corrective is part of a bigger wave, which is part of a still bigger wave (fractality); an impulse would usually NOT get channeled into parallel trend lines.
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 45)

### [TIME] B-wave time heuristic for corrective family selection
- RULE: In corrective patterns inspect wave B timing: if B takes LESS time than A, diametric/triangle are more likely; if B takes MORE time than A, all corrections are possible, with zigzag or flat more likely.
- TYPE: time
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 9)

### [PROCESS-METHOD] Day 2 manual analysis steps
- RULE: Start from weekly/daily/hourly/15-minute; draw channel; try to identify impulse or corrective; apply the B-time heuristic; plot Ichimoku cloud; go to hourly/15-minute for the trade.
- TYPE: process
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md (§Page 9)

### [IMPULSE] alternation worked example
- RULE: Alternation example: compare wave 2 and wave 4 by retracement, price, time, pattern, and complexity; wave 2 retracement shown near 61.8% of wave 1; wave 4 retracement example around 38.2% of wave 1+3.
- TYPE: guideline
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 6)

### [SETUP-TRADE] trading cycle: context vs signal separation
- RULE: Separate Context from Signal. Context = market environment, Midcap/Nifty ratio, leadership/relative sector outperformance, scanner-based stock selection. Signal = pattern, divergence, time cycles, Elliott Wave, volume profile, options data, 15-minute chart execution, stop-loss, target, and reward:risk. For investing use weekly, daily, and hourly charts.
- TYPE: setup
- SOURCE: 04_source_page_conversions/Brahmastra_Mentorship_Day_5_Trading_Cycle.md (§Page 1)

### [SCOPE] NeoWave additions over classic Elliott
- RULE: NeoWave additions include: diametric, extracting triangle, two-stage confirmation, neutral triangle, and more (stricter) impulse rules. Impulse is 5 waves; corrective pattern is 3 waves; corrective types: Zigzag 5-3-5, Flat 3-3-5, Triangle 3-3-3-3-3, Diametric 7 legs.
- TYPE: scope
- SOURCE: 04_source_page_conversions/Brahmastra_Mentorship_Day_5_6_EW_Composite.md (§Page 1)

### [TIME-CYCLES] time cycles as turn-window evidence
- RULE: Time cycles are used as supporting evidence for a turn window ("Are time cycles supporting a turn window?" in the signal checklist; "time cycles" is a Signal component in the trading cycle framework). Deck shows "Nifty Time Cycles", "Nifty Cycles", and a "Nifty 55 Days Cycles" chart — a 55-day cycle length on Nifty.
- TYPE: time
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Pages 61, 77, 78); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§Signal checklist)
- NOTES: Cycle charts are image-based; only the 55-day figure is readable from the page title. Course context: "Kaal Chakra (Master of Cycles)" is the companion time-cycles course (deck Page 84).

### [INDICATORS] divergence and volume as supporting evidence
- RULE: Momentum divergence (RSI/momentum) is used only as supporting evidence at an important wave end; volume profile/volume behavior and options/positioning data should agree with the count before trading.
- TYPE: indicator
- SOURCE: 00_MASTER_TRADINGVIEW_PLAYBOOK.md (§TradingView setup; §Signal checklist)

### [PROCESS-METHOD] channelling technique (image-only)
- RULE: A "CHANELLING TECHNIQUE" section exists (deck Page 27) — the technique details are only in the page image and could not be read from text.
- TYPE: process
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 27)
- NOTES: Practical channel rules that ARE textual elsewhere: impulses usually do not channel in parallel lines (deck p.45); zigzag/flat 3-of-4 touch-point channel rules; C ending on channel warns of complex correction.

### [DATA] wave chart plotting convention
- RULE: Use wave charts plotting the high and low of the period in chronological order (basic price-vs-time wave chart; example labels 0-1-2-3-4-5 followed by A-B-C).
- TYPE: process
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Page 44); 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md (§Page 2)

### [SCOPE] pack purpose and disclaimer
- RULE: The pack is for educational use only — a charting and review framework, not investment advice or guaranteed outcomes; converted notes are cleaned/reorganized from image-based handwritten PDFs rather than blind OCR; source page images are included so nothing important is lost.
- TYPE: scope
- SOURCE: README.md (§Notes on conversion quality); 00_MASTER_TRADINGVIEW_PLAYBOOK.md (header)

### [SCOPE] source attribution
- RULE: Source material: "Neo Wave with Ichimoku Cloud" — Ashish Kyal Trading Gurukul / Waves Strategy Advisors (SEBI Registration No. INH000001097); course content covers Elliott Wave basics, impulsive extensions and terminal pattern, corrective zigzag/flat/triangle, application principles, pattern implications, evolving structures (diametric, extracting/neutral triangle), and Ichimoku Cloud.
- TYPE: scope
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§Pages 1, 2, 10)

### [SCOPE] duplicate source file
- RULE: Sutra_of_Waves_Day_2_Notes_DUPLICATE.pdf is byte-for-byte identical to Sutra_of_Waves_Day_2_Notes.pdf; use Sutra_of_Waves_Day_2_Notes.md and its assets.
- TYPE: scope
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes_DUPLICATE.md

### [DATA] image-only pages that may carry unread rules
- RULE: Numerous deck pages are image-only ("Visual/chart example") with headings but no extractable rule text: pp.13-15, 20-26 (impulse examples), 27 (Channelling Technique), 28 (Alternation), 29 (Extensions), 30 (Terminal Impulse), 38 (2 Stage Confirmation), 39-43 (Double/Tripple Combination), 47-48 (Diametric), 50-51 (Ichimoku charts), 52 (Neutral Triangle), 53 (3rd Extension Terminal), 54-55 (Extracting Triangle), 56-76 (market counts and examples incl. 72 Expanding Triangle), 77-79 (time cycles), 85, 88. Page 58 and 91 contain garbled OCR. Any rules drawn only in these images are NOT captured in this ledger.
- TYPE: scope
- SOURCE: 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md (§various pages)
- NOTES: Similarly all pages of the Day 1/Day 2/Brahmastra notes are handwritten images; their .md interpretations were extracted above but the underlying sketches may contain additional detail.

## FILES READ
- 00_MASTER_TRADINGVIEW_PLAYBOOK.md
- 01_WAVE_RULES_REFERENCE.md
- 02_PATTERN_DECISION_TREE.md
- README.md
- 04_source_page_conversions/Brahmastra_Mentorship_Day_5_6_EW_Composite.md
- 04_source_page_conversions/Brahmastra_Mentorship_Day_5_Trading_Cycle.md
- 04_source_page_conversions/Day_2_SOW_Fibo_System.md
- 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes.md
- 04_source_page_conversions/Sutra_of_Waves_Day_1_Notes2.md
- 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes.md
- 04_source_page_conversions/Sutra_of_Waves_Day_2_Notes_DUPLICATE.md
- 04_source_page_conversions/Sutra_of_Waves_NeoWave_Training_Deck.md
- 05_tradingview_worksheets/One_Page_Quick_Reference.md
- 05_tradingview_worksheets/TradingView_Manual_Worksheets.md
