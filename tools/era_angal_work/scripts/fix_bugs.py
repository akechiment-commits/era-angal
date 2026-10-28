#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix multiple bugs:
1. STAGE.ERB: Remove orphaned code (lines 10-53) before @GET_SEMESTER_NAME
2. STAGE.ERB: Fix @STAGE_CAPTURE to use 3-category menu
3. STAGE.ERB: Fix 'IF CSTR:TARGET:25 != ' (missing "")
4. LOCATION_EVENT.ERB: Fix PARAM:0 -> BASE:0 / MAXBASE:0 in solo event
5. SHOP.ERB: Move PRINT_SHOPITEM to separate shop screen via [120] toggle
"""

import re

# ============================================================
# Fix STAGE.ERB
# ============================================================
def fix_stage():
    with open('ERB/STAGE.ERB', 'rb') as f:
        text = f.read().decode('cp932')

    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    # Find the first @GET_SEMESTER_NAME line
    get_sem_idx = next(i for i, l in enumerate(lines) if l.strip() == '@GET_SEMESTER_NAME')
    # Lines 0..7 are the file header comments (keep them)
    # Lines 8..get_sem_idx-1 are orphaned code (delete them)
    header = lines[:8]
    rest   = lines[get_sem_idx:]
    lines  = header + rest

    text = '\n'.join(lines)

    # Fix @STAGE_CAPTURE: replace simplified 9-item menu with 3-category menu
    # Find the @STAGE_CAPTURE function body and replace it
    old_capture = None
    stage_cap_start = text.find('@STAGE_CAPTURE\n')
    if stage_cap_start == -1:
        stage_cap_start = text.find('@STAGE_CAPTURE\r\n')
    # Find the next @-function after STAGE_CAPTURE to know where it ends
    next_func = re.search(r'\n@[A-Z_]', text[stage_cap_start + 1:])
    if next_func:
        end_pos = stage_cap_start + 1 + next_func.start()
    else:
        end_pos = len(text)
    old_capture = text[stage_cap_start:end_pos]

    new_capture = (
        "@STAGE_CAPTURE\n"
        "DRAWLINE\n"
        "CALL GET_SEMESTER_NAME\n"
        "\n"
        ";残り日数計算\n"
        "LOCAL:0 = FLAG:24\n"
        "IF FLAG:5 == 0\n"
        "\tLOCAL:0 *= 15\n"
        "ELSEIF FLAG:5 == 1\n"
        "\tLOCAL:0 *= 10\n"
        "ELSEIF FLAG:5 == 2\n"
        "\tLOCAL:0 *= 8\n"
        "ELSE\n"
        "\tLOCAL:0 *= 5\n"
        "ENDIF\n"
        "LOCAL:1 = LOCAL:0 - DAY\n"
        "SIF LOCAL:1 < 0\n"
        "\tLOCAL:1 = 0\n"
        "\n"
        "PRINTFORML 【どこへ行く？】\n"
        "PRINTFORML 現在学期: %STR:10%\n"
        "IF FLAG:27 == 0\n"
        "\tPRINTFORML 試験フェーズ: 前半（中間試験待ち）　残り{LOCAL:1}日\n"
        "ELSE\n"
        "\tPRINTFORML 試験フェーズ: 後半（期末試験待ち）　残り{LOCAL:1}日\n"
        "ENDIF\n"
        "PRINTL\n"
        "PRINTFORML [0] 教室へ行く（各クラスを訪問）\n"
        "PRINTFORML [1] 部室へ行く（各部活の部室を訪問）\n"
        "PRINTFORML [2] 委員会室へ行く（各委員会を訪問）\n"
        "PRINTFORML [9] 戻る\n"
        "PRINTL\n"
        "\n"
        "$INPUT_LOOP\n"
        "INPUT\n"
        "IF RESULT == 0\n"
        "\tCALL LOCATION_SUBMENU_CLASS\n"
        "\tSIF RESULT\n"
        "\t\tBEGIN TURNEND\n"
        "\tRETURN 1\n"
        "ELSEIF RESULT == 1\n"
        "\tCALL LOCATION_SUBMENU_CLUB\n"
        "\tSIF RESULT\n"
        "\t\tBEGIN TURNEND\n"
        "\tRETURN 1\n"
        "ELSEIF RESULT == 2\n"
        "\tCALL LOCATION_SUBMENU_COMMITTEE\n"
        "\tSIF RESULT\n"
        "\t\tBEGIN TURNEND\n"
        "\tRETURN 1\n"
        "ELSEIF RESULT == 9\n"
        "\tRETURN 0\n"
        "ELSE\n"
        "\tGOTO INPUT_LOOP\n"
        "ENDIF\n"
        "RETURN 0\n"
        "\n"
    )
    text = text[:stage_cap_start] + new_capture + text[end_pos:]

    # Fix 'IF CSTR:TARGET:25 != ' (missing "") - there may be trailing spaces
    # In the Shift-JIS decoded text, CSTR may appear as that
    text = re.sub(r'IF CSTR:TARGET:25 != \s*\n', 'IF CSTR:TARGET:25 != ""\n', text)

    # Normalize line endings and write
    text = text.replace('\n', '\r\n')
    with open('ERB/STAGE.ERB', 'wb') as f:
        f.write(text.encode('cp932'))
    print("STAGE.ERB fixed")


# ============================================================
# Fix LOCATION_EVENT.ERB: PARAM:0 -> BASE:0 / MAXBASE:0
# ============================================================
def fix_location_event():
    with open('ERB/LOCATION_EVENT.ERB', 'rb') as f:
        text = f.read().decode('cp932')

    # Replace the broken health-recovery block in @LOCATION_SOLO_EVENT
    old_block = (
        "\tIF BASE:0 > 0\n"
        "\t\tIF PARAM:0 < BASE:0\n"
        "\t\t\tPARAM:0 += BASE:0 / 5 + 1\n"
        "\t\t\tSIF PARAM:0 > BASE:0  PARAM:0 = BASE:0\n"
        "\t\tENDIF\n"
        "\tENDIF"
    )
    new_block = (
        "\tIF BASE:0 < MAXBASE:0\n"
        "\t\tBASE:0 += MAXBASE:0 / 5 + 1\n"
        "\t\tSIF BASE:0 > MAXBASE:0  BASE:0 = MAXBASE:0\n"
        "\tENDIF"
    )

    # Also handle CRLF variants
    old_crlf = old_block.replace('\n', '\r\n')
    new_crlf  = new_block.replace('\n', '\r\n')

    if old_block in text:
        text = text.replace(old_block, new_block)
        print("LOCATION_EVENT.ERB: fixed PARAM:0 block (LF)")
    elif old_crlf in text:
        text = text.replace(old_crlf, new_crlf)
        print("LOCATION_EVENT.ERB: fixed PARAM:0 block (CRLF)")
    else:
        # Try a regex approach for the broken lines
        text = re.sub(
            r'\tIF BASE:0 > 0\r?\n\t\tIF PARAM:0 < BASE:0\r?\n\t\t\tPARAM:0 \+= BASE:0 / 5 \+ 1\r?\n\t\t\tSIF PARAM:0 > BASE:0  PARAM:0 = BASE:0\r?\n\t\tENDIF\r?\n\tENDIF',
            new_block,
            text
        )
        print("LOCATION_EVENT.ERB: fixed PARAM:0 block (regex)")

    with open('ERB/LOCATION_EVENT.ERB', 'wb') as f:
        f.write(text.encode('cp932'))


# ============================================================
# Fix SHOP.ERB: Move PRINT_SHOPITEM behind [120] toggle
# ============================================================
def fix_shop():
    with open('ERB/SHOP.ERB', 'rb') as f:
        text = f.read().decode('cp932')

    # 1) Wrap PRINT_SHOPITEM in a FLAG:70 check
    old_print = (
        ";0-99に自動的に売り物を表示させる。\n"
        ";これは変更しない\n"
        "PRINT_SHOPITEM"
    )
    new_print = (
        ";0-99のショップアイテムはFLAG:70==1の時のみ表示\n"
        "IF FLAG:70 == 1\n"
        "\tPRINTFORML 【ショップ】購入したいアイテムの番号を入力してください\n"
        "\tPRINT_SHOPITEM\n"
        "\tDRAWLINE\n"
        "ENDIF"
    )

    # The actual text in Shift-JIS might differ - search for PRINT_SHOPITEM
    # and the surrounding comment in the decoded text
    # Let's do a simple find/replace just on the PRINT_SHOPITEM line
    # preceded by its comment
    if 'PRINT_SHOPITEM' in text:
        # Find the comment line + PRINT_SHOPITEM block
        # The comment is garbled Shift-JIS, so just find PRINT_SHOPITEM
        # Look for the standalone PRINT_SHOPITEM (not inside IF)
        # It appears between the FLAG:23&16 blocks

        # Simple approach: find 'PRINT_SHOPITEM\n' (standalone line) and wrap it
        # We need to be careful not to match it inside the IF FLAG:23&16 restore block
        # The standalone call is at line 205 in the original

        # Replace just the standalone PRINT_SHOPITEM line (not indented)
        text = re.sub(
            r'^PRINT_SHOPITEM\s*$',
            (
                ";ショップアイテムはFLAG:70==1の時のみ表示\r\n"
                "IF FLAG:70 == 1\r\n"
                "\tPRINTFORML 【ショップ】購入したい商品の番号を入力してください\r\n"
                "\tPRINT_SHOPITEM\r\n"
                "\tDRAWLINE\r\n"
                "ENDIF"
            ),
            text,
            count=1,
            flags=re.MULTILINE
        )
        print("SHOP.ERB: wrapped PRINT_SHOPITEM")
    else:
        print("SHOP.ERB: PRINT_SHOPITEM not found!")

    # 2) Add [120] - ショップ to the action menu
    # Find COUNT == 25 block (currently last item before ELSE/CONTINUE)
    # and add a new ELSEIF for COUNT == 26 (120)
    old_count25 = (
        "ELSEIF COUNT == 25 && DAY:5 <= 4 && TIME == 1 && TARGET >= 0\n"
        "\t\tPRINTLC [120] - 祭り              \n"
        "\tELSE"
    )
    new_count25 = (
        "ELSEIF COUNT == 25 && DAY:5 <= 4 && TIME == 1 && TARGET >= 0\n"
        "\t\tPRINTLC [121] - 祭り              \n"
        "\tELSEIF COUNT == 26\n"
        "\t\tIF FLAG:70 == 1\n"
        "\t\t\tPRINTLC [120] - ショップを閉じる  \n"
        "\t\tELSE\n"
        "\t\t\tPRINTLC [120] - ショップ          \n"
        "\t\tENDIF\n"
        "\tELSE"
    )

    # The CRLF version
    old_crlf = old_count25.replace('\n', '\r\n')
    new_crlf  = new_count25.replace('\n', '\r\n')

    if old_count25 in text:
        text = text.replace(old_count25, new_count25)
        print("SHOP.ERB: added [120] button (LF)")
    elif old_crlf in text:
        text = text.replace(old_crlf, new_crlf)
        print("SHOP.ERB: added [120] button (CRLF)")
    else:
        # Use regex to find the COUNT==25 block generically
        m = re.search(r'ELSEIF COUNT == 25.*?\n\s+ELSE', text, re.DOTALL)
        if m:
            print(f"SHOP.ERB: found COUNT==25 block at {m.start()}-{m.end()}")
            print(repr(m.group()[:200]))
        else:
            print("SHOP.ERB: COUNT==25 block not found, trying to add [120] before REPEAT loop end")
            # Add before the closing ELSE of the REPEAT loop
            # Find the last ELSEIF COUNT == before ELSE\n\t\tCONTINUE
            text = re.sub(
                r'(\tELSE\s*\n\t\tCONTINUE\s*\n\tENDIF)',
                (
                    "\tELSEIF COUNT == 26\r\n"
                    "\t\tIF FLAG:70 == 1\r\n"
                    "\t\t\tPRINTLC [120] - ショップを閉じる  \r\n"
                    "\t\tELSE\r\n"
                    "\t\t\tPRINTLC [120] - ショップ          \r\n"
                    "\t\tENDIF\r\n"
                    "\tELSE\r\n"
                    "\t\tCONTINUE\r\n"
                    "\tENDIF"
                ),
                text,
                count=1
            )
            print("SHOP.ERB: added [120] via regex fallback")

    # 3) Add handler for RESULT==120 in @USERSHOP
    # Find a good insertion point: before RESULT==101 (ストーリー進行)
    old_101 = (
        ";攻略開始\n"
        "ELSEIF RESULT == 101\n"
        "\tTFLAG:600 = 34\n"
        "\tCALL KOJO_JUN\n"
        "\tCALL STAGE_CAPTURE\n"
        "\tBEGIN TURNEND\n"
        "\tRETURN 1"
    )
    new_101 = (
        ";ショップ表示切替\n"
        "ELSEIF RESULT == 120\n"
        "\tIF FLAG:70 == 1\n"
        "\t\tFLAG:70 = 0\n"
        "\tELSE\n"
        "\t\tFLAG:70 = 1\n"
        "\tENDIF\n"
        "\tBEGIN SHOP\n"
        "\tRETURN 1\n"
        "\n"
        ";攻略開始\n"
        "ELSEIF RESULT == 101\n"
        "\tTFLAG:600 = 34\n"
        "\tCALL KOJO_JUN\n"
        "\tCALL STAGE_CAPTURE\n"
        "\tBEGIN TURNEND\n"
        "\tRETURN 1"
    )
    old_crlf = old_101.replace('\n', '\r\n')
    new_crlf  = new_101.replace('\n', '\r\n')
    if old_101 in text:
        text = text.replace(old_101, new_101)
        print("SHOP.ERB: added RESULT==120 handler (LF)")
    elif old_crlf in text:
        text = text.replace(old_crlf, new_crlf)
        print("SHOP.ERB: added RESULT==120 handler (CRLF)")
    else:
        print("SHOP.ERB: RESULT==101 block not found for 120 handler insertion")
        # Regex fallback
        text = re.sub(
            r'(;攻略開始\r?\n)(ELSEIF RESULT == 101)',
            (
                ";ショップ表示切替\r\n"
                "ELSEIF RESULT == 120\r\n"
                "\tIF FLAG:70 == 1\r\n"
                "\t\tFLAG:70 = 0\r\n"
                "\tELSE\r\n"
                "\t\tFLAG:70 = 1\r\n"
                "\tENDIF\r\n"
                "\tBEGIN SHOP\r\n"
                "\tRETURN 1\r\n"
                "\r\n"
                r"\1\2"
            ),
            text,
            count=1
        )
        print("SHOP.ERB: added RESULT==120 handler via regex")

    # Also handle the 祭り [120] → [121] rename in @USERSHOP handler
    text = re.sub(r'RESULT == 120 && DAY:5 <= 4', 'RESULT == 121 && DAY:5 <= 4', text)

    with open('ERB/SHOP.ERB', 'wb') as f:
        f.write(text.encode('cp932'))
    print("SHOP.ERB fixed")


if __name__ == '__main__':
    fix_stage()
    fix_location_event()
    fix_shop()
    print("All done.")
