# -*- coding: utf-8 -*-
# CHAR_22 鯱いかり COM_ERB 共通フィラー。先頭から N 個の空「」を順に埋める。
import re
PATH = 'ERB/CHAR/CHAR_22_鯱いかり_COM.ERB'

def fill_front(strings, label=''):
    raw = open(PATH, 'rb').read()
    assert b'\r\n' in raw, 'COM ERB must be CRLF'
    text = raw.decode('cp932')
    empties = text.count('「」')
    assert empties >= len(strings), f'空「」{empties} < 用意{len(strings)}'
    norm = []
    for i, s in enumerate(strings):
        s2 = (s.replace('〜', '～').replace('~', '～')
                .replace('—', '―').replace('–', '―'))
        for bad in ['わたし', '僕', '俺']:
            assert bad not in s2, f'[{i}] 禁止一人称 {bad}: {s2}'
        assert 'あたし' in s2 or len(s2) < 14 or 'あたい' not in s2, None
        assert 'わたし' not in s2
        # 漢字「私」も禁止（私服/私語の熟語が無ければ）
        if '私' in s2:
            assert ('私服' in s2 or '私語' in s2), f'[{i}] 裸の私: {s2}'
        assert '「」' not in s2, f'[{i}] 空「」混入: {s2}'
        try:
            s2.encode('cp932')
        except UnicodeEncodeError as e:
            raise SystemExit(f'[{i}] cp932不可: {s2}\n{e}')
        norm.append(s2)
    parts = text.split('「」')
    out = parts[0]
    for i in range(len(parts) - 1):
        out += ('「' + norm[i] + '」') if i < len(norm) else '「」'
        out += parts[i + 1]
    data = out.encode('cp932')
    with open(PATH, 'wb') as f:
        f.write(data)
    left = out.count('「」')
    print(f'{label} OK: {len(norm)}枠記入, 残り空「」={left}, {len(data)} bytes')
