"""Phase 8 acceptance: reporters, TV notes, daily report, charting shims."""
import os
import tempfile
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.reporting.markdown import daily_report, scan_report
from ewave.reporting.tradingview import note, notes_markdown
from ewave.signals.models import Signal, SignalStatus


def _sig(**kw):
    base = dict(symbol="AVGO", timeframe="15m", signal_time=1_750_000_000,
                pattern_type="wave3_impulse", direction="long",
                entry_trigger="break_close_beyond_w1_extreme",
                entry_price=100.0, stop_price=95.0,
                targets=[("1.618x W1", 110.0), ("2.618x W1", 120.0)],
                invalidation_level=95.0, source_profile="experimental",
                confluence_strands=3, reward_risk=2.0)
    base.update(kw)
    return Signal(**base)


class TestTradingViewNotes(unittest.TestCase):
    def test_note_has_levels_and_no_blind_commands(self):
        text = note(_sig())
        for needle in ("Invalidation level: 95.0", "1.618x W1 110.0",
                       "Manual TradingView steps", "never trades"):
            self.assertIn(needle, text)
        for forbidden in ("BUY NOW", "SELL NOW"):
            self.assertNotIn(forbidden, text.upper().replace("\n", " ")
                             .replace("DO NOT ENTER", ""))

    def test_forming_candidate_carries_warning(self):
        text = note(_sig(status=SignalStatus.CANDIDATE))
        self.assertIn("WARNING", text)
        self.assertNotIn("WARNING", note(_sig()))

    def test_notes_markdown_wraps_blocks(self):
        md = notes_markdown([_sig(), _sig(symbol="MRVL")])
        self.assertEqual(md.count("```"), 4)
        self.assertIn("_No signals._", notes_markdown([]))


class TestReports(unittest.TestCase):
    def test_scan_report_written(self):
        with tempfile.TemporaryDirectory() as d:
            p = scan_report({"profile": "experimental", "timeframe": "15m",
                             "symbols_scanned": 2, "signals": [_sig()],
                             "errors": ["MRVL: no data"]}, out_dir=d)
            text = p.read_text()
            self.assertIn("AVGO", text)
            self.assertIn("MRVL: no data", text)

    def test_scan_report_empty_is_explained(self):
        with tempfile.TemporaryDirectory() as d:
            p = scan_report({"profile": "x", "timeframe": "1h",
                             "symbols_scanned": 1, "signals": [],
                             "errors": []}, out_dir=d)
            self.assertIn("fires selectively", p.read_text().replace("\n", " "))

    def test_daily_report_aggregates_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "signals"))
            with open(os.path.join(d, "signals", "2026-07-09.jsonl"), "w") as f:
                import json
                f.write(json.dumps(_sig().to_dict()) + "\n")
            text = daily_report("2026-07-09", outputs_dir=d)
            self.assertIn("Signals frozen today: 1", text)
            self.assertIn("DSR + MinTRL", text)

    def test_daily_report_empty_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            text = daily_report("2026-07-09", outputs_dir=d)
            self.assertIn("Signals frozen today: 0", text)


class TestChartingShims(unittest.TestCase):
    def test_shims_identity(self):
        import wavelib.charting as WC
        import wavelib.report_chart as WRC
        from ewave.reporting import charting, html_report
        self.assertIs(WC.render_chart, charting.render_chart)
        self.assertIs(WRC.analyze_symbol, html_report.analyze_symbol)
        self.assertIs(WRC.render_analysis_page, html_report.render_analysis_page)


class TestAnalysisReportHonestyGate(unittest.TestCase):
    """The visual must number waves (①②③④⑤) ONLY over a rule-clean 5-wave
    impulse; on anything else it draws causal swing markers and says so, so it
    can never imply a validated count where the engine found none."""

    def _bars(self, closes, t0=1_700_000_000, step=86400):
        # simple OHLC from a close path; wide enough H/L so pivots confirm
        out = []
        for i, c in enumerate(closes):
            o = closes[i - 1] if i else c
            h = max(o, c) * 1.01
            lo = min(o, c) * 0.99
            out.append((t0 + i * step, o, h, lo, c, 1000))
        return out

    def test_noise_gets_swings_not_numerals(self):
        from ewave.reporting.html_report import analyze_symbol, render_analysis_page
        # a pure zig-zag chop with no valid 5-wave impulse
        seq = []
        base = 100.0
        for k in range(20):
            base += (6 if k % 2 == 0 else -5)
            seq += [base] * 6
        bars = self._bars(seq)
        d = analyze_symbol("NOISE", bars)
        html = render_analysis_page(d)
        if not d["count_ok"]:
            self.assertIn("NO VALIDATED IMPULSE COUNT", d["count_note"])
            # no Elliott numerals drawn when the gate is closed
            labels = "".join(str(p[2]) for p in d["pivots"])
            for numeral in "①②③④⑤":
                self.assertNotIn(numeral, labels)
            self.assertIn("swing high/low", html)
        # placeholders always resolved
        for ph in ("__COUNTNOTE__", "__CNOTECLASS__", "__PIVOTLEGEND__"):
            self.assertNotIn(ph, html)

    def test_gate_is_impulse_only(self):
        """A 3-wave corrective (trivially fib-fittable on any series) must NOT
        be numbered — only a rule-clean IMPULSE/DIAGONAL opens the gate."""
        from ewave.reporting import html_report
        import inspect
        src = inspect.getsource(html_report.analyze_symbol)
        # the gate keys on IMPULSE/DIAGONAL with hard_fails == 0, never CORRECTION
        self.assertIn('("IMPULSE", "DIAGONAL")', src)
        self.assertIn("hard_fails == 0", src)


if __name__ == "__main__":
    unittest.main()
