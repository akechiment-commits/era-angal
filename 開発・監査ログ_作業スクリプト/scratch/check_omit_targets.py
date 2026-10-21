# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

targets = ['181', '182', 'ITEM:86', 'ITEM:87', 'ITEMSALES:86', 'ITEMSALES:87', 'BOUGHT == 86', 'BOUGHT == 87']

matches = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            for t in targets:
                if t in line:
                    matches.append((path, i, t, line.strip()))

with open('scratch_omit_targets.txt', 'w', encoding='utf-8') as out:
    for p, i, t, l in matches:
        out.write(f"{p}:{i} [{t}] -> {l}\n")

print(f"Total matches: {len(matches)}")
