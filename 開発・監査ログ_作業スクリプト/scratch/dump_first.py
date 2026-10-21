# -*- coding: utf-8 -*-
with open('ERB/SYSTEM_基本システム処理.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_eventfirst.txt', 'w', encoding='utf-8') as out:
    for i in range(min(80, len(lines))):
        out.write(f"{i+1}: {lines[i]}")
