import os
import glob
import re
import csv
import sys

# Ensure clean utf-8 output to file
output_log = []

def log(msg=""):
    output_log.append(str(msg))

# 1. Load character database
chara_list = []
# Load from CSV/Chara*.csv to get accurate ID
for cid in range(1, 73):
    files = glob.glob(f"CSV/Chara{cid}_*.csv")
    if not files:
        # maybe Chara01?
        files = glob.glob(f"CSV/Chara0{cid}_*.csv")
    if not files:
        continue
    filepath = files[0]
    filename = os.path.basename(filepath)
    # read content
    callname = ""
    fullname = ""
    with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            if line.startswith('名前,'):
                fullname = line.strip().split(',')[1]
            elif line.startswith('呼び名,'):
                callname = line.strip().split(',')[1]
    
    # Split surname and given name
    # e.g. "峰山 しおん" -> surname="峰山", given="しおん"
    # or "クー・カロア"
    if ' ' in fullname:
        parts = fullname.split(' ')
        sur = parts[0]
        giv = parts[1]
    elif '　' in fullname:
        parts = fullname.split('　')
        sur = parts[0]
        giv = parts[1]
    elif '・' in fullname:
        parts = fullname.split('・')
        sur = parts[0]
        giv = parts[1]
    else:
        sur = fullname
        giv = callname
    
    chara_list.append({
        'id': cid,
        'fullname': fullname,
        'callname': callname,
        'sur': sur,
        'giv': giv
    })

log(f"Loaded {len(chara_list)} characters.")

# Targets: 64 to 72
targets = [
    (64, 'しおん', '峰山しおん'),
    (65, 'そら', '時国そら'),
    (66, 'セイラ', '曽根セイラ'),
    (67, 'ましろ', '日滝ましろ'),
    (68, 'ふみ', '深鳥ふみ'),
    (69, 'はじめ', '神樹はじめ'),
    (70, 'ほとり', '神無月ほとり'),
    (71, 'ひびき', '棗ひびき'),
    (72, 'あんず', 'あんず')
]

for cid, short_name, full_name in targets:
    log("\n" + "="*60)
    log(f"ID {cid}: {full_name} ({short_name})")
    log("="*60)
    
    # Collect all dialogue files for this character
    files = glob.glob(f"tools/output/*{short_name}*.txt")
    dialogue_lines = []
    for fpath in files:
        fname = os.path.basename(fpath)
        # Skip analysis files if any, but let's check
        if '分析' in fname:
            continue
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                for line in f:
                    dialogue_lines.append(line.strip())
        except Exception as e:
            try:
                with open(fpath, 'r', encoding='cp932') as f:
                    for line in f:
                        dialogue_lines.append(line.strip())
            except Exception as e2:
                pass
    
    log(f"Total dialogue lines collected: {len(dialogue_lines)} across {len(files)} files")
    full_text = "\n".join(dialogue_lines)
    
    # 1. Search calls to each of the 72 characters
    calls_found = {}
    for other in chara_list:
        oid = other['id']
        if oid == cid:
            continue
        
        # Patterns to check
        # surname + suffix
        # givname + suffix
        # nick
        patterns = [
            other['sur'],
            other['giv'],
            other['callname']
        ]
        # remove empty or too short
        patterns = list(set([p for p in patterns if len(p) >= 2]))
        
        matches = []
        for p in patterns:
            # Look for occurrences with suffix or punctuation
            # e.g., 峰山くん, しおんさん, etc.
            # regex: (?:^|[「『（(【\s、。！？!?])(p(?:さん|ちゃん|くん|君|様|先輩|後輩|殿|氏|先生|部長|委員長|会長|たん)?)
            # or just find p + suffix:
            found = re.findall(rf'({re.escape(p)}(?:さん|ちゃん|くん|君|様|先輩|後輩|殿|氏|先生|部長|委員長|会長|たん)?)', full_text)
            matches.extend(found)
        
        # Count frequency of each variant
        counts = {}
        for m in matches:
            counts[m] = counts.get(m, 0) + 1
        
        if counts:
            # Sort by frequency
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            calls_found[oid] = (other['fullname'], sorted_counts)
    
    # Also look for special keywords: 先輩, 後輩, 部長, 会長, 先生, 転校生, プロデューサー, 貴女, 君, あなた, お前, あんた, etc.
    keywords = ['会長', '部長', '委員長', '先輩', '後輩', '先生', '転校生', 'プロデューサー', 'プロデューサーさん', '少年', '少女', '貴女', 'あなた', 'あんた', 'お前', '君', 'きみ']
    kw_counts = {}
    for kw in keywords:
        cnt = len(re.findall(re.escape(kw), full_text))
        if cnt > 0:
            kw_counts[kw] = cnt
    
    log(f"Keywords frequency: {kw_counts}")
    
    log("\nCalls to other characters (sorted by total frequency):")
    sorted_calls = sorted(calls_found.items(), key=lambda x: sum(c[1] for c in x[1][1]), reverse=True)
    for oid, (oname, variants) in sorted_calls:
        total = sum(c[1] for c in variants)
        var_str = ", ".join([f"{v}: {c}" for v, c in variants[:5]])
        log(f"  [{oid:2d}] {oname} (total {total}): {var_str}")

with open('tools/era_angal_work/survey_3c_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(output_log))

print("Survey complete! Saved to tools/era_angal_work/survey_3c_results.txt")
