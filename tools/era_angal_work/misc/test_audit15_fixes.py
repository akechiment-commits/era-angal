# -*- coding: utf-8 -*-
"""
test_audit15_fixes.py

Unit tests for Audit #15 fixes:
- Control flow & SIF scope normalization across 14 ERB files.
- RANDOM_S rename and curiosity/optimism roll fix.
"""

import unittest
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def read_erb(rel_pattern):
    matches = list(ROOT.glob(rel_pattern))
    if not matches:
        raise FileNotFoundError(f"Pattern {rel_pattern} did not match any file")
    with open(matches[0], "r", encoding="cp932", errors="replace") as f:
        return f.read()

class TestAudit15Fixes(unittest.TestCase):
    def test_random_s_personality_roll(self):
        content = read_erb("ERB/*RANDOM_S*.ERB")
        # Ensure curiosity/optimism is wrapped in IF ... ELSEIF ... ENDIF
        pattern = re.compile(
            r'ELSEIF\s+O\s*==\s*5.*?'
            r'P\s*=\s*RAND:3\s*'
            r'IF\s+P\s*==\s*0\s*'
            r'TALENT:23\s*=\s*1\s*'
            r'TALENT:25\s*=\s*0\s*'
            r'ELSEIF\s+P\s*==\s*1\s*'
            r'TALENT:25\s*=\s*1\s*'
            r'TALENT:23\s*=\s*0\s*'
            r'ENDIF',
            re.DOTALL
        )
        self.assertRegex(content, pattern)

    def test_comf392_confession_talents(self):
        content = read_erb("ERB/COMF/COMF392.ERB")
        # Verify 9 talents with TIMES A & TIMES B are in IF...ENDIF
        for talent_num in [10, 22, 28, 35, 36, 80]:
            self.assertIn(f"IF TALENT:{talent_num}", content)
        for talent_num in [11, 32, 34]:
            self.assertIn(f"IF TALENT:{talent_num} == 1", content)
        # Ensure SIF TALENT:10 is gone
        self.assertNotIn("SIF TALENT:10\t", content)

    def test_comf72_breast_size_pain(self):
        content = read_erb("ERB/COMF/COMF72.ERB")
        self.assertIn("IF TALENT:141", content)
        self.assertNotIn("SIF TALENT:141", content)

    def test_comf28_taimen_zawi(self):
        content = read_erb("ERB/COMF/COMF28.ERB")
        self.assertIn("IF TALENT:85\t; 【[恋慕]】", content)
        self.assertNotIn("SIF TALENT:85\t; 【[恋慕]】", content)

    def test_comf110_masturbation(self):
        content = read_erb("ERB/COMF/COMF110.ERB")
        self.assertIn("IF TALENT:80\t; 【[倒錯的]】", content)
        self.assertIn("IF TALENT:21\t; 【[無関心]】", content)
        self.assertNotIn("SIF TALENT:80\t; 【[倒錯的]】", content)
        self.assertNotIn("SIF TALENT:21\t; 【[無関心]】", content)

    def test_self_training_gem(self):
        content = read_erb("ERB/SELF_*.ERB")
        self.assertIn("IF ABL:6 >= 3", content)
        self.assertNotIn("SIF ABL:6 >= 3", content)

    def test_event_morning_semen(self):
        content = read_erb("ERB/*EVENT_MORNING*.ERB")
        self.assertNotIn("SIF TALENT:MASTER:121 || TALENT:MASTER:122", content)
        self.assertEqual(content.count("IF TALENT:MASTER:121 || TALENT:MASTER:122"), 4)

    def test_auto_train_undress(self):
        content = read_erb("ERB/*AUTO_TRAIN*.ERB")
        pattern = re.compile(r'IF\s+TFLAG:44.*?CALL\s+GET_OUT_MOVIE.*?TRYCALLFORM\s+CHAR_UNDRESS_\{NO:TARGET\}.*?ENDIF', re.DOTALL)
        self.assertRegex(content, pattern)

    def test_source_nipple_cap_comment(self):
        content = read_erb("ERB/*SOURCE*.ERB")
        pattern = re.compile(r';ニプルキャップ装着中\r?\n\s*SIF TEQUIP:15')
        self.assertRegex(content, pattern)

    def test_no_blank_line_sif(self):
        for erb_pat in ["ERB/COMF/COMF21.ERB", "ERB/COMF/COMF22.ERB", "ERB/COMF/COMF30.ERB"]:
            content = read_erb(erb_pat)
            pattern = re.compile(r'SIF TALENT:PLAYER:12[12].*?\r?\n\s+BASE:PLAYER:2 \+=')
            self.assertRegex(content, pattern)

    def test_aftertra_variety_track(self):
        content = read_erb("ERB/*AFTERTRA*.ERB")
        self.assertIn("IF SELECTCOM != 7 && FLAG:(16010 + SELECTCOM) == 0", content)
        self.assertNotIn("SIF SELECTCOM != 7 && FLAG:(16010 + SELECTCOM) == 0", content)

if __name__ == "__main__":
    unittest.main()
