# -*- coding: utf-8 -*-
with open('tools/era_angal_work/batch1_results.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = re.findall(r'CHAR_(\d+)\s+\|\s+([^\n|]+)\|\s+([^\n]+)\n\s+Text:\s+([^\n]+)', text)

from collections import Counter
type_counts = Counter([e[2] for e in entries])
for t, c in type_counts.most_common(10):
    print(f"{t}: {c}")

print("\nSample of top issue:")
top_issue = type_counts.most_common(1)[0][0]
samples = [e for e in entries if e[2] == top_issue][:5]
for s in samples:
    print(f"CHAR_{s[0]} | {s[1]} | {s[3][:80]}")
