# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

def load_csv(path):
    d = {}
    if not os.path.exists(path): return d
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';'): continue
            parts = line.split(',')
            if parts[0].isdigit():
                d[int(parts[0])] = parts[1].strip()
    return d

csv_talent = load_csv('CSV/Talent.csv')
csv_abl = load_csv('CSV/Abl.csv')
csv_exp = load_csv('CSV/Exp.csv')
csv_mark = load_csv('CSV/Mark.csv')

event_files = [p for p in files if 'EVENT' in p or 'DAILY' in p or 'AFTER' in p or 'SYS' in p]

oddities = []

for path in event_files:
    if 'tools' in path or 'YU-CTION' in path: continue
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if not code: continue

            for m in re.finditer(r'\bABL(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                idx = int(m.group(1))
                if idx not in csv_abl:
                    oddities.append((path, i, f"Undefined ABL:{idx}", line.strip()))

            for m in re.finditer(r'\bTALENT(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                idx = int(m.group(1))
                if idx not in csv_talent:
                    oddities.append((path, i, f"Undefined TALENT:{idx}", line.strip()))

            for m in re.finditer(r'\bEXP(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                idx = int(m.group(1))
                if idx not in csv_exp:
                    oddities.append((path, i, f"Undefined EXP:{idx}", line.strip()))

            for m in re.finditer(r'\bMARK(?::[A-Za-z0-9_]+)?:(\d+)\b', code):
                idx = int(m.group(1))
                if idx not in csv_mark:
                    oddities.append((path, i, f"Undefined MARK:{idx}", line.strip()))

with open('scratch_event_oddities.txt', 'w', encoding='utf-8') as out:
    for p, i, desc, l in oddities:
        out.write(f"{p}:{i} [{desc}] -> {l}\n")

print(f"Total Event oddities: {len(oddities)}")
