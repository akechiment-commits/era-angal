# -*- coding: utf-8 -*-
with open('ERB/SYS_THREE_MONTHS_3ヶ月サイクル処理.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_three_months.txt', 'w', encoding='utf-8') as out:
    for i in range(min(220, len(lines))):
        out.write(f"{i+1}: {lines[i]}")
