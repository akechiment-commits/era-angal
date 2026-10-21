# -*- coding: utf-8 -*-
import os

targets = ['人体として有り得ないほど', '胸のふくらみを撫でた', 'ふくらみを撫でた', 'ゆっくりと胸の']

matches = []
for root, dirs, files in os.walk('ERB'):
    for f in files:
        if f.endswith(('.ERB', '.erb')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='cp932', errors='ignore') as fp:
                for i, line in enumerate(fp, 1):
                    for t in targets:
                        if t in line:
                            matches.append((p, i, t, line.strip()))

print(f"Total matches: {len(matches)}")
for p, i, t, l in matches:
    print(f"{p}:{i} [{t}] -> {l}")
