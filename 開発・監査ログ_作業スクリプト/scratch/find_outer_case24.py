# -*- coding: utf-8 -*-
import sys, re

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    text = f.read().decode('cp932')

# 外側の SELECTCASE SP の中の CASE を見つける
# SPのCASEはインデントが \t\tCASE X
# 内部の AIのCASEはインデントが \t\t\t\tCASE X

lines = text.split('\r\n')
for i, l in enumerate(lines):
    if l.startswith('\t\tCASE 24'):
        print(f"Line {i+1}: {repr(l)}")
        for j in range(max(0, i-2), min(len(lines), i+10)):
            print(f"  {j+1}: {lines[j]}")
        print("="*40)
