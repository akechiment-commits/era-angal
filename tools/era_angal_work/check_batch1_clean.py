# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

# Official Primary First-Person Dictionary based on statistical analysis of all scenarios
OFFICIAL_FPS = {
    1: '私', 2: 'わたし', 3: 'わたし', 4: 'あたし', 5: 'あたし', 6: 'わたし',
    7: 'あたし', 8: 'あたし', 9: 'ぼく', 10: 'わたし', 11: 'わたし', 12: 'あたし',
    13: 'あたし', 14: 'おら', 15: 'あたし', 16: 'あたい', 17: 'わたし', 18: 'わたし',
    19: 'あたし', 20: 'わたし', 21: 'わたし', 22: 'あたし', 23: 'わたし', 24: 'わたし',
    25: 'わたし', 26: 'あたし', 27: 'わたし', 28: 'うち', 29: 'あたし', 30: 'わたし',
    31: 'わたくし', 32: 'あたし', 33: 'ウチ', 34: 'わたし', 35: 'あたし', 36: 'わたし',
    37: '私', 38: '私', 39: 'あたし', 40: 'あたし', 41: 'わたし', 42: '私',
    43: 'わたし', 44: 'わたし', 45: 'わたくし', 46: 'わたし', 47: 'わたし', 48: '僕',
    49: 'わたし', 50: 'あたし', 51: 'わたし', 52: 'あたし', 53: 'あたし', 54: 'あたし',
    55: 'わたし', 56: '俺', 57: 'あたし', 58: 'あたし', 59: 'わたし', 60: 'あたし',
    61: '私', 62: 'ボク', 63: 'わたし', 64: '私', 65: 'わたし', 66: 'あたし',
    67: '私', 68: 'あたし', 69: 'わたし', 70: 'あたし', 71: 'うち', 72: 'わたし'
}

# Equivalent variations that are acceptable
ALLOWED_VARIANTS = {
    '私': ['私', 'わたし'],
    'わたし': ['わたし', '私'],
    'あたし': ['あたし'],
    'あたい': ['あたい'],
    'ぼく': ['ぼく', '僕', 'ボク'],
    '僕': ['僕', 'ぼく', 'ボク'],
    'ボク': ['ボク', 'ぼく', '僕'],
    'おら': ['おら', 'オラ'],
    'うち': ['うち', 'ウチ'],
    'ウチ': ['ウチ', 'うち'],
    '俺': ['俺', 'おれ', 'オレ'],
    'わたくし': ['わたくし']
}

ALL_PRONOUNS = ['私', 'わたし', 'あたし', 'あたい', 'ボク', 'ぼく', '僕', 'うち', 'ウチ', 'オラ', 'おら', '俺', 'おれ', 'オレ', 'わたくし']

def check_batch(start_id, end_id):
    results = defaultdict(list)
    for cid in range(start_id, end_id + 1):
        expected_fp = OFFICIAL_FPS.get(cid, 'わたし')
        allowed = ALLOWED_VARIANTS.get(expected_fp, [expected_fp])
        wrong_fps = [p for p in ALL_PRONOUNS if p not in allowed]
        
        files = glob.glob(f'ERB/CHAR/CHAR_{cid:02d}_*.ERB')
        for fpath in files:
            fname = os.path.basename(fpath)
            is_com = '_COM' in fname
            with open(fpath, 'r', encoding='cp932') as fp:
                lines = fp.readlines()
                
            current_com = None
            for idx, line in enumerate(lines, 1):
                line_str = line.strip()
                
                com_m = re.search(r'SELECTCOM\s*==\s*(\d+)', line_str)
                if com_m:
                    current_com = int(com_m.group(1))
                    
                is_print = re.match(r'(?:PRINTFORMW?|PRINTL?W?)\s+(.*)', line_str)
                if not is_print:
                    continue
                    
                content = is_print.group(1)
                if content.startswith('@"') and content.endswith('"'):
                    content = content[2:-1]
                elif content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                    
                # 1. Duplicate honorifics / replacement residues
                if re.search(r'(?:先輩先輩|さんさん|ちゃんちゃん|様様|殿殿)', content):
                    results[cid].append({
                        'file': fname, 'line': idx, 'com': current_com,
                        'type': '重複敬称', 'text': content,
                        'desc': '置換痕跡による敬称重複'
                    })
                if '%LOCALS%さん' in content:
                    results[cid].append({
                        'file': fname, 'line': idx, 'com': current_com,
                        'type': '%LOCALS%重複敬称', 'text': content,
                        'desc': '%LOCALS%に余計な「さん」が付着'
                    })
                if re.search(r'[。][、]', content):
                    results[cid].append({
                        'file': fname, 'line': idx, 'com': current_com,
                        'type': '句読点異常', 'text': content,
                        'desc': '「。、」の混入'
                    })
                if re.search(r'[、]{2,}', content):
                    results[cid].append({
                        'file': fname, 'line': idx, 'com': current_com,
                        'type': '読点連続', 'text': content,
                        'desc': '「、、」の重複'
                    })
                    
                # 2. Viewpoint reversal
                if is_com and current_com == 312:
                    # 頭を撫でる (PLAYER -> TARGET)
                    if re.search(r'(?:撫でてあげる|撫でてやる|よしよししてあげる|よしよし、|よしよし♪|いいこいいこ)', content):
                        results[cid].append({
                            'file': fname, 'line': idx, 'com': current_com,
                            'type': '視点逆転', 'text': content,
                            'desc': 'COM312(頭を撫でる)でTARGET側が撫でるセリフになっている'
                        })
                elif is_com and current_com == 307:
                    # 櫛で梳かす (PLAYER -> TARGET)
                    if re.search(r'(?:梳いてあげる|梳いてやる|とかしてあげる|とかしてやる)', content):
                        results[cid].append({
                            'file': fname, 'line': idx, 'com': current_com,
                            'type': '視点逆転', 'text': content,
                            'desc': 'COM307(櫛で梳かす)でTARGET側が梳かすセリフになっている'
                        })
                        
                # 3. First person breakdown inside dialogue
                speech_matches = re.findall(r'「([^」]*)」?', content)
                for sp in speech_matches:
                    for wfp in wrong_fps:
                        if wfp in ['うち', 'ウチ'] and re.search(r'うちの(?:部|クラス|学校|親|家|部屋|チーム|生徒|仲間|子)', sp):
                            continue
                        if re.search(rf'(?<![ぁ-んァ-ヶ一-龠]){re.escape(wfp)}(?=[はがをにものでと、。！？…―\s])', sp):
                            results[cid].append({
                                'file': fname, 'line': idx, 'com': current_com,
                                'type': '一人称ブレ', 'text': content,
                                'desc': f'想定一人称「{expected_fp}」と異なる「{wfp}」が混入'
                            })
                            break
    return results

# Check Batch 1: CHAR 01 - 12
b1_issues = check_batch(1, 12)
total_b1 = sum(len(v) for v in b1_issues.values())
print(f"Batch 1 (CHAR 01-12) Total issues: {total_b1}")

with open('tools/era_angal_work/batch1_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b1_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b1_issues[cid])} issues)\n")
        for iss in b1_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch1_clean_report.txt successfully!")
