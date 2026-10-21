"""Source regression for config bounds, Mike's trait and temporary cats."""
import re
import unittest

from test_master_ability_purchase import ROOT, source, function
from test_audit4_fixes import run


class Audit6FixTests(unittest.TestCase):
    def test_general_config_bounds_precede_indexed_access(self):
        body = function(source("CONFIG_設定画面*"), "SET_CONFIGURE")
        guard = re.search(r"ELSEIF (RESULT < 0 \|\| RESULT > 100)", body)[1]
        self.assertLess(body.index(guard), body.index("ELSEIF LOCAL:RESULT"))
        for number in (-2**63, -1, 101, 2**63-1):
            self.assertTrue(eval(guard.replace("RESULT", str(number)).replace("||", "or")))
        for number in (0, 23, 90, 99):
            self.assertFalse(eval(guard.replace("RESULT", str(number)).replace("||", "or")))

    def test_filter_character_bounds_precede_character_access(self):
        body = function(source("CONFIG_設定画面*"), "SHOW_CHARA_LIST_COM_FILTERING")
        selection = body[body.index("$INPUTLOOP"):]
        guard = "RESULT < 0 || RESULT >= CHARANUM"
        self.assertLess(selection.index(guard), selection.index("CFLAG:RESULT:別れ"))
        self.assertLess(selection.index("RESULT == 301"), selection.index(guard))
        for number in (-1, 3, 1000):
            self.assertTrue(eval(guard.replace("RESULT", str(number)).replace("CHARANUM", "3").replace("||", "or")))

    def test_mike_initial_trait_removed_and_old_save_migrates_only_once(self):
        csv = (ROOT / "CSV/Chara19_猫塚みけ.csv").read_bytes().decode("cp932")
        self.assertNotRegex(csv, r"(?m)^素質,54\s*$")
        body = function(source("TREASURE*"), "MIGRATE_MIKE_CAT_TONGUE")
        self.assertIn("SIF FLAG:15087", body)
        self.assertIn("FLAG:15087 = 1", body)
        condition = re.search(r"IF (NO:COUNT == 19 .+)", body)[1]
        for char_no, temporary, should_remove in [(19, 0, True), (19, 16384, False), (20, 0, False)]:
            resolved = condition.replace("NO:COUNT", str(char_no)).replace("TEQUIP:COUNT:40", str(temporary))
            self.assertEqual(bool(eval(resolved.replace("1p14", "16384").replace("&&", "and"))), should_remove)
        self.assertIn("CALL MIGRATE_MIKE_CAT_TONGUE", function(source("SHOP_ショップ*"), "SHOW_SHOP"))
        flags = (ROOT / "CSV/Flag.csv").read_bytes().decode("cp932")
        self.assertEqual(len(re.findall(r"^15087,", flags, re.M)), 1)

    def test_cat_elixirs_mark_only_newly_granted_traits_for_removal(self):
        body = function(source("TREASURE*"), "USE_TREASURE_ITEM")
        for result, traits in [(25, (54,)), (30, (54, 124, 215))]:
            block = body.split(f"ELSEIF RESULT == {result}", 1)[1]
            block = block.split("ELSEIF RESULT ==", 1)[0]
            for trait in traits:
                grant = re.search(rf"IF TALENT:{trait} == 0\s+(TEQUIP:40 \|= .+?)\s+TALENT:{trait} = 1\s+ENDIF", block)
                self.assertIsNotNone(grant)
                statement = grant[0].replace("1p14", "16384").replace("1p16", "65536")
                for original in (0, 1):
                    state = run(statement, {f"TALENT:{trait}": original})
                    self.assertEqual(state[f"TALENT:{trait}"], 1)
                    self.assertEqual(bool(state["TEQUIP:0:40"]), original == 0)


if __name__ == "__main__":
    unittest.main()
