# -*- coding: utf-8 -*-
with open('ERB/COMF/COMF390.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if 'クラブのＱ' in line or 'ハートのＱ' in line or 'ダイヤのＱ' in line or 'スペードのＱ' in line or 'Ｑ' in line:
        # check preceding line
        prev = lines[i-2].strip()
        print(f"Line {i}: {prev} -> {line.strip()}")
