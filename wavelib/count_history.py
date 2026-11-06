"""
count_history.py — the count the engine HELD at every bar, not just the last one.
==================================================================================
`analyze_symbol` answers "what is the count now?".  This module replays the
history causally — at bar i it sees ``bars[:i]`` only — and records, for every
bar, two reads of the structure as the engine would have labelled it *at that
moment*:

* **anchored**: `wave_counts()` on the trailing `window` bars — the committed
  1-5 / A-B-C (A-E) count with pattern, degree label and honest confidence;
* **recent**:   `label_and_validate()` best candidate on the same window — the
  freshest validated 5-wave / 3-wave fragment.

Consecutive bars that hold the *same* labelling are compressed into a segment, so
the output is the count's **continuation**: how long each labelling survived,
and how it changed when it did (the legs EXTENDED, the pattern was RELABELLED,
or the anchor SHIFTED).  `render_count_history_page` draws it: price line, a
pattern band per bar, a scrubber/play-head that redraws the as-of labelled legs,
and the transitions table.  Pure stdlib; causal by construction.
"""
from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field

from .automation import label_and_validate
from .wavetree import wave_counts

_LABELS = {"IMPULSE": "12345", "DIAGONAL": "12345", "CORRECTION": "ABC"}


def _d(t) -> str:
    return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc).strftime("%Y-%m-%d")


@dataclass
class CountSegment:
    """One labelling held unchanged over a run of consecutive bars."""
    kind: str                       # "anchored" | "recent"
    pattern: str                    # IMPULSE / ZIGZAG / FLAT / TRIANGLE / CORRECTION / ... / NONE
    start_t: float                  # first bar on which this labelling was held
    end_t: float                    # last bar on which it was held
    n_bars: int
    legs: list                      # [(label, t0, p0, t1, p1), ...] as labelled at the time
    detail: dict = field(default_factory=dict)   # degree_label/confidence/coverage or hard_fails/warns/fib
    transition: str = "START"       # how this segment arose from the previous one

    @property
    def signature(self):
        return (self.pattern, tuple(int(l[3]) for l in self.legs))

    def describe(self) -> str:
        legs = " → ".join(f"{lab}@{p1:,.2f}" for lab, _t0, _p0, _t1, p1 in self.legs)
        return f"{self.pattern}: {legs}" if legs else self.pattern


@dataclass
class CountSnapshot:
    i: int                          # bars[:i] were visible
    t: float                        # time of the last visible bar
    close: float
    anchored: int | None            # index into anchored segments (None = no count)
    recent: int | None              # index into recent segments


@dataclass
class CountHistory:
    symbol: str
    bars: list
    window: int
    stride: int
    snapshots: list
    anchored: list                  # list[CountSegment]
    recent: list                    # list[CountSegment]

    def segments(self, kind: str = "anchored") -> list:
        return self.anchored if kind == "anchored" else self.recent


# ----------------------------------------------------------------------------
def _anchored_read(sub, scales):
    cs = wave_counts(sub, scales=scales, max_alternates=0)
    if not cs:
        return None
    c = cs[0]
    legs = [(lab, n.start.t, round(n.start.price, 4), n.end.t, round(n.end.price, 4))
            for lab, n in c.labels]
    return c.pattern, legs, {"degree_label": c.degree_label,
                             "confidence": round(c.confidence, 3),
                             "coverage": round(c.coverage, 3)}


def _recent_read(sub, degrees):
    cands = label_and_validate(sub, degrees=degrees, max_candidates=1)
    if not cands:
        return None
    c = cands[0]
    labs = _LABELS.get(c.count_type, "12345")
    legs = [(labs[k] if k < len(labs) else "?", w.start.t, round(w.start.price, 4),
             w.end.t, round(w.end.price, 4)) for k, w in enumerate(c.waves)]
    return c.count_type, legs, {"degree": c.degree, "hard_fails": c.hard_fails,
                                "warns": c.warns, "fib_score": round(c.fib_score, 3)}


def _transition(prev: CountSegment | None, cur: CountSegment) -> str:
    if prev is None:
        return "START"
    if prev.pattern == "NONE":
        return "NEW"
    if cur.pattern == "NONE":
        return "LOST"
    if prev.pattern != cur.pattern:
        return "RELABEL"
    if prev.legs and cur.legs and int(prev.legs[0][1]) == int(cur.legs[0][1]):
        return "EXTEND"                 # same origin, legs advanced/redrawn
    return "SHIFT"                      # same pattern, new anchor


def _push(segs: list, kind: str, read, t: float) -> int:
    """Append to the open segment if the labelling is unchanged, else start one."""
    pattern, legs, detail = read if read else ("NONE", [], {})
    sig = (pattern, tuple(int(l[3]) for l in legs))
    if segs and segs[-1].signature == sig:
        segs[-1].end_t = t
        segs[-1].n_bars += 1
        segs[-1].detail = detail        # confidence drifts within a segment; keep latest
    else:
        seg = CountSegment(kind, pattern, t, t, 1, legs, detail)
        seg.transition = _transition(segs[-1] if segs else None, seg)
        segs.append(seg)
    return len(segs) - 1


def count_history(bars, symbol: str = "", window: int = 300, stride: int = 1,
                  min_history: int = 60, degrees=(0.05, 0.10, 0.15),
                  scales=(0.04, 0.07, 0.12, 0.20), progress=None) -> CountHistory:
    """Causal replay: for i in range(min_history, len(bars)+1, stride) label
    ``bars[max(0, i-window):i]``.  Nothing after bar i-1 is ever visible."""
    snaps, anch, rec = [], [], []
    idx = list(range(min_history, len(bars) + 1, stride))
    if idx and idx[-1] != len(bars):
        idx.append(len(bars))           # always include the final bar
    for k, i in enumerate(idx):
        sub = bars[max(0, i - window):i]
        t = sub[-1][0]
        a = _push(anch, "anchored", _anchored_read(sub, scales), t)
        r = _push(rec, "recent", _recent_read(sub, degrees), t)
        snaps.append(CountSnapshot(i, t, sub[-1][4],
                                   None if anch[a].pattern == "NONE" else a,
                                   None if rec[r].pattern == "NONE" else r))
        if progress and (k % 250 == 0 or i == len(bars)):
            progress(f"{symbol} {k + 1}/{len(idx)}  {_d(t)}  anchored={anch[a].pattern} "
                     f"recent={rec[r].pattern}")
    return CountHistory(symbol, bars, window, stride, snaps, anch, rec)


# ----------------------------------------------------------------------------
def history_markdown(h: CountHistory, kind: str = "anchored", min_bars: int = 1) -> str:
    segs = [s for s in h.segments(kind) if s.n_bars >= min_bars]
    out = [f"### {h.symbol} — {kind} count continuation "
           f"(window {h.window} bars, stride {h.stride}, {len(h.snapshots)} replay steps)", "",
           "| held from | to | bars | transition | count as labelled at the time | detail |",
           "|---|---|---:|---|---|---|"]
    for s in segs:
        if kind == "anchored" and s.detail:
            det = (f"{s.detail.get('degree_label', '')} · conf {s.detail.get('confidence', 0):.0%}"
                   f" · covers {s.detail.get('coverage', 0):.0%}")
        elif s.detail:
            det = (f"deg {s.detail.get('degree')} · {s.detail.get('hard_fails')} hard-fails · "
                   f"{s.detail.get('warns')} warns · fib {s.detail.get('fib_score', 0):.0%}")
        else:
            det = ""
        out.append(f"| {_d(s.start_t)} | {_d(s.end_t)} | {s.n_bars} | {s.transition} | "
                   f"{s.describe()} | {det} |")
    n = len(h.segments(kind))
    kinds = {}
    for s in h.segments(kind):
        kinds[s.transition] = kinds.get(s.transition, 0) + 1
    out.append("")
    out.append(f"{n} segments; transitions: " +
               ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) + ".")
    return "\n".join(out) + "\n"


def _seg_json(s: CountSegment) -> dict:
    return {"p": s.pattern, "s": s.start_t, "e": s.end_t, "n": s.n_bars, "tr": s.transition,
            "legs": [[lab, t0, p0, t1, p1] for lab, t0, p0, t1, p1 in s.legs], "d": s.detail}


_PAGE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>__SYM__ count history · wavelib</title>
<style>
:root{--bg:#0a0d0f;--panel:#11161a;--grid:#1c252b;--ink:#e8eef0;--dim:#7c8a91;--teal:#27e0c4;--amber:#f2b134;--red:#ff5d57;--green:#48d97a;--line:#3aa6ff;--violet:#b48cff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:system-ui,Segoe UI,Roboto,sans-serif;padding:22px;min-height:100vh}
.wrap{max-width:1120px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;border-bottom:1px solid var(--grid);padding-bottom:14px}
h1{font-size:24px;line-height:1.15}h1 small{display:block;font-size:11px;color:var(--teal);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px}
.px{text-align:right}.px .now{font-size:22px;font-weight:700;color:var(--amber)}.px .sub{font-size:11.5px;color:var(--dim);margin-top:3px}
.chartbox{background:var(--panel);border:1px solid var(--grid);border-radius:10px;margin-top:16px;padding:8px 6px 4px;overflow:hidden}
svg{width:100%;height:auto;display:block}
.ctl{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin-top:12px;font-size:12.5px;color:#cdd6da}
.ctl input[type=range]{flex:1;min-width:220px;accent-color:var(--teal)}
button{background:#1a2228;color:var(--ink);border:1px solid var(--grid);border-radius:6px;padding:5px 11px;font-size:12.5px;cursor:pointer}button:hover{border-color:var(--teal)}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:10px;font-size:11.5px;color:var(--dim)}.legend span{display:inline-flex;align-items:center;gap:6px}.sw{width:14px;height:10px;border-radius:2px;display:inline-block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--grid);border-radius:10px;padding:14px 16px}.card h2{font-size:13.5px;color:var(--teal);margin-bottom:8px}
.card li{font-size:12.5px;line-height:1.65;color:#cdd6da;list-style:none;padding-left:14px;position:relative;margin-bottom:4px}.card li::before{content:"\25B8";position:absolute;left:0;color:var(--amber)}
.k{color:var(--amber);font-weight:700}.g{color:var(--green);font-weight:700}.r{color:var(--red);font-weight:700}.dim{color:var(--dim)}
table{width:100%;border-collapse:collapse;font-size:12px;margin-top:10px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--grid);vertical-align:top}th{color:var(--dim);font-weight:600;position:sticky;top:0;background:var(--panel)}
td.n{text-align:right;font-variant-numeric:tabular-nums}tr.seg{cursor:pointer}tr.seg:hover td{background:#182028}tr.cur td{background:#1a2a2a}
.tbox{max-height:420px;overflow:auto;border:1px solid var(--grid);border-radius:8px;margin-top:10px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:10.5px;font-weight:700;background:#1a2228}
.tabs{display:flex;gap:8px;margin-top:18px}.tabs button.on{border-color:var(--teal);color:var(--teal)}
.foot{margin-top:16px;font-size:10.5px;color:var(--dim);line-height:1.6;border-top:1px solid var(--grid);padding-top:12px}
</style></head><body><div class="wrap">
<header><div><h1><small>__SUBTITLE__</small>__SYM__ — count continuation, bar by bar</h1></div>
<div class="px"><div class="now" id="asof">—</div><div class="sub" id="asofsub">drag the scrubber · causal: only bars to the left of the play-head were visible</div></div></header>
<div class="chartbox"><svg id="c" viewBox="0 0 1100 600" preserveAspectRatio="xMidYMid meet"></svg></div>
<div class="ctl"><button id="play">▶ play</button><button id="step">step ▸</button>
<label>speed <select id="spd"><option value="1">1 bar</option><option value="3" selected>3 bars</option><option value="10">10 bars</option><option value="30">30 bars</option></select>/tick</label>
<input type="range" id="pos" min="0" max="0" value="0"><span id="posl" class="dim"></span>
<label><input type="checkbox" id="follow"> zoom to the engine's window</label></div>
<div class="legend"><span><i class="sw" style="background:var(--line)"></i>close</span><span><i class="sw" style="background:var(--teal)"></i>anchored count legs (as labelled then)</span><span><i class="sw" style="background:var(--amber)"></i>recent candidate legs</span><span><i class="sw" style="background:#2a3a44"></i>engine window</span>
<span><i class="sw" style="background:#27e0c4"></i>IMPULSE</span><span><i class="sw" style="background:#b48cff"></i>DIAGONAL</span><span><i class="sw" style="background:#f2b134"></i>ZIGZAG / CORRECTION</span><span><i class="sw" style="background:#ff8c5a"></i>FLAT</span><span><i class="sw" style="background:#48d97a"></i>TRIANGLE</span><span><i class="sw" style="background:#3a4650"></i>other / none</span></div>
<div class="grid2"><div class="card"><h2>Anchored count held at the play-head</h2><ul id="acard"></ul></div><div class="card"><h2>Recent validated candidate at the play-head</h2><ul id="rcard"></ul></div></div>
<div class="tabs"><button id="tabA" class="on">anchored segments (__NA__)</button><button id="tabR">recent segments (__NR__)</button></div>
<div class="tbox"><table><thead><tr><th>#</th><th>held from</th><th>to</th><th>bars</th><th>transition</th><th>count as labelled at the time</th><th>detail</th></tr></thead><tbody id="segs"></tbody></table></div>
<div class="foot">Replay of <b>__NSTEPS__</b> steps over <b>__NBARS__</b> daily bars (window __WINDOW__, stride __STRIDE__). At each step the engine saw only the bars up to the play-head, so every row is the count that was actually held then — including the ones later abandoned. EXTEND = same origin, legs advanced; RELABEL = pattern changed; SHIFT = same pattern, new anchor; LOST/NEW = count dropped/appeared. Analysis tooling only — not investment advice.</div>
</div>
<script>
const D=__DATA__;
const NS="http://www.w3.org/2000/svg",svg=document.getElementById("c");
const W=1100,H=600,mL=10,mR=86,mT=18,bandH=16,mB=36+2*bandH+8;
const COL={IMPULSE:"#27e0c4",DIAGONAL:"#b48cff",ZIGZAG:"#f2b134",CORRECTION:"#f2b134",FLAT:"#ff8c5a",TRIANGLE:"#48d97a",WXY:"#e0b0ff",NONE:"#3a4650"};
const col=p=>COL[p]||"#5a6a78";
const el=(n,a)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e};
const tx=(x,y,s,a)=>{const t=el("text",{x,y,...a});t.textContent=s;svg.appendChild(t);return t};
const tIdx=new Map();D.line.forEach((d,i)=>tIdx.set(d[0],i));
const idxOf=t=>{if(tIdx.has(t))return tIdx.get(t);let lo=0,hi=D.line.length-1;while(lo<hi){const m=(lo+hi)>>1;if(D.line[m][0]<t)lo=m+1;else hi=m}return lo};
const fmt=t=>new Date(t*1000).toISOString().slice(0,10);
const pos=document.getElementById("pos");pos.max=D.snaps.length-1;pos.value=D.snaps.length-1;
let kind="A",cur=D.snaps.length-1,timer=null;
const follow=document.getElementById("follow");
function draw(){
  svg.innerHTML="";const s=D.snaps[cur];const iEnd=s[0]-1; // bars[:i] visible -> last index i-1
  let i0=0,i1=D.line.length-1;
  if(follow.checked){i0=Math.max(0,s[0]-D.window);i1=iEnd}
  const vis=D.line.slice(i0,i1+1);
  let pmin=Infinity,pmax=-Infinity;vis.forEach(d=>{if(d[1]<pmin)pmin=d[1];if(d[1]>pmax)pmax=d[1]});
  const useLog=pmax/pmin>4;const f=p=>useLog?Math.log(p):p;const lo=f(pmin),hi=f(pmax),pad=(hi-lo)*0.06||1;
  const X=i=>mL+(i-i0)/((i1-i0)||1)*(W-mL-mR),Y=p=>mT+(hi+pad-f(p))/((hi-lo+2*pad)||1)*(H-mT-mB);
  // engine window shade
  const w0=Math.max(i0,s[0]-D.window);
  svg.appendChild(el("rect",{x:X(w0),y:mT,width:Math.max(0,X(iEnd)-X(w0)),height:H-mT-mB,fill:"#2a3a4455"}));
  // grid + axis
  for(let k=0;k<=6;k++){const v=lo+(hi-lo)*k/6;const p=useLog?Math.exp(v):v;svg.appendChild(el("line",{x1:mL,y1:Y(p),x2:W-mR,y2:Y(p),stroke:"#1c252b"}));tx(W-mR+8,Y(p)+4,"$"+(p>=100?p.toFixed(0):p.toFixed(1)),{fill:"#7c8a91","font-size":11})}
  for(let k=0;k<=5;k++){const i=Math.round(i0+(i1-i0)*k/5);tx(X(i),H-mB+14,fmt(D.line[i][0]).slice(0,7),{fill:"#7c8a91","font-size":11,"text-anchor":"middle"})}
  // price: visible (seen) part solid, future part faint
  const path=(a,b)=>{let d="";for(let i=a;i<=b;i++)d+=(i===a?"M":"L")+X(i).toFixed(1)+" "+Y(D.line[i][1]).toFixed(1)+" ";return d};
  if(iEnd>i0)svg.appendChild(el("path",{d:path(i0,Math.min(iEnd,i1)),fill:"none",stroke:"#3aa6ff","stroke-width":1.6,"stroke-linejoin":"round"}));
  if(iEnd<i1)svg.appendChild(el("path",{d:path(Math.max(iEnd,i0),i1),fill:"none",stroke:"#3aa6ff55","stroke-width":1.2,"stroke-dasharray":"3 4"}));
  // bands: pattern held at each bar (anchored top, recent bottom)
  const by=H-mB+22;const bw=Math.max(1,(W-mL-mR)/((i1-i0)||1));
  D.snaps.forEach(sn=>{const ii=sn[0]-1;if(ii<i0||ii>i1)return;const x=X(ii);const a=sn[2]==null?"NONE":D.A[sn[2]].p,r=sn[3]==null?"NONE":D.R[sn[3]].p;
    svg.appendChild(el("rect",{x:x-bw/2,y:by,width:bw+0.6,height:bandH-2,fill:col(a)}));svg.appendChild(el("rect",{x:x-bw/2,y:by+bandH,width:bw+0.6,height:bandH-2,fill:col(r)}))});
  tx(W-mR+8,by+11,"anchored",{fill:"#7c8a91","font-size":10});tx(W-mR+8,by+bandH+11,"recent",{fill:"#7c8a91","font-size":10});
  // as-of legs
  const legs=(seg,c,dy,bold)=>{if(!seg)return;seg.legs.forEach(([lab,t0,p0,t1,p1],k)=>{const a=idxOf(t0),b=idxOf(t1);if(b<i0||a>i1)return;
    svg.appendChild(el("line",{x1:X(a),y1:Y(p0),x2:X(b),y2:Y(p1),stroke:c,"stroke-width":bold?2.4:1.6,opacity:bold?1:0.9}));
    const up=p1>p0;svg.appendChild(el("circle",{cx:X(b),cy:Y(p1),r:bold?4.5:3.5,fill:c,stroke:"#0a0d0f","stroke-width":1.2}));
    tx(X(b),up?Y(p1)-9-dy:Y(p1)+17+dy,lab,{fill:c,"font-size":bold?13:11.5,"font-weight":700,"text-anchor":"middle"})})};
  legs(s[3]==null?null:D.R[s[3]],"#f2b134",10,false);legs(s[2]==null?null:D.A[s[2]],"#27e0c4",0,true);
  // play-head
  svg.appendChild(el("line",{x1:X(iEnd),y1:mT,x2:X(iEnd),y2:H-mB+2*bandH+22,stroke:"#ff5d57","stroke-width":1.4,"stroke-dasharray":"4 3"}));
  svg.appendChild(el("circle",{cx:X(iEnd),cy:Y(s[1]),r:4.5,fill:"#ff5d57",stroke:"#0a0d0f","stroke-width":1.5}));
  // readouts
  document.getElementById("asof").textContent=fmt(D.line[iEnd][0])+"  $"+s[1].toFixed(2);
  document.getElementById("asofsub").textContent="bar "+(iEnd+1)+" of "+D.line.length+" · engine window = last "+Math.min(D.window,iEnd+1)+" bars";
  document.getElementById("posl").textContent=fmt(D.line[iEnd][0]);
  const card=(id,seg,isA)=>{const u=document.getElementById(id);if(!seg){u.innerHTML="<li>no valid count on the window</li>";return}
    const d=seg.d||{};const det=isA?`${d.degree_label||""} · confidence <span class='k'>${Math.round((d.confidence||0)*100)}%</span> · covers ${Math.round((d.coverage||0)*100)}% of window`
      :`scale ${d.degree} · <span class='${d.hard_fails?"r":"g"}'>${d.hard_fails} hard-fails</span> · ${d.warns} warns · fib quality ${Math.round((d.fib_score||0)*100)}%`;
    const k0=D.snaps.findIndex(x=>(isA?x[2]:x[3])===(isA?s[2]:s[3]));const sofar=cur-k0+1;const total=seg.n;
    u.innerHTML=`<li>Pattern <span class='k'>${seg.p}</span> — ${det}</li><li>Held since <span class='k'>${fmt(seg.s)}</span> · <span class='k'>${sofar}</span> bar${sofar===1?"":"s"} so far${cur===D.snaps.length-1||sofar<total?"":""} · arrived by <span class='tag' style='color:${col(seg.p)}'>${seg.tr}</span></li>`+
      seg.legs.map(([lab,t0,p0,t1,p1])=>`<li>wave <b>${lab}</b>: ${fmt(t0)} $${p0.toFixed(2)} → ${fmt(t1)} $${p1.toFixed(2)}</li>`).join("")};
  card("acard",s[2]==null?null:D.A[s[2]],true);card("rcard",s[3]==null?null:D.R[s[3]],false);
  document.querySelectorAll("tr.seg").forEach(tr=>tr.classList.toggle("cur",+tr.dataset.k===(kind==="A"?s[2]:s[3])));
  const c=document.querySelector("tr.cur");if(c&&!timer)c.scrollIntoView({block:"nearest"});
}
function table(){const segs=kind==="A"?D.A:D.R;const tb=document.getElementById("segs");tb.innerHTML="";
  segs.forEach((g,k)=>{const d=g.d||{};const det=kind==="A"?`${d.degree_label||""} · conf ${Math.round((d.confidence||0)*100)}% · covers ${Math.round((d.coverage||0)*100)}%`:`deg ${d.degree??""} · ${d.hard_fails??""} HF · ${d.warns??""} W · fib ${Math.round((d.fib_score||0)*100)}%`;
    const legs=g.legs.map(l=>`${l[0]}@${l[4].toFixed(2)}`).join(" → ");
    const tr=document.createElement("tr");tr.className="seg";tr.dataset.k=k;tr.innerHTML=`<td class='n'>${k+1}</td><td>${fmt(g.s)}</td><td>${fmt(g.e)}</td><td class='n'>${g.n}</td><td><span class='tag' style='color:${col(g.p)}'>${g.tr}</span></td><td><span style='color:${col(g.p)};font-weight:700'>${g.p}</span> ${legs}</td><td class='dim'>${g.p==="NONE"?"":det}</td>`;
    tr.onclick=()=>{const j=D.snaps.findIndex(s=>(kind==="A"?s[2]:s[3])===k);if(j>=0){cur=j;pos.value=j;draw()}};tb.appendChild(tr)});draw()}
pos.oninput=()=>{cur=+pos.value;draw()};
document.getElementById("step").onclick=()=>{cur=Math.min(D.snaps.length-1,cur+1);pos.value=cur;draw()};
const play=document.getElementById("play");
play.onclick=()=>{if(timer){clearInterval(timer);timer=null;play.textContent="▶ play";return}
  if(cur>=D.snaps.length-1)cur=0;play.textContent="❚❚ pause";
  timer=setInterval(()=>{cur=Math.min(D.snaps.length-1,cur+(+document.getElementById("spd").value));pos.value=cur;draw();if(cur>=D.snaps.length-1){clearInterval(timer);timer=null;play.textContent="▶ play"}},80)};
follow.onchange=draw;
document.getElementById("tabA").onclick=()=>{kind="A";document.getElementById("tabA").classList.add("on");document.getElementById("tabR").classList.remove("on");table()};
document.getElementById("tabR").onclick=()=>{kind="R";document.getElementById("tabR").classList.add("on");document.getElementById("tabA").classList.remove("on");table()};
table();
</script></body></html>"""


def render_count_history_page(h: CountHistory, output_path=None, desc: str = "") -> str:
    data = {
        "window": h.window,
        "line": [[b[0], b[4]] for b in h.bars],
        "snaps": [[s.i, s.close, s.anchored, s.recent] for s in h.snapshots],
        "A": [_seg_json(s) for s in h.anchored],
        "R": [_seg_json(s) for s in h.recent],
    }
    html = (_PAGE.replace("__SYM__", h.symbol)
            .replace("__SUBTITLE__", desc or f"{h.symbol} · daily · causal replay")
            .replace("__NA__", str(len(h.anchored))).replace("__NR__", str(len(h.recent)))
            .replace("__NSTEPS__", str(len(h.snapshots))).replace("__NBARS__", str(len(h.bars)))
            .replace("__WINDOW__", str(h.window)).replace("__STRIDE__", str(h.stride))
            .replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(html)
    return html
