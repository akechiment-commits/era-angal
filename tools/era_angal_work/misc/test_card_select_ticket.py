"""Source-driven menu/claim tests using the real 1884-card data table."""
from pathlib import Path
import re
import unittest

from test_ending_casino_cycle_fixes import ErbPaths, ROOT


def read(pattern):
    return next(ROOT.glob(pattern)).read_bytes().decode("cp932").replace("\r\n", "\n")


def card_data():
    source = read("ERB/CARD_DATA_*")
    source = re.search(r"^@CARD_GET_DATA\b.*?(?=^@|\Z)", source, re.M | re.S)[0]
    cards = {}
    for match in re.finditer(r"^CASE (\d+)\s*\n(.*?)(?=^CASE |^ENDSELECT)", source, re.M | re.S):
        values = {int(index): int(value) for index, value in re.findall(r"RESULT:(\d+) = (\d+)", match[2])}
        title = re.search(r"^\s*STR:0 = (.*)$", match[2], re.M)[1].strip()
        cards[int(match[1])] = (values, title)
    assert len(cards) == 1884
    return cards


CARDS = card_data()


class SelectPaths(ErbPaths):
    def __init__(self, inputs=()):
        super().__init__(inputs)
        self.data = CARDS.copy()
        self.default_character = int(re.search(
            r"@CARD_SELECT_TICKET_IS_MISSING, ARG, ARG:1 = (-?\d+)",
            read("ERB/CARD_SELECT_TICKET_*"))[1])
        for match in re.finditer(r"^@(\w+)\b[^\n]*\n(.*?)(?=^@|\Z)", read("ERB/CARD_SELECT_TICKET_*"), re.M | re.S):
            lines = [line.split(";", 1)[0].strip() for line in match[2].splitlines()]
            self.functions[match[1]] = [line for line in lines if line]
        self.stubs["CARD_GET_DATA"] = self.get_card
        # Existing acquisition and recalc are integration boundaries; all new
        # selection, ownership guards, confirmation, and deductions execute ERB.
        self.stubs["GACHA_ACQUIRE_CARD"] = self.acquire
        self.stubs["CARD_RECALC_BONUSES"] = lambda args: 0

    def run(self, name, args=()):
        if name == "CARD_SELECT_TICKET_IS_MISSING" and len(args) == 1:
            args = (*args, self.default_character)
        return super().run(name, args)

    def get_card(self, args):
        values, title = self.data.get(args[0], ({}, ""))
        for index in range(1, 5):
            self.state[f"RESULT:{index}"] = values.get(index, 0)
        self.state["STR:0"] = title
        return int(bool(values))

    def acquire(self, args):
        self.state[f"FLAG:{3000 + args[0]}"] += 1
        return 1


class CardSelectTicketTests(unittest.TestCase):
    def test_menu_entry_and_ticket_are_registered_and_not_for_sale(self):
        gacha = read("ERB/GACHA_*")
        self.assertIn("[7] カードセレクトチケット使用（所持{ITEM:96}枚）", gacha)
        self.assertRegex(gacha, r"CASE 7\s+CALL CARD_SELECT_TICKET_USE")
        self.assertRegex(read("CSV/Item.csv"), r"(?m)^96,カードセレクトチケット,0,")
        self.assertIn("ITEMSALES:96 = 0", read("ERB/SHOP_ITEM_*"))

    def test_no_ticket_never_opens_selection(self):
        vm = SelectPaths()
        self.assertEqual(vm.run("CARD_SELECT_TICKET_USE"), 0)
        self.assertFalse(any(name == "CARD_SELECT_TICKET_CHARACTER" for name, _ in vm.calls))

    def test_character_then_card_then_confirm_consumes_one(self):
        vm = SelectPaths([1, 1, 1])
        vm.state["ITEM:96"] = 2
        first = min(cid for cid, (values, _) in CARDS.items() if values[1] == 1)
        before_target, before_count = vm.state["TARGET"], vm.state["CHARANUM"]
        self.assertEqual(vm.run("CARD_SELECT_TICKET_USE"), 1)
        self.assertEqual(vm.state["ITEM:96"], 1)
        self.assertEqual(vm.state[f"FLAG:{3000 + first}"], 1)
        self.assertIn(("GACHA_ACQUIRE_CARD", (first,)), vm.calls)
        self.assertIn(("CARD_RECALC_BONUSES", ()), vm.calls)
        self.assertEqual((vm.state["TARGET"], vm.state["CHARANUM"]), (before_target, before_count))
        self.assertFalse(vm.inputs)

    def test_second_use_excludes_the_card_just_obtained(self):
        vm = SelectPaths([1, 1, 1, 1, 1, 1])
        vm.state["ITEM:96"] = 2
        vm.run("CARD_SELECT_TICKET_USE")
        vm.run("CARD_SELECT_TICKET_USE")
        claims = [args[0] for name, args in vm.calls if name == "GACHA_ACQUIRE_CARD"]
        self.assertEqual(len(set(claims)), 2)
        self.assertEqual(vm.state["ITEM:96"], 0)

    def test_cancel_at_character_card_or_confirmation_does_not_consume(self):
        for inputs in ([0], [1, 0, 0], [1, 1, 0, 0, 0]):
            with self.subTest(inputs=inputs):
                vm = SelectPaths(inputs)
                vm.state["ITEM:96"] = 1
                self.assertEqual(vm.run("CARD_SELECT_TICKET_USE"), 0)
                self.assertEqual(vm.state["ITEM:96"], 1)
                self.assertFalse(any(name == "GACHA_ACQUIRE_CARD" for name, _ in vm.calls))
                self.assertFalse(vm.inputs)

    def test_character_pagination_covers_all_data_characters(self):
        characters = sorted({values[1] for values, _ in CARDS.values() if values[1] > 0})
        for inputs, index in (([1], 0), ([17, 1], 15), ([19, 11], 70), ([17, 18, 1], 0), ([16, 1], 0)):
            with self.subTest(inputs=inputs):
                vm = SelectPaths(inputs)
                self.assertEqual(vm.run("CARD_SELECT_TICKET_CHARACTER"), characters[index])

    def test_invalid_character_input_and_last_page_empty_rows_are_rejected(self):
        vm = SelectPaths([-1, 999, 9223372036854775807, 19, 15, 11])
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CHARACTER"), 71)
        self.assertFalse(vm.inputs)

    def test_completed_character_is_not_listed(self):
        vm = SelectPaths([1])
        for cid, (values, _) in CARDS.items():
            if values[1] == 1:
                vm.state[f"FLAG:{3000 + cid}"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CHARACTER"), 2)

    def test_complete_collection_keeps_ticket_and_asks_for_no_input(self):
        vm = SelectPaths()
        vm.state["ITEM:96"] = 1
        for cid, (values, _) in CARDS.items():
            if values[1] > 0:
                vm.state[f"FLAG:{3000 + cid}"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_USE"), 0)
        self.assertEqual(vm.state["ITEM:96"], 1)
        self.assertEqual(vm.state["FLAG:3299"], 0)

    def test_group_cards_use_individual_character_versions_and_reject_legacy_originals(self):
        # The original group row is not in normal gacha pools. Its expanded
        # versions belong to the members and are selected under those members.
        group = sorted(cid for cid, (values, _) in CARDS.items() if values[1] == 0)
        self.assertEqual(len(group), 42)
        for card in group:
            vm = SelectPaths()
            vm.state["ITEM:96"] = 1
            self.assertEqual(vm.run("CARD_SELECT_TICKET_CLAIM", (card,)), 0)
            self.assertEqual(vm.state["ITEM:96"], 1)
            self.assertEqual(vm.state[f"FLAG:{3000 + card}"], 0)
        vm = SelectPaths([19, 12, 11])
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CHARACTER"), 71)
        vm = SelectPaths()
        vm.state["ITEM:96"] = 1
        self.assertEqual(CARDS[1749][0][1], 61)
        self.assertEqual(vm.run("CARD_SELECT_TICKET_IS_MISSING", (1749, 61)), 1)
        self.assertEqual(vm.run("CARD_SELECT_TICKET_IS_MISSING", (1749, 48)), 0)
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CLAIM", (1749,)), 1)
        self.assertEqual(vm.state["FLAG:4749"], 1)
        self.assertEqual(vm.state["ITEM:96"], 0)

    def test_card_pagination_and_owned_filter(self):
        pool = sorted(cid for cid, (values, _) in CARDS.items() if values[1] == 1)
        last_page_first = (len(pool) - 1) // 15 * 15
        for inputs, expected in (([1], pool[0]), ([17, 1], pool[15]), ([19, 1], pool[last_page_first]),
                                 ([17, 16, 1], pool[0]), ([16, 1], pool[0])):
            with self.subTest(inputs=inputs):
                vm = SelectPaths(inputs)
                self.assertEqual(vm.run("CARD_SELECT_TICKET_CARD", (1,)), expected)
        vm = SelectPaths([1])
        vm.state[f"FLAG:{3000 + pool[0]}"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CARD", (1,)), pool[1])

    def test_invalid_card_and_confirm_input_cannot_consume(self):
        vm = SelectPaths([-1, 999, 9223372036854775807, 0])
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CARD", (1,)), 0)
        vm = SelectPaths([1, 1, -1, 999, 0, 0, 0])
        vm.state["ITEM:96"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_USE"), 0)
        self.assertEqual(vm.state["ITEM:96"], 1)

    def test_character_with_no_missing_cards_returns_without_consumption(self):
        vm = SelectPaths()
        vm.state["ITEM:96"] = 1
        for cid, (values, _) in CARDS.items():
            if values[1] == 1:
                vm.state[f"FLAG:{3000 + cid}"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CARD", (1,)), 0)
        self.assertEqual(vm.state["ITEM:96"], 1)

    def test_claim_revalidates_ticket_card_and_ownership(self):
        for card, tickets, owned in ((0, 1, 0), (-1, 1, 0), (1885, 1, 0),
                                      (9223372036854775807, 1, 0), (1, 0, 0), (1, 1, 1)):
            with self.subTest(card=card, tickets=tickets, owned=owned):
                vm = SelectPaths()
                vm.state["ITEM:96"] = tickets
                if 1 <= card <= 1884:
                    vm.state[f"FLAG:{3000 + card}"] = owned
                self.assertEqual(vm.run("CARD_SELECT_TICKET_CLAIM", (card,)), 0)
                self.assertEqual(vm.state["ITEM:96"], tickets)
                self.assertFalse(any(name == "GACHA_ACQUIRE_CARD" for name, _ in vm.calls))

    def test_every_rarity_and_event_card_are_eligible(self):
        for rarity in range(1, 7):
            card = next(cid for cid, (values, _) in CARDS.items() if values[2] == rarity and values[1] > 0)
            vm = SelectPaths()
            self.assertEqual(vm.run("CARD_SELECT_TICKET_IS_MISSING", (card,)), 1)
        # Last registered card is an event card, and stays eligible outside its event month.
        vm = SelectPaths()
        vm.state["ITEM:96"] = 1
        self.assertEqual(vm.run("CARD_SELECT_TICKET_CLAIM", (1884,)), 1)

    def test_character_mismatch_or_invalid_metadata_cannot_be_claimed(self):
        vm = SelectPaths()
        self.assertEqual(vm.run("CARD_SELECT_TICKET_IS_MISSING", (1, 72)), 0)
        for char, rarity in ((0, 1), (-1, 1), (200, 1), (7, 0), (7, 7)):
            vm = SelectPaths()
            vm.data[1] = ({1: char, 2: rarity}, "invalid")
            vm.state["ITEM:96"] = 1
            self.assertEqual(vm.run("CARD_SELECT_TICKET_CLAIM", (1,)), 0)
            self.assertEqual(vm.state["ITEM:96"], 1)

    def test_eligible_cards_exactly_match_existing_character_gacha_pools(self):
        source = read("ERB/CARD_DATA_*")
        pool_source = re.search(r"^@CARD_GET_CHARPOOL\b.*?(?=^@|\Z)", source, re.M | re.S)[0]
        pools = set(map(int, re.findall(r"^\s*GLOBAL:21(?:0[1-9]|[1-9]\d) = (\d+)", pool_source, re.M)))
        assigned = {card for card, (values, _) in CARDS.items() if values[1] > 0}
        self.assertEqual(len(assigned), 1842)
        self.assertEqual(assigned, pools)
        self.assertNotIn("集合・その他", read("ERB/CARD_SELECT_TICKET_*"))

    def test_milestone_boundaries_and_jump_rewards(self):
        for count, tickets in ((3, 0), (4, 0), (5, 1), (9, 1), (10, 2), (19, 2),
                               (20, 3), (30, 4), (70, 8), (72, 8)):
            with self.subTest(count=count):
                vm = SelectPaths()
                vm.roster(list(range(1, count + 1)))
                self.assertEqual(vm.run("HAREM_ENDING_REWARD"), tickets)
                self.assertEqual(vm.state["ITEM:96"], tickets)
                self.assertEqual(vm.run("HAREM_ENDING_REWARD"), 0)
                self.assertEqual(vm.state["ITEM:96"], tickets)

    def test_game_files_are_cp932_crlf_and_ticket_function_names_are_unique(self):
        for pattern in ("ERB/CARD_SELECT_TICKET_*", "ERB/GACHA_*", "ERB/ENDING_*", "ERB/SHOP_ITEM_*", "CSV/Item.csv", "CSV/Flag.csv"):
            path = next(ROOT.glob(pattern))
            raw = path.read_bytes()
            raw.decode("cp932")
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""), path.name)
        declarations = re.findall(r"^@(CARD_SELECT_TICKET_\w+)\b", read("ERB/CARD_SELECT_TICKET_*"), re.M)
        self.assertEqual(len(declarations), len(set(declarations)))


if __name__ == "__main__":
    unittest.main()
