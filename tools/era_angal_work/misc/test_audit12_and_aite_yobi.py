# -*- coding: utf-8 -*-
"""Regression tests for Audit #12 (CLUB_ACTIVITY skill cap preservation & INIT_CLUB_FLAGS)
and @AITE_YOBI / Kojo %LOCALS%, top-level RETURN reachability, & syntax integrity across all 144 character files.
"""
import glob
import os
import re
import unittest

from test_audit4_fixes import ROOT, function, run, source


def _strip_ui_cmds(body: str) -> str:
    out = []
    for line in body.splitlines():
        if line.strip().startswith(("DRAWLINE", "WAIT", "PRINT", "TRYCALLFORM")):
            continue
        code = line.split(";", 1)[0]
        code = (
            code.replace("ABL:MASTER:", "ABL:0:")
            .replace("ABL:TARGET:", "ABL:1:")
            .replace("EXP:MASTER:", "EXP:0:")
            .replace("EXP:TARGET:", "EXP:1:")
        )
        m = re.match(r"^(\s*)([A-Z][A-Z0-9_]*(?::[A-Z0-9]+)*)\s*-=\s*(.+)$", code)
        if m:
            code = f"{m.group(1)}{m.group(2)} = {m.group(2)} - ({m.group(3).strip()})"
        out.append(code)
    return "\n".join(out)


class TestAudit12ClubActivity(unittest.TestCase):
    def setUp(self):
        self.text = source("CLUB_ACTIVITY_部活動システム.ERB")

    def test_no_raw_above_100_overwrite_on_abl(self):
        """Ensure SIF ABL:... > 100 / ABL:... = 100 is no longer used to overwrite ABL > 100."""
        self.assertIsNone(re.search(r"SIF\s+ABL:(MASTER|TARGET):\d+\s*>\s*100", self.text))

    def test_do_activity_preserves_cooking_skill_above_100(self):
        """@DO_ACTIVITY (生活系活動 ARG=4) must not reduce ABL:90 >= 100 down to 100."""
        body = _strip_ui_cmds(function(self.text, "DO_ACTIVITY"))
        body_no_rand = re.sub(r"\bRAND:\d+", "0", body)
        st = run(
            body_no_rand,
            {
                "TFLAG:82": 4,
                "MASTER": 0,
                "TARGET": 1,
                "ABL:0:50": 50,
                "ABL:1:50": 50,
                "ABL:0:90": 300,
                "ABL:1:90": 200,
                "MAXBASE:0:0": 1000,
                "BASE:0:0": 1000,
                "MAXBASE:1:0": 1000,
                "BASE:1:0": 1000,
                "EXP:0:90": 10,
                "EXP:1:90": 10,
            },
        )
        self.assertEqual(st["ABL:0:90"], 300)
        self.assertEqual(st["ABL:1:90"], 200)
        self.assertEqual(st["BASE:0:0"], 875)
        self.assertEqual(st["EXP:0:90"], 14)

    def test_do_activity_increments_cooking_skill_below_100_up_to_100(self):
        """@DO_ACTIVITY increases ABL:90 when < 100, capping the club gain at 100."""
        body = _strip_ui_cmds(function(self.text, "DO_ACTIVITY"))
        body_no_rand = re.sub(r"\bRAND:\d+", "0", body)
        st = run(
            body_no_rand,
            {
                "TFLAG:82": 4,
                "MASTER": 0,
                "TARGET": 1,
                "ABL:0:50": 50,
                "ABL:1:50": 50,
                "ABL:0:90": 99,
                "ABL:1:90": 50,
                "MAXBASE:0:0": 1000,
                "BASE:0:0": 1000,
                "MAXBASE:1:0": 1000,
                "BASE:1:0": 1000,
            },
        )
        self.assertEqual(st["ABL:0:90"], 100)
        self.assertGreater(st["ABL:1:90"], 50)
        self.assertLessEqual(st["ABL:1:90"], 100)

    def test_activity_random_event_preserves_cooking_skill_above_100(self):
        """@ACTIVITY_RANDOM_EVENT (生活系活動 ARG=4) preserves ABL:90 >= 100 across all random outcomes."""
        body = _strip_ui_cmds(function(self.text, "ACTIVITY_RANDOM_EVENT"))
        for r_val in (0, 20, 50, 80):
            body_fixed_rand = re.sub(r"\bRAND:100\b", str(r_val), re.sub(r"\bRAND:\d+", "2", body))
            st = run(
                body_fixed_rand,
                {
                    "TFLAG:82": 4,
                    "MASTER": 0,
                    "TARGET": 1,
                    "ABL:0:90": 350,
                    "ABL:1:90": 250,
                    "ABL:0:50": 120,
                    "ABL:1:50": 120,
                },
            )
            self.assertEqual(st["ABL:0:90"], 350)
            self.assertEqual(st["ABL:1:90"], 250)
            self.assertEqual(st["ABL:0:50"], 120)
            self.assertEqual(st["ABL:1:50"], 120)

    def test_init_club_flags_uses_if_endif_for_break(self):
        """@INIT_CLUB_FLAGS must use IF ... BREAK ... ENDIF rather than SIF + 2 lines."""
        body = function(self.text, "INIT_CLUB_FLAGS")
        self.assertIn("IF CFLAG:COUNT:25 > 0", body)
        self.assertNotIn("SIF CFLAG:COUNT:25 > 0", body)


class TestAiteYobiAndKojoIntegrity(unittest.TestCase):
    def test_aite_yobi_slot_and_no_resolution(self):
        """@AITE_YOBI must guard AI_SLOT bounds, resolve NO:AI_SLOT into AI, and index NAME/CALLNAME by AI_SLOT."""
        text = source("AITE_YOBI_相手呼称.ERB")
        self.assertIn("#DIM AI_SLOT", text)
        self.assertIn("AI_SLOT = ARG:1", text)
        self.assertIn("SIF AI_SLOT < 0 || AI_SLOT >= CHARANUM", text)
        self.assertIn("AI = NO:AI_SLOT", text)
        self.assertIn('SUR \'= REPLACE(NAME:AI_SLOT, CALLNAME:AI_SLOT, "")', text)
        self.assertIn("GET_CHARA_GRADE(AI)", text)
        self.assertNotIn("%CALLNAME:AI%", text)
        self.assertIn("%CALLNAME:AI_SLOT%", text)

    def test_all_kojo_com_locals_and_reachability(self):
        """Every CHAR_[0-9]*_COM.ERB block using %LOCALS% must call AITE_YOBI with ASSI, have all core @CHAR_* functions, and 0 unreachable code after top-level RETURN."""
        com_files = sorted(glob.glob(str(ROOT / "ERB/CHAR/CHAR_[0-9]*_COM.ERB")))
        self.assertEqual(len(com_files), 72)

        for path in com_files:
            m_cid = re.search(r"CHAR_(\d+)_", os.path.basename(path))
            cid = int(m_cid.group(1))
            with open(path, "rb") as f:
                raw = f.read()
            text = raw.decode("cp932")
            lines = text.split("\r\n")

            funcs = set(re.findall(r"^@[A-Za-z0-9_]+", text, re.MULTILINE))
            for req_fn in (
                f"@KOJO_MESSAGE_COM_{cid}",
                f"@CHAR_VIRGIN_{cid}",
                f"@CHAR_FIRST_KISS_{cid}",
                f"@CHAR_UNDRESS_{cid}",
                f"@CHAR_EJAC_{cid}",
                f"@CHAR_EJAC_MOUTH_{cid}",
                f"@CHAR_EJAC_IN_{cid}",
                f"@CHAR_ORGASM_{cid}",
            ):
                self.assertIn(req_fn, funcs, f"{os.path.basename(path)} missing {req_fn}")

            # Verify no top-level RETURN has code following it before next @function
            depth = 0
            prev_sif = False
            for idx, line in enumerate(lines):
                s = line.split(";", 1)[0].strip()
                if not s:
                    continue
                if s.startswith("@"):
                    depth = 0
                    prev_sif = False
                    continue
                if prev_sif:
                    prev_sif = False
                    continue
                if s.startswith("SIF "):
                    prev_sif = True
                    continue
                if re.match(r"^IF\b", s):
                    depth += 1
                elif re.match(r"^ENDIF\b", s):
                    depth = max(0, depth - 1)
                elif re.match(r"^RETURN\b", s) and depth == 0:
                    rem = [x.split(";", 1)[0].strip() for x in lines[idx + 1 :]]
                    next_code = next((x for x in rem if x), "")
                    self.assertTrue(
                        not next_code or next_code.startswith("@"),
                        f"{os.path.basename(path)} L{idx+1}: unreachable code after top-level RETURN: {next_code}",
                    )

            blocks = []
            cur_start = None
            for idx, line in enumerate(lines):
                if re.match(r"^\s*IF\s+SELECTCOM\s*==", line):
                    if cur_start is not None:
                        blocks.append((cur_start, idx))
                    cur_start = idx
                elif (line.startswith("@") or line.strip() == "RETURN 0") and cur_start is not None:
                    blocks.append((cur_start, idx))
                    cur_start = None
            if cur_start is not None:
                blocks.append((cur_start, len(lines)))

            for b_start, b_end in blocks:
                code_lines = [
                    l.split(";", 1)[0]
                    for l in lines[b_start:b_end]
                    if not l.lstrip().startswith(";")
                ]
                block_code = "\n".join(code_lines)
                uses_locals = "%LOCALS%" in block_code
                has_assi_call = bool(
                    re.search(rf"CALL\s+AITE_YOBI\s*,\s*{cid}\s*,\s*ASSI\b", block_code)
                )
                self.assertEqual(
                    uses_locals,
                    has_assi_call,
                    f"{os.path.basename(path)} L{b_start+1}: uses_locals={uses_locals} != has_assi_call={has_assi_call}",
                )


if __name__ == "__main__":
    unittest.main()
