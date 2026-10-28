"""Execute cycle helpers from the CP932 ERB source; no engine/UI coverage."""
import random
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import ROOT, source, function


CYCLE = source("DANGER_DAY*")


def run(name, state, character=0, fresh=0, seed=1):
    state["ARG"] = character
    state["ARG:1"] = fresh
    rng = random.Random(seed)

    def key(token):
        return re.sub(r":ARG(?=:)", f":{state['ARG']}", token)

    def expr(text):
        text = re.sub(r"\b(?:CFLAG|TALENT):ARG:\d+|\bLOCAL\b|\bARG(?::1)?\b",
                      lambda m: str(state[key(m[0])]), text)
        text = re.sub(r"RAND:(\d+)|RAND:\((\d+)\)",
                      lambda m: str(rng.randrange(int(m[1] or m[2]))), text)
        text = text.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        return eval(text, {"__builtins__": {}, "MAX": max, "MIN": min})

    active, frames, skip = True, [], False
    for raw in function(CYCLE, name).splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line:
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
                return
            match = re.fullmatch(r"(CFLAG:ARG:\d+|TALENT:ARG:\d+|LOCAL) = (.+)", line)
            if not match:
                raise AssertionError("Unsupported statement: " + line)
            state[key(match[1])] = int(expr(match[2]))


def character(length=28, bleeding=5, day=0):
    return defaultdict(int, {"CFLAG:0:1276": length, "CFLAG:0:1277": bleeding,
                             "CFLAG:0:1278": 1, "CFLAG:0:33": day})


class MenstrualCycleTests(unittest.TestCase):
    def test_default_cycle_boundaries(self):
        for day in range(28):
            state = character(day=day)
            run("UPDATE_MENSTRUAL_STATUS", state)
            self.assertEqual(state["TALENT:0:138"], int(day < 5))
            self.assertEqual(state["TALENT:0:137"], int(8 <= day <= 14))

    def test_all_normal_lengths_and_bleeding_durations(self):
        for length in range(21, 36):
            for bleeding in range(2, 8):
                fertile, period = [], []
                for day in range(length):
                    state = character(length, bleeding, day)
                    run("UPDATE_MENSTRUAL_STATUS", state)
                    if state["TALENT:0:137"]:
                        fertile.append(day)
                    if state["TALENT:0:138"]:
                        period.append(day)
                self.assertEqual(period, list(range(bleeding)))
                self.assertEqual(fertile, list(range(length - 20, length - 13)))

    def test_overlap_depends_on_short_cycle_and_long_bleeding(self):
        for length, bleeding, overlap in [(28, 5, False), (21, 7, True), (35, 7, False)]:
            results = []
            for day in range(length):
                state = character(length, bleeding, day)
                run("UPDATE_MENSTRUAL_STATUS", state)
                results.append(bool(state["TALENT:0:137"] and state["TALENT:0:138"]))
            self.assertEqual(any(results), overlap)

    def test_new_character_range_and_individual_variation(self):
        samples = set()
        for seed in range(1000):
            state = defaultdict(int)
            run("INIT_MENSTRUAL_CYCLE", state, fresh=1, seed=seed)
            length, bleeding, day = (state[f"CFLAG:0:{n}"] for n in (1276, 1277, 33))
            self.assertTrue(21 <= length <= 35)
            self.assertTrue(2 <= bleeding <= 7)
            self.assertTrue(0 <= day < length)
            samples.add((length, bleeding, day))
        self.assertGreater(len(samples), 100)

    def test_old_save_migrates_once_without_advancing_on_refresh(self):
        for old_day in range(15):
            state = defaultdict(int, {"CFLAG:0:33": old_day})
            run("INIT_MENSTRUAL_CYCLE", state)
            before = dict(state)
            run("INIT_MENSTRUAL_CYCLE", state, seed=500)
            self.assertEqual(dict(state), before)
            self.assertTrue(0 <= state["CFLAG:0:33"] < state["CFLAG:0:1276"])
            run("UPDATE_MENSTRUAL_STATUS", state)
            if 8 <= old_day <= 11:
                self.assertEqual(state["TALENT:0:138"], 1)
            if 12 <= old_day <= 14:
                self.assertEqual(state["TALENT:0:137"], 1)

    def test_pregnant_and_male_characters_clear_both_states(self):
        for talent in (122, 134):
            state = character(21, 7, 2)
            state[f"TALENT:0:{talent}"] = 1
            state["TALENT:0:137"] = state["TALENT:0:138"] = 1
            run("UPDATE_MENSTRUAL_STATUS", state)
            self.assertEqual(state["CFLAG:0:33"], 0)
            self.assertEqual(state["TALENT:0:137"], 0)
            self.assertEqual(state["TALENT:0:138"], 0)

    def test_daily_advance_matches_three_calendar_days_and_wraps(self):
        daily = function(CYCLE, "EVENT_DANGERDAY")
        amount = int(re.search(r"CFLAG:COUNT:33 \+= (\d+)", daily)[1])
        self.assertEqual(amount, 3)
        self.assertIn("CFLAG:COUNT:33 %= CFLAG:COUNT:1276", daily)
        for length in range(21, 36):
            for day in range(length):
                state = character(length, 5, (day + amount) % length)
                run("UPDATE_MENSTRUAL_STATUS", state)
                self.assertTrue(0 <= state["CFLAG:0:33"] < length)

    def test_refresh_hook_and_memory_reset_preserve_cycle(self):
        refresh = function(CYCLE, "REFRESH_MENSTRUAL_STATUS")
        self.assertNotIn("+=", refresh)
        self.assertIn("CALL REFRESH_MENSTRUAL_STATUS", function(source("SHOP_ショップ*"), "SHOW_SHOP"))
        reset = source("SHOP_ITEM*")
        for index in (33, 1276, 1277, 1278):
            self.assertIn(f"CFLAG:TARGET:{index} = CFLAG:R:{index}", reset)
        definitions = (ROOT / "CSV/Cflag.csv").read_bytes().decode("cp932")
        for index in (1276, 1277, 1278):
            self.assertEqual(len(re.findall(rf"^{index},", definitions, re.M)), 1)


if __name__ == "__main__":
    unittest.main()
