import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Character ID to Name mapping
chara_dict = {}
for cid in range(1, 73):
    files = glob.glob(f"CSV/Chara{cid}_*.csv") + glob.glob(f"CSV/Chara0{cid}_*.csv")
    if not files:
        continue
    filepath = files[0]
    callname = ""
    fullname = ""
    with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            if line.startswith('名前,'):
                fullname = line.strip().split(',')[1]
            elif line.startswith('呼び名,'):
                callname = line.strip().split(',')[1]
    chara_dict[cid] = {'full': fullname, 'call': callname}

print("Loaded characters 1 to 72.")

# Survey each character's calls to:
# 1. 主人公 (AI:0) - 転校生, 少年, 先輩, あんた, きみ, お前, ダーリン, プロデューサー, etc.
# 2. あんず (AI:72) - あんず, あんずさん, あんずちゃん, アンジー, etc.

results = {}

for cid in range(1, 73):
    cname = chara_dict[cid]['call']
    # find files
    files = glob.glob(f"tools/output/*{cname}*.txt")
    tenkousei_files = glob.glob(f"tools/output/*{cname}*転校生*.txt")
    
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
    
    # 1. Search calls to 主人公
    # Check tenkousei files specifically if available
    hero_calls = []
    # Patterns for hero
    hero_patterns = [
        r'転校生[くん|さん|ちゃん|しゃん|殿|様]*',
        r'プロデューサー[さん|様]*',
        r'少年',
        r'ダーリン',
        r'ヘルプマン',
        r'お兄ちゃん先輩',
        r'お兄ちゃん',
        r'せんぱい',
        r'先輩'
    ]
    hero_counts = {}
    for p in hero_patterns:
        m = re.findall(p, full_text)
        if m:
            for item in m:
                if item:
                    hero_counts[item] = hero_counts.get(item, 0) + 1
    
    # 2. Search calls to あんず (AI:72)
    anzu_patterns = [
        r'あんずさん',
        r'あんずちゃん',
        r'あんずお姉ちゃん',
        r'あんず先輩',
        r'あんず様',
        r'アンジー',
        r'あんず'
    ]
    anzu_counts = {}
    for p in anzu_patterns:
        m = re.findall(p, full_text)
        if m:
            for item in m:
                if item:
                    anzu_counts[item] = anzu_counts.get(item, 0) + 1
    
    # Sort
    sorted_hero = sorted(hero_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_anzu = sorted(anzu_counts.items(), key=lambda x: x[1], reverse=True)
    
    results[cid] = {
        'name': cname,
        'hero': sorted_hero[:5],
        'anzu': sorted_anzu[:5]
    }

# Also inspect あんず_間接資料.txt for how each character refers to anzu
with open('tools/output/あんず_間接資料.txt', 'r', encoding='utf-8') as f:
    anzu_doc = f.read()

print("Surveying calls to あんず from indirect document...")
anzu_doc_by_chara = {}
current_chara = None
for line in anzu_doc.splitlines():
    m = re.match(r'###\s*\[([^\]]+)\.txt\]', line)
    if m:
        current_chara = m.group(1)
        anzu_doc_by_chara[current_chara] = []
    elif current_chara and line.strip():
        anzu_doc_by_chara[current_chara].append(line.strip())

for cid in range(1, 73):
    cname = chara_dict[cid]['call']
    r = results[cid]
    hero_str = ", ".join([f"{k}:{v}" for k, v in r['hero']])
    anzu_str = ", ".join([f"{k}:{v}" for k, v in r['anzu']])
    
    # Check indirect doc
    doc_lines = anzu_doc_by_chara.get(cname, [])
    doc_mentions = []
    if doc_lines:
        doc_text = " ".join(doc_lines)
        for p in [r'あんずさん', r'あんずちゃん', r'あんずお姉ちゃん', r'アンジー', r'あんず']:
            cnt = len(re.findall(p, doc_text))
            if cnt > 0:
                doc_mentions.append(f"{p}:{cnt}")
    doc_str = ", ".join(doc_mentions)
    print(f"[{cid:2d}] {cname:6s} | 主人公: [{hero_str}] | あんず(直接): [{anzu_str}] | あんず(間接): [{doc_str}]")
