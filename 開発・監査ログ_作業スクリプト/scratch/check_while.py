# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Look for WHILE without CLEARLINE or INPUT, or tight GOTO loops
while_loops = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            code = line.split(';')[0].strip()
            if code.upper().startswith('WHILE 1') or code.upper().startswith('WHILE -1') or code.upper().startswith('WHILE TRUE'):
                while_loops.append((path, i, code))

print(f"WHILE 1 loops: {len(while_loops)}")
for p, i, c in while_loops:
    print(f"{p}:{i} -> {c}")
