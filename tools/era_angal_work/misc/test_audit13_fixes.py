# -*- coding: utf-8 -*-
"""
Tests for Audit #13 fixes:
1. Category 1: 0 unquoted single-line PRINTFORMW dialogue lines across all 144 CHAR_*.ERB files.
2. Category 2: 0 duplicate SELECTCOM blocks in CHAR_01 and 0 duplicate/contradictory SELECTCOM blocks in CHAR_27.
3. Category 3: Female-only / assistant-partner COM viewpoint and partner gender in CHAR_27, 66, 67.
4. Category 4: COMF203.ERB execution gates, actor references, and @COM_ORDER_203 fixes.
5. Category 5: ABL ladder variable indexes in CALC_EJAC, COMF391, COMF66, COMF68, COMF71, COMF191-195, COMF205, COMF372, COMF380, COMF381.
6. Category 6: @COM_ORDER_* display vs calc consistency in COMF68, COMF360, COMF361, COMF367, COMF370.
"""

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]


def read_erb(path: pathlib.Path) -> str:
    return path.read_bytes().decode("cp932")


class TestAudit13Fixes(unittest.TestCase):
    def test_category1_no_unquoted_spoken_dialogue(self):
        char_dir = ROOT / "ERB" / "CHAR"
        unquoted = []
        for p in char_dir.glob("CHAR_*.ERB"):
            text = read_erb(p)
            in_train_msg = False
            for idx, line in enumerate(text.splitlines(), 1):
                s = line.strip()
                if s.startswith("@"):
                    in_train_msg = s.startswith("@TRAIN_MESSAGE")
                if not in_train_msg and s.startswith("PRINTFORMW "):
                    txt = s[len("PRINTFORMW ") :]
                    if (
                        not txt.startswith("「")
                        and not txt.endswith("」")
                        and not txt.startswith("（")
                        and not txt.endswith("）")
                        and not txt.startswith("◆")
                        and not txt.startswith("%CALLNAME:PLAYER%")
                        and not txt.startswith("%CALLNAME:TARGET%")
                    ):
                        unquoted.append(f"{p.name}:{idx}: {txt}")

        self.assertEqual(
            unquoted,
            [],
            f"Found unquoted spoken dialogue lines: {unquoted[:10]} (total: {len(unquoted)})",
        )

    def test_category2_char01_and_char27_deduplication(self):
        # CHAR_01: Should only have 1 instance of IF SELECTCOM == 280
        t01 = read_erb(ROOT / "ERB" / "CHAR" / "CHAR_01_三善かなえ_COM.ERB")
        self.assertEqual(len(re.findall(r"SELECTCOM == 280\b", t01)), 1)
        self.assertEqual(len(re.findall(r"SELECTCOM == 410\b", t01)), 1)

        # CHAR_27: No contradictory && ASSIPLAY == 0 inside Tsuyuri section
        t27 = read_erb(ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB")
        m_start = t27.find(";=== NATSUNO YURI TSUYURI")
        m_end = t27.find(";=== NATSUNO YURI TSUYURI ALL COMMANDS END ===")
        self.assertNotEqual(m_start, -1)
        self.assertNotEqual(m_end, -1)
        tsuyuri_sec = t27[m_start:m_end]
        self.assertNotIn("&& ASSIPLAY == 0", tsuyuri_sec)

        # Check that duplicate branches (COM300, 307, 318, 320, etc.) are each present exactly once
        self.assertEqual(len(re.findall(r"SELECTCOM == 318\b", tsuyuri_sec)), 1)
        self.assertEqual(len(re.findall(r"SELECTCOM == 300\b", tsuyuri_sec)), 1)
        self.assertEqual(len(re.findall(r"SELECTCOM == 307\b", tsuyuri_sec)), 1)
        self.assertEqual(len(re.findall(r"SELECTCOM == 320\b", tsuyuri_sec)), 1)

    def test_category3_female_partner_kojo(self):
        # CHAR_27 COM60 (助手にキスさせる)
        t27 = read_erb(ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB")
        matches_27 = re.findall(r"IF SELECTCOM == 60\b.*?(?=;--- COM\d|\Z)", t27, re.S)
        self.assertGreaterEqual(len(matches_27), 2)
        com60_27 = matches_27[-1]
        self.assertIn("CALL AITE_YOBI, 27, ASSI", com60_27)
        self.assertIn("%LOCALS%", com60_27)
        self.assertNotIn("男は嫌いなのに", com60_27)

        # CHAR_66 COM61 (クンニ強制) & COM63 (貝あわせ)
        t66 = read_erb(ROOT / "ERB" / "CHAR" / "CHAR_66_曽根セイラ_COM.ERB")
        m66_61 = re.search(r"IF SELECTCOM == 61\b.*?(?=;--- COM\d|\Z)", t66, re.S)
        self.assertIsNotNone(m66_61)
        com61_66 = m66_61.group(0)
        self.assertIn("CALL AITE_YOBI, 66, ASSI", com61_66)
        self.assertIn("%LOCALS%", com61_66)
        self.assertNotIn("転校生くん", com61_66)

        m66_63 = re.search(r"IF SELECTCOM == 63\b.*?(?=;--- COM\d|\Z)", t66, re.S)
        self.assertIsNotNone(m66_63)
        com63_66 = m66_63.group(0)
        self.assertIn("CALL AITE_YOBI, 66, ASSI", com63_66)
        self.assertIn("%LOCALS%", com63_66)
        self.assertNotIn("転校生くん", com63_66)

        # CHAR_67 COM61 (クンニ強制)
        t67 = read_erb(ROOT / "ERB" / "CHAR" / "CHAR_67_日滝ましろ_COM.ERB")
        m67_61 = re.search(r";--- COM61 クンニ ---.*?(?=;--- COM\d|\Z)", t67, re.S)
        self.assertIsNotNone(m67_61)
        com61_67 = m67_61.group(0)
        self.assertIn("CALL AITE_YOBI, 67, ASSI", com61_67)
        self.assertIn("%LOCALS%", com61_67)
        self.assertNotIn("キスだけで、こんなに熱くなるのか", com61_67)

    def test_category4_comf203_fixes(self):
        t203 = read_erb(ROOT / "ERB" / "COMF" / "COMF203.ERB")
        # Execution gate
        self.assertIn("SIF TALENT:PLAYER:122", t203)
        self.assertIn("SIF TALENT:PLAYER:0 == 1", t203)
        self.assertNotIn("SIF TALENT:MASTER:122\t; 【MASTER:[オトコ]】", t203)

        # COM logic
        self.assertIn("SIF TEQUIP:PLAYER:86", t203)
        self.assertIn("SOURCE:11 += SOURCE:11 + (ABL:1 * 350)", t203)
        self.assertIn("EXP:PLAYER:40 += 4", t203)

        # COM_ORDER_203
        self.assertNotIn("15000", t203)
        self.assertIn("TALENT:70\t; 【[快感に素直]】\r\n\t\tPRINT  + \r\n\t\tPRINTS TALENTNAME:70", t203)
        self.assertIn("TALENT:85 && ASSIPLAY == 0\t; 【[恋慕] / 調教者:[主人]】\r\n\t\tPRINT  + \r\n\t\tPRINTS TALENTNAME:85", t203)
        self.assertIn("TALENT:87\t; 【[小悪魔]】\r\n\t\tPRINT  + \r\n\t\tPRINTS TALENTNAME:87\r\n\t\tPRINTV '(,3,')", t203)

    def test_category5_abl_ladder_fixes(self):
        # CALC_EJAC
        t_ejac = read_erb(ROOT / "ERB" / "COMF" / "CALC_EJAC.ERB")
        self.assertIn("MIN(MAX(0, ABL:1), 1000000) * 5 + 125", t_ejac)
        self.assertIn("ELSEIF ABL:PLAYER:8 == 1\t; 【PLAYER:[マゾっ気]Lv==1】", t_ejac)

        # COMF391
        t391 = read_erb(ROOT / "ERB" / "COMF" / "COMF391.ERB")
        self.assertIn("ELSEIF ABL:6 == 3\t; 【[奉仕精神]Lv==3】", t391)

        # COMF66 & 68
        t66 = read_erb(ROOT / "ERB" / "COMF" / "COMF66.ERB")
        t68 = read_erb(ROOT / "ERB" / "COMF" / "COMF68.ERB")
        self.assertIn("SOURCE:5 = SOURCE:5 * (ABL:11 * 3)", t66)
        self.assertIn("SOURCE:5 = SOURCE:5 * (ABL:11 * 3)", t68)

        # COMF71
        t71 = read_erb(ROOT / "ERB" / "COMF" / "COMF71.ERB")
        self.assertIn("SOURCE:1 = 200 + (ABL:4 * 50)", t71)
        self.assertIn("SOURCE:2 = 200 + (ABL:5 * 50)", t71)

        # COMF191..195, 380, 381
        for fn in ["COMF191.ERB", "COMF192.ERB", "COMF193.ERB", "COMF194.ERB", "COMF195.ERB", "COMF380.ERB", "COMF381.ERB"]:
            t = read_erb(ROOT / "ERB" / "COMF" / fn)
            self.assertRegex(t, r"SOURCE:3 = SOURCE:3 \* \(ABL:PLAYER:6 \* 75 \+ 25\)")

        # COMF205
        t205 = read_erb(ROOT / "ERB" / "COMF" / "COMF205.ERB")
        self.assertIn("SOURCE:4 = 375 + (ABL:10 * 25)", t205)

        # COMF372
        t372 = read_erb(ROOT / "ERB" / "COMF" / "COMF372.ERB")
        self.assertIn("SOURCE:3 = 200 + (ABL:5 * 10)", t372)

    def test_category6_com_order_display_fixes(self):
        # COMF68
        t68 = read_erb(ROOT / "ERB" / "COMF" / "COMF68.ERB")
        self.assertIn("IF TALENT:82 && TALENT:MASTER:122\t; 【[男嫌い] / MASTER:[オトコ]】", t68)
        self.assertIn("IF TALENT:MASTER:121\t; 【MASTER:[ふたなり]】", t68)

        # COMF360, 361, 367, 370
        for fn in ["COMF360.ERB", "COMF361.ERB", "COMF367.ERB", "COMF370.ERB"]:
            t = read_erb(ROOT / "ERB" / "COMF" / fn)
            self.assertIn("PRINTS TALENTNAME:151\r\n\t\tPRINTV '(,30,')", t)


if __name__ == "__main__":
    unittest.main()
