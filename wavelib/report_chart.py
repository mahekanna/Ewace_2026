"""
report_chart.py
===============
Rich, annotated HTML analysis pages — auto-generated from the wavelib engine, in
the visual spirit of the project's original hand-built charts (dark theme, price
line, labelled wave pivots, Fibonacci target lines, shaded zone, findings cards).

`analyze_symbol()` runs the engine to produce the chart data; `render_analysis_page()`
turns that data into a self-contained HTML file (inline SVG drawing, no deps).
"""
from __future__ import annotations
import datetime
import json

from .toolkit import zigzag_causal, pivots_to_waves, fib_retrace
from .rules import is_terminal
from .confluence import score_reversal
from .automation import label_and_validate


def _fmt(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")


def analyze_symbol(symbol, bars, zone, bullish=True, desc=""):
    """Run the engine on `bars` (t,o,h,l,c,v) and return a chart-data dict."""
    closes = [b[4] for b in bars]
    line = [[b[0], b[4]] for b in bars]
    last_close = closes[-1]

    # macro swing pivots for labelling
    piv = [p for p in zigzag_causal(bars, pct=0.10)]
    # top = highest pivot; launch low = lowest pivot before the top
    top_i = max(range(len(piv)), key=lambda i: piv[i].price)
    top = piv[top_i]
    pre = piv[:top_i] or piv
    launch = min(pre, key=lambda p: p.price)

    # label the last up-to-7 pivots as the visible swing sequence
    labels = ["①", "②", "③", "④", "⑤", "Ⓐ", "Ⓑ", "Ⓒ"]
    tail = piv[-7:]
    pivots = []
    for i, p in enumerate(tail):
        lab = labels[i] if i < len(labels) else ""
        kind = "T" if p is top else p.kind
        pivots.append([p.t, round(p.price, 2), lab, kind])
    pivots.append([bars[-1][0], round(last_close, 2), "now", "N"])

    # Fibonacci retracement targets of the last major up-leg (launch -> top)
    fibs = fib_retrace(top.price, launch.price)
    targets = [[round(v, 2), f"{r:.3f}  ${v:,.0f}", 0.85] for r, v in sorted(fibs.items())]

    # engine read
    cands = label_and_validate(bars, degrees=(0.05, 0.10, 0.15), max_candidates=1)
    best = cands[0] if cands else None
    term = is_terminal(pivots_to_waves(piv[-6:])) if len(piv) >= 6 else None
    rep = score_reversal(symbol, bars, zone, bullish=bullish)

    tier = ("HIGH-CONFIDENCE reversal" if rep.score >= 4
            else "BUILDING — not yet confirmed" if rep.score >= 2
            else "structurally allowed only")

    card_engine = ("What the engine detects", [
        f"Swing top <span class='r'>${top.price:,.2f}</span> on {top.date}; "
        f"launch low <span class='k'>${launch.price:,.2f}</span> ({launch.date}).",
        (f"Best auto-count: <span class='k'>{best.count_type}</span> "
         f"(quality {best.fib_score:.0%}, {best.hard_fails} rule-breaks)." if best
         else "No clean count at the tested scales."),
        (f"Terminal/diagonal check on the last 5 legs: "
         f"<span class='k'>{term.detail}</span>" if term and term.status.value != 'N/A'
         else "Last 5 legs are a directional move (no terminal overlap)."),
        f"Price <span class='k'>${last_close:,.2f}</span> vs reversal zone "
        f"<span class='g'>${zone[0]}-{zone[1]}</span>.",
    ])
    card_conf = ("Reversal confluence (live)",
                 [f"{'<span class=g>&#10003;</span>' if s.confirm else '<span class=dim>&#9675;</span>'} "
                  f"<b>{s.name}</b>: {s.detail}" for s in rep.strands]
                 + [f"<b>Score {rep.score}/7</b> &rarr; <span class='k'>{tier}</span>."])

    return {
        "symbol": symbol,
        "desc": desc or symbol,
        "subtitle": f"{desc or symbol} · daily · auto-generated",
        "headline": f"Elliott / NeoWave — best count: {best.count_type if best else 'n/a'}",
        "price": last_close,
        "change": f"in ${zone[0]}-{zone[1]} reversal zone · score {rep.score}/7",
        "asof": _fmt(bars[-1][0]),
        "line": line,
        "pivots": pivots,
        "targets": targets,
        "zone": list(zone),
        "cards": [card_engine, card_conf],
    }


_PAGE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>__SYM__ · wavelib</title>
<style>
:root{--bg:#0a0d0f;--panel:#11161a;--grid:#1c252b;--ink:#e8eef0;--dim:#7c8a91;
--teal:#27e0c4;--amber:#f2b134;--red:#ff5d57;--green:#48d97a;--line:#3aa6ff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:system-ui,Segoe UI,Roboto,sans-serif;padding:22px;min-height:100vh}
.wrap{max-width:1080px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;border-bottom:1px solid var(--grid);padding-bottom:14px}
h1{font-size:26px;letter-spacing:-.3px;line-height:1.1}
h1 small{font-weight:500;font-size:11px;color:var(--teal);display:block;letter-spacing:2px;margin-bottom:6px;text-transform:uppercase}
.px{text-align:right}.px .now{font-size:24px;font-weight:700;color:var(--red)}.px .chg{font-size:12px;color:var(--amber)}.px .ath{font-size:11px;color:var(--dim);margin-top:3px}
.chartbox{background:var(--panel);border:1px solid var(--grid);border-radius:10px;margin-top:16px;padding:8px 6px 2px;overflow:hidden}
svg{width:100%;height:auto;display:block}
.legend{display:flex;flex-wrap:wrap;gap:18px;margin-top:14px;font-size:11.5px;color:var(--dim)}
.legend span{display:inline-flex;align-items:center;gap:7px}.swatch{width:16px;height:3px;border-radius:2px;display:inline-block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px}@media(max-width:720px){.grid2{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--grid);border-radius:10px;padding:16px 18px}
.card h2{font-size:14px;color:var(--teal);margin-bottom:10px}
.card li{font-size:12.5px;line-height:1.7;color:#cdd6da;list-style:none;padding-left:16px;position:relative;margin-bottom:6px}
.card li::before{content:"\25B8";position:absolute;left:0;color:var(--amber)}
.k{color:var(--amber);font-weight:700}.r{color:var(--red);font-weight:700}.g{color:var(--green);font-weight:700}.dim{color:var(--dim)}
.foot{margin-top:16px;font-size:10.5px;color:var(--dim);line-height:1.6;border-top:1px solid var(--grid);padding-top:12px}
</style></head><body><div class="wrap">
<header><div><h1><small>__SUBTITLE__</small>__HEADLINE__</h1></div>
<div class="px"><div class="now">$__PRICE__</div><div class="chg">__CHANGE__</div><div class="ath">as of __ASOF__ · not investment advice</div></div></header>
<div class="chartbox"><svg id="c" viewBox="0 0 1040 520" preserveAspectRatio="xMidYMid meet"></svg></div>
<div class="legend">
<span><i class="swatch" style="background:var(--line)"></i>daily close</span>
<span><i class="swatch" style="background:var(--teal)"></i>wave pivot</span>
<span><i class="swatch" style="background:var(--green)"></i>Fibonacci target</span>
<span><i class="swatch" style="background:#3a4f3f"></i>reversal zone</span>
<span><i class="swatch" style="background:var(--red)"></i>last price</span></div>
<div class="grid2">__CARDS__</div>
<div class="foot">Auto-generated by wavelib: causal ZigZag pivots &rarr; Elliott/NeoWave rule checks &rarr; Fibonacci levels &rarr; reversal-confluence score. Elliott Wave is interpretive; this is the engine's highest-scoring read on the tested scales, not a certainty. Analysis tooling only.</div>
</div>
<script>
const D=__DATA__;
const NS="http://www.w3.org/2000/svg",svg=document.getElementById("c");
const W=1040,H=520,mL=10,mR=92,mT=22,mB=34;
function el(n,a){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e}
function tx(x,y,s,a){const t=el("text",{x,y,...a});t.textContent=s;svg.appendChild(t);return t}
const xs=D.line.map(d=>d[0]),t0=Math.min(...xs),t1=Math.max(...xs);
let ps=D.line.map(d=>d[1]).concat(D.pivots.map(p=>p[1])).concat(D.targets.map(t=>t[0])).concat(D.zone);
let pMin=Math.min(...ps),pMax=Math.max(...ps);const pad=(pMax-pMin)*0.06||1;pMin-=pad;pMax+=pad;
const X=t=>mL+(t-t0)/((t1-t0)||1)*(W-mL-mR),Y=p=>mT+(pMax-p)/((pMax-pMin)||1)*(H-mT-mB);
// gridlines + price axis (6 steps)
for(let i=0;i<=6;i++){const p=pMin+(pMax-pMin)*i/6;svg.appendChild(el("line",{x1:mL,y1:Y(p),x2:W-mR,y2:Y(p),stroke:"#1c252b","stroke-width":1}));tx(W-mR+8,Y(p)+4,"$"+p.toFixed(0),{fill:"#7c8a91","font-size":11});}
// date ticks
for(let i=0;i<=4;i++){const t=t0+(t1-t0)*i/4;const d=new Date(t*1000).toISOString().slice(0,7);tx(X(t),H-12,d,{fill:"#7c8a91","font-size":11,"text-anchor":"middle"});}
// reversal zone band
const zl=Y(Math.max(...D.zone)),zh=Y(Math.min(...D.zone));
svg.appendChild(el("rect",{x:mL,y:zl,width:W-mL-mR,height:Math.abs(zh-zl),fill:"#48d97a18",stroke:"none"}));
tx(mL+6,zl+14,"reversal zone $"+D.zone[0]+"-"+D.zone[1],{fill:"#48d97a","font-size":10.5});
// Fibonacci targets
D.targets.forEach(([p,lab,op])=>{if(p<pMin||p>pMax)return;svg.appendChild(el("line",{x1:mL,y1:Y(p),x2:W-mR,y2:Y(p),stroke:"#48d97a","stroke-width":1,"stroke-dasharray":"2 5",opacity:op}));tx(mL+6,Y(p)-5,lab,{fill:"#48d97a","font-size":10})});
// price area + line
let dp=D.line.map((d,i)=>(i?"L":"M")+X(d[0]).toFixed(1)+" "+Y(d[1]).toFixed(1)).join(" ");
svg.appendChild(el("path",{d:dp+` L ${X(t1).toFixed(1)} ${H-mB} L ${X(t0).toFixed(1)} ${H-mB} Z`,fill:"#3aa6ff14"}));
svg.appendChild(el("path",{d:dp,fill:"none",stroke:"#3aa6ff","stroke-width":2,"stroke-linejoin":"round"}));
// pivots + labels
D.pivots.forEach(([t,p,lab,kind])=>{const x=X(t),y=Y(p);const col=(kind==="T"||kind==="N")?"#ff5d57":"#27e0c4";svg.appendChild(el("circle",{cx:x,cy:y,r:kind==="T"?5.5:4,fill:col,stroke:"#0a0d0f","stroke-width":1.5}));const up=(kind==="H"||kind==="T");tx(x,up?y-12:y+18,lab,{fill:col,"font-size":13,"font-weight":700,"text-anchor":"middle"});tx(x,up?y-26:y+31,"$"+p.toFixed(0),{fill:"#9fb0b6","font-size":9.5,"text-anchor":"middle"})});
</script></body></html>"""


def render_analysis_page(data, output_path=None):
    cards = "".join(
        "<div class='card'><h2>" + title + "</h2><ul>"
        + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></div>"
        for title, bullets in data["cards"])
    html = (_PAGE
            .replace("__SYM__", data["symbol"])
            .replace("__SUBTITLE__", data["subtitle"])
            .replace("__HEADLINE__", data["headline"])
            .replace("__PRICE__", f"{data['price']:,.2f}")
            .replace("__CHANGE__", data["change"])
            .replace("__ASOF__", data["asof"])
            .replace("__CARDS__", cards)
            .replace("__DATA__", json.dumps(
                {"line": data["line"], "pivots": data["pivots"],
                 "targets": data["targets"], "zone": data["zone"]})))
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(html)
    return html
