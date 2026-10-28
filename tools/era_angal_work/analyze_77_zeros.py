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

# 77 zeros list
zeros = []
with open('tools/era_angal_work/audit_all_checked.txt', 'r', encoding='utf-8') as fp:
    mode = False
    for line in fp:
        if line.startswith('=== ZERO VALID OCCURRENCES'):
            mode = True
            continue
        if line.startswith('=== LOW VALID OCCURRENCES'):
            break
        if mode and line.strip():
            m = re.match(r'CHAR_(\d+)\s+(.*?)\s+->\s+AI_(\d+)\s+(.*?):\s+"([^"]+)"', line.strip())
            if m:
                sp_id, sp_name, ai_id, ai_name, call_str = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4), m.group(5)
                zeros.append((sp_id, sp_name, ai_id, ai_name, call_str))

print(f"Analyzing {len(zeros)} zeros...")

detailed_analysis = []
for sp_id, sp_name, ai_id, ai_name, call_str in zeros:
    lines = speaker_dialogue.get(sp_id, [])
    t_name, t_cname, t_sur = chara_info.get(ai_id, (ai_name, ai_name, ''))
    
    # Search for all occurrences of t_cname or t_sur in speaker lines
    found_lines = []
    if ai_id == 0:
        # Protagonist
        for l in lines:
            if any(k in l for k in ['転校生', '先輩', 'せんぱい', 'プロデューサー', 'あんた', 'アンタ', 'あなた', 'オマエ', 'お前', '君', 'キミ']):
                found_lines.append(l)
    else:
        for l in lines:
            # Check if t_cname or t_sur is in l
            if t_cname and t_cname in l:
                found_lines.append(l)
            elif t_sur and t_sur in l:
                found_lines.append(l)
                
    detailed_analysis.append((sp_id, sp_name, ai_id, ai_name, call_str, len(found_lines), found_lines[:5]))

with open('tools/era_angal_work/zeros_full_analysis.txt', 'w', encoding='utf-8') as out:
    for sp_id, sp_name, ai_id, ai_name, call_str, cnt, samples in detailed_analysis:
        out.write(f"CHAR_{sp_id:02d} {sp_name} -> AI_{ai_id:02d} {ai_name} (Current: \"{call_str}\") | Mentions: {cnt}\n")
        if samples:
            for s in samples:
                out.write(f"    * {s[:110]}\n")
        else:
            out.write("    * (NO MENTIONS IN ORIGINAL SCENARIOS/DIALOGUE)\n")
        out.write("\n")

print("Wrote zeros_full_analysis.txt")
