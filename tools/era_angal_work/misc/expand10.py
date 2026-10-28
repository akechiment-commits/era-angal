# -*- coding: utf-8 -*-
"""
expand10.py — まとめ系（2枠）/枠0 の独自コマンドを 詳細系10枠 に機械変換し、CSVを配線する。
2026-06-10 方針変更（全キャラ詳細系10枠統一）の実装ヘルパー。基準構造は CHAR_01/49。

使い方:
  from tools.expand10 import expand
  scenes = [
    # ウフフ5（COM280-284）
    {'com':280,'name':'場面名','jibun':'%CALLNAME:PLAYER%は…','koibito':'恋人口上(「」なし)','tsujo':'通常口上(「」なし)'},
    ... 281,282,283,284 ...
    # 純愛5（COM410-414）
    {'com':410,'name':'場面名','jibun':'…','koibito':'…','tsujo':'…'},
    ... 411,412,413,414 ...
  ]
  expand(56, scenes)   # COM ERB の独自セクションを詳細系に置換 ＋ CSV に CSTR80-89/フラグ69=1023

検算は呼び出し側で audit_koujo_drift.py / IF=ENDIF / cp932 を行うこと。
"""
import glob, re, os

UFUFU=[280,281,282,283,284]
JUNAI=[410,411,412,413,414]

def _com_path(cno):
    g=glob.glob(f'ERB/CHAR/CHAR_{cno}_*_COM.ERB')
    assert len(g)==1, f'COM not unique for {cno}: {g}'
    return g[0]

def _csv_path(cno):
    g=glob.glob(f'CSV/Chara{cno}_*.csv')
    assert len(g)==1, f'CSV not unique for {cno}: {g}'
    return g[0]

def _check(s):
    assert chr(0x7E) not in s, f'half tilde in: {s!r}'      # 半角~禁止
    assert chr(0x2014) not in s, f'em dash in: {s!r}'        # —禁止
    s.encode('cp932')

def build_section(scenes):
    by={s['com']:s for s in scenes}
    assert set(by)==set(UFUFU+JUNAI), f'need exactly 280-284,410-414; got {sorted(by)}'
    out=[]
    out.append(';==============================================================')
    out.append('; 口上独自ウフフ（COM280-284）/ 口上独自純愛（COM410-414）')
    out.append(';==============================================================')
    out.append(';--- COM280-284 独自ウフフ ---')
    out.append(';  ※ウフフ中の独自カスタムコマンド（各キャラ固有の性的シチュエーション）')
    for k,com in enumerate(UFUFU):
        s=by[com]
        head='IF' if k==0 else 'ELSEIF'
        out.append(f'{head} SELECTCOM == {com}')
        out.append(f'\t;◆地の文（場面: {s["name"]}）')
        out.append(f'\tPRINTFORMW {s["jibun"]}')
        out.append('\tIF TALENT:TARGET:153')
        out.append(f'\t\tPRINTFORMW 「{s["koibito"]}」')
        out.append('\tELSE')
        out.append(f'\t\tPRINTFORMW 「{s["tsujo"]}」')
        out.append('\tENDIF')
    out.append('ENDIF')
    out.append('')
    out.append(';--- COM410-414 独自純愛 ---')
    out.append(';  ※純愛系の独自カスタムコマンド（ウフフ外・各キャラ固有のシチュエーション）')
    for k,com in enumerate(JUNAI):
        s=by[com]
        head='IF' if k==0 else 'ELSEIF'
        out.append(f'{head} SELECTCOM == {com}')
        out.append(f'\t;◆地の文（場面: {s["name"]}）')
        out.append(f'\tPRINTFORMW {s["jibun"]}')
        out.append('\tIF TALENT:TARGET:153')
        out.append(f'\t\tPRINTFORMW 「{s["koibito"]}」')
        out.append('\tELSE')
        out.append(f'\t\tPRINTFORMW 「{s["tsujo"]}」')
        out.append('\tENDIF')
    out.append('ENDIF')
    for l in out: _check(l)
    return out

def expand(cno, scenes, write=True):
    P=_com_path(cno)
    L=[l.rstrip('\r') for l in open(P,'rb').read().decode('cp932').split('\n')]
    # anchors
    etch=[i for i,l in enumerate(L) if 'えっち系' in l and '；' not in l]
    etch=[i for i,l in enumerate(L) if 'えっち系' in l]
    assert etch, 'えっち系 header not found'
    etch_i=etch[0]
    assert L[etch_i-1].startswith(';='), f'expected ;=== before えっち at {etch_i}: {L[etch_i-1]!r}'
    end_excl=etch_i-1   # replace up to (not including) the ;=== of えっち section
    # dokuji section start: the ;=== preceding '口上独自ウフフ' header, else insert at end_excl
    dh=[i for i,l in enumerate(L) if '口上独自ウフフ' in l]
    if dh:
        start=dh[0]-1
        assert L[start].startswith(';='), f'expected ;=== before dokuji header at {start}'
    else:
        start=end_excl  # 枠0 with no section: insert
    newsec=build_section(scenes)+['']  # trailing blank before えっち ;===
    L2=L[:start]+newsec+L[end_excl:]
    text='\r\n'.join(L2)
    nif=sum(1 for l in L2 if re.match(r'^\s*IF\b',l))
    nend=sum(1 for l in L2 if re.match(r'^\s*ENDIF\b',l))
    assert nif==nend, f'IF/ENDIF imbalance {nif}/{nend}'
    for l in L2: _check(l)
    if write:
        open(P,'wb').write(text.encode('cp932'))
    return nif,nend

def wire_csv(cno, scenes):
    by={s['com']:s for s in scenes}
    P=_csv_path(cno)
    data=open(P,'rb').read().decode('cp932')
    lines=data.replace('\r\n','\n').split('\n')
    # drop existing フラグ69 / CSTR80-89 lines and trailing blanks
    keep=[]
    for l in lines:
        s=l.rstrip('\r')
        if re.match(r'^フラグ,\s*69\b',s): continue
        if re.match(r'^CSTR,\s*8[0-9]\b',s): continue
        keep.append(s)
    while keep and keep[-1].strip()=='': keep.pop()
    add=['フラグ,69,1023']
    for k,com in enumerate(UFUFU): add.append(f'CSTR,8{k},{by[com]["name"]}')
    for k,com in enumerate(JUNAI): add.append(f'CSTR,8{5+k},{by[com]["name"]}')
    for a in add: _check(a)
    out=keep+add
    open(P,'wb').write(('\r\n'.join(out)+'\r\n').encode('cp932'))
    return add

if __name__=='__main__':
    print('expand10 helper. import expand/wire_csv.')
