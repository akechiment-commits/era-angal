"""Check the common purple-elixir pleasure modifier against actual source."""
import unittest

from test_master_ability_purchase import source, function
from test_audit4_fixes import run


BODY = function(source("TRACHECK*"), "PURPLE_ELIXIR_PLEASURE")
CHANNELS = (0, 1, 2, 14, 18)


class PurpleElixirTests(unittest.TestCase):
    def test_boost_doubles_all_pleasure_channels_even_when_already_sensitive(self):
        initial = {f"UP:{n}": 100 + n for n in CHANNELS}
        for sensitive in (0, 1, 2):
            state = run(BODY, {**initial, "TEQUIP:0:40": 64, "TALENT:102": sensitive})
            for n in CHANNELS:
                self.assertEqual(state[f"UP:{n}"], 2 * initial[f"UP:{n}"])

    def test_modifier_is_inactive_without_drug_or_during_excluded_processing(self):
        initial = {f"UP:{n}": 100 for n in CHANNELS}
        for equipment, processing in [(0, 0), (8, 0), (64, 1)]:
            state = run(BODY, {**initial, "TEQUIP:0:40": equipment, "TFLAG:201": processing})
            self.assertTrue(all(state[f"UP:{n}"] == 100 for n in CHANNELS))

    def test_extreme_values_saturate_without_integer_overflow(self):
        for value, expected in [(-1, 0), (0, 0), (5*10**15, 10**16), (2**63-1, 10**16)]:
            state = run(BODY, {**{f"UP:{n}": value for n in CHANNELS}, "TEQUIP:0:40": 64})
            self.assertTrue(all(state[f"UP:{n}"] == expected for n in CHANNELS))

    def test_common_modifier_and_both_cleanup_paths_cover_mental_sensitivity(self):
        shared = function(source("TRACHECK*"), "UP_TALENT_CVA_CHECK")
        self.assertEqual(shared.count("CALL PURPLE_ELIXIR_PLEASURE"), 1)
        for pattern, name in [("SOURCE*", "SOURCE_CHECK"), ("REVMODE*", "REVMODE_SOURCE_CHECK")]:
            self.assertIn("CALL UP_TALENT_CVA_CHECK", function(source(pattern), name))
        for pattern in ("AFTERTRA*", "YU-CTION*"):
            cleanup = source(pattern).split(";超敏感体質喪失", 1)[1]
            self.assertIn("TALENT:597 -= 1", cleanup)
            self.assertIn("TALENT:596 = 1", cleanup)


if __name__ == "__main__":
    unittest.main()
