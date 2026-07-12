# Legacy / Ruleset Extraction Ledger

_Source packs: ElliottWave_Legacy_Repo_Usage_Roadmap_Pack, ElliottWave_Existing_Repo_Audit_Pack, and base-repo RULESET.md + deep/06 + deep/11._

---

### [IMPULSE] R1 — Wave 2 never retraces 100%+ of Wave 1
- RULE: Wave 2 never retraces > 100% of wave 1 → end(W2) stays beyond origin(W1). Bull: w2.end.price > w1.start.price; Bear: w2.end.price < w1.start.price. Invalidation level = exact origin price of wave 1.
- TYPE: hard
- SOURCE: docs/RULESET.md (§A R1); docs/research/deep/06 (§2.2 Rule 1)
- NOTES: If wave 2 erases all of wave 1, no net progress occurred; impulse count collapses and must be reclassified.

### [IMPULSE] R2 — Wave 3 never the shortest of 1/3/5
- RULE: Wave 3 is never the shortest of 1/3/5 → len(W3) > len(W1) OR len(W3) > len(W5). FAIL only if len3 < len1 AND len3 < len5 (absolute minimum of all three).
- TYPE: hard
- SOURCE: docs/RULESET.md (§A R2); docs/research/deep/06 (§2.2 Rule 2)
- NOTES: Wave 3 may be shorter than wave 1 but must not be shorter than wave 5 (and vice versa).

### [IMPULSE] R3 — Wave 4 does not enter Wave 1 territory
- RULE: Wave 4 does not enter wave-1 price territory. Bull: low(W4) > high(W1) i.e. w4.end.price > w1.end.price; Bear: w4.end.price < w1.end.price. Invalidation = extreme endpoint of wave 1 (not origin). Suspended/exception for diagonals.
- TYPE: hard
- SOURCE: docs/RULESET.md (§A R3); docs/research/deep/06 (§2.2 Rule 3)
- NOTES: The sole exception is a diagonal formation where wave 4 overlap with wave 1 is expected.

### [IMPULSE] Extension rule
- RULE: Exactly one of 1/3/5 extends; equities → usually W3. Extended wave ≥ 1.618× the next-longest motive wave. In NeoWave this is HARD (no 161.8× ⇒ no extension). ~90% of extensions occur in wave 3; wave 5 next most common; wave 1 rarest.
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A guidelines); docs/research/deep/06 (§2.3)
- NOTES: Elliott: guideline/WARN. NeoWave (doc 02 §2.4): hard. check_extension returns extended wave only if longest/second ≥ 1.618.

### [IMPULSE] Wave 3 extended sub-rules
- RULE: When W3 extended: W3 ≥ 1.618×W1 (often 1.618–2.618, sometimes larger); waves 1 and 5 tend to equality; if equality fails, W5 = 0.618×W1 next most probable.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§2.3)

### [IMPULSE] Wave 5 extended sub-rules
- RULE: When W5 extended: W3 must be longer than W1 (else R2 fails); W5 commonly extends to 1.618× the net distance of W1 through W3 (measured from W4 endpoint); accompanied by strong momentum and channel throw-over.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§2.3)

### [IMPULSE] Wave 1 extended sub-rules
- RULE: When W1 extended (rare): W3 and W5 tend to be relatively equal in price and time; net distance from end of W3 to end of W5 often equals 0.618 of W1.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§2.3)

### [IMPULSE] Equality guideline
- RULE: The two non-extended motive waves tend to equality OR 0.618×. When W3 extended: W5 ≈ W1 (primary) or W5 = 0.618×W1 (secondary).
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A); docs/research/deep/06 (§2.6)

### [IMPULSE] Alternation guideline
- RULE: W2 and W4 alternate in form/depth/time; depth difference typically > 15–20 pp. If W2 is sharp (zigzag/double zigzag, B<61.8% of A), W4 will usually be sideways (flat/triangle/double three), and vice versa. Applies in ~70–80% of cases → strong WARN, never FAIL.
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A); docs/research/deep/06 (§2.4, §14.3)
- NOTES: In a diagonal, waves 2 and 4 are both typically zigzags — no alternation expected.

### [IMPULSE] W2 depth guideline
- RULE: W2 typical 50–61.8% of W1; valid 38.2% (shallow) … 76.4–85.4% (deep). Deep-doc variant: 50–78.6% typical (0.500/0.618/0.786). W2 retracement > 78.6% not yet crossing W1 origin is still valid but raises degree concern.
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A); docs/research/deep/06 (§2.5)

### [IMPULSE] W4 depth guideline
- RULE: W4 typical 23.6–38.2% of W3; deep-doc variant 23.6–50% (0.236/0.382/0.500); 50% only in triangles. Wave 2 typically deeper than wave 4.
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A); docs/research/deep/06 (§2.5)

### [IMPULSE] W3 vs W1 guideline
- RULE: W3 most commonly 1.618×W1; 2.618×/3.618× when extended; ≥1.0× lower bound.
- TYPE: fib
- SOURCE: docs/RULESET.md (§A)

### [IMPULSE] Wave personality
- RULE: W1 tentative · W2 deep/sharp · W3 strongest, broadest, highest momentum/volume · W4 sideways/boring · W5 frothy, momentum divergence, lower volume.
- TYPE: guideline
- SOURCE: docs/RULESET.md (§A)

### [IMPULSE] Definition & position
- RULE: Impulse = five-wave motive 1-2-3-4-5 in trend direction at one-larger degree. Waves 1,3,5 are motive (impulse or diagonal); waves 2,4 are corrective. Appears as complete motive sequence, as W1/W3/W5 within larger impulse, and as waves A and C of a zigzag.
- TYPE: setup
- SOURCE: docs/research/deep/06 (§2.1)

### [CONFIRMATION-LINES] Impulse channeling (base/acceleration/final)
- RULE: Base channel (after W2): lower line through wave-0 origin and W2 end, upper parallel through W1 top — price holding above lower during W3 confirms motive. Acceleration channel (after W4): lower line through W2 end and W4 end, upper parallel through W3 top — W5 target = upper parallel. Final channel (after W5): lines through W1 top and W3 top, parallel through W2 bottom — W5 ideally meets/slightly breaches upper (throw-over) or falls short (weak/truncated fifth).
- TYPE: indicator
- SOURCE: docs/RULESET.md (§A/§D); docs/research/deep/06 (§2.7)

### [ZIGZAG] Zigzag (5-3-5) hard rules
- RULE: Zigzag A-B-C, sub-structure 5-3-5 (A impulse/leading-diagonal, B any 3, C impulse/ending-diagonal). Hard: (1) B not past A origin (≤100% of A); (2) B retraces ≤ 61.8% of A (the defining zigzag/flat classifier); (3) C surpasses end of A.
- TYPE: hard
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§7.1)
- NOTES: If C fails to exceed A end → running flat, not a zigzag.

### [ZIGZAG] Zigzag Fibonacci guidelines
- RULE: B retraces 38.2–61.8% of A (most common ~50%); C ≈ 100% of A (equality, primary); C = 0.618×A (secondary/truncated); C = 1.618×A (extended). Table: C typ. 0.618–1.618×A.
- TYPE: fib
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§7.1, §12.4)

### [ZIGZAG] Double zigzag (W-X-Y) hard rules
- RULE: W(5-3-5)—X(any 3)—Y(5-3-5). Hard: (1) W is a zigzag; (2) X < W in price; (3) X retraces ≥ 20% of W; (4) Y is a zigzag; (5) Y ≥ X in price; (6) C of W cannot be a failure (truncated C = WARN); (7) X cannot be an ending triangle. Most common combination; appears mostly in W2 or WB.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§7.2)

### [ZIGZAG] Triple zigzag (W-X-Y-X-Z)
- RULE: Three zigzags linked by two X-waves; relatively rare; same rules as double zigzag applied recursively; final wave Z must be a zigzag.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§7.3)

### [ZIGZAG] Zigzag B ≤ 61.8% hard (NeoWave) + C surpasses A
- RULE: In NeoWave B ≤ 61.8% of A is a HARD limit (not guideline); C endpoint must exceed A endpoint else truncated C (WARN).
- TYPE: hard
- SOURCE: docs/research/deep/11 (T33, T34)

### [FLAT] Flat (3-3-5) classifier
- RULE: Flat A-B-C sub-structure 3-3-5 (A any 3, B any 3, C impulse/ending-diagonal). Defining test: B retraces > 61.8% of A → flat family; ≤ 61.8% → zigzag.
- TYPE: hard
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§8.1)

### [FLAT] Regular flat
- RULE: B retraces ~90–100% of A (0.818–1.000); C ≈ 100% of A from B endpoint (C ≈ A); C ends near A endpoint without significantly exceeding it. RULESET: B 61.8–100%, C≈A.
- TYPE: fib
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§8.2, §12.4)

### [FLAT] Expanded flat (most common)
- RULE: B > 100% of A (typical 105–138%); C extends significantly beyond A endpoint (typical 1.382–1.618×A). Hard: B endpoint crosses A start; C must exceed A endpoint. Fib: B ≈ 1.236–1.382×A (range 1.000–1.618); C ≈ 1.618×B common; C ≈ 1.0×A min, 1.618×A typical.
- TYPE: hard
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§8.3, §12.4)

### [FLAT] Running flat (rare)
- RULE: B > 100% of A (same signature as expanded); C FAILS to reach A endpoint (falls short in A's direction). Fib: B ≈ 1.000–1.236×A; C ≈ 0.618–0.786×A (truncated). RULESET: B >100%, C truncated < end of A.
- TYPE: fib
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§8.4)
- NOTES: Distinction from expanded flat is whether C clears A's endpoint (expanded yes, running no).

### [FLAT] Flat B ≥ 61.8% hard lower bound (NeoWave)
- RULE: B in a flat must retrace ≥ 61.8% of A; below that → triangle leg or zigzag B.
- TYPE: hard
- SOURCE: docs/research/deep/11 (T35)

### [FLAT] Flat B strength sub-classification
- RULE: Flat B-wave: strong B > 100% of A; normal B 80–100%; weak B 61.8–80%. Used to predict C target range.
- TYPE: guideline
- SOURCE: docs/research/deep/11 (T60, GAP-7)

### [FLAT] Post-flat implications
- RULE: After regular flat: trend resumes with moderate force. After expanded flat: powerful trend resumption. After running flat: strongest subsequent trend signal.
- TYPE: guideline
- SOURCE: docs/research/deep/06 (§8.5)

### [TRIANGLE] Triangle (3-3-3-3-3) base rules
- RULE: 5 legs A-B-C-D-E each corrective (3-wave). Contracting a>b>c>d>e (converging); expanding (diverging); barrier (one flat line). Position: W4, B, or final X. Wave E often over/undershoots a-c line. Trendlines: A-C line and B-D line.
- TYPE: hard
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§9.1)

### [TRIANGLE] Contracting triangle hard rules
- RULE: (1) C never moves beyond A endpoint; (2) D never beyond B endpoint; (3) E never beyond C endpoint; (4) standard contracting B does not exceed A start; (5) each leg subdivides as a three. Size contracting: each leg > next. Fib: each leg ≈ 0.618× preceding same-direction leg (B≈0.618×A, C≈0.618×B, D≈0.618×C, E≈0.618×D).
- TYPE: hard
- SOURCE: docs/research/deep/06 (§9.2, §12.4)

### [TRIANGLE] Barrier triangle
- RULE: Same as contracting but one trendline is approximately horizontal (within ~3% tolerance). If B-D line horizontal → breaks upward; if A-C line horizontal → breaks downward.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§9.3); docs/research/deep/11 (T41)

### [TRIANGLE] Expanding triangle
- RULE: Trendlines diverge; each leg longer than prior same-direction leg. Hard: C beyond A endpoint; D beyond B endpoint; E beyond C endpoint (E longest of A/C/E); size ordering A<B<C<D<E. Fib: B,C,D typically retrace 105–125% of preceding sub-wave.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§9.4, §12.4)

### [TRIANGLE] Running triangle
- RULE: Wave B exceeds origin of wave A; all other contracting rules still apply (C not beyond A end, D not beyond B end, E not beyond C end). Indicates very strong trend. Highest mislabel risk.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§9.5); docs/research/deep/11 (T39)

### [TRIANGLE] Neutral triangle (NeoWave exclusive)
- RULE: C is longest leg; A ≈ E (each ≥ 38.2% of C); C ≤ 161.8–261.8% of A. Extracting-triangle term retired by Neely (QA-923) → maps to neutral triangle with extended C.
- TYPE: hard
- SOURCE: docs/research/deep/11 (T38, T59)

### [TRIANGLE] Post-triangle thrust
- RULE: After E completes, thrust minimum ≈ distance of widest leg (wave A) from apex/breakout; common 75–125% of widest leg; can exceed 125% in strong markets. RULESET A-7: target 75–125% of widest leg from E. NeoWave timing: thrust completes in ≤ shortest leg duration.
- TYPE: fib
- SOURCE: docs/RULESET.md (§F A-7); docs/research/deep/06 (§9.6); docs/research/deep/11 (T40)

### [TERMINAL] Ending diagonal (W5/C) definition & structure
- RULE: Ending diagonal appears only at termination of a larger trend (W5 of impulse, or wave C of flat/zigzag). Sub-structure 3-3-3-3-3 (every sub-wave subdivides as a three). Signals exhaustion; after completion market reverses sharply and rapidly retraces the entire diagonal, often to origin.
- TYPE: setup
- SOURCE: docs/research/deep/06 (§4.1, §4.2); docs/RULESET.md (§C)

### [TERMINAL] Ending diagonal hard rules
- RULE: (1) W2 does not exceed W1 start (≤100%); (2) W3 exceeds W1 end; (3) W4 does not cross W2 end (may overlap W1); (4) W5 exceeds W3 end; (5) W3 not shortest of 1/3/5; (6) contracting: W1>W3>W5 and W4>W2; (7) sub-structure 3-3-3-3-3 (a leg subdividing as a five INVALIDATES; flagged REF without sub-degree data).
- TYPE: hard
- SOURCE: docs/research/deep/06 (§4.3, §4.9)

### [TERMINAL] Ending diagonal W4/W1 overlap diagnostic
- RULE: In ending diagonal W4 almost always overlaps W1 (key diagnostic vs impulse). Absence of overlap → WARN. W4 must NOT cross end of W2 (else FAIL).
- TYPE: hard
- SOURCE: docs/research/deep/06 (§4.4); docs/research/deep/11 (T28)

### [TERMINAL] Ending diagonal trendline convergence & throw-over
- RULE: L1 through W1 and W3 endpoints (upper boundary in uptrend); L2 through W2 and W4 endpoints (lower boundary); converge toward apex (wedge). W5 typically ends near L1; may slightly exceed (throw-over) then reverse rapidly. Contracting: slope_13 > slope_24. Throw-over common but not required.
- TYPE: indicator
- SOURCE: docs/research/deep/06 (§4.5, §4.6); docs/research/deep/11 (T23)

### [TERMINAL] Ending diagonal Fibonacci
- RULE: W2 retr W1 0.618–0.786 (sec 0.500); W4 retr W3 0.618–0.786 (sec 0.500); W3/W1 0.618 (sec 0.786); W5/W3 0.618 smallest (sec 0.382); post-pattern retrace target = diagonal origin (min = wave 5 origin). Each corrective wave (2,4) typically retraces 0.66–0.81 of preceding motive wave.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§4.7, §12.3)

### [TERMINAL] Ending diagonal post-pattern retrace
- RULE: After completion, move retraces entire diagonal very rapidly (faster than diagonal took to form). Minimum target = origin of W5; common target = origin of entire diagonal (W1 start); overshoot ~0.236 beyond origin. Retrace faster than any same-direction sub-wave within diagonal.
- TYPE: setup
- SOURCE: docs/research/deep/06 (§4.8)

### [TERMINAL] NeoWave terminal impulse (vs ending diagonal)
- RULE: NeoWave terminal = ED equivalent with extra constraints: (1) 3-3-3-3-3 strictly enforced; (2) W2 retraces ≥ 61.8% of W1 (Neely floor) [note: RULESET §E states W2 ≤ 61.8% of W1 as terminal hard limit]; (3) post-terminal reversal must retrace terminal in LESS time than terminal took to form; (4) if W2 > 61.8% of W1, may be terminal regardless of overlapping W4; (5) channeling uses 2-4 line (lower) and 1-3 line (upper) confirmed by end of W4.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§11.1); docs/RULESET.md (§E terminals)
- NOTES: Conflict flagged: deep/06 §11.1 says W2 ≥ 61.8% floor; RULESET §E and deep/11 T29 say W2 ≤ 61.8% hard limit in terminal. Both statements present in sources.

### [TERMINAL] Terminal (RULESET §E) hard rules
- RULE: Terminals: 3-3-3-3-3, W4/W1 overlap, W2 ≤ 61.8% of W1; after completion full fast retrace to origin in ~¼–½ build-time (bias, not a price/time guarantee).
- TYPE: hard
- SOURCE: docs/RULESET.md (§E §2.7); docs/research/deep/11 (T29, T30, T32)

### [TERMINAL] Terminal shape & retrace window
- RULE: Shape contracting w1>w3>w5 (textbook) or expanding w5>w3>w1 (rarer, WARN). Retrace bias window = 1/4 to 1/2 of build time; origin is the structural target (directional bias, NOT a timed forecast). Terminal retrace over-projection warning: retrace often takes longer while still qualifying; use price target (diagonal origin) as primary confirmation, not timing.
- TYPE: time
- SOURCE: docs/research/deep/11 (T30, T32, §5.7); docs/research/deep/06 (§14.10)

### [TERMINAL] Leading diagonal (W1/A) definition & structure
- RULE: Leading diagonal appears only at start of a trend (W1 of impulse, or wave A of zigzag). Sub-structure 5-3-5-3-5 (waves 1,3,5 are impulses/small leading diagonals; waves 2,4 are zigzags). Rarest motive pattern; signals less-vigorous new trend; continuation follows.
- TYPE: setup
- SOURCE: docs/research/deep/06 (§3.1, §3.2); docs/RULESET.md (§C)

### [TERMINAL] Leading diagonal hard rules (contracting)
- RULE: (1) W2 endpoint does not exceed W1 start; (2) W3 must exceed W1 endpoint; (3) W4 must not exceed W2 endpoint; (4) W5 must exceed W3 endpoint; (5) W3 never shortest of 1/3/5; (6) contracting: W3<W1, W4>W2, W5<W3. W4 almost always overlaps W1 (diagnostic) but must not cross end of W2.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§3.3, §3.4)

### [TERMINAL] Leading diagonal Fibonacci & post-pattern
- RULE: W2 retr W1 0.618 (sec 0.786); W4 retr W3 0.618 (sec 0.786); W3/W1 0.618 shorter; W5/W3 0.618 shorter; W5 proj = 0.618×W3 from W4 end or =W1. Both corrective waves (2,4) typically retrace 0.66–0.81 of preceding motive. Post-pattern: deep W2 retrace 61.8–78.6% of the entire diagonal, then powerful W3.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§3.6, §3.7, §12.3)

### [TERMINAL] Contracting vs expanding diagonal
- RULE: Contracting: motive 1>3>5, corrective 2<4, trendlines converge (most common). Expanding: motive 1<3<5, corrective 2>4, trendlines diverge (rarer; typically leading position with 5-3-5-3-5). Expanding diagonal hard rules: l3>l1, l5>l3, l4<l2; W4 still must not cross W2 endpoint.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§5.1, §5.2)

### [DIAMETRIC] NeoWave diametric (7 legs)
- RULE: 7-legged formation a-b-c-d-e-f-g, NO X-wave connector. Hard: exactly 7 legs; no X-wave (all adjacent); time similarity is the norm (waves tend to time equality, not price); does NOT exhibit Fibonacci price/time relationships. Time S&B: max/min time ratio < 3×.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§11.2); docs/research/deep/11 (T42)

### [DIAMETRIC] Diametric shapes & post-pattern
- RULE: Bowtie = legs a–d expand in price then e–g contract. Diamond = legs a–d contract then e–g expand. Post-pattern: wave immediately after leg G is larger and faster than any same-direction leg within the diametric. Post-diametric thrust ≈ widest part of formation; sharp but no hard timing rule.
- TYPE: setup
- SOURCE: docs/research/deep/06 (§11.2); docs/research/deep/11 (T43, T44)

### [DIAMETRIC] NeoWave symmetrical (9 legs)
- RULE: 9-legged formation a-i; most waves similar in TIME, price, and complexity within advancing group and within declining group (groups dissimilar to each other); no X-waves; no Fibonacci relationships; post-pattern move large and fast. Detection is REF-grade → display WARN, manual confirmation, extremely rare.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§11.3); docs/research/deep/11 (T45, §5.5)

### [COMPLEX-X] Combination (double/triple three) base rules
- RULE: Double W-X-Y / triple W-X-Y-X-Z; X < 61.8% of W; triangle only as final element; never more than one zigzag (a double zigzag is a separate label). Appear mostly in W4, WB, WX positions ("sideways" corrections).
- TYPE: hard
- SOURCE: docs/RULESET.md (§B); docs/research/deep/06 (§10.1)

### [COMPLEX-X] Double three (W-X-Y) hard rules
- RULE: (1) X smaller than W in price; (2) X retraces ≥ 20% of W; (3) X typically 50–61.8% of W (guideline); (4) Y ≥ X in price; (5) overall combination makes no significant net progress; (6) no two adjacent components of same type (W=zigzag and Y=zigzag → "double zigzag" not "double three"). W: zigzag/flat/triangle (usually not triangle in W); X: zigzag most common, cannot be ending triangle; Y: combinations end with flat or triangle.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§10.2)

### [COMPLEX-X] Triple three (W-X-Y-X-Z)
- RULE: Three corrections + two X-waves. W any correction except triangle (some allow); X1/X2 follow X-wave rules; Y any correction; Z = flat or triangle (combinations must END with flat or triangle).
- TYPE: hard
- SOURCE: docs/research/deep/06 (§10.3)

### [COMPLEX-X] X-wave detailed rules
- RULE: (1) any corrective structure valid (zigzag most common, flat second); (2) X SMALLER in price than preceding component (W or Y); (3) X retraces 50–61.8% of W primary, range 20–80%; (4) ending triangle not valid as X-wave; (5) X typically takes less time than W. NeoWave: small x-wave < 61.8% of prior correction; >100% is a structural error; x-wave power rating ≤ prior correction and ≥ least complex sub-wave of prior correction.
- TYPE: hard
- SOURCE: docs/research/deep/06 (§10.4); docs/research/deep/11 (T46, T47)

### [PROCESS-METHOD] Impulse vs Diagonal vs Triangle decision tree
- RULE: STEP1: check W4/W1 overlap — no overlap → IMPULSE candidate (apply 3 hard rules); overlap present → DIAGONAL. STEP2: leading if in W1/A position (expect 5-3-5-3-5), ending if in W5/C position (expect 3-3-3-3-3). STEP3: contracting (l1>l3>l5 AND l4>l2) vs expanding (l1<l3<l5 AND l4<l2); neither → WARN.
- TYPE: process
- SOURCE: docs/research/deep/06 (§6.1)

### [PROCESS-METHOD] Triangle vs Diagonal disambiguation
- RULE: Net progress ≥ 40% of total price range → diagonal candidate; sideways ≤ 30% → triangle candidate. Triangle: no net progress, corrective position (W4/B/X), thrust = widest leg, labels A-B-C-D-E, B can exceed A start (running), A-C/B-D lines, E often falls short of A-C. Ending diagonal: net trend progress, motive-terminal position (W5/C), sharp reversal, labels 1-2-3-4-5, B cannot exceed hard, 1-3/2-4 lines, 5th meets/exceeds 1-3.
- TYPE: process
- SOURCE: docs/research/deep/06 (§6.2, §14.7)

### [PROCESS-METHOD] Impulse vs Leading diagonal (W1 position)
- RULE: No W4/W1 overlap → impulse candidate. Overlap + contracting wedge → leading diagonal. Overlap + not contracting → WARN (expanding diagonal or count error). Leading diagonal: internal W2 is a zigzag, W2 retrace 61.8–78.6% (deeper), following W2 very deep (~78.6%), W3 often shorter than W1.
- TYPE: process
- SOURCE: docs/research/deep/06 (§6.3)

### [FIB] Retracement & extension levels
- RULE: Retrace levels: .236/.382/.5/.618/.764/.786. Extension levels: 1.0/1.272/1.618/2.0/2.618/3.618/4.236. Core ratios with derivations: 0.236=φ⁻³, 0.382=φ⁻², 0.500=midpoint, 0.618=φ⁻¹, 0.786=√0.618, 1.272=√1.618, 1.382=1+0.382, 1.618=φ, 2.618=φ², 3.618=φ³, 4.236=φ⁴.
- TYPE: fib
- SOURCE: docs/RULESET.md (§D); docs/research/deep/06 (§12.1)

### [FIB] Per-wave target table
- RULE: W2 .5/.618 of W1 · W3 1.618×W1 (2.618/3.618 ext) · W4 .236/.382 of W3 · W5 =W1 / .618×net(W1→W3) / 1.618×W1 · zigzag C =A / 1.618×A · flat B .618–1.382×A · flat C 1.0–1.618×A. Deep-doc: W2 primary 0.618 (sec 0.786, tert 0.500); W3/W1 extended 1.618/2.618/3.618; W4 primary 0.382 (sec 0.500, tert 0.236); W5 extension = W4 end + 1.618×W1 or + 1.0×W1.
- TYPE: fib
- SOURCE: docs/RULESET.md (§D); docs/research/deep/06 (§12.2)

### [FIB] Machine-checkable Fibonacci tolerance
- RULE: FIB_RATIOS = [0.236, 0.382, 0.500, 0.618, 0.786, 1.000, 1.272, 1.382, 1.618, 2.618, 3.618]; FIB_TOLERANCE = ±0.05 (5% of measured distance). is_near_fib passes if distance from nearest fib ≤ 0.05.
- TYPE: fib
- SOURCE: docs/research/deep/06 (§12.5)

### [FIB] Fib cluster target (C-8)
- RULE: Where ≥3 independent Fib measurements overlap within 1–2% = the target zone.
- TYPE: fib
- SOURCE: docs/RULESET.md (§F C-8)

### [FIB] Fibonacci is guideline not hard rule
- RULE: Wave structure hard rules are absolute; Fibonacci ratio relationships are probabilistic. A pattern satisfying all hard rules but no Fibonacci guidelines is still VALID (atypical). Never FAIL a count on Fibonacci grounds alone.
- TYPE: guideline
- SOURCE: docs/research/deep/06 (§14.2)

### [FIB] Diametric/Symmetrical lack Fibonacci
- RULE: Diametrics and Symmetricals are defined by TIME equality, not price Fibonacci. Searching for Fibonacci targets in these patterns is a category error.
- TYPE: guideline
- SOURCE: docs/research/deep/06 (§14.8)

### [SCOPE] Degree by duration
- RULE: GrandSC multi-century · SC 40–70y · Cycle 1y–decades · Primary months–2y · Intermediate weeks–months · Minor days–weeks · Minute hrs–days · Minuette min–hrs · Subminuette <min. [free, basis=Frost&Prechter]
- TYPE: scope
- SOURCE: docs/RULESET.md (§D §2.5)

### [SCOPE] Degree is heuristic / notation
- RULE: Neely bottom-up degree assignment carries degree_confidence="HEURISTIC"; S&B rules constrain but rarely uniquely determine degree. Card must show degree_confidence: HEURISTIC and all candidate degree assignments with S&B violation counts. Progress-label degree brackets: (i)(ii)... minor, ((i))((ii))... intermediate, (I)(II)... primary.
- TYPE: scope
- SOURCE: docs/research/deep/06 (§14.6); docs/research/deep/11 (T58, §5.4)

### [PROCESS-METHOD] NeoWave bottom-up construction
- RULE: monowave → polywave (3/5) → multiwave → macrowave; construct from smallest up. Compaction hierarchy assigns compacted :5/:3 label at each level. Power ratings (integer complexity): monowave=1, polywave=2, multiwave=3, macrowave=4.
- TYPE: process
- SOURCE: docs/RULESET.md (§E §2.1); docs/research/deep/11 (T16, T17)

### [PROCESS-METHOD] Monowave structure labels :5/:3
- RULE: :5 (motive: retraces prior wave faster than it formed, more price/time) vs :3 (corrective: ≤61.8% retrace, ≥ equal time/complexity). Additional sub-type labels: :F3 :c3 :L5 :s5 :sL3 :L3 from the 7-rule decision tree with conditions a–d. This is the pattern-identity test the crude wave-3 signal skips.
- TYPE: process
- SOURCE: docs/RULESET.md (§E §2.1); docs/research/deep/11 (T05, T06)

### [PROCESS-METHOD] NeoWave seven retracement rules
- RULE: By m2/m1 ratio: R1 <38.2% (m1=extended 3rd) · R2 38.2–61.8% (1st/5th) · R3/4 61.8–100% (a-wave/1st, conditions a–d on m0/m1) · R5 100–161.8% (not a retrace→trend change) · R6 161.8–261.8% (strong reversal) · R7 >261.8% (x-wave/extreme). Breakpoints at 38.2% / 61.8% / 100% / 161.8% / 261.8%.
- TYPE: process
- SOURCE: docs/RULESET.md (§E §2.5); docs/research/deep/11 (T11, T12)

### [PROCESS-METHOD] Rule 3 vs Rule 4 overlap split
- RULE: Rules 3 and 4 share the r21 range 0.618–1.00 but opposite structural implications: Rule 3 (no overlap into m0 territory) → corrective (:3 or :F3); Rule 4 (m2 retraces into m0 price territory, overlap) → possibly motive (:c3). ~30–40% of monowaves in trending/extended markets get ambiguous labels resolvable with the m0/m1 ratio test.
- TYPE: process
- SOURCE: docs/research/deep/11 (T13, GAP-1, §5.2)

### [TIME] Similarity & Balance (S&B)
- RULE: Adjacent same-degree waves relate in price ∈ [1/3, 3×] AND time ∈ [1/3, 3×]; at least one must hold, both ideal. THIS is the NeoWave time rule (not a fixed bar count). Must run on EVERY adjacent corrective pair (W2/W4, A/C, W1/W3, W3/W5, triangle legs), not just W2/W4.
- TYPE: time
- SOURCE: docs/RULESET.md (§E §2.3); docs/research/deep/11 (T07, T08, T09)

### [PROCESS-METHOD] Rule of Proportion / Extension (NeoWave)
- RULE: Subwave ≤ parent unless extending; extension must be ≥ 161.8× (161.8%) of next-longest. Treated as HARD in NeoWave (no valid extension < 1.618 ⇒ not a trending impulse); currently WARN in Elliott guidelines.
- TYPE: hard
- SOURCE: docs/RULESET.md (§E §2.4); docs/research/deep/11 (T10, T25)

### [TIME] Wave-2 / Wave-4 time rule (trending impulse)
- RULE: In a trending impulse, W2 must consume ≥ W1 time (bars) and W4 must consume ≥ W3 time before the wave can be considered complete — a TIMING hard rule (FAIL if not). For terminal impulse these are reversed (corrective sub-waves CAN be shorter). Catches early-reversal mislabelling on 4h/hourly.
- TYPE: time
- SOURCE: docs/research/deep/11 (T26, T56, GAP-6)

### [CONFIRMATION-LINES] NeoWave channeling (0-2, 2-4, 1-3)
- RULE: 0-2 line locates true end of W2; W3 should not break it (base channel; corrects W2 endpoint if price violates and reverses). 2-4 line [hard]: no part of W3 or W5 breaks it; break signals impulse nearing completion. 1-3 line = W5 target (parallel to 2-4 through W1 top); throw-over (blow-off) vs fell-short (truncated). Channeling built BEFORE the pattern is named.
- TYPE: indicator
- SOURCE: docs/RULESET.md (§E §2.2); docs/research/deep/11 (T18, T19, T20, T23)

### [CONFIRMATION-LINES] Two-stage completion timing (NeoWave)
- RULE: Stage 1 — price breaks the 2-4 line in < time(W5) ⇒ impulse over. Stage 2 — all of W5 retraced (to W5 origin) in ≤ time(W5) ⇒ confirmed. Both required; can only be checked on bars arriving after pattern completes (asynchronous).
- TYPE: time
- SOURCE: docs/RULESET.md (§E §2.6); docs/research/deep/11 (T21, T22, T49, §5.6)

### [PROCESS-METHOD] Post-constructive rules
- RULE: Reverse Logic — when counts conflict, prefer the least-complete plausible count (furthest from completion). Behaviour-over-structure — if post-pattern price doesn't confirm, the count is wrong. Post-correction thrust — after flat/zigzag, thrust proportional to correction size in ≤ correction duration.
- TYPE: process
- SOURCE: docs/RULESET.md (§E §2.9); docs/research/deep/11 (T50, T51, T36)

### [PROCESS-METHOD] Rule of Neutrality & Rollback (pre-labelling)
- RULE: Rule of Neutrality — merge tiny monowaves (< ~10% of adjacent wave) into neighbours before labelling to prevent phantom pivots. Rollback rules R1 (near-miss), R2 (one-bar spike), R3 (flat top) — correct monowave endpoints when price briefly overshoots a prior pivot. Wrong endpoints → wrong r21 ratios → wrong rule application → wrong labels. Thresholds are imprecise ("trivially small"/"barely exceeds") → flag rollback-corrected pivots as REF.
- TYPE: process
- SOURCE: docs/research/deep/11 (T02, T03, GAP-4, §5.1)

### [DATA] Chart standardisation (NeoWave pre-flight)
- RULE: Uniform bar resolution, arithmetic price scale (NOT log), no missing bars, bar compaction for overlapping bars. Pre-flight check: "Chart OK: uniform 4H bars, arithmetic scale" or WARN if log-scale detected; flag missing bar count.
- TYPE: data
- SOURCE: docs/research/deep/11 (T01)

### [SETUP-TRADE] A-1 Wave-3 entry
- RULE: W2 retraces 38.2–61.8% of W1 and holds above W1 start → enter on break + CLOSE above W1 high (or limit in the 50–61.8% zone with a momentum-reversal candle). Stop below W2 low (B-1); target 1.618×W1 from W2 low (C-1).
- TYPE: setup
- SOURCE: docs/RULESET.md (§F Table A / B / C)

### [SETUP-TRADE] A-3 Wave-5 entry
- RULE: W4 retraces 23.6–38.2% of W3, no W1 overlap → break + close above W3 high. Stop below W4 low (B-3).
- TYPE: setup
- SOURCE: docs/RULESET.md (§F)

### [SETUP-TRADE] A-4/A-8 Wave-5 / ending-diagonal fade (short)
- RULE: W5 ≈ 1.0–1.618×W1 or upper channel + RSI bearish divergence + W5 vol < W3 vol → break below W4 low / diagonal lower boundary. Stop above W5 extreme (B-4). Half size.
- TYPE: setup
- SOURCE: docs/RULESET.md (§F)

### [SETUP-TRADE] A-7 Triangle thrust
- RULE: ABCDE complete, E in channel → break of D extreme; target 75–125% of widest leg from E.
- TYPE: setup
- SOURCE: docs/RULESET.md (§F)

### [SETUP-TRADE] A-9 NeoWave 2-4 entry
- RULE: Enter in prior-impulse direction once both Stage-1 & Stage-2 timing gates confirm; stop at W5 extreme.
- TYPE: setup
- SOURCE: docs/RULESET.md (§F)

### [SETUP-TRADE] Stops (Table B)
- RULE: Structural, count-voiding level 0.1–0.3% beyond. B-1 [W3] below W2 low · B-3 [W5] below W4 low · B-4 [W5 fade] above W5 extreme · B-6 [wave-C long] below A start.
- TYPE: risk
- SOURCE: docs/RULESET.md (§F Table B)

### [SETUP-TRADE] Targets (Table C)
- RULE: C-1 [W3] T1 1.618×W1 from W2 low, T2 2.618×, T3 4.236× (extended); take 30–50% at T1, trail stop to breakeven. C-2 [W5] =W1 / +0.618×net(W1→W3) / upper 2-4 parallel. C-5 [post-ABC new impulse] 0.382/0.618/1.0 retrace of the correction. C-8 [Fib cluster] ≥3 overlapping Fib measurements within 1–2%.
- TYPE: risk
- SOURCE: docs/RULESET.md (§F Table C)

### [SETUP-TRADE] Confluence (Table D) — a label alone never trades
- RULE: Minimum viable = D-1 Fib zone + (D-2/D-3 momentum divergence) + (D-6/D-7 structure break) = ≥3 strands. Also D-4 RSI>60 in W3 up · D-5 W3 vol > W1 vol · D-11 NeoWave time gate · D-13 multi-TF align.
- TYPE: setup
- SOURCE: docs/RULESET.md (§F Table D)

### [RISK] Risk / time (Table E)
- RULE: E-2 [hard] minimum 2:1 R:R or no trade. E-1 fixed-fraction 1–2% (0.5% if <3 strands). E-4 W3 entry = full size; W5 fade / ABC = half. E-5/E-6 trail after T1 / below each W3 sub-wave. E-10 entry trigger must fire within ~the prior corrective-leg duration (Neely time gate) — else cancel. E-12 never buy a completed-W5 breakout.
- TYPE: risk
- SOURCE: docs/RULESET.md (§F Table E)

### [SETUP-TRADE] NeoWave trading method (entry/stop/confirmation)
- RULE: Entry after two consecutive bars in the new direction post-pattern; ALSO post-pattern price must move further and faster than largest counter-trend wave of the prior pattern. Stop above/below the pattern's origin (terminals: terminal start; impulse: W2 origin). Fib price targets: W3 = 1.618/2.618/4.236×W1 from W2 end; W5 = W1 or 0.618×W3 from W4 end; post-correction thrust ≈ prior correction size. Trading-method output gated: if Stage 1 not confirmed → "NO TRADE".
- TYPE: setup
- SOURCE: docs/research/deep/11 (T53, T54, T55, T57, §5.3)

### [VALIDATION] Invalidation levels (NeoWave)
- RULE: Count invalid if: W2 > 100% of W1 (trending); W2 > 61.8% of W1 (terminal); W4 overlaps W1 (trending); W3 shortest. Terminal count negated if price passes terminal origin.
- TYPE: validation
- SOURCE: docs/research/deep/11 (T57)

### [SETUP-TRADE] Wave-3 experimental strategy spec
- RULE: Rules: (1) detect W1 and W2 structure; (2) W2 retraces 38.2% to 78.6% of W1; (3) W2 must not exceed W1 origin; (4) entry only when current candle breaks W1 extreme; (5) stop beyond W2 extreme; (6) targets = 1.618× and 2.618× of W1 from W2 extreme. Must not be marked production-ready; tests for long/short/invalid-W2/no-breakout/no-lookahead.
- TYPE: setup
- SOURCE: Audit Pack 03 (TASK S010); Roadmap 01 Phase 11
- NOTES: Roadmap variant requires: confirmed W1, confirmed W2, W2 retracement zone, break-and-close above W1 high, structural stop at W2 low, R:R ≥ 2:1, confluence threshold (≥3 strands per Milestone H S003).

### [SETUP-TRADE] Wave-3 rule-faithful build plan
- RULE: (1) Pattern ID: verify W1 motive (:5) and W2 corrective (:3) on finer scale; (2) W2 zone tighten to 38.2–61.8% golden zone (76.4% deep = WARN), hold above W1 origin; (3) Confluence gate ≥3: Fib-zone (D-1) + RSI bullish divergence at W2 low (D-3) + BOS/CHoCH up (D-7), optional vol W3>W1 (D-5); (4) Entry break+close above W1 high, entry-trigger window = W2 duration (not 96 bars); (5) Stop W2 low − 0.1–0.2%; (6) T1 1.618×W1, T2 2.618×, take 50% at T1, stop→breakeven, trail under W3 sub-waves; (7) require R:R ≥ 2:1 and confluence ≥3.
- TYPE: setup
- SOURCE: docs/RULESET.md (§H)

### [VALIDATION] Audit of crude wave3.py signal
- RULE: ZigZag pct=0.02 for W1/W2 = free/unprincipled (should be monowave/structure-labelled or multi-scale). W2 band 38.2–78.6% = loose (golden zone is 38.2–61.8%). 96-bar time stop = WRONG (not a rule; real gate = prior-leg duration E-10, hold managed by S&B time [1/3,3×]). EWO>0-only gate = insufficient (needs Fib zone + RSI divergence D-3 + BOS/structure break D-7, ≥3 strands). Missing: W1-is-:5/W2-is-:3 check, R:R gate (E-2), scale-out/trail, alternate count, multi-TF, volume W3>W1.
- TYPE: validation
- SOURCE: docs/RULESET.md (§G)
- NOTES: The +0.17–0.44R result got the skeleton right (R1, A-1, B-1, C-1) but is not rule-faithful; arbitrary 96-bar stop and EWO-only gate could be carrying or masking the edge.

### [VALIDATION] Sub-wave verification limitation
- RULE: Engine works on single-degree pivot sequences; sub-structure rules (3-3-3-3-3 vs 5-3-5-3-5) cannot be machine-checked without sub-degree pivot data → all sub-structure checks flagged REF, requiring human/multi-degree verification. Structure-label ambiguity is irreducible for 30–40% of monowaves → carry multiple candidate labels forward (":5|:3" notation).
- TYPE: validation
- SOURCE: docs/research/deep/06 (§14.1); docs/research/deep/11 (§5.2)

### [VALIDATION] Throw-over is empirical, not a rule
- RULE: Presence/absence of throw-over does not validate/invalidate an ending diagonal; it signals completeness (throw-over = likely complete; fall-short = possibly still building or truncated 5th).
- TYPE: validation
- SOURCE: docs/research/deep/06 (§14.4)

### [VALIDATION] Combination recursion cap
- RULE: Combinations can be nested (a double three can be a leg of a larger triple three). Cap recursion depth to avoid over-counting.
- TYPE: validation
- SOURCE: docs/research/deep/06 (§14.9)

### [AUTOMATION-SPEC] RuleResult status model
- RULE: Status = PASS / FAIL / WARN / NA / REF. RuleResult contains rule name, status, detail, severity, source-profile. Hard FAIL invalidates count; WARN does not invalidate (reduces confidence); REF means manual review required; NA when not applicable. Hard rule violation = wrong count.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 6); Audit 02 (Phase 4); docs/research/deep/06 (§1); docs/RULESET.md (legend)

### [AUTOMATION-SPEC] Rule profile separation
- RULE: Every rule must belong to a profile; classic Elliott and SOW/NeoWave rules must remain separate profiles. Profiles: classic_elliott, sow_neowave_strict, hybrid_research (also: experimental_wave3, manual_review). Each profile decides which rules are hard, which are warnings, which require manual review. Reject if it mixes classical Elliott and NeoWave as one undefined rule set.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 7); Roadmap 05 (Gate 4); Audit 02 (Phase 7); Audit 04 (§3)

### [AUTOMATION-SPEC] MonoWave required fields
- RULE: Each mono-wave must compute: start_time, end_time, confirmed_time, start_price, end_price, direction, price_length, time_length, percent_change, slope, retracement_against_previous, extension_against_previous (also signed length). Only confirmed pivots generate mono-waves; provisional pivots excluded; mono-waves chronological. Do not label Elliott waves at this stage.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 5); Audit 03 (TASK S005)

### [AUTOMATION-SPEC] Causal ZigZag pivot contract
- RULE: Causal percentage-reversal ZigZag: each confirmed pivot includes timestamp when reversal confirmation occurred; pivot confirmation timestamp ≥ pivot timestamp; final extreme remains provisional (confirmed_t = None) and must not be used for candidate generation; output pivots alternate H/L; same-kind adjacent pivots collapse to the more extreme pivot; running on bars[:t] never needs bars after t.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 4); Audit 03 (TASK S003); Roadmap 02 (map)

### [AUTOMATION-SPEC] Fractal swing pivot contract
- RULE: n-left / n-right fractal swing pivots: a pivot at index i is confirmed only at i+n_right; no pivots allowed in the final n_right bars (cannot be confirmed yet); ties should not produce pivots; tests for swing highs/lows, confirmation lag, no-lookahead.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 4); Audit 03 (TASK S004)

### [AUTOMATION-SPEC] Candidate output schema
- RULE: Candidates ranked, not forced. Example: {"pattern":"possible_impulse","status":"VALID_WITH_WARNINGS","confidence":0.68,"failed_rules":[],"warnings":["wave_2_deeper_than_typical"],"manual_review":["degree_assignment"]}.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 8)

### [AUTOMATION-SPEC] Confluence engine role
- RULE: Confluence answers "Is the permitted reversal actually being confirmed?" and must not create wave labels by itself; kept separate from wave labeling. Split into RSI/MACD/volume/structure-break(CHoCH/BOS)/channel/cycle modules. Applied only after structural detection is stable.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 9); Audit 02 (Phase 9)

### [AUTOMATION-SPEC] Ghost-forward validation contract
- RULE: Feed bars one timestamp at a time; at index t engine may receive only bars[:t+1]; every candidate/signal records knowable_time; validator proves no signal used bars later than knowable_time. Output ledger: forecast_time, entry_time, direction, target, stop/invalidation, result, bars_held, R multiple. No trading strategy inside the validator. Ghost-forward becomes a permanent validation layer.
- TYPE: automation-spec
- SOURCE: Roadmap 01 (Phase 10); Audit 03 (TASK S009); Audit 02 (Phase 8)

### [VALIDATION] No-lookahead policy
- RULE: No future bars read by signal logic; pivots use confirmed_t (not pivot_t) for signal timing; last unconfirmed pivot excluded from candidate generation; backtests run bar-by-bar (not full-history labeling first); every signal has a timestamp proving when it became knowable.
- TYPE: validation
- SOURCE: Audit 04 (§1); Roadmap 05 (Gate 2)

### [DATA] New bar schema (Alpaca MCP)
- RULE: Fields: symbol, timestamp (datetime / unix ns), open, high, low, close, volume, vwap (optional), timeframe, session_type (regular/extended/full), source (alpaca_mcp), adjustment (raw/split/all). Validate: duplicate candles rejected, missing timestamps detected/logged, timezone awareness, invalid OHLC values. Cache path: /data_cache/alpaca/{symbol}/{timeframe}/{session_type}.parquet.
- TYPE: data
- SOURCE: Roadmap 01 (Phase 2); Audit 02 (Phase 2); Audit 00 (§3.3); Roadmap 05 (Gate 3)

### [DATA] Data layer must be built on Alpaca MCP, not legacy REST/JSON
- RULE: New data layer written cleanly around Alpaca MCP (~10 years of bars, extended-hours). Old scripts/alpaca_fetch.py and data/live/*.json are reference-only, not canonical. Do not use old data layer or JSON snapshots for the new engine.
- TYPE: data
- SOURCE: Roadmap 00 (§2); Roadmap 01 (Phase 2); Audit 00 (§3.3)

### [VALIDATION] Statistical validation checklist
- RULE: Minimum trade count defined before evaluation; results split by symbol, timeframe, session type, and regime; costs and slippage included; out-of-sample validation performed; multiple-testing risk logged; positive result not accepted without baseline comparison. Strategy baselines: random-entry, flipped-direction, buy-and-hold, trend-following. RTH and extended-hours separated.
- TYPE: validation
- SOURCE: Audit 04 (§4, §5); Audit 02 (Phase 10)

### [VALIDATION] Strict wave-3 sample too small
- RULE: Strict wave-3 reports underpowered: AVGO strict = 3 trades, MRVL strict = 7 trades — not enough to claim edge. Looser wave-3 signal has more trades but needs broader testing.
- TYPE: validation
- SOURCE: Audit 00 (§3.6)

### [VALIDATION] Old forecast has no edge — research only
- RULE: Old next-leg forecast (completed structure → predict opposite of last leg → trade) showed weak/no edge; treat as research reference only, never as production trading signal. Correct wave counts do not automatically create trading edge; separate structure detection from trade confirmation.
- TYPE: validation
- SOURCE: Audit 00 (§3.2, §9); Roadmap 00 (§3); Roadmap 02 (map, forecast.py Archive P4)

### [SCOPE] Legacy repo is reference-only
- RULE: Ewace_2026 is a legacy research prototype / salvage source / test-idea library / research evidence — NOT the direct production base. Archive under legacy/ewace_2026_reference/. Do not edit legacy files; production code must never import from legacy; do not let agents scan the whole legacy folder; do not treat generated reports as requirements. 177 tests passed at audit.
- TYPE: scope
- SOURCE: Roadmap 00; Roadmap 01 (Phase 0); Audit 00 (§1, §2.1)

### [SCOPE] Legacy import guard
- RULE: No file under src/ may contain "legacy.", "ewace_2026_reference", or "wavelib." import tokens. Guard test scans src/*.py and asserts forbidden tokens absent. Migration pattern: read old behavior → write new tests → clean new implementation → prove no-lookahead → do not import old module.
- TYPE: scope
- SOURCE: Roadmap policies/LEGACY_IMPORT_POLICY; Roadmap task_cards TASK_L002; Roadmap 04 (Step 3)

### [SCOPE] LLM context policy
- RULE: An agent never receives the entire legacy repo. Pattern: one agent + one task card + one or two legacy reference files + one acceptance checklist. Level 0 (no legacy) for skeleton/data/config; Level 1 (single file) for simple migration; Level 2 (2–3 files) when behavior crosses modules; Level 3 (human-only, must be summarized first) for reports/charts/data/live/AVGO-MRVL conclusions/forecast reports/full docs. If a task card does not name a specific legacy source file, agent must not open the legacy repo.
- TYPE: scope
- SOURCE: Roadmap 03; Roadmap 00 (Practical Rule)

### [SCOPE] Forbidden agent behaviors
- RULE: Agents must not: import from legacy in production; edit legacy files; rewrite roadmap based on old reports; implement old forecast.py as production signal; use static JSON snapshots as canonical data; use AVGO/MRVL levels as universal rules; add ML before the deterministic rule engine is stable; add live trading/order execution.
- TYPE: scope
- SOURCE: Roadmap 03 (Forbidden); Audit 00 (§7)

### [SCOPE] Symbol-agnostic requirement
- RULE: AVGO/MRVL charts, reports, levels, and single-symbol validation outcomes are examples only, not universal Elliott rules; do not let agents infer universal trading rules from them. Migrated code must be symbol-agnostic (Migration Rule test 3).
- TYPE: scope
- SOURCE: Audit 00 (§3.4, §6); Roadmap 00 (§4); Audit 02 (Migration Rule)

### [PROCESS-METHOD] Acceptance gates for legacy reuse
- RULE: A legacy module is accepted only if all hold: architecture fit = yes; no-lookahead proof = yes; data contract fit = yes; rule profile clear = yes; tests pass = yes; human-readable output = yes; no direct legacy import = yes. Pipeline: Data → Pivots → MonoWaves → Rule Validation → Pattern Candidates → Scoring → Manual Output → Backtest. Reject if it mixes detection + strategy + forecast + charting + data fetching.
- TYPE: process
- SOURCE: Roadmap 05 (Gates 1–7, Final Formula)

### [PROCESS-METHOD] Migration order (four-test rule)
- RULE: Never migrate code because it exists. Migrate only if: (1) fits new architecture; (2) has/can receive no-lookahead tests; (3) is symbol-agnostic; (4) supports manual TradingView workflow or future automation. Order: Tests first, Contracts second, Code third, Reports last. P0: RuleStatus/RuleResult → Pivot.confirmed_t → causal zigzag tests → implementation → fractal tests → implementation → pivots-to-monowave → no-lookahead suite.
- TYPE: process
- SOURCE: Audit 02 (Migration Rule, Final); Roadmap 02 (P0/P1/P2 order)

### [PROCESS-METHOD] Classical Elliott migration scope (Phase 5)
- RULE: Only classical basics first: Impulse candidate = 5 waves; W2 cannot exceed origin of W1; W3 cannot be shortest among 1/3/5; W4 cannot overlap W1 except terminal profile; Alternation as WARN; Fibonacci as scoring, not hard invalidation. Do not include yet: full NeoWave zoo, diametric, neutral triangle, extracting triangle, complex correction engine.
- TYPE: process
- SOURCE: Audit 02 (Phase 5); Audit 03 (TASK S007)

### [PROCESS-METHOD] Corrective rules migration (one at a time)
- RULE: Implement corrections one at a time: Zigzag, Flat, Triangle. Each must have: mandatory rules, soft rules, confirmation rule, invalidation rule, TradingView manual drawing note. Ambiguous NeoWave interpretation returns REF or WARN, never forced PASS. Do not implement complex corrections/diametric/neutral triangle/extracting triangle yet.
- TYPE: process
- SOURCE: Audit 02 (Phase 6); Audit 03 (TASK S008)

### [SETUP-TRADE] Manual TradingView output format
- RULE: Generate manual trading notes, not blind buy/sell. Example fields: Symbol, Timeframe, Pattern candidate, Current position (e.g. C wave in progress), Invalidation (B high), Confirmation (Break of 0-B line), TradingView actions (mark pivots, draw 0-B trendline, watch for break, validate with Ichimoku/cloud/momentum).
- TYPE: setup
- SOURCE: Roadmap PHASED_USAGE_ROADMAP (Milestone G)

### [PROCESS-METHOD] Human interpretability requirement
- RULE: Output must explain which rule passed/failed/warned/requires manual review and why the candidate scored as it did. Reject black-box labels like "BUY because Elliott Wave says so" or "Wave 3 confirmed without details".
- TYPE: process
- SOURCE: Roadmap 05 (Gate 6)

### [SCOPE] Degree assignment kept behind manual-review flag
- RULE: assign_degrees_neely is heuristic and can mislead → research only first, keep behind manual-review flag (P2). Strict NeoWave labeling and forecast backtest helpers are research-only (P3).
- TYPE: scope
- SOURCE: Audit 01 (salvage matrix)

### [INDICATORS] Confluence strands catalog
- RULE: Candidate confirmation strands: RSI divergence, MACD turn, volume capitulation, CHoCH/BOS (structure break), channel break, cycle alignment seam (FLD/Hurst via CycleSignal / cycle_seam). Confluence must remain separate from wave labeling.
- TYPE: indicator
- SOURCE: Audit 02 (Phase 9); Roadmap 02 (map cycle_seam)

### [SCOPE] Not-in-scope items
- RULE: Do not add: live trading / broker executor / order execution; ML before deterministic rule engine is stable and baseline rule performance exists; trade sizing/execution advice. Live trading fails closed (gates only).
- TYPE: scope
- SOURCE: Roadmap 03; Audit 02 (Phase 10); Audit 00 (§7)

## FILES READ
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/00_WHEN_TO_USE_THIS_REPO.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/01_LEGACY_REPO_ROADMAP.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/02_LEGACY_TO_NEW_ARCHITECTURE_MAP.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/03_CONTEXT_POLICY_FOR_CODEX_CLAUDE.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/04_REPO_CLEANUP_AND_ARCHIVE_PLAN.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/05_ACCEPTANCE_GATES_FOR_LEGACY_REUSE.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/06_FINAL_DECISION_SUMMARY.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/README.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/matrices/LEGACY_USAGE_DECISION_MATRIX.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/policies/LEGACY_IMPORT_POLICY.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/roadmap/PHASED_USAGE_ROADMAP.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L001_ARCHIVE_LEGACY_REPO.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L002_ADD_NO_LEGACY_IMPORT_GUARD.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L003_ALPACA_MCP_DATA_CONTRACT.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L004_PORT_CORE_MODELS.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L005_PORT_CAUSAL_ZIGZAG.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L006_PORT_FRACTAL_PIVOTS.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L007_BUILD_MONOWAVE_ENGINE.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L008_SPLIT_RULE_ENGINE.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L009_REBUILD_GHOST_FORWARD.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/ElliottWave_Legacy_Repo_Usage_Roadmap_Pack/task_cards/TASK_L010_WAVE3_RESEARCH_ONLY.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/00_EXISTING_REPO_AUDIT_REPORT.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/01_LEGACY_SALVAGE_MATRIX.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/02_MIGRATION_PLAN.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/03_CODEX_TASK_CARDS_FOR_SALVAGE.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/04_VALIDATION_CHECKLIST.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Existing_Repo_Audit_Pack/ElliottWave_Existing_Repo_Audit_Pack/README.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/docs/RULESET.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/docs/research/deep/06_diagonals_and_patterns.md
- /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/Ewace_2026-claude-ewave-2026-base-repo-ZRYzS/docs/research/deep/11_neowave_techniques.md
