import os
import re
import csv
from collections import defaultdict

# Load 72 characters
with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code.split('# Output files mapping')[0])

target_3a = [
    (46, 'みづき', '双葉みづき'),
    (47, 'みなづき', '双葉みなづき'),
    (48, 'みつる', '四方みつる'),
    (49, 'ぼたん', '小松ぼたん'),
    (50, 'ぎん', '山條ぎん'),
    (51, 'かすみ', '御影かすみ'),
    (52, 'やこ', '湖南やこ')
]

def analyze_character_calls(target_cid, target_callname):
    text = ""
    for suffix in ["", "_関係性", "_転校生"]:
        p = f"tools/output/{target_callname}{suffix}.txt"
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                text += f.read() + "\n"
    
    # Also files containing target_callname
    for p in os.listdir('tools/output'):
        if target_callname in p and p not in [f"{target_callname}.txt", f"{target_callname}_関係性.txt", f"{target_callname}_転校生.txt"]:
            with open(f"tools/output/{p}", 'r', encoding='utf-8', errors='replace') as f:
                text += f.read() + "\n"
    
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    calls_found = defaultdict(list)
    
    for other_id, other_full, other_sur, other_cn, other_grade in chara_names:
        if other_id == target_cid:
            continue
        
        search_terms = []
        if len(other_sur) >= 2:
            search_terms.extend([
                rf'{other_sur}さん', rf'{other_sur}ちゃん', rf'{other_sur}君', rf'{other_sur}くん',
                rf'{other_sur}クン', rf'{other_sur}様', rf'{other_sur}さま', rf'{other_sur}殿',
                rf'{other_sur}先輩', rf'{other_sur}センパイ', rf'{other_sur}氏', rf'{other_sur}'
            ])
        if len(other_cn) >= 2:
            search_terms.extend([
                rf'{other_cn}さん', rf'{other_cn}ちゃん', rf'{other_cn}君', rf'{other_cn}くん',
                rf'{other_cn}クン', rf'{other_cn}様', rf'{other_cn}さま', rf'{other_cn}殿',
                rf'{other_cn}先輩', rf'{other_cn}センパイ', rf'{other_cn}'
            ])
            
        found_words = defaultdict(int)
        sample_lines = defaultdict(list)
        for term in search_terms:
            pat = rf'(?:^|[^ぁ-んァ-ヶー一-龠])({term})(?:$|[^ぁ-んァ-ヶー一-龠])'
            for l in lines:
                m = re.search(pat, l)
                if m:
                    word = m.group(1)
                    if len(word) == 2 and word in ['まり', 'ゆり', 'すず', 'るか', 'かな', 'サン', 'ぎん', 'クー']:
                        if not any(k in l for k in [other_sur, 'ちゃん', 'さん', 'くん', '君', '殿', '氏', '先輩']):
                            continue
                    found_words[word] += 1
                    if len(sample_lines[word]) < 3:
                        sample_lines[word].append(l)
        
        if found_words:
            calls_found[other_id] = (other_full, other_grade, found_words, sample_lines)
            
    return calls_found

with open('tools/era_angal_work/3a_all_verified.txt', 'w', encoding='utf-8') as f:
    for cid, callname, fullname in target_3a:
        calls = analyze_character_calls(cid, callname)
        f.write(f"\n=======================================================\n")
        f.write(f"=== ID {cid:02d}: {fullname} ({callname}) 相手呼称精密分析 ===\n")
        for oid in sorted(calls.keys()):
            full, grade, fwords, samples = calls[oid]
            f.write(f"ID {oid:02d}: {full} ({grade}年)\n")
            for w, cnt in sorted(fwords.items(), key=lambda x: x[1], reverse=True):
                f.write(f"   呼称: 『{w}』 ({cnt}回)\n")
                for s in samples[w][:2]:
                    f.write(f"      例: {s}\n")

print("Saved all 3-A verified analysis.")
