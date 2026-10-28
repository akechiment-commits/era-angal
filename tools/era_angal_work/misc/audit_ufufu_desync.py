import os, glob, re, sys

report = []

for ch_id in range(1, 73):
    csv_candidates = glob.glob(f'CSV/Chara{ch_id}_*.csv') + glob.glob(f'CSV/Chara{ch_id:02d}_*.csv')
    if not csv_candidates: continue
    csv_file = csv_candidates[0]
    
    cstr = {}
    with open(csv_file, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            m = re.match(r'^\s*CSTR\s*,\s*(8[0-4])\s*,\s*(.*)$', line)
            if m:
                cstr[int(m.group(1)) - 80] = m.group(2).strip()
                
    com_candidates = glob.glob(f'ERB/CHAR/CHAR_{ch_id:02d}_*_COM.ERB') + glob.glob(f'ERB/CHAR/CHAR_{ch_id}_*_COM.ERB')
    if not com_candidates: continue
    com_file = com_candidates[0]
    
    with open(com_file, 'r', encoding='cp932', errors='ignore') as f:
        com_text = f.read()
        
    narrs = {}
    for i in range(5):
        com_num = 280 + i
        m = re.search(rf'@TRAIN_MESSAGE_B{com_num}_{ch_id}\b\s*\n(.*?)(?=@TRAIN_MESSAGE|\Z)', com_text, re.DOTALL)
        if m:
            narrs[i] = m.group(1).strip()
        else:
            narrs[i] = ''
            
    dlgs = {}
    dlg_scenes = {}
    for i in range(5):
        com_num = 280 + i
        m = re.search(rf'IF SELECTCOM == {com_num}\b(.*?)(?=(ELSEIF SELECTCOM|ELSE\b|ENDIF\b))', com_text, re.DOTALL)
        if m:
            block = m.group(1)
            dlgs[i] = block.strip()
            scene_m = re.search(r'場面:\s*([^）\)\n]+)', block)
            dlg_scenes[i] = scene_m.group(1).strip() if scene_m else ''
        else:
            dlgs[i] = ''
            dlg_scenes[i] = ''
            
    ch_mismatches = []
    has_desync = False
    for i in range(5):
        c_name = cstr.get(i, '')
        d_scene = dlg_scenes.get(i, '')
        narr = narrs.get(i, '').replace('\n', ' ')
        
        scene_match = [k for k, v in cstr.items() if v and (v in d_scene or d_scene in v)]
        
        narr_matches = []
        for k, v in cstr.items():
            k_words = [w for w in re.split(r'[の・で中にをとへがは]', v) if len(w) >= 2]
            if any(w in narr for w in k_words):
                narr_matches.append(k)
                
        if d_scene and d_scene != c_name:
            has_desync = True
        elif narr_matches and i not in narr_matches:
            has_desync = True
            
        ch_mismatches.append({
            'idx': i,
            'com': 280 + i,
            'cstr': c_name,
            'scene': d_scene,
            'narr': narr[:50],
            'scene_match': scene_match,
            'narr_matches': narr_matches
        })
        
    if has_desync:
        report.append((ch_id, os.path.basename(csv_file), com_file, cstr, ch_mismatches))

print(f'Total characters with detected desync: {len(report)} / 72')
os.makedirs('tools/era_angal_work/misc', exist_ok=True)
with open('tools/era_angal_work/misc/ufufu_desync_report.txt', 'w', encoding='utf-8') as out:
    out.write(f'Total characters with detected desync: {len(report)} / 72\n\n')
    for ch_id, csv_name, com_file, cstr, mismatches in report:
        out.write(f'=== Chara {ch_id}: {csv_name} ===\n')
        for m in mismatches:
            out.write(f'  COM{m["com"]}: CSTR="{m["cstr"]}" | Scene="{m["scene"]}"\n')
            out.write(f'    Narr: {m["narr"]}\n')
            out.write(f'    Scene match: {m["scene_match"]}, Narr match: {m["narr_matches"]}\n')
        out.write('\n')
print('Report written to tools/era_angal_work/misc/ufufu_desync_report.txt')
