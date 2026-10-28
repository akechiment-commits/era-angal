# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

flag3_assignments = []
flag3_pat = re.compile(r'\bFLAG:3\s*=\s*(\d+|[A-Za-z0-9_]+)')

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if flag3_pat.search(code):
                flag3_assignments.append((path, i, code))

with open('scratch_flag3.txt', 'w', encoding='utf-8') as out:
    for p, i, c in flag3_assignments:
        out.write(f"{p}:{i} -> {c}\n")
