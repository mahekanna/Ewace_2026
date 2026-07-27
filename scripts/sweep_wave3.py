"""
sweep_wave3.py — the wave-3 operating-point sweep (research track).
===================================================================
Question (docs/FULL_AUTOMATION_ROADMAP.md): is there a rule-faithful operating
point between the proven crude skeleton and the too-tight strict profile with
>=30 trades/yr/symbol AND a DSR-supported edge?

Method: grid of Profile objects anchored at sow_neowave_soft, backtested with
ewave.backtest.engine.backtest_wave3 (causal, one position at a time, costs
from configs/execution.json) over every symbol given. Per config: pooled R
series across symbols -> expectancy, PF, win rate, trades/yr/symbol, Sharpe,
PSR, MinTRL, and DSR against the FULL trials registry. Each config logs
exactly ONE pooled trial (per-symbol runs are components, not variants).

Selection rule (pre-committed, stated before results are read): among configs
with >=30 pooled trades/yr/symbol, rank by DSR; tie-break MinTRL vs sample.

  python3 scripts/sweep_wave3.py                 # full grid + baseline
  python3 scripts/sweep_wave3.py --symbols avgo,mrvl --quick
"""
import argparse
import csv
import itertools
import json
import os
import statistics
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))

from ewave.backtest.engine import backtest_wave3                   # noqa: E402
from ewave.backtest.fills import FillModel                         # noqa: E402
from ewave.backtest.metrics import summarize                       # noqa: E402
from ewave.data.store import Store                                 # noqa: E402
from ewave.rules.profiles import Profile, get_profile              # noqa: E402

SEMIS = ["avgo", "mrvl", "nvda", "amd", "tsm", "qcom", "asml", "lrcx",
         "mu", "arm", "smci", "amat"]
BARS_PER_YEAR = 26 * 252          # RTH 15m bars in a trading year


def grid():
    """The pre-committed 36-config grid (3 strands x 3 rr x 2 pattern x 2 band)."""
    out = []
    for strands, rr, pid, band in itertools.product(
            (1, 2, 3), (1.0, 1.5, 2.0), (True, False),
            (("golden", 0.618, 0.764), ("wide", 0.786, None))):
        name = (f"sw_s{strands}_rr{rr:g}_{'pid' if pid else 'nopid'}_{band[0]}")
        out.append(Profile(
            name=name, zigzag_pct=0.02, retr_lo=0.382,
            retr_hi=band[1], deep_hi=band[2],
            min_w1_frac=0.01, stop_buf=0.001, use_momentum=True,
            require_pattern_id=pid, min_confluence_strands=strands,
            min_rr=rr, entry_window_w2_mult=2, sb_time_budget_w1_mult=3,
            time_stop_bars=0, scale_out=True))
    return out


def run_config(profile, symbol_bars, fills, registry, label=None):
    per_symbol = {}
    pooled = []
    years_total = 0.0
    for sym, bars in symbol_bars.items():
        trades = backtest_wave3(bars, profile, fill_model=fills)
        rs = [t.r for t in trades]
        years = len(bars) / BARS_PER_YEAR
        years_total += years
        per_symbol[sym] = {"trades": len(rs),
                           "exp": round(statistics.mean(rs), 3) if rs else None}
        pooled += rs

    class _T:  # minimal trade shim for summarize (needs .r/.planned_rr/.bars_held)
        def __init__(self, r):
            self.r, self.planned_rr, self.bars_held = r, 0.0, 0
    m = summarize([_T(r) for r in pooled], symbol="POOLED",
                  timeframe="15m", profile=label or profile.name,
                  registry_path=registry, log=True)
    from ewave.validation.stats import skew_kurt
    m["_skew_kurt"] = skew_kurt(pooled) if len(pooled) >= 3 else (0.0, 3.0)
    # pooled trades / total symbol-years = trades per symbol-year
    m["trades_per_yr_per_symbol"] = round(len(pooled) / years_total, 1) \
        if years_total else 0.0
    m["per_symbol"] = per_symbol
    m["config"] = {"strands": profile.min_confluence_strands,
                   "min_rr": profile.min_rr,
                   "pattern_id": profile.require_pattern_id,
                   "retr_hi": profile.retr_hi, "deep_hi": profile.deep_hi,
                   "scale_out": profile.scale_out}
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SEMIS))
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry", "trials.jsonl"))
    ap.add_argument("--out", default=os.path.join(_ROOT, "outputs", "backtests"))
    ap.add_argument("--quick", action="store_true", help="first 6 configs only")
    a = ap.parse_args()

    store = Store()
    fills = FillModel.from_config()
    symbol_bars = {}
    for sym in [s.strip().lower() for s in a.symbols.split(",")]:
        try:
            symbol_bars[sym] = store.read(sym, "15m").tuples()
        except FileNotFoundError:
            print(f"skip {sym}: no 15m data")
    print(f"symbols: {', '.join(symbol_bars)} "
          f"({sum(len(b) for b in symbol_bars.values())} bars total); "
          f"costs: {fills.slippage_bps}bps + {fills.commission_per_share}/sh")

    # baseline: the proven crude skeleton, pooled (single-target, no gates)
    baseline = run_config(get_profile("experimental"), symbol_bars, fills,
                          a.registry, label="baseline_experimental_pooled")
    print(f"\nBASELINE experimental (pooled): {baseline['trades']} trades, "
          f"{baseline['expectancy_r']}R, PF {baseline['profit_factor']}, "
          f"~{baseline['trades_per_yr_per_symbol']} trades/yr/sym, "
          f"DSR {baseline['dsr']}\n")

    rows = []
    configs = grid()[:6] if a.quick else grid()
    for i, prof in enumerate(configs, 1):
        m = run_config(prof, symbol_bars, fills, a.registry)
        rows.append(m)
        print(f"[{i:2d}/{len(configs)}] {m['profile']:28s} "
              f"n={m['trades']:4d} ({m['trades_per_yr_per_symbol']:5.1f}/yr/sym) "
              f"exp={m['expectancy_r'] if m['expectancy_r'] is not None else '  -  '} "
              f"PF={m['profit_factor']} DSR={m['dsr']}")

    # Family DSR: the selection family is THIS sweep (baseline + grid). The
    # registry-wide DSR (column `dsr`) mixes Sharpe scales from unrelated old
    # strategies — maximally conservative; `dsr_family` is the textbook
    # multiple-testing correction for picking the best of these N configs.
    from ewave.validation.stats import deflated_sharpe_ratio, skew_kurt
    family = [baseline] + rows
    fam_srs = [m["sharpe_per_trade"] for m in family
               if m.get("sharpe_per_trade") is not None]
    fam_var = (statistics.variance(fam_srs) if len(fam_srs) > 1 else 0.0)
    for m in family:
        m["dsr_family"] = None
        if m.get("sharpe_per_trade") is not None and m["trades"] >= 3 and fam_var > 0:
            sk, ku = m.get("_skew_kurt", (0.0, 3.0))
            m["dsr_family"] = round(deflated_sharpe_ratio(
                m["sharpe_per_trade"], m["trades"], sk, ku,
                len(fam_srs), fam_var), 4)

    os.makedirs(a.out, exist_ok=True)
    csv_path = os.path.join(a.out, "sweep_wave3.csv")
    cols = ["profile", "trades", "trades_per_yr_per_symbol", "expectancy_r",
            "win_rate", "profit_factor", "max_drawdown_r", "sharpe_per_trade",
            "psr", "min_trl", "dsr", "dsr_family", "n_trials"]
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + ["config"])
        w.writerow([baseline.get(c) for c in cols] + [json.dumps(baseline["config"])])
        for m in rows:
            w.writerow([m.get(c) for c in cols] + [json.dumps(m["config"])])
    with open(os.path.join(a.out, "sweep_wave3.json"), "w") as f:
        json.dump({"baseline": baseline, "grid": rows}, f, indent=1)
    print(f"\nwrote {csv_path} (+ .json). Selection rule: >=30 trades/yr/sym, "
          "rank by DSR, tie-break MinTRL.")


if __name__ == "__main__":
    main()
