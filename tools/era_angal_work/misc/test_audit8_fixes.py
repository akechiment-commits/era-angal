"""Regression for potion guards, numeric temporary bust changes, and coin input."""
import re
import unittest
from test_master_ability_purchase import ROOT, source, function
from test_audit4_fixes import run

INFO = source("INFO*")
def expanded(name):
    text = function(INFO, name).replace("\r\n", "\n")
    text = re.sub(r"(?m)^RETURN\s*$", "", text)
    text = text.replace("LOCAL = BUST_TENTHS(C)", "LOCAL = CFLAG:C:1101")
    text = text.replace("BUST_TENTHS(C)", "CFLAG:C:1101")
    text = text.replace("HEIGHT_CM(C)", "HEIGHT")
    text = text.replace("TOINT(SUBSTRING(CSTR:C:22, 0, 3))", "HEIGHT")
    text = text.replace("TALENT:C:", "TALENT:0:")
    text = text.replace("TEQUIP:C:40 -= (TEQUIP:C:40 & 7)", "TEQUIP:C:40 += -(TEQUIP:C:40 & 7)")
    for helper in ("TEMP_BUST_CATEGORY", "TEMP_BUST_ADJUST", "BUST_ADJUST", "SYNC_BUST_TALENT"):
        pattern = rf"(?m)^([ \t]*)CALL {helper}, C(?:, (.+))?$"
        def inline(match):
            initial = "D = " + match[2] + "\n" if match[2] is not None else ""
            return initial + expanded(helper)
        text = re.sub(pattern, inline, text)
    return text

def apply(name, state, delta=0):
    return run(expanded(name), {"C": 0, "HEIGHT": 160, **state, "D": delta})

class Audit8FixTests(unittest.TestCase):
    def test_red_potion_no_longer_blocks_commands(self):
        for path, names in [("COMF/COMABLE.ERB", ["COM_ABLE84", "COM_ABLE87", "COM_ABLE88"]),
                            ("COMF/COMF37.ERB", ["COM_ABLE37"]), ("COMF/COMF201.ERB", ["COM_ABLE201"])]:
            for name in names:
                self.assertNotIn("TEQUIP:41", function(source(path), name))
        self.assertIn("IF TEQUIP:41 == 0", function(INFO, "LIFE_LIMIT_MAXBASE"))

    def test_size_change_synchronizes_exclusive_traits_and_restores(self):
        for original, delta in [(800, 80), (850, -100), (920, 80), (1150, 80)]:
            initial = {"CFLAG:0:1101": original}
            changed = apply("TEMP_BUST_ADJUST", initial, delta)
            self.assertEqual(changed["CFLAG:0:1101"], original + delta)
            self.assertEqual(changed["TEQUIP:0:149"], delta)
            self.assertLessEqual(sum(changed[f"TALENT:0:{n}"] for n in (109, 110, 141, 143)), 1)
            restored = apply("RESTORE_TEMP_BUST", changed)
            self.assertEqual(restored["CFLAG:0:1101"], original)
            self.assertEqual(restored["TEQUIP:0:149"], 0)

    def test_record_tracks_actual_clamped_change_and_preserves_later_growth(self):
        for original, delta, expected in [(1880, 100, 20), (620, -100, -20)]:
            changed = apply("TEMP_BUST_ADJUST", {"CFLAG:0:1101": original}, delta)
            self.assertEqual(changed["TEQUIP:0:149"], expected)
            self.assertEqual(apply("RESTORE_TEMP_BUST", changed)["CFLAG:0:1101"], original)
        changed = apply("TEMP_BUST_ADJUST", {"CFLAG:0:1101": 800}, 80)
        grown = apply("BUST_ADJUST", changed, 30)
        restored = apply("RESTORE_TEMP_BUST", grown)
        self.assertEqual(restored["CFLAG:0:1101"], 830)
        self.assertEqual(apply("RESTORE_TEMP_BUST", restored)["CFLAG:0:1101"], 830)

    def test_normalization_and_old_trait_only_save_follow_numeric_size(self):
        normalized = apply("TEMP_BUST_NORMALIZE", {"CFLAG:0:1101": 1000})
        self.assertEqual(normalized["CFLAG:0:1101"], 819)
        self.assertFalse(any(normalized[f"TALENT:0:{n}"] for n in (109, 110, 141, 143)))
        legacy = apply("RESTORE_TEMP_BUST", {"CFLAG:0:1101": 880, "TEQUIP:0:40": 4+64,
                                            "TALENT:0:109": 1, "TALENT:0:110": 1})
        self.assertEqual(legacy["CFLAG:0:1101"], 880)
        self.assertEqual(legacy["TALENT:0:109"], 0)
        self.assertEqual(legacy["TALENT:0:110"], 1)
        self.assertEqual(legacy["TEQUIP:0:40"], 64)

    def test_extracts_guarantee_their_category_at_every_supported_height(self):
        for height in range(55, 251):
            for initial in (600, 1000, 1900):
                for mode, trait in [(-1, 109), (0, None), (1, 110)]:
                    changed = apply("TEMP_BUST_CATEGORY", {"HEIGHT": height, "CFLAG:0:1101": initial}, mode)
                    expected = {n: int(n == trait) for n in (109, 110, 141, 143)}
                    self.assertEqual({n: changed[f"TALENT:0:{n}"] for n in expected}, expected,
                                     (height, initial, mode, changed["CFLAG:0:1101"]))
                    self.assertEqual(apply("RESTORE_TEMP_BUST", changed)["CFLAG:0:1101"], initial)

    def test_live_height_is_used_and_height_changes_resynchronize_bust(self):
        body = expanded("HEIGHT_ADJUST").replace("HEIGHT", "CFLAG:C:1103")
        state = run(body, {"C": 0, "D": 6, "CFLAG:0:1103": 160, "CFLAG:0:1101": 880})
        self.assertEqual(state["CFLAG:0:1103"], 166)
        self.assertEqual(state["TALENT:0:110"], 0)
        for name in ("SYNC_BUST_TALENT", "TEMP_BUST_CATEGORY"):
            actual = function(INFO, name)
            self.assertIn("HEIGHT_CM(C)", actual)
            self.assertNotIn("CSTR:C:22", actual)
        section = source("TREASURE*").split("ELSEIF RESULT >= 19", 1)[1].split("ELSEIF (RESULT == 22", 1)[0]
        self.assertIn("CALL TEMP_BUST_CATEGORY, TARGET, -1", section)
        self.assertIn("CALL TEMP_BUST_CATEGORY, TARGET, 1", section)

    def test_all_breast_drug_paths_and_cleanup_use_shared_size_helpers(self):
        medicine = source("TREASURE*")
        section = medicine.split("ELSEIF RESULT >= 19", 1)[1].split("ELSEIF (RESULT == 22", 1)[0]
        self.assertIn("TEMP_BUST_NORMALIZE", section)
        self.assertIn("TEMP_BUST_CATEGORY", section)
        self.assertNotRegex(section, r"TALENT:(109|110)\s*=")
        for name in ("COM310_179", "COM310_180", "COM310_220"):
            body = function(source("COMF/COMF310.ERB"), name)
            self.assertIn("CALL TEMP_BUST_ADJUST", body)
            self.assertNotRegex(body, r"TALENT:(109|110)\s*=")
        # YU-CTION's auction path was removed; AFTERTRA is the active cleanup route.
        for pattern in ("AFTERTRA*",):
            self.assertIn("CALL RESTORE_TEMP_BUST, TARGET", source(pattern))

    def test_random_and_pregnancy_size_changes_follow_the_same_numeric_system(self):
        random = source("RANDOM_S*")
        for actor in ("TARGET", "MASTER"):
            self.assertIn(f"CALL BUST_ADJUST, {actor}, -(RAND:41 + 60)", random)
            self.assertIn(f"CALL BUST_ADJUST, {actor}, (RAND:41 + 60)", random)
        pregnancy = source("EVENT_N*")
        self.assertNotRegex(pregnancy, r"(?m)^\s*TALENT:[TC]:(109|110)\s*=")
        self.assertIn("CALL BUST_ADJUST, C, -(RAND:51 + 40)", function(pregnancy, "REVERSE_B_SIZE"))

    def test_coin_applies_valid_input_and_caps_training_level(self):
        body = function(source("COMF/COMF310.ERB"), "COM310_219")
        self.assertLess(body.index("!INRANGE(RESULT, 0, A)"), body.index("ABL:1 = RESULT"))
        bound = re.search(r"(?m)^\s*A = MIN[^\n]+", body)[0]
        assignment = "ABL:1 = RESULT"
        for previous, limit in [(0, 1), (10, 11), (9999, 9999), (2**63-1, 9999)]:
            self.assertEqual(run(bound, {"ABL:1": previous})["A"], limit)
            for selected in (0, limit):
                self.assertEqual(run(assignment, {"ABL:1": previous, "RESULT": selected})["ABL:1"], selected)

if __name__ == "__main__":
    unittest.main()
