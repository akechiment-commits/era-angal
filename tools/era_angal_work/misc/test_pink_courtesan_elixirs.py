"""Evaluate elixir gain, exact restoration, and bounded desire modifiers."""
import re
import unittest
from test_master_ability_purchase import source, function
from test_audit4_fixes import run

TRACHECK = source("TRACHECK*")
def body(name):
    # Existing evaluator does not implement -=; express the identical operation.
    s = function(TRACHECK, name).replace("\r\n", "\n")
    return re.sub(r"(?m)^(\s*)([A-Z][A-Z0-9]*(?::[A-Z0-9]+)*) -= (.+)$", r"\1\2 += -(\3)", s)

class PinkCourtesanTests(unittest.TestCase):
    def test_skill_boost_scales_and_restores_exactly_including_growth(self):
        for original, expected in [(0, 10), (10, 25), (100, 160), (9999, 15008), (2**63-1, 2**63-1)]:
            state = run(body("COURTESAN_ELIXIR_SKILL"), {"ABL:2": original, "TEQUIP:0:40": 4096})
            self.assertEqual(state["ABL:2"], expected)
            growth = 7 if original < 2**63-8 else 0
            state["ABL:2"] += growth
            restored = run(body("RESTORE_COURTESAN_ELIXIR"), state)
            self.assertEqual(restored["ABL:2"], original + growth)
            self.assertEqual(restored["TEQUIP:0:148"], 0)
            self.assertEqual(restored["TEQUIP:0:40"], 0)
            self.assertEqual(run(body("RESTORE_COURTESAN_ELIXIR"), restored)["ABL:2"], original + growth)

    def test_legacy_skill_bonus_and_other_elixirs_are_preserved(self):
        state = run(body("RESTORE_COURTESAN_ELIXIR"), {"ABL:2": 110, "TEQUIP:0:40": 4096 + 64})
        self.assertEqual(state["ABL:2"], 100)
        self.assertEqual(state["TEQUIP:0:40"], 64)
        state = run(body("RESTORE_COURTESAN_ELIXIR"), {"ABL:2": 110, "TEQUIP:0:40": 64})
        self.assertEqual(state["ABL:2"], 110)

    def test_pink_activation_has_no_immediate_parameter_gain(self):
        for count in (0, 1, 5):
            state = run(body("PINK_ELIXIR_ACTIVATE"), {"PALAM:5": 1000, "TFLAG:37": -30, "TEQUIP:0:28": count})
            self.assertEqual(state["PALAM:5"], 1000)
            self.assertEqual(state["TFLAG:37"], -30)
            self.assertEqual(state["TEQUIP:0:28"], 1 if count == 0 else count)

    def test_pink_desire_multiplier_is_safe_and_not_active_without_drug(self):
        for value, expected in [(0, 0), (100, 300), (2**63-1, 10**16-1)]:
            state = run(body("PINK_ELIXIR_DESIRE"), {"UP:5": value, "TEQUIP:0:28": 1})
            self.assertEqual(state["UP:5"], expected)
        for count, excluded in [(0, 0), (1, 1)]:
            state = run(body("PINK_ELIXIR_DESIRE"), {"UP:5": 100, "TEQUIP:0:28": count, "TFLAG:201": excluded})
            self.assertEqual(state["UP:5"], 100)

    def test_shared_activation_modifier_and_both_cleanup_routes(self):
        self.assertIn("CALL PINK_ELIXIR_ACTIVATE", source("TREASURE*"))
        self.assertIn("CALL PINK_ELIXIR_ACTIVATE", source("COMF/COMF310.ERB"))
        self.assertIn("CALL PINK_ELIXIR_DESIRE", function(TRACHECK, "UP_TALENT_CHECK"))
        for pattern in ["SOURCE*", "REVMODE*"]:
            self.assertIn("CALL UP_TALENT_CHECK", source(pattern))
        for pattern in ["AFTERTRA*", "YU-CTION*"]:
            self.assertIn("CALL RESTORE_COURTESAN_ELIXIR", source(pattern))

if __name__ == "__main__":
    unittest.main()
