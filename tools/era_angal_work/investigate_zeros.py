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

# Speaker mapping to chara_id
speaker_to_id = {}
for cid, (name, cname, sur) in chara_info.items():
    speaker_to_id[cname] = cid
    speaker_to_id[name] = cid
speaker_to_id['やくも'] = 63 # 八雲ちづる
speaker_to_id['クー'] = 38
speaker_to_id['サン'] = 57
speaker_to_id['セイラ'] = 66
speaker_to_id['レンレン'] = 37

# Collect all dialogues per speaker across all scenarios and output
speaker_dialogue = defaultdict(list)
for fpath in glob.glob('tools/scenarios/*.txt'):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            line = line.strip()
            m = re.match(r'【(.*?)】(.*)', line)
            if m:
                spk, text = m.group(1), m.group(2)
                # handle combined speakers like かなえ・きこ
                for s in re.split(r'[・＆]', spk):
                    s = s.strip()
                    if s in speaker_to_id:
                        speaker_dialogue[speaker_to_id[s]].append(text)

# Also output texts
for cid, (name, cname, sur) in chara_info.items():
    if cid == 0: continue
    path = os.path.join('tools', 'output', f'{cname}.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            for l in fp:
                l = l.strip()
                if l:
                    speaker_dialogue[cid].append(l)

print("Loaded dialogues for speakers:", len(speaker_dialogue))

# Read zero occurrences
zeros = []
with open('tools/era_angal_work/audit_accurate_zero_occurrences.txt', 'r', encoding='utf-8') as fp:
    for l in fp:
        m = re.match(r'CHAR_(\d+)\s+(.*?)\s+->\s+AI_(\d+)\s+(.*?):\s+"([^"]+)"', l.strip())
        if m:
            sp_id, sp_name, ai_id, ai_name, call_str = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4), m.group(5)
            zeros.append((sp_id, sp_name, ai_id, ai_name, call_str))

print(f"Investigating {len(zeros)} zero occurrences...")

# For each zero entry, let's search if the speaker EVER talks about or to the target AI,
# or what the speaker actually calls the target AI or protagonist.
report = []
for sp_id, sp_name, ai_id, ai_name, call_str in zeros:
    lines = speaker_dialogue.get(sp_id, [])
    # Search for target AI name, callname, surname
    ai_target_info = chara_info.get(ai_id, (ai_name, ai_name, ''))
    t_name, t_cname, t_sur = ai_target_info

    # Find any lines where speaker mentions target
    mentions = []
    if ai_id == 0:
        # Protagonist: search for 転校生, せんぱい, 先輩, プロデューサー, お前, あんた, キミ, etc.
        patterns = [r'転校生', r'せんぱい', r'先輩', r'プロデューサー', r'あなた', r'あんた', r'アンタ', r'お前', r'オマエ', r'君', r'キミ']
        for l in lines:
            for p in patterns:
                if re.search(p, l):
                    mentions.append(l)
                    break
    else:
        # Target character
        patterns = [re.escape(t_cname)]
        if t_sur:
            patterns.append(re.escape(t_sur))
        regex = re.compile('|'.join(patterns))
        for l in lines:
            if regex.search(l):
                mentions.append(l)

    report.append({
        'sp_id': sp_id, 'sp_name': sp_name,
        'ai_id': ai_id, 'ai_name': ai_name,
        'call_str': call_str,
        'total_lines': len(lines),
        'mentions_count': len(mentions),
        'sample_mentions': mentions[:5]
    })

with open('tools/era_angal_work/zero_investigation.txt', 'w', encoding='utf-8') as out:
    for r in report:
        out.write(f"=== CHAR_{r['sp_id']} {r['sp_name']} -> AI_{r['ai_id']} {r['ai_name']} (Configured: \"{r['call_str']}\") ===\n")
        out.write(f"Speaker total lines: {r['total_lines']}, Mentions of target: {r['mentions_count']}\n")
        if r['sample_mentions']:
            out.write("Samples:\n")
            for sm in r['sample_mentions']:
                out.write(f"  * {sm[:120]}\n")
        out.write("\n")

print("Wrote tools/era_angal_work/zero_investigation.txt")
