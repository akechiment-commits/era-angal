"""Actor-aware ejaculation bonus and action-dependent pink elixir checks."""
import re
import unittest
from test_master_ability_purchase import ROOT, source, function
from test_audit4_fixes import run

def returns(body):
    body = body.replace("\r\n", "\n")
    body = body.replace("TEQUIP:(ARG:1):40", "TEQUIP:GIVER:40").replace("BASE:(ARG:2):2", "BASE:RECEIVER:2")
    body = re.sub(r"(?m)^(\s*)SIF (.+)\n\s*RETURNF (.+)$",
                  r"\1IF \2\nRESULT = \3\nRETURN 0\nENDIF", body)
    body = re.sub(r"(?m)^\s*RETURNF (.+)$", r"RESULT = \1\nRETURN 0", body)
    return body

GAIN = returns(function(source("COMF/CALC_EJAC.ERB"), "COURTESAN_EJAC_GAIN"))
PINK = returns(function(source("TRACHECK*"), "PINK_ELIXIR_EVENT_BONUS"))

def gain(value=100, giver=1, receiver=0, equipment=4096, gauge=0):
    return run(GAIN, {"ARG": value, "ARG:1": giver, "ARG:2": receiver, "GIVER": giver,
                     "RECEIVER": receiver, "CHARANUM": 3, f"TEQUIP:{giver}:40": equipment,
                     f"BASE:{receiver}:2": gauge})["RESULT"]

class ElixirRebalanceTests(unittest.TestCase):
    def test_only_active_drug_on_the_other_actor_doubles_the_gain(self):
        self.assertEqual(gain(), 200)
        self.assertEqual(gain(equipment=0), 100)
        self.assertEqual(gain(equipment=64), 100)
        self.assertEqual(gain(giver=0, receiver=0), 100)
        self.assertEqual(gain(value=0), 0)
        for giver, receiver in [(-1, 0), (3, 0), (1, -1), (1, 3)]:
            self.assertEqual(gain(giver=giver, receiver=receiver), 100)

    def test_boost_and_final_gauge_addition_do_not_overflow(self):
        for gauge in (0, 10**16-1, 10**16, 2**63-1):
            value = gain(value=2**63-1, gauge=gauge)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(gauge + value, max(gauge, 10**16))
            self.assertLessEqual(gauge + value, 2**63-1)

    def test_both_calculators_route_assistant_target_and_player(self):
        text = source("COMF/CALC_EJAC.ERB")
        for name in ("CALC_EJAC", "CALC_EJAC_P"):
            body = function(text, name)
            self.assertIn("IF ARG:1 == TARGET", body)
            self.assertIn("IF ARG:0 == 65", body)
            self.assertIn("COURTESAN_EJAC_GAIN(B, ASSI, ARG:1)", body)
            self.assertIn("COURTESAN_EJAC_GAIN(B, PLAYER, ARG:1)", body)
            self.assertIn("COURTESAN_EJAC_GAIN(B, TARGET, ARG:1)", body)
        for filename in ("COMF21.ERB", "COMF22.ERB", "COMF30.ERB"):
            self.assertIn("COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)", source("COMF/" + filename))
        self.assertIn("COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)", source("YU-CTION*"))

    def test_pink_event_bonus_requires_actual_desire_and_active_drug(self):
        for desire, expected in [(0, 0), (999, 0), (1000, 1), (3000, 3), (15000, 15), (2**63-1, 15)]:
            for active in (0, 1):
                state = run(PINK, {"TARGET": 0, "CHARANUM": 2, "PALAM:5": desire, "TEQUIP:0:28": active})
                self.assertEqual(state["RESULT"], expected if active else 0)
        for target in (-1, 2):
            self.assertEqual(run(PINK, {"TARGET": target, "CHARANUM": 2})["RESULT"], 0)

    def test_event_paths_share_desire_based_bonus_and_repeated_use_is_rejected(self):
        self.assertIn("PINK_ELIXIR_EVENT_BONUS()", function(source("COMMON*"), "PUSH_OVER_RATE"))
        self.assertEqual(source("COMF/COMF323.ERB").count("PINK_ELIXIR_EVENT_BONUS()"), 2)
        section = source("TREASURE*").split("ELSEIF RESULT == 28", 1)[1].split("ELSEIF RESULT == 29", 1)[0]
        self.assertLess(section.index("IF TEQUIP:28 > 0"), section.index("ITEM:528 -= 1"))
        self.assertIn("RESTART", section)

if __name__ == "__main__":
    unittest.main()
