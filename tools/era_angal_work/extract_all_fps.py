# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict, Counter

chara_roster = {}
with open('tools/era_angal_work/actual_csv_charas.txt', 'r', encoding='utf-8') as fp:
    for l in fp:
        m = re.match(r'(\d+):\s*(.*?)\s*\((.*?)\)', l.strip())
        if m:
            cid = int(m.group(1))
            name = m.group(2).strip()
            cname = m.group(3).strip()
            chara_roster[cid] = (name, cname)

pronouns = ['私', 'わたし', 'あたし', 'あたい', 'ボク', 'ぼく', '僕', 'うち', 'ウチ', 'オラ', 'おら', '俺', 'おれ', 'わたくし', '自分']

actual_fp_stats = {}

for cid, (name, cname) in chara_roster.items():
    if cid == 0: continue
    path = os.path.join('tools', 'output', f'{cname}.txt')
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        text = fp.read()
        
    counts = Counter()
    for p in pronouns:
        # Match pronoun followed by particle
        # exclude e.g. うちの部, 私生活, ボクサー etc.
        m = re.findall(rf'(?<![ぁ-んァ-ヶ一-龠]){p}(?=[はがをにものでと、。！？…―\s])', text)
        if p in ['うち', 'ウチ']:
            # filter out うちの部 etc.
            valid_m = [x for x in m] # already followed by はがをにものでと、
        counts[p] = len(m)
        
    top_p = counts.most_common(3)
    actual_fp_stats[cid] = (name, cname, top_p)

with open('tools/era_angal_work/all_charas_actual_fps.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(actual_fp_stats.keys()):
        name, cname, top_p = actual_fp_stats[cid]
        top_str = ', '.join([f'{p}:{c}' for p, c in top_p if c > 0])
        out.write(f"CHAR_{cid:02d} {name:<12s} ({cname}): {top_str}\n")

print("Wrote all_charas_actual_fps.txt")
