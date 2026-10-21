# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Look for suspicious logic:
# 1. IF conditions that are always False: e.g. A && !A or X > 10 && X < 5
# 2. Duplicate ELSEIF conditions
# 3. Setting a variable and immediately overwriting it without using it
suspicious_logic = []

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        lines = f.readlines()
        current_func = ""
        conditions = []
        for i, line in enumerate(lines, 1):
            code = line.split(';')[0].strip()
            if not code: continue
            if code.startswith('@'):
                current_func = code
                conditions = []
                continue
            
            # Check duplicate conditions in IF-ELSEIF chains
            if code.startswith('IF '):
                conditions = [code[3:].strip()]
            elif code.startswith('ELSEIF '):
                cond = code[7:].strip()
                if cond in conditions:
                    suspicious_logic.append((path, i, "Duplicate condition in IF/ELSEIF", code))
                conditions.append(cond)
            elif code.startswith('ENDIF'):
                conditions = []

print(f"Suspicious logic: {len(suspicious_logic)}")
for p, i, d, c in suspicious_logic[:30]:
    print(f"{p}:{i} [{d}] -> {c}")
