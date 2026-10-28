import os, glob, re, sys

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

total_updated_csv = 0
total_updated_erb = 0

for ch_id in range(1, 73):
    csv_candidates = glob.glob(f'CSV/Chara{ch_id}_*.csv') + glob.glob(f'CSV/Chara{ch_id:02d}_*.csv')
    com_candidates = glob.glob(f'ERB/CHAR/CHAR_{ch_id:02d}_*_COM.ERB') + glob.glob(f'ERB/CHAR/CHAR_{ch_id}_*_COM.ERB')
    if not csv_candidates or not com_candidates: continue
    csv_file = csv_candidates[0]
    com_file = com_candidates[0]
    
    # Read CSV
    with open(csv_file, 'r', encoding='cp932', errors='ignore') as f:
        csv_lines = f.readlines()
        
    cstr = {}
    for line in csv_lines:
        m = re.match(r'^\s*CSTR\s*,\s*(8[0-4])\s*,\s*(.*)$', line)
        if m:
            cstr[int(m.group(1)) - 80] = m.group(2).strip()
            
    # Read COM
    with open(com_file, 'r', encoding='cp932', errors='ignore') as f:
        com_text = f.read()
        
    # Extract original narrations
    narr_blocks = {}
    narr_texts = {}
    for i in range(5):
        com_num = 280 + i
        # match entire function from header to next function
        m = re.search(rf'(@TRAIN_MESSAGE_B{com_num}_{ch_id}\b\s*\n(.*?))(?=@TRAIN_MESSAGE|\Z)', com_text, re.DOTALL)
        if m:
            narr_blocks[i] = m.group(2).strip() # just body
            narr_texts[i] = m.group(2).strip()
        else:
            narr_blocks[i] = ''
            narr_texts[i] = ''
            
    # Extract dialogues and scene labels
    dlgs = {}
    dlg_scenes = {}
    for i in range(5):
        com_num = 280 + i
        m = re.search(rf'IF SELECTCOM == {com_num}\b(.*?)(?=(ELSEIF SELECTCOM|ELSE\b|ENDIF\b))', com_text, re.DOTALL)
        if m:
            block = m.group(1).strip()
            dlgs[i] = block
            scene_m = re.search(r'(場面:|--- COM28\d\s+)([^）\)\n\r\-]+)', block)
            dlg_scenes[i] = scene_m.group(2).strip() if scene_m else ''
        else:
            dlgs[i] = ''
            dlg_scenes[i] = ''

    # 1. Match CSTR to Dlg
    dlg_to_cstr = {}
    used_c = set()
    for d_idx in range(5):
        d_scene = dlg_scenes.get(d_idx, '')
        for c_idx in range(5):
            if c_idx not in used_c and cstr.get(c_idx) == d_scene and d_scene:
                dlg_to_cstr[d_idx] = c_idx
                used_c.add(c_idx)
                break
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
            n_text = narr_texts.get(n_idx, '')
            s = match_score(target_kws, n_text)
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

    # Check if update is needed
    csv_needs_update = (list(dlg_to_cstr.values()) != [0, 1, 2, 3, 4])
    erb_needs_update = (list(dlg_to_narr.values()) != [0, 1, 2, 3, 4])

    if csv_needs_update:
        # Update CSTR,80-84 in CSV
        new_csv_lines = []
        for line in csv_lines:
            m = re.match(r'^\s*CSTR\s*,\s*(8[0-4])\s*,\s*(.*)$', line)
            if m:
                slot = int(m.group(1)) - 80
                # What should be at slot?
                # At slot i, we want the CSTR that corresponds to dlg slot i:
                c_idx = dlg_to_cstr[slot]
                new_title = cstr[c_idx]
                new_csv_lines.append(f'CSTR,{80+slot},{new_title}\r\n')
            else:
                new_csv_lines.append(line if line.endswith('\r\n') else line.rstrip('\r\n') + '\r\n')
        with open(csv_file, 'w', encoding='cp932', newline='') as f:
            f.writelines(new_csv_lines)
        total_updated_csv += 1

    if erb_needs_update:
        # In com_text, replace the bodies of @TRAIN_MESSAGE_B280_{ch_id} to B284_{ch_id}
        # We can construct the new section
        new_com_text = com_text
        for slot in range(5):
            com_num = 280 + slot
            target_n_idx = dlg_to_narr[slot]
            new_body = narr_blocks[target_n_idx]
            
            # Find and replace old body
            pattern = rf'(@TRAIN_MESSAGE_B{com_num}_{ch_id}\b\s*\r?\n)(.*?)(?=\r?\n@TRAIN_MESSAGE|\r?\n;|\Z)'
            
            def make_repl(m, b=new_body):
                return m.group(1) + '\t' + b
                
            new_com_text = re.sub(pattern, make_repl, new_com_text, count=1, flags=re.DOTALL)
            
        with open(com_file, 'w', encoding='cp932', newline='\r\n') as f:
            f.write(new_com_text)
        total_updated_erb += 1

print(f'Sync completed!')
print(f'Total CSV files updated: {total_updated_csv}')
print(f'Total ERB files updated: {total_updated_erb}')
