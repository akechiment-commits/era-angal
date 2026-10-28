"""Verify retired skills cannot affect or consume resources in current play."""
import re
import unittest

from test_master_ability_purchase import ROOT, source, function, run_menu


class ExpressionUnificationTests(unittest.TestCase):
    def test_old_skill_or_aptitude_reads_only_exist_in_save_migration(self):
        pattern = r"\bABL:(?:\w+:)?(?:51|52|91|92)\b"
        for path in (ROOT / "ERB").rglob("*.ERB"):
            text = path.read_bytes().decode("cp932")
            for line in text.splitlines():
                code = line.split(";", 1)[0]
                if re.search(pattern, code):
                    self.assertEqual(path.name, "CLUB_SYSTEM_部活管理データ.ERB")
                    self.assertIn("ABL:COUNT:94 = MAX(ABL:COUNT:94, ABL:COUNT:91, ABL:COUNT:92)", code)

    def test_manual_menus_have_no_old_skill_choices(self):
        for m_sense in (False, True):
            sort = function(source("NEW_PRINT_XXX_J*"), "ABL_SORT_M" if m_sense else "ABL_SORT")
            entries = [(int(i), int(value)) for i, value in re.findall(r"^X:(\d+) = (\d+)", sort, re.M)]
            self.assertEqual([i for i, _ in entries], list(range(len(entries))))
            self.assertNotIn(91, [v for _, v in entries])
            self.assertNotIn(92, [v for _, v in entries])
            self.assertEqual(run_menu(2, m_sense)[0], "purchase")
        self.assertIn("SIF ARG == 91 || ARG == 92", function(source("SHOP_ショップ*"), "ABLUP_MASTER_MONEY"))

    def test_retired_individual_and_bulk_upgrades_do_not_spend_resources(self):
        for number in (91, 92):
            text = (ROOT / f"ERB/ABL/ABLUP{number}.ERB").read_bytes().decode("cp932")
            self.assertEqual(function(text, f"ABLUP{number}MAIN").split("RETURN 0")[0].strip(), "")
            self.assertIn("Z = 0", function(text, f"ISABLUP{number}"))
            self.assertNotIn("JUEL:", text)
        auto = source("ABL/ABL_AUTO.ERB")
        self.assertNotIn("CALL AUT_KASHOU_0", auto)
        self.assertNotIn("CALL AUT_SATUEI_0", auto)
        for name in ("AUT_KASHOU_0", "AUT_SATUEI_0"):
            self.assertEqual(function(auto, name).strip(), "RETURN 0")
        shop = source("SHOP_ITEM*")
        self.assertNotIn("ITEMSALES:61 = 1", shop)
        self.assertNotIn("@ABL91_CHECK", shop)

    def test_culture_bonus_uses_expression_at_existing_thresholds(self):
        text = source("SCHOOL_EVENT*")
        body = function(text, "GET_CULTURE_PERFORMANCE_BONUS")
        expression = re.search(r"^LOCAL = (.+)$", body, re.M)[1].strip()
        for value, expected in ((0, 0), (10, 5), (39, 19), (40, 20), (100, 20)):
            actual = eval(expression.replace("ABL:ARG:94", str(value)).replace("/", "//"),
                          {"__builtins__": {}, "MIN": min})
            self.assertEqual(actual, expected)
        self.assertIn("EXP:ARG:93", body)
        self.assertNotIn("GET_CULTURE_SINGING_BONUS", text)

    def test_recording_and_karaoke_effects_use_expression(self):
        video = function(source("SELLVIDEO_ビデオ販売*"), "SELLVIDEO_EXP_RATE")
        self.assertIn("P *= LIMIT(ABL:MASTER:94, 1, 5)", video)
        self.assertIn("P *= LIMIT(ABL:ASSI:94, 1, 5)", video)
        self.assertIn("P *= LIMIT(ABL:MASTER:94 / 5, 1, 5)", video)
        karaoke = source("COMF/COMF323.ERB")
        self.assertIn("EXP:93 += ABL:94 / 5 + 1", karaoke)

    def test_legacy_progress_merges_once_without_double_counting(self):
        body = function(source("CLUB_SYSTEM*"), "SYNC_CLUB_ABL")
        self.assertIn("IF FLAG:15086 == 0", body)
        self.assertIn("FLAG:15086 = 1", body)
        expression = re.search(r"ABL:COUNT:94 = (MAX[^\n]+)", body)[1].strip()
        for values, expected in (((10, 10, 10), 10), ((10, 11, 12), 12), ((20, 10, 5), 20)):
            expr = expression
            for number, value in zip((94, 91, 92), values):
                expr = expr.replace(f"ABL:COUNT:{number}", str(value))
            self.assertEqual(eval(expr, {"__builtins__": {}, "MAX": max}), expected)


if __name__ == "__main__":
    unittest.main()
