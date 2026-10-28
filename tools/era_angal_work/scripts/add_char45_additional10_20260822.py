from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"

ADDITIONAL = '''
;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
\tCALL AITE_YOBI, 45, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%の唇を奪うところまで、転校生のお兄さまに見せるなんて……ふふ、少しばかり刺激的でよろしくてよ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅ……♪　%LOCALS%が照れるほど、もっと見せつけたくなるわね。お兄さま、目を逸らしてはいけなくてよ？」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%、もう一度。わたくしが欲しいのは、あなたの戸惑う顔ですもの……お兄さまも、きちんとご覧なさい♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、%LOCALS%と？　あなた、わたくしにずいぶん大胆な役を……あら、断るとは言っていなくてよ？」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ん……ふふ、今のは挨拶にしては長かったかしら。%LOCALS%、そんな顔をなさらないで」
\t\tELSE
\t\t\tPRINTFORMW 「あなたの唇、思ったより素直ね。……ええ、もう一度くらいなら、よろしくてよ♪」
\t\tENDIF
\tENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
\tCALL AITE_YOBI, 45, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と息を合わせて、あなたを挟むのね。ふふ、三人の視線までわたくしの掌の上……よろしくてよ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あら、%LOCALS%の熱がこちらまで返ってくるわ。坊や、まだ余裕があるつもりかしら？」
\t\tELSE
\t\t\tPRINTFORMW 「ふふ、二人分で翻弄されている顔……。あなた、わたくしから目を逸らしてはいけなくてよ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、二人がかりですの？　あなた、わたくしをずいぶん甘く見ていたのではなくて？」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「%LOCALS%と動きが重なると、思ったより……っ。あら、わたくしまで乱すおつもりかしら」
\t\tELSE
\t\t\tPRINTFORMW 「急ぐ必要はなくてよ。二人とも、わたくしが合図するまで待ちなさいな」
\t\tENDIF
\tENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
\tCALL AITE_YOBI, 45, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%の震えが、そのままわたくしの奥へ返ってくるのね……ふふ、思った以上に対等でよろしくてよ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ……%LOCALS%が動くたび、わたくしまで……。そんなふうに息を乱されるの、悪くなくってよ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「もう少し、強くてもよろしくてよ。%LOCALS%の顔を見ていると、わたくしまで素直になりそう……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「これは……%LOCALS%の動きが、こちらにも返ってくるの？　まあ、なかなか興味深い経験ですこと」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……！　%LOCALS%、急に動くのはおよしなさいな。わたくし、驚いて声が……っ」
\t\tELSE
\t\t\tPRINTFORMW 「ふふ、手を握っていてくださる？　余裕があるように見えて、わたくしも少し不安なのよ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、そんなに欲しがって……ふふ、よろしいわ。好きなだけ甘えていらっしゃい♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「飲む音を聞かせるなんて、ずいぶん甘え上手になったものね。わたくし、褒めてあげてよ♪」
\t\tELSE
\t\t\tPRINTFORMW 「離れるのはまだ早くてよ。あなたが満足するまで、わたくしが抱いていてあげるわ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「あら、わたくしの胸から直接？　坊や、ずいぶん大胆なお願いをするのねぇ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……そんなに近くで見上げるのはおよしなさいな。令嬢の沽券が……っ」
\t\tELSE
\t\t\tPRINTFORMW 「もう十分ではなくて？　……いえ、あなたがそんな顔をするなら、あと少しだけよろしくてよ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「搾る手つきまで覚えてしまったのね。ふふ、あなたに任せるのも悪くなくってよ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あら、そんなに見つめて……出てくるものまで愛でるなんて、よほどわたくしが好きなのね♪」
\t\tELSE
\t\t\tPRINTFORMW 「もう少し丁寧になさい。わたくしの胸を扱えるのは、あなたにだけ許した特権ですもの……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、手で搾るおつもり？　作業のように扱ったら、すぐに減点してよ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ……そこは少し強すぎてよ。わたくしの顔色を見ながら、上品におやりなさいな」
\t\tELSE
\t\t\tPRINTFORMW 「量を数えるのはおやめなさい。令嬢の秘密を数字にするなんて、よろしくなくてよ……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「そこ……っ。わたくしの余裕を崩す場所を、よく見つけたわね……ふふ、続けてよろしくてよ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、待って……止めるとは言っていなくてよ。あなたの指、もう少しだけ……」
\t\tELSE
\t\t\tPRINTFORMW 「声が、隠せない……。お兄さま、そんな顔でご覧になるなんて、ずるいわ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「そこは……っ、あら、わたくしの弱点を探すなんて、なかなか生意気ですこと」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぁ……っ、い、いまのは忘れなさい。令嬢の声を記事にするなど、許しませんからね……っ」
\t\tELSE
\t\t\tPRINTFORMW 「少し休ませなさいな……。まだ、わたくしの頭がきちんと働いておりませんの」
\t\tENDIF
\tENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「あら……止められないのね。こんな姿まで見せるのは、あなたを信じているからでしてよ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「目を逸らしてはいけなくてよ？　恥ずかしいところほど、あなたには見届けてもらいますから……」
\t\tELSE
\t\t\tPRINTFORMW 「ふふ……わたくしの沽券が、ずいぶん簡単に崩れてしまったわね。抱きしめて、今夜は離れないで♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「な、何ですの!?　待ちなさい、これは事故でしてよ！　わたくしの意志では……っ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「見ないで、とは言いませんけれど……笑ったら、次の茶会には呼びませんからね……！」
\t\tELSE
\t\t\tPRINTFORMW 「今のことは忘れなさい。これは令嬢と坊やの、秘密の取引でしてよ……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
\tCALL AITE_YOBI, 45, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%の胸と触れ合うと、あなたの反応とは違う熱が返ってくるのね……ふふ、興味深いわ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……%LOCALS%の鼓動、こんなに近いの。わたくし、落ち着いているふりが難しくなってきたわ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%、そのまま……。あなたの柔らかさを知るの、わたくしだけの秘密にしておきましょう♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、%LOCALS%と胸を合わせるの？　ふふ、ずいぶん大胆な趣向ですこと」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ……いきなり押しつけるのはおよしなさいな。わたくし、驚いてしまってよ……っ」
\t\tELSE
\t\t\tPRINTFORMW 「顔を見られるほうが困るわね……%LOCALS%、少しだけゆっくりにしてくださる？」
\t\tENDIF
\tENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
\tCALL AITE_YOBI, 45, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「転校生のお兄さまに騎乗したまま、%LOCALS%が顔に……。ふふ、二人分の熱を受け止めるのも、わたくしの役目かしら♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「%LOCALS%が動くたび、下からも揺らされて……っ。あら、わたくしを崩すつもりなのね、お兄さま……♪」
\t\tELSE
\t\t\tPRINTFORMW 「二人とも、わたくしを見ていらっしゃい。どちらかだけに構われるなど、よろしくなくてよ……っ」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「まあ、騎乗したまま顔まで？　あなた、わたくしをどうしたいのかしら……！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「%LOCALS%が動くと、下まで揺れるのね……っ。あら、これは少々、手に余りましてよ」
\t\tELSE
\t\t\tPRINTFORMW 「急に動くのはおよしなさい。わたくしが合図するまで、二人ともゆっくりなさいな……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「よしよし……♪　今日もよく耐えましたわね、お兄さま。わたくしが撫でて差し上げるから、何も考えず甘えていらして♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「まあ、目を閉じてしまうの？　ふふ、そんなにわたくしの手が気に入ったなら、もっと撫でてあげますわ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「お話はしなくてよろしくてよ。わたくしの膝で、心が静まるまで休んでいらっしゃいな……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「転校生くん、少しお疲れのようね。よろしければ、わたくしが頭を撫でて差し上げてよ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あら、素直に目を閉じるなんて……ふふ、たまには誰かに甘えるのも悪くなくてよ」
\t\tELSE
\t\t\tPRINTFORMW 「言葉にできないことまで、無理に話す必要はなくてよ。わたくしが聞いて差し上げるわ……」
\t\tENDIF
\tENDIF
ENDIF
'''

def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))

def main() -> None:
    text = read_cp932(TARGET)
    if ";--- COM60 助手にキスさせる ---" in text:
        raise SystemExit("CHAR45 additional10 already exists")
    marker = "\nRETURN 0\n"
    positions = [i for i in range(len(text)) if text.startswith(marker, i)]
    if not positions:
        raise SystemExit("main RETURN 0 not found")
    insert_at = positions[-1]
    text = text[:insert_at] + "\n" + ADDITIONAL.strip("\n") + "\n" + text[insert_at:]
    write_cp932(TARGET, text)
    print("added CHAR45 additional10: 10 commands / 60 lines")

if __name__ == "__main__":
    main()

