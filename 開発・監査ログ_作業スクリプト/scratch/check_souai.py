# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# 1. Look for TALENT:89 = 1 assignments
pat_souai = re.compile(r'\bTALENT(?::[A-Za-z0-9_]+)?:89\s*=\s*1\b')
souai_assignments = []

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if pat_souai.search(code):
                souai_assignments.append((path, i, code))

# 2. Look for item 85 (エンゲージリング) sales conditions and usage
# ITEMSALES:85, BOUGHT == 85, etc.

with open('scratch_souai.txt', 'w', encoding='utf-8') as out:
    out.write("=== TALENT:89 = 1 (相愛取得) ===\n")
    for p, i, c in souai_assignments:
        out.write(f"{p}:{i} -> {c}\n")

print(f"Souai assignments: {len(souai_assignments)}")
