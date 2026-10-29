"""Execute the actual cooking aptitude branches at and beyond their boundaries."""
from decimal import Decimal
import re
import unittest

from test_master_ability_purchase import source, evaluate


def aptitude_effect(pattern, aptitude, base=1000):
    text = source(pattern)
    start = re.search(r"^IF (ABL:(?:MASTER:)?50) >= 2", text, re.M)
    if not start:
        raise AssertionError("Highest cooking aptitude tier missing")
    block = text[start.start():text.index("ENDIF", start.start())]
    state = {start[1]: aptitude}
    taken = False
    active = False
    value = base
    for raw in block.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.startswith("IF "):
            active = bool(evaluate(line[3:], state))
            taken = active
        elif line.startswith("ELSEIF "):
            active = not taken and bool(evaluate(line[7:], state))
            taken |= active
        elif active and line.startswith("TIMES "):
            multiplier = Decimal(line.split(",")[1].strip())
            value = int(Decimal(value) * multiplier)
    return value


class CookingAptitudeTests(unittest.TestCase):
    def test_self_sale_tiers_and_no_drop_above_two(self):
        for aptitude, expected in ((-1, 750), (0, 1000), (1, 1500),
                                   (2, 1750), (3, 1750), (50, 1750), (100, 1750)):
            with self.subTest(aptitude=aptitude):
                self.assertEqual(aptitude_effect("LUNCH_SELF_SALE*", aptitude), expected)

    def test_both_meal_tiers_and_no_drop_above_two(self):
        for pattern in ("LUNCH_SELF_EAT*", "LUNCH_EAT*"):
            for aptitude, expected in ((-1, 900), (0, 1000), (1, 1100),
                                       (2, 1200), (3, 1200), (50, 1200), (100, 1200)):
                with self.subTest(pattern=pattern, aptitude=aptitude):
                    self.assertEqual(aptitude_effect(pattern, aptitude), expected)

    def test_monotonic_for_every_reachable_aptitude(self):
        for pattern in ("LUNCH_SELF_SALE*", "LUNCH_SELF_EAT*", "LUNCH_EAT*"):
            values = [aptitude_effect(pattern, level) for level in range(-1, 101)]
            self.assertEqual(values, sorted(values), pattern)


if __name__ == "__main__":
    unittest.main()
