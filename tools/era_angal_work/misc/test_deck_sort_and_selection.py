"""Source-driven deck regression checks, separate from Emuera UI testing."""
import re
import unittest

from test_master_ability_purchase import source, function, evaluate


def member_score(values):
    body = function(source("DECK_BATTLE*"), "DECK_MEMBER_SCORE")
    state = {token: 0 for token in re.findall(r"\b(?:ABL|EXP|CFLAG):ARG:\d+", body)}
    state.update(values)
    active = True
    for raw in body.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.startswith("IF "):
            active = bool(evaluate(line[3:], state))
        elif line == "ELSE":
            active = not active
        elif line == "ENDIF":
            active = True
        elif active:
            match = re.fullmatch(r"(LOCAL:\d+) (\+=|=) (.+)", line)
            if match:
                value = evaluate(match[3], state)
                state[match[1]] = state.get(match[1], 0) + value if match[2] == "+=" else value
            elif line.startswith("RETURNF "):
                return evaluate(line[8:], state)
    raise AssertionError("Missing score return")


def remap_from_source(old_chars, new_chars, slots):
    body = source("CHARA_SORT*")
    backup_expr = re.search(r"DECK_MEMBER_NO:\(LOCAL:97\) = (NO:[^\n]+)", body)[1].strip()
    restore_expr = re.search(r"FLAG:\(200 \+ LOCAL:97\) = (GETCHARA[^\n]+)", body)[1].strip()
    saved = []
    for index in slots:
        if index < 1 or index >= len(old_chars):
            saved.append(-1)
        else:
            self_contained = backup_expr.replace("NO:(LOCAL:98)", str(old_chars[index]))
            saved.append(evaluate(self_contained, {}))
    restored = []
    for no in saved:
        if no < 0:
            restored.append(-1)
        else:
            expression = restore_expr.replace("DECK_MEMBER_NO:(LOCAL:97)", str(no))
            restored.append(eval(expression, {"__builtins__": {},
                                               "GETCHARA": lambda n: new_chars.index(n) if n in new_chars else -1}))
    return restored


class DeckSortAndSelectionTests(unittest.TestCase):
    def test_regression_actual_score_ranking(self):
        a = {"ABL:ARG:88": 70, "EXP:ARG:95": 200}
        b = {"ABL:ARG:88": 50, "ABL:ARG:93": 100}
        self.assertEqual(member_score(a), 1500)
        self.assertEqual(member_score(b), 1200)
        self.assertGreater(member_score(a), member_score(b))

    def test_all_score_components_are_retained(self):
        values = {"CFLAG:ARG:2": 1500, "ABL:ARG:88": 50, "ABL:ARG:93": 10,
                  "CFLAG:ARG:306": 20, "EXP:ARG:2": 10, "EXP:ARG:94": 10,
                  "EXP:ARG:95": 10, "EXP:ARG:22": 10, "ABL:ARG:1": 10}
        # 110 affinity + 500 academic + 70 sport + 40 card + 150 experience;
        # ability multiplier is 1020/1000.
        self.assertEqual(member_score(values), 887)

    def test_battle_and_auto_selection_share_score_and_refresh_cards(self):
        text = source("DECK_BATTLE*")
        self.assertIn("LOCAL:1 = DECK_MEMBER_SCORE(Z)", function(text, "CALC_DECK_SCORE"))
        auto = function(text, "AUTO_SELECT_DECK")
        self.assertIn("D = DECK_MEMBER_SCORE(LOCAL)", auto)
        self.assertLess(auto.index("CALL CARD_RECALC_BONUSES"), auto.index("DECK_MEMBER_SCORE(LOCAL)"))
        self.assertIn("IF D > B", auto)
        self.assertIn("SIF CFLAG:LOCAL:21 == 1", auto)

    def test_sort_preserves_members_slot_order_and_empty_slots(self):
        old = [0, 11, 22, 33, 44, 55]
        slots = [1, -1, 4, 2, 5]
        for new in ([0, 22, 11, 33, 44, 55], [0, 55, 44, 33, 22, 11],
                    [0, 44, 11, 55, 22, 33]):
            with self.subTest(order=new):
                restored = remap_from_source(old, new, slots)
                identities = [new[i] if i >= 0 else None for i in restored]
                self.assertEqual(identities, [11, None, 44, 22, 55])

    def test_all_sort_paths_wrap_mutation(self):
        text = source("CHARA_SORT*")
        for name, command in (("CHARA_SORT", "SORTCHARA TALENT:150, BACK"),
                              ("SWAP_SORT", "SWAPCHARA LOCAL:1, LOCAL:2"),
                              ("AUTO_SORT", "SORTCHARA CFLAG:21")):
            body = function(text, name)
            self.assertIn("#DIM DYNAMIC DECK_MEMBER_NO, 5", body)
            self.assertLess(body.index("DECK_MEMBER_NO:(LOCAL:97) = NO:(LOCAL:98)"), body.index(command))
            self.assertGreater(body.index("GETCHARA(DECK_MEMBER_NO:(LOCAL:97))"), body.index(command))


if __name__ == "__main__":
    unittest.main()
