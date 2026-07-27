"""Phase 9 — SOW/NeoWave doctrine gap-closure acceptance (bundle audit G1–G12).

Synthetic pass/fail coverage for every validator added in the gap-closure
round (RULESET §I): confirmation lines (0-B, B-D, diametric boundary),
triangle sub-rules + extracting triangle, diametric paired legs, zigzag/flat
time + C rules, flat B bands, X-wave bounds, terminal W3>W1, the causal
Ichimoku indicator + opt-in confluence strand, ghost-forward provenance/lag
metrics, and the Pivot/Bar model enrichments. All new gates are opt-in or
advisory (WARN/REF/NA) — nothing here touches the validated signal paths.
"""
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.rules.result import Pivot, Status, Wave

DAY = 86400.0


def _w(t0_days, p0, t1_days, p1) -> Wave:
    """Synthetic wave from (day, price) to (day, price)."""
    return Wave(Pivot(t0_days * DAY, p0, "L" if p1 > p0 else "H"),
                Pivot(t1_days * DAY, p1, "H" if p1 > p0 else "L"))


def _by_rule(results, needle):
    hits = [r for r in results if needle in r.rule]
    assert hits, f"no RuleResult matching {needle!r} in {[r.rule for r in results]}"
    return hits[0]


# --------------------------------------------------------------------------- #
# Confirmation lines (rules.neowave — RULESET §I.5)
# --------------------------------------------------------------------------- #
class TestZeroBConfirmation(unittest.TestCase):
    # down zigzag: A 100->80, B 80->90, C 90->70 (C takes 10 days)
    A = _w(0, 100, 10, 80)
    B = _w(10, 80, 15, 90)
    C = _w(15, 90, 25, 70)

    def test_confirmed_break_passes_both_stages(self):
        from ewave.rules.neowave import zero_b_confirmation
        # one day after C ends, price is above the 0-B line AND beyond B's extreme
        res = zero_b_confirmation(self.A, self.B, self.C, 26 * DAY, 95.0)
        self.assertEqual([r.status for r in res], [Status.PASS, Status.PASS])

    def test_no_break_warns(self):
        from ewave.rules.neowave import zero_b_confirmation
        res = zero_b_confirmation(self.A, self.B, self.C, 26 * DAY, 75.0)
        self.assertEqual([r.status for r in res], [Status.WARN, Status.WARN])

    def test_slow_break_warns(self):
        from ewave.rules.neowave import zero_b_confirmation
        # break happens but 20 days after C (> time of C = 10d) -> not confirmed
        res = zero_b_confirmation(self.A, self.B, self.C, 45 * DAY, 95.0)
        self.assertEqual(res[0].status, Status.WARN)


def _contracting_triangle():
    """5-leg contracting triangle after a decline; a-side below the B-D line."""
    return [_w(0, 100, 10, 80),    # a (len 20)
            _w(10, 80, 20, 92),    # b (12)
            _w(20, 92, 30, 84),    # c (8)
            _w(30, 84, 40, 90),    # d (6)
            _w(40, 90, 50, 86)]    # e (4)


class TestBDLine(unittest.TestCase):
    def test_clean_bd_line_passes(self):
        from ewave.rules.neowave import bd_line_test
        self.assertEqual(bd_line_test(_contracting_triangle()).status, Status.PASS)

    def test_premature_e_break_warns(self):
        from ewave.rules.neowave import bd_line_test
        legs = _contracting_triangle()
        legs[4] = _w(40, 90, 50, 95)   # E ends beyond the B-D line (~89 at day 50)
        self.assertEqual(bd_line_test(legs).status, Status.WARN)

    def test_wrong_arity_is_na(self):
        from ewave.rules.neowave import bd_line_test
        self.assertEqual(bd_line_test(_contracting_triangle()[:3]).status, Status.NA)

    def test_bd_confirmation_fast_break(self):
        from ewave.rules.neowave import bd_confirmation
        # day 51: price 92 is above the B-D line (~88.9) = away from the a-side,
        # 1 day after E (<= shortest leg 10d)
        res = bd_confirmation(_contracting_triangle(), 51 * DAY, 92.0)
        self.assertEqual(res[0].status, Status.PASS)

    def test_bd_confirmation_no_break_warns(self):
        from ewave.rules.neowave import bd_confirmation
        res = bd_confirmation(_contracting_triangle(), 51 * DAY, 85.0)
        self.assertEqual(res[0].status, Status.WARN)


def _diametric():
    """7-leg bowtie diametric (equal ~10-day legs, paired magnitudes)."""
    return [_w(0, 100, 10, 80),    # a (20)
            _w(10, 80, 20, 90),    # b (10)
            _w(20, 90, 30, 78),    # c (12)
            _w(30, 78, 40, 92),    # d (14)
            _w(40, 92, 50, 76),    # e (16)
            _w(50, 76, 60, 94),    # f (18)
            _w(60, 94, 70, 74)]    # g (20)


class TestDiametric(unittest.TestCase):
    def test_boundary_confirmation_fast_break(self):
        from ewave.rules.neowave import diametric_boundary_confirmation
        # D-F line rises 0.1/day (92@40d -> 94@60d); E sits below it. Day 71,
        # price 97 has crossed above (~95.1) = away from the E side, within G's time.
        res = diametric_boundary_confirmation(_diametric(), 71 * DAY, 97.0)
        self.assertEqual(res[0].status, Status.PASS)

    def test_boundary_no_break_warns(self):
        from ewave.rules.neowave import diametric_boundary_confirmation
        res = diametric_boundary_confirmation(_diametric(), 71 * DAY, 80.0)
        self.assertEqual(res[0].status, Status.WARN)

    def test_wrong_arity_is_na(self):
        from ewave.rules.neowave import diametric_boundary_confirmation
        res = diametric_boundary_confirmation(_diametric()[:5], 71 * DAY, 97.0)
        self.assertEqual(res[0].status, Status.NA)

    def test_paired_legs_pass_on_similar_pairs(self):
        from ewave.rules.corrections import diametric_pair_checks
        res = diametric_pair_checks(_diametric())
        self.assertEqual(len(res), 3)   # G~A, F~B, E~C
        self.assertTrue(all(r.status is Status.PASS for r in res))

    def test_paired_legs_warn_when_price_and_time_both_off(self):
        from ewave.rules.corrections import diametric_pair_checks
        legs = _diametric()
        legs[6] = _w(60, 94, 105, 24)   # g: 70 points over 45 days (5x A price, 4.5x A time)
        res = diametric_pair_checks(legs)
        self.assertEqual(_by_rule(res, "G~A").status, Status.WARN)


# --------------------------------------------------------------------------- #
# Triangle sub-rules (rules.triangles — RULESET §I.2)
# --------------------------------------------------------------------------- #
class TestTriangleSubrules(unittest.TestCase):
    def test_textbook_contracting_passes(self):
        from ewave.rules.triangles import triangle_subrules
        res = triangle_subrules(_contracting_triangle())
        self.assertTrue(all(r.status is Status.PASS for r in res))

    def test_large_e_warns(self):
        from ewave.rules.triangles import triangle_subrules
        legs = _contracting_triangle()
        legs[4] = _w(40, 90, 50, 60)   # E becomes the LARGEST leg
        res = triangle_subrules(legs)
        self.assertEqual(_by_rule(res, "E smallest").status, Status.WARN)

    def test_shallow_retraces_warn(self):
        from ewave.rules.triangles import triangle_subrules
        legs = [_w(0, 100, 10, 60),    # a (40)
                _w(10, 60, 20, 70),    # b (10) = 25% of a
                _w(20, 70, 30, 67),    # c (3)  = 30% of b
                _w(30, 67, 40, 68),    # d (1)  = 33% of c
                _w(40, 68, 50, 67.6)]  # e (0.4)= 40% of d
        res = triangle_subrules(legs)
        self.assertEqual(_by_rule(res, ">=3 legs").status, Status.WARN)

    def test_extracting_triangle_detected(self):
        from ewave.rules.triangles import is_extracting_triangle
        legs = [_w(0, 100, 10, 80),    # a (20)
                _w(10, 80, 20, 86),    # b (6)
                _w(20, 86, 30, 74),    # c (12)
                _w(30, 74, 40, 84),    # d (10) > b
                _w(40, 84, 50, 79)]    # e (5)  < c < a
        self.assertEqual(is_extracting_triangle(legs).status, Status.PASS)

    def test_contracting_is_not_extracting(self):
        from ewave.rules.triangles import is_extracting_triangle
        self.assertEqual(is_extracting_triangle(_contracting_triangle()).status,
                         Status.NA)


# --------------------------------------------------------------------------- #
# Complex-correction X bounds (rules.triangles — RULESET §I.3)
# --------------------------------------------------------------------------- #
class TestXWaveBounds(unittest.TestCase):
    prior = _w(0, 100, 10, 90)   # length 10

    def test_small_x_passes(self):
        from ewave.rules.triangles import x_wave_check
        self.assertEqual(x_wave_check(self.prior, _w(10, 90, 15, 95)).status,
                         Status.PASS)

    def test_oversized_x_is_structural_error(self):
        from ewave.rules.triangles import x_wave_check
        # 120% of W: too big for an x-wave, too small for the large-X regime
        self.assertEqual(x_wave_check(self.prior, _w(10, 90, 15, 102)).status,
                         Status.FAIL)

    def test_large_x_regime_is_ref(self):
        from ewave.rules.triangles import x_wave_check
        # >=161.8% of W -> LARGE-X regime: reassess degree (REF, never a gate)
        r = x_wave_check(self.prior, _w(10, 90, 15, 107))
        self.assertEqual(r.status, Status.REF)
        self.assertIn("LARGE-X", r.detail)

    def test_max_two_x_waves(self):
        from ewave.rules.corrections import max_x_count_check
        self.assertEqual(max_x_count_check(2).status, Status.PASS)
        self.assertEqual(max_x_count_check(3).status, Status.FAIL)


# --------------------------------------------------------------------------- #
# Zigzag / flat refinements (rules.corrections — RULESET §I.4/§I.5)
# --------------------------------------------------------------------------- #
class TestCorrectionRefinements(unittest.TestCase):
    def test_zigzag_c_beyond_a_passes(self):
        from ewave.rules.corrections import zigzag_c_check
        legs = [_w(0, 100, 10, 80), _w(10, 80, 15, 90), _w(15, 90, 25, 70)]
        self.assertEqual(zigzag_c_check(legs).status, Status.PASS)

    def test_truncated_c_warns(self):
        from ewave.rules.corrections import zigzag_c_check
        legs = [_w(0, 100, 10, 80), _w(10, 80, 15, 90), _w(15, 90, 25, 85)]
        r = zigzag_c_check(legs)
        self.assertEqual(r.status, Status.WARN)
        self.assertIn("truncated", r.detail)

    def test_b_slower_than_a_passes(self):
        from ewave.rules.corrections import correction_time_rules
        res = correction_time_rules([_w(0, 100, 10, 80), _w(10, 80, 22, 90)])
        self.assertEqual([r.status for r in res], [Status.PASS])

    def test_b_faster_than_a_warns_with_sow_diagnosis(self):
        from ewave.rules.corrections import correction_time_rules
        res = correction_time_rules([_w(0, 100, 10, 80), _w(10, 80, 14, 90)])
        self.assertEqual([r.status for r in res], [Status.WARN, Status.REF])
        self.assertIn("triangle/diametric", res[1].detail)

    def test_flat_b_bands(self):
        from ewave.rules.corrections import flat_b_band
        A = _w(0, 100, 10, 80)                       # length 20
        cases = [(93.0, "WEAK"), (98.0, "NORMAL"), (102.0, "STRONG")]
        for b_end, band in cases:
            r = flat_b_band(A, _w(10, 80, 20, b_end))
            self.assertEqual(r.status, Status.PASS, r.detail)
            self.assertIn(band, r.rule)
        # <61.8% retrace is zigzag territory, not a flat
        self.assertEqual(flat_b_band(A, _w(10, 80, 20, 90)).status, Status.NA)


# --------------------------------------------------------------------------- #
# Terminal W3 > W1 (rules.diagonals — audit G10)
# --------------------------------------------------------------------------- #
class TestTerminalW3(unittest.TestCase):
    @staticmethod
    def _terminal(w3_top):
        return [_w(0, 100, 10, 110),           # w1 (10)
                _w(10, 110, 20, 104),          # w2 (60% retrace)
                _w(20, 104, 30, w3_top),       # w3
                _w(30, w3_top, 40, 108),       # w4 (overlaps w1's end 110)
                _w(40, 108, 50, 112)]          # w5

    def test_w3_exceeds_w1_passes(self):
        from ewave.rules.diagonals import terminal_rules
        res = terminal_rules(self._terminal(116.0))   # w3 len 12 > 10
        self.assertEqual(_by_rule(res, "wave3 exceeds wave1").status, Status.PASS)

    def test_w3_short_of_w1_warns(self):
        from ewave.rules.diagonals import terminal_rules
        res = terminal_rules(self._terminal(112.0))   # w3 len 8 < 10
        self.assertEqual(_by_rule(res, "wave3 exceeds wave1").status, Status.WARN)


# --------------------------------------------------------------------------- #
# Ichimoku: causal indicator + opt-in strand (audit G6)
# --------------------------------------------------------------------------- #
def _trend_bars(n=120, start=100.0, step=0.5):
    bars = []
    p = start
    for i in range(n):
        o, c = p, p + step
        bars.append((i * 900.0, o, c + 0.2, o - 0.2, c, 1000.0))
        p = c
    return bars


class TestIchimoku(unittest.TestCase):
    def test_causality_prefix_invariance(self):
        """Values at bar i must not change when future bars are appended —
        the no-lookahead property every new indicator must prove."""
        from ewave.features.indicators import ichimoku
        bars = _trend_bars(120)
        full = ichimoku(bars)
        part = ichimoku(bars[:90])
        for key in ("tenkan", "kijun", "senkou_a", "senkou_b"):
            self.assertEqual(full[key][:90], part[key],
                             f"{key} repaints when future bars arrive")

    def test_warmup_is_none_and_no_chikou(self):
        from ewave.features.indicators import ichimoku
        ik = ichimoku(_trend_bars(120))
        self.assertIsNone(ik["senkou_b"][50])      # 52+26 bars of warmup
        self.assertIsNotNone(ik["senkou_b"][100])
        self.assertNotIn("chikou", ik)             # unusable at t -> not exposed

    def test_strand_direction(self):
        from ewave.signals.confluence import ichimoku_trend
        up = _trend_bars(120, step=0.5)
        self.assertTrue(ichimoku_trend(up, bullish=True).confirm)
        self.assertFalse(ichimoku_trend(up, bullish=False).confirm)

    def test_strand_insufficient_history(self):
        from ewave.signals.confluence import ichimoku_trend
        self.assertFalse(ichimoku_trend(_trend_bars(40)).confirm)

    def test_score_reversal_strand_is_opt_in(self):
        """Default confluence report is unchanged (6 strands); the Ichimoku
        strand appears only when explicitly enabled — anchors stay pinned."""
        from ewave.signals.confluence import score_reversal
        bars = _trend_bars(120)
        zone = (bars[-1][4] - 5, bars[-1][4] + 5)
        off = score_reversal("TEST", bars, zone, bullish=True)
        on = score_reversal("TEST", bars, zone, bullish=True, use_ichimoku=True)
        self.assertEqual(len(on.strands), len(off.strands) + 1)
        self.assertIn("Ichimoku", [s.name for s in on.strands][-1])

    def test_profile_knob_defaults_off(self):
        from ewave.rules.profiles import Profile
        self.assertFalse(Profile(name="x").use_ichimoku)


# --------------------------------------------------------------------------- #
# Ghost-forward enrichment (spec §10-§17 — audit G5)
# --------------------------------------------------------------------------- #
class TestGhostForwardEnrichment(unittest.TestCase):
    @staticmethod
    def _run():
        from ewave.validation.ghost_forward import stability
        bars = _trend_bars(80)

        def forecaster(window):
            if len(window) < 20:
                return None
            t = window[-1][0]
            return {"direction": "up", "target": window[-1][4] + 5,
                    "invalidation": window[-1][4] - 5, "confidence": 0.5,
                    "kind": "test",
                    "meta": {"setup_confirmed_t": t - 1800.0}}  # knowable 2 bars ago

        snaps = stability.snapshot_pass(bars, forecaster, roll=20, forward="all",
                                        horizon=10, profile="unit-test",
                                        config_hash="cafe12345678")
        outs = stability.outcome_pass(bars, snaps, roll=20, forward="all",
                                      horizon=10, frozen=True)
        return snaps, stability.metrics(snaps, outs)

    def test_snapshot_provenance_fields(self):
        snaps, _ = self._run()
        s = next(s for s in snaps if s.has_forecast)
        self.assertEqual(s.profile, "unit-test")
        self.assertEqual(s.config_hash, "cafe12345678")
        self.assertEqual(s.setup_confirmed_t, s.t - 1800.0)

    def test_metrics_expose_lag_states_and_repaint_level(self):
        _, m = self._run()
        self.assertEqual(m["late_signal_rate"], 1.0)          # every fire lags setup
        self.assertEqual(m["avg_signal_lag_secs"], 1800.0)
        self.assertIn("repaint_level", m)
        self.assertIn(m["repaint_level"], ("NONE", "LOW", "MEDIUM", "HIGH"))
        self.assertEqual(sorted(m["stability_states"]),
                         ["disappeared", "downgraded", "reclassified",
                          "stable", "upgraded"])


# --------------------------------------------------------------------------- #
# Model enrichments (ewauto SPEC parity — Pivot provenance, Bar vwap)
# --------------------------------------------------------------------------- #
class TestModelEnrichments(unittest.TestCase):
    bars = _trend_bars(120)

    def test_pivot_provenance_defaults_are_inert(self):
        p = Pivot(0.0, 100.0, "H")
        self.assertEqual(p.source, "")
        self.assertIsNone(p.meta)

    def test_detectors_stamp_source_and_threshold(self):
        from ewave.pivots.fractal import detect
        from ewave.pivots.percentage_reversal import zigzag_causal
        # sawtooth so the zigzag actually finds reversals
        saw = []
        for i in range(200):
            p = 100.0 + (10.0 if (i // 10) % 2 == 0 else -10.0) * ((i % 10) / 10.0)
            saw.append((i * 900.0, p, p + 0.5, p - 0.5, p, 1000.0))
        pv = zigzag_causal(saw, pct=0.02)
        self.assertTrue(pv)
        self.assertEqual(pv[0].source, "pct_reversal")
        self.assertEqual(pv[0].meta, {"pct": 0.02})
        pa = zigzag_causal(saw, pct=1.0, atr_n=14)
        self.assertEqual(pa[0].source, "atr")
        self.assertEqual(pa[0].meta, {"pct": 1.0, "atr_n": 14})
        pf = detect(saw, 2, 2)
        self.assertTrue(pf)
        self.assertEqual(pf[0].source, "fractal")
        self.assertEqual(pf[0].meta, {"n_left": 2, "n_right": 2})

    def test_bar_vwap_roundtrip_and_legacy_stability(self):
        from ewave.data.models import BarSeries
        d = {"symbol": "X", "interval": "1d", "asof": "2026-01-01",
             "bars": [{"t": 1, "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 10,
                       "vwap": 1.25},
                      {"t": 2, "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 10}]}
        bs = BarSeries.from_dict(d)
        self.assertEqual(bs.bars[0].vwap, 1.25)
        self.assertIsNone(bs.bars[1].vwap)         # absent stays absent
        self.assertEqual(bs.to_dict(), d)          # serialize only when set
        # engine tuple form is untouched (six fields, no vwap)
        self.assertEqual(len(bs.bars[0].tuple()), 6)


if __name__ == "__main__":
    unittest.main()
