"""
charting.py
===========
Programmatic SVG chart emitter (docs/research/04 §4 Item 6) — replaces the
hand-built charts/*.html. Pure stdlib (xml.etree.ElementTree + datetime).

Coordinate transform: t -> x (linear), price -> y (inverted linear). Renders the
wave skeleton as polylines with pivot dots, optional projection target lines and
shaded zones, plus readable price (left) and date (bottom) labels.
"""
from __future__ import annotations
import datetime
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


def _date(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")


def _text(parent, x, y, s, size=12, anchor="start", color="#333", weight="normal"):
    el = ET.SubElement(parent, "text", x=f"{x:.1f}", y=f"{y:.1f}",
                       attrib={"font-size": str(size), "font-family": "sans-serif",
                               "fill": color, "text-anchor": anchor, "font-weight": weight})
    el.text = s
    return el


def render_chart(waves, projections=None, zones=(), title: str = "",
                 width: int = 960, height: int = 540, output_path=None) -> str:
    """
    Emit a standalone SVG string for a wave set with optional projection targets
    and shaded zones, plus price/date axis labels. Returns the SVG; if
    `output_path` is given, also writes it.

    waves       : list of Wave objects (each drawn as a <polyline> with end dots).
    projections : {label: [price, ...]} -> each target a horizontal <line> + label.
    zones       : list of (lo, hi) price bands -> each a <rect> + label.
    """
    projections = projections or {}
    padL, padR, padT, padB = 64, 24, 44, 40

    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                     width=str(width), height=str(height),
                     viewBox=f"0 0 {width} {height}")
    ET.SubElement(svg, "rect", x="0", y="0", width=str(width), height=str(height),
                  attrib={"fill": "#ffffff"})
    if title:
        _text(svg, padL, 26, title, size=16, weight="bold", color="#111")
    if not waves:
        return ET.tostring(svg, encoding="unicode")

    t0, t1, p0, p1 = _bounds(waves, zones, projections)
    # pad the price range a touch so the line isn't flush to the edges
    margin = (p1 - p0) * 0.05 or 1.0
    p0, p1 = p0 - margin, p1 + margin
    tspan = (t1 - t0) or 1.0
    pspan = (p1 - p0) or 1.0

    def x(t):
        return padL + (t - t0) / tspan * (width - padL - padR)

    def y(p):
        return padT + (p1 - p) / pspan * (height - padT - padB)

    # plot frame
    ET.SubElement(svg, "rect", x=str(padL), y=str(padT),
                  width=str(width - padL - padR), height=str(height - padT - padB),
                  attrib={"fill": "none", "stroke": "#ddd", "stroke-width": "1"})

    # shaded zones (behind) + label
    for lo, hi in zones:
        yt, yb = y(hi), y(lo)
        ET.SubElement(svg, "rect", x=str(padL), y=f"{min(yt, yb):.1f}",
                      width=str(width - padL - padR), height=f"{abs(yb - yt):.1f}",
                      attrib={"class": "zone", "fill": "#cfe8ff",
                              "fill-opacity": "0.45", "stroke": "none"})
        _text(svg, width - padR - 4, min(yt, yb) + 13, f"zone {lo:g}-{hi:g}",
              size=11, anchor="end", color="#2469a6")

    # projection target lines + labels
    for label, targets in projections.items():
        for tgt in targets:
            yy = y(tgt)
            ET.SubElement(svg, "line", x1=str(padL), y1=f"{yy:.1f}",
                          x2=str(width - padR), y2=f"{yy:.1f}",
                          attrib={"stroke": "#e08020", "stroke-dasharray": "5 3",
                                  "stroke-width": "1"})
            _text(svg, padL + 4, yy - 3, f"{label} {tgt:g}", size=10, color="#b5651d")

    # price labels on the left axis (high / last / low)
    last_price = waves[-1].end.price
    for p in sorted({p1 - margin, p0 + margin, last_price}, reverse=True):
        _text(svg, padL - 6, y(p) + 4, f"{p:.2f}", size=11, anchor="end", color="#555")

    # date labels on the bottom axis
    _text(svg, padL, height - padB + 18, _date(t0), size=11, color="#555")
    _text(svg, width - padR, height - padB + 18, _date(t1), size=11, anchor="end", color="#555")

    # wave legs (one polyline each) + pivot dots
    for w in waves:
        pts = f"{x(w.start.t):.1f},{y(w.start.price):.1f} {x(w.end.t):.1f},{y(w.end.price):.1f}"
        ET.SubElement(svg, "polyline", points=pts,
                      attrib={"fill": "none", "stroke": "#1a1a1a", "stroke-width": "2"})
    seen = set()
    for w in waves:
        for piv in (w.start, w.end):
            key = (round(x(piv.t), 1), round(y(piv.price), 1))
            if key in seen:
                continue
            seen.add(key)
            ET.SubElement(svg, "circle", cx=f"{key[0]}", cy=f"{key[1]}", r="3",
                          attrib={"fill": "#c0392b"})
    # mark the last price
    _text(svg, x(waves[-1].end.t), y(last_price) - 8, f"{last_price:.2f}",
          size=11, anchor="middle", color="#c0392b", weight="bold")

    out = ET.tostring(svg, encoding="unicode")
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(out)
    return out
