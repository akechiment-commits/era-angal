"""Exhaustive random outcomes for the actual ERB pregnancy predicate."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import source, function


BODY = function(source("EVENT_N_妊娠*"), "NAKADASHI_CHECK")


def check(amount, draw, small=False, danger=True, drug=False, father=1, existing=0):
    state = defaultdict(int, {"T": 0, "P": father, f"CFLAG:0:{100 + father}": amount,
                              "CFLAG:0:104": existing, "TALENT:0:100": int(small),
                              "TALENT:0:137": int(danger), "TEQUIP:0:86": int(drug)})
    domains = []

    def key(token):
        parts = token.split(":")
        if parts[0] in ("CFLAG", "TALENT", "TEQUIP"):
            parts[1:] = [str(state[p]) if not p.isdigit() else p for p in parts[1:]]
        return ":".join(parts)

    def expr(text):
        def random_value(match):
            domain = int(match[1]) if match[1].isdigit() else state[match[1]]
            if not 0 <= draw < domain:
                raise AssertionError((draw, domain))
            domains.append(domain)
            return str(draw)
        text = re.sub(r"RAND:(LOCAL|\d+)", random_value, text)
        text = re.sub(r"\b[A-Z][A-Z0-9]*(?::[A-Z0-9]+)*",
                      lambda m: "min" if m[0] == "MIN" else str(state[key(m[0])]), text)
        text = text.replace("&&", " and ").replace("||", " or ")
        return eval(text, {"__builtins__": {}, "min": min})

    active, frames, skip = True, [], False
    for raw in BODY.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not (active and expr(line[4:]))
        elif line.startswith("IF "):
            frames.append(active)
            active = active and bool(expr(line[3:]))
        elif line == "ELSE":
            active = frames[-1] and not active
        elif line == "ENDIF":
            active = frames.pop()
        elif active:
            if line.startswith("RETURN "):
                break
            match = re.fullmatch(r"([A-Z][A-Z0-9]*(?::[A-Z0-9]+)*) = (.+)", line)
            if not match:
                raise AssertionError("Unsupported statement: " + line)
            state[key(match[1])] = expr(match[2])
    return state["CFLAG:0:104"], domains


class PregnancyProbabilityTests(unittest.TestCase):
    def test_linear_curve_and_ceiling_for_both_body_types(self):
        for small, ceiling in [(False, 16), (True, 24)]:
            for amount in range(1, ceiling + 6):
                outcomes = [check(amount, draw, small=small) for draw in range(ceiling)]
                self.assertEqual(sum(father == 1 for father, _ in outcomes), min(amount, ceiling))
                self.assertTrue(all(domains == [ceiling] for _, domains in outcomes))

    def test_drug_uses_lower_ceiling_regardless_of_fertile_window(self):
        for small, ceiling in [(False, 4), (True, 6)]:
            for danger in (False, True):
                for amount in range(1, ceiling + 4):
                    outcomes = [check(amount, draw, small=small, danger=danger, drug=True)
                                for draw in range(ceiling)]
                    self.assertEqual(sum(father == 1 for father, _ in outcomes), min(amount, ceiling))
                    self.assertTrue(all(domains == [ceiling] for _, domains in outcomes))

    def test_nonfertile_probability_still_uses_one_per_thousand(self):
        for amount in (1, 5, 16, 24, 100, 1001):
            for small in (False, True):
                self.assertEqual(sum(check(amount, draw, small=small, danger=False)[0] == 1
                                     for draw in range(1000)), min(amount, 1000))

    def test_no_positive_amount_means_no_random_draw(self):
        for amount in (-10, -1, 0):
            self.assertEqual(check(amount, 0), (0, []))

    def test_existing_casino_pregnancy_is_preserved(self):
        self.assertEqual(check(24, 0, existing=99), (99, []))

    def test_father_identity_and_separate_accumulation(self):
        for father in (1, 2, 3):
            self.assertEqual(check(16, 15, father=father), (father, [16]))
            self.assertEqual(check(1, 1, father=father), (0, [16]))


if __name__ == "__main__":
    unittest.main()
