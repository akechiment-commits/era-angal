#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean fix for STAGE.ERB: remove orphaned code + replace @STAGE_CAPTURE."""
import re

with open('ERB/STAGE.ERB', 'rb') as f:
    text = f.read().decode('cp932')
lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')

# State of file (0-indexed):
#   0-5:  comment header
#   6-62: orphaned @STAGE_CAPTURE body (no label) → DELETE
#   63+:  @GET_SEMESTER_NAME, then @STAGE_CAPTURE (old), then rest

header   = lines[:6]           # keep comment header
from_gsn = lines[63:]          # from @GET_SEMESTER_NAME onwards (no orphaned code)
lines    = header + from_gsn
text     = '\n'.join(lines)

# Now replace the old @STAGE_CAPTURE with the correct 3-category menu
new_capture = """\n@STAGE_CAPTURE
DRAWLINE
CALL GET_SEMESTER_NAME

;残り日数計算
LOCAL:0 = FLAG:24
IF FLAG:5 == 0
\tLOCAL:0 *= 15
ELSEIF FLAG:5 == 1
\tLOCAL:0 *= 10
ELSEIF FLAG:5 == 2
\tLOCAL:0 *= 8
ELSE
\tLOCAL:0 *= 5
ENDIF
LOCAL:1 = LOCAL:0 - DAY
SIF LOCAL:1 < 0
\tLOCAL:1 = 0

PRINTFORML 【どこへ行く？】
PRINTFORML 現在学期: %STR:10%
IF FLAG:27 == 0
\tPRINTFORML 試験フェーズ: 前半（中間試験待ち）　残り{LOCAL:1}日
ELSE
\tPRINTFORML 試験フェーズ: 後半（期末試験待ち）　残り{LOCAL:1}日
ENDIF
PRINTL
PRINTFORML [0] 教室へ行く（各クラスを訪問）
PRINTFORML [1] 部室へ行く（各部活の部室を訪問）
PRINTFORML [2] 委員会室へ行く（各委員会を訪問）
PRINTFORML [9] 戻る
PRINTL

$INPUT_LOOP
INPUT
IF RESULT == 0
\tCALL LOCATION_SUBMENU_CLASS
\tSIF RESULT
\t\tBEGIN TURNEND
\tRETURN 1
ELSEIF RESULT == 1
\tCALL LOCATION_SUBMENU_CLUB
\tSIF RESULT
\t\tBEGIN TURNEND
\tRETURN 1
ELSEIF RESULT == 2
\tCALL LOCATION_SUBMENU_COMMITTEE
\tSIF RESULT
\t\tBEGIN TURNEND
\tRETURN 1
ELSEIF RESULT == 9
\tRETURN 0
ELSE
\tGOTO INPUT_LOOP
ENDIF
RETURN 0

"""

# Find and replace old @STAGE_CAPTURE
pos = text.find('\n@STAGE_CAPTURE\n')
if pos == -1:
    print("ERROR: @STAGE_CAPTURE not found!")
else:
    # Find next @function after it
    next_func = re.search(r'\n@[A-Z_]', text[pos+1:])
    end_pos = pos + 1 + next_func.start() if next_func else len(text)
    text = text[:pos] + new_capture + text[end_pos:]
    print(f"Replaced @STAGE_CAPTURE (pos {pos}, end {end_pos})")

# Fix CSTR:TARGET:25 != '' (missing closing quote in string comparison)
count = len(re.findall(r'IF CSTR:TARGET:25 != \s*\n', text))
text = re.sub(r'IF CSTR:TARGET:25 != \s*\n', 'IF CSTR:TARGET:25 != ""\n', text)
print(f"Fixed {count} CSTR:TARGET:25 comparison(s)")

# Write back
text = text.replace('\n', '\r\n')
with open('ERB/STAGE.ERB', 'wb') as f:
    f.write(text.encode('cp932'))
print("STAGE.ERB written.")
