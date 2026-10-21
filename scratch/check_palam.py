# -*- coding: utf-8 -*-
import os, re

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

csv_palam = load_csv('CSV/Palam.csv')
print(f"Defined PALAM indices: {sorted(list(csv_palam))}")

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

palam_errors = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            for m in re.finditer(r'\b(?:PALAM|CUP|CDOWN|UP|DOWN|JUEL|GOTJUEL)(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                idx = int(m.group(1))
                if idx not in csv_palam and idx != 100:  # 100 is sometimes negation or special
                    palam_errors.append((path, i, idx, line.strip()))

print(f"Undefined PALAM/JUEL usages: {len(palam_errors)}")
for p, i, idx, l in palam_errors[:20]:
    print(f"{p}:{i} [index:{idx}] -> {l}")
