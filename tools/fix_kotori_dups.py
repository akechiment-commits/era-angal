# -*- coding: utf-8 -*-
# 完全重複7件の是正（2つ目を別表現へ）。行番号順で2つ目だけ置換するため
# 「N個目の出現」を厳密に置換する
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'ERB/CHAR/CHAR_14_花音ことり_COM.ERB')
t = open(PATH, 'rb').read().decode('cp932')
lines = t.split('\r\n')

# (対象行番号1始まり, 新セリフ) ※先のグレップ結果の「2つ目」を差し替え
fixes = {
    818: 'うはぁ、ここすごいなぁ！　えへ、おら、こういうとこ慣れてねぇげど……転校生しゃんとなら、わくわくするだ☆',  # COM321通常側
    1865: 'ん、れろ……ちゅぱ……。えへ、ウフフの最中だがら、思いきり舐めでやるだ転校生しゃん……♪',  # COM373恋人
    2295: 'ん゛っ……おらが腰を振ると、転校生しゃん、気持ちよさそうで……。えへ、おら、嬉しくなっちまうだ……♪',  # COM195/381系恋人
    3757: 'ん゛っ、あぁ……っ。胸もおしりも、いっぺんに……。えへ、すごすぎるだよぉ……っ♪',  # 恋人・複絶頂・膣なし・強・1
    3768: 'ん゛っ……だ、だめ、あちこちいっぱい……っ。あぅ、おら、こわいだよぉ……っ',  # 通常・複絶頂・膣なし・強・1
    3782: 'ん、あちこちで、気持ちよかっだ♪　えへ、転校生しゃんと一緒だと、すごいなぁ……♪',  # 恋人・複絶頂・膣なし・通常・1
    3793: 'ん、あちこちいけだなぁ。えへ、おら、こんなに感じるなんて……♪',  # 通常・複絶頂・膣なし・通常・1
}

import re
for ln, new in fixes.items():
    i = ln - 1
    m = re.search(r'(PRINTFORMW?\s+「)(.+?)(」)', lines[i])
    if not m:
        raise SystemExit('行%dにPRINTFORMWなし: %s' % (ln, lines[i]))
    if '~' in new:
        raise SystemExit('半角~: ' + new)
    new.encode('cp932')
    lines[i] = lines[i][:m.start()] + m.group(1) + new + m.group(3) + lines[i][m.end():]

out = '\r\n'.join(lines)
data = out.encode('cp932')
with open(PATH, 'wb') as f:
    f.write(data)

# 再チェック
from collections import Counter
bodies = [re.search(r'PRINTFORMW?\s+「(.+?)」', l).group(1)
          for l in out.split('\r\n') if re.search(r'PRINTFORMW?\s+「(.+?)」', l)]
dup = [k for k, v in Counter(bodies).items() if v > 1]
print('重複是正後の完全重複数=', len(dup), ' 空「」=', out.count('「」'), ' 半角~=', out.count('~'))
