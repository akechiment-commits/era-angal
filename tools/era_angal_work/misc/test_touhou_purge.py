"""Regressions for removal of obsolete character identity rules."""
import re
import unittest
from test_master_ability_purchase import ROOT, source, function
from test_audit4_fixes import run

class TouhouPurgeTests(unittest.TestCase):
    def test_body_configuration_depends_on_traits_not_identity(self):
        body = function(source("COMMON*"), "GET_BASE8")
        self.assertNotIn("NO:", body)
        for small, child, expected in [(0, 0, 1000), (1, 0, 300), (0, 1, 0), (1, 1, 0)]:
            state = run(body.replace(":ARG:", ":0:"), {"ARG": 0, "TALENT:0:100": small, "TALENT:0:149": child})
            self.assertEqual(state["BASE:0:8"], expected)
            self.assertEqual(state["MAXBASE:0:8"], expected)
            self.assertEqual(state["TALENT:0:65"], expected == 0)

    def test_boss_selection_uses_only_real_csvs(self):
        body = function(source("COMMON*"), "GET_BOSS_NO")
        self.assertIn("EXISTCSV LOCAL, 0", body)
        self.assertNotIn("FLAG:3", body)
        self.assertNotIn("666", body)
        self.assertLess(body.index("SIF D == 0"), body.index("RAND:D"))

    def test_rest_commands_and_prayer_have_no_old_character_rules(self):
        for number in [312, 313, 314, 325]:
            body = source(f"COMF/COMF{number}.ERB")
            self.assertNotRegex(body, r"NO:(TARGET|MASTER|PLAYER|ASSI)\s*(?:==|!=)\s*\d+")
        body = source("COMF/COMF325.ERB")
        self.assertNotIn("REIMUSAMA", body)
        self.assertIn("CALL LIFE_LIMIT_MAXBASE", body)
        self.assertIn("BASE:MASTER:4 += A:1", body)
        self.assertIn("ABL:0 * 100", source("COMF/COMF314.ERB"))
        pat = function(source("COMF/COMF312.ERB"), "COM_HEAD_PAT_CORE")
        self.assertIn("CALL GET_DAILY_SUCCESS_RATE", pat)
        self.assertIn("A:1 = RAND:100", pat)
        self.assertIn("STR:0 = 頭を撫でてもらう", pat)

    def test_kotatsu_sleep_branch_is_closed_before_common_effects(self):
        body = function(source("COMF/COMF314.ERB"), "EQUIP_COM314")
        depth = 0
        for raw in body.splitlines():
            line = raw.split(";", 1)[0].strip()
            if line.startswith("IF "):
                depth += 1
            elif line == "ENDIF":
                depth -= 1
                self.assertGreaterEqual(depth, 0)
            elif line.startswith("LOSEBASE:") or line.startswith("SOURCE:18"):
                self.assertEqual(depth, 0)
        self.assertEqual(depth, 0)
        self.assertEqual(body.count("CALL KOTATSU_SLEEP_CHECK"), 1)
        sleep = function(source("COMF/COMF314.ERB"), "KOTATSU_SLEEP_CHECK")
        self.assertEqual(sleep.count("BEGIN AFTERTRAIN"), 1)
        self.assertEqual(sleep.count("CALL SELF_KOJO"), 1)
        self.assertIn("SELECTCOM == 368 || SELECTCOM == 369", sleep)
        self.assertIn("LOSEBASE:0 += 3", body)
        self.assertIn("LOSEBASE:1 -= 60", body)

    def test_selected_date_destination_is_retained(self):
        body = function(source("COMF/COMF323.ERB"), "PARTNER_DATE_PLACE")
        self.assertNotIn("TEQUIP:2 =", body)
        self.assertNotIn("NO:", body)
        self.assertIn("RETURN 1", body)

    def test_unused_transformation_does_not_change_species_or_equipment(self):
        lib = source("ADDIN-FUNC*")
        for name in ["GET_STRAINCORRECT", "GET_STRAINCORR_VALUE"]:
            self.assertNotIn("TEQUIP:L:1", function(lib, name))
        self.assertNotIn("TEQUIP:1", function(source("INFO*"), "SHOW_EQUIP_2"))

    def test_renamed_dynamic_drug_callbacks_and_date_menu_resolve(self):
        all_source = "\n".join(p.read_bytes().decode("cp932") for p in (ROOT / "ERB").rglob("*.ERB"))
        for forbidden in ["HOURAI_KOJO_", "ADD_REIMUSAMA", "GENSOUKYO_DATE", "SEIRENSEN_DATE", "IS_CHIREIDEN", "IS_MYORENJI"]:
            self.assertNotIn(forbidden, all_source)
        self.assertIn("TRYCCALLFORM IMMORTAL_DRUG_KOJO_{NO:TARGET}", all_source)
        for number in range(1, 73):
            self.assertRegex(all_source, rf"(?m)^@IMMORTAL_DRUG_KOJO_{number}\s*$")
        self.assertIn("@SCHOOL_AREA_DATE", all_source)

if __name__ == "__main__":
    unittest.main()
