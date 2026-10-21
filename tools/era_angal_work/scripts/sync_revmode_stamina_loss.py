# -*- coding: utf-8 -*-
"""
REVMODE_SOURCE_CHECK の体力・気力消費計算を、
通常調教（SOURCE_CHECK）と完全に同等・同レベルの計算式に正しく移植するスクリプト。
"""

import glob
import sys

def main():
    normal_source_file = glob.glob('ERB/SOURCE*.ERB')[0]
    with open(normal_source_file, 'rb') as f:
        normal_text = f.read().decode('cp932').replace('\r\n', '\n')

    # Find the EXACT blocks in normal SOURCE_CHECK:
    idx_d = normal_text.find('D = UP:9/16')
    pos_a = normal_text.rfind('IF BASE:1 <= 0', 0, idx_d)
    assert pos_a != -1 and idx_d != -1, "Base<=0 or D=UP:9/16 not found"

    pos_end = normal_text.find('BASE:0 -= LOSEBASE:0\nBASE:1 -= LOSEBASE:1', idx_d)
    assert pos_end != -1, "pos_end not found"

    full_calc_block = normal_text[pos_a:pos_end]

    # Remove TFLAG:543 halving so it's 100% full normal rate
    old_halving = '''IF TFLAG:543
\tLOSEBASE:0 = (LOSEBASE:0 + 1) / 2
\tLOSEBASE:1 = (LOSEBASE:1 + 1) / 2
\tDOWNBASE:MASTER:0 = (DOWNBASE:MASTER:0 + 1) / 2
ENDIF\n'''
    if old_halving in full_calc_block:
        full_calc_block = full_calc_block.replace(old_halving, ';主導権完全委譲時も通常調教と同等に100%全額消費\n')

    # Read REVMODE
    revmode_path = 'ERB/REVMODE_リバースモード.ERB'
    with open(revmode_path, 'rb') as f:
        rev_text = f.read().decode('cp932').replace('\r\n', '\n')

    target_start_1 = ';体力・気力の減少（通常調教と完全同等に消費）'
    target_start_2 = ';体力・気力の減少'

    pos_rev_start = rev_text.find(target_start_1)
    if pos_rev_start == -1:
        pos_rev_start = rev_text.find(target_start_2)
    assert pos_rev_start != -1, "Target start in REVMODE not found"

    pos_rev_end = rev_text.find('BASE:0 -= LOSEBASE:0\nBASE:1 -= LOSEBASE:1', pos_rev_start)
    assert pos_rev_end != -1, "Target end in REVMODE not found"

    new_content = ''';-------------------------------------------------
;体力・気力の減少（通常調教と完全同等に消費）
;-------------------------------------------------
''' + full_calc_block

    rev_text = rev_text[:pos_rev_start] + new_content + rev_text[pos_rev_end:]

    with open(revmode_path, 'wb') as f:
        f.write(rev_text.replace('\n', '\r\n').encode('cp932'))

    print("Successfully replaced with complete normal stamina loss logic.")

if __name__ == '__main__':
    main()
