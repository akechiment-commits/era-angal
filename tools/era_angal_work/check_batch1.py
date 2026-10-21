# -*- coding: utf-8 -*-
import os, glob, re

# Inspect CHAR 01 to 12
chara_fps = {
    1: '私',      # 三善かなえ
    2: 'わたし',  # 北川ゆき
    3: 'わたし',  # 小野ちよ
    4: 'あたし',  # 早川きこ
    5: 'あたし',  # 桃智あすか
    6: 'わたし',  # 藍乃あいか
    7: 'あたし',  # 高原ちあき
    8: 'あたし',  # 丸子みさき
    9: 'あたし',  # 月永るか
    10: 'わたし', # 木之下ゆゆ
    11: 'わたし', # 氷野くるみ
    12: 'あたし'  # 神樹いちか
}

all_fps = ['私', 'わたし', 'あたし', 'あたい', 'ボク', 'ぼく', '僕', 'うち', 'ウチ', 'オラ', 'おら', '俺', 'おれ', 'わたくし']

results = []

for cid in range(1, 13):
    expected_fp = chara_fps[cid]
    wrong_fps = [fp for fp in all_fps if fp != expected_fp]
    # some exceptions: e.g. わたし / 私 might be kanji variation, but let's check
    
    files = glob.glob(f'ERB/CHAR/CHAR_{cid:02d}_*.ERB')
    for fpath in files:
        fname = os.path.basename(fpath)
        is_com = '_COM' in fname
        with open(fpath, 'r', encoding='cp932') as fp:
            lines = fp.readlines()
            
        current_com = None
        current_func = None
        
        # Track multiline dialogue blocks for bracket check
        in_dialogue = False
        dialogue_buf = []
        dialogue_start_line = 0
        
        for idx, line in enumerate(lines, 1):
            line_str = line.strip()
            
            if line_str.startswith('@'):
                current_func = line_str
                
            com_m = re.search(r'SELECTCOM\s*==\s*(\d+)', line_str)
            if com_m:
                current_com = int(com_m.group(1))
                
            is_print = re.match(r'(?:PRINTFORMW?|PRINTL?W?)\s+(.*)', line_str)
            if is_print:
                content = is_print.group(1)
                if content.startswith('@"') and content.endswith('"'):
                    content = content[2:-1]
                elif content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                    
                # 1. Punctuation & substitution anomalies
                if '先輩先輩' in content:
                    results.append((cid, fname, idx, current_com, '重複敬称「先輩先輩」', content))
                if 'さんさん' in content:
                    results.append((cid, fname, idx, current_com, '重複敬称「さんさん」', content))
                if '%LOCALS%さん' in content:
                    results.append((cid, fname, idx, current_com, '重複敬称「%LOCALS%さん」', content))
                if '。、' in content:
                    results.append((cid, fname, idx, current_com, '句読点異常「。、」', content))
                if '、、' in content:
                    results.append((cid, fname, idx, current_com, '読点重複「、、」', content))
                    
                # 2. Viewpoint reversal
                if is_com and current_com == 312:
                    # 頭を撫でる
                    if re.search(r'(?:撫でてあげる|撫でてやる|よしよししてあげる|よしよし、|よしよし♪|いいこいいこ)', content):
                        results.append((cid, fname, idx, current_com, 'COM312視点逆転(TARGETが撫でる側)', content))
                elif is_com and current_com == 307:
                    # 櫛で梳かす
                    if re.search(r'(?:梳いてあげる|梳いてやる|とかしてあげる|とかしてやる|髪を梳いてあげる)', content):
                        results.append((cid, fname, idx, current_com, 'COM307視点逆転(TARGETが梳かす側)', content))
                elif is_com and current_com == 60:
                    # 助手にキスさせる
                    # Check if TARGET says she is being kissed instead of kissing ASSI
                    pass
                    
                # 3. First person check (inside speech brackets 「...」)
                speech_matches = re.findall(r'「([^」]*)」?', content)
                for sp in speech_matches:
                    for wfp in wrong_fps:
                        # Be careful about context: e.g. "ボクサー", "私生活", "うちの部"
                        if wfp in ['うち', 'ウチ'] and re.search(r'うちの(?:部|クラス|学校|親|家|部屋|チーム|生徒|仲間)', sp):
                            continue
                        # "僕たち" etc.
                        # Check standalone pronoun pattern
                        p_regex = re.compile(rf'(?<![ぁ-んァ-ヶ一-龠]){re.escape(wfp)}(?=[はがをにものでと、。！？…―\s])')
                        if p_regex.search(sp):
                            # Ignore kanji variation between 私 and わたし if minor, but let's record
                            if {expected_fp, wfp} == {'私', 'わたし'}:
                                continue
                            results.append((cid, fname, idx, current_com, f'一人称ブレ(想定:{expected_fp}, 検出:{wfp})', content))

with open('tools/era_angal_work/batch1_results.txt', 'w', encoding='utf-8') as out:
    out.write(f"=== BATCH 1 (CHAR 01-12) CHECK RESULTS ({len(results)} issues) ===\n\n")
    for cid, fname, lnum, com, desc, text in results:
        com_s = f"[COM{com}] " if com else ""
        out.write(f"CHAR_{cid:02d} | {fname}:{lnum} | {com_s}{desc}\n")
        out.write(f"  Text: {text}\n\n")

print(f"Batch 1 check finished: {len(results)} issues found.")
