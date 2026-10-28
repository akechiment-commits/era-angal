# -*- coding: utf-8 -*-
"""
吃り音ミス検出 lint（読みベース）。
「X、語…」の X(単一かな=吃り音) が、直後の語の読みの先頭モーラと一致しない箇所を洗い出す。
例: 「だ、脱ぐ」→ 脱ぐ=ぬぐ。正しい吃りは「ぬ」。だ≠ぬ → 検出。

仕組み:
  - PRINTFORM 行の 「…」 内を対象に、句読点/記号/clause頭の直後に来る「単一かな＋、」を吃り候補とする。
  - 直後の語を pykakasi で読み(ひらがな)に変換し、先頭モーラと吃りかなを比較。
  - 喘ぎ(ん/っ/ー)・助詞や間投詞らしき位置・敬語接頭(お/ご)・既知の特殊読み語は除外/補正。

使い方: python3 tools/check_stutter.py [対象パス...]   (既定= ERB/ 配下の *.ERB 全部)
       python3 tools/check_stutter.py --all   全候補(okも)を表示
"""
import re, sys, glob
try:
    from kojo_util import join_kojo
except ImportError:
    from tools.kojo_util import join_kojo

import pykakasi
kks = pykakasi.kakasi()

def kata2hira(s):
    return ''.join(chr(ord(c)-0x60) if 'ァ'<=c<='ヶ' else c for c in s)

# この作品で頻出かつ pykakasi が読み違えやすい語 → 正しい先頭モーラ（接頭辞で前方一致）
READING_OVERRIDE = [
    ('達く','い'),('達っ','い'),('達ち','い'),('達け','い'),('達か','い'),('達ら','い'),  # 絶頂=いく
    ('痛','い'),('疼','う'),('破','や'),('大き','お'),('擦','こ'),         # こすれる読み優先
    ('入','い'),('挿','い'),('厭','い'),('息','い'),('弄','い'),
    ('上手','じ'),('下手','へ'),('一','い'),('未','ま'),('堪','た'),
]
ONSET_SKIP = set('んっー')          # 喘ぎ等、吃りではない
# 節頭で読点を伴うと、ほぼ確実に助詞/間投詞（吃りでない）。不一致でも抑制する。
PARTICLE = set('ねさがよわもをにへのらで')
# 感嘆・フィラーになりやすい仮名。吃り音とも重なるため不一致でも「低信頼」に回す
# （「あ、見て」「ま、まあ」「は、」等の感嘆と、本物の吃りミスが混在する）。
INTERJ = set('あまはえおう')
SMALL = set('ぁぃぅぇぉっゃゅょゎ')
HONOR = set('おご')                 # 敬語接頭(お奉仕/ご奉仕等)→漢字頭でも正扱い

# 吃りかなの直前がこれらなら「助詞/変数の後」＝吃りでない（除外）
# 平仮名/カタカナ/漢字/英数/%/）/」/＞/数字
PREV_WORD = re.compile(r'[ぁ-んァ-ヶ一-龠a-zA-Z0-9%）＞>」』,]')

STUT = re.compile(r'([ぁ-ん])、(?=\S)')

def reading_onset(chunk):
    for pre, on in READING_OVERRIDE:
        if chunk.startswith(pre):
            return on
    res = kks.convert(chunk)
    if not res:
        return None
    hira = kata2hira(res[0]['hira'] or res[0]['kana'] or res[0]['orig'])
    for ch in hira:
        if 'ぁ' <= ch <= 'ん':
            return ch
    return None

def check_serif(text):
    out = []
    for m in STUT.finditer(text):
        k = m.group(1)
        if k in ONSET_SKIP or k in SMALL or k in PARTICLE:
            continue
        i = m.start()
        # 直前が語の一部(助詞位置) なら吃りでない
        if i > 0 and PREV_WORD.match(text[i-1]):
            continue
        after = text[m.end():]
        chunk = re.split(r'[、。「」！？♪…\s]', after)[0][:8]
        if not chunk:
            continue
        # 読みミスは「漢字語の吃り」でのみ起こる。後続が漢字始まりの時だけ検査する。
        # （後続がかな始まり＝同かな自明正 or 喘ぎ「は、ぁ」「は、ひ」等の誤検出を排除）
        if not re.match(r'[一-龠々〆ヶ]', chunk):
            continue
        if chunk[0] == k:                 # 後続が同かな始まり＝自明に正
            continue
        if k in HONOR:                    # お/ご＋漢字＝敬語接頭の吃り(お奉仕等)→正扱い
            continue
        onset = reading_onset(chunk)
        if onset is None:
            continue
        out.append((k, chunk, onset, onset == k))
    return out

def main():
    args = sys.argv[1:]
    show_low = '--low' in args            # 低信頼(感嘆語起点)も出す
    args = [a for a in args if a != '--low']
    paths = args or sorted(glob.glob('ERB/CHAR/*.ERB'))
    high, low = [], []
    for p in paths:
        try:
            t = join_kojo(open(p, 'rb').read().decode('cp932'))
        except Exception:
            continue
        for ln, line in enumerate(t.split('\n'), 1):
            if 'PRINTFORM' not in line or '「' not in line:
                continue
            for mq in re.finditer(r'「([^」]*)」', line):
                for k, chunk, onset, ok in check_serif(mq.group(1)):
                    if ok:
                        continue
                    rec = f'{p}:{ln}  「{k}、{chunk}…」 吃り[{k}]≠読み[{onset}]'
                    (low if k in INTERJ else high).append(rec)
    print(f'★高信頼（吃りミスの可能性大）: {len(high)} 件')
    for r in high:
        print('  ', r)
    if show_low:
        print(f'\n△低信頼（感嘆語と紛れる・要目視）: {len(low)} 件')
        for r in low:
            print('  ', r)
    else:
        print(f'\n△低信頼（あ/ま/は/え/お/う 起点）: {len(low)} 件  ※--low で表示')

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
