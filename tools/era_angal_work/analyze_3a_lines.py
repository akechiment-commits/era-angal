import os
import glob
import re
import csv
from collections import defaultdict

# 1. Load all characters from character_data.csv or ERB
with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    all_chara_rows = list(reader)

# Map index 1-72 to chara info
chara_list = {}
# Read ERB to get accurate ID to Name mapping
with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932', errors='replace') as f:
    erb_lines = f.readlines()

for line in erb_lines:
    m = re.match(r'\s*CASE (\d+)\s*;(.*)', line)
    if m:
        cid = int(m.group(1))
        cname = m.group(2).strip()
        if cid <= 72 and cid not in chara_list:
            chara_list[cid] = cname

# Full mapping with surname, callname
id_to_info = {}
for cid in range(1, 73):
    # find row in csv
    for r in all_chara_rows:
        # Match by name
        cname = chara_list.get(cid, '')
        if r['name'] in cname or cname in r['name']:
            # split surname/callname if possible
            # e.g., '円城寺れいか' -> surname='円城寺', callname='れいか'
            # special case: クー・カロア
            if 'カロア' in r['name']:
                sur = 'クー・カロア'
                cn = 'クー'
            elif len(r['name']) >= 4:
                # common patterns
                sur = r['name'][:2] if len(r['name']) == 4 else r['name'][:3]
                cn = r['name'][len(sur):]
            else:
                sur = r['name'][:1]
                cn = r['name'][1:]
            id_to_info[cid] = {'id': cid, 'name': r['name'], 'class': r.get('class'), 'club': r.get('club'), 'intro': r.get('intro')}
            break

print(f"Loaded {len(chara_list)} characters from ERB.")

# Target 3-A characters
target_3a = [
    (45, '円城寺れいか'),
    (46, '双葉みづき'),
    (47, '双葉みなづき'),
    (48, '四方みつる'),
    (49, '小松ぼたん'),
    (50, '山條ぎん'),
    (51, '御影かすみ'),
    (52, '湖南やこ')
]

# Patterns for extracting calls:
# e.g. "○○さん", "○○ちゃん", "○○先輩", "○○部長", "○○君", "○○くん", "○○", etc.
# Also search specific nicknames mentioned in existing ERB:
existing_erb_calls = {
    45: {8: '丸子さん', 13: '羽森さん', 14: '花音さん', 26: '堀田さん', 34: '桐島さん', 40: '夜霧さん', 49: '小松さん', 52: '湖南さん', 59: '水嶌さん', 63: '八雲さん', 65: '時国さん', 67: '日滝さん', 69: 'はじめさん', 72: 'あんずさん'},
    46: {47: 'みなづき'},
    47: {22: 'いかりちゃん', 23: 'こはるちゃん', 28: 'こよいちゃん', 41: 'ともちゃん', 44: 'ひよのちゃん', 45: 'れいかちゃん', 46: 'みづき', 48: 'みつるちゃん', 50: 'ぎんちゃん', 51: 'かすみん', 59: 'うしおちゃん', 60: 'かえでちゃん', 61: 'ひまりちゃん', 65: 'そらちゃん'},
    48: {24: '三波さん', 25: '八朔さん', 27: '夏野さん', 31: 'まりあさん', 32: '安条さん', 35: '梅園さん', 36: '遠見さん', 52: '湖南さん', 57: '岩戸さん', 60: '瀬川さん', 63: '八雲さん', 66: '曽根さん', 68: '深鳥さん'},
    50: {24: '三波殿', 37: '龍泉寺殿', 45: '円城寺殿', 52: '湖南殿', 56: '八壁殿'},
    52: {36: 'トミコ'}
}

# Scan output text files
results = {}
for cid, name in target_3a:
    results[cid] = {'name': name, 'calls': defaultdict(list)}
    # Find text file
    pattern = f"tools/output/*{name}*.txt"
    files = glob.glob(pattern)
    if not files:
        # try callname or surname
        files = glob.glob(f"tools/output/*{name[:2]}*.txt") + glob.glob(f"tools/output/*{name[-2:]}*.txt")
    
    text = ""
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            text += f.read() + "\n"
    
    results[cid]['text_len'] = len(text)
    results[cid]['filepaths'] = files

    # Scan for calls to all other characters (1 to 72)
    # We will search for mentions of surnames, callnames, and nicknames
    for other_id, other_name in chara_list.items():
        if other_id == cid:
            continue
        # get tokens to search
        # remove symbols
        raw_name = re.sub(r'[\s・]', '', other_name)
        # surname candidates, callname candidates
        tokens = []
        if len(raw_name) == 4:
            tokens.append(raw_name[:2]) # surname
            tokens.append(raw_name[2:]) # callname
        elif len(raw_name) == 5:
            tokens.append(raw_name[:3]) # 3-letter surname e.g. 龍泉寺
            tokens.append(raw_name[:2])
            tokens.append(raw_name[3:])
            tokens.append(raw_name[2:])
        elif len(raw_name) == 3:
            tokens.append(raw_name[:1])
            tokens.append(raw_name[1:])
            tokens.append(raw_name[:2])
            tokens.append(raw_name[2:])
        tokens.append(raw_name)
        
        # also add existing ERB call if any
        if other_id in existing_erb_calls.get(cid, {}):
            tokens.append(existing_erb_calls[cid][other_id])
        
        # Filter tokens (length >= 2, exclude very generic words)
        tokens = list(set([t for t in tokens if len(t) >= 2]))
        
        for t in tokens:
            # Search pattern: token + (さん|ちゃん|先輩|センパイ|君|くん|クン|様|さま|殿|氏)?
            pat = rf'({re.escape(t)}(?:さん|ちゃん|先輩|センパイ|君|くん|クン|様|さま|殿|氏|部長|会長|先生)?)'
            matches = re.findall(pat, text)
            if matches:
                # count
                counts = defaultdict(int)
                for m in matches:
                    counts[m] += 1
                for call_form, count in counts.items():
                    results[cid]['calls'][other_id].append((call_form, count))

# Save summary to file
with open('tools/era_angal_work/3a_analysis_raw.txt', 'w', encoding='utf-8') as f:
    for cid, name in target_3a:
        f.write(f"\n==================================================\n")
        f.write(f"ID {cid}: {name} (Files: {results[cid]['filepaths']}, Len: {results[cid]['text_len']})\n")
        f.write(f"Existing ERB calls: {existing_erb_calls.get(cid, {})}\n")
        f.write(f"Mentions found:\n")
        for other_id in sorted(results[cid]['calls'].keys()):
            other_name = chara_list.get(other_id, f"ID_{other_id}")
            calls = results[cid]['calls'][other_id]
            f.write(f"  -> {other_id:02d} {other_name}: {calls}\n")

print("Analysis raw saved to tools/era_angal_work/3a_analysis_raw.txt")
