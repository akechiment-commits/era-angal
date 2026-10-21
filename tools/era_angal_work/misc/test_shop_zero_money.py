import unittest
import os
import re

class TestShopZeroMoney(unittest.TestCase):
    def setUp(self):
        self.shop_path = os.path.join("ERB", "SHOP_ショップ.ERB")
        with open(self.shop_path, "r", encoding="cp932", errors="replace") as f:
            self.lines = f.readlines()
        self.content = "".join(self.lines)

    def test_menu_display_100_no_money_check(self):
        """[100] パートナーと過ごす display should NOT require MONEY > 0"""
        for i, line in enumerate(self.lines):
            if "COUNT == 0" in line and "TARGET >= 0" in line:
                self.assertNotIn("MONEY", line, f"Line {i+1} still contains MONEY check: {line}")
                self.assertIn("IF COUNT == 0 && TARGET >= 0", line)

    def test_menu_display_106_no_money_check(self):
        """[106] 休憩 display should NOT require MONEY > 0"""
        for i, line in enumerate(self.lines):
            if "COUNT == 5" in line and "ELSEIF" in line:
                self.assertNotIn("MONEY", line, f"Line {i+1} still contains MONEY check: {line}")
                self.assertIn("ELSEIF COUNT == 5", line)

    def test_input_handler_100_no_money_check(self):
        """RESULT == 100 handler should NOT require MONEY > 0"""
        for i, line in enumerate(self.lines):
            if "RESULT == 100" in line and "TARGET >= 0" in line:
                self.assertNotIn("MONEY", line, f"Line {i+1} still contains MONEY check: {line}")
                self.assertIn("IF RESULT == 100 && TARGET >= 0", line)

    def test_input_handler_106_no_money_check(self):
        """RESULT == 106 handler should NOT require MONEY > 0"""
        for i, line in enumerate(self.lines):
            if "RESULT == 106" in line and "ELSEIF" in line:
                self.assertNotIn("MONEY", line, f"Line {i+1} still contains MONEY check: {line}")
                self.assertIn("ELSEIF RESULT == 106", line)

    def test_no_money_gt_zero_in_shop(self):
        """Verify that MONEY > 0 does not appear anywhere in SHOP_ショップ.ERB"""
        matches = [f"Line {i+1}: {line.strip()}" for i, line in enumerate(self.lines) if "MONEY > 0" in line]
        self.assertEqual(matches, [], f"Found unexpected MONEY > 0 in SHOP_ショップ.ERB: {matches}")

if __name__ == "__main__":
    unittest.main()
