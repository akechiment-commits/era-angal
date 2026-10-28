import os, glob, re

def get_keywords(text):
    return set(re.findall(r'[\u4e00-\u9fff\u30a0-\u30ff]{2,}', text))

def match_score(kws, text):
    if not kws or not text: return 0
    t_kws = get_keywords(text)
    score = len(kws & t_kws) * 3
    for w in kws:
        if w in text:
            score += 5
    return score

unresolved = []
perfect_mappings = []

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

    # Let's verify mapping for this character:
    # Anchor: Dialogue slot i (0..4)
    # Target: Find matching Narration slot j (0..4) and matching CSTR slot k (0..4)
    
    # 1. Match CSTR to Dlg
    # In 52+ characters, CSTR[i] already matches Dlg[i].
    dlg_to_cstr = {}
    used_c = set()
    # First pass: exact title match
    for d_idx in range(5):
        d_scene = dlg_scenes.get(d_idx, '')
        for c_idx in range(5):
            if c_idx not in used_c and cstr.get(c_idx) == d_scene and d_scene:
                dlg_to_cstr[d_idx] = c_idx
                used_c.add(c_idx)
                break
    # Second pass: keyword score
    for d_idx in range(5):
        if d_idx in dlg_to_cstr: continue
        d_text = dlg_scenes.get(d_idx, '') + ' ' + dlgs.get(d_idx, '')[:200]
        best_c = -1
        best_s = -1
        for c_idx in range(5):
            if c_idx in used_c: continue
            c_title = cstr.get(c_idx, '')
            s = match_score(get_keywords(c_title), d_text)
            if s > best_s:
                best_s = s
                best_c = c_idx
        if best_c != -1 and best_s > 0:
            dlg_to_cstr[d_idx] = best_c
            used_c.add(best_c)
        else:
            # Fallback to remaining
            rem = [c for c in range(5) if c not in used_c]
            if rem:
                dlg_to_cstr[d_idx] = rem[0]
                used_c.add(rem[0])

    # 2. Match Narration to Dlg
    dlg_to_narr = {}
    used_n = set()
    for d_idx in range(5):
        d_scene = dlg_scenes.get(d_idx, '')
        c_title = cstr.get(dlg_to_cstr.get(d_idx, -1), '')
        target_kws = get_keywords(d_scene) | get_keywords(c_title)
        best_n = -1
        best_s = -1
        for n_idx in range(5):
            if n_idx in used_n: continue
            n_text = narrs.get(n_idx, '')
            s = match_score(target_kws, n_text)
            # also check similarity with dlg text
            s += match_score(get_keywords(dlgs.get(d_idx, '')[:150]), n_text)
            if s > best_s:
                best_s = s
                best_n = n_idx
        if best_n != -1 and best_s > 0:
            dlg_to_narr[d_idx] = best_n
            used_n.add(best_n)
        else:
            rem = [n for n in range(5) if n not in used_n]
            if rem:
                dlg_to_narr[d_idx] = rem[0]
                used_n.add(rem[0])

    is_bijective = (len(set(dlg_to_cstr.values())) == 5 and len(set(dlg_to_narr.values())) == 5)
    if is_bijective:
        perfect_mappings.append((ch_id, os.path.basename(csv_file), dlg_to_cstr, dlg_to_narr))
    else:
        unresolved.append((ch_id, os.path.basename(csv_file), dlg_to_cstr, dlg_to_narr))

print(f'Bijective mappings successfully formed: {len(perfect_mappings)} / 72')
print(f'Unresolved: {len(unresolved)}')
if unresolved:
    for u in unresolved:
        print(u)
