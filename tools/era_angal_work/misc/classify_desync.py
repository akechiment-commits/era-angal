import os, glob, re

def get_keywords(text):
    # extract kanji/katakana words >= 2 chars
    return set(re.findall(r'[\u4e00-\u9fff\u30a0-\u30ff]{2,}', text))

results = []

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
            # scene comment or header
            scene_m = re.search(r'(場面:|--- COM28\d\s+)([^）\)\n\r\-]+)', block)
            dlg_scenes[i] = scene_m.group(2).strip() if scene_m else ''
        else:
            dlgs[i] = ''
            dlg_scenes[i] = ''

    results.append({
        'id': ch_id,
        'csv_file': csv_file,
        'com_file': com_file,
        'cstr': cstr,
        'narrs': narrs,
        'dlgs': dlgs,
        'dlg_scenes': dlg_scenes
    })

print(f'Loaded {len(results)} characters.')

# Now for each character, let's identify the 5 scenes and what slot they are in for:
# 1. CSTR (CSV)
# 2. Narration
# 3. Dialogue
# Let's see how many characters have exact match between all 3!
perfect = 0
mismatched = []

for r in results:
    ch_id = r['id']
    cstr = r['cstr']
    narrs = r['narrs']
    dlg_scenes = r['dlg_scenes']
    
    # Map each slot 0..4 in CSTR to a scene label
    # Check if Narration 0..4 matches CSTR 0..4
    # Check if Dialogue 0..4 matches CSTR 0..4
    # We can do this by computing keyword similarity
    narr_matches = {}
    dlg_matches = {}
    
    for i in range(5):
        c_title = cstr.get(i, '')
        c_kw = get_keywords(c_title)
        
        # Check narrs
        best_narr = -1
        best_narr_score = 0
        for ni in range(5):
            n_text = narrs.get(ni, '')
            n_kw = get_keywords(n_text)
            score = len(c_kw & n_kw)
            if any(w in n_text for w in c_kw):
                score += 5
            if score > best_narr_score:
                best_narr_score = score
                best_narr = ni
        narr_matches[i] = best_narr
        
        # Check dlgs
        best_dlg = -1
        best_dlg_score = 0
        for di in range(5):
            d_scene = dlg_scenes.get(di, '')
            d_text = r['dlgs'].get(di, '')
            score = 0
            if c_title and (c_title in d_scene or d_scene in c_title):
                score += 10
            d_kw = get_keywords(d_scene) | get_keywords(d_text[:200])
            score += len(c_kw & d_kw)
            if score > best_dlg_score:
                best_dlg_score = score
                best_dlg = di
        dlg_matches[i] = best_dlg

    # Check if 1:1 identity
    is_identity = (
        all(narr_matches.get(i) == i for i in range(5)) and
        all(dlg_matches.get(i) == i for i in range(5))
    )
    if is_identity:
        perfect += 1
    else:
        mismatched.append({
            'id': ch_id,
            'name': os.path.basename(r['csv_file']),
            'cstr': cstr,
            'narr_perm': [narr_matches.get(i) for i in range(5)],
            'dlg_perm': [dlg_matches.get(i) for i in range(5)],
            'dlg_scenes': dlg_scenes,
            'narrs': [narrs.get(i, '')[:40] for i in range(5)]
        })

print(f'Perfect match: {perfect} / {len(results)}')
print(f'Mismatched: {len(mismatched)} / {len(results)}')

with open('tools/era_angal_work/misc/mismatched_summary.txt', 'w', encoding='utf-8') as out:
    for m in mismatched:
        out.write(f'Chara {m["id"]}: {m["name"]}\n')
        out.write(f'  CSTR:       {m["cstr"]}\n')
        out.write(f'  Dlg scenes: {m["dlg_scenes"]}\n')
        out.write(f'  Narr match: {m["narr_perm"]}\n')
        out.write(f'  Dlg match:  {m["dlg_perm"]}\n\n')
print('Summary written to tools/era_angal_work/misc/mismatched_summary.txt')
