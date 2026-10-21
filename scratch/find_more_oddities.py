# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Let's inspect some specific interesting patterns:
# 1. Variables with potential typos or mismatch:
#    e.g. CFLAG, TFLAG, FLAG with very high numbers or undefined
# 2. Logic errors: e.g. IF A && !A, or duplicate conditions, or impossible ranges
# 3. CSV definitions check:
#    Let's check CFLAG usages against Cflag.csv, TFLAG against Tflag.csv, FLAG against Flag.csv

def load_csv(path):
    d = set()
    if not os.path.exists(path): return d
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';'): continue
            parts = line.split(',')
            if parts[0].isdigit():
                d.add(int(parts[0]))
    return d

csv_flag = load_csv('CSV/Flag.csv')
csv_cflag = load_csv('CSV/Cflag.csv')
csv_tflag = load_csv('CSV/Tflag.csv')

print(f"Loaded: Flag={len(csv_flag)}, Cflag={len(csv_cflag)}, Tflag={len(csv_tflag)}")

# Find any FLAG / CFLAG / TFLAG usages that have comments indicating what they are,
# or where there might be bugs.
# Also let's check for dead code or suspicious patterns in COMF files.
