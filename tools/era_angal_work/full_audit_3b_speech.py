import re
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    (53, 'まり.txt', '花丘まり'),
    (54, 'あやめ.txt', '久坂あやめ'),
    (55, 'さくら.txt', '伊藤さくら'),
    (56, 'ひかる.txt', '八壁ひかる'),
    (57, 'サン.txt', '岩戸サン'),
    (58, 'るり.txt', '天宮るり'),
    (59, 'うしお.txt', '水嶌うしお'),
    (60, 'かえで.txt', '瀬川かえで'),
    (61, 'ひまり.txt', '鶴海ひまり'),
    (62, 'すず.txt', '黒森すず'),
    (63, 'ちづる.txt', '八雲ちづる'),
]

for cid, filename, fullname in targets:
    fpath = f"tools/output/{filename}"
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"\n{'='*60}")
    print(f"ID {cid}: {fullname} ({filename})")
    print('='*60)
    
    # 1. First person analysis
    fps = ['あたし', 'わたし', '私', 'わたくし', '俺', 'オレ', 'おれ', 'ボク', '僕', 'ぼく', 'うち', 'ウチ', '自分', fullname.split(' ')[0], filename.replace('.txt', '')]
    fps = list(dict.fromkeys(fps))
    fp_counts = {}
    for fp in fps:
        # count occurrences with particles or standalone
        m = re.findall(rf'(?:^|[「『（(\s、。！？!?])({re.escape(fp)})(?:[はがものにをって]|自身|たち|ら)', text)
        if m:
            fp_counts[fp] = len(m)
    sorted_fps = sorted(fp_counts.items(), key=lambda x: x[1], reverse=True)
    print("一人称 (実数):", sorted_fps[:5])
    
    # 2. Second person analysis
    sps = ['あなた', 'あんた', 'アンタ', 'きみ', 'キミ', '君', 'お前', 'おまえ', 'オマエ', '貴女', '貴方', '汝', '貴様', 'ユー']
    sp_counts = {}
    for sp in sps:
        m = re.findall(rf'(?:^|[「『（(\s、。！？!?])({re.escape(sp)})(?:[はがものにをって]|たち|ら|[、。！？!?\s])', text)
        if m:
            sp_counts[sp] = len(m)
    sorted_sps = sorted(sp_counts.items(), key=lambda x: x[1], reverse=True)
    print("二人称 (実数):", sorted_sps[:5])
    
    # 3. Tone / Ending particles sample
    dialogues = [l.strip() for l in text.splitlines() if l.strip()]
    print(f"セリフ総行数: {len(dialogues)}")
    print("セリフ代表サンプル (3件):")
    for d in dialogues[10:13]:
        print(f"  {d[:80]}")
