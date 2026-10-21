# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

def check_specific(cname, target_words):
    print(f"=== {cname} specific calls ===")
    with open(f'tools/output/{cname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for w in target_words:
        hits = [l.strip() for l in lines if w in l]
        print(f"[{w}] ({len(hits)} hits):")
        for h in hits[:6]:
            print(f"  {h[:120]}")

with open('scratch/check_specific_out.txt', 'w', encoding='utf-8') as out:
    orig = sys.stdout
    sys.stdout = out
    check_specific('なつみ', ['小松', 'ぼたん', 'ひまり', '会長', 'そら', 'セイラ', '曽根', 'ましろ', 'ふみ', 'ほとり', 'ひびき'])
    check_specific('つゆり', ['時国', 'そら', '曽根', 'セイラ', 'ひまり', '会長', 'ぼたん', '小松'])
    check_specific('さあや', ['ひまり', '会長', 'セイラ', '曽根', 'ぼたん', '小松', 'あいか', 'ゆゆ', '夢路', '柊'])
    sys.stdout = orig

print("Done.")
