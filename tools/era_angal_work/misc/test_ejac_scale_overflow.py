"""Evaluate actual ERB formulas with checked Int64 intermediates."""
import ast
import re
import unittest
from collections import defaultdict
from test_master_ability_purchase import source, function

TEXT = source("COMF/CALC_EJAC.ERB").replace("\r\n", "\n")
I64 = 2**63-1
CAP = 10**15

def checked(value):
    if isinstance(value, int):
        assert -2**63 <= value <= I64, value
    return value

class Evaluator:
    def __init__(self, state):
        self.state = defaultdict(int, state)
    def key(self, name):
        fields = name.split(":")
        if fields[0] in ("ABL", "BASE", "MAXBASE", "TEQUIP", "CFLAG"):
            if len(fields) == 2:
                fields.insert(1, str(self.state["TARGET"]))
            fields[1:] = [field if field.lstrip("-").isdigit() else str(self.state[field]) for field in fields[1:]]
        elif fields[0] == "RELATION":
            fields[1:] = [field if field.lstrip("-").isdigit() else str(self.state[field]) for field in fields[1:]]
        return ":".join(fields)
    def expr(self, text):
        text = text.replace("TEQUIP:(ARG:1):40", f"TEQUIP:{self.state['ARG:1']}:40")
        text = text.replace("BASE:(ARG:2):2", f"BASE:{self.state['ARG:2']}:2")
        calls = {"MIN": "min", "MAX": "max", "LIMIT": "limit", "EJAC_SCALE": "scale", "COURTESAN_EJAC_GAIN": "gain"}
        text = re.sub(r"\b[A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*", lambda m: calls.get(m[0], str(self.state[self.key(m[0])])), text)
        text = text.replace("&&", " and ").replace("||", " or ")
        def ev(node):
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.UnaryOp): return checked(-ev(node.operand))
            if isinstance(node, ast.BoolOp):
                return all(ev(x) for x in node.values) if isinstance(node.op, ast.And) else any(ev(x) for x in node.values)
            if isinstance(node, ast.Compare):
                x, y, op = ev(node.left), ev(node.comparators[0]), node.ops[0]
                return x == y if isinstance(op, ast.Eq) else x != y if isinstance(op, ast.NotEq) else x > y if isinstance(op, ast.Gt) else x >= y if isinstance(op, ast.GtE) else x < y if isinstance(op, ast.Lt) else x <= y
            if isinstance(node, ast.Call):
                args = [ev(x) for x in node.args]
                if node.func.id == "min": return min(args)
                if node.func.id == "max": return max(args)
                if node.func.id == "limit": return min(max(args[0], args[1]), args[2])
                name = "EJAC_SCALE" if node.func.id == "scale" else "COURTESAN_EJAC_GAIN"
                state = dict(self.state)
                state.update({"ARG" if i == 0 else f"ARG:{i}": n for i, n in enumerate(args)})
                return Evaluator(state).execute(function(TEXT, name))
            if isinstance(node, ast.BinOp):
                x, y = ev(node.left), ev(node.right)
                if isinstance(node.op, ast.Add): result = x + y
                elif isinstance(node.op, ast.Sub): result = x - y
                elif isinstance(node.op, ast.Mult): result = x * y
                elif isinstance(node.op, ast.Mod): result = x % y
                elif isinstance(node.op, ast.BitAnd): result = x & y
                else: result = abs(x)//abs(y) * (-1 if (x < 0) != (y < 0) else 1)
                return checked(result)
            raise AssertionError(ast.dump(node))
        return ev(ast.parse(text, mode="eval").body)
    def execute(self, body):
        active, stack, skip = True, [], False
        for raw in body.splitlines():
            line = raw.split(";", 1)[0].strip()
            if not line or line.startswith("#"): continue
            if skip: skip = False; continue
            if line.startswith("IF "):
                stack.append([active, False]); active = active and bool(self.expr(line[3:])); stack[-1][1] = active
            elif line.startswith("ELSEIF "):
                parent, taken = stack[-1]; active = parent and not taken and bool(self.expr(line[7:])); stack[-1][1] |= active
            elif line == "ELSE":
                parent, taken = stack[-1]; active = parent and not taken
            elif line == "ENDIF": active = stack.pop()[0]
            elif line.startswith("SIF "): skip = not (active and self.expr(line[4:]))
            elif active:
                if line.startswith("RETURNF "): return self.expr(line[8:])
                match = re.fullmatch(r"([A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*) (=|\+=) (.+)", line)
                assert match, line
                name, op, value = match.groups(); key = self.key(name)
                result = self.expr(value)
                self.state[key] = checked(result + self.state[key] if op == "+=" else result)
        return self.state["B"]

def calculate(skill, service, name="CALC_EJAC", command=31, drug=0, all_high=False):
    body = function(TEXT, name)
    head, rest = body.split("SELECTCASE ARG:0", 1)
    cases, tail = rest.split("ENDSELECT", 1)
    match = re.search(rf"(?m)^CASE {command}\s*$", cases)
    assert match, command
    selected = cases[match.end():]
    selected = re.split(r"(?m)^CASE ", selected, 1)[0]
    state = {"TARGET": 0, "PLAYER": 1, "MASTER": 1, "ASSI": 2, "CHARANUM": 3,
             "ARG:0": command, "ARG:1": 1, "ABL:0:2": skill, "ABL:0:6": service,
             "ABL:0:0": 5, "ABL:1:3": 5, "TEQUIP:0:40": drug}
    if all_high:
        for actor in range(3):
            for ability in (0, 1, 2, 3, 4, 6, 11): state[f"ABL:{actor}:{ability}"] = I64
        state.update({"RELATION:0:1": I64, "CFLAG:0:1102": I64, "TFLAG:19": 1})
    return Evaluator(state).execute(head + selected + tail)

class EjacScaleTests(unittest.TestCase):
    def test_scale_matches_exact_arithmetic_without_any_int64_intermediate_overflow(self):
        for value in (0, 1, 333, CAP, I64):
            for numerator in (0, 1, 2, 100, 10**6, I64):
                for denominator in (1, 2, 10, 100, 1000):
                    got = Evaluator({"ARG": value, "ARG:1": numerator, "ARG:2": denominator}).execute(function(TEXT, "EJAC_SCALE"))
                    self.assertEqual(got, min(CAP, value*numerator//denominator))

    def test_normal_case_keeps_existing_result(self):
        self.assertEqual(calculate(10, 10), 33600)
        self.assertEqual(calculate(100, 100), 1586408187)

    def test_reported_high_skill_cases_are_positive_and_saturate(self):
        for name in ("CALC_EJAC", "CALC_EJAC_P"):
            for skill in (9999, 15008):
                self.assertEqual(calculate(skill, 9999, name), CAP)
                self.assertEqual(calculate(skill, 9999, name, drug=4096), CAP*2)

    def test_extreme_inputs_and_final_gauge_addition_are_bounded(self):
        for command in (20, 31):
            self.assertGreater(calculate(I64, I64, command=command, all_high=True), 0)
        for drug in (0, 4096):
            got = Evaluator({"ARG": I64, "ARG:1": 0, "ARG:2": 1, "CHARANUM": 2,
                             "TEQUIP:0:40": drug, "BASE:1:2": I64}).execute(function(TEXT, "COURTESAN_EJAC_GAIN"))
            self.assertEqual(got, 0)

    def test_direct_gain_routes_use_the_same_safe_multiplier(self):
        for path in ("COMF/COMF21.ERB", "COMF/COMF22.ERB", "COMF/COMF30.ERB", "YU-CTION*"):
            text = source(path)
            end = text.index("BASE:PLAYER:2 += COURTESAN_EJAC_GAIN")
            start = text.rfind(";ABL:技巧をみる", 0, end)
            section = text[start:end]
            self.assertIn("EJAC_SCALE(", section)
            self.assertNotRegex(section, r"B = B \*")

if __name__ == "__main__": unittest.main()
