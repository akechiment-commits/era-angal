# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

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

with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    erb_text = f.read()

pos2 = erb_text.find(';--- (2) 個別の特殊呼称（上書き）---')
indiv_text = erb_text[pos2:] if pos2 != -1 else erb_text

speaker_blocks = re.findall(r'\t\tCASE (\d+)\s*\n\t\t\t;([^\n]+)\n\t\t\tSELECTCASE AI\n(.*?)\t\t\tENDSELECT', indiv_text, re.DOTALL)

FALSE_POSITIVE_WORDS = {
    'いちか': ['いちから', 'いちかばちか'],
    'はじめ': ['はじめて', 'はじめに', 'はじめまし', 'はじめよう', 'はじめたい', 'はじめましょ', 'はじめようか', 'はじめちゃ', 'はじめの', 'はじめる', 'はじめだ', 'はじめな', 'はじめよ', 'はじめから', '祈りはじめた', '勉強をはじめる', '名乗りはじめた'],
    'すず': ['すずし', 'すずめ'],
    'サン': ['サンタ', 'サンキュー', 'サンド', 'サングラス', 'サンオイル', 'サンプル', 'サンダル', 'バレンタイン'],
    'クー': ['クーラー', 'クール', 'クープ'],
    'ちか': ['ちから', 'ちかづ', 'ちかい', 'ちかく', 'ちかごろ', 'ちかづい', 'ちかづか', 'ちかつ'],
    'なな': ['ななめ', 'ななな', 'なな、']
}

all_records = []
for sp_id_str, sp_comment, ai_content in speaker_blocks:
    sp_id = int(sp_id_str)
    sp_name, sp_cname, sp_sur = chara_info.get(sp_id, (f'CHAR_{sp_id}', f'CHAR_{sp_id}', ''))
    
    ai_cases = re.findall(r'CASE (\d+)\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_content)
    for ai_id_str, call_str in ai_cases:
        ai_id = int(ai_id_str)
        ai_name, ai_cname, ai_sur = chara_info.get(ai_id, (f'TARGET_{ai_id}', f'TARGET_{ai_id}', ''))
        
        lines = speaker_dialogue.get(sp_id, [])
        valid_matches = []
        for l in lines:
            if call_str in l:
                is_fp = False
                if call_str in FALSE_POSITIVE_WORDS:
                    temp_l = l
                    for bad in FALSE_POSITIVE_WORDS[call_str]:
                        temp_l = temp_l.replace(bad, '')
                    if call_str not in temp_l:
                        is_fp = True
                if not is_fp:
                    valid_matches.append(l)
                    
        all_records.append({
            'sp_id': sp_id,
            'sp_name': sp_name,
            'sp_cname': sp_cname,
            'ai_id': ai_id,
            'ai_name': ai_name,
            'ai_cname': ai_cname,
            'call_str': call_str,
            'count': len(valid_matches),
            'samples': valid_matches[:2]
        })

# Let's inspect everything where count == 0 or count <= 2
with open('tools/era_angal_work/audit_full_inventory.txt', 'w', encoding='utf-8') as out:
    out.write(f"TOTAL INDIVIDUAL CALL ENTRIES: {len(all_records)}\n\n")
    for r in all_records:
        if '%' in r['call_str']:
            status = 'VARIABLE'
        elif r['count'] == 0:
            status = 'ZERO_COUNT'
        elif r['count'] <= 2:
            status = 'LOW_COUNT'
        else:
            status = 'VERIFIED'
        out.write(f"[{status:10s}] CHAR_{r['sp_id']:02d} {r['sp_name']:<10s} -> AI_{r['ai_id']:02d} {r['ai_name']:<10s}: \"{r['call_str']}\" (count={r['count']})\n")
        if r['samples']:
            for s in r['samples']:
                out.write(f"             Sample: {s[:100]}\n")

print("Wrote audit_full_inventory.txt")
