# -*- coding: utf-8 -*-
import re

with open('scratch_omit_targets.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

exact_targets = []
# Match TALENT:181, TALENT:182, ITEM:86, ITEM:87, ITEMSALES:86, ITEMSALES:87, BOUGHT == 86, BOUGHT == 87
pat = re.compile(r'\b(TALENT(?::[A-Za-z0-9_]+)?:(?:181|182)|ITEMSALES:(?:86|87)|ITEM:(?:86|87)|BOUGHT\s*==\s*(?:86|87))\b')

for line in lines:
    if pat.search(line):
        exact_targets.append(line.strip())

with open('scratch_exact_omit.txt', 'w', encoding='utf-8') as out:
    for item in exact_targets:
        out.write(item + '\n')

print(f"Exact matches: {len(exact_targets)}")
