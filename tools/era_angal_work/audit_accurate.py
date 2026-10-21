# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

def main():
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        erb_text = f.read()

    # Load actual chara mapping from actual_csv_charas.txt
    chara_info = {}
    with open('tools/era_angal_work/actual_csv_charas.txt', 'r', encoding='utf-8') as fp:
        for l in fp:
            # e.g. 10: 木之下ゆゆ (ゆゆ)
            m = re.match(r'(\d+):\s*(.*?)\s*\((.*?)\)', l.strip())
            if m:
                cid = int(m.group(1))
                name = m.group(2).strip()
                cname = m.group(3).strip()
                sur = name.replace(cname, '').replace('・', '').strip()
                chara_info[cid] = (name, cname, sur)

    # Load speaker dialogue from tools/output/{cname}.txt
    output_texts = {}
    for cid, (name, cname, sur) in chara_info.items():
        if cid == 0: continue
        path = os.path.join('tools', 'output', f'{cname}.txt')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                output_texts[cname] = fp.read()
        else:
            # try full name
            path2 = os.path.join('tools', 'output', f'{name}.txt')
            if os.path.exists(path2):
                with open(path2, 'r', encoding='utf-8', errors='ignore') as fp:
                    output_texts[cname] = fp.read()

    # Load all scenarios speaker lines
    scenario_files = glob.glob('tools/scenarios/*.txt')
    scenario_speaker_lines = defaultdict(list)
    for fpath in scenario_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            for line in fp:
                line = line.strip()
                m = re.match(r'【(.*?)】(.*)', line)
                if m:
                    spk, text = m.group(1), m.group(2)
                    scenario_speaker_lines[spk].append(text)

    # Extract all individual rules from ERB
    pos2 = erb_text.find(';--- (2) 個別の特殊呼称（上書き）---')
    if pos2 == -1:
        parts = erb_text.split('SELECTCASE SP')
        indiv_text = parts[2]
    else:
        indiv_text = erb_text[pos2:]

    speaker_blocks = re.findall(r'\t\tCASE (\d+)\s*\n\t\t\t;([^\n]+)\n\t\t\tSELECTCASE AI\n(.*?)\t\t\tENDSELECT', indiv_text, re.DOTALL)
    print(f'Parsed {len(speaker_blocks)} speaker blocks in ERB.')

    all_entries = []
    for sp_id_str, sp_comment, ai_content in speaker_blocks:
        sp_id = int(sp_id_str)
        sp_name, sp_cname, sp_sur = chara_info.get(sp_id, (f'CHAR_{sp_id}', f'CHAR_{sp_id}', ''))

        ai_cases = re.findall(r'CASE (\d+)\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_content)
        for ai_id_str, call_str in ai_cases:
            ai_id = int(ai_id_str)
            ai_name, ai_cname, ai_sur = chara_info.get(ai_id, (f'TARGET_{ai_id}', f'TARGET_{ai_id}', ''))
            all_entries.append((sp_id, sp_name, sp_cname, ai_id, ai_name, ai_cname, call_str))

    print(f'Total individual call entries: {len(all_entries)}')

    zero_occurrences = []
    verified_entries = []

    for sp_id, sp_name, sp_cname, ai_id, ai_name, ai_cname, call_str in all_entries:
        # If call_str contains %, skip
        if '%' in call_str:
            continue

        # Check in output text
        out_txt = output_texts.get(sp_cname, '')
        count_out = out_txt.count(call_str)

        # Check in scenarios for speaker
        scen_lines = scenario_speaker_lines.get(sp_cname, [])
        if not scen_lines:
            scen_lines = scenario_speaker_lines.get(sp_name, [])
        # also try checking if call_str is in any lines
        count_scen = sum(1 for l in scen_lines if call_str in l)

        total_count = count_out + count_scen

        # Special check for Protagonist (ai_id == 0)
        # Check if call_str is used in scenarios by speaker
        if ai_id == 0:
            # e.g. "転校生くん", "転校生さん", "プロデューサー", etc.
            is_valid_p = (total_count > 0)
        else:
            is_valid_p = True

        verified_entries.append((sp_id, sp_name, ai_id, ai_name, call_str, count_out, count_scen, total_count))
        if total_count == 0:
            zero_occurrences.append((sp_id, sp_name, ai_id, ai_name, call_str))

    print(f'Verified {len(verified_entries)} entries.')
    print(f'Zero occurrences found: {len(zero_occurrences)}')

    with open('tools/era_angal_work/audit_accurate_zero_occurrences.txt', 'w', encoding='utf-8') as out:
        out.write(f'=== ACCURATE ZERO OCCURRENCE ENTRIES ({len(zero_occurrences)}) ===\n')
        for sp_id, sp_name, ai_id, ai_name, call_str in zero_occurrences:
            out.write(f'CHAR_{sp_id} {sp_name} -> AI_{ai_id} {ai_name}: "{call_str}"\n')

    print('Wrote audit_accurate_zero_occurrences.txt successfully!')

if __name__ == '__main__':
    main()
