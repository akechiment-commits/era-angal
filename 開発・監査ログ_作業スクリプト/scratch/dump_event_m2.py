# -*- coding: utf-8 -*-
import glob

f_target = glob.glob('ERB/*EVENT_M*')[1]

with open(f_target, 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_event_m2.txt', 'w', encoding='utf-8') as out:
    out.write(f"=== {f_target} Lines 525-615 ===\n")
    for i in range(524, min(len(lines), 615)):
        out.write(f"{i+1}: {lines[i]}")

    out.write("\n=== Lines 3430-3480 ===\n")
    for i in range(3429, min(len(lines), 3480)):
        out.write(f"{i+1}: {lines[i]}")
