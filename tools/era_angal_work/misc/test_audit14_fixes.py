# -*- coding: utf-8 -*-
"""
Tests for Audit #14 fixes:
1. File rename: PASSIVE_パッシブスキル.ERB -> PASSIVE_パートナーターン.ERB
2. Item name index typo in @COM_ORDER: COMF33, COMF38, COMF62, COMF63 use ITEMNAME:26 instead of 21.
3. Daily life expression syntax: DAILY_LIFE uses %CALLNAME:(TOINT(...))% parentheses.
4. Crash prevention: YU-SYS uses TRYCALLFORM KOJO_NEXT_PLAY_{NO:TARGET}.
5. Crash prevention: PASSIVE_パートナーターン uses TRYCALLFORM PASSIVE_MESSAGE_{ARG:1}.
6. Crash prevention: COMMON comments out CALL ATTENDANT.
7. Deprecation documentation: CSV/Talent.csv, CSV/Item.csv, CSV/Mark.csv contain deprecation notes.
"""

import glob
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]


def read_erb(path: pathlib.Path) -> str:
    return path.read_bytes().decode("cp932")


class TestAudit14Fixes(unittest.TestCase):
    def test_passive_renamed_to_partner_turn(self):
        old_file = ROOT / "ERB" / "PASSIVE_パッシブスキル.ERB"
        new_file = ROOT / "ERB" / "PASSIVE_パートナーターン.ERB"
        self.assertFalse(old_file.exists(), "Old PASSIVE file should not exist")
        self.assertTrue(new_file.exists(), "New PASSIVE_パートナーターン.ERB must exist")

    def test_com_order_item_index_fix(self):
        for com in [33, 38, 62, 63]:
            path = ROOT / "ERB" / "COMF" / f"COMF{com}.ERB"
            text = read_erb(path)
            self.assertNotIn("PRINTS ITEMNAME:21", text, f"COMF{com} still has ITEMNAME:21")
            self.assertIn("PRINTS ITEMNAME:26", text, f"COMF{com} missing ITEMNAME:26")

    def test_daily_life_parenthesized_toint(self):
        matches = list(ROOT.glob("ERB/*DAILY_LIFE*.ERB"))
        self.assertTrue(len(matches) > 0)
        text = read_erb(matches[0])
        self.assertNotIn("%CALLNAME:TOINT", text, "DAILY_LIFE still has unparenthesized TOINT")
        self.assertIn("%CALLNAME:(TOINT(LOCALS))%", text)
        self.assertIn("%CALLNAME:(TOINT(LOCALS:0))%", text)

    def test_yu_sys_trycallform_kojo_next_play(self):
        matches = list(ROOT.glob("ERB/*YU-SYS*.ERB"))
        self.assertTrue(len(matches) > 0)
        text = read_erb(matches[0])
        self.assertNotIn("\nCALLFORM KOJO_NEXT_PLAY", text)
        self.assertIn("TRYCALLFORM KOJO_NEXT_PLAY_{NO:TARGET}", text)

    def test_passive_trycallform_message(self):
        path = ROOT / "ERB" / "PASSIVE_パートナーターン.ERB"
        text = read_erb(path)
        self.assertNotIn("\nCALLFORM PASSIVE_MESSAGE_{ARG:1}", text)
        self.assertIn("TRYCALLFORM PASSIVE_MESSAGE_{ARG:1}", text)

    def test_common_commented_out_attendant(self):
        matches = list(ROOT.glob("ERB/*COMMON*.ERB"))
        self.assertTrue(len(matches) > 0)
        text = read_erb(matches[0])
        self.assertNotIn("\nCALL ATTENDANT", text)
        self.assertIn(";CALL ATTENDANT ; 廃止済み", text)

    def test_csv_deprecation_notes(self):
        talent = read_erb(ROOT / "CSV" / "Talent.csv")
        self.assertIn("廃止済み", talent)
        mark = read_erb(ROOT / "CSV" / "Mark.csv")
        self.assertIn("廃止済み", mark)
        item = read_erb(ROOT / "CSV" / "Item.csv")
        self.assertIn("廃止済み", item)


if __name__ == "__main__":
    unittest.main()
