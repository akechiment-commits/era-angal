# -*- coding: utf-8 -*-
import glob

f_target = glob.glob('ERB/*EVENT_M*')[1]
with open(f_target, 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

for i in range(550, 615):
    print(f"{i+1}: {lines[i].strip()}")
