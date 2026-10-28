"""Source-driven regression for recovery, drug eligibility and hidden clothes."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import ROOT, source, function


SHOP = source("SHOP_ITEM*")
TREASURE = source("TREASURE*")


def expression(text, values):
    state = defaultdict(int, values)

    def value(match):
        token = match[0]
        if token in ("MIN", "MAX"):
            return token.lower()
        token = token.replace(":ARG:", f":{state['ARG']}:")
        return str(state[token])

    text = re.sub(r"\b[A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*", value, text)
    text = text.replace("||", " or ").replace("&&", " and ")
    return eval(text, {"__builtins__": {}, "min": min, "max": max})


def eligible(character, master=0, current=100, maximum=1000, separated=0):
    state = {"ARG": character, "MASTER": master, "CHARANUM": 3,
             f"BASE:{character}:0": current, f"MAXBASE:{character}:0": maximum,
             f"CFLAG:{character}:21": separated}
    skip = False
    for raw in function(SHOP, "CAN_USE_ENERGY_DRUG").splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not expression(line[4:], state)
        elif line.startswith("RETURNF "):
            return expression(line[8:], state)
        else:
            raise AssertionError(line)


class Audit5FixTests(unittest.TestCase):
    def test_energy_drug_excludes_master_even_when_not_index_zero(self):
        self.assertFalse(eligible(0))
        self.assertFalse(eligible(1, master=1))
        self.assertTrue(eligible(1))
        self.assertTrue(eligible(2))

    def test_energy_drug_requires_deficit_present_character_and_valid_index(self):
        for arguments in [dict(character=-1), dict(character=3), dict(character=1, separated=1),
                          dict(character=1, current=1000), dict(character=1, current=2000)]:
            self.assertFalse(eligible(**arguments))
        self.assertTrue(eligible(1, current=0))

    def test_energy_drug_sale_and_target_list_use_shared_predicate(self):
        sale = function(SHOP, "SALEITEM_CHECK")
        use = function(SHOP, "USE_ITEM")
        self.assertIn("SIF CAN_USE_ENERGY_DRUG(COUNT)", sale)
        self.assertIn("SIF BOUGHT == 70 && CAN_USE_ENERGY_DRUG(COUNT) == 0", use)
        self.assertIn("ELSEIF TFLAG:RESULT == 0", use)

    def test_full_recovery_preserves_existing_hp_and_mp_overcap(self):
        block = function(TREASURE, "USE_TREASURE_ITEM").split("ELSEIF RESULT == 17", 1)[1].split("ELSEIF RESULT == 18", 1)[0]
        for current, maximum, expected in [(100, 5000, 5000), (5000, 5000, 5000), (6000, 5000, 6000)]:
            for resource in (0, 1):
                formula = re.search(rf"BASE:{resource} = (.+)", block)[1].strip()
                self.assertEqual(expression(formula, {f"BASE:{resource}": current,
                                                      f"MAXBASE:{resource}": maximum}), expected)

    def test_energy_drug_cannot_reduce_overcap_and_recovers_only_to_maximum(self):
        use = function(SHOP, "USE_ITEM")
        block = use.split(";体力回復", 1)[1].split("ENDIF", 1)[0]
        formula = re.search(r"BASE:RESULT:0 = (.+)", block)[1].strip()
        self.assertIn("SIF BASE:RESULT:0 < MAXBASE:RESULT:0", block)
        for current, expected in [(100, 400), (4900, 5000)]:
            self.assertEqual(expression(formula, {"BASE:RESULT:0": current, "MAXBASE:RESULT:0": 5000}), expected)

    def test_red_elixir_recovers_to_double_hp_preserves_more_and_keeps_unlock(self):
        block = function(TREASURE, "USE_TREASURE_ITEM").split("ELSEIF RESULT == 27", 1)[1].split("ELSEIF RESULT == 28", 1)[0]
        formula = re.search(r"BASE:0 = (.+)", block)[1].strip()
        for current, maximum, expected in [(0, 5000, 10000), (6000, 5000, 10000), (15000, 5000, 15000),
                                          (0, 2**63-1, 999999999999999998)]:
            self.assertEqual(expression(formula, {"BASE:0": current, "MAXBASE:0": maximum}), expected)
        self.assertLess(block.index("TEQUIP:41 = 1"), block.index("BASE:0 ="))
        self.assertIn("ITEM:527 -= 1", block)
        self.assertIn("IF TEQUIP:41", block)  # Existing effect cannot be reused.

    def test_purple_drug_allows_existing_sensitive_traits(self):
        block = function(TREASURE, "USE_TREASURE_ITEM").split("ELSEIF RESULT == 24", 1)[1].split("ELSEIF RESULT == 25", 1)[0]
        self.assertNotIn("こんなもの必要ない", block)
        self.assertNotIn("IF TALENT:42", block)
        self.assertIn("IF TEQUIP:40 & 64", block)
        self.assertIn("ITEM:524 -= 1", block)

    def test_only_displayed_available_clothes_can_be_purchased(self):
        text = (ROOT / "ERB/COMF/COMF391.ERB").read_bytes().decode("cp932")
        guard = re.search(r"ELSEIF (LOCAL:RESULT != 1)", function(text, "CLOTHES_SHOP"))[1]
        for availability, rejected in [(-1, True), (0, True), (1, False)]:
            self.assertEqual(expression(guard, {"LOCAL:RESULT": availability}), rejected)


if __name__ == "__main__":
    unittest.main()
