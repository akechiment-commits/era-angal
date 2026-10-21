"""Source-driven checks for completed-action recovery and its hooks."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import ROOT, source, function


BODY = function(source("COUNTERSYSTEM*"), "TRAINER_ENDURANCE_RECOVERY")


def recover(state, trainer=0):
    state["ARG"] = trainer

    def key(token):
        return token.replace(":ARG:", f":{trainer}:")

    def expr(text):
        text = re.sub(r"\b[A-Z][A-Z0-9]*(?::[A-Z0-9]+)*",
                      lambda m: {"MIN": "min", "MAX": "max"}.get(m[0], str(state[key(m[0])])), text)
        text = text.replace("||", " or ").replace("&&", " and ").replace("/", "//")
        return eval(text, {"__builtins__": {}, "min": min, "max": max})

    skip = False
    for raw in BODY.splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith(("#DIM", "PRINT")):
            continue
        if skip:
            skip = False
            continue
        if line.startswith("SIF "):
            skip = not expr(line[4:])
        elif line.startswith("RETURN "):
            return
        else:
            match = re.fullmatch(r"([A-Z][A-Z0-9]*(?::[A-Z0-9]+)*) (=|\+=) (.+)", line)
            if not match:
                raise AssertionError("Unsupported statement: " + line)
            value = expr(match[3])
            target = key(match[1])
            state[target] = state[target] + value if match[2] == "+=" else value


def initial(current=0, maximum=5000, turns=0):
    return defaultdict(int, {"CHARANUM": 3, "BASE:0:4": current,
                             "MAXBASE:0:4": maximum, "TFLAG:111": turns})


class TrainerEnduranceRecoveryTests(unittest.TestCase):
    def test_recovers_only_every_four_completed_actions(self):
        state = initial()
        for turn in range(1, 17):
            recover(state)
            self.assertEqual(state["BASE:0:4"], (turn // 4) * 25)
            self.assertEqual(state["TFLAG:111"], turn % 4)

    def test_zero_endurance_is_recoverable_and_small_maximum_gets_one(self):
        for maximum, expected in [(1, 1), (100, 1), (199, 1), (200, 1), (5000, 25), (10000, 50)]:
            state = initial(maximum=maximum, turns=3)
            recover(state)
            self.assertEqual(state["BASE:0:4"], expected)

    def test_upper_limit_and_existing_overcap_are_preserved(self):
        for current, expected in [(4990, 5000), (5000, 5000), (5100, 5100)]:
            state = initial(current=current, turns=3)
            recover(state)
            self.assertEqual(state["BASE:0:4"], expected)

    def test_invalid_trainer_does_not_count_or_recover(self):
        for trainer in (-1, 3, 100):
            state = initial(turns=3)
            recover(state, trainer)
            self.assertEqual(state["TFLAG:111"], 3)
            self.assertEqual(state["BASE:0:4"], 0)

    def test_recovers_current_trainer_including_assistant(self):
        state = initial(turns=3)
        state["BASE:1:4"], state["MAXBASE:1:4"] = 0, 8000
        recover(state, trainer=1)
        self.assertEqual(state["BASE:1:4"], 40)
        self.assertEqual(state["BASE:0:4"], 0)

    def test_zero_or_invalid_maximum_does_not_recover(self):
        for maximum in (0, -1):
            state = initial(maximum=maximum, turns=3)
            recover(state)
            self.assertEqual(state["BASE:0:4"], 0)

    def test_both_successful_action_paths_hook_after_resource_updates(self):
        for pattern, name in [("SOURCE*", "SOURCE_CHECK"), ("REVMODE*", "REVMODE_SOURCE_CHECK")]:
            body = function(source(pattern), name)
            hook = "CALL TRAINER_ENDURANCE_RECOVERY, PLAYER"
            self.assertEqual(body.count(hook), 1)
            update = re.search(r"^\s*UPCHECK\s*$", body, re.M)
            self.assertIsNotNone(update)
            self.assertGreater(body.index(hook), update.start())
        event = function(source("EVENT_TRAIN*"), "EVENTTRAIN")
        self.assertRegex(event, r"REPEAT 200\s+TFLAG:COUNT = 0\s+REND")
        csv = (ROOT / "CSV/Tflag.csv").read_bytes().decode("cp932")
        self.assertEqual(len(re.findall(r"^111,", csv, re.M)), 1)


if __name__ == "__main__":
    unittest.main()
