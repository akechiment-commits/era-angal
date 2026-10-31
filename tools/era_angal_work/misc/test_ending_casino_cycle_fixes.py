"""Execute the changed ERB paths with scripted input; no Emuera UI or save I/O."""
from collections import defaultdict, deque
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
FILES = ["ENDING_*", "GACHA_*", "CASINO_UNDERGROUND_*", "COMF/COMF390.ERB"]


class ErbPaths:
    """Small source interpreter for these numeric, menu, and reward paths only.

    Display commands have no effect. The destructive stage event and partner
    selection are recorded stubs, so this verifies flow without touching saves.
    Unsupported executed instructions fail instead of silently being skipped.
    """

    def __init__(self, inputs=()):
        self.state = defaultdict(int, MASTER=0, TARGET=1, CHARANUM=4)
        self.inputs = deque(inputs)
        self.calls = []
        self.functions = {}
        self.stubs = {
            "START_PARTNER_SELECT": lambda args: 1,
            "UNDERGROUND_STAGE_PENALTY": lambda args: 1,
        }
        for pattern in FILES:
            source = next((ROOT / "ERB").glob(pattern)).read_bytes().decode("cp932")
            for match in re.finditer(r"^@(\w+)\b[^\n]*\n(.*?)(?=^@|\Z)", source, re.M | re.S):
                lines = [line.split(";", 1)[0].strip() for line in match[2].splitlines()]
                self.functions[match[1]] = [line for line in lines if line]
        self.roster([1, 2, 3])

    def roster(self, numbers):
        self.state["CHARANUM"] = len(numbers) + 1
        for cid, number in enumerate(numbers, 1):
            self.state[f"NO:{cid}"] = number
            self.state[f"TALENT:{cid}:85"] = 1

    def key(self, token, frame):
        name, *indices = token.split(":")
        resolved = [part if part.isdigit() else str(self.get(part, frame)) for part in indices]
        if name in {"CFLAG", "TALENT", "BASE", "MAXBASE"} and len(resolved) == 1:
            resolved.insert(0, str(self.state["TARGET"]))
        return ":".join([name, *resolved])

    def get(self, token, frame):
        key = self.key(token, frame) if ":" in token else token
        name = token.split(":")[0]
        return frame.get(key, 0) if name in frame["_locals"] else self.state[key]

    def put(self, token, value, frame):
        key = self.key(token, frame) if ":" in token else token
        name = token.split(":")[0]
        if name in frame["_locals"]:
            frame[key] = value
        else:
            self.state[key] = value

    def expr(self, expression, frame):
        expression = re.sub(r"IS_UNDERGROUND_PARTNER_BROKEN\(TARGET\)",
                            str(self.state["BROKEN"]), expression)
        expression = re.sub(r"GETCHARA\((\d+)\)", lambda match: str(next(
            (cid for cid in range(self.state["CHARANUM"])
             if self.state[f"NO:{cid}"] == int(match[1])), -1)), expression)
        expression = re.sub(r"\b[A-Z][A-Z_0-9]*(?::[A-Z_0-9]+)*",
                            lambda match: str(self.get(match[0], frame)), expression)
        expression = expression.replace("&&", " and ").replace("||", " or ")
        expression = re.sub(r"!(?!=)", " not ", expression).replace("/", "//")
        return eval(expression, {"__builtins__": {}}, {})

    def run(self, name, args=()):
        self.calls.append((name, tuple(args)))
        if name in self.stubs:
            value = self.stubs[name](args)
            self.state["RESULT"] = value
            return value
        lines = self.functions[name]
        frame = {"_locals": {"ARG", "LOCAL"}, "ARG": args[0] if args else 0,
                 "ARG:1": args[1] if len(args) > 1 else 0}
        labels = {line[1:]: i for i, line in enumerate(lines) if line.startswith("$")}
        branches = []
        loops = []
        active = True
        pc = 0
        for _ in range(100000):
            if pc >= len(lines):
                return self.state["RESULT"]
            line = lines[pc]
            pc += 1
            if line.startswith("IF "):
                parent = active
                active = parent and bool(self.expr(line[3:], frame))
                branches.append([parent, active])
                continue
            if line.startswith("ELSEIF "):
                parent, taken = branches[-1]
                active = parent and not taken and bool(self.expr(line[7:], frame))
                branches[-1][1] |= active
                continue
            if line == "ELSE":
                parent, taken = branches[-1]
                active = parent and not taken
                branches[-1][1] = True
                continue
            if line == "ENDIF":
                active = branches.pop()[0]
                continue
            if not active:
                continue
            if line.startswith("#DIM"):
                variable = re.search(r"#DIM(?: DYNAMIC)? (\w+)", line)[1]
                frame["_locals"].add(variable)
                frame[variable] = 0
            elif line.startswith("SIF "):
                if not self.expr(line[4:], frame):
                    pc += 1
            elif line.startswith("FOR "):
                variable, start, end = [part.strip() for part in line[4:].split(",")]
                lo, hi = self.expr(start, frame), self.expr(end, frame)
                self.put(variable, lo, frame)
                if lo >= hi:
                    depth = 1
                    while depth:
                        following = lines[pc]
                        pc += 1
                        depth += following.startswith("FOR ")
                        depth -= following == "NEXT"
                else:
                    loops.append((variable, hi, pc))
            elif line == "NEXT":
                variable, end, start = loops[-1]
                self.put(variable, self.get(variable, frame) + 1, frame)
                if self.get(variable, frame) < end:
                    pc = start
                else:
                    loops.pop()
            elif line == "CONTINUE":
                depth = 1
                while depth:
                    following = lines[pc]
                    depth += following.startswith("FOR ")
                    depth -= following == "NEXT"
                    if depth:
                        pc += 1
            elif line.startswith("TRYCALLFORM "):
                # Optional KOJO callbacks do not change the numeric paths modeled here.
                self.calls.append(("TRYCALLFORM", (line[12:].strip(),)))
            elif line.startswith("CALL "):
                callee, *expressions = [part.strip() for part in line[5:].split(",")]
                self.run(callee, tuple(self.expr(part, frame) for part in expressions))
            elif line == "INPUT":
                if not self.inputs:
                    raise AssertionError(f"Unexpected input in {name}")
                self.state["RESULT"] = self.inputs.popleft()
            elif line.startswith("GOTO "):
                pc = labels[line[5:]]
            elif line.startswith("RETURN "):
                value = self.expr(line[7:], frame)
                self.state["RESULT"] = value
                return value
            elif line.startswith(("PRINT", "SETCOLOR", "RESETCOLOR", "DRAWLINE", "WAIT", "$", "VARSET")):
                pass
            elif line.startswith(("LOCALS", "STR:", "TSTR:")):
                pass
            else:
                match = re.fullmatch(r"([A-Z][A-Z_0-9:]*) (=|\+=|-=|\*=|\|=) (.+)", line)
                increment = re.fullmatch(r"([A-Z][A-Z_0-9:]*)\+\+", line)
                if match:
                    variable, op, expression = match.groups()
                    value = self.expr(expression, frame)
                    old = self.get(variable, frame)
                    self.put(variable, {"=": lambda: value, "+=": lambda: old + value,
                                        "-=": lambda: old - value, "*=": lambda: old * value,
                                        "|=": lambda: old | value}[op](), frame)
                elif increment:
                    self.put(increment[1], self.get(increment[1], frame) + 1, frame)
                else:
                    raise AssertionError(f"Unsupported executed instruction in {name}: {line}")
        raise AssertionError(f"Loop did not finish: {name}")


class EndingCasinoCycleFixTests(unittest.TestCase):
    def test_first_replay_and_expanded_harem(self):
        vm = ErbPaths([1, 1, 1])
        vm.roster(list(range(1, 6)))
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual((vm.state["ITEM:96"], vm.state["MONEY"]), (1, 0))
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual(vm.state["ITEM:96"], 1)
        vm.roster(list(range(1, 11)))
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual((vm.state["ITEM:96"], vm.state["MONEY"]), (2, 0))
        self.assertEqual([vm.state[f"CFLAG:{cid}:2"] for cid in range(1, 11)], [0] * 10)

    def test_reward_history_survives_reordering_relationship_loss_and_cycles(self):
        vm = ErbPaths()
        vm.roster(list(range(1, 11)))
        vm.run("HAREM_ENDING_REWARD")
        vm.roster([3, 1, 2, *range(4, 11)])
        vm.state["TALENT:2:85"] = 0
        self.assertEqual(vm.run("HAREM_ENDING_REWARD"), 0)
        vm.state["TALENT:2:85"] = 1
        vm.run("ENDING_NEW_CYCLE")
        self.assertEqual(vm.run("HAREM_ENDING_REWARD"), 0)
        self.assertEqual((vm.state["ITEM:96"], vm.state["MONEY"]), (2, 0))

    def test_legacy_money_reward_does_not_block_new_ticket_milestones(self):
        vm = ErbPaths([1, 1])
        vm.state["FLAG:46"] = 4
        vm.state["FLAG:15088"] = 1
        vm.roster(list(range(1, 11)))
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual((vm.state["ITEM:96"], vm.state["MONEY"]), (2, 0))
        vm.roster(list(range(1, 23)))
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual(vm.state["ITEM:96"], 3)

    def test_both_endings_share_anzu_unlock_and_do_not_relock_existing_anzu(self):
        vm = ErbPaths([1])
        vm.run("EXECUTE_HAREM_ENDING")
        self.assertEqual(vm.state["FLAG:1071"], 2)
        vm.state["FLAG:1071"] = 1
        vm.run("UNLOCK_ENDING_REWARDS")
        self.assertEqual(vm.state["FLAG:1071"], 1)
        self.assertTrue(vm.state["FLAG:28"] & 1)
        source = next((ROOT / "ERB").glob("ENDING_*")).read_bytes().decode("cp932")
        individual = re.search(r"^@EXECUTE_PARTNER_ENDING\b.*?(?=^@)", source, re.M | re.S)[0]
        self.assertIn("CALL UNLOCK_ENDING_REWARDS", individual)

    def test_new_cycle_keeps_stock_and_resumes_next_month(self):
        vm = ErbPaths()
        vm.state.update({"DAY": 359, "FLAG:207": 35, "FLAG:15081": 36,
                         "FLAG:15082": 7, "FLAG:15083": 3, "FLAG:15084": 2, "FLAG:15085": 1})
        vm.run("ENDING_NEW_CYCLE")
        self.assertEqual((vm.state["DAY"], vm.state["FLAG:207"], vm.state["FLAG:15081"]), (0, 0, 1))
        self.assertEqual(vm.state["FLAG:15082"], 7)
        vm.run("TICKET_BUDGET_CHECK")
        self.assertEqual(vm.state["FLAG:15082"], 7)
        vm.state["DAY"] = 10
        vm.run("TICKET_BUDGET_CHECK")
        self.assertEqual([vm.state[f"FLAG:{n}"] for n in range(15082, 15086)], [157, 33, 17, 6])
        self.assertGreater(vm.state["DAY"] // 10, vm.state["FLAG:207"])

    def test_old_rewound_save_rebases_month_markers_without_granting_stock(self):
        vm = ErbPaths()
        vm.state.update({"DAY": 20, "FLAG:207": 35, "FLAG:15081": 36, "FLAG:15082": 7,
                         "FLAG:24": 1, "FLAG:5": 1})
        vm.run("TICKET_BUDGET_CHECK")
        self.assertEqual((vm.state["FLAG:15081"], vm.state["FLAG:15082"]), (3, 7))
        vm.run("ENDING_CHECK")
        self.assertEqual(vm.state["FLAG:207"], 2)

    def test_normal_chips_cash_out_before_both_underground_entries(self):
        vm = ErbPaths()
        vm.state.update(T=100, MONEY=9000)
        vm.run("CASINO_CASH_OUT_FOR_UNDERGROUND")
        self.assertEqual((vm.state["T"], vm.state["MONEY"]), (0, 19000))
        vm.run("CASINO_CASH_OUT_FOR_UNDERGROUND")
        self.assertEqual(vm.state["MONEY"], 19000)
        source = next((ROOT / "ERB").glob("COMF/COMF390.ERB")).read_bytes().decode("cp932")
        self.assertEqual(len(re.findall(r"CALL CASINO_CASH_OUT_FOR_UNDERGROUND\s+CALL UNDERGROUND_CASINO_MAIN", source)), 2)

    def test_bankruptcy_retreat_exits_lobby_with_one_penalty_and_settles_chips(self):
        for inputs, debt in (([0, 1], 3000000), ([4, 0, 1], 1000000)):
            with self.subTest(inputs=inputs):
                vm = ErbPaths(inputs)
                vm.state.update({"CFLAG:0:785": debt, "MONEY": 100000})
                vm.run("UNDERGROUND_CASINO_MAIN")
                penalties = [call for call in vm.calls if call[0] == "UNDERGROUND_STAGE_PENALTY"]
                self.assertEqual(len(penalties), 1)
                self.assertEqual(vm.state["CFLAG:0:785"], debt - 350000)
                self.assertFalse(vm.inputs)

    def test_table_retreat_propagates_to_lobby_and_settlement(self):
        for game in ("VIP_BLACK_JACK", "VIP_DICE_GAME"):
            vm = ErbPaths([0, 1])
            vm.state.update({"CFLAG:0:785": 3000000, "MONEY": 100000})
            self.assertEqual(vm.run(game, (0,)), 35)
            self.assertEqual(vm.state["RESULT:1"], 1)
            self.assertEqual(sum(call[0] == "UNDERGROUND_STAGE_PENALTY" for call in vm.calls), 1)
        for menu in (2, 3):
            vm = ErbPaths([menu])
            def retreat(args):
                vm.state["RESULT:1"] = 1
                return 35
            vm.stubs["VIP_BLACK_JACK" if menu == 2 else "VIP_DICE_GAME"] = retreat
            vm.run("UNDERGROUND_CASINO_MAIN")
            self.assertEqual(vm.state["MONEY"], 350000)
            self.assertFalse(vm.inputs)

    def test_bankruptcy_continue_preserves_chips_and_does_not_request_exit(self):
        vm = ErbPaths([0, 0])
        self.assertEqual(vm.run("UNDERGROUND_BANKRUPTCY_EVENT", (100,)), 135)
        self.assertEqual(vm.state["RESULT:1"], 0)

    def test_explicit_settlement_does_not_offer_another_game_and_cashes_rescue(self):
        vm = ErbPaths([0])
        vm.state["CFLAG:0:785"] = 300000
        vm.run("UNDERGROUND_SETTLEMENT", (0,))
        self.assertEqual((vm.state["CFLAG:0:785"], vm.state["MONEY"]), (0, 50000))
        self.assertEqual(sum(call[0] == "UNDERGROUND_STAGE_PENALTY" for call in vm.calls), 1)
        self.assertFalse(vm.inputs)

    def test_broken_forced_exit_does_not_trigger_penalty_twice(self):
        vm = ErbPaths()
        vm.state.update({"BROKEN": 1, "CFLAG:0:785": 3000000})
        vm.run("UNDERGROUND_CASINO_MAIN")
        self.assertEqual(sum(call[0] == "UNDERGROUND_STAGE_PENALTY" for call in vm.calls), 1)
        self.assertEqual(vm.state["CFLAG:0:785"], 3000000)

    def test_ordinary_table_cancel_clears_stale_exit_request(self):
        for game in ("VIP_BLACK_JACK", "VIP_DICE_GAME"):
            vm = ErbPaths([0])
            vm.state["RESULT:1"] = 1
            self.assertEqual(vm.run(game, (10,)), 10)
            self.assertEqual(vm.state["RESULT:1"], 0)

    def test_changed_game_files_preserve_encoding_and_block_structure(self):
        for pattern in [*(f"ERB/{p}" for p in FILES), "CSV/Flag.csv"]:
            path = next(ROOT.glob(pattern))
            raw = path.read_bytes()
            text = raw.decode("cp932")
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""), path.name)
            lines = [line.split(";", 1)[0].strip() for line in text.splitlines()]
            self.assertEqual(sum(line.startswith("IF ") for line in lines), lines.count("ENDIF"), path.name)


if __name__ == "__main__":
    unittest.main()
