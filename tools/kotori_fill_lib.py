# -*- coding: utf-8 -*-
"""CHAR_14 花音ことり COM_ERB 埋め込み共通ライブラリ。
   COMブロック（;--- COMxxx ヘッダ〜次ヘッダ）単位で空「」を順次置換する。
   また @CHAR_VIRGIN_14 等のラベル単位でも置換できる。
"""
import re
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(_ROOT, 'ERB/CHAR/CHAR_14_花音ことり_COM.ERB')
EMPTY = '「」'  # 全角カギの空


def load():
    return open(PATH, 'rb').read().decode('cp932')


def save(text):
    # 検証：CRLF維持・半角~なし・cp932可
    assert '\r\n' in text
    assert '\n' not in text.replace('\r\n', ''), 'bare LF混入'
    if '~' in text:
        raise SystemExit('半角~混入')
    data = text.encode('cp932')  # ★確定してから書く
    with open(PATH, 'wb') as f:
        f.write(data)
    return len(data)


def check_texts(texts):
    for s in texts:
        if '~' in s:
            raise SystemExit('半角~混入: ' + s)
        s2 = s.replace('～', '〜')
        try:
            s2.encode('cp932')
        except UnicodeEncodeError as e:
            raise SystemExit('cp932不可: %s (%s)' % (s, e))


def norm(s):
    return s.replace('～', '〜')


def fill_blocks(text, mapping):
    """mapping: {com_no(int): [texts...]} COMブロック単位。
       ;--- COM<no> で始まる行から次の ;--- COM までの範囲の空「」を順に置換。"""
    lines = text.split('\r\n')
    # ブロック範囲を特定
    headers = []  # (com_no, idx)
    for i, l in enumerate(lines):
        m = re.match(r';--- COM(\d+)\b', l.strip())
        if m:
            headers.append((int(m.group(1)), i))
    hidx = {}
    for k, (com, idx) in enumerate(headers):
        end = headers[k + 1][1] if k + 1 < len(headers) else len(lines)
        # 同じCOM番号が複数ヘッダの場合は最初のものだけ使う（重複ヘッダ対策）
        if com not in hidx:
            hidx[com] = (idx, end)
    for com, texts in mapping.items():
        if com not in hidx:
            raise SystemExit('COM%d ブロックが見つからない' % com)
        check_texts(texts)
        start, end = hidx[com]
        ti = 0
        for j in range(start, end):
            if EMPTY in lines[j]:
                if ti >= len(texts):
                    raise SystemExit('COM%d: 空スロ過多（texts不足 %d）' % (com, len(texts)))
                lines[j] = lines[j].replace(EMPTY, '「' + norm(texts[ti]) + '」', 1)
                ti += 1
        if ti != len(texts):
            raise SystemExit('COM%d: 空スロ=%d だが texts=%d' % (com, ti, len(texts)))
    return '\r\n'.join(lines)


def fill_label(text, label, texts, start_after_label=True):
    """@<label> 行から次の @ ラベル（または RETURN 0直後の次ラベル）までの空「」を順次置換。"""
    lines = text.split('\r\n')
    # ラベル位置
    li = None
    for i, l in enumerate(lines):
        if l.strip() == '@' + label:
            li = i
            break
    if li is None:
        raise SystemExit('ラベル @%s が見つからない' % label)
    # 次の @ ラベル
    end = len(lines)
    for j in range(li + 1, len(lines)):
        if re.match(r'@[A-Za-z_0-9]+', lines[j].strip()):
            end = j
            break
    check_texts(texts)
    ti = 0
    for j in range(li, end):
        if EMPTY in lines[j]:
            if ti >= len(texts):
                raise SystemExit('%s: 空スロ過多' % label)
            lines[j] = lines[j].replace(EMPTY, '「' + norm(texts[ti]) + '」', 1)
            ti += 1
    if ti != len(texts):
        raise SystemExit('%s: 空スロ=%d だが texts=%d' % (label, ti, len(texts)))
    return '\r\n'.join(lines)


def remaining(text):
    return text.count(EMPTY)
