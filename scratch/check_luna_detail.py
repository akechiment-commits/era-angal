# -*- coding: utf-8 -*-
import sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/output/るな.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines in るな.txt: {len(lines)}")

# 1. 相手への呼びかけ（「〜はん」「〜先輩」「〜さん」「〜ちゃん」「〜」「呼び捨て」）
# 関西弁で「会長はん」など
keywords = [
    'クー', 'カロア', 'ちあき', '高原', 'みけ', '猫塚', '会長', 'ひまり', '円城寺', 'れいか',
    '双葉', 'みづき', 'ぼたん', '小松', 'サン', '岩戸', '湖南', 'やこ', 'はじめ', '神樹',
    'あんず', 'さあや', '堀田', 'かな', '梅園', '藍乃', 'あいか', 'ゆき', '北川',
    'つゆり', '八朔', 'なつみ', '三波', 'まい', '安条', 'まりあ', '夢路'
]

print("=== るな キーワード呼びかけ精読 ===")
for kw in keywords:
    hits = [l.strip() for l in lines if kw in l]
    if hits:
        print(f"\n--- {kw} ({len(hits)}件) ---")
        for h in hits[:5]:
            print(f"  {h[:120]}")
