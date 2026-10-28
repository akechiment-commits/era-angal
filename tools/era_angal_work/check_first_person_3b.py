import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    (53, 'まり', '花丘まり'),
    (54, 'あやめ', '久坂あやめ'),
    (55, 'さくら', '伊藤さくら'),
    (56, 'ひかる', '八壁ひかる'),
    (57, 'サン', '岩戸サン'),
    (58, 'るり', '天宮るり'),
    (59, 'うしお', '水嶌うしお'),
    (60, 'かえで', '瀬川かえで'),
    (61, 'ひまり', '鶴海ひまり'),
    (62, 'すず', '黒森すず'),
    (63, 'ちづる', '八雲ちづる'),
]

candidates = [
    '私', 'わたし', 'あたし', 'アタシ', 'わたくし', 'ワタクシ',
    '僕', 'ぼく', 'ボク',
    '俺', 'おれ', 'オレ',
    'うち', 'ウチ',
    '自分', '我', '余', 'あちし', 'あたい'
]

for cid, short_name, full_name in targets:
    print(f"\n{'='*60}")
    print(f"ID {cid}: {full_name} ({short_name})")
    print('='*60)
    
    files = glob.glob(f"tools/output/*{short_name}*.txt")
    lines = []
    for fp in files:
        if '分析' in fp:
            continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                lines.extend(f.readlines())
        except:
            with open(fp, 'r', encoding='cp932', errors='ignore') as f:
                lines.extend(f.readlines())
    
    text = "".join(lines)
    
    # Also test character's own name as first person
    cands = candidates + [short_name]
    
    counts = {}
    for c in cands:
        # Match c followed by particle は, が, も, の, に, を, って
        pattern = rf'(?:^|[「『（(\s、。！？!?])({re.escape(c)})(?:[はがものにをって]|自身|たち|ら)'
        m = re.findall(pattern, text)
        if m:
            counts[c] = len(m)
        else:
            # direct count of c in dialogue
            pass
    
    sorted_c = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("First person frequency (with particle):", sorted_c[:8])
    
    # Sample lines for top 1
    if sorted_c:
        top_fp = sorted_c[0][0]
        sample_pattern = rf'([^\n。！？!?]*?{re.escape(top_fp)}[はがもの][^\n。！？!?]*)'
        samples = re.findall(sample_pattern, text)
        print(f"Samples of top '{top_fp}':")
        for s in samples[:3]:
            print(f"  {s.strip()[:80]}")

    # Also check analysis file for first person if mentioned
    ana_files = glob.glob(f"tools/output/*{short_name}*分析*.txt")
    for af in ana_files:
        with open(af, 'r', encoding='utf-8', errors='ignore') as f:
            for l in f:
                if '一人称' in l or 'わたし' in l or '私' in l or '僕' in l or 'オレ' in l or 'うち' in l:
                    if len(l.strip()) < 80:
                        print("  Analysis mention:", l.strip())
                        break
