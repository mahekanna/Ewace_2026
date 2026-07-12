"""Phase 0 acceptance: package imports, config loader, CLI skeleton."""
import io
import json
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

import ewave
from ewave import cli, config

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPackage(unittest.TestCase):
    def test_version(self):
        self.assertRegex(ewave.__version__, r"^\d+\.\d+\.\d+$")

    def test_subpackages_import(self):
        import importlib
        for name in ("data", "data.adapters", "features", "pivots", "monowaves",
                     "rules", "patterns", "signals", "validation",
                     "validation.ghost_forward", "backtest", "risk",
                     "execution", "scanner", "reporting"):
            importlib.import_module(f"ewave.{name}")


class TestConfig(unittest.TestCase):
    def test_all_shipped_configs_load(self):
        base = os.path.join(REPO, "configs")
        for name in ("app", "data", "watchlists", "profiles", "risk", "execution"):
            cfg = config.load(name, base_dir=base)
            self.assertIsInstance(cfg, dict, name)

    def test_missing_config_raises(self):
        with self.assertRaises(config.ConfigError):
            config.load("nonexistent", base_dir=os.path.join(REPO, "configs"))

    def test_profiles_strict_matches_ruleset(self):
        """The strict profile must encode RULESET §H exactly (mirrors
        wave3_signal_strict defaults) so Phase 3 can prove preset equivalence."""
        p = config.load("profiles", base_dir=os.path.join(REPO, "configs"))
        s = p["sow_neowave_strict"]
        self.assertEqual(s["min_confluence_strands"], 3)
        self.assertEqual(s["min_rr"], 2.0)
        self.assertEqual(s["retr_lo"], 0.382)
        self.assertEqual(s["retr_hi"], 0.618)
        self.assertEqual(s["deep_hi"], 0.764)
        self.assertTrue(s["require_pattern_id"])
        crude = p["experimental"]
        self.assertEqual(crude["retr_hi"], 0.786)
        self.assertEqual(crude["min_confluence_strands"], 0)
        self.assertEqual(crude["time_stop_bars"], 96)

    def test_risk_live_disabled_by_default(self):
        r = config.load("risk", base_dir=os.path.join(REPO, "configs"))
        self.assertFalse(r["live_enabled"])
        e = config.load("execution", base_dir=os.path.join(REPO, "configs"))
        self.assertEqual(e["mode"], "paper")
        self.assertFalse(e["live"]["enabled"])


class TestCli(unittest.TestCase):
    def test_parser_has_all_subcommands(self):
        parser = cli.build_parser()
        sub = next(a for a in parser._actions
                   if isinstance(a, cli.argparse._SubParsersAction))
        self.assertEqual(
            set(sub.choices),
            {"fetch-data", "validate-data", "resample", "pivots", "scan",
             "ghost-forward", "backtest", "paper-trade", "report", "journal"})

    def test_no_command_prints_help(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cli.main([])
        self.assertEqual(rc, 0)
        self.assertIn("ewave", out.getvalue())

    def test_unbuilt_commands_exit_2_with_phase_note(self):
        """Any dispatch entry whose module doesn't import yet must exit 2 and
        name its phase. Skips once every phase is built."""
        import importlib
        unbuilt = []
        for cmd, (mod, func, phase) in cli._DISPATCH.items():
            try:
                getattr(importlib.import_module(mod), func)
            except (ImportError, AttributeError):
                unbuilt.append((cmd, phase))
        if not unbuilt:
            self.skipTest("all commands built")
        for cmd, phase in unbuilt:
            err = io.StringIO()
            with redirect_stderr(err):
                rc = cli.main([cmd] + (["--symbols", "X"]
                                       if cmd in ("ghost-forward", "backtest") else []))
            self.assertEqual(rc, 2, cmd)
            self.assertIn(phase, err.getvalue())

    def test_dispatch_table_covers_all_subcommands(self):
        parser = cli.build_parser()
        sub = next(a for a in parser._actions
                   if isinstance(a, cli.argparse._SubParsersAction))
        self.assertEqual(set(sub.choices), set(cli._DISPATCH))


class TestContractDataStillValid(unittest.TestCase):
    def test_a_cached_file_parses(self):
        path = os.path.join(REPO, "data", "live", "avgo_1d_2026-06.json")
        with open(path) as f:
            d = json.load(f)
        self.assertIn("bars", d)
        ts = [b["t"] for b in d["bars"]]
        self.assertEqual(ts, sorted(ts))


if __name__ == "__main__":
    unittest.main()
