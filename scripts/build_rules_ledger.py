#!/usr/bin/env python3
"""
build_rules_ledger.py — assemble docs/RULES_LEDGER.md from agent extracts.
==========================================================================
Reads the per-pack extraction files produced by the ledger reader agents
(scratchpad/ledger/extract_*.md), parses their `### [CATEGORY] title` entries,
merges EXACT-duplicate rules (union of sources — nothing is dropped), groups by
category in a canonical order, assigns a stable per-category ID, and emits one
numbered ledger. Near-duplicates are KEPT (they usually carry different specific
numbers) — the goal is completeness, not brevity.

Usage:  python3 scripts/build_rules_ledger.py <extract_dir> <out.md>
"""
import os
import re
import sys
import glob

CAT_ORDER = [
    ("IMPULSE", "IMP", "Impulse (motive) waves"),
    ("TERMINAL", "TRM", "Terminal impulse / ending diagonal"),
    ("ZIGZAG", "ZZ", "Zigzag corrections"),
    ("FLAT", "FLT", "Flat corrections"),
    ("TRIANGLE", "TRI", "Triangles (contracting / expanding / neutral / extracting)"),
    ("DIAMETRIC", "DIA", "Diametric & symmetrical formations"),
    ("COMPLEX-X", "CX", "Complex corrections & X-waves"),
    ("CONFIRMATION-LINES", "CNF", "Confirmation lines & two-stage confirmation"),
    ("FIB", "FIB", "Fibonacci relationships"),
    ("TIME", "TIM", "Wave time rules"),
    ("TIME-CYCLES", "CYC", "Time cycles (Kaal Chakra / Hurst)"),
    ("ICHIMOKU", "ICH", "Ichimoku Cloud"),
    ("INDICATORS", "IND", "Other indicators"),
    ("SETUP-TRADE", "SET", "Trade setups & execution"),
    ("RISK", "RSK", "Risk & money management"),
    ("PROCESS-METHOD", "MTH", "Analysis method & order of operations"),
    ("DATA", "DAT", "Data contract & preparation"),
    ("VALIDATION", "VAL", "Validation, backtesting & selection"),
    ("AUTOMATION-SPEC", "AUT", "Automation / engineering specs"),
    ("SCOPE", "SCP", "Scope, exclusions & policy"),
]
CAT_INFO = {c: (pre, desc) for c, pre, desc in CAT_ORDER}

ENTRY_RE = re.compile(r"^###\s*\[([A-Z\-]+)\]\s*(.*)$")


def parse_file(path):
    """Yield dicts for each ### entry in an extract file."""
    with open(path) as f:
        text = f.read()
    # stop before the FILES READ footer
    text = re.split(r"^##\s*FILES READ", text, flags=re.M)[0]
    blocks = re.split(r"(?m)^(?=###\s*\[)", text)
    src_pack = os.path.basename(path).replace("extract_", "").replace(".md", "")
    for blk in blocks:
        m = ENTRY_RE.match(blk.strip().splitlines()[0]) if blk.strip() else None
        if not m:
            continue
        cat, title = m.group(1), m.group(2).strip()
        fields = {"CATEGORY": cat, "TITLE": title, "PACK": src_pack,
                  "RULE": "", "TYPE": "", "SOURCE": "", "NOTES": ""}
        for key in ("RULE", "TYPE", "SOURCE", "NOTES"):
            fm = re.search(rf"(?m)^-\s*{key}:\s*(.*)$", blk)
            if fm:
                fields[key] = fm.group(1).strip()
        if fields["RULE"]:
            yield fields


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def merge(entries):
    """Merge exact-normalized-duplicate RULE text; union the sources."""
    seen = {}
    order = []
    for e in entries:
        k = (e["CATEGORY"], norm(e["RULE"]))
        if k in seen:
            base = seen[k]
            for s in (e["SOURCE"], e["PACK"]):
                if s and s not in base["_sources"]:
                    base["_sources"].append(s)
            if len(e["NOTES"]) > len(base["NOTES"]):
                base["NOTES"] = e["NOTES"]
        else:
            e["_sources"] = [s for s in (e["SOURCE"], e["PACK"]) if s]
            seen[k] = e
            order.append(e)
    return order


def main():
    ext_dir = sys.argv[1] if len(sys.argv) > 1 else \
        "/tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/ledger"
    out = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "docs", "RULES_LEDGER.md")
    files = sorted(glob.glob(os.path.join(ext_dir, "extract_*.md")))
    all_entries = []
    for f in files:
        all_entries += list(parse_file(f))
    merged = merge(all_entries)

    by_cat = {}
    for e in merged:
        by_cat.setdefault(e["CATEGORY"], []).append(e)

    lines = []
    lines.append("# RULES LEDGER — every rule, setup & explanation from the shared docs\n")
    lines.append("_Single canonical registry so nothing from any shared document is lost._ "
                 "Assembled by `scripts/build_rules_ledger.py` from agent extractions of "
                 "the full bundle (SOW instructor materials, the md/TradingView-playbook "
                 "pack, the research-validation pack, the automation SPEC + agent-prompt "
                 "packs, and the legacy/audit packs) merged with the page-cited PDF notes "
                 "in `docs/research/sow_deep_read/`. Exact-duplicate rules are merged "
                 "(sources unioned); near-duplicates are kept because they usually carry "
                 "different specific numbers.\n")
    total = len(merged)
    known = sum(len(v) for v in by_cat.values())
    lines.append(f"**{total} distinct rule entries** across "
                 f"{len([c for c, _, _ in CAT_ORDER if c in by_cat])} categories. "
                 "Where a rule is enforced in code, the RULESET section / validator is "
                 "named in `docs/research/SOW_METHOD.md` (compliance matrix) and drawn in "
                 "`docs/atlas/SOW_PATTERN_ATLAS.html`.\n")

    # table of contents
    lines.append("## Contents\n")
    for cat, pre, desc in CAT_ORDER:
        if cat in by_cat:
            lines.append(f"- **{pre}** — {desc} ({len(by_cat[cat])})")
    lines.append("")

    # unknown categories (typo/new) appended at end so nothing is dropped
    extra_cats = [c for c in by_cat if c not in CAT_INFO]

    def emit_cat(cat, pre, desc):
        lines.append(f"\n## {pre} · {desc}\n")
        for i, e in enumerate(by_cat[cat], 1):
            rid = f"{pre}-{i:02d}"
            srcs = " · ".join(dict.fromkeys(e["_sources"]))
            lines.append(f"### {rid} — {e['TITLE']}")
            lines.append(f"- **Rule:** {e['RULE']}")
            meta = f"- **Type:** {e['TYPE'] or 'n/a'}"
            lines.append(meta)
            lines.append(f"- **Source:** {srcs}")
            if e["NOTES"]:
                lines.append(f"- **Notes:** {e['NOTES']}")
            lines.append("")

    for cat, pre, desc in CAT_ORDER:
        if cat in by_cat:
            emit_cat(cat, pre, desc)
    for cat in extra_cats:
        emit_cat(cat, cat[:3].upper(), cat.title())

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {out}: {total} entries, {len(by_cat)} categories, "
          f"from {len(files)} extract files ({len(all_entries)} raw)")


if __name__ == "__main__":
    main()
