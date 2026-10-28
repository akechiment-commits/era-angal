# -*- coding: utf-8 -*-
import sys, os, re

def investigate_char(cname):
    print(f"==================== {cname} 呼びかけ調査 ====================")
    with open(f'tools/output/{cname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    keywords = [
        'こよ', 'なっちゃん', 'ゆり', 'さあや', 'まりあ', 'なな', 'ゆう', 'もも', 'すみれ', 'しずく',
        'あんず', 'つゆり', 'なつみ', '梅園', 'かな', '猫塚', 'みけ', '星海', '安条', 'まい',
        'セイラ', 'はじめ', 'ましろ', 'ぎん', 'るか', 'ちか', 'レンレン', 'クー', 'カロア',
        'ひまり', '会長', '部長', 'せんぱい', '先輩', '先生'
    ]
    
    found = []
    for l in lines:
        for kw in keywords:
            if kw in l:
                found.append((kw, l.strip()))
                break
    
    print(f"Total keyword hits: {len(found)}")
    by_kw = {}
    for kw, l in found:
        by_kw.setdefault(kw, []).append(l)
        
    for kw, l_list in sorted(by_kw.items()):
        print(f"\n--- キーワード: {kw} (全{len(l_list)}件) ---")
        for sample in l_list[:6]:
            print(f"  {sample[:120]}")

out_path = r'scratch/calls_24_26_out.txt'
with open(out_path, 'w', encoding='utf-8') as out:
    orig = sys.stdout
    sys.stdout = out
    investigate_char('つゆり')
    investigate_char('さあや')
    investigate_char('なつみ')
    sys.stdout = orig

print("Done.")
