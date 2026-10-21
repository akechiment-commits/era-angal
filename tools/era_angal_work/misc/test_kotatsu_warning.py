"""Exercise kotatsu warning and next-action sleep transitions."""
import unittest
from test_master_ability_purchase import source, function
from test_audit4_fixes import run
BODY = function(source("COMF/COMF314.ERB"), "KOTATSU_SLEEP_CHECK").replace("BEGIN AFTERTRAIN", "SLEPT = 1\nRETURN 0")
INITIAL = {"TEQUIP:0:7": 1, "RAND:4": 0, "RAND:2": 0,
           "BASE:0:0": 10, "BASE:0:4": 20, "MAXBASE:0:0": 100, "MAXBASE:0:4": 200,
           "BASE:1:0": 30, "BASE:1:4": 40, "MAXBASE:1:0": 300, "MAXBASE:1:4": 400,
           "PLAYER": 1}
class KotatsuWarningTests(unittest.TestCase):
    def test_warning_turn_cannot_sleep_even_when_both_draws_are_zero(self):
        state = run(BODY, INITIAL)
        self.assertEqual(state["TEQUIP:0:150"], 1)
        self.assertEqual(state["SLEPT"], 0)
        self.assertEqual(state["BASE:0:0"], 10)

    def test_only_the_next_action_can_sleep_and_recovers_both_people(self):
        warned = run(BODY, INITIAL)
        slept = run(BODY, {**warned, "RAND:4": 3})
        self.assertEqual(slept["SLEPT"], 1)
        self.assertEqual(slept["TEQUIP:0:150"], 0)
        for actor in (0, 1):
            for channel in (0, 4):
                self.assertEqual(slept[f"BASE:{actor}:{channel}"], slept[f"MAXBASE:{actor}:{channel}"])

    def test_sleep_healing_preserves_existing_health_above_maximum(self):
        state = run(BODY, {**INITIAL, "TEQUIP:0:150": 1, "BASE:0:0": 3800, "BASE:1:0": 4000})
        self.assertEqual(state["SLEPT"], 1)
        self.assertEqual(state["BASE:0:0"], 3800)
        self.assertEqual(state["BASE:1:0"], 4000)
        self.assertEqual(state["BASE:0:4"], state["MAXBASE:0:4"])

    def test_recovering_from_warning_does_not_rewarn_in_the_same_action(self):
        warned = run(BODY, INITIAL)
        recovered = run(BODY, {**warned, "RAND:2": 1})
        self.assertEqual(recovered["TEQUIP:0:150"], 0)
        self.assertEqual(recovered["SLEPT"], 0)
        self.assertEqual(run(BODY, recovered)["TEQUIP:0:150"], 1)

    def test_stowing_and_exempt_actions_clear_warning(self):
        for values in [{"TEQUIP:0:7": 0}, {"SELECTCOM": 368}, {"SELECTCOM": 369}]:
            state = run(BODY, {**INITIAL, "TEQUIP:0:150": 1, **values})
            self.assertEqual(state["TEQUIP:0:150"], 0)
            self.assertEqual(state["SLEPT"], 0)
        com = function(source("COMF/COMF314.ERB"), "COM314")
        self.assertIn("TEQUIP:7 = 0\r\n\tTEQUIP:150 = 0", com)
        self.assertIn("TEQUIP:150 = 0", function(source("AFTERTRA*"), "RETURN_TALENT"))

if __name__ == "__main__":
    unittest.main()
