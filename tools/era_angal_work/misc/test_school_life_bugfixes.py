"""Source-driven regression checks; Emuera UI testing is still separate."""
import re
import unittest

from test_master_ability_purchase import ROOT, source, function, evaluate


def eval_state(expr, state):
    def resolve(match):
        variable, index, field = match.groups()
        number = state[index] if index in state else int(index)
        size = state["CHARANUM"] if field else 1000
        if not 0 <= number < size:
            raise IndexError((variable, number))
        return str(state.get((variable, number, field), 0))
    expr = re.sub(r"\b(CFLAG|LOCAL):([A-Z]+|-?\d+)(?::(\d+))?", resolve, expr)
    return evaluate(expr, state)


def input_path(body, label, state):
    """Run actual input branches until their first action, checking array reads."""
    body = body.split(label, 1)[1]
    stack = []
    active = True
    for raw in body.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.startswith("IF "):
            parent = active
            active = parent and bool(eval_state(line[3:], state))
            stack.append([parent, active])
        elif line.startswith("ELSEIF "):
            parent, taken = stack[-1]
            active = parent and not taken and bool(eval_state(line[7:], state))
            stack[-1][1] |= active
        elif line == "ELSE":
            parent, taken = stack[-1]
            active = parent and not taken
        elif line == "ENDIF":
            active = stack.pop()[0]
        elif active:
            if line.startswith(("RETURN", "GOTO", "RESTART", "REPEAT")):
                return line
            if line.startswith("CFLAG:"):
                return "update"
    raise AssertionError("Unexpected input path")


class SchoolLifeBugfixTests(unittest.TestCase):
    def test_rest_room_invalid_numbers_and_valid_actions(self):
        body = function(source("SHOP_ショップ*"), "KYUUKEIJO")
        state = {"CHARANUM": 4, "MASTER": 0, "ASSI": -1, "TARGET": 1, "LOCAL": 2}
        for choice in (-2, 4, 99, 9999, 9223372036854775807):
            with self.subTest(choice=choice):
                self.assertEqual(input_path(body, "$INPUTLOOPAZUKARI", dict(state, RESULT=choice)),
                                 "GOTO INPUTLOOPAZUKARI")
        for choice in (-1, 100, 1000):
            self.assertEqual(input_path(body, "$INPUTLOOPAZUKARI", dict(state, RESULT=choice)), "RETURN 1")
        self.assertEqual(input_path(body, "$INPUTLOOPAZUKARI", dict(state, RESULT=2)), "update")
        self.assertEqual(input_path(body, "$INPUTLOOPAZUKARI", dict(state, RESULT=200)), "REPEAT CHARANUM")

    def test_accessory_invalid_numbers_and_existing_actions(self):
        body = function(source("ACCESSORY*"), "ACCESSORY_SHOW")
        state = {"CHARANUM": 4, "MASTER": 0, ("LOCAL", 2, None): 1}
        for choice in (-2, 99, 101, 999, 1001, 9223372036854775807):
            self.assertEqual(input_path(body, "$INPUT_LOOP", dict(state, RESULT=choice)), "GOTO INPUT_LOOP")
        self.assertEqual(input_path(body, "$INPUT_LOOP", dict(state, RESULT=2)), "update")
        self.assertEqual(input_path(body, "$INPUT_LOOP", dict(state, RESULT=200)), "update")
        self.assertEqual(input_path(body, "$INPUT_LOOP", dict(state, RESULT=100)), "RETURN 0")

    def test_anzu_is_in_third_page_loop(self):
        body = function(source("SCHOOL_EVENT*"), "SHOW_EVENT_PARTNER_LIST")
        lo, hi = map(int, re.search(r"FOR LOCAL, (\d+), (\d+)", body).groups())
        pages = [[n for n in range(lo, hi) if 25 * page < n <= 25 * (page + 1)]
                 for page in range(3)]
        self.assertEqual(pages[2], list(range(51, 73)))
        self.assertEqual(sum(pages, []), list(range(1, 73)))

    def test_both_date_updates_advance_year_in_january(self):
        for name in ("EVENTSHOP", "YOUBI"):
            body = function(source("DAYS*"), name)
            expr = re.search(r"^DAY:3 = (.+)$", body, re.M)[1].strip()
            years = [evaluate(expr, {"DAY": day, "DAY:4": 2015}) for day in (89, 90, 119, 120, 210)]
            self.assertEqual(years, [2015, 2016, 2016, 2016, 2017])

    def test_recorded_and_legacy_date_years_match(self):
        for name, variable in (("GET_CURRENT_DATE_INT", "DAY"), ("CONVERT_DAY_INT_TO_DATE_INT", "D_VAL")):
            body = function(source("DAYS*"), name)
            expr = re.search(r"^D_YEAR = (.+)$", body, re.M)[1].strip()
            expr = expr.replace("(DAY:4 ? DAY:4 # 2015)", "DAY:4")
            for day, expected in ((89, 2015), (90, 2016), (119, 2016), (120, 2016)):
                numeric_expr = re.sub(r"\b" + variable + r"\b(?!:)", "TESTDAY", expr)
                self.assertEqual(evaluate(numeric_expr, {"TESTDAY": day, "DAY:4": 2015}), expected)
        year = function(source("DAYS*"), "GET_SCHOOL_YEAR")
        expr = re.search(r"RETURNF (.+)", year)[1].strip().replace("(DAY:4 ? DAY:4 # 2015)", "DAY:4")
        self.assertEqual([evaluate(expr, {"DAY": d, "DAY:4": 2015}) for d in (89, 90, 119, 120)],
                         [2015, 2015, 2015, 2016])
        for text in (source("SCHOOL_EVENT*"), function(source("EVENT_BOARD_イベントボード*"), "EVENT_BOARD_STORY_CYCLE_RESET")):
            self.assertNotIn("DAY:3", text)

    def test_old_record_migration_preserves_other_dates(self):
        body = function(source("DAYS*"), "MIGRATE_CALENDAR_DATES")
        condition = re.search(r"IF (LOCAL:1[^\n]+)", body)[1].strip()
        increment = int(re.search(r"CFLAG:COUNT:LOCAL \+= (\d+)", body)[1])
        for date, expected in ((0, 0), (91, 91), (20150101, 20160101),
                               (20150328, 20160328), (20150401, 20150401), (20151228, 20151228)):
            state = {"LOCAL:1": date, "LOCAL:2": date % 10000 // 100}
            self.assertEqual(date + (increment if evaluate(condition, state) else 0), expected)
        self.assertRegex(body, r"SIF FLAG:15098 >= 1\s+RETURN 0")
        self.assertIn("FLAG:15098 = 1", body)

    def test_all_committee_destinations_match_csv(self):
        names = ["体育委員会", "保健委員会", "図書委員会", "緑化委員会", "美化委員会", "選挙管理委員会", "風紀委員会"]
        body = function(source("LOCATION_EVENT*"), "LOCATION_ENCOUNTER")
        body = body.split("ELSEIF TFLAG:86 == 2", 1)[1].split("; 誰もいなかった", 1)[0]
        rooms = re.findall(r"(?:IF|ELSEIF) TFLAG:84 == (\d+)\s*\n(.*?)(?=\tELSEIF|\tENDIF)", body, re.S)
        self.assertEqual(len(rooms), 7)
        for room, content in rooms:
            expected = names[int(room)]
            self.assertIn("── " + expected + " ──", content)
            members = re.findall(r"LOCAL:[1-9] = (\d+)", content)
            for number in members:
                csv = next((ROOT / "CSV").glob("Chara" + number + "_*" )).read_bytes().decode("cp932")
                self.assertEqual(re.search(r"^CSTR,26,(.+)$", csv, re.M)[1].strip(), expected)


if __name__ == "__main__":
    unittest.main()
