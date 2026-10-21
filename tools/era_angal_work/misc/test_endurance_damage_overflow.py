"""Reproduce the screenshot overflow and execute the corrected ERB arithmetic."""
import math
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import source, function


TEXT = source("COUNTERSYSTEM*")
SCALE = function(TEXT, "SCALE_ENDURANCE_DAMAGE")
DAMAGE = function(TEXT, "PARTNER_TURN_ENDURANCE_DAMAGE")
DAMAGE = DAMAGE[DAMAGE.index("STRENGTH = LIMIT"):DAMAGE.index("IF BEFORE_ENDURANCE > 0")]
MAX_INTEGER = 2**63 - 1


def execute(body, state):
    def key(token):
        return token.replace("BASE:(TFLAG:996):4", f"BASE:{state['TFLAG:996']}:4")

    def expr(text):
        text = text.replace("BASE:(TFLAG:996):4", f"BASE:{state['TFLAG:996']}:4")
        builtins = {"MIN": "min", "MAX": "max", "LIMIT": "limit", "SQRT": "sqrt",
                    "SCALE_ENDURANCE_DAMAGE": "scale"}
        text = re.sub(r"\b[A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*",
                      lambda m: builtins.get(m[0], str(state[m[0]])), text)
        text = text.replace("/", "//")
        return eval(text, {"__builtins__": {}, "min": min, "max": max,
                           "limit": lambda value, low, high: min(max(value, low), high),
                           "sqrt": math.isqrt, "scale": scale})

    skip = False
    for raw in body.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith(("#", "PRINT")):
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not expr(line[4:])
        elif line.startswith("RETURNF "):
            return expr(line[8:])
        else:
            match = re.fullmatch(r"(.+?) (=|\+=|\*=) (.+)", line)
            if not match:
                raise AssertionError("Unsupported statement: " + line)
            target, value = key(match[1]), expr(match[3])
            if match[2] == "+=":
                value += state[target]
            elif match[2] == "*=":
                value *= state[target]
            if not 0 <= value <= MAX_INTEGER:
                raise AssertionError("Integer overflow: " + line)
            state[target] = value


def scale(value, factor):
    return execute(SCALE, defaultdict(int, {"ARG": value, "ARG:1": factor}))


def damage(strength, endurance, level=4, volume=48, half=False):
    state = defaultdict(int, {"TFLAG:714": strength, "TFLAG:302": level,
                              "TFLAG:719": volume, "TFLAG:543": int(half),
                              "TFLAG:996": 0, "BASE:0:4": endurance})
    execute(DAMAGE, state)
    return state


class EnduranceDamageOverflowTests(unittest.TestCase):
    def test_original_screenshot_arithmetic_wraps_negative_and_becomes_one(self):
        strength = 17592413445
        raw = 2400 * math.isqrt(strength) + 48 * 8
        product = raw * (100 + strength * 2)
        self.assertGreater(product, MAX_INTEGER)
        wrapped = (product + 2**63) % 2**64 - 2**63
        self.assertLess(wrapped, 0)
        self.assertEqual(max(1, -(abs(wrapped) // 100)), 1)
        state = damage(strength, 5000)
        self.assertEqual(state["DAMAGE"], 5000)
        self.assertEqual(state["BASE:0:4"], 0)

    def test_safe_scaling_matches_exact_math_including_fraction_and_saturation(self):
        for value in (1, 99, 100, 101, 2400, 318326784, 8000000000000000):
            for factor in (100, 102, 2102, 35184826990, 2000000000000100):
                self.assertEqual(scale(value, factor), min(value * factor // 100, 9000000000000000000))

    def test_ordinary_consumption_formula_and_half_turn_are_preserved(self):
        for strength in (1, 2, 4, 1001):
            for level in (1, 2, 4):
                raw = 600 * level * math.isqrt(strength) + 48 * level * 2
                expected = raw * (100 + strength * 2) // 100
                for half in (False, True):
                    state = damage(strength, 10000000, level=level, half=half)
                    wanted = (expected + 1) // 2 if half else expected
                    self.assertEqual(state["DAMAGE"], wanted)
                    self.assertEqual(state["BASE:0:4"], 10000000 - wanted)

    def test_extreme_values_cannot_wrap_or_restore_endurance(self):
        for strength in (17592413445, 10**15, MAX_INTEGER):
            for half in (False, True):
                state = damage(strength, 10**15, volume=MAX_INTEGER, half=half)
                self.assertEqual(state["DAMAGE"], 10**15)
                self.assertEqual(state["BASE:0:4"], 0)

    def test_damage_display_matches_actual_loss_at_low_or_zero_endurance(self):
        for endurance in (0, 1, 25, 5000):
            state = damage(17592413445, endurance)
            self.assertEqual(state["DAMAGE"], endurance - state["BASE:0:4"])
            self.assertIn("の耐力-{DAMAGE}", DAMAGE)


if __name__ == "__main__":
    unittest.main()
