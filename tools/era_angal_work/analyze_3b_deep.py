import os
import re
import csv
from collections import defaultdict

# 72 characters definitions
with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code.split('# Output files mapping')[0])

target_3b = [
    (53, '花丘まり', 'まり'),
    (54, '久坂あやめ', 'あやめ'),
    (55, '伊藤さくら', 'さくら'),
    (56, '八壁ひかる', 'ひかる'),
    (57, '岩戸サン', 'サン'),
    (58, '天宮るり', 'るり'),
    (59, '水嶌うしお', 'うしお'),
    (60, '瀬川かえで', 'かえで'),
    (61, '鶴海ひまり', 'ひまり'),
    (62, '黒森すず', 'すず'),
    (63, '八雲ちづる', 'ちづる')
]

# Check files for each character
output_dir = 'tools/output'
all_output_files = os.listdir(output_dir)

report = []

for cid, fullname, callname in target_3b:
    report.append(f"\n================================================================================")
    report.append(f"【ID {cid:02d} : {fullname}】(CALLNAME: {callname})")
    
    # Matching files
    matched_files = []
    # exact callname.txt
    if f"{callname}.txt" in all_output_files:
        matched_files.append(f"{callname}.txt")
    if f"{callname}_関係性.txt" in all_output_files:
        matched_files.append(f"{callname}_関係性.txt")
    if f"{callname}_転校生.txt" in all_output_files:
        matched_files.append(f"{callname}_転校生.txt")
        
    for f in all_output_files:
        if callname in f and f not in matched_files:
            matched_files.append(f)
            
    report.append(f"対象ファイル: {matched_files}")
    
    all_text = ""
    for mf in matched_files:
        with open(os.path.join(output_dir, mf), 'r', encoding='utf-8', errors='replace') as fp:
            all_text += fp.read() + "\n"
            
    report.append(f"総文字数: {len(all_text)}")
    
    # 1. First-person analysis
    fps = {}
    for fp_word in ['わたし', 'わたくし', 'あたし', 'アタシ', 'ボク', 'ぼく', '僕', 'オレ', 'おれ', '俺', '自分', 'うち', callname]:
        c = len(re.findall(rf'(?:^|[^ぁ-んァ-ヶー一-龠]){re.escape(fp_word)}(?:$|[^ぁ-んァ-ヶー一-龠])', all_text))
        if c > 0:
            fps[fp_word] = c
    report.append(f"一人称分析: {fps}")
    
    # 2. Player calling analysis
    pcalls = {}
    for pword in ['転校生', 'プロデューサー', 'あなた', 'あんた', 'お前', 'オマエ', '君', 'きみ']:
        c = len(re.findall(re.escape(pword), all_text))
        if c > 0:
            pcalls[pword] = c
    report.append(f"プレイヤー呼称分析: {pcalls}")
    
    # 3. Vocatives to other 71 characters
    lines = [l.strip() for l in all_text.splitlines() if l.strip()]
    
    mentions = defaultdict(lambda: defaultdict(list))
    
    for other_id, other_full, other_sur, other_cn, other_grade in chara_names:
        if other_id == cid:
            continue
        
        # Test terms:
        # Full surname + suffixes
        # Full callname + suffixes
        terms = []
        if len(other_sur) >= 2:
            for suf in ['さん', 'ちゃん', '君', 'くん', 'クン', '様', 'さま', '殿', 'どの', '先輩', 'センパイ', '氏', '']:
                terms.append(other_sur + suf)
        if len(other_cn) >= 2:
            for suf in ['さん', 'ちゃん', '君', 'くん', 'クン', '様', 'さま', '殿', 'どの', '先輩', 'センパイ', '氏', '']:
                terms.append(other_cn + suf)
                
        # Special foreign name handle: クー・カロア
        if other_id == 38:
            terms.extend(['カロア', 'クー', 'クーちゃん', 'クーさん', 'カロアさん', 'カロアクン'])
        # Special nickname checks based on intro or known settings
        if other_id == 72:
            terms.extend(['あんず', 'あんずさん', 'あんずちゃん', 'あんず先輩'])
            
        # Deduplicate terms
        terms = list(set(terms))
        
        for t in terms:
            # We want exact word boundary match
            pat = rf'(?:^|[^ぁ-んァ-ヶー一-龠])({re.escape(t)})(?:$|[^ぁ-んァ-ヶー一-龠])'
            for l in lines:
                m = re.search(pat, l)
                if m:
                    w = m.group(1)
                    # Exclude common false positives if word is generic
                    if w in ['まり', 'ゆり', 'すず', 'るか', 'かな', 'サン', 'ぎん', 'クー', 'さくら', 'うしお', 'そら', 'はじめ', 'ひびき', 'つばさ', 'ことり', 'ひめの', 'みけ', 'しずく', 'すみれ', 'いかり']:
                        if not any(k in l for k in [other_sur, 'ちゃん', 'さん', 'くん', '君', '殿', 'どの', '様', '先輩']):
                            continue
                    mentions[other_id][w].append(l)
                    
    # Also search titles/roles
    for title in ['会長', '生徒会長', '部長', '副部長', '王子', '先生']:
        for l in lines:
            if title in l:
                mentions[999][title].append(l)
                
    report.append("--- 検出された相手呼称 ---")
    for other_id in sorted(mentions.keys()):
        if other_id == 999:
            report.append("【役職言及】:")
            for t, l_list in mentions[999].items():
                report.append(f"  * {t} ({len(l_list)}回): {l_list[:2]}")
            continue
            
        oinfo = [c for c in chara_names if c[0] == other_id][0]
        ofull = oinfo[1]
        ograde = oinfo[4]
        mdict = mentions[other_id]
        
        call_strs = []
        for w, l_list in sorted(mdict.items(), key=lambda x: len(x[1]), reverse=True):
            call_strs.append(f"『{w}』({len(l_list)}回)")
            
        report.append(f"  -> ID {other_id:02d} {ofull} ({ograde}年): {', '.join(call_strs)}")
        for w, l_list in sorted(mdict.items(), key=lambda x: len(x[1]), reverse=True)[:2]:
            report.append(f"       例: {l_list[0][:80]}")

with open('tools/era_angal_work/3b_analysis_deep.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(report))

print("Saved 3b_analysis_deep.txt successfully.")
