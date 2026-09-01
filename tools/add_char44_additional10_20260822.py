from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_44_笹芽ひよの_COM.ERB"

ADDITIONAL = '''
;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
\tCALL AITE_YOBI, 44, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%の唇、やわらかいですぅ……。転校生さんに見られてるのに、もう一度って思ってしまいます……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅ……っ。あうっ、顔が近いですぅ……！　%LOCALS%の反応、気になって仕方ないですけど、今は離れたくないですぅ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%が目を閉じると、わたしまで逃げられなくなって……転校生さん、もう少しだけ見ていてくださいぃ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「えっ、%LOCALS%とキスするんですかぁ!?　あ、あの、まずは心の準備を……はわわっ、近いですぅ……！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ……ちゅ、って……。い、いまのは確認ですぅ！　取材ではなくて、えっと……確認ですからぁ……っ」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%、ごめんなさい、まだ心の準備が……。でも、そんな顔をされたら、もう一度だけなら……っ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
\tCALL AITE_YOBI, 44, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と息を合わせて、転校生さんを挟むんですかぁ……。はわわ、わたし、どこを見たら……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、%LOCALS%の動きが返ってきて……転校生さんの熱も、いっぺんに……っ。二人とも、ゆっくりでお願いしますぅ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「脚が震えて、合図も出せないですぅ……。%LOCALS%、わたしの手、握っててください……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ、ふたりで、ですかぁ!?　わたし一人でもいっぱいいっぱいなのに……はわわっ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、待ってくださいぃ……！　%LOCALS%と動きが重なると、わたし、どちらに合わせれば……っ」
\t\tELSE
\t\t\tPRINTFORMW 「転校生さん、急がないでくださいねぇ……。わたしが倒れたら、新聞部の原稿が止まっちゃいますぅ……っ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
\tCALL AITE_YOBI, 44, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と同じ震えが返ってくる……っ。あう、離れてるのに、近いですぅ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……%LOCALS%が動くと、こっちまで同じところが跳ねて……声、抑えられないですぅ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%の息が聞こえるたび、もっと合わせたくなって……わたし、取材どころじゃなくなりましたぁ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ……同じ震えが、返ってくるんですかぁ!?　%LOCALS%、だいじょうぶですか、これ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひぅっ、動くたびに、こっちまで……っ。ま、待って、わたし、うまく言葉に……」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%、手を握っててくださいぃ……。ひとりで耐えるより、少し安心できる気がしますぅ……っ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「そ、そんなに近くで……。転校生さんが飲んでる音、聞こえますぅ……っ。はわわ、顔が熱いですぅ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ……急がなくていいですからねぇ。わたし、見られてるだけで、胸までそわそわして……♪」
\t\tELSE
\t\t\tPRINTFORMW 「ふぇ……もう少し、このままですかぁ？　転校生さんが嬉しそうなら、わたしも……がんばりますぅ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「え、えぇ!?　本当に飲むんですかぁ!?　わたし、そんなに大きくないですし、期待されても……はわわっ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひぅっ、音が近いですぅ……！　あの、わたしの顔を見ないでくださいぃ……っ」
\t\tELSE
\t\t\tPRINTFORMW 「もう、終わりでいいですかぁ……？　胸が変に敏感になって、落ち着かないですぅ……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「そんなに丁寧に触れられると、胸まで調べられてるみたいで……って、何を言ってるんですかわたしぃ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、そこ、力が変わると……っ。転校生さん、わたしの顔を見て、ちゃんと加減してくださいねぇ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「出てくるものまで見られるの、恥ずかしいですぅ……でも、あなたがそんな顔をするなら……もう少しだけ……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「手で、ですかぁ……？　あ、あの、急に量を確認しないでくださいねぇ……っ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ、強いですぅ！　胸だけじゃなくて、お腹までびくってして……そ、そんなに見ないで……！」
\t\tELSE
\t\t\tPRINTFORMW 「わたし、手伝えませんから、やさしくしてくださいねぇ……。痛くなったら、すぐ言いますぅ……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「そこ、ですぅ……っ。転校生さん、どうしてそんなに正確なんですかぁ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あ、あうっ……！　わたし、返事をする余裕が……でも、止めないでくださいぃ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「はわわっ、脚に力が入らないですぅ……。転校生さんのそばから、離れたくない……っ」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「そこは、だめですぅっ……！　え、違います、止めてじゃなくて、えっと……少し、待ってくださいぃ……！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇっ、声が変ですぅ……！　い、いまのは記事にしないで、忘れてくださいねぇ……っ」
\t\tELSE
\t\t\tPRINTFORMW 「もう、何も考えられないですぅ……。少しだけ、手を止めて……わたし、呼吸を戻しますから……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「ま、待ってくださいぃ……！　転校生さんの前で、こんな……はわわ、わたしの身体、言うことを聞いてくれません……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あうっ……そんなに見ないでくださいぃ……。でも、手を握ってくれるなら、逃げませんから……」
\t\tELSE
\t\t\tPRINTFORMW 「ふぇぇ……これも、記事にしたら誰も信じてくれませんよぉ……。転校生さんだけは、笑わないでくださいね……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ!?　ち、違います、これは事故ですぅ！　わたしがしたいわけじゃ……はわわっ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「見ないでくださいぃ……！　わたし、新聞記者なのに、こんな失態……。あの、誰にも言わないで……っ」
\t\tELSE
\t\t\tPRINTFORMW 「ご、ごめんなさい……。いまは、何も聞かないでください。わたしが落ち着くまで、少し離れてて……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
\tCALL AITE_YOBI, 44, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%の胸、近いですぅ……。触れるたびに、息まで同じになって……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……%LOCALS%の鼓動、こんなに近くで聞こえるんですねぇ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%、もう少しだけ、ゆっくり……わたし、逃げたくないのに、顔が熱くて……っ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ、胸を合わせるんですかぁ!?　あ、あの、まず説明を……はわわっ、近いですぅ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひぅっ、触れるたびにびっくりしますぅ……。%LOCALS%、急がないでくださいねぇ……っ」
\t\tELSE
\t\t\tPRINTFORMW 「わたし、どこを見ればいいんですかぁ……？　顔を見たらもっと恥ずかしいですぅ……」
\t\tENDIF
\tENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
\tCALL AITE_YOBI, 44, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「転校生さんに乗ったまま、%LOCALS%が顔の上に……っ。ふたつ同時なんて、わたし、取材メモも落としちゃいますぅ……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「%LOCALS%が動くと、下からも揺れて……っ。あうっ、わたし、どちらに合わせればいいんですかぁ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「転校生さん、%LOCALS%、ちゃんと、わたしのこと見ててくださいぃ……。ひとりにされたら、泣いちゃいますぅ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ、転校生さんに乗ったまま、%LOCALS%が顔に……!?　わ、わたし、そんな器用にできませんよぉ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、待ってくださいぃ！　%LOCALS%が動くと、下まで揺れて……脚が、脚がもちませんっ！」
\t\tELSE
\t\t\tPRINTFORMW 「どちらも急に動かないでくださいねぇ……。わたし、ちゃんと返事できるように、ゆっくりお願いしますぅ……っ」
\t\tENDIF
\tENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「よしよし……♪　転校生さん、今日もお疲れさまですぅ。わたしでよければ、ここにいますからねぇ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「はわわっ、そんなに目を閉じてくれると……わたし、もっと撫でたくなりますぅ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「うまく言葉にできないことも、記事にしなくて大丈夫ですぅ。わたしが、黙って聞いてますから……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「あの、転校生さん……少しだけ、頭を撫でてもいいですかぁ？　つ、疲れてるように見えますぅ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇっ、目を閉じた……えっと、眠っても大丈夫ですよぉ。わたし、起こしますから……たぶん」
\t\tELSE
\t\t\tPRINTFORMW 「わたし、話を聞くのは得意ですぅ……書くより、今日は聞くだけにしますからねぇ」
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
        raise SystemExit("CHAR44 additional10 already exists")
    marker = "\nRETURN 0\n"
    positions = [i for i in range(len(text)) if text.startswith(marker, i)]
    if not positions:
        raise SystemExit("main RETURN 0 not found")
    insert_at = positions[-1]
    text = text[:insert_at] + "\n" + ADDITIONAL.strip("\n") + "\n" + text[insert_at:]
    write_cp932(TARGET, text)
    print("added CHAR44 additional10: 10 commands / 60 lines")

if __name__ == "__main__":
    main()
