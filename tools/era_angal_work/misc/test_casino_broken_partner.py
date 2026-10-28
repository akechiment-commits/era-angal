# -*- coding: utf-8 -*-
"""
test_casino_broken_partner.py

Unit tests for Underground Casino balance changes:
- Partner at lower limit (MAXBASE:0 <= 300 and MAXBASE:1 <= 300) cannot clear debt via sacrifice.
- Broken partner cannot be used as collateral for special loans (@UNDERGROUND_BORROW) or credit bets.
- In games (Blackjack, Dice), bets are restricted to held chips (BET_MONEY <= ARG * 10000).
- Debt remains intact unless cleared with a fresh partner or paid off with chips/cash.
- A route to break already-broken characters further is preserved via menu [4] (廃棄処分・生贄執行)
  and bankruptcy stage penalties, deepening Phase 5+ collapse without clearing debt or giving free chips.
- Seamless disposal flow: choosing [4] immediately enters the disposal stage without redundant bankruptcy prompts.
- Negative debt overflow self-healing and safeguards.
"""

import unittest
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASINO_FILE = ROOT / "ERB" / "CASINO_UNDERGROUND_裏カジノ.ERB"
SYSTEM_FILE = ROOT / "ERB" / "SYSTEM_基本システム処理.ERB"

class TestCasinoBrokenPartner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CASINO_FILE, "r", encoding="cp932", newline="") as f:
            cls.content = f.read()
        with open(SYSTEM_FILE, "r", encoding="cp932", newline="") as f:
            cls.system_content = f.read()

    def test_file_encoding_and_newlines(self):
        with open(CASINO_FILE, "rb") as f:
            raw = f.read()
        self.assertIn(b"\r\n", raw)
        self.assertEqual(len(raw.replace(b"\r\n", b"").split(b"\n")), 1, "Should not contain bare LF")
        # Ensure it decodes cleanly as CP932
        raw.decode("cp932")

    def test_broken_partner_function_exists(self):
        self.assertIn("@IS_UNDERGROUND_PARTNER_BROKEN", self.content)
        self.assertIn("#FUNCTION", self.content)
        
        # Verify function logic pattern
        pattern = re.compile(
            r"@IS_UNDERGROUND_PARTNER_BROKEN(?:\(ARG\s*=\s*-1\))?[\s\S]*?"
            r"MAXBASE:ARG:0\s*<=\s*300\s*&&\s*MAXBASE:ARG:1\s*<=\s*300[\s\S]*?"
            r"RETURNF\s+1[\s\S]*?RETURNF\s+0",
            re.MULTILINE
        )
        self.assertRegex(self.content, pattern)

    def test_broken_partner_logic_simulation(self):
        def is_broken(hp, mp):
            return 1 if (hp <= 300 and mp <= 300) else 0

        self.assertEqual(is_broken(300, 300), 1)
        self.assertEqual(is_broken(200, 150), 1)
        self.assertEqual(is_broken(301, 300), 0)
        self.assertEqual(is_broken(300, 301), 0)
        self.assertEqual(is_broken(1000, 1000), 0)

    def test_lobby_menu_broken_partner_options(self):
        # [1] Special loan blocked message when broken
        borrow_pattern = re.compile(
            r"@UNDERGROUND_BORROW, ARG[\s\S]*?"
            r"IF\s+IS_UNDERGROUND_PARTNER_BROKEN\(TARGET\)[\s\S]*?"
            r"RETURN\s+ARG",
            re.MULTILINE
        )
        self.assertRegex(self.content, borrow_pattern)

        # [4] Option label when broken
        self.assertIn("【廃棄処分・生贄執行】（壊れきったパートナーを差し出し、さらに徹底的に破壊する）※借金清算なし", self.content)

        # Menu 4 confirmation prompt
        self.assertIn("支配人「おや……？ このお嬢様は既に心身ともに限界まで壊れきっており、当カジノでの担保価値はございませんよ」", self.content)
        self.assertIn("[0] ステージに差し出し、さらに破壊する", self.content)

    def test_disposal_stage_event_dedicated_flow(self):
        # Verify @UNDERGROUND_DISPOSAL_STAGE_EVENT exists
        self.assertIn("@UNDERGROUND_DISPOSAL_STAGE_EVENT, ARG", self.content)

        # Verify that Option 4 calls UNDERGROUND_DISPOSAL_STAGE_EVENT when broken
        opt4_pattern = re.compile(
            r"ELSEIF\s+RESULT\s*==\s*4\s*&&[\s\S]*?IF\s+IS_UNDERGROUND_PARTNER_BROKEN\(TARGET\)[\s\S]*?"
            r"CALL\s+UNDERGROUND_DISPOSAL_STAGE_EVENT,\s*VIP_CHIP",
            re.MULTILINE
        )
        self.assertRegex(self.content, opt4_pattern)

        # Verify UNDERGROUND_DISPOSAL_STAGE_EVENT directly advances stage and calls penalty
        disposal_pattern = re.compile(
            r"@UNDERGROUND_DISPOSAL_STAGE_EVENT,\s*ARG[\s\S]*?"
            r"CALL\s+UNDERGROUND_STAGE_PENALTY,\s*TFLAG:110[\s\S]*?"
            r"RETURN\s+ARG",
            re.MULTILINE
        )
        self.assertRegex(self.content, disposal_pattern)

        # Verify no choices inside UNDERGROUND_DISPOSAL_STAGE_EVENT
        match = re.search(r"@UNDERGROUND_DISPOSAL_STAGE_EVENT, ARG[\s\S]*?RETURN ARG", self.content)
        self.assertIsNotNone(match)
        self.assertNotIn("INPUT", match.group(0))

    def test_bankruptcy_event_no_prompt_when_broken(self):
        # In @UNDERGROUND_BANKRUPTCY_EVENT, when WAS_BROKEN is true, choices are skipped
        bank_pattern = re.compile(
            r"IF\s+WAS_BROKEN[\s\S]*?連行されていく……[\s\S]*?"
            r"ELSE[\s\S]*?"
            r"PRINTL \[0\] パートナーを担保としてステージに差し出す[\s\S]*?"
            r"ENDIF",
            re.MULTILINE
        )
        self.assertRegex(self.content, bank_pattern)

    def test_stage_penalty_debt_retention_when_broken(self):
        # Case 3 (Stage 3): debt cleared only if WAS_BROKEN == 0
        case3_pattern = re.compile(
            r"CASE\s+3\b[\s\S]*?"
            r"IF\s+WAS_BROKEN[\s\S]*?借金（\$\{CFLAG:MASTER:785\}）は帳消しになりませんでした！[\s\S]*?"
            r"ELSE[\s\S]*?"
            r"CFLAG:MASTER:785\s*=\s*0",
            re.MULTILINE
        )
        self.assertRegex(self.content, case3_pattern)

        # Case 4 (Stage 4): debt cleared only if WAS_BROKEN == 0
        case4_pattern = re.compile(
            r"CASE\s+4\b[\s\S]*?"
            r"IF\s+WAS_BROKEN[\s\S]*?借金（\$\{CFLAG:MASTER:785\}）は帳消しになりませんでした！[\s\S]*?"
            r"ELSE[\s\S]*?"
            r"CFLAG:MASTER:785\s*=\s*0",
            re.MULTILINE
        )
        self.assertRegex(self.content, case4_pattern)

        # Case 5 (Phase 5+): debt cleared only if WAS_BROKEN == 0
        case5_pattern = re.compile(
            r"CASE\s+5\b[\s\S]*?"
            r"IF\s+WAS_BROKEN[\s\S]*?借金（\$\{CFLAG:MASTER:785\}）は帳消しになりませんでした！[\s\S]*?"
            r"ELSE[\s\S]*?"
            r"CFLAG:MASTER:785\s*=\s*0",
            re.MULTILINE
        )
        self.assertRegex(self.content, case5_pattern)

    def test_rescue_chips_blocked_when_broken(self):
        # Bankruptcy event does not award chips if WAS_BROKEN
        rescue_pattern = re.compile(
            r"; 既に壊れきったパートナーの場合は救済チップなし[\s\S]*?"
            r"IF\s+WAS_BROKEN[\s\S]*?"
            r"RETURN\s+ARG[\s\S]*?"
            r"RESCUE_CHIP\s*=\s*20\s*\+\s*\(TFLAG:110\s*\*\s*15\)[\s\S]*?"
            r"ARG\s*\+=\s*RESCUE_CHIP",
            re.MULTILINE
        )
        self.assertRegex(self.content, rescue_pattern)

    def test_blackjack_betting_restrictions(self):
        # Broken partner bet limit check in Blackjack
        bj_pattern = re.compile(
            r"IF\s+IS_UNDERGROUND_PARTNER_BROKEN\(TARGET\)\s*&&\s*BET_MONEY\s*>\s*ARG\s*\*\s*10000[\s\S]*?"
            r"手持ち（VIPチップ{ARG}枚）を超えるツケ賭けはできません！[\s\S]*?"
            r"GOTO\s+V_BJ_LOOP",
            re.MULTILINE
        )
        self.assertRegex(self.content, bj_pattern)

        # Option [6] All-in hidden when broken
        self.assertIn("IF !IS_UNDERGROUND_PARTNER_BROKEN(TARGET)\r\n\tPRINTL [6] 全財産オールイン", self.content)

        # Double down chip check
        self.assertIn("IF IS_UNDERGROUND_PARTNER_BROKEN(TARGET)\r\n\t\tIF ARG < BET_MONEY / 10000", self.content)

        # Dealer raise blocked when broken
        self.assertIn("DOUBLE_DOWN == 0 && !IS_UNDERGROUND_PARTNER_BROKEN(TARGET)", self.content)

    def test_dice_betting_restrictions(self):
        # Broken partner bet limit check in Dice
        dice_pattern = re.compile(
            r"IF\s+IS_UNDERGROUND_PARTNER_BROKEN\(TARGET\)\s*&&\s*BET_MONEY\s*>\s*ARG\s*\*\s*10000[\s\S]*?"
            r"手持ち（VIPチップ{ARG}枚）を超えるツケ賭けはできません！[\s\S]*?"
            r"GOTO\s+V_DICE_LOOP",
            re.MULTILINE
        )
        self.assertRegex(self.content, dice_pattern)

        # Arashi penalty does not add debt when broken
        self.assertIn("IF !IS_UNDERGROUND_PARTNER_BROKEN(TARGET)\r\n\t\t\tCFLAG:MASTER:785 += BET_MONEY", self.content)

    def test_negative_debt_self_heal_and_overflow_cap(self):
        # Lobby self-heal
        self.assertIn("; 借金負数・オーバーフローの自己修復", self.content)
        self.assertIn("IF CFLAG:MASTER:785 < 0\r\n\tCFLAG:MASTER:785 = 9000000000000000000\r\nENDIF", self.content)

        # System interest overflow safety
        self.assertIn("64bit整数オーバーフロー防止", self.system_content)
        self.assertIn("ELSEIF CFLAG:MASTER:785 < 0\r\n\tCFLAG:MASTER:785 = 9000000000000000000", self.system_content)

    def test_flow_control_blocks_balanced(self):
        # Verify IF/ENDIF balance
        lines = self.content.splitlines()
        if_count = sum(1 for l in lines if re.match(r"^\s*IF\b", l))
        endif_count = sum(1 for l in lines if re.match(r"^\s*ENDIF\b", l))
        self.assertEqual(if_count, endif_count, f"IF ({if_count}) vs ENDIF ({endif_count}) count mismatch")

        select_count = sum(1 for l in lines if re.match(r"^\s*SELECTCASE\b", l))
        endselect_count = sum(1 for l in lines if re.match(r"^\s*ENDSELECT\b", l))
        self.assertEqual(select_count, endselect_count, f"SELECTCASE ({select_count}) vs ENDSELECT ({endselect_count}) mismatch")

if __name__ == "__main__":
    unittest.main()
