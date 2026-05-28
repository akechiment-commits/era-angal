# -*- coding: utf-8 -*-
# こよい(28) COM_ERB 空枠フィルター（セクション単位・順次置換）
import re, sys

PATH = 'ERB/CHAR/CHAR_28_星海こよい_COM.ERB'

def load():
    with open(PATH, 'rb') as f:
        return f.read().decode('cp932')

def save(text):
    assert '\r\n' in text, 'CRLF must be preserved'
    for s in re.findall(r'PRINTFORM[LW]\s+「(.*?)」', text):
        try:
            s.encode('cp932')
        except UnicodeEncodeError as e:
            raise SystemExit(f'cp932不可: {s!r} ({e})')
    data = text.encode('cp932')  # 先に確定
    with open(PATH, 'wb') as f:
        f.write(data)

def find_block(lines, comnum):
    """IF SELECTCOM == comnum の行から、次の同種境界までの (start,end)"""
    pat = re.compile(r'^\s*IF\s+SELECTCOM\s*==\s*' + str(comnum) + r'\b')
    start = None
    for i, l in enumerate(lines):
        if pat.search(l):
            start = i; break
    if start is None:
        raise SystemExit(f'COM{comnum} 見つからず')
    for j in range(start + 1, len(lines)):
        if (re.match(r'\s*IF\s+SELECTCOM\s*==', lines[j])
                or re.match(r'\s*;---\s*COM', lines[j])
                or re.match(r'\s*@\w+', lines[j])
                or re.match(r'\s*;===', lines[j])):
            return start, j
    return start, len(lines)

def fill_com(comnum, repls, expect_comments=None):
    """COM番号ブロック内の空 PRINTFORM「」 を repls で順次置換。"""
    text = load()
    nl = '\r\n'
    lines = text.split(nl)
    s, e = find_block(lines, comnum)
    # 空枠のインデックスを収集
    idxs = [i for i in range(s, e) if re.search(r'PRINTFORM[LW]\s+「」', lines[i])]
    if len(idxs) == 0:
        print(f'COM{comnum}: 既記入(空0)→スキップ'); return
    if len(idxs) != len(repls):
        raise SystemExit(f'COM{comnum}: 空枠{len(idxs)}個 != 用意{len(repls)}個')
    # 任意: 直前コメントの確認
    if expect_comments:
        for k, i in enumerate(idxs):
            prevcmt = ''
            for back in range(i - 1, s - 1, -1):
                ls = lines[back].strip()
                if ls.startswith(';'):
                    prevcmt = ls.lstrip('; ').strip(); break
                if ls and not ls.startswith('PRINTFORM'):
                    break
            if expect_comments[k] not in prevcmt:
                raise SystemExit(f'COM{comnum} slot{k}: 想定コメント「{expect_comments[k]}」≠実際「{prevcmt}」')
    for i, txt in zip(idxs, repls):
        lines[i] = re.sub(r'(PRINTFORM[LW]\s+「)」', lambda m: m.group(1) + txt + '」', lines[i])
    save(nl.join(lines))
    print(f'COM{comnum}: {len(repls)}枠 記入')

# ============ COM3 自慰（12枠）============
COM3 = [
 # 恋人・ビデオ・1/2/3
 'は、はぅ……っ。か、カメラ、回ってるんやんな……？　うう、恥ずかしいわぁ……。で、でも、転校生くんが見たいんやったら……うち、見せたげる♪　んっ……ここ、こうやって……あぁっ',
 '（あかん、レンズ見てると、よけい意識してまう……）……んっ、んんっ。転校生くん、後で見返すんやろ？　うちのこんな顔……忘れんといてな……はぁっ、はぁっ',
 'ん、んっ……ここ、いじってるとこ、ばっちり撮れてる……？　うう、こんなんお嫁にいけへんわぁ……。せやけど、転校生くんになら……ぜんぶ見られてもええねん♪',
 # 通常・ビデオ・1/2/3
 'ほ、ほんまに撮るん……？　うう、やめてや〜……。（でも、ここでやめたら、もっと困らせてまう……）……んっ、わ、わかった、やるから……',
 '（あかんあかん、こんなん記録されたら……）……はぅっ、ん……。み、見んといて……ううん、見られてるから……よけい、体、熱なってくる……っ',
 'うひゃっ、ズームせんといて……っ！　うう、うちの恥ずかしいとこ、ぜんぶ……。は、はぁっ、んっ……もう、どないなっても知らへんからな……っ',
 # 恋人・1/2/3
 'ん……っ、転校生くんが見ててくれるなら……うち、頑張れるわぁ。ここ、転校生くんがいつも触ってくれるとこ……自分でしたら、なんや、ちゃうなぁ……はぅっ',
 '（転校生くんのこと考えながらやと、すぐ……）……あっ、あっ、んんっ。なぁ、うちのこと、可愛いて思てくれてる……？　はぁ、もう、止まらへんよぉ……っ',
 '見て、転校生くん……。うち、こんなにはしたない子になってもた……。ぜんぶ、転校生くんのせいやで……？　んっ、んっ、あぁっ……いっちゃう……っ',
 # 通常・1/2/3
 'な、なんでうち、こんなことを……。（は、はやく終わらせよ……）……んっ、はぅっ。こ、こんなん、誰にも見せられへんわぁ……っ',
 '（あぁ、体が、勝手に……）……んっ、んんっ。だ、だめ、声、出てまう……。うち、ほんまは、こんな子とちゃうのに……はぁっ、はぁっ',
 'ひっ、ん……っ。こ、ここ、敏感すぎて……すぐ、つらくなってまう……。うう、もう、堪忍してぇ……っ、んあぁっ',
]

def fill_sec(label, repls):
    """@label セクション内の空 PRINTFORM「」 を repls で順次置換。"""
    text = load()
    nl = '\r\n'
    lines = text.split(nl)
    pat = re.compile(r'^\s*@' + label + r'\b')
    start = None
    for i, l in enumerate(lines):
        if pat.search(l):
            start = i; break
    if start is None:
        raise SystemExit(f'@{label} 見つからず')
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r'\s*@\w+', lines[j]):
            end = j; break
    idxs = [i for i in range(start, end) if re.search(r'PRINTFORM[LW]\s+「」', lines[i])]
    if len(idxs) == 0:
        print(f'@{label}: 既記入(空0)→スキップ'); return
    if len(idxs) != len(repls):
        raise SystemExit(f'@{label}: 空枠{len(idxs)}個 != 用意{len(repls)}個')
    for i, txt in zip(idxs, repls):
        lines[i] = re.sub(r'(PRINTFORM[LW]\s+「)」', lambda m: m.group(1) + txt + '」', lines[i])
    save(nl.join(lines))
    print(f'@{label}: {len(repls)}枠 記入')


if __name__ == '__main__':
    fill_com(3, COM3)
