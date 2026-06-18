# -*- coding: utf-8 -*-
"""
長い口上(PRINTFORM[LW] 「…」 単一行)を、折り返し幅手前の意味の切れ目で最少限改行し、
PRINTFORML チェーン(最終行のみ PRINTFORMW)へ分割する。
- TRIGGER 全角字超のみ対象 / 各表示行を LINE_TARGET 全角以下に収める最少分割。
- 切れ目優先度: 。！？♪☆… 等 > 、 。句読点は前の行末に残す。
- %VAR% は展開後を考慮し概算幅4で数える。
- 「で始まり」で閉じる単一行のみ対象（既に複数行のものは触らない）。
"""
import re
TRIGGER=60.0
LINE_TARGET=44.0

def width(s):
    # %...% は展開後の呼称等を概算4幅
    s=re.sub(r'%[^%]*%', '名'*4, s)
    w=0.0
    for c in s:
        w += 0.5 if (ord(c)<0x100) else 1.0
    return w

# 切れ目になる文字（この文字の直後で改行可）。優先度高→低
HARD=set('。！？♪☆…！？')
HARD|=set('!?')
SOFT=set('、，')

def split_text(inner):
    """inner(「」の中身)を表示行リストへ。改行不要なら[inner]を返す。"""
    if width(inner) <= TRIGGER:
        return [inner]
    # セグメント分割: HARD/SOFT 文字の直後で区切る（記号連続はまとめる）
    segs=[]; cur=''
    i=0; n=len(inner)
    while i<n:
        c=inner[i]; cur+=c
        if c in HARD or c in SOFT:
            # 後続の連続する記号(。」♪っ…等)も巻き込む
            while i+1<n and (inner[i+1] in HARD or inner[i+1] in SOFT or inner[i+1] in '」』）)♪☆っ〜ー'):
                i+=1; cur+=inner[i]
            segs.append((cur, c in HARD)); cur=''
        i+=1
    if cur: segs.append((cur, False))
    # 貪欲パッキング: LINE_TARGET以下に詰める。優先HARD境界、無理ならSOFT。
    lines=[]; line=''
    for seg,ishard in segs:
        if line and width(line+seg) > LINE_TARGET:
            lines.append(line); line=seg
        else:
            line+=seg
    if line: lines.append(line)
    # 継続行(2行目以降)の行頭空白(全角/半角)を除去
    lines=[lines[0]]+[x.lstrip('\u3000 ') for x in lines[1:]]
    # 1行に収まってしまった(境界が無く分割不能)場合はそのまま
    if len(lines)<=1:
        return [inner]
    return lines

def wrap_file(path, write=True):
    raw=open(path,'rb').read().decode('cp932')
    lines=[l.rstrip('\r') for l in raw.split('\n')]
    out=[]; changed=0
    pat=re.compile(r'^(\s*)PRINTFORM([LW])\s+「(.*)」\s*$')
    for l in lines:
        m=pat.match(l)
        if m:
            indent,lw,inner=m.group(1),m.group(2),m.group(3)
            if '「' not in inner and width(inner)>TRIGGER:
                parts=split_text(inner)
                if len(parts)>1:
                    # 先頭に「、末尾に」。中間はPRINTFORML、最終は元のL/W維持
                    new=[]
                    for k,p in enumerate(parts):
                        first='「' if k==0 else ''
                        last='」' if k==len(parts)-1 else ''
                        cmd = ('PRINTFORM'+lw) if k==len(parts)-1 else 'PRINTFORML'
                        new.append(f'{indent}{cmd} {first}{p}{last}')
                    out.extend(new); changed+=1; continue
        out.append(l)
    norm='\r\n'.join(out)
    for x in norm.split('\r\n'): x.encode('cp932')
    if write: open(path,'wb').write(norm.encode('cp932'))
    return changed

if __name__=='__main__':
    import sys
    for p in sys.argv[1:]:
        print(p, '改行挿入口上数:', wrap_file(p, write=('--dry' not in sys.argv)))
