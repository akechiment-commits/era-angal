import os
import re

target_files = [
    'ERB/DECK_BATTLE_戦闘.ERB',
    'ERB/EVENT_BOARD_イベントボード.ERB',
    'ERB/GACHA_ガチャシステム.ERB',
    'ERB/SUGOROKU_すごろく.ERB',
    'ERB/CARD_COLLECTION_カードコレクション.ERB',
    'ERB/STAGE_学校生活・システム.ERB',
    'ERB/INFO_情報表示.ERB',
    'ERB/SHOP_ショップ.ERB',
    'ERB/SHOP_ITEM_ショップアイテム定義.ERB',
    'ERB/TRAIN.ERB',
]

issues = []

for rel_path in target_files:
    if not os.path.exists(rel_path):
        # find matching file
        base = os.path.basename(rel_path).split('_')[0]
        found = False
        for root, dirs, files in os.walk('ERB'):
            for f in files:
                if f.startswith(base) and f.endswith('.ERB'):
                    rel_path = os.path.join(root, f)
                    found = True
                    break
            if found: break
    if not os.path.exists(rel_path):
        continue

    with open(rel_path, 'r', encoding='cp932') as fp:
        lines = fp.readlines()

    for idx, line in enumerate(lines, 1):
        clean = line.split(';')[0].strip()
        if not clean:
            continue
            
        # 1. Check for missing quotes in PRINTFORM
        # 2. Check for SIF followed by PRINT and missing indentation/line
        # 3. Check for obvious typos: e.g. TFLG instead of TFLAG, FLG instead of FLAG
        for typo in ['TFLG:', 'CFLG:', 'FLG:', 'EX:', 'AB:', 'TALEN:', 'ITM:']:
            if typo in clean:
                issues.append((rel_path, idx, f'Suspicious variable typo: {typo}', clean))
                
        # 4. Check for RESULT without assignment or invalid input loops
        if clean == 'INPUT' and idx < len(lines):
            # check next line
            pass

print(f'Total issues found: {len(issues)}')
for p, l, kind, txt in issues:
    print(f'{p}:{l}: {kind} -> {txt}')
