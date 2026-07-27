"""
reporting.markdown — scan/daily report writers (outputs/reports/).
==================================================================
Reporting renders; it never decides (docs/ARCHITECTURE.md). The daily report
aggregates whatever run artifacts exist under outputs/ — signals scanned,
risk decisions, paper P&L, ghost-forward and backtest summaries.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from ..signals.models import Signal


def scan_report(result: dict, out_dir: str = "outputs/reports") -> Path:
    sigs: List[Signal] = result["signals"]
    lines = [f"# Scan report — {result['timeframe']} / profile {result['profile']}",
             "",
             f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC; "
             f"{result['symbols_scanned']} symbols scanned._", ""]
    if sigs:
        lines += ["| symbol | dir | signal time (UTC) | entry | stop | T1 | R:R | strands | id |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for s in sigs:
            t = datetime.fromtimestamp(s.signal_time, timezone.utc)
            lines.append(f"| {s.symbol} | {s.direction} | {t:%Y-%m-%d %H:%M} "
                         f"| {s.entry_price} | {s.stop_price} | {s.target_1} "
                         f"| {s.reward_risk} | {s.confluence_strands} | {s.signal_id} |")
    else:
        lines.append("_No signals on the latest bars (the wave-3 entry fires "
                     "selectively — only on a confirmation-break candle)._")
    if result.get("errors"):
        lines += ["", "## Errors"] + [f"- {e}" for e in result["errors"]]
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)
    path = p / "latest_scan_report.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def _read_json(path: Path) -> Optional[dict]:
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def daily_report(date: Optional[str] = None, outputs_dir: str = "outputs") -> str:
    date = date or datetime.now(timezone.utc).date().isoformat()
    out = Path(outputs_dir)
    lines = [f"# ewave daily report — {date}", "",
             f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC._", ""]

    day_file = out / "signals" / f"{date}.jsonl"
    if day_file.exists():
        rows = [json.loads(x) for x in day_file.read_text().splitlines() if x.strip()]
        lines += [f"## Signals frozen today: {len(rows)}"]
        for r in rows[:20]:
            lines.append(f"- {r['symbol']} {r['direction']} {r['pattern_type']} "
                         f"entry {r['entry_price']} stop {r['stop_price']} "
                         f"[{r['source_profile']}] id {r['signal_id']}")
    else:
        lines += ["## Signals frozen today: 0"]

    lines += [""]
    paper = out / "paper_trading" / "daily_report.md"
    if paper.exists():
        lines += ["## Paper trading (latest replay)", ""]
        lines += [f"> {l}" for l in paper.read_text().splitlines()[3:12]]
    ghost_runs = sorted((out / "ghost_forward").glob("*/metrics.json"))
    if ghost_runs:
        lines += ["", "## Ghost-forward runs on disk"]
        for g in ghost_runs[:10]:
            m = _read_json(g) or {}
            lines.append(f"- {g.parent.name}: {m.get('forecasts')} signals, "
                         f"hit-rate {m.get('target_hit_rate')}, "
                         f"MFE/MAE(R) {m.get('avg_mfe_r')}/{m.get('avg_mae_r')}")
    bt_runs = sorted((out / "backtests").glob("*/metrics.json"))
    if bt_runs:
        lines += ["", "## Backtest runs on disk"]
        for b in bt_runs[:10]:
            m = _read_json(b) or {}
            lines.append(f"- {b.parent.name}: {m.get('trades')} trades, "
                         f"expectancy {m.get('expectancy_r')}R, "
                         f"PF {m.get('profit_factor')}, DSR {m.get('dsr')} "
                         f"(trial #{m.get('n_trials')})")
    lines += ["", "_Selection discipline: judge edges by DSR + MinTRL from "
              "registry/trials.jsonl, never raw expectancy "
              "(docs/FULL_AUTOMATION_ROADMAP.md)._"]
    return "\n".join(lines) + "\n"
