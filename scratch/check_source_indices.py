# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Let's search for:
# 1. Negative LOSEBASE: (healing health instead of consuming?)
# 2. SOURCE index greater than 23 (SOURCE range in era-angal: let's check Sourcename.csv)
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

csv_source = load_csv('CSV/Source.csv')
print(f"Defined SOURCE indices: {sorted(list(csv_source))}")

source_errors = []
for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            for m in re.finditer(r'\bSOURCE(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                s_idx = int(m.group(1))
                if s_idx not in csv_source:
                    source_errors.append((path, i, s_idx, line.strip()))

print(f"Undefined SOURCE usages: {len(source_errors)}")
for p, i, idx, l in source_errors[:20]:
    print(f"{p}:{i} [SOURCE:{idx}] -> {l}")
