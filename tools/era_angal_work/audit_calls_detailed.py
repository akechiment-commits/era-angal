# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

# Load actual chara mapping
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

results = []
for sp_id_str, sp_comment, ai_content in speaker_blocks:
    sp_id = int(sp_id_str)
    sp_name, sp_cname, sp_sur = chara_info.get(sp_id, (f'CHAR_{sp_id}', f'CHAR_{sp_id}', ''))
    
    ai_cases = re.findall(r'CASE (\d+)\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_content)
    for ai_id_str, call_str in ai_cases:
        ai_id = int(ai_id_str)
        ai_name, ai_cname, ai_sur = chara_info.get(ai_id, (f'TARGET_{ai_id}', f'TARGET_{ai_id}', ''))
        
        # Check in speaker dialogues
        lines = speaker_dialogue.get(sp_id, [])
        matching_lines = [l for l in lines if call_str in l]
        
        results.append({
            'sp_id': sp_id,
            'sp_name': sp_name,
            'ai_id': ai_id,
            'ai_name': ai_name,
            'call_str': call_str,
            'count': len(matching_lines),
            'sample': matching_lines[0] if matching_lines else ''
        })

# Filter out protagonist AI==0 if count > 0
# Let's inspect all entries where count == 0, and also check small counts (< 3)
with open('tools/era_angal_work/audit_all_individual_calls.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total individual calls: {len(results)}\n\n")
    
    zero_calls = [r for r in results if r['count'] == 0 and '%' not in r['call_str']]
    out.write(f"=== ZERO OCCURRENCE CALLS ({len(zero_calls)}) ===\n")
    for r in zero_calls:
        out.write(f"CHAR_{r['sp_id']:02d} {r['sp_name']} -> AI_{r['ai_id']:02d} {r['ai_name']}: \"{r['call_str']}\"\n")
        
    out.write(f"\n=== LOW OCCURRENCE CALLS (1-2 times) ===\n")
    low_calls = [r for r in results if 1 <= r['count'] <= 2 and '%' not in r['call_str']]
    for r in low_calls:
        out.write(f"CHAR_{r['sp_id']:02d} {r['sp_name']} -> AI_{r['ai_id']:02d} {r['ai_name']}: \"{r['call_str']}\" ({r['count']} times) | Sample: {r['sample'][:80]}\n")

print(f"Total calls: {len(results)}, Zeros: {len(zero_calls)}, Low: {len(low_calls)}")
