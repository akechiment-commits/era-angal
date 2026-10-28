import os, glob, re

def get_keywords(text):
    return set(re.findall(r'[\u4e00-\u9fff\u30a0-\u30ff]{2,}', text))

def match_score(kws, text):
    if not kws or not text: return 0
    t_kws = get_keywords(text)
    score = len(kws & t_kws) * 2
    for w in kws:
        if w in text:
            score += 5
    return score

report = []

for ch_id in range(1, 73):
    csv_candidates = glob.glob(f'CSV/Chara{ch_id}_*.csv') + glob.glob(f'CSV/Chara{ch_id:02d}_*.csv')
    com_candidates = glob.glob(f'ERB/CHAR/CHAR_{ch_id:02d}_*_COM.ERB') + glob.glob(f'ERB/CHAR/CHAR_{ch_id}_*_COM.ERB')
    if not csv_candidates or not com_candidates: continue
    csv_file = csv_candidates[0]
    com_file = com_candidates[0]
    
    cstr = {}
    with open(csv_file, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            m = re.match(r'^\s*CSTR\s*,\s*(8[0-4])\s*,\s*(.*)$', line)
            if m:
                cstr[int(m.group(1)) - 80] = m.group(2).strip()
                
    with open(com_file, 'r', encoding='cp932', errors='ignore') as f:
        com_text = f.read()
        
    narrs = {}
    for i in range(5):
        m = re.search(rf'@TRAIN_MESSAGE_B{280+i}_{ch_id}\b\s*\n(.*?)(?=@TRAIN_MESSAGE|\Z)', com_text, re.DOTALL)
        narrs[i] = m.group(1).strip() if m else ''
        
    dlgs = {}
    dlg_scenes = {}
    for i in range(5):
        m = re.search(rf'IF SELECTCOM == {280+i}\b(.*?)(?=(ELSEIF SELECTCOM|ELSE\b|ENDIF\b))', com_text, re.DOTALL)
        if m:
            block = m.group(1).strip()
            dlgs[i] = block
            scene_m = re.search(r'(場面:|--- COM28\d\s+)([^）\)\n\r\-]+)', block)
            dlg_scenes[i] = scene_m.group(2).strip() if scene_m else ''
        else:
            dlgs[i] = ''
            dlg_scenes[i] = ''

    # For each slot in Dlg (0..4), find best matching CSTR (0..4)
    dlg_to_cstr = {}
    for d_idx in range(5):
        d_text = dlg_scenes.get(d_idx, '') + ' ' + dlgs.get(d_idx, '')[:150]
        best_c = -1
        best_s = -1
        for c_idx in range(5):
            c_title = cstr.get(c_idx, '')
            c_kws = get_keywords(c_title)
            s = match_score(c_kws, d_text)
            if c_title and (c_title in d_text):
                s += 20
            if s > best_s:
                best_s = s
                best_c = c_idx
        dlg_to_cstr[d_idx] = best_c

    # For each slot in Narr (0..4), find best matching CSTR (0..4)
    narr_to_cstr = {}
    for n_idx in range(5):
        n_text = narrs.get(n_idx, '')
        best_c = -1
        best_s = -1
        for c_idx in range(5):
            c_title = cstr.get(c_idx, '')
            c_kws = get_keywords(c_title)
            s = match_score(c_kws, n_text)
            if c_title and (c_title in n_text):
                s += 20
            if s > best_s:
                best_s = s
                best_c = c_idx
        narr_to_cstr[n_idx] = best_c

    dlg_matches_cstr = (list(dlg_to_cstr.values()) == [0, 1, 2, 3, 4])
    narr_matches_cstr = (list(narr_to_cstr.values()) == [0, 1, 2, 3, 4])
    narr_matches_dlg = (list(narr_to_cstr.values()) == list(dlg_to_cstr.values()))

    status = 'OK' if (dlg_matches_cstr and narr_matches_cstr) else 'MISMATCH'
    report.append({
        'id': ch_id,
        'name': os.path.basename(csv_file),
        'status': status,
        'dlg_to_cstr': list(dlg_to_cstr.values()),
        'narr_to_cstr': list(narr_to_cstr.values()),
        'dlg_matches_cstr': dlg_matches_cstr,
        'narr_matches_cstr': narr_matches_cstr,
        'narr_matches_dlg': narr_matches_dlg
    })

print(f'Total: {len(report)}')
ok_count = sum(1 for r in report if r['status'] == 'OK')
print(f'OK: {ok_count}, Mismatched: {len(report) - ok_count}')

narr_wrong_only = sum(1 for r in report if r['dlg_matches_cstr'] and not r['narr_matches_cstr'])
cstr_wrong_only = sum(1 for r in report if not r['dlg_matches_cstr'] and r['narr_matches_dlg'])
other_wrong = sum(1 for r in report if r['status'] == 'MISMATCH' and not (r['dlg_matches_cstr'] and not r['narr_matches_cstr']) and not (not r['dlg_matches_cstr'] and r['narr_matches_dlg']))

print(f'Category 1 (Dlg matches CSTR, but Narration is shuffled): {narr_wrong_only}')
print(f'Category 2 (Narration and Dlg match each other, but CSTR is shuffled): {cstr_wrong_only}')
print(f'Category 3 (Other / more complex shuffle): {other_wrong}')

with open('tools/era_angal_work/misc/detailed_classification.txt', 'w', encoding='utf-8') as out:
    for r in report:
        out.write(f'Chara {r["id"]:02d} ({r["name"]}): {r["status"]}\n')
        out.write(f'  Dlg -> CSTR:  {r["dlg_to_cstr"]} (matches CSTR: {r["dlg_matches_cstr"]})\n')
        out.write(f'  Narr -> CSTR: {r["narr_to_cstr"]} (matches CSTR: {r["narr_matches_cstr"]})\n')
        out.write(f'  Narr == Dlg:  {r["narr_matches_dlg"]}\n\n')
print('Detailed report written to tools/era_angal_work/misc/detailed_classification.txt')
