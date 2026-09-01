from __future__ import annotations

from pathlib import Path
import re


TARGET = Path(r"ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB")
MARKER = ";=== BOTAN RAND3 AND ADDITIONAL10 START ==="


def q(*lines: str) -> tuple[str, ...]:
    if len(lines) != 6:
        raise ValueError("expected lover3 + normal3")
    return lines


NEW_LINES: dict[int, tuple[str, ...]] = {
    60: q(
        "%LOCALS%に触れた唇が、まだ熱い……。転校生くん、そんな顔で見てたの？",
        "ん……ちゅ。%LOCALS%も照れてる。ふふ、わたしまで隠れたくなるなぁ",
        "もう一度？　……そんなに見つめられたら、断るほうが難しいよ♪",
        "%LOCALS%にキスするの？　転校生くん、急に決めるから心の準備が間に合わないよ",
        "ちゅ……。今のは驚いただけ。……でも、嫌だったとは言ってないからね",
        "%LOCALS%の頬、赤いね。わたしまで変に意識しちゃうから、あんまり見ないでよ",
    ),
    62: q(
        "%LOCALS%の熱と転校生くんの熱が重なると、脚まで落ち着かなくなる……ふふ、二人ぶんは贅沢だね♪",
        "%LOCALS%、そのまま……転校生くんの息が変わるたび、わたしもつられてしまう",
        "一緒に動くと、どっちのせいで震えてるのか分からないね。……まあ、分からなくてもいいか♪",
        "えっ、二人で？　わたしの脚が急に忙しくなっちゃった……",
        "%LOCALS%、そんなに急がないで。転校生くんまで動くと、合わせられないよ",
        "ふふ、競争しなくていいからね。ちゃんと息を合わせてくれたら、もう少し楽にできるんだけど",
    ),
    76: q(
        "%LOCALS%の動きがそのまま返ってくる……。ふふ、ひとつの熱を分け合ってるみたい♪",
        "そんなに急がなくていいよ。%LOCALS%が震えると、わたしまで釣られちゃう",
        "止まると名残惜しくて、続くと声が追いつかない……%LOCALS%、もう少しだけね",
        "%LOCALS%、今のは強いよ……。わたしの声、聞こえてる？",
        "動きがずれると、変なところで重なってしまうね。ふふ、ゆっくりでいいから",
        "あっ、また返ってきた……。そんなふうにされたら、平気なふりが続かないよ",
    ),
    78: q(
        "そんなに急がなくていいよ……。甘えられると、わたしのほうが離せなくなる♪",
        "夢中になってる顔を見てると、胸の奥までくすぐったいね。ゆっくりでいいよ",
        "音が近くで響くと、わたしまで平然としていられなくなる……もう少し、こっちへ",
        "ほ、本当に口をつけるの？　そんな目で決められたら、わたし断れなくなるよ……",
        "顔を上げると目が合っちゃう……っ。今は、見ないでくれないかな",
        "終わった途端に離れないで。わたしの胸が、まだ落ち着いてないんだからね",
    ),
    79: q(
        "任せると決めたんだから、焦らず触ってね……。転校生くんの手つきなら信じられる♪",
        "指の動きを目で追っちゃうなぁ。胸に触れられるたび、平静を装うのが難しい",
        "そんなに丁寧にされると、拒む理由がなくなる……。ふふ、困ったひとだね",
        "数を取るみたいに扱わないで。これは作業じゃなくて、わたしの身体だよ",
        "そこまで強くしなくていい……。声が漏れても、笑わずに受け止めてよね",
        "視線の置き場に困るなぁ……。嫌じゃないけど、心の準備が追いついてないんだ",
    ),
    84: q(
        "そこに触られると膝から力が抜ける……。転校生くん、わたしの弱みを見つけたね♪",
        "返事をしようとすると声が細くなる……。この借りは、あとで返してもらうから",
        "止まると惜しくて、続くと乱れる……。わたし、ずいぶん欲張りになったね♪",
        "そこは、まだ触らないで……。今の声は聞かなかったことにしてくれる？",
        "一度、間を置いてよ……っ。気持ちが追いつかないまま進まれると、本当に困る",
        "頭が白くなるまで続くなんて……止めてほしいのに、手を退けてとも言えないよ",
    ),
    86: q(
        "見ないでって言っても、もう見てるんでしょ……。だったら、せめて笑わないで♪",
        "手を握るより肩を貸して。膝に力が戻るまで、ここにいてほしいんだ",
        "こんな姿を見ても逃げずにいてくれる……それだけで、少し救われるなぁ",
        "な、何をしたの……？　身体が勝手に言うことを聞かなくなって、恥ずかしいよ",
        "今のことを口にしたら、わたし、泣きそうだから……。何も言わずにいてね",
        "落ち着くまで、こっちを見ないで……でも、行かないで。そこにいてよね",
    ),
    202: q(
        "%LOCALS%の熱が胸越しに重なる……。近すぎて、逃げる理由がなくなるね♪",
        "擦れるたび呼吸のタイミングまで乱れる……。%LOCALS%、急がずそのまま",
        "張り合うつもりはないのに、二人の間で胸が揺れると、もっと感じたくなる",
        "胸を合わせるなら、いきなり押しつけないで……。%LOCALS%、まず様子を見てよ",
        "どうしてそこばかり見るの……っ。静かにしてくれたら、もう少し隠さずにいられるのに",
        "二人とも同じところへ触れると、反応が混ざって頭が追いつかないよ……",
    ),
    258: q(
        "転校生くんに跨がるわたしの下で、%LOCALS%が顔に触れて……二人ぶんの熱で足が震える♪",
        "%LOCALS%が転校生くんの顔の上で動くたび、わたしの腰まで揺れを拾う……苦しければ合図して",
        "わたしは腰を動かして、%LOCALS%は転校生くんの顔で……妙に息が合うと嬉しいね",
        "わたしが上で、%LOCALS%は転校生くんの顔へ……？　二人を同時に受け持つなんて聞いてないよ",
        "%LOCALS%、動きを合わせて。転校生くんの様子が見えないと、わたしも加減できないからね",
        "降りる必要はないけど、苦しかったらすぐ知らせて。無理をされるのは嫌だから",
    ),
    318: q(
        "もう、ひとりで頑張らなくていいよ。今日はわたしが、転校生くんの重さを預かるから♪",
        "言葉は後でいいよ。わたしの手がここにあることだけ、覚えてて",
        "撫でているうちに、わたしまで肩の力が抜けた……。眠るまで手を止めないよ",
        "顔を隠したままでもいい。でも、ひとりで耐えるのはもうやめて……わたしに預けて",
        "よく持ちこたえたね。今だけは刀を置くみたいに、何も背負わず休みなよ♪",
        "話したくなったときでいい。わたしは急かさないから、ここで待ってるね",
    ),
}


NEW_A0: dict[int, tuple[str, str]] = {
    60: ("%LOCALS%の唇、やわらかい……。ふふ、転校生くんが見てると、わたしまでそわそわするね♪", "%LOCALS%に触れるの？　わたし、こういうのはまだ慣れてないから、急に笑わないでよね"),
    62: ("二人ぶんの熱が重なると、脚が勝手に震える……ふふ、贅沢だね♪", "えっ、二人で？　わたしの脚、そんなに器用じゃないよ……ゆっくりね"),
    76: ("%LOCALS%とつながった熱が、ひとつの波みたいに来る……。変なのに、目が離せないね♪", "%LOCALS%、今の振動……少し強いよ。わたしの声、聞こえてる？"),
    78: ("そんなに甘えられると、胸のほうまで熱くなる……。ふふ、もう少しおいで♪", "えっ、ほんとうに飲むの？　……そんな顔されたら、断れないじゃない"),
    79: ("ゆっくりでいいよ。転校生くんの手が触れるたび、胸まで目を覚ますね♪", "いきなり強くしないで。わたし、作業みたいに扱われるのは嫌だから"),
    84: ("そこを探すの、上手になったね……。膝から力が抜けちゃうよ♪", "そこは……っ、まだ心の準備がないよ。声が出ても笑わないでね"),
    86: ("見ないでって言いながら、そばにはいてほしいんだ……。変だね、わたし♪", "えっ、待って……身体が勝手に……。こんなところ、見ないでよ"),
    202: ("%LOCALS%と胸が触れると、鼓動まで近くなるね……。ふふ、きれいな熱♪", "%LOCALS%とこんなに近くなるの？　いきなりは、ちょっと驚くよ"),
    258: ("わたしの下で%LOCALS%が動くと、腰までつられて……転校生くん、ちゃんと息してる？♪", "わたしが上で、%LOCALS%は顔のところ……？　先に言ってよ、心の準備がいるから"),
    318: ("ほら、力を抜いて。わたしの手、ちゃんとここにあるからね♪", "泣きそうな顔してるね。今日はわたしが、ゆっくり撫でてあげるよ"),
}


ORG: dict[str, tuple[str, ...]] = {}


def add_org(scene: str, love: tuple[str, str, str], normal: tuple[str, str, str]) -> None:
    ORG[f"恋人・{scene}"] = love
    ORG[f"通常・{scene}"] = normal


add_org("五重絶頂・全部位最強★", (
    "だめ……っ、甘いのも熱いのも、いっぺんに来て……わたし、もう笑えない……っ",
    "あ、あぁっ……足も胸も、ぜんぶ言うことを聞かない……。転校生くん、ぎゅって……っ",
    "待って……いく、いくから……っ。こんなに満たされて、わたし、どこまで溶けるの……っ",
), (
    "なに、これ……っ、あちこち勝手に跳ねて……わたし、立てない……っ",
    "や、やだ……声まで変になる……っ。見ないでって言えないの、ずるいよ……",
    "もう考えられない……っ、甘すぎて、頭の中までほどけて……っ",
))
add_org("五重絶頂・最強", (
    "あっ、だめ……熱が散らばって、息が追いつかない……っ",
    "ふぁ……まだ笑えると思ってたのに、転校生くんの腕で力が抜ける……",
    "いっちゃう……っ、止めないで。今日は、ちゃんと甘えていたい……♪",
), (
    "う、うそ……一度に来ると、平気な顔できないじゃない……っ",
    "息、どこで吸えばいいの……っ。わたしの声、聞かなかったことにしてよ……",
    "からだが勝手にほどけてく……もう、ちょっとだけゆっくりにして……っ",
))
add_org("五重絶頂・強", (
    "あっ……いっぱい来ちゃう……。ふふ、こんな顔、見せるつもりなかったのに",
    "ん……っ、身体のあちこちが忙しい……転校生くん、手を離さないで",
    "いく……っ、あぁ、また……。一緒だと、怖いくらい気持ちいいね……♪",
), (
    "ちょっと待って……一度に来すぎて、声が追いつかないよ……",
    "んっ……身体が跳ねた……。今の、見なかったことにできる？",
    "だめ、まだ余裕あると思ってたのに……足に力が入らない……っ",
))
add_org("五重絶頂・通常", (
    "ふふ……いっちゃった。こんなに一緒に感じると、満たされるね♪",
    "あ……今の、きれいに重なった……。転校生くん、もう一回はだめ？",
    "ふぅ、力抜けちゃった。甘いもの、あとでご褒美にしてね",
), (
    "あっ……いった、よ。……今のは、まあ、悪くなかったかな",
    "ん……身体がふるえた。こんなに反応するとは思わなかったよ",
    "ふふ、立てないや。少しだけ、そばにいてくれる？",
))

add_org("複絶頂・膣含む・最強", (
    "なかも、胸も、ぜんぶ重なって……っ、もうどこが気持ちいいのか分からない……",
    "あ、あぁ……奥からほどけてく……転校生くん、声、聞いてて……っ",
    "いく……っ、いっぺんに来るの、怖いのに……離れたくない……っ",
), (
    "なかと他のところが一緒に震える……っ、息が、うまくできない……",
    "ひっ……身体の中まで跳ねる……。これ以上は、平気なふりできないよ……っ",
    "あっ、もう……全部持っていかれる……っ、少しだけ待って……",
))
add_org("複絶頂・膣含む・強", (
    "なかが熱くて、別のところまでつられて……。ふふ、贅沢すぎるね",
    "ん……声が細くなる……転校生くん、そばで笑わないで……",
    "いく……っ、奥からきゅっと来た……。まだ手を離さないでね♪",
), (
    "なかが勝手にきゅっとする……他も一緒だと、頭が追いつかないよ……",
    "あ……今の、深く響いた……。もう少し、ゆっくりなら……",
    "いきそう……っ、こんなに正直になるの、困るなぁ……",
))
add_org("複絶頂・膣含む・通常", (
    "ふふ……いっちゃった。なかまで一緒にほどけると、しあわせだね♪",
    "あ、また来る……転校生くんの手、あったかい……",
    "まだ余韻が残ってる。もう少し、このまま寄りかかっていたいな",
), (
    "あっ……いった、よ。なかまで響くと、変な感じだね",
    "ん……胸と腰が同時にふるえた……。少し休ませてよね",
    "ふふ、思ったより効いたなぁ。変な顔で笑わないでよ？",
))

add_org("複絶頂・膣なし・最強", (
    "あちこちから来て、どこにも逃げられない……っ、転校生くん、抱いて……",
    "あぁ……胸も唇も、同時に熱い……わたし、もう返事できない……っ",
    "いく……っ、ぜんぶほどける……。ひとりにしないで、ね……っ",
), (
    "な、なにこれ……胸も息も、一緒に崩れる……っ",
    "ひっ……あちこち跳ねて、声を抑える場所がない……っ",
    "もう、どこを見ればいいの……。身体が勝手に終わらせちゃう……っ",
))
add_org("複絶頂・膣なし・強", (
    "熱が重なって、笑ってごまかせない……。もっと近くで見てて……",
    "ん……胸も腰も忙しい……転校生くん、手を握ってよ",
    "いく……っ、こんなにまとめて甘くなるなんて、ずるいね……♪",
), (
    "あっ、いろんなところが一緒に……。ちょっと、これは忙しすぎるよ……",
    "んっ……いま声出た？　……聞こえなかったことにしてね",
    "もう少しでだめ……。止まるなら、いまのうちにしてよ……っ",
))
add_org("複絶頂・膣なし・通常", (
    "ふふ、いっちゃった。あちこち一緒だと、君のそばから離れたくなくなるね♪",
    "あ……息がまだ戻らない。転校生くん、もう少しだけ触ってて",
    "胸も唇もじんじんする……今日は、わたしの負けでいいよ",
), (
    "あっ……いった。身体のあちこちがふるえるの、ちょっと恥ずかしいな",
    "ん……まだ熱い。落ち着くまで、急に離れないでよね",
    "ふふ、効いたよ。……まあ、少しくらいなら認めてあげる",
))

add_org("膣・最強", (
    "あっ……奥、深い……っ、もう、笑ってごまかせないよ。転校生くん、近くにいて……",
    "ふぁ……なかがほどける……っ。こんなに正直になるの、あなたのせいだからね……",
    "いく……っ、奥から押し上げられて、息が……。ぎゅって、して……っ",
), (
    "う、うそ……奥まで来ると、足が勝手に震える……っ",
    "ひっ……なか、熱い……。わたし、こんな声出すんだ……",
    "もう……だめ、いく……っ。少しだけ、ゆっくりにしてよ……",
))
add_org("膣・強", (
    "ん……奥に触れるたび、甘くなる……。もう少し、深くてもいいよ♪",
    "あっ、声がほどける……転校生くん、手を握って",
    "いきそう……っ、止まると寂しいから、そのままね",
), (
    "そこ、急に深くしないで……っ。身体が先に返事しちゃう",
    "ん……なかが熱い。今のは、ちょっと効いたかな",
    "あっ……もう少しで、変な声になる……見ないでよね",
))
add_org("膣・通常", (
    "ふふ、奥でふるえた……。転校生くんとなら、こういうのも悪くないね♪",
    "あ、来た……なかがあったかくなって、安心する",
    "まだ残ってる……今日は、もう少し抱いてて",
), (
    "あっ……いった、みたい。……ちょっと恥ずかしいな",
    "ん……今の深さ、覚えておこうかな",
    "ふふ、効いたね。水でも飲んで少し休もうよ",
))

add_org("アナル・最強", (
    "あっ……後ろ、熱い……っ、こんなところでほどけるの、悔しいのに……",
    "ふぁ……お尻の奥まで震えてる……転校生くん、手を離さないで……っ",
    "いく……っ、後ろでなんて……。もう、恥ずかしがる余裕もないよ……っ",
), (
    "う、うそ……後ろまで熱が回る……っ、声、抑えられない……",
    "ひっ……お尻が勝手に震えてる……。見ないで、でも行かないで……っ",
    "もうだめ……後ろでいくなんて、わたし、知らなかったよ……っ",
))
add_org("アナル・強", (
    "ん……後ろが熱い……。ふふ、変なところまで素直になっちゃうね",
    "あっ、響いた……転校生くん、もう少しだけ支えてて",
    "いきそう……っ、後ろから来るのも、悪くないかも……♪",
), (
    "そこ、急に押さないで……っ。後ろがじんじんして、落ち着かないよ",
    "ん……お尻がふるえた。今のは、聞かなかったことにしてね",
    "あっ、もう少し……。変なところで、声が出ちゃいそう……",
))
add_org("アナル・通常", (
    "ふふ、後ろでふるえた……。あなたのせいだよ♪",
    "あ、まだじんじんする……。もう少し、手を握ってて",
    "お尻まで熱くなるんだね。今日は新しいことを覚えちゃった",
), (
    "あっ……いった、よ。後ろでなんて、少しびっくりだな",
    "ん……まだ熱が残ってる。急に離れないでよね",
    "ふふ、効いたよ。……わたし、少し休んでもいい？",
))

add_org("クリ・最強", (
    "あっ……腰が勝手に跳ねる……っ、転校生くん、そこから逃がさないで……",
    "ふぁ……頭まで白くなる……。わたしの声、ちゃんと聞こえてる……？",
    "いく……っ、もう止められない……。こんなに乱れるの、悔しいよ……っ",
), (
    "う、うそ……腰が勝手に……っ、声まで追いつかないよ……",
    "ひっ……先から震えが上がってくる……。こんな、聞いてない……っ",
    "もうだめ……身体が先に終わっちゃう……。少し待ってよ……っ",
))
add_org("クリ・強", (
    "ん……そこ、好き……。止まると惜しくて、続くと声が崩れるね",
    "あっ、また跳ねた……転校生くん、笑わないでよ",
    "いきそう……っ、腰を押さえてても、もう隠せないね♪",
), (
    "そこ、同じところばかり……っ。わたし、平気な顔できなくなるよ",
    "ん……じんって来た。今の、ちょっと強かったかな",
    "あっ……声、出る……。聞こえても、知らないからね",
))
add_org("クリ・通常", (
    "ふふ、そこでほどけた……。転校生くん、上手になったね♪",
    "あ……腰がふるえた。もう一度、ゆっくり触ってみる？",
    "まだじんじんしてる……。甘いものより、こっちが残るなんてね",
), (
    "あっ……いった、みたい。腰が勝手に動くの、変な感じだね",
    "ん……じんじんする。ちょっとだけ、休ませてよ",
    "ふふ、効いたなぁ。……まあ、今日は合格にしてあげる",
))

add_org("バスト・最強", (
    "あっ……胸が熱い……っ、転校生くんの手、もう離さないで……",
    "ふぁ……乳首から全身まで震える……。こんなの、隠せないよ……っ",
    "いく……っ、胸だけでこんなに崩れるなんて……ぎゅってして……っ",
), (
    "う、うそ……胸が勝手に跳ねる……っ、見ないでよ……",
    "ひっ……先が熱い……。声、出ちゃうの、恥ずかしい……っ",
    "もうだめ……胸でいくなんて、わたし、知らなかった……っ",
))
add_org("バスト・強", (
    "ん……先が甘く痺れる……。ふふ、そんなに大事そうに触るんだね",
    "あっ、胸の奥まで響いた……転校生くん、少しだけゆっくりにして",
    "いきそう……っ、触れられるたび、身体が近づきたがる……♪",
), (
    "そこ、強くしないで……っ。胸だけ先に熱くなるよ",
    "ん……先がじんってする。今のは、ちょっと効いたかな",
    "あっ、もう少しで声が……。見ないで、でも手は止めないでよ",
))
add_org("バスト・通常", (
    "ふふ、胸でふるえた……。転校生くんに触られると、宝物みたいだね♪",
    "あ、熱い……。胸の先だけ、まだ君を覚えてる",
    "余韻が残ってるね。今日は、もう少し甘やかしてよ",
), (
    "あっ……いった、よ。胸でなんて、ちょっと意外だな",
    "ん……先がじんじんする。見られると余計に恥ずかしいよ",
    "ふふ、効いたね。……胸のこと、からかわないでよ？",
))

add_org("キス・最強", (
    "んむっ……ふぁ……唇から力が抜ける……っ。息ができなくても、離れたくない……",
    "ちゅ……っ、舌が触れるだけで、胸まで甘くなる……転校生くん、もう一度……っ",
    "いく……っ、キスだけでこんなになるの……。もっと、ぎゅってして……っ",
), (
    "うあっ……唇が痺れて、声がこぼれる……っ。こんなの、聞いてないよ……",
    "ちゅ……息が続かない……っ。でも、離れるって言えない……",
    "もうだめ……キスだけで、頭の中までほどけちゃう……っ",
))
add_org("キス・強", (
    "ちゅ……ん、いきそう……。転校生くんの唇、甘いね♪",
    "息がはずむ……舌が触れるたび、笑っていられなくなる",
    "んっ……もう少し深くして。今、離れたら寂しいから……♪",
), (
    "ちゅ……っ、急に深くしないで……。息が追いつかないよ",
    "ん……唇がじんじんする。今の、少し強かったかな",
    "あっ……声、出ちゃう。キスでこんなになるなんて、困ったなぁ",
))
add_org("キス・通常", (
    "ふふ、キスでふるえた……。転校生くん、癖になりそうだね♪",
    "ちゅ……ん、まだ唇が熱い。もう少し、このままでいよ",
    "息が戻らないね。……でも、嫌じゃないから困るなぁ",
), (
    "あっ……いった、よ。唇だけでなんて、変な感じだね",
    "ん……ちゅ。まだ痺れてる。急に離れないでよね",
    "ふふ、効いたよ。……キスの採点は、今日は内緒にしておくね",
))


SOFTEN = {
    "変態すぎるよ": "困ったひとだなぁ",
    "変態すぎ": "困ったひとすぎ",
    "変態だなぁ": "困ったひとだなぁ",
    "変態": "困ったひと",
    "無礼にもほどがあるよ": "そんなに驚かせないでよ",
    "反則だよ": "ずるいよ",
    "反則": "ずるい",
    "作法は身につけておきなさい": "少し落ち着いてよね",
    "作業台じゃないんだから": "そんなに器用じゃないんだから",
    "本気で怒るから": "ほんとに困っちゃうから",
    "怒るから": "困っちゃうから",
    "怒るよ": "困っちゃうよ",
    "覚悟してよね": "覚えておいてね",
    "禁止": "なし",
    "しなさい": "してね",
    "するな": "しないで",
    "おとなしく": "じっと",
    "逃げられない": "逃げ道がない",
    "えへへ": "ふふ",
    "だめぇ": "だめだよ",
}


def replace_print_line(lines: list[str], index: int, speech: str) -> None:
    old = lines[index]
    indent = old[: len(old) - len(old.lstrip())]
    ending = "\r\n" if old.endswith("\r\n") else "\n" if old.endswith("\n") else ""
    lines[index] = f'{indent}PRINTFORMW 「{speech}」{ending}'


def block_end(lines: list[str], start: int) -> int:
    depth = 0
    for i in range(start, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("IF "):
            depth += 1
        elif stripped == "ENDIF":
            depth -= 1
            if depth == 0:
                return i + 1
    raise RuntimeError(f"ENDIF not found at {start + 1}")


def rewrite_a12(
    lines: list[str],
    start: int,
    end: int,
    values: tuple[str, ...],
    a0_values: tuple[str, str] | None = None,
) -> None:
    if len(values) != 6:
        raise ValueError("rewrite_a12 needs lover3 + normal3")
    branch_lines = [
        i for i in range(start, end)
        if lines[i].startswith("\t\tELSEIF A == 1")
    ]
    else_lines = [
        i for i in range(start, end)
        if lines[i].startswith("\t\tELSE") and not lines[i].startswith("\t\tELSEIF")
    ]
    if len(branch_lines) != 2 or len(else_lines) != 2:
        raise RuntimeError(f"A=1/A=2 groups not found at {start + 1}: {branch_lines}, {else_lines}")
    zero_lines = [
        i for i in range(start, end)
        if lines[i].startswith("\t\tIF A == 0")
    ]
    if len(zero_lines) != 2:
        raise RuntimeError(f"A=0 groups not found at {start + 1}: {zero_lines}")
    if a0_values is not None:
        replace_print_line(lines, zero_lines[0] + 1, a0_values[0])
        replace_print_line(lines, zero_lines[1] + 1, a0_values[1])
    replace_print_line(lines, branch_lines[0] + 1, values[1])
    replace_print_line(lines, branch_lines[1] + 1, values[4])
    replace_print_line(lines, else_lines[0] + 1, values[2])
    replace_print_line(lines, else_lines[1] + 1, values[5])


def rewrite_additional10(lines: list[str]) -> int:
    marker = next(i for i, line in enumerate(lines) if MARKER in line)
    boundary = next(i for i in range(marker + 1, len(lines)) if lines[i].strip() == "RETURN 0")
    starts = [
        (i, int(m.group(1)))
        for i, line in enumerate(lines[marker:boundary], marker)
        if (m := re.match(r"^IF SELECTCOM == (\d+)$", line.rstrip("\r\n")))
    ]
    count = 0
    for pos, (start, command_id) in enumerate(starts):
        if command_id not in NEW_LINES:
            continue
        end = starts[pos + 1][0] if pos + 1 < len(starts) else boundary
        rewrite_a12(lines, start, end, NEW_LINES[command_id], NEW_A0[command_id])
        count += 1
    return count


def soften_legacy_rand3(lines: list[str]) -> int:
    start = next(i for i, line in enumerate(lines) if line.startswith(";--- COM0 "))
    end = next(i for i, line in enumerate(lines) if MARKER in line)
    branch = 0
    changed = 0
    for i in range(start, end):
        stripped = lines[i].strip()
        if lines[i].startswith("\t\tIF A == 0"):
            branch = 0
        elif lines[i].startswith("\t\tELSEIF A == 1"):
            branch = 1
        elif lines[i].startswith("\t\tELSE") and not lines[i].startswith("\t\tELSEIF"):
            branch = 2
        if branch not in (1, 2) or "PRINTFORM" not in lines[i]:
            continue
        old = lines[i]
        new = old
        for before, after in SOFTEN.items():
            new = new.replace(before, after)
        # The generated branches used a pause before nearly every clause. Keep
        # the hesitations that carry feeling, but remove sentence-punctuation pauses.
        new = new.replace("……。", "。").replace("……、", "、")
        if new != old:
            lines[i] = new
            changed += 1
    return changed


def rewrite_orgasm(lines: list[str]) -> int:
    start = next(i for i, line in enumerate(lines) if line.strip() == "@CHAR_ORGASM_49")
    seen: dict[str, int] = {}
    changed = 0
    for i in range(start + 1, len(lines)):
        label = lines[i].strip()
        if not (label.startswith(";恋人・") or label.startswith(";通常・")):
            continue
        key = re.sub(r"・[123]$", "", label[1:])
        if key not in ORG:
            continue
        index = seen.get(key, 0)
        if index >= 3:
            raise RuntimeError(f"too many orgasm branches for {key}")
        quote_index = i + 1
        while quote_index < len(lines) and "PRINTFORM" not in lines[quote_index]:
            quote_index += 1
        if quote_index >= len(lines):
            raise RuntimeError(f"speech missing after {label}")
        values = ORG[key]
        replace_print_line(lines, quote_index, values[index])
        seen[key] = index + 1
        changed += 1
    missing = sorted(set(ORG) - set(seen))
    incomplete = sorted(key for key, count in seen.items() if count != 3)
    if missing or incomplete:
        raise RuntimeError(f"orgasm map mismatch missing={missing} incomplete={incomplete}")
    return changed


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    legacy_changed = soften_legacy_rand3(lines)
    add_count = rewrite_additional10(lines)
    orgasm_count = rewrite_orgasm(lines)
    result = "".join(lines)
    direct_repairs = {
        "%LOCALS%、とろとろ。……こういう感じなんだ……勉強になるなぁ……": "%LOCALS%、もうそんな声……。ふふ、わたしが触れるたび、素直になっていくね♪",
        "ふーん、%LOCALS%のを、舐めるの……？　……れろ……。……ふふ、女の子の味、こんな感じなんだ……勉強になるなぁ": "ふーん、%LOCALS%のを、舐めるの……？　……れろ……。声、近いね。もう少し聞かせて♪",
        "それ、どう使うの？　わたしに任せるなら、ちゃんと手順を教えてよね": "その道具、先にわたしの手で触ってみるね。痛かったら、すぐ言ってよ",
        "作業みたいに見ないで。わたしも緊張してるんだから、ひと声かけてよ……っ": "そんな顔で見られると、わたしまで手元がふるえる……。もう少し近くにいてよ",
        "道具を使うと反応が分かりやすいなぁ。ふふ、観察してるだけでも楽しい": "道具が動くたび、顔まで変わるんだね。ふふ、もう少しそのまま見せて♪",
        "ゆっくり動かすと、声の変化がよく分かるね。わたし、こういう観察は得意なんだ": "%LOCALS%の声が近くでほどけていく……。聞いてると、わたしまで息が熱くなるね",
        "%LOCALS%に、クスコを……。……ふふ、奥まで、見えちゃうね……。……君も、いっしょに、観察する……？♪": "%LOCALS%の顔、赤いね……。わたしまで見ていられなくなりそう♪",
        "君の足でされると、身体まで勝手に反応しちゃう。ふふ、変な奉仕だね♪": "足の熱が触れるたび、身体が先に返事しちゃう……。ふふ、変な感じだね♪",
        "君のものをわたしと%CALLNAME:ASSI%で。二人の息が合うと、反応まで揃うんだね♪": "%CALLNAME:ASSI%と息が重なると、君の声まで近くなる……。ふふ、もう少し続けよっか♪",
        "ここまで見せるつもりじゃなかったのに……っ。採点するみたいに見ないでよね！": "ここまで見られるつもりじゃなかったのに……っ。そんな目で見られたら、隠すほうが難しいよ",
        "わたしの胸を比べてる？　採点は甘いものを食べてからにしてよね！": "胸ばかり見ないでよ……。そんなに見られると、こっちまで意識しちゃうじゃない",
    }
    for before, after in direct_repairs.items():
        count = result.count(before)
        normalized_after = after.replace("……。", "。").replace("……、", "、")
        after_count = result.count(after)
        normalized_count = result.count(normalized_after)
        if count == 1 and after_count == 0 and normalized_count == 0:
            result = result.replace(before, after)
        elif count == 0 and (after_count == 1 or normalized_count == 1):
            continue
        else:
            raise RuntimeError(
                f"direct repair expected one old or one new form: {before!r}, old={count}, new={after_count}, normalized={normalized_count}"
            )
    # These forms were introduced by the previous draft, not by the source
    # character. Remove them one expression at a time rather than changing
    # the character's whole voice by a global pronoun substitution.
    obvious = {
        "えへへ": "ふふ",
        "だめぇ": "だめだよ",
        "変態すぎるよ": "困ったひとだなぁ",
        "変態すぎ": "困ったひとだなぁ",
        "変態だなぁ": "困ったひとだね",
        "変態": "困ったひと",
    }
    for before, after in obvious.items():
        result = result.replace(before, after)
    if newline == "\r\n" and "\n" in result.replace("\r\n", ""):
        raise RuntimeError("bare LF introduced")
    encoded = result.encode("cp932")
    TARGET.write_bytes(encoded)
    print(f"legacy RAND3 A1/A2 softened lines: {legacy_changed}")
    print(f"additional10 blocks rewritten: {add_count}/10")
    print(f"orgasm branches rewritten: {orgasm_count}/150")
    print(f"bytes={len(encoded)} CRLF={encoded.count(bytes([13, 10]))}")


if __name__ == "__main__":
    main()
