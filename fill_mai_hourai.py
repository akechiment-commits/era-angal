# -*- coding: utf-8 -*-
# CHAR_32 安条まい 蓬莱の薬 @HOURAI_KOJO_32（専用ERB・★LF改行厳守★・4枠）
# TFLAG:91: CASE0=目撃 CASE1=自ら飲む(山場・名前呼び解禁) CASE2=無理やり(本気の怒り) CASE3=拒否
# まいの哲学=「終わりがあるから青春が輝く/今この現実が好き」、寂しさの核=永遠にあんたのそばに。

PATH = 'ERB/KOUJO/KOJO_HOURAI_蓬莱薬口上.ERB'
START = "@HOURAI_KOJO_32"

slots = [
# CASE0 目撃
"お、おい、あんた……それ、不老不死の薬じゃん!?　飲んじゃったの……？　うわ～、とんでもない決断したね～。永遠に終わらない命なんて、あたしには想像もつかないよ。……でもまぁ、あんたが選んだ道なら、口出しはしないよ。あたしは「終わりがあるからこそ」って信じてるけど……あんたの隣で、できるだけ長く青春してあげる。独りにはしないからさ、安心しな♪",
# CASE1 自ら飲む（山場・名前呼び解禁）
"……あたしも、飲んじゃおうかな。あんたと、永遠に。……えへへ、柄じゃないこと言ってる、あたし。あのね、あたしずっと「いつか終わる」前提で生きてきたんだ。家族とも距離があって、脇役で……独りで晩ごはん食べる人生に、慣れてたつもりだった。でも、%CALLNAME:PLAYER%があたしを「いちばん」にしてくれたから。終わらない時間も、あんたとなら怖くない。むしろ、ずっとあんたのそばにいられるなんて、最高じゃん？　永遠に、よろしくね、あたしの旦那さん♪",
# CASE2 無理やり飲まされる（本気の怒り＝怒り実在）
"……ちょっ、何飲ませたの!?　蓬莱の薬って……不老不死!?　あんた、あたしの許可なく、勝手に……っ。……あはは、笑えないよ、これは。あたしの人生の終わり方は、あたしが決めるの。それを、こんなふうに奪うなんてさ。……マジで怒ってるかんね？　あんたのこと、嫌いになりたくないのに。この落とし前、どうつけてくれるわけ……？",
# CASE3 拒否
"……いや、それは飲まないよ。せっかくだけど、ね？　あたしね、終わりがあるから、青春ってこんなにキラキラ輝くんだって信じてるんだ。散る桜が綺麗なのと、おんなじでさ。永遠に生きちゃったら、きっとあたし、この一瞬の眩しさを忘れちゃう。……今日が終わっても、明日がある。それで、じゅうぶんだよ。あたしは、この限りある「今」を、あんたと精いっぱい生きたいんだ♪",
]

import re
norm=[]
for s in slots:
    assert '~' not in s, f'半角~: {s}'
    s=s.replace('〜','～'); s.encode('cp932'); norm.append(s)
slots=norm

raw=open(PATH,'rb').read()
assert b'\r\n' not in raw, 'この専用ERBはLF改行（CRLF混入禁止）'
text=raw.decode('cp932')
si=text.index(START)
# 次の @HOURAI_KOJO_ までを _32 ブロックとする
nxt=text.find('\n@HOURAI_KOJO_', si+1)
ei=nxt if nxt!=-1 else len(text)
block=text[si:ei]
pat=re.compile(r'(PRINTFORM[LW]\s+)「」')
cnt=len(pat.findall(block))
print('@HOURAI_KOJO_32 空:',cnt,'/用意:',len(slots))
assert cnt==len(slots), f'不一致 {cnt} vs {len(slots)}'
it=iter(slots)
block2=pat.sub(lambda m:m.group(1)+'「'+next(it)+'」', block)
assert not list(it)
text=text[:si]+block2+text[ei:]
data=text.encode('cp932')
assert b'\r\n' not in data, 'CRLF混入'
open(PATH,'wb').write(data)
print('蓬莱@32充填完了。LF維持:', b'\r\n' not in data,'/半角~:',data.count(b'~') if False else text.count(chr(0x7E)))
print('%CALLNAME:PLAYER%:', block2.count('%CALLNAME:PLAYER%'))
