# -*- coding: utf-8 -*-
# 再利用ライブラリ: COMブロック単位で空き「」を埋める（位置ズレ防止）
import re

def fill_blocks(path, mapping, verbose=True):
    """mapping: { com_number(int) : [本文str, ...] }
    各COMの ;--- COMn ... 見出しから次の ;--- COM / ;=== までの範囲内の空き「」を順次置換。"""
    t = open(path, 'rb').read().decode('cp932')
    assert '\r\n' in t, 'CRLFでない'
    lines = t.split('\r\n')
    # 見出し位置を収集
    heads = []  # (idx, com or None for section divider)
    for i, l in enumerate(lines):
        s = l.strip()
        m = re.match(r';---\s*COM(\d+)\b', s)
        if m:
            heads.append((i, int(m.group(1))))
        elif re.match(r';={5,}', s):
            heads.append((i, None))
    # 各COMのブロック範囲を決定
    def block_range(com):
        for k, (idx, c) in enumerate(heads):
            if c == com:
                start = idx
                end = heads[k+1][0] if k+1 < len(heads) else len(lines)
                return start, end
        raise SystemExit(f'COM{com} 見出しが見つからない')
    # チェック
    for com, arr in mapping.items():
        for s in arr:
            try: s.encode('cp932')
            except UnicodeEncodeError as e: raise SystemExit(f'cp932不可 COM{com}: {s} -> {e}')
            if '~' in s: raise SystemExit(f'半角~ COM{com}: {s}')
            if '?' in s or '!' in s: raise SystemExit(f'半角?! COM{com}: {s}')
            if '%CALLNAME%' in s and '%CALLNAME:' not in s.replace('%CALLNAME%','X'):
                pass
            if re.search(r'%CALLNAME%(?!:)', s): raise SystemExit(f'裸CALLNAME COM{com}: {s}')
    # 置換
    for com, arr in mapping.items():
        start, end = block_range(com)
        it = iter(arr); cnt = [0]
        def repl(m):
            if cnt[0] < len(arr):
                cnt[0]+=1; return '「'+next(it)+'」'
            return m.group(0)
        for i in range(start, end):
            if '「」' in lines[i]:
                lines[i] = re.sub('「」', repl, lines[i])
        if cnt[0] != len(arr):
            raise SystemExit(f'COM{com}: 用意{len(arr)}件 vs 空き{cnt[0]}件 不一致')
        if verbose: print(f'  COM{com}: {cnt[0]}スロ記入')
    new = '\r\n'.join(lines)
    data = new.encode('cp932')
    open(path, 'wb').write(data)
    if verbose: print(f'残り空き「」: {new.count("「」")}')
    return new


def fill_ordered_anchors(path, specs, verbose=True):
    """specs: 文書順の [(anchor_substr, [lines]), ...]
    各anchorを含む行を見つけ、その直後から次のanchorまでの空き「」を順次置換。"""
    import re as _re
    t = open(path, 'rb').read().decode('cp932')
    assert '\r\n' in t
    lines = t.split('\r\n')
    # 各specのチェック
    for anc, arr in specs:
        for s in arr:
            try: s.encode('cp932')
            except UnicodeEncodeError as e: raise SystemExit(f'cp932不可 [{anc}]: {s} -> {e}')
            if '~' in s: raise SystemExit(f'半角~ [{anc}]: {s}')
            if '?' in s or '!' in s: raise SystemExit(f'半角?! [{anc}]: {s}')
            if _re.search(r'%CALLNAME%(?!:)', s): raise SystemExit(f'裸CALLNAME [{anc}]: {s}')
    # anchor行index
    pos = []
    for anc, arr in specs:
        idx = None
        for i, l in enumerate(lines):
            if anc in l:
                idx = i; break
        if idx is None: raise SystemExit(f'anchor見つからず: {anc}')
        pos.append((idx, anc, arr))
    # 文書順検証
    for k in range(1, len(pos)):
        if pos[k][0] <= pos[k-1][0]:
            raise SystemExit(f'anchorが文書順でない: {pos[k][1]}')
    # 各区間で置換
    for k, (idx, anc, arr) in enumerate(pos):
        end = pos[k+1][0] if k+1 < len(pos) else len(lines)
        it = iter(arr); cnt = [0]
        def repl(m):
            if cnt[0] < len(arr):
                cnt[0]+=1; return '「'+next(it)+'」'
            return m.group(0)
        for i in range(idx, end):
            if '「」' in lines[i]:
                lines[i] = _re.sub('「」', repl, lines[i])
        if cnt[0] != len(arr):
            raise SystemExit(f'[{anc}]: 用意{len(arr)} vs 記入{cnt[0]} 不一致')
        if verbose: print(f'  [{anc}]: {cnt[0]}スロ記入')
    new = '\r\n'.join(lines)
    data = new.encode('cp932')
    open(path, 'wb').write(data)
    if verbose: print(f'残り空き「」: {new.count("「」")}')
    return new
