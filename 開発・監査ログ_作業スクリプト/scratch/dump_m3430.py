# -*- coding: utf-8 -*-
import glob

f_target = glob.glob('ERB/*EVENT_M*')[1]

with open(f_target, 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_event_m3430.txt', 'w', encoding='utf-8') as out:
    for i in range(3429, min(len(lines), 3530)):
        out.write(f"{i+1}: {lines[i]}")
