import re
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

# Chara dict
chara_dict = {0: {'full': 'あなた', 'call': 'あなた'}}
for cid in range(1, 73):
    files = glob.glob(f'CSV/Chara{cid}_*.csv') + glob.glob(f'CSV/Chara0{cid}_*.csv')
    filepath = files[0]
    callname = ""
    fullname = ""
    with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            if line.startswith('名前,'):
                fullname = line.strip().split(',')[1]
            elif line.startswith('呼び名,'):
                callname = line.strip().split(',')[1]
    # Split surname and callname
    sur = fullname.replace(callname, '').replace('・', '').replace(' ', '').replace('　', '').strip()
    if not sur:
        sur = callname
    chara_dict[cid] = {'full': fullname, 'call': callname, 'sur': sur}

# Target: 53 to 63
targets_3b = [
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

for sp, short_name, full_name in targets_3b:
    print(f"\n{'='*60}")
    print(f"AUDITING CHAR_{sp}: {full_name} ({short_name})")
    print('='*60)
    
    files = glob.glob(f"tools/output/*{short_name}*.txt")
    dialogues = []
    for fp in files:
        if '分析' in fp:
            continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                dialogues.extend(f.readlines())
        except:
            with open(fp, 'r', encoding='cp932', errors='ignore') as f:
                dialogues.extend(f.readlines())
    full_text = "".join(dialogues)
    
    # 1. Search calls to each of 72 characters
    found_calls = {}
    for other_id in range(1, 73):
        if other_id == sp:
            continue
        sur = chara_dict[other_id]['sur']
        call = chara_dict[other_id]['call']
        
        # patterns
        pts = list(set([sur, call]))
        pts = [p for p in pts if len(p) >= 2]
        
        matches = []
        for p in pts:
            m = re.findall(rf'({re.escape(p)}(?:さん|ちゃん|くん|君|様|先輩|後輩|殿|氏|先生|部長|委員長|会長|たん)?)', full_text)
            matches.extend(m)
        if matches:
            from collections import Counter
            cnt = Counter(matches)
            found_calls[other_id] = cnt.most_common(3)
    
    # Sort by total frequency
    sorted_calls = sorted(found_calls.items(), key=lambda x: sum(c[1] for c in x[1]), reverse=True)
    print("Top calls to other characters:")
    for oid, top_c in sorted_calls[:15]:
        c_str = ", ".join([f"{k}:{v}" for k, v in top_c])
        print(f"  [{oid:02d}] {chara_dict[oid]['full']:10s} ({chara_dict[oid]['call']}): {c_str}")
