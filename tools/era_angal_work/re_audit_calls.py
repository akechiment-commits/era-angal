# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

# 1. Load actual chara mapping
chara_info = {}
with open('tools/era_angal_work/actual_csv_charas.txt', 'r', encoding='utf-8') as fp:
    for l in fp:
        m = re.match(r'(\d+):\s*(.*?)\s*\((.*?)\)', l.strip())
        if m:
            cid = int(m.group(1))
            name = m.group(2).strip()
            cname = m.group(3).strip()
            sur = name.replace(cname, '').replace('・', '').strip()
            chara_info[cid] = (name, cname, sur)

speaker_to_id = {}
for cid, (name, cname, sur) in chara_info.items():
    speaker_to_id[cname] = cid
    speaker_to_id[name] = cid
speaker_to_id['やくも'] = 63
speaker_to_id['クー'] = 38
speaker_to_id['サン'] = 57
speaker_to_id['セイラ'] = 66
speaker_to_id['レンレン'] = 37

# Collect all dialogues per speaker
speaker_dialogue = defaultdict(list)
for fpath in glob.glob('tools/scenarios/*.txt'):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            line = line.strip()
            m = re.match(r'【(.*?)】(.*)', line)
            if m:
                spk, text = m.group(1), m.group(2)
                for s in re.split(r'[・＆]', spk):
                    s = s.strip()
                    if s in speaker_to_id:
                        speaker_dialogue[speaker_to_id[s]].append(text)

for cid, (name, cname, sur) in chara_info.items():
    if cid == 0: continue
    path = os.path.join('tools', 'output', f'{cname}.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            for l in fp:
                l = l.strip()
                if l:
                    speaker_dialogue[cid].append(l)

# Parse ERB
with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    erb_text = f.read()

pos2 = erb_text.find(';--- (2) 個別の特殊呼称（上書き）---')
if pos2 == -1:
    parts = erb_text.split('SELECTCASE SP')
    indiv_text = parts[2]
else:
    indiv_text = erb_text[pos2:]

speaker_blocks = re.findall(r'\t\tCASE (\d+)\s*\n\t\t\t;([^\n]+)\n\t\t\tSELECTCASE AI\n(.*?)\t\t\tENDSELECT', indiv_text, re.DOTALL)

# Words that can be false positives if matching exact substring
FALSE_POSITIVE_WORDS = {
    'いちか': ['いちから', 'いちかばちか'],
    'はじめ': ['はじめて', 'はじめに', 'はじめまし', 'はじめよう', 'はじめたい', 'はじめましょ', 'はじめようか', 'はじめちゃ', 'はじめの', 'はじめる', 'はじめだ', 'はじめな', 'はじめよ', 'はじめから'],
    'すず': ['すずし', 'すずめ'],
    'サン': ['サンタ', 'サンキュー', 'サンド', 'サングラス', 'サンオイル', 'サンプル', 'サンダル', 'バレンタイン'],
    'クー': ['クーラー', 'クール', 'クープ'],
    'みつる': ['みつる'],
    'いさみ': ['いさみ足', 'いさみ'],
    'ひよの': ['ひよの'],
    'ちか': ['ちから', 'ちかづ', 'ちかい', 'ちかく', 'ちかごろ', 'ちかづい', 'ちかづか', 'ちかつ'],
    'なな': ['ななめ', 'ななな', 'なな、']
}

all_checked = []
for sp_id_str, sp_comment, ai_content in speaker_blocks:
    sp_id = int(sp_id_str)
    sp_name, sp_cname, sp_sur = chara_info.get(sp_id, (f'CHAR_{sp_id}', f'CHAR_{sp_id}', ''))
    
    ai_cases = re.findall(r'CASE (\d+)\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_content)
    for ai_id_str, call_str in ai_cases:
        ai_id = int(ai_id_str)
        ai_name, ai_cname, ai_sur = chara_info.get(ai_id, (f'TARGET_{ai_id}', f'TARGET_{ai_id}', ''))
        
        lines = speaker_dialogue.get(sp_id, [])
        valid_matches = []
        
        # Check false positive filters
        for l in lines:
            if call_str in l:
                # filter false positive
                is_fp = False
                if call_str in FALSE_POSITIVE_WORDS:
                    # check if ALL occurrences in this line are inside forbidden substrings
                    temp_l = l
                    for bad in FALSE_POSITIVE_WORDS[call_str]:
                        temp_l = temp_l.replace(bad, '')
                    if call_str not in temp_l:
                        is_fp = True
                if not is_fp:
                    valid_matches.append(l)
        
        all_checked.append({
            'sp_id': sp_id,
            'sp_name': sp_name,
            'sp_cname': sp_cname,
            'ai_id': ai_id,
            'ai_name': ai_name,
            'ai_cname': ai_cname,
            'call_str': call_str,
            'valid_count': len(valid_matches),
            'samples': valid_matches[:3]
        })

with open('tools/era_angal_work/audit_all_checked.txt', 'w', encoding='utf-8') as out:
    # Separate into:
    # 1. OK (count >= 1, not % variable, or AI==0 with valid count)
    # 2. Variable (%CALLNAME...)
    # 3. SUSPICIOUS / ZERO COUNT (count == 0, excluding variable)
    
    zeros = [c for c in all_checked if c['valid_count'] == 0 and '%' not in c['call_str']]
    lows = [c for c in all_checked if 1 <= c['valid_count'] <= 2 and '%' not in c['call_str']]
    
    out.write(f"=== ZERO VALID OCCURRENCES ({len(zeros)}) ===\n")
    for c in zeros:
        out.write(f"CHAR_{c['sp_id']:02d} {c['sp_name']} -> AI_{c['ai_id']:02d} {c['ai_name']}: \"{c['call_str']}\"\n")
        
    out.write(f"\n=== LOW VALID OCCURRENCES (1-2) ({len(lows)}) ===\n")
    for c in lows:
        out.write(f"CHAR_{c['sp_id']:02d} {c['sp_name']} -> AI_{c['ai_id']:02d} {c['ai_name']}: \"{c['call_str']}\" ({c['valid_count']} times)\n")
        for s in c['samples']:
            out.write(f"    sample: {s[:100]}\n")

print(f"Audit finished. Zeros: {len(zeros)}, Lows: {len(lows)}")
