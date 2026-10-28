"""Source-driven regression checks, supplemented by the Emuera runtime audit."""
import re
import unittest

from test_master_ability_purchase import ROOT, source, function, evaluate


def sale_growth(level, points, meal_marker=0):
    body = function(source("LUNCH_SELF_SALE*"), "LUNCH_SELF_SALE")
    body = body[body.index("LOCAL:14 = 0"):body.index("\nWAIT")]
    state = {"ABL:MASTER:90": level, "FLAG:4": points,
             "TFLAG:14": meal_marker, "LOCAL:14": 0}
    active = True
    stack = []
    for raw in body.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.startswith("IF "):
            parent = active
            active = parent and bool(evaluate(line[3:], state))
            stack.append([parent, active])
        elif line.startswith("ELSEIF "):
            parent, taken = stack[-1]
            active = parent and not taken and bool(evaluate(line[7:], state))
            stack[-1][1] |= active
        elif line == "ENDIF":
            active = stack.pop()[0]
        elif active:
            match = re.fullmatch(r"([A-Z:0-9]+) (\+=|=) (\d+)", line)
            if match:
                name, operator, value = match.groups()
                state[name] = (state[name] if operator == "+=" else 0) + int(value)
    return state


class ClubCookingFlagsTests(unittest.TestCase):
    def test_all_cooking_growth_boundaries(self):
        for level, required in ((0, 25), (4, 25), (5, 50), (19, 50),
                                (20, 100), (49, 100), (50, 150), (59, 150),
                                (60, 250), (69, 250), (70, 500), (89, 500),
                                (90, 1000), (999, 1000), (1000, 10000),
                                (9998, 10000)):
            with self.subTest(level=level):
                below = sale_growth(level, required - 1)
                self.assertEqual(below["ABL:MASTER:90"], level)
                self.assertEqual(below["FLAG:4"], required - 1)
                ready = sale_growth(level, required)
                self.assertEqual(ready["ABL:MASTER:90"], level + 1)
                self.assertEqual(ready["FLAG:4"], 0)

    def test_cooking_cap_and_meal_flag_independence(self):
        self.assertEqual(sale_growth(9999, 100000)["ABL:MASTER:90"], 9999)
        self.assertEqual(sale_growth(0, 0, meal_marker=1)["ABL:MASTER:90"], 0)
        self.assertEqual(sale_growth(90, 1000, meal_marker=1)["ABL:MASTER:90"], 91)

    def test_club_csv_and_milk_use_separate_fields(self):
        definitions = (ROOT / "CSV/Cflag.csv").read_text(encoding="cp932")
        self.assertEqual(len(re.findall(r"^1287,", definitions, re.M)), 1)
        for path in (ROOT / "CSV").glob("Chara*.csv"):
            text = path.read_text(encoding="cp932")
            self.assertNotRegex(text, r"(?m)^フラグ,25,")
        for number, expected in ((1, 2), (5, 1), (72, 2)):
            text = next((ROOT / "CSV").glob(f"Chara{number}_*")).read_text(encoding="cp932")
            self.assertIn(f"フラグ,1287,{expected}", text)
        init = function(source("COMMON*"), "NEWCHARA_INIT")
        self.assertIn("CFLAG:A:25 = EXP:A:54", init)
        self.assertNotIn("CFLAG:A:1287", init)

    def test_club_repair_is_per_character_and_uses_csv(self):
        body = function(source("CLUB_ACTIVITY*"), "INIT_CLUB_FLAGS")
        self.assertIn("CSVCFLAG NO:COUNT, 1287, 0", body)
        self.assertIn("CFLAG:COUNT:1287 = RESULT", body)
        self.assertNotIn("RETURN 0", body)
        for pattern in ("CLUB_ACTIVITY*", "DECK_BATTLE*", "SCHOOL_EVENT*", "SHOP_ショップ*"):
            self.assertNotRegex(source(pattern), r"CFLAG:(?:TARGET|COUNT|Z):25\b")


if __name__ == "__main__":
    unittest.main()
