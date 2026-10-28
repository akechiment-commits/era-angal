# -*- coding: utf-8 -*-
with open('tools/era_angal_work/batch5_clean_report.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = re.findall(r'### CHAR_(\d+)[^\n]*\n((?:\s+-\s+\[[^\n]+\n\s+[^\n]+\n)+)', text)

from collections import Counter
counts_by_char = {}
for cid, block in entries:
    iss = re.findall(r'-\s+\[(.*?)\]', block)
    counts_by_char[cid] = Counter(iss)

for cid in sorted(counts_by_char.keys(), key=lambda x: int(x)):
    print(f"CHAR_{cid}: {dict(counts_by_char[cid])}")
