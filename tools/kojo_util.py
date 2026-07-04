# -*- coding: utf-8 -*-
"""
複数行に分割された口上（PRINTFORML 「… → … → PRINTFORMW …」 のチェーン）を、
走査用に1論理行へ結合するヘルパー。監査ツールが「…」単一行前提で書かれているため、
デコード直後に join_kojo() を通すと分割済み口上も従来どおり検出できる。
"""
import re

_PAT = re.compile(r'^(\s*)PRINTFORM([LW])\s+(.*)$')

def join_kojo(text):
    lines = [l.rstrip('\r') for l in text.split('\n')]
    out = []
    i = 0
    n = len(lines)
    while i < n:
        l = lines[i]
        m = _PAT.match(l)
        # 「を開いて同一行で閉じていない＝複数行口上の開始
        if m and ('「' in m.group(3)) and (m.group(3).count('「') > m.group(3).count('」')):
            indent = m.group(1)
            buf = m.group(3)
            j = i + 1
            while j < n and (buf.count('「') > buf.count('」')):
                mj = _PAT.match(lines[j])
                if not mj:
                    break
                buf += mj.group(3)   # 後続PRINTFORM[LW]の本文を連結
                j += 1
            out.append(f'{indent}PRINTFORMW {buf}')
            i = j
        else:
            out.append(l)
            i += 1
    return '\n'.join(out)
