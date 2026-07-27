# RULESET — Elliott Wave + NeoWave, the complete rules we build to

_Compiled line-by-line from our own research (`docs/research/01_elliott_wave.md`,
`02_neowave_neely.md`, `04_…` / `practitioner/04_trading_rules_risk.md`,
`deep/05–11`, `practitioner/01–03`). Every rule cites its source doc. This is the
authoritative spec the engine and the trade signals must implement — no arbitrary
parameters. Where the theory leaves a value free, it is marked **[free]** with its
basis; where the theory fixes it, it is **[hard]** or **[guideline]**._

Legend: **[H]** hard rule (violation = wrong count) · **[G]** guideline (probabilistic,
WARN) · **[N]** NeoWave-specific · **[free]** tunable with stated basis.

---

## A. ELLIOTT — IMPULSE (motive 5-wave) — doc 01 §2.1

- **R1 [H]** Wave 2 never retraces > 100% of wave 1 → `end(W2)` stays beyond `origin(W1)`. (01 §2.1)
- **R2 [H]** Wave 3 is never the *shortest* of 1/3/5 → `len(W3) > len(W1)` OR `> len(W5)`. (01 §2.1)
- **R3 [H]** Wave 4 does not enter wave-1 price territory → bull: `low(W4) > high(W1)`. *Suspended for diagonals.* (01 §2.1)

### Impulse guidelines — doc 01 §2.2
- **Extension [G/N]** exactly one of 1/3/5 extends; equities → usually W3. Extended wave ≥ **1.618×** the next-longest motive wave. *In NeoWave this is **[H]** (doc 02 §2.4): no 161.8× ⇒ no extension.*
- **Equality [G]** the two non-extended motive waves tend to equality OR 0.618×. (01 §2.2)
- **Alternation [G]** W2 and W4 alternate in form/depth/time; depth difference typically > 15–20 pp. (01 §2.2)
- **W2 depth [G]** typical **50–61.8%** of W1; valid 38.2% (shallow) … 76.4–85.4% (deep). (01 §2.2)
- **W4 depth [G]** typical **23.6–38.2%** of W3; 50% only in triangles. (01 §2.2)
- **W3 vs W1 [G]** most commonly **1.618×**; 2.618×/3.618× when extended; ≥1.0× lower bound. (01 §2.2)
- **Personality [G]** W1 tentative · W2 deep/sharp · **W3 strongest, broadest, highest momentum/volume** · W4 sideways/boring · W5 frothy, momentum divergence, lower volume. (01 §2.2)
- **Channeling [G/N]** base 0-2 line; acceleration 1-3 line; deceleration 2-4 line (see §D). (01 §2.2, 02 §2.2)

## B. ELLIOTT — CORRECTIONS — doc 01 §2.3
- **Zigzag (5-3-5) [H]** B retraces **≤ 61.8%** of A (the classifier); B not past A origin; C surpasses end of A. C typ. 0.618–1.618×A, equality common. (01 §2.3.1)
- **Flat (3-3-5) [H]** B retraces **> 61.8%** of A. Subtypes: **Regular** B 61.8–100%, C≈A; **Expanded** B >100% (105–138%), C >100% of A; **Running** B >100%, C truncated (< end of A). (01 §2.3.2)
- **Triangle (3-3-3-3-3) [H]** 5 legs a-e each corrective. Contracting a>b>c>d>e (converging); expanding (diverging); barrier (one flat line). Position: W4, B, or final X. Wave E often over/undershoots a-c line. (01 §2.3.3)
- **Combination [H]** double W-X-Y / triple W-X-Y-X-Z; X < 61.8% of W; triangle only as final; never >1 zigzag. (01 §2.3.4)

## C. ELLIOTT — DIAGONALS — doc 01 §2.4
- **Leading (W1/A):** sub-structure **5-3-5-3-5**; W4/W1 overlap common; *continuation* follows. (01 §2.4.2)
- **Ending (W5/C):** sub-structure **3-3-3-3-3**; W4/W1 overlap **expected**; *sharp full reversal* follows (fast retrace to origin — see NeoWave §F). (01 §2.4.1)

## D. DEGREE & FIBONACCI — doc 01 §2.5–2.6
- **Degree by duration [free, basis=Frost&Prechter]:** GrandSC multi-century · SC 40–70y · Cycle 1y–decades · Primary months–2y · Intermediate weeks–months · Minor days–weeks · Minute hrs–days · Minuette min–hrs · Subminuette <min. (01 §2.5)
- **Retrace levels:** .236/.382/.5/.618/.764/.786. **Extension levels:** 1.0/1.272/1.618/2.0/2.618/3.618/4.236. (01 §2.6)
- **Per-wave targets (table, 01 §2.6 / 04 Fib ref):** W2 .5/.618 of W1 · **W3 1.618×W1 (2.618/3.618 ext)** · W4 .236/.382 of W3 · W5 =W1 / .618×net(W1→W3) / 1.618×W1 · zigzag C =A / 1.618×A · flat B .618–1.382×A · flat C 1.0–1.618×A.

## E. NEOWAVE — STRUCTURE & DEGREE — doc 02
- **Bottom-up [N]** monowave → polywave (3/5) → multiwave → macrowave; *construct from smallest up.* (02 §2.1)
- **Monowave structure labels [N]** `:5`(motive: retraces prior wave faster than it formed, more price/time) vs `:3`(corrective: ≤61.8% retrace, ≥ equal time/complexity); + `:F3 :c3 :L5 :s5 :sL3 :L3`. *This is the pattern-identity test my signal skips.* (02 §2.1)
- **Seven retracement rules [N]** by m2/m1: R1 <38.2% (m1=extended 3rd) · R2 38.2–61.8% (1st/5th) · R3/4 61.8–100% (a-wave/1st, conditions a–d on m0/m1) · R5 100–161.8% (not a retrace→trend change) · R6 161.8–261.8% (strong reversal) · R7 >261.8% (x-wave/extreme). (02 §2.5)
- **Similarity & Balance [N, H-for-degree]** adjacent same-degree waves relate in **price ∈ [⅓, 3×]** AND **time ∈ [⅓, 3×]**; ≥1 must hold, both ideal. **THIS is the time rule** (not a fixed bar count). (02 §2.3)
- **Rule of Proportion / Extension [N, H]** subwave ≤ parent unless extending; extension **≥ 161.8×** next-longest. (02 §2.4)

### NeoWave channeling & confirmation — doc 02 §2.2/2.6
- **0-2 line:** locate true end of W2; W3 should not break it. **2-4 line [N,H]:** no part of W3 or W5 breaks it. **1-3 line:** W5 target; throw-over (blow-off) vs fell-short (truncated). (02 §2.2)
- **Two-stage completion timing [N,H]:** *Stage 1* — price breaks the 2-4 line in **< time(W5)** ⇒ impulse over. *Stage 2* — all of W5 retraced in **≤ time(W5)** ⇒ confirmed. (02 §2.6)
- **Terminals [N]:** 3-3-3-3-3, W4/W1 overlap, W2 ≤ 61.8% of W1; after completion **full fast retrace to origin in ~¼–½ build-time** (bias, not a price/time guarantee). (02 §2.7)
- **Post-constructive [N]:** *Reverse Logic* — prefer the least-complete plausible count; *Behaviour-over-structure* — if post-pattern price doesn't confirm, the count is wrong. (02 §2.9)

## F. TRADING RULES — practitioner/04

### Entry by wave position (Table A)
- **A-1 [W3 entry]:** W2 retraces 38.2–61.8% of W1 and holds above W1 start → enter on **break + CLOSE above W1 high** (or limit in the 50–61.8% zone with a momentum-reversal candle).
- **A-3 [W5 entry]:** W4 retraces 23.6–38.2% of W3, no W1 overlap → break + close above W3 high.
- **A-4/A-8 [W5 / ending-diagonal fade — short]:** W5 ≈ 1.0–1.618×W1 or upper channel + RSI bearish divergence + W5 vol < W3 vol → break below W4 low / diagonal lower boundary.
- **A-7 [triangle thrust]:** ABCDE complete, E in channel → break of D extreme; target 75–125% of widest leg from E.
- **A-9 [NeoWave 2-4]:** enter in prior-impulse direction once both Stage-1 & Stage-2 timing gates confirm; stop at W5 extreme.

### Stops (Table B) — the structural, count-voiding level (0.1–0.3% beyond)
- **B-1 [W3]** below **W2 low** · **B-3 [W5]** below W4 low · **B-4 [W5 fade]** above W5 extreme · **B-6 [wave-C long]** below A start.

### Targets (Table C) — partial-exit + trail
- **C-1 [W3]** T1 **1.618×W1 from W2 low**, T2 2.618×, T3 4.236× (extended). **Take 30–50% at T1, trail stop to breakeven.**
- **C-2 [W5]** =W1 / +0.618×net(W1→W3) / upper 2-4 parallel.
- **C-5 [post-ABC new impulse]** 0.382/0.618/1.0 retrace of the correction.
- **C-8 [Fib cluster]** where ≥3 independent Fib measurements overlap within 1–2% = the target zone.

### Confluence (Table D) — **a label ALONE never trades**
Minimum viable = **D-1 Fib zone + (D-2/D-3 momentum divergence) + (D-6/D-7 structure break)** = ≥3 strands. Also: D-4 RSI>60 in W3 up · D-5 W3 vol > W1 vol · D-11 NeoWave time gate · D-13 multi-TF align.

### Risk / time (Table E)
- **E-2 [H-for-trading]** minimum **2:1 R:R** or no trade. **E-1** fixed-fraction 1–2% (0.5% if <3 strands). **E-4** W3 entry = full size; W5 fade / ABC = half. **E-5/E-6** trail after T1 / below each W3 sub-wave. **E-10** entry trigger must fire within ~the prior corrective-leg duration (Neely time gate) — else cancel. **E-12** never buy a completed-W5 breakout.

---

## G. AUDIT — current `wavelib/wave3.py` vs this ruleset

| What the signal does now | Rule basis? | Verdict |
|---|---|---|
| ZigZag pct=0.02 to find W1/W2 | none (proxy for monowave construction §E) | **[free, unprincipled]** — should be monowave/structure-labelled, or at least multi-scale; 0.02 is arbitrary |
| W2 retrace band 38.2–78.6% | partial (A-1 golden zone is 38.2–61.8%; 76.4–85.4% is "deep") | **loose** — widen of the golden zone; OK-ish but not the high-prob band |
| W2 must hold W1 origin (`c>a`) | **R1 [H]** | ✅ correct |
| Entry = break above W1 high (close) | **A-1** | ✅ correct |
| Stop = W2 low − 0.1% | **B-1** | ✅ correct |
| Target = 1.618×W1 from W2 low | **C-1** | ✅ correct (missing T2/T3 scale-out) |
| **EWO>0 only** | weak proxy for D-4/personality | **insufficient** — Table D needs Fib-zone + **RSI divergence (D-3)** + **structure break/BOS (D-7)**; ≥3 strands. A label alone never trades. |
| **96-bar time stop** | **NONE** | **❌ WRONG** — not a rule. Real: entry-trigger window = prior-leg duration (E-10); hold managed by structure + S&B time [⅓,3×] (§E), not a constant |
| Single target, no scale-out/trail | C-1/E-5/E-6 | **missing** — take 30–50% at T1, trail to breakeven, trail under sub-waves |
| No W1-is-`:5` / W2-is-`:3` check | **§E structure labels** | **❌ missing pattern identification** — W1 must be motive (5 / `:5`), W2 corrective (3 / `:3`) |
| No R:R gate | **E-2** | **missing** — reject < 2:1 |
| No alternate count / multi-TF | E-3 / D-13 | missing |
| No volume W3>W1 | D-5 | missing |

**Conclusion:** the +0.17–0.44R result came from a signal that gets the *skeleton* right (R1, A-1, B-1, C-1) but is **not rule-faithful** — it lacks pattern identification (is this really a motive W1 + corrective W2?), the confluence gate (≥3 strands), the correct **time logic** (S&B, not 96 bars), and scale-out/R:R discipline. The arbitrary 96-bar stop and EWO-only gate could be carrying or masking the edge.

---

## H. BUILD PLAN — a rule-faithful wave-3 entry (next)

1. **Pattern ID:** verify W1 is motive (5 sub-waves / `:5`) and W2 is corrective (3 / `:3`) using the structure-label/monowave logic (§E) on a finer scale — not a blind 2-leg ZigZag.
2. **W2 zone:** tighten to the 38.2–61.8% golden zone (allow 76.4% deep as WARN); hold-above-W1-origin (R1).
3. **Confluence gate (≥3, Table D):** Fib-zone (D-1) + **RSI bullish divergence at the W2 low** (D-3) + **BOS/CHoCH up** (D-7); optional vol W3>W1 (D-5), EWO/RSI>... (D-4).
4. **Entry:** break + close above W1 high (A-1). **Entry-trigger window = W2's duration** (E-10), not 96 bars.
5. **Stop:** W2 low − 0.1–0.2% (B-1).
6. **Targets + management:** T1 1.618×W1, T2 2.618× (C-1); **take 50% at T1, stop→breakeven, trail under W3 sub-waves** (E-5/E-6). Exit logic governed by structure, with an S&B-time *monitor* ([⅓,3×] vs W1), not a fixed bar count.
7. **Gate:** require **R:R ≥ 2:1** (E-2) and confluence ≥ 3 or no trade.
8. **Re-run the year-long ghost forward test** on the rule-faithful version and compare to the current +0.17–0.44R — to see whether *the rules themselves* add edge over the crude skeleton.

---

## I. DOCTRINE COMPLETION (2026-07 bundle audit — SOW/Ashish Kyal sources + deep/06,11)

_Added after auditing the full source bundle (SOW Day-1/Day-2 notes, NeoWave
training deck, Fibo system sheet, Brahmastra mentorship material, master-pack
wave-rules reference). Sections below close the gaps between this spec, the
source doctrine, and the engine's own deeper research._

### I.1 Diametric (7-leg a–g) [N]
- **[H]** Exactly 7 legs a–g, each corrective (3-3-3-3-3-3-3); **no X-wave
  connectors**. (deep/11 T42; SOW Day-2 p.6)
- **[H-time]** Time similarity is the norm: adjacent legs relate in TIME
  (equality in time, not price). (deep/11 T43)
- **[G]** Paired-leg relationships by price OR time: **G≈A (or G≈61.8%A),
  F≈B, E≈C**. (SOW Fibo sheet; Day-2 p.6)
- Shapes: **bow-tie** (middle leg shortest — contract then expand),
  **diamond** (middle leg longest — expand then contract), running variant.
- **[G]** Post-g **thrust ≈ widest part** of the pattern; sharp. (deep/11 T44)

### I.2 Triangle sub-rules (supplementing §B) [N/G]
- **[G]** Wave **E is the smallest leg** (contracting family). (ref §66-79)
- **[G]** **≥3 of the 5 legs retrace >50%** of the preceding leg. (ref)
- **[H]** **B-D line discipline**: the baseline through the ends of B and D
  must be clean — **no part of C or E breaks it prematurely**; the decisive
  post-E break OF the B-D line is the triangle-complete confirmation.
  (SOW Day-2 p.4; ref §78)
- **[G]** Position rule: a triangle cannot normally form in wave 2 (terminal
  context excepted). (SOW Day-2 p.4)
- **[G]** Thrust: 75–125% of the widest leg from E (SOW quotes 100–125%);
  thrust should complete in **≤ the shortest leg's duration**. (deep/11 T40)
- **Neutral triangle [N]**: C longest; A≈E (each ≥38.2% of C); C ≤ 261.8% of
  A. **Extracting triangle [N]**: **e < c < a AND d > b** (alternating
  contraction/expansion; Neely later folded it into the neutral family).
  (SOW Day-2 p.5; deep/11 T38/T59)
- **Symmetrical (9-leg) [N]**: 9 corrective legs; price+time+complexity
  similar within the advancing group and within the declining group; **no
  Fibonacci relationships** expected; no X-waves. (deep/11 T45)

### I.3 Complex-correction X bounds (supplementing §B) [N]
- **[H]** **Maximum two X waves** (W-X-Y or W-X-Y-X-Z; never more). (SOW
  Day-2 p.7)
- **[G]** Small-X: retraces **<61.8%** of the prior pattern W. 61.8–100% =
  large-X WARN. **[H]** X >100% of W without large-X context = structural
  error (not an x-wave).
- **[N]** **Large-X regime: X ≥ 1.618×W** ⇒ the "connector" is oversized —
  reassess degree and relabel (the correction is of a larger degree than
  assumed). (SOW Day-2 p.8)
- **[G]** X-wave complexity ≤ the prior correction's and ≥ its least-complex
  sub-wave. (deep/11 T46/T47)

### I.4 Flat B-wave bands (supplementing §B) [N]
Weak B: 61.8–80% of A · Normal B: 80–100% · **Strong B: >100%** (expanded/
running family). C-failure and double-failure flats exist (C falls short).
(deep/11 T60; SOW Day-2 p.3)

### I.5 Confirmation lines per family — the SOW two-stage pattern [N,H]
Every pattern family has a confirmation line; **no completion is trusted
until the line breaks within its time limit** (this generalizes §E's 2-4
rule):
| family | line | stage-1 break time limit |
|---|---|---|
| impulse | **2-4** | ≤ time(W5) (§E, implemented) |
| zigzag / flat | **0-B** | ≤ time(C) (SOW Day-2 p.2) |
| triangle | **B-D** (after E) | ≤ shortest-leg duration |
| diametric | boundary after G | ≈ ≤ time(G) |

Corrective **time rules**: in zigzag AND flat, **B should take ≥ the time of
A** [G]. Diagnosis heuristic [G]: if B takes LESS time than A → triangle/
diametric become more likely; if B ≥ A's time → all corrections possible, ZZ/
flat most likely. (SOW Day-2 p.9)

### I.6 Pre-labelling conditioning [N]
- **Rule of Neutrality**: merge monowaves smaller than ~10% of their
  neighbours before structure labelling. (deep/11 T02)
- **Endpoint rollback**: correct pivot endpoints on near-miss/one-bar-spike/
  flat-top cases before labelling. (deep/11 T03)
- **Chart standardization**: NeoWave proportion work assumes an arithmetic
  price scale and uniform bar spacing. (deep/11 T01) — the engine's
  log-magnitude comparisons (§E) are the deliberate large-range adaptation.

### I.7 Wave-2 61.8% posture (audit G4 — the documented decision)
The SOW/NeoWave sources state W2 ≤61.8% of W1 as *the* rule; classic Elliott's
inviolable rule is <100% (R1). **This engine keeps R1 (<100%) as the hard
invalidator** and enforces the 61.8% cap **per profile** through the W2
retracement bands (strict/golden profiles cap entry setups at 0.618, deep to
0.764 as WARN-band; the crude research profile allows to 0.786). Terminals
are exempt (W2 may retrace deeper — SOW Day-1 p.5). Rationale: demoting a
count to INVALID at 61.8% would discard structures the classic rule set
allows; the profile band achieves the SOW discipline where it matters — at
the entry gate.

### I.8 Scope notes (deliberate boundaries)
- **Time-cycles / date forecasting** (Brahmastra "Timing the Markets",
  forecasting dates): this is the **"when" layer** and belongs to the
  sibling repo chakra_quant; it enters this engine ONLY through the typed
  `CycleSignal` seam (`ewave.signals.cycle_seam`) as the 7th confluence
  strand. Not implemented here by design.
- **Gann price levels** (used as S/R confluence on the SOW charts): candidate
  future confluence strand; no validated level algorithm in the source
  bundle, so not implemented.
- **3-of-4 channel touch points** (zigzag/flat channel quality): manual
  charting heuristic [G, manual]; not automated.
