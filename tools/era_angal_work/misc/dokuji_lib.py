# -*- coding: utf-8 -*-
# 独自コマンド(COM280-284 ウフフ / COM410-414 純愛)を CHAR_NN_*_COM.ERB に挿入し、
# CSTR:80-89(コマンド名)を Chara<NN> CSV に定義する共通処理。
# 使い方: from tools.dokuji_lib import apply_dokuji  →  apply_dokuji(nn, ufufu, junai, names)
#   ufufu = {280:(恋人,通常),281:...,284:...}
#   junai = {410:(恋人,通常),...,414:...}
#   names = {80:'..',...,89:'..'}  (80-84=ウフフ名, 85-89=純愛名)
import glob, re, sys

def _find(nn, com):
    pat = f'ERB/CHAR/CHAR_{nn:02d}_*' + ('_COM.ERB' if com else '.ERB')
    fs = [f for f in glob.glob(pat) if (('_COM' in f) == com)]
    assert len(fs) == 1, (pat, fs)
    return fs[0]

def _chain(d, nums):
    out = []
    for idx, n in enumerate(nums):
        koi, tsu = d[n]
        out.append(('IF' if idx == 0 else 'ELSEIF') + f' SELECTCOM == {n}')
        out.append('\tIF TALENT:TARGET:153')
        out.append(f'\t\tPRINTFORMW 「{koi}」')
        out.append('\tELSE')
        out.append(f'\t\tPRINTFORMW 「{tsu}」')
        out.append('\tENDIF')
    out.append('ENDIF')
    return out

def _write_cp932_crlf(path, text):
    norm = '\r\n'.join(l.rstrip('\r') for l in text.split('\n'))
    assert '~' not in norm, 'ASCII tilde found'
    for i, l in enumerate(norm.split('\r\n')):
        l.encode('cp932')  # raises on bad char
    open(path, 'wb').write(norm.encode('cp932'))

# CFLAG:69「独自コマンド使用判定」bit0-9 を全立て(=1023)＝独自コマンド280-284/410-414を有効化。
# Chara CSV では「フラグ,<番号>,<値>」が CFLAG 初期値設定の書式。
FLAG69_VALUE = 1023  # bit0..9 全ON (2^10-1)

def _set_flag69(clines):
    out = [l for l in clines if not re.match(r'\s*フラグ\s*,\s*69\s*,', l)]
    line = f'フラグ,69,{FLAG69_VALUE}'
    idxs = [i for i,l in enumerate(out) if re.match(r'\s*フラグ\s*,', l)]
    if idxs:
        out.insert(idxs[-1]+1, line)
    else:
        cs = [i for i,l in enumerate(out) if re.match(r'\s*CSTR\s*,', l)]
        out.insert(cs[0] if cs else len(out), line)
    return out

def enable_flag69(nn):
    """既に CSTR/口上 導入済みのキャラに フラグ,69,1023 だけ追加する遡及用。"""
    csv = glob.glob(f'CSV/Chara{nn}_*.csv')[0]
    ct = open(csv,'rb').read().decode('cp932')
    clines = _set_flag69(ct.split('\n'))
    _write_cp932_crlf(csv, '\n'.join(clines))
    chk = [l.strip() for l in open(csv,'rb').read().decode('cp932').split('\n') if re.match(r'\s*フラグ\s*,\s*69\s*,', l)]
    print(f'CHAR_{nn:02d}: {chk[0]} -> {csv.split("/")[-1]}')

def apply_dokuji(nn, ufufu, junai, names):
    assert set(ufufu) == {280,281,282,283,284}
    assert set(junai) == {410,411,412,413,414}
    assert set(names) == set(range(80,90))
    com = _find(nn, True)
    t = open(com,'rb').read().decode('cp932'); lines = t.split('\n')
    assert 'SELECTCOM == 280' not in t, '既に独自枠あり: '+com
    block = [
        ';==============================================================',
        '; 口上独自ウフフ（COM280-284）/ 口上独自純愛（COM410-414）',
        ';==============================================================',
        ';--- COM280-284 独自ウフフ ---',
        ';  ※ウフフ中の独自カスタムコマンド（各キャラ固有の性的シチュエーション）',
    ] + _chain(ufufu,[280,281,282,283,284]) + [
        '',
        ';--- COM410-414 独自純愛 ---',
        ';  ※純愛系の独自カスタムコマンド（ウフフ外・各キャラ固有のシチュエーション）',
    ] + _chain(junai,[410,411,412,413,414]) + ['']
    ins = None
    for i,ln in enumerate(lines):
        if 'えっち系・よく使うコマンド' in ln:
            ins = i-1; break
    assert ins is not None and lines[ins].startswith(';==='), (ins, lines[ins] if ins else None)
    new = lines[:ins] + block + lines[ins:]
    _write_cp932_crlf(com, '\n'.join(new))
    # CSV CSTR:80-89
    csv = _find(nn, False).replace('ERB/CHAR/','CSV/').replace('.ERB','.csv')
    csv = glob.glob(f'CSV/Chara{nn}_*.csv')[0]
    ct = open(csv,'rb').read().decode('cp932'); clines = ct.split('\n')
    def tgt(ln):
        m = re.match(r'\s*CSTR\s*,\s*(\d+)\s*,', ln)
        return m and int(m.group(1)) in names
    clines = [l for l in clines if not tgt(l)]
    last = max(i for i,l in enumerate(clines) if re.match(r'\s*CSTR\s*,\s*\d+', l))
    add = [f'CSTR,{n},{names[n]}' for n in range(80,90)]
    clines = clines[:last+1] + add + clines[last+1:]
    clines = _set_flag69(clines)
    _write_cp932_crlf(csv, '\n'.join(clines))
    # 検算
    raw = open(com,'rb').read(); tt = raw.decode('cp932')
    ifc = len(re.findall(r'^\s*IF\b',tt,re.M)); ec = len(re.findall(r'^\s*ENDIF\b',tt,re.M))
    slots = [n for n in [280,281,282,283,284,410,411,412,413,414] if re.search(rf'SELECTCOM == {n}\b',tt)]
    print(f'CHAR_{nn:02d}: 独自枠{len(slots)}/10 IF/ENDIF {ifc}/{ec} {"OK" if ifc==ec else "X"} '
          f'CRLF {raw.count(chr(13).encode()+chr(10).encode())}/{raw.count(chr(10).encode())} -> {com.split("/")[-1]}, CSTR -> {csv.split("/")[-1]}')
    assert ifc==ec and len(slots)==10
