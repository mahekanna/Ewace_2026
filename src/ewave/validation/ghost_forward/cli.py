"""Handler for `ewave ghost-forward` — snapshot-freeze replay of a profile."""
from __future__ import annotations

import sys
from pathlib import Path

from ... import config
from ...data.store import Store
from ...rules.profiles import get_profile
from . import report, stability
from .forecasters import wave3_forecaster


def cmd_ghost_forward(args) -> int:
    try:
        profile = get_profile(args.profile)
    except config.ConfigError as e:
        print(e, file=sys.stderr)
        return 2
    store = Store()
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    rc = 0
    for sym in symbols:
        try:
            series = store.read(sym, args.tf)
        except FileNotFoundError as e:
            print(f"{sym}: {e}", file=sys.stderr)
            rc = 1
            continue
        bars = series.tuples()
        if len(bars) <= args.roll + args.horizon:
            print(f"{sym}: not enough bars ({len(bars)}) for roll+horizon",
                  file=sys.stderr)
            rc = 1
            continue
        out_dir = Path("outputs/ghost_forward") / f"{sym.lower()}_{args.tf}_{args.profile}"
        fc = wave3_forecaster(profile)
        import dataclasses
        import hashlib
        cfg_hash = hashlib.sha1(str(sorted(
            dataclasses.asdict(profile).items())).encode()).hexdigest()[:12]
        snaps = stability.snapshot_pass(bars, fc, args.roll, args.forward,
                                        args.horizon, out_dir / "snapshots.jsonl",
                                        profile=profile.name, config_hash=cfg_hash)
        outcomes = stability.outcome_pass(bars, snaps, args.roll, args.forward,
                                          args.horizon, frozen=True,
                                          out_path=out_dir / "outcomes.jsonl")
        m = stability.metrics(snaps, outcomes)
        import json
        with open(out_dir / "metrics.json", "w") as f:
            json.dump(m, f, indent=1)
        report.render(sym, args.tf, snaps, outcomes, m, args.roll, args.horizon,
                      out_dir / "summary.md")
        if getattr(args, "csv", False):
            import csv as _csv
            import dataclasses as _dc
            with open(out_dir / "snapshots.csv", "w", newline="") as f:
                rows = [_dc.asdict(x) for x in snaps]
                w = _csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            with open(out_dir / "outcomes.csv", "w", newline="") as f:
                w = _csv.DictWriter(f, fieldnames=list(outcomes[0].keys()))
                w.writeheader()
                w.writerows(outcomes)
        hit = m["outcomes"].get("HIT", 0)
        inv = m["outcomes"].get("INVALIDATED", 0)
        print(f"{sym} {args.tf} [{args.profile}]: {m['forecasts']} signals over "
              f"{m['steps']} steps -> HIT {hit} / INVALIDATED {inv} / "
              f"OPEN {m['outcomes'].get('OPEN', 0)}; "
              f"hit-rate {m['target_hit_rate']}; MFE/MAE(R) "
              f"{m['avg_mfe_r']}/{m['avg_mae_r']} -> {out_dir}/")
    return rc
