# -*- coding: utf-8 -*-
"""装着アイテム6種(COM11/13/14/15/16/17)の付け外し口上を1キャラ分埋める汎用フィラー。
各道具 4スロ=[装着堕ち, 装着通常, 取外堕ち, 取外通常] の順。cp932/CRLF維持。
使い方: data dict {com番号:[4文]} を渡して fill_char(path, data)。"""
import re

HDR_OLD = '; 装着アイテム 付け外し口上（未実装＝空「」。後で各キャラに肉付け）'

def fill_char(path, data, char_label):
    raw = open(path, 'rb').read()
    t = raw.decode('cp932')
    lines = t.split('\n')

    def section_bounds(com):
        hdr = f';--- COM{com} '
        s = None
        for i, l in enumerate(lines):
            if l.startswith(hdr):
                s = i; break
        assert s is not None, f'{path}: header COM{com} not found'
        e = len(lines)
        for j in range(s + 1, len(lines)):
            if lines[j].startswith(';--- COM') or lines[j].startswith(';====='):
                e = j; break
        return s, e

    total = 0
    for com, texts in data.items():
        assert len(texts) == 4, f'COM{com}: need 4 texts'
        s, e = section_bounds(com)
        idx = [i for i in range(s, e) if lines[i].strip() == 'PRINTFORMW 「」']
        assert len(idx) == 4, f'{path} COM{com}: empty slots {len(idx)} != 4'
        for i, x in zip(idx, texts):
            ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
            lines[i] = f'{ind}PRINTFORMW 「{x}」'
            total += 1

    t2 = '\n'.join(lines)
    # 見出しコメントを記入済へ更新
    new_hdr = f'; 装着アイテム 付け外し口上（{char_label}の声で記入済）'
    t2 = t2.replace(HDR_OLD, new_hdr)

    norm = '\r\n'.join(l.rstrip('\r') for l in t2.split('\n'))
    assert '~' not in norm and '—' not in norm, f'{path}: bad char'
    for l in norm.split('\r\n'):
        l.encode('cp932')  # cp932不可文字を早期検出
    open(path, 'wb').write(norm.encode('cp932'))

    # 検算
    r2 = open(path, 'rb').read(); d2 = r2.decode('cp932')
    assert r2.count(b'\r\n') == d2.count('\n'), f'{path}: CRLF不整合'
    nif = len(re.findall(r'^\s*IF\b', d2, re.M))
    nend = len(re.findall(r'^\s*ENDIF\b', d2, re.M))
    assert nif == nend, f'{path}: IF{nif}/ENDIF{nend}'
    print(f'OK {path}: {total}枠 / IF=ENDIF={nif} / CRLF整合')
