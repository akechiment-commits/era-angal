"""Source regression for menu guards and partner-to-assistant actor routing."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import ROOT, source, function
from test_pregnancy_probability import check


def run(body, state):
    state = defaultdict(int, state)

    def key(token):
        parts = token.split(":")
        if parts[0] in ("BASE", "MAXBASE", "CFLAG", "TEQUIP"):
            if len(parts) == 2:
                parts.insert(1, str(state["TARGET"]))
            parts[1:] = [part if part.isdigit() else str(state[part]) for part in parts[1:]]
        return ":".join(parts)

    def expr(text):
        names = {"MIN": "min", "MAX": "max", "LIMIT": "limit"}
        text = re.sub(r"\b[A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*",
                      lambda m: names.get(m[0], str(state[key(m[0])])), text)
        text = text.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        return eval(text, {"__builtins__": {}, "min": min, "max": max,
                          "limit": lambda n, low, high: min(max(n, low), high)})

    active, frames, skip = True, [], False
    for raw in body.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith(("#", "PRINT", "CALL ")):
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not (active and expr(line[4:]))
        elif line.startswith("IF "):
            frames.append([active, False])
            active = active and bool(expr(line[3:]))
            frames[-1][1] = active
        elif line.startswith("ELSEIF "):
            parent, taken = frames[-1]
            active = parent and not taken and bool(expr(line[7:]))
            frames[-1][1] |= active
        elif line == "ELSE":
            parent, taken = frames[-1]
            active = parent and not taken
        elif line == "ENDIF":
            active = frames.pop()[0]
        elif active:
            if line.startswith("RETURN "):
                return state
            match = re.fullmatch(r"([A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*) (=|\+=|\|=) (.+)", line)
            if not match:
                raise AssertionError(line)
            target, value = key(match[1]), expr(match[3])
            if match[2] == "+=":
                value += state[target]
            elif match[2] == "|=":
                value |= state[target]
            state[target] = value
    return state


class Audit4FixTests(unittest.TestCase):
    def test_menu_rejects_negative_and_large_values_before_array_access(self):
        for filename, name, array in [("COMF310.ERB", "SOZAI_SHOP", "TSTR:RESULT"),
                                     ("COMF391.ERB", "CLOTHES_SHOP", "T:RESULT")]:
            text = (ROOT / "ERB/COMF" / filename).read_bytes().decode("cp932")
            body = function(text, name)
            selection = body[body.index("$INPUT_LOOP\r\n"):]
            self.assertLess(selection.index("RESULT < 0 || RESULT > 100"), selection.index(array))
            guard = re.search(r"ELSEIF (RESULT < 0 \|\| RESULT > 100)", selection)[1]
            for value in (-2**63, -501, -1, 101, 2**63-1):
                self.assertTrue(eval(guard.replace("RESULT", str(value)).replace("||", "or")))
            for value in (0, 1, 35, 99):
                self.assertFalse(eval(guard.replace("RESULT", str(value)).replace("||", "or")))
            self.assertLess(selection.index("IF RESULT == 100"), selection.index(guard))

    def test_command_65_uses_partner_gauge_and_default_keeps_trainer(self):
        command = (ROOT / "ERB/COMF/COMF65.ERB").read_bytes().decode("cp932")
        self.assertIn("CALL SAMEN_CHECK, TARGET", command)
        body = function(source("EVENT_SHOOT_射精*"), "SAMEN_CHECK").split("TFLAG:714 =")[0]
        for argument, master_gauge, partner_gauge, expected in [
            (1, 0, 60000, 4), (1, 60000, 0, 0), (-1, 60000, 0, 4), (-1, 0, 60000, 0),
        ]:
            state = run(body, {"ARG": argument, "PLAYER": 0, "CHARANUM": 3,
                               "BASE:0:2": master_gauge, "BASE:1:2": partner_gauge,
                               "MAXBASE:0:2": 10000, "MAXBASE:1:2": 10000})
            self.assertEqual(state["TFLAG:302"], expected)
            self.assertEqual(state["BASE:0:2"], master_gauge)
            self.assertEqual(state["BASE:1:2"], partner_gauge)

    def test_partner_condom_is_checked_on_actual_shooter(self):
        body = function(source("EVENT_SHOOT_N*"), "CONDOM_CHECK")
        for wearer, expected in [(0, 0), (1, 1), (2, 0)]:
            state = run(body, {"P": 1, "MASTER": 0, "ASSI": 2, f"TEQUIP:{wearer}:85": 1})
            self.assertEqual(state["CFLAG:0:105"], expected)
            self.assertEqual(state["CFLAG:0:107"], 4 if expected else 0)

    def test_direct_partner_shot_records_assistant_and_correct_father(self):
        body = function(source("EVENT_SHOOT_N*"), "IN_VAGINA_CHECK")
        block = body.split("ELSEIF TFLAG:703 == 8", 1)[1].split(";3P", 1)[0]
        block = block[block.index("IF TFLAG:302"):]
        state = run(block, {"ASSI": 2, "TFLAG:302": 4})
        self.assertEqual(state["CFLAG:2:103"], 4)
        self.assertEqual(state["CFLAG:2:101"], 0)
        self.assertEqual(check(state["CFLAG:2:103"], 0, father=3, drug=True)[0], 3)

    def test_later_partner_check_routes_command_65_to_assistant(self):
        body = function(source("EVENT_SHOOT_N*"), "IN_VAGINA_CHECK_T")
        for command, recipient in [(65, 2), (23, 0), (188, 0)]:
            state = run(body, {"FLAG:62": 1, "E": 4, "SELECTCOM": command,
                               "PLAYER": 0, "ASSI": 2, "CHARANUM": 3})
            self.assertEqual(state[f"CFLAG:{recipient}:103"], 4)
            other = 0 if recipient == 2 else 2
            self.assertEqual(state[f"CFLAG:{other}:103"], 0)

    def test_assistant_pregnancy_reads_partner_father_slot(self):
        body = function(source("EVENT_N_妊娠*"), "IN_VAGINA_T_TO_A")
        self.assertIn("T = ASSI", body)
        self.assertIn("P = 3", body)
        child = function(source("EVENT_N_妊娠*"), "GET_CHILD_T_TO_A")
        self.assertIn("CFLAG:ASSI:104 == 3", child)
        self.assertIn("CALL PREGNANCY_FEEL, ASSI, TARGET, 0", child)


if __name__ == "__main__":
    unittest.main()
