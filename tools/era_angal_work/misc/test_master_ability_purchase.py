"""Regression checks against the ERB source; does not replace Emuera play testing."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def source(pattern):
    return next((ROOT / "ERB").glob(pattern)).read_bytes().decode("cp932")


def function(text, name):
    return re.search(r"^@" + name + r"\b[^\n]*\n(.*?)(?=^@|\Z)",
                     text, re.M | re.S).group(1)


def evaluate(expression, state):
    def value(match):
        key = match.group()
        if key.startswith("X:"):
            index = state[key[2:]] if key[2:] in state else int(key[2:])
            if not 0 <= index < len(state["X"]):
                raise IndexError(index)
            return str(state["X"][index])
        return str(state[key])

    expression = re.sub(r"[A-Z][A-Z0-9]*(?::[A-Z0-9]+)*", value, expression)
    expression = expression.replace("||", " or ").replace("&&", " and ")
    expression = expression.replace("/", "//")
    return eval(expression, {"__builtins__": {}}, {})


def run_menu(choice, m_sense=False, male=False):
    """Execute selection guards and array reads from the actual menu source."""
    sort = function(source("NEW_PRINT_XXX_J*"), "ABL_SORT_M" if m_sense else "ABL_SORT")
    state = {"RESULT": choice, "TALENT:MASTER:122": int(male), "X": [0] * 1000}
    for line in sort.splitlines():
        match = re.fullmatch(r"\s*(A|X:\d+)\s*=\s*(\d+)\s*", line)
        if match:
            key, number = match.groups()
            if key == "A":
                state["A:0"] = int(number)
            else:
                state["X"][int(key[2:])] = int(number)
    active = True
    taken = False
    for raw in function(source("SHOP_ショップ*"), "ABL_UP_MASTER").splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.startswith("IF "):
            active = bool(evaluate(line[3:], state))
            taken = active
        elif line.startswith("ELSEIF "):
            active = not taken and bool(evaluate(line[7:], state))
            taken |= active
        elif line == "ELSE":
            active = not taken
        elif line == "ENDIF":
            active = True
            taken = False
        elif active:
            if line == "RESTART":
                return "retry", state
            if line.startswith("RETURN "):
                return "exit", state
            if line == "CALL ABLUP_MASTER_MONEY(LOCAL)":
                return "purchase", state
            match = re.fullmatch(r"(LOCAL(?::\d+)?) = (.+)", line)
            if match:
                state[match[1]] = evaluate(match[2], state)
    raise AssertionError("Unexpected menu path")


class MasterAbilityPurchaseTests(unittest.TestCase):
    def test_invalid_input_does_not_read_outside_menu(self):
        for m_sense in (False, True):
            for choice in (-9223372036854775808, -1, 21 if m_sense else 20,
                           99, 101, 999, 1000, 9223372036854775807):
                with self.subTest(m_sense=m_sense, choice=choice):
                    action, _ = run_menu(choice, m_sense)
                    self.assertEqual(action, "retry")

    def test_exit_and_existing_purchases_still_work(self):
        for m_sense in (False, True):
            self.assertEqual(run_menu(100, m_sense)[0], "exit")
            for choice, ability in ((1, 1), (2, 2)):
                action, state = run_menu(choice, m_sense)
                self.assertEqual((action, state["LOCAL"]), ("purchase", ability))

    def test_hidden_academic_choice_is_rejected(self):
        for m_sense in (False, True):
            sort = function(source("NEW_PRINT_XXX_J*"), "ABL_SORT_M" if m_sense else "ABL_SORT")
            choice = int(re.search(r"X:(\d+) = 88", sort)[1])
            for male in (False, True):
                action, state = run_menu(choice, m_sense, male)
                self.assertEqual(state["LOCAL"], 88)
                self.assertEqual(action, "retry")
        display = function(source("SHOP_ショップ*"), "SHOW_ABLUP_SELECT_MASTER")
        self.assertRegex(display, r"SIF [^\n]*LOCAL == 88\s*\n\s*CONTINUE")

    def test_academic_recalculation_ignores_old_purchase_and_decays(self):
        body = function(source("STAGE*"), "CALC_ACADEMIC_LEVEL")
        for experience, expected in ((100, 60), (90, 59), (200, 70)):
            for old_bonus in (0, 1, 500):
                state = {"TARGET": 1, "ARG:0": 0, "ABL:TARGET:88": 999,
                         "ABL:TARGET:98": 50, "EXP:TARGET:95": experience,
                         "CFLAG:TARGET:88": old_bonus}
                for raw in body.splitlines():
                    match = re.fullmatch(r"([A-Z0-9:]+) = (.+)", raw.strip())
                    if match:
                        state[match[1]] = evaluate(match[2], state)
                self.assertEqual(state["ABL:TARGET:88"], expected)
                self.assertEqual(state["CFLAG:TARGET:88"], 0)
                self.assertEqual(state["TARGET"], 1)

    def test_removed_purchase_helpers_have_no_references(self):
        for path in (ROOT / "ERB").rglob("*.ERB"):
            text = path.read_bytes().decode("cp932")
            self.assertNotRegex(text, r"\b(?:ABLUP_MASTER_88|GET_BATTLE_PRICE|BATTLE_PRICE_[IG4])\b")


if __name__ == "__main__":
    unittest.main()
