# -*- coding: utf-8 -*-
# 全実装キャラの @KOJO_JUN_Kxx の TFLAG:600 == 3 分岐に「無下に断る」欄(空)を追加。
# 既存セリフ=保留(TFLAG:601==1)に温存、無下(else)に空 PRINTFORMW 「」 を新設。
# CHAR_14（実装済み）は対象外。
import os, re

ROOT = 'ERB/CHAR'
EMPTY = 'PRINTFORMW 「」'

def process(path):
    b = open(path, 'rb').read()
    t = b.decode('cp932')
    # CRLFファイルのみ対象（全CHARはCRLF）
    if b'\r\n' not in b:
        return None
    lines = t.split('\r\n')
    # @KOJO_JUN_K が無ければスキップ
    if not re.search(r'@KOJO_JUN_K\d+', t):
        return None
    # TFLAG:600 == 3 の IF 行を探す
    start = None
    for i, l in enumerate(lines):
        if re.match(r'IF TFLAG:600 == 3\s*$', l):
            start = i
            break
    if start is None:
        return None
    # 既に TFLAG:601 対応済みならスキップ
    # （ブロック内に TFLAG:601 があるか）
    # ネスト対応で ENDIF を探す
    depth = 0
    end = None
    for j in range(start, len(lines)):
        s = lines[j].strip()
        if re.match(r'IF\b', s):
            depth += 1
        if re.match(r'ENDIF\b', s):
            depth -= 1
            if depth == 0:
                end = j
                break
    if end is None:
        return None
    block_inner = lines[start+1:end]  # IF と ENDIF の間
    if any('TFLAG:601' in x for x in block_inner):
        return 'skip(already)'

    # 既存中身の各行に1段インデント(タブ)を追加して保留側へ
    indented = ['\t' + x if x.strip() != '' else x for x in block_inner]

    new_block = []
    new_block.append('IF TFLAG:600 == 3')
    new_block.append('\t; TFLAG:601: 1=保留（もう少し待って） / 0=無下に断る')
    new_block.append('\tIF TFLAG:601 == 1')
    new_block += indented
    new_block.append('\tELSE')
    new_block.append('\t\t;無下に断る（判定値が大きく届かない）')
    new_block.append('\t\t' + EMPTY)
    new_block.append('\tENDIF')
    new_block.append('ENDIF')

    lines = lines[:start] + new_block + lines[end+1:]
    out = '\r\n'.join(lines)
    # 検証
    data = out.encode('cp932')
    return data

changed = []
skipped = []
for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith('.ERB'):
        continue
    if fn == 'CHAR_14_花音ことり.ERB':
        continue
    if fn.endswith('_COM.ERB'):
        continue
    p = os.path.join(ROOT, fn)
    r = process(p)
    if r is None:
        continue
    if r == 'skip(already)':
        skipped.append(fn)
        continue
    with open(p, 'wb') as f:
        f.write(r)
    changed.append(fn)

print('追加したファイル数:', len(changed))
print('スキップ(対応済み):', skipped)
for c in changed:
    print('  ', c)
