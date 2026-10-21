# -*- coding: utf-8 -*-
import glob, re

f_target = glob.glob('ERB/*EVENT_M*')[1]
with open(f_target, 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

# Look for places where "割れ目を" or "ワレメを" or "秘裂を" or "アナルを" is printed,
# followed by another "〜を貫く" or "〜を" in the next few lines!
for i, line in enumerate(lines, 1):
    if re.search(r'PRINT(?:FORM)?\s+.*(?:割れ目を|ワレメを|秘裂を|アナルを|窄まりを)', line):
        print(f"Match at line {i}: {line.strip()}")
        for j in range(i, min(len(lines), i + 25)):
            if 'PRINTW' in lines[j] or 'PRINTFORMW' in lines[j]:
                print(f"  {j+1}: {lines[j].strip()}")
