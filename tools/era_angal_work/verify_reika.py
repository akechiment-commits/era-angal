import os
import re
import csv
from collections import defaultdict

# Load 72 characters
with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    # get chara_names
    code = f.read()

# Execute mapping
exec(code.split('# Output files mapping')[0])

def analyze_character_calls(target_cid, target_callname):
    # Read files
    text = ""
    for suffix in ["", "_関係性", "_転校生"]:
        p = f"tools/output/{target_callname}{suffix}.txt"
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                text += f.read() + "\n"
    
    # Lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    
    calls_found = defaultdict(list)
    
    # We want to test every other character
    for other_id, other_full, other_sur, other_cn, other_grade in chara_names:
        if other_id == target_cid:
            continue
        
        # Test exact patterns
        # 1. surname + suffixes (さん, ちゃん, 君, くん, 様, 殿, 先輩, 氏, etc.)
        # 2. callname + suffixes
        # 3. plain surname, plain callname (in quotes or dialogue)
        # 4. special nicknames
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
                    # avoid false positive if word is too generic (like "まり", "ゆり", "るか", "すず")
                    if len(word) == 2 and word in ['まり', 'ゆり', 'すず', 'るか', 'かな', 'サン', 'ぎん']:
                        # check if it looks like person reference
                        if not any(k in l for k in [other_sur, 'ちゃん', 'さん', 'くん', '君']):
                            continue
                    found_words[word] += 1
                    if len(sample_lines[word]) < 3:
                        sample_lines[word].append(l)
        
        if found_words:
            calls_found[other_id] = (other_full, other_grade, found_words, sample_lines)
            
    return calls_found

# Run for Reika (45)
reika_calls = analyze_character_calls(45, 'れいか')

with open('tools/era_angal_work/reika_verified.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== 円城寺れいか 相手呼称精密分析 ===\n")
    for oid in sorted(reika_calls.keys()):
        full, grade, fwords, samples = reika_calls[oid]
        f.write(f"ID {oid:02d}: {full} ({grade}年)\n")
        for w, cnt in sorted(fwords.items(), key=lambda x: x[1], reverse=True):
            f.write(f"   呼称: 『{w}』 ({cnt}回)\n")
            for s in samples[w][:2]:
                f.write(f"      例: {s}\n")

print("Saved Reika verified analysis.")
