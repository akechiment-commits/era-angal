# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# 1. Check FLAG:5 assignments (Difficulty setting)
flag5_assignments = []
flag5_pat = re.compile(r'\bFLAG:5\s*=\s*(\d+|[A-Za-z0-9_]+)')

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if flag5_pat.search(code):
                flag5_assignments.append((path, i, code))

# 2. Check TALENT:180 assignments (Obtaining 服従)
# Also check TALENT:TARGET:180, TALENT:ARG:180, TALENT:COUNT:180, etc.
talent180_assignments = []
talent180_pat = re.compile(r'\bTALENT(?::[A-Za-z0-9_]+)?:180\s*=\s*(\d+|[A-Za-z0-9_]+)')

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if talent180_pat.search(code):
                talent180_assignments.append((path, i, code))

with open('scratch_difficulty_subjugation.txt', 'w', encoding='utf-8') as out:
    out.write("=== FLAG:5 ASSIGNMENTS (DIFFICULTY) ===\n")
    for p, i, c in flag5_assignments:
        out.write(f"{p}:{i} -> {c}\n")

    out.write("\n=== TALENT:180 ASSIGNMENTS (服従) ===\n")
    for p, i, c in talent180_assignments:
        out.write(f"{p}:{i} -> {c}\n")
