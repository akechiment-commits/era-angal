from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_66_曽根セイラ_COM.ERB"


RESTORE_COM3 = r'''IF SELECTCOM == 3
    ; ビデオ撮影中
    IF TEQUIP:53
        A = RAND:3
        IF TALENT:TARGET:153
            IF A == 0
                ;恋人・ビデオ・1
                PRINTFORMW 「ふぁっ……あぁん、ビデオ撮ってるのっ！？　はうう、恥ずかしいけれど、転校生くんが残したいなら……だぁい好きっ☆」
            ELSEIF A == 1
                ;恋人・ビデオ・2
                PRINTFORMW 「んん、ふぁ……っ、あぁ、ビデオに残っちゃうの～！　はうう、ちゃんと撮れてるかしら？」
            ELSE
                ;恋人・ビデオ・3
                PRINTFORMW 「あぁん、転校生くんっ、後で一緒に観るのね？　ふふ、絶対二人だけでなのだけれどっ☆」
            ENDIF
        ELSE
            IF A == 0
                ;通常・ビデオ・1
                PRINTFORMW 「は、ひっ……ビ、ビデオはっ！？　うう、絶対誰にも見せないでねっ、お願いだけれど！」
            ELSEIF A == 1
                ;通常・ビデオ・2
                PRINTFORMW 「ふぁ、はうう……ビデオに残るって、刺激的なのだけれど～♪」
            ELSE
                ;通常・ビデオ・3
                PRINTFORMW 「んん、ふぁ……っ、転校生くんの趣味って、けっこう深いのね？　ふふふ♪」
            ENDIF
        ENDIF
    ELSE
        ; 通常
        A = RAND:3
        IF TALENT:TARGET:153
            IF A == 0
                ;恋人・1
                PRINTFORMW 「ふぁっ……あぁん、転校生くんに見られながらだけれどっ！？　はうう、恥ずかしいけれど興奮しちゃうのだけれど～♪」
            ELSEIF A == 1
                ;恋人・2
                PRINTFORMW 「んん、ふぁ……あぁ、転校生くんの目線を感じるけれど～♪　ふふ、もっと見て、なのだけれど！」
            ELSE
                ;恋人・3
                PRINTFORMW 「あぁん、ふぁ、ふぁ……っ、転校生くんに見せるって、こんな興奮するのね？　だぁい好きっ☆」
            ENDIF
        ELSE
            IF A == 0
                ;通常・1
                PRINTFORMW 「は、ひっ……み、見ないでっ！？　うう、自分でいじってるとこ恥ずかしいけれど～！」
            ELSEIF A == 1
                ;通常・2
                PRINTFORMW 「ふぁ、はうう……っ、んん、自分でやるのと違う気分なのだけれど～♪」
            ELSE
                ;通常・3
                PRINTFORMW 「あぁん、ねぇ、転校生くんが見てると、あたしいつもより興奮しちゃうけれど～♪」
            ENDIF
        ENDIF
    ENDIF
ENDIF
'''


ADDITIONAL10 = r''';=== CHAR66 曽根セイラ 追加10 START ===
;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
    CALL AITE_YOBI, 66, ASSI
    LOCALS '= @"%RESULTS%"
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「%LOCALS%と唇を重ねるの、ふふふ……転校生くんに見られていても、今夜はあたしのRock'n'Rollなのだけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んん……%LOCALS%の息が近いのね。音楽みたいに呼吸を合わせたら、もっと気持ちよくなるかしら？」
        ELSE
            PRINTFORMW 「はうう……もう一度だけ、%LOCALS%にお願いしてもいい？　転校生くん、あたしたちのハーモニーを聴いていてね☆」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「%LOCALS%とキスするの、ちょっと緊張するけれど……転校生くん、笑わないで見ていてね？」
        ELSEIF A == 1
            PRINTFORMW 「んん、顔が近いと心臓が忙しいのだけれど。%LOCALS%、急がないで、あたしのペースにしてほしいの♪」
        ELSE
            PRINTFORMW 「はうう……女の子同士でも、こんなにどきどきするのね。転校生くん、今のは内緒にしてくれるかしら？」
        ENDIF
    ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
    CALL AITE_YOBI, 66, ASSI
    LOCALS '= @"%RESULTS%"
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「%LOCALS%と一緒に転校生くんを挟むのね。ふふふ、息を合わせるのもバンドみたいで楽しいけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んんっ……両側から熱が来ると、あたしまで歌いたくなっちゃうのだけれど。%LOCALS%、もう少しだけ揃えてね☆」
        ELSE
            PRINTFORMW 「はうう、あたしと%LOCALS%のリズム、ちゃんと聴こえてるかしら？　転校生くん、最後まで目をそらさないでね♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「%LOCALS%と一緒にするなんて聞いてなかったのだけれど……転校生くん、急に強くしないで、お願いね？」
        ELSEIF A == 1
            PRINTFORMW 「んん、脚の置き場所がわからなくなっちゃうの。%LOCALS%、あたしに合わせて、ゆっくりにしてくれるかしら？」
        ELSE
            PRINTFORMW 「は、はうう……ふたり分の熱で頭までぼうっとするけれど、笑わないでね。あたし、ちゃんと頑張っているのだから！」
        ENDIF
    ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
    CALL AITE_YOBI, 66, ASSI
    LOCALS '= @"%RESULTS%"
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「%LOCALS%と一本の振動を分けるのね。ふふふ、音のない楽器みたいで、身体の奥まで一緒に響くけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んんっ……%LOCALS%の震えが伝わるたび、あたしの声まで揃っちゃうの。転校生くん、もっと聴いていてね☆」
        ELSE
            PRINTFORMW 「はうう……離れたくないのに、力が抜けちゃうけれど。%LOCALS%、最後まで手をつないでいてほしいの♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「%LOCALS%と同じ道具を使うのね？　説明を聞いているだけで緊張するけれど、乱暴にはしないでね……」
        ELSEIF A == 1
            PRINTFORMW 「んん、そこまで震えると思わなかったのだけれど……%LOCALS%、あたしの声が聞こえなくなるほど急にしないでっ」
        ELSE
            PRINTFORMW 「は、はうう……女の子同士でつながっているみたいで、変な感じなの。転校生くん、見ているなら責任を持ってね？」
        ENDIF
    ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「んん……そんなに夢中で飲んでくれるのね。はうう、あたしのことを必要としてくれるの、だぁい好きっ☆」
        ELSEIF A == 1
            PRINTFORMW 「ふふふ、急がなくても逃げないけれど……転校生くんが甘えてくれるなら、もう少しこのままでいてあげるの♪」
        ELSE
            PRINTFORMW 「はうう……あたしの胸に顔を埋めているのね。心臓の音まで聞こえているかしら？　安心して眠ってもいいのだけれど☆」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「えっ、飲むの？　んん……恥ずかしいけれど、そんなに頼まれたら、少しだけならいいのだけれど……」
        ELSEIF A == 1
            PRINTFORMW 「はうう、そんな音を立てたら聞こえちゃうの。転校生くん、ゆっくりにして、あたしの顔も見ないでね？」
        ELSE
            PRINTFORMW 「ふふ、ちゃんと飲めているかしら？　終わったらすぐ離れるのではなくて、少しだけ抱きしめてほしいのだけれど♪」
        ENDIF
    ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「そんなに優しく触れてくれるのね。ふふふ、転校生くんの手つき、ライブ前のチューニングより丁寧なのだけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んん……見られながら搾られると、胸だけじゃなくて顔まで熱くなるの。もっとあたしを見ていてね☆」
        ELSE
            PRINTFORMW 「はうう、止められると余計に気になっちゃうけれど……転校生くんが満足するまで、あたしが歌っていてあげるの♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「痛くしないでね？　あたし、こういうのは慣れていないのだけれど……手つきは、ちゃんと優しくしてほしいの」
        ELSEIF A == 1
            PRINTFORMW 「んんっ、急に強くしたらびっくりするけれど！　あたしの顔を見て、加減を覚えてくれるかしら？」
        ELSE
            PRINTFORMW 「ふふ……そんなに真剣な顔をしなくてもいいの。けれど、終わるまでそばにいてくれるなら、少し安心できるのだけれど♪」
        ENDIF
    ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「そこを見つけたのね？　はうう、転校生くんはあたしの弱い音まで探すのが上手なのだけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んんっ、言葉より先に声が出ちゃうの。ふふふ、そんなにあたしを夢中にさせて、どうするつもりかしら☆」
        ELSE
            PRINTFORMW 「はうう……もう少しだけ、そこを離さないで。Rock'n'Rollみたいに、途切れずに響かせてほしいの♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「そこは、まだ心の準備が……んん、でも、止めてとは言っていないのだけれど。ゆっくりお願いね？」
        ELSEIF A == 1
            PRINTFORMW 「は、はうう……声が変になっちゃうけれど、笑わないで！　あたし、ちゃんと返事をしたいのにできないのだから！」
        ELSE
            PRINTFORMW 「んん、こんなところで音楽のことを考える余裕がなくなるなんて……転校生くん、責任を取ってくれるかしら？」
        ENDIF
    ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「は、はうう……止められないのね。転校生くん、見ていてもいいけれど、あたしをひとりにしないでね……♪」
        ELSEIF A == 1
            PRINTFORMW 「んんっ、こんな音まで聞かれちゃうの！？　ふふ、恥ずかしいけれど、恋人さんなら受け止めてくれるかしら☆」
        ELSE
            PRINTFORMW 「あぁ……あたしの身体、勝手に歌っているみたい。終わったら、何も言わずに抱きしめてほしいのだけれど♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「や、やめて、止められないのっ！？　はうう……こんなの、転校生くんに見られたくないのだけれど！」
        ELSEIF A == 1
            PRINTFORMW 「は、ひっ……あたし、ちゃんと我慢できると思っていたのに！　お願いだから、今のことは忘れてねっ」
        ELSE
            PRINTFORMW 「んん……身体が言うことを聞かないの。笑ったら泣いちゃうけれど、終わるまで手だけ握っていてくれるかしら？」
        ENDIF
    ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
    CALL AITE_YOBI, 66, ASSI
    LOCALS '= @"%RESULTS%"
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「%LOCALS%と胸を合わせるのね。ふふふ、音を合わせるみたいに息まで重なるの、素敵だけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んん……%LOCALS%の鼓動が近いの。転校生くん、あたしたちのハーモニー、ちゃんと聴こえているかしら☆」
        ELSE
            PRINTFORMW 「はうう、離れると物足りなくなっちゃうのだけれど……%LOCALS%、もう少しだけこのままでいてね♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「%LOCALS%と胸を合わせるの？　女の子同士でも恥ずかしいけれど、急に押しつけないで、合図をしてね？」
        ELSEIF A == 1
            PRINTFORMW 「んんっ……肌が触れると、思ったより熱いのね。転校生くん、見ているなら変なことを言わないでくれるかしら！」
        ELSE
            PRINTFORMW 「はうう……%LOCALS%の呼吸まで伝わってくるの。あたし、ちゃんと平気な顔をしていられている？」
        ENDIF
    ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
    CALL AITE_YOBI, 66, ASSI
    LOCALS '= @"%RESULTS%"
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「%LOCALS%が転校生くんの顔に乗るのね。あたしも上で揺れているけれど、二人とも置いていかないでね♪」
        ELSEIF A == 1
            PRINTFORMW 「んん……脚に力を入れると、%LOCALS%の声まで近くなるの。ふふふ、三人で歌っているみたいだけれど☆」
        ELSE
            PRINTFORMW 「はうう、あたしの腰も転校生くんの呼吸も止まらないのね。%LOCALS%、あたしとリズムを合わせてほしいの♪」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「%LOCALS%まで顔に乗るなんて聞いていないのだけれど！　転校生くん、苦しくないか見ながら、あたしにも教えてね？」
        ELSEIF A == 1
            PRINTFORMW 「んんっ、上も下も揺れると、どこへ力を入れればいいのかわからなくなるの。急に動かないでね！」
        ELSE
            PRINTFORMW 「は、はうう……%LOCALS%の声が近すぎて、あたしまで慌てちゃうけれど。転校生くん、ちゃんと息をしているかしら？」
        ENDIF
    ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
    A = RAND:3
    IF TALENT:TARGET:85
        IF A == 0
            PRINTFORMW 「よしよし、今日もよく頑張ったのね。転校生くんの頭を撫でていると、あたしまで安心するのだけれど♪」
        ELSEIF A == 1
            PRINTFORMW 「んん、ここに頭を預けていていいの。あたしがゆっくり撫でてあげるから、音楽を聴くみたいに力を抜いてね☆」
        ELSE
            PRINTFORMW 「はうう……転校生くんの髪、触れていると落ちつくの。あたしがそばにいるって、手のひらで伝わるかしら？」
        ENDIF
    ELSE
        IF A == 0
            PRINTFORMW 「ほら、頭をこちらへ。元気がないときくらい、あたしに甘えてもいいのだけれど……よしよし♪」
        ELSEIF A == 1
            PRINTFORMW 「んん、そんなに俯かないで。あたしが撫でているから、少しだけ顔を上げてくれるかしら？」
        ELSE
            PRINTFORMW 「はうう……大丈夫、大丈夫なの。あたしが何度でも撫でてあげるから、ひとりで頑張らなくていいのだけれど♪」
        ENDIF
    ENDIF
ENDIF
;=== CHAR66 曽根セイラ 追加10 END ===
'''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    if re.search(r"(?m)^IF SELECTCOM == 3[ \t]*$", text):
        lines = text.split("\n")
        custom_comment = next(
            (line for line in lines if line.startswith(";--- COM410-414 ")),
            ";--- COM410-414 独自純愛 ---",
        )
        lines = [line for line in lines if not line.startswith(";--- COM410-414 ")]
        com4_comment = next(
            (line for line in lines if line.startswith(";--- COM4 ")),
            ";--- COM4 フェラする ---",
        )
        lines = [line for line in lines if not line.startswith(";--- COM4 ")]
        lines = [line for line in lines if not line.startswith(";--- COM3 ")]

        com3 = next(i for i, line in enumerate(lines) if line.strip() == "IF SELECTCOM == 3")
        lines.insert(com3, ";--- COM3 ビデオ撮影中 ---")
        com4 = next(i for i, line in enumerate(lines) if line.strip() == "IF SELECTCOM == 4")
        lines.insert(com4, com4_comment)
        com410 = next(i for i, line in enumerate(lines) if line.strip() == "IF SELECTCOM == 410")
        lines.insert(com410, custom_comment)
        TARGET.write_bytes("\r\n".join(lines).encode("cp932"))
        print("CHAR66: repaired COM3/COM4 annotations")
        return
    for command in (60, 62, 76, 78, 79, 84, 86, 202, 258, 318):
        if re.search(rf"(?m)^IF SELECTCOM == {command}[ \t]*$", text):
            raise SystemExit(f"CHAR66 COM{command} already exists")

    marker = re.search(r"(?m)^IF SELECTCOM == 4[ \t]*$", text)
    if marker is None:
        raise SystemExit("CHAR66 COM4 anchor is missing")
    text = text[: marker.start()] + RESTORE_COM3 + "\n" + text[marker.start() :]

    marker = re.search(r"(?m)^;--- COM0[^\n]*$", text)
    if marker is None:
        raise SystemExit("CHAR66 COM0 anchor is missing")
    text = text[: marker.start()] + ADDITIONAL10 + "\n" + text[marker.start() :]
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("CHAR66: restored COM3 and added COM60/62/76/78/79/84/86/202/258/318")


if __name__ == "__main__":
    main()
