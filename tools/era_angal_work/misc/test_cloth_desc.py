# -*- coding: utf-8 -*-
import unittest
import os
import re

class TestClothDesc(unittest.TestCase):
    def setUp(self):
        self.cloth_desc_path = 'ERB/CLOTH_DESC_衣装描写.ERB'
        self.comf391_path = 'ERB/COMF/COMF391.ERB'
        with open(self.cloth_desc_path, 'r', encoding='cp932') as f:
            self.cloth_desc_content = f.read()
        with open(self.comf391_path, 'r', encoding='cp932') as f:
            self.comf391_content = f.read()

    def test_cloth_train_equip_desc_exists(self):
        self.assertIn('@CLOTH_TRAIN_EQUIP_DESC', self.cloth_desc_content)

    def test_comf391_calls_cloth_train_equip_desc(self):
        self.assertIn('CALL CLOTH_TRAIN_EQUIP_DESC(TEQUIP:65)', self.comf391_content)

    def test_all_costumes_handled_in_selectcase(self):
        # Costume IDs from 1 to 35 and 255
        expected_cases = list(range(1, 36)) + [255]
        for cid in expected_cases:
            pattern = rf'CASE\s+{cid}\b'
            self.assertTrue(
                re.search(pattern, self.cloth_desc_content),
                f"Missing CASE {cid} in @CLOTH_TRAIN_EQUIP_DESC"
            )

    def test_school_swimsuit_situations(self):
        # Case 5 (navy) and Case 6 (white) must handle wet, aroused, and normal
        for cid in [5, 6, 32]:
            pattern = rf'CASE\s+{cid}\b[\s\S]*?(?=CASE\s+\d+|CASEELSE|ENDSELECT)'
            match = re.search(pattern, self.cloth_desc_content)
            self.assertIsNotNone(match, f"Could not find case {cid}")
            case_text = match.group(0)
            self.assertIn('IF IS_WET', case_text)
            self.assertIn('ELSEIF IS_AROUSED', case_text)
            self.assertIn('PATTERN == 0', case_text)
            self.assertIn('PATTERN == 1', case_text)

    def test_stain_handlers(self):
        # Stains should be checked before or during selectcase
        self.assertIn('TFLAG:265', self.cloth_desc_content) # 精液
        self.assertIn('TFLAG:264', self.cloth_desc_content) # ローション
        self.assertIn('TFLAG:262', self.cloth_desc_content) # 尿
        self.assertIn('TFLAG:263', self.cloth_desc_content) # 汚物

if __name__ == '__main__':
    unittest.main()
