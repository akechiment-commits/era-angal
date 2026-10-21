# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Check for UP:17 or UP:24 in context of 快B
matches = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if 'UP:17' in line or 'UP:24' in line or 'PALAM:17' in line:
                matches.append((path, i, line.strip()))

with open('scratch_up17.txt', 'w', encoding='utf-8') as out:
    for p, i, l in matches:
        out.write(f"{p}:{i} -> {l}\n")

print(f"Matches for UP:17/24: {len(matches)}")
