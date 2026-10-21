# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

pat = re.compile(r'\bMARK:MASTER:90\s*=')
assignments = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if pat.search(line):
                assignments.append((path, i, line.strip()))

print(f"MARK:MASTER:90 assignments: {len(assignments)}")
for p, i, l in assignments:
    print(f"{p}:{i} -> {l}")
