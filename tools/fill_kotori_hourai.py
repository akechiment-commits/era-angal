# -*- coding: utf-8 -*-
# CHAR_14 花音ことり 蓬莱の薬口上 @HOURAI_KOJO_14（専用ERB・★LF改行維持★）
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'ERB/KOUJO/KOJO_HOURAI_蓬莱薬口上.ERB')

t = open(PATH, 'rb').read().decode('cp932')
assert '\r\n' not in t, 'このファイルはLFのはず（CRLF混入を防ぐ）'

# TFLAG:91 → CASE 0:目撃 / 1:自ら飲む(実名解禁=山場) / 2:無理やり / 3:拒否
texts = [
    # CASE0 プレイヤーが先に飲むのを目撃
    'え……転校生しゃん、それ飲んじまっだのが……？　不老不死の薬……。うう、ずっと生きるなんで、寂しくねぇが……？　……でも、あんたが決めだことだもんな。おら、見守るだよ……。',
    # CASE1 自らの意志で飲む（山場・実名解禁）
    'おら……飲むだ、この薬。だって、転校生しゃん……%CALLNAME:PLAYER%しゃんと、ずっと一緒にいてぇんだもの。寂しい島の子供だったおらが、やっと見つけた居場所だ。永遠だって、あんたとなら、こわくねぇ。ずっと、ずっと、おらの歌を聴いでぇな……♪',
    # CASE2 無理やり飲まされる
    'ん゛っ……!?　な、なに飲まされだ……っ。あぅ、身体が、熱い……これ、不老不死の……っ。う、うう……おら、こんなの望んでねぇだよぉ……。ずっと生きるなんで、こわいだよぉ……っ',
    # CASE3 拒否
    'い、嫌だぁっ……!?　そんな薬、飲まねぇ……っ。おら、ふつうに生きで、ふつうに歳をとりてぇだ。永遠なんて、いらねぇ……。つばさしゃんや、みんなと一緒に、歩いでいきてぇんだ……っ',
]

# 検証
for s in texts:
    if '~' in s:
        raise SystemExit('半角~混入: ' + s)
    s.encode('cp932')

EMPTY = '「」'
# @HOURAI_KOJO_14 区間だけを対象に置換
lines = t.split('\n')
si = None
for i, l in enumerate(lines):
    if l.strip() == '@HOURAI_KOJO_14':
        si = i
        break
assert si is not None
ei = len(lines)
for j in range(si + 1, len(lines)):
    if lines[j].strip().startswith('@HOURAI_KOJO'):
        ei = j
        break
ti = 0
for j in range(si, ei):
    if EMPTY in lines[j]:
        lines[j] = lines[j].replace(EMPTY, '「' + texts[ti] + '」', 1)
        ti += 1
assert ti == 4, 'HOURAI空スロ=%d (expect 4)' % ti

out = '\n'.join(lines)
assert '\r\n' not in out, 'CRLF混入'
data = out.encode('cp932')
with open(PATH, 'wb') as f:
    f.write(data)
print('蓬莱口上 OK  @HOURAI_KOJO_14記入  残@14空=', '「」' in out.split('@HOURAI_KOJO_14')[1].split('@HOURAI_KOJO')[0])
