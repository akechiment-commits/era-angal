# -*- coding: utf-8 -*-
import sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/output/まりあ.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines in まりあ.txt: {len(lines)}")

# 1. 相手への呼びかけ（「〜さま」「〜様」「〜さん」「〜ちゃん」「〜先輩」「〜先生」「〜くん」）
pats = [
    r'([^\s「」]*(?:様|さま|さん|ちゃん|先輩|先生|くん|君)[^\s「」]*)'
]

hits = []
for idx, l in enumerate(lines):
    line_clean = l.strip()
    if not line_clean: continue
    for p in pats:
        for m in re.finditer(p, line_clean):
            word = m.group(1)
            # ノイズ除去（神様、皆様、お客様、ごちそうさま等）
            if word in ['神様', '神さま', '皆様', 'みなさま', 'お客様', 'お疲れ様', 'お疲れさま', 'ごちそうさま']:
                continue
            hits.append((word, line_clean))

print(f"Total call candidates: {len(hits)}")
c = Counter([x[0] for x in hits])
for term, count in c.most_common(40):
    print(f"  {term}: {count}回")

print("\n--- 代表的なセリフ抜粋 ---")
by_term = {}
for term, line in hits:
    by_term.setdefault(term, []).append(line)

for term, count in c.most_common(25):
    print(f"\n【{term}】 ({count}回)")
    for s in by_term[term][:3]:
        print(f"   {s[:120]}")
