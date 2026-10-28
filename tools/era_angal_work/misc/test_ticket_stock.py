"""Run stock and purchase arithmetic from the actual ERB source."""
import re
import unittest
from collections import defaultdict

from test_master_ability_purchase import source, function, evaluate


def run(name, values):
    state = defaultdict(int, values)
    active = True
    frames = []
    skip_next = False

    def expression(expr):
        expr = re.sub(r"FLAG:\(([^()]+)\)",
                      lambda m: "FLAG:" + str(evaluate(m[1], state)), expr)
        return evaluate(expr, state)

    for raw in function(source("GACHA*"), name).splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        if skip_next:
            skip_next = False
            continue
        if line.startswith("SIF "):
            skip_next = not (active and expression(line[4:]))
        elif line.startswith("IF "):
            parent = active
            active = parent and bool(expression(line[3:]))
            frames.append([parent, active, None])
        elif line.startswith("ELSEIF "):
            parent, taken, _ = frames[-1]
            active = parent and not taken and bool(expression(line[7:]))
            frames[-1][1] |= active
        elif line == "ELSE":
            parent, taken, _ = frames[-1]
            active = parent and not taken
        elif line.startswith("SELECTCASE "):
            frames.append([active, False, expression(line[11:]) if active else None])
            active = False
        elif line.startswith("CASE "):
            parent, taken, selected = frames[-1]
            active = parent and not taken and selected in [int(n) for n in line[5:].split(",")]
            frames[-1][1] |= active
        elif line in ("ENDIF", "ENDSELECT"):
            active = frames.pop()[0]
        elif active:
            if line.startswith("RETURN "):
                return expression(line[7:]), dict(state)
            if line.startswith(("PRINT", "LOCALS =")):
                continue
            match = re.fullmatch(r"(MONEY|LOCAL:\d+|FLAG:\d+|FLAG:\([^()]+\)) (\+=|-=|=) (.+)", line)
            if match:
                key = re.sub(r"FLAG:\(([^()]+)\)",
                             lambda m: "FLAG:" + str(evaluate(m[1], state)), match[1])
                value = expression(match[3])
                if match[2] == "+=":
                    state[key] += value
                elif match[2] == "-=":
                    state[key] -= value
                else:
                    state[key] = value
            else:
                raise AssertionError("Unsupported statement: " + line)
    raise AssertionError("Missing return")


class TicketStockTests(unittest.TestCase):
    def test_old_save_starts_with_base_stock_and_ignores_global(self):
        _, state = run("TICKET_BUDGET_CHECK", {"DAY": 40, "GLOBAL:232": 99, "GLOBAL:233": 999999})
        self.assertEqual([state[f"FLAG:{i}"] for i in range(15081, 15086)], [5, 150, 30, 15, 5])

    def test_same_month_preserves_marker_and_rewind_rebases_without_replenishing(self):
        values = {"DAY": 40, "FLAG:15081": 5, "FLAG:15082": 12,
                  "FLAG:15083": 3, "FLAG:15084": 2, "FLAG:15085": 0}
        for day in (40, 49, 20, 40):
            _, state = run("TICKET_BUDGET_CHECK", dict(values, DAY=day))
            self.assertEqual([state[f"FLAG:{i}"] for i in range(15081, 15086)],
                             [day // 10 + 1, 12, 3, 2, 0])

    def test_elapsed_months_add_stock_and_preserve_remainder(self):
        _, state = run("TICKET_BUDGET_CHECK", {"DAY": 70, "FLAG:15081": 5, "FLAG:15082": 12})
        self.assertEqual([state[f"FLAG:{i}"] for i in range(15081, 15086)], [8, 462, 90, 45, 15])

    def test_switching_saves_does_not_change_either_stock(self):
        a = {"DAY": 40, "FLAG:15081": 5, "FLAG:15082": 10}
        b = {"DAY": 20, "FLAG:15081": 3, "FLAG:15082": 20}
        for _ in range(3):
            _, a = run("TICKET_BUDGET_CHECK", a)
            _, b = run("TICKET_BUDGET_CHECK", b)
        self.assertEqual((a["FLAG:15082"], b["FLAG:15082"]), (10, 20))

    def test_all_ticket_types_and_bulk_sizes_charge_exactly(self):
        for kind, price in enumerate((300, 1500, 3000, 10000), 1):
            for qty in (1, 5, 10, 100, 1000):
                result, state = run("TICKET_BUY", {"ARG": kind, "ARG:1": qty,
                    "MONEY": price * qty, f"FLAG:{15081 + kind}": qty,
                    f"FLAG:{15000 + kind}": 7})
                self.assertEqual(result, 1)
                self.assertEqual((state["MONEY"], state[f"FLAG:{15081 + kind}"],
                                  state[f"FLAG:{15000 + kind}"]), (0, 0, qty + 7))

    def test_insufficient_stock_or_money_cannot_change_purchase_values(self):
        for money, stock in ((300000, 99), (29999, 100)):
            result, state = run("TICKET_BUY", {"ARG": 1, "ARG:1": 100,
                                "MONEY": money, "FLAG:15082": stock, "FLAG:15001": 3})
            self.assertEqual(result, 0)
            self.assertEqual((state["MONEY"], state["FLAG:15082"], state["FLAG:15001"]), (money, stock, 3))

    def test_bulk_menu_visibility_and_purchase_routes(self):
        shop = function(source("GACHA*"), "GACHA_TICKET_SHOP")
        for qty, offset in ((100, 20), (1000, 30)):
            for kind in range(1, 5):
                self.assertRegex(shop, rf"SIF FLAG:{15081 + kind} >= {qty}\s+PRINTFORML \[{offset + kind}\]")
            self.assertIn(f"CALL TICKET_BUY, RESULT - {offset}, {qty}", shop)

    def test_ticket_system_no_longer_reads_or_writes_shared_budget(self):
        text = source("GACHA*")
        self.assertNotRegex(text, r"GLOBAL:23[2-6]\b")
        for name in ("GACHA_TICKET_SHOP", "TICKET_BUY", "TICKET_BUDGET_CHECK"):
            self.assertNotIn("SAVEGLOBAL", function(text, name))


if __name__ == "__main__":
    unittest.main()
