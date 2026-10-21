# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

# 1. Load Chara Master (ID, Name, Callname, First person)
chara_roster = {}
with open('tools/era_angal_work/actual_csv_charas.txt', 'r', encoding='utf-8') as fp:
    for l in fp:
        m = re.match(r'(\d+):\s*(.*?)\s*\((.*?)\)', l.strip())
        if m:
            cid = int(m.group(1))
            name = m.group(2).strip()
            cname = m.group(3).strip()
            chara_roster[cid] = {'name': name, 'cname': cname}

# Load first-person pronoun per chara from ledger
# Let's inspect tools/キャラ資料/呼称定義台帳_20261014.md for first-person
first_person_map = {}
with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'r', encoding='utf-8') as fp:
    text = fp.read()
    # matches like: ### CHAR_01 三善かなえ ... 一人称: 「私」
    for m in re.finditer(r'### CHAR_(\d+)[^\n]*\n.*?一人称[：:\s]*[「『]?([^」』\n、]+)[」』]?', text, re.DOTALL):
        cid = int(m.group(1))
        fp_str = m.group(2).strip()
        first_person_map[cid] = fp_str

print(f"Loaded {len(first_person_map)} first-person mappings.")

# Scan all kojo ERB files in ERB/CHAR/
kojo_files = glob.glob('ERB/CHAR/CHAR_*.ERB')
print(f"Total kojo ERB files found: {len(kojo_files)}")

issues = defaultdict(list)

# Common regex patterns for syntax / punctuation issues
PUNCT_PATTERNS = [
    (r'[。][、]', '句読点混入「。、」'),
    (r'[、]{2,}', '読点連続「、、」'),
    (r'[。]{2,}', '句点連続「。。」'),
    (r'[！？][、]', '感嘆符後読点「！、」「？、」'),
    (r'(?:さんさん|先輩先輩|ちゃんちゃん|様様|殿殿)', '重複敬称（置換痕跡）'),
    (r'%LOCALS%さん', '%LOCALS%に重複敬称'),
    (r'%%', '不正な二重パーセント')
]

for fpath in kojo_files:
    fname = os.path.basename(fpath)
    m = re.match(r'CHAR_(\d+)_(.*?)(\.ERB|_COM\.ERB)', fname)
    if not m:
        continue
    cid = int(m.group(1))
    cname = m.group(2)
    is_com = '_COM' in fname

    try:
        with open(fpath, 'r', encoding='cp932') as fp:
            lines = fp.readlines()
    except Exception as e:
        issues[cid].append({'type': 'ENCODING', 'file': fname, 'line': 0, 'desc': f'CP932 decode error: {e}'})
        continue

    current_com = None
    for line_idx, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()

        # Track COM command
        com_m = re.search(r'SELECTCOM\s*==\s*(\d+)', line)
        if com_m:
            current_com = int(com_m.group(1))

        # Only inspect dialogue output lines
        if not re.match(r'(?:PRINTFORMW?|PRINTL?W?)\s+.*', line):
            continue

        # Extract text content inside quotes if present
        text_content = line
        quote_m = re.search(r'PRINTFORMW?\s+(?:@?"(.*)"|@?(.*))', line)
        if quote_m:
            text_content = quote_m.group(1) or quote_m.group(2) or ''

        # 1. Bracket mismatch
        open_kagi = text_content.count('「')
        close_kagi = text_content.count('」')
        if open_kagi != close_kagi:
            issues[cid].append({
                'type': 'BRACKET_MISMATCH',
                'file': fname,
                'line': line_idx,
                'com': current_com,
                'text': text_content[:80],
                'desc': f'カギカッコ不整合 (「={open_kagi}, 」={close_kagi})'
            })

        # 2. Punctuation & substitution anomalies
        for pat, desc in PUNCT_PATTERNS:
            if re.search(pat, text_content):
                issues[cid].append({
                    'type': 'PUNCTUATION',
                    'file': fname,
                    'line': line_idx,
                    'com': current_com,
                    'text': text_content[:80],
                    'desc': desc
                })

        # 3. Viewpoint reversal checks on specific COMs
        if is_com and current_com is not None:
            # COM 312: 頭を撫でる (PLAYER -> TARGET). TARGET should NOT say "撫でてあげる", "撫でてやる", "よしよし" to PLAYER
            if current_com == 312:
                if re.search(r'(?:撫でてあげる|撫でてやる|よしよし|いいこいいこ)', text_content):
                    issues[cid].append({
                        'type': 'VIEWPOINT_REVERSAL',
                        'file': fname,
                        'line': line_idx,
                        'com': 312,
                        'text': text_content[:80],
                        'desc': 'COM312(頭を撫でる)でTARGET側が撫でるセリフになっている疑い'
                    })
            # COM 307: 櫛で梳かす (PLAYER -> TARGET). TARGET should NOT say "梳いてあげる", "梳いてやる"
            elif current_com == 307:
                if re.search(r'(?:梳いてあげる|梳いてやる|とかしてあげる|とかしてやる)', text_content):
                    issues[cid].append({
                        'type': 'VIEWPOINT_REVERSAL',
                        'file': fname,
                        'line': line_idx,
                        'com': 307,
                        'text': text_content[:80],
                        'desc': 'COM307(櫛で梳かす)でTARGET側が梳くセリフになっている疑い'
                    })
            # COM 60: 助手にキスさせる (PLAYER orders ASSI and TARGET to kiss). Check if TARGET or ASSI confused
            elif current_com == 60:
                pass

print(f"Scan finished. Total characters with detected issues: {len(issues)}")

total_issues_count = sum(len(v) for v in issues.values())
print(f"Total issue instances: {total_issues_count}")

with open('tools/era_angal_work/kojo_scan_initial_results.txt', 'w', encoding='utf-8') as out:
    out.write(f"=== KOJO COMPREHENSIVE SCAN RESULTS ({total_issues_count} issues across {len(issues)} characters) ===\n\n")
    for cid in sorted(issues.keys()):
        ch_name = chara_roster.get(cid, {}).get('name', f'CHAR_{cid}')
        c_issues = issues[cid]
        out.write(f"### CHAR_{cid:02d} {ch_name} ({len(c_issues)} issues)\n")
        for iss in c_issues:
            com_info = f"[COM{iss.get('com')}] " if iss.get('com') else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_info}{iss['desc']}\n")
            out.write(f"      Text: {iss['text']}\n")
        out.write("\n")

print("Wrote tools/era_angal_work/kojo_scan_initial_results.txt successfully!")
