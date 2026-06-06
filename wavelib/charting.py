"""
charting.py
===========
Programmatic SVG chart emitter (docs/research/04 §4 Item 6) — replaces the
hand-built charts/*.html. Pure stdlib (xml.etree.ElementTree).

Coordinate transform: t -> x (linear), price -> y (inverted linear).
"""
from __future__ import annotations
import xml.etree.ElementTree as ET


def _bounds(waves, zones, projections):
    ts, ps = [], []
    for w in waves:
        ts += [w.start.t, w.end.t]
        ps += [w.start.price, w.end.price]
    for lo, hi in zones:
        ps += [lo, hi]
    for targets in projections.values():
        ps += list(targets)
    return min(ts), max(ts), min(ps), max(ps)


def render_chart(waves, projections=None, zones=(), title: str = "",
                 width: int = 900, height: int = 500, output_path=None) -> str:
    """
    Emit a standalone SVG string for a wave set with optional projection targets
    and zones. Returns the SVG; if `output_path` is given, also writes it.

    waves       : list of Wave objects (each drawn as a <polyline>).
    projections : {label: [price, ...]} -> each target a horizontal <line>.
    zones       : list of (lo, hi) price bands -> each a <rect>.
    """
    projections = projections or {}
    pad = 40
    if not waves:
        svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                         width=str(width), height=str(height))
        return ET.tostring(svg, encoding="unicode")

    t0, t1, p0, p1 = _bounds(waves, zones, projections)
    tspan = (t1 - t0) or 1.0
    pspan = (p1 - p0) or 1.0

    def x(t):
        return pad + (t - t0) / tspan * (width - 2 * pad)

    def y(p):
        return pad + (p1 - p) / pspan * (height - 2 * pad)

    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                     width=str(width), height=str(height),
                     viewBox=f"0 0 {width} {height}")
    if title:
        t = ET.SubElement(svg, "text", x=str(pad), y="20",
                          attrib={"font-size": "16", "font-family": "sans-serif"})
        t.text = title

    # zones (drawn first, behind everything)
    for lo, hi in zones:
        yt, yb = y(hi), y(lo)
        ET.SubElement(svg, "rect", x=str(pad), y=str(min(yt, yb)),
                      width=str(width - 2 * pad), height=str(abs(yb - yt)),
                      attrib={"fill": "#cfe8ff", "fill-opacity": "0.4", "stroke": "none"})

    # projection target lines
    for label, targets in projections.items():
        for tgt in targets:
            yy = y(tgt)
            ET.SubElement(svg, "line", x1=str(pad), y1=str(yy),
                          x2=str(width - pad), y2=str(yy),
                          attrib={"stroke": "#e08020", "stroke-dasharray": "4 3",
                                  "stroke-width": "1"})

    # one polyline per wave
    for w in waves:
        pts = f"{x(w.start.t)},{y(w.start.price)} {x(w.end.t)},{y(w.end.price)}"
        ET.SubElement(svg, "polyline", points=pts,
                      attrib={"fill": "none", "stroke": "#1a1a1a", "stroke-width": "2"})

    out = ET.tostring(svg, encoding="unicode")
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(out)
    return out
