"""Evaluate text branch selection from the actual ERB helper."""
import unittest
from collections import defaultdict

from test_master_ability_purchase import source, function, evaluate


BODY = function(source("EVENT_TEXT*"), "ANIMAL_EAR_REACTION_TEXT")


def reaction(values=None, chance=0, variant=0):
    state = defaultdict(int, {"TARGET": 0, "CHARANUM": 2, "FLAG:6": 1,
                             "TALENT:TARGET:124": 1, "BASE:TARGET:0": 1000})
    state.update(values or {})
    active, stack, skip, printed, draws = True, [], False, [], 0

    def expr(text):
        nonlocal draws
        if "RAND:3" in text:
            text = text.replace("RAND:3", str(chance if draws == 0 else variant))
            draws += 1
        return evaluate(text, state)

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
            stack.append([active, False, None])
            active = active and bool(expr(line[3:]))
            stack[-1][1] = active
        elif line.startswith("ELSEIF "):
            parent, taken, _ = stack[-1]
            active = parent and not taken and bool(expr(line[7:]))
            stack[-1][1] |= active
        elif line == "ELSE":
            parent, taken, _ = stack[-1]
            active = parent and not taken
        elif line.startswith("SELECTCASE "):
            stack.append([active, False, expr(line[11:]) if active else None])
            active = False
        elif line.startswith("CASE "):
            parent, taken, selected = stack[-1]
            active = parent and not taken and selected == int(line[5:])
            stack[-1][1] |= active
        elif line == "CASEELSE":
            parent, taken, _ = stack[-1]
            active = parent and not taken
        elif line in ("ENDIF", "ENDSELECT"):
            active = stack.pop()[0]
        elif active:
            if line.startswith("RETURN "):
                break
            if line.startswith("PRINTFORML "):
                printed.append(line[11:])
            else:
                raise AssertionError(line)
    return printed


class AnimalEarTextTests(unittest.TestCase):
    def test_no_text_for_missing_trait_invalid_target_faint_or_hidden_text(self):
        for values in [{"TALENT:TARGET:124": 0}, {"TARGET": -1}, {"TARGET": 2},
                       {"FLAG:6": 0}, {"TFLAG:899": 1}, {"BASE:TARGET:0": 0},
                       {"CFLAG:TARGET:99": 2}]:
            self.assertEqual(reaction(values), [])

    def test_five_reaction_categories_have_three_variants_each(self):
        contexts = [{"SOURCE:6": 1}, {"SELECTCOM": 312, "TALENT:TARGET:153": 1},
                    {"SELECTCOM": 301}, {"UP:0": 100}, {}]
        results = []
        for context in contexts:
            for variant in range(3):
                lines = reaction(context, variant=variant)
                self.assertEqual(len(lines), 1)
                results.extend(lines)
        self.assertEqual(len(set(results)), 15)

    def test_frequency_gate_and_hurt_reaction_precedence(self):
        for chance in (1, 2):
            self.assertEqual(reaction(chance=chance), [])
        self.assertEqual(reaction({"SOURCE:6": 1, "SELECTCOM": 312, "TALENT:TARGET:153": 1}),
                         reaction({"SOURCE:6": 1}))

    def test_common_hook_and_helper_do_not_change_game_stats(self):
        main = function(source("EVENT_TEXT*"), "TEXT")
        self.assertEqual(main.count("CALL ANIMAL_EAR_REACTION_TEXT"), 1)
        self.assertLess(main.index("RETURN 0\r\nENDIF"), main.index("CALL ANIMAL_EAR_REACTION_TEXT"))
        self.assertNotRegex(BODY, r"(?m)^\s*(?:BASE|ABL|TALENT|CFLAG|TEQUIP|UP):[^\n]*\s(?:=|\+=|-=)")


if __name__ == "__main__":
    unittest.main()
