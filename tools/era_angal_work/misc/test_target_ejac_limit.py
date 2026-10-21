"""Evaluate the actual partner gain helper, including cap randomization."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import source, function


TEXT = source("TRACHECK*")
BODY = function(TEXT, "GET_TARGET_EJAC_GAIN")
CAP = 10**15


def gain(inputs, draw=100000):
    state = defaultdict(int, {("ARG" if i == 0 else f"ARG:{i}"): n for i, n in enumerate(inputs)})

    def expr(text):
        text = re.sub(r"RAND:(\d+)", lambda m: str(draw) if 0 <= draw < int(m[1]) else "invalid", text)
        text = re.sub(r"\b[A-Z][A-Z0-9]*(?::[A-Z0-9]+)*",
                      lambda m: "limit" if m[0] == "LIMIT" else str(state[m[0]]), text)
        return eval(text.replace("/", "//"), {"__builtins__": {},
                    "limit": lambda n, low, high: min(max(n, low), high)})

    skip = False
    for raw in BODY.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not expr(line[4:])
        elif line.startswith("RETURNF "):
            return expr(line[8:])
        else:
            match = re.fullmatch(r"GAIN (=|\+=) (.+)", line)
            if not match:
                raise AssertionError(line)
            value = expr(match[2])
            state["GAIN"] = value + state["GAIN"] if match[1] == "+=" else value
            if not 0 <= state["GAIN"] <= 2**63 - 1:
                raise AssertionError("Int64 overflow")


class PartnerEjaculationLimitTests(unittest.TestCase):
    def test_normal_weighting_is_preserved(self):
        for values in [(0, 0, 0, 0, 0), (100, 50, 70, 90, 110), (10**8, 0, 0, 0, 0)]:
            expected = values[0] * 3 + values[1] // 10 + values[2] // 5 + values[3] // 5 + values[4]
            self.assertEqual(gain(values), expected)

    def test_cap_varies_from_ninety_to_one_hundred_ten_percent(self):
        values = (CAP, CAP, CAP, CAP, CAP)
        self.assertEqual(gain(values, 0), CAP * 9 // 10)
        self.assertEqual(gain(values, 100000), CAP)
        self.assertEqual(gain(values, 200000), CAP * 11 // 10)
        multipliers = {(gain(values, n) // 20 + 5049) // 5000 for n in range(0, 200001, 10000)}
        self.assertEqual(len(multipliers), 21)
        self.assertGreater(min(multipliers), 1000)

    def test_extreme_and_negative_inputs_cannot_overflow(self):
        self.assertEqual(gain((-1,) * 5), 0)
        self.assertEqual(gain((2**63 - 1,) * 5, 200000), CAP * 11 // 10)
        # All positive modifiers combined are at most 13.2x before dividing by 20.
        self.assertLess((CAP * 11 // 10) * 132 // 10 + CAP, 2**63 - 1)

    def test_display_and_statistics_use_actual_randomized_multiplier(self):
        body = function(TEXT, "TARGET_EJAC_CHECK")
        self.assertIn("GET_TARGET_EJAC_GAIN(UP:0, UP:1, UP:2, UP:14, UP:18)", body)
        self.assertIn("TFLAG:715 = S / EJAC", body)
        self.assertEqual(body.count("射精×{TFLAG:715}"), 3)
        self.assertIn("CFLAG:TARGET:1280 += TFLAG:715", body)
        self.assertIn("EJAC = LIMIT(MAXBASE:2, 1, 1000000000000000)", body)


if __name__ == "__main__":
    unittest.main()
