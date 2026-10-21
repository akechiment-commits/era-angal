"""CHAR53 花丘まりのRAND:3化・追加10コマンド・絶頂口上改訂。"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"
BACKUP_PATH = ROOT / "tools/backups/CHAR53_before_rand3_additional10_orgasm_20260813/CHAR_53_花丘まり_COM.ERB"
MARKER = ";=== MARI RAND3 ADDITIONAL10 ORGASM REVISION START ==="


def q(love1: str, love2: str, normal1: str, normal2: str) -> tuple[str, ...]:
    return love1, love2, normal1, normal2


# 「説明」ではなく、触れられた瞬間の息・照れ・甘えを返すための短いプロファイル。
# love_focus / normal_focus は部位の実況ではなく、反応の足場として使う。
SIMPLE_PROFILES: dict[int, tuple[str, str, str, str]] = {
    4: ("口元", "口", "あんたの舌が触れる", "口で来る"),
    7: ("体温", "隣", "何もしないで寄り添う", "何もしないでいる"),
    8: ("奥", "そこ", "指が奥まで来る", "指で触る"),
    9: ("後ろ", "お尻", "舌が後ろに触れる", "そんなところを舐める"),
    10: ("身体の奥", "お腹", "振動が奥まで響く", "こんな機械を当てる"),
    18: ("肌", "背中", "湯気のなかで触れられる", "シャワーを当てる"),
    19: ("後ろ", "お尻", "ひとつずつ奥へ来る", "そこへ入れる"),
    26: ("お尻", "後ろ", "正面から抱かれる", "こんな格好で来る"),
    27: ("後ろ", "お尻", "背中から押される", "後ろから来る"),
    28: ("お尻", "そこ", "顔を見ながら後ろへ来る", "向き合ったまま触る"),
    29: ("背中", "お尻", "密着したまま後ろへ来る", "背中から抱く"),
    35: ("肌", "お尻", "泡越しに身体を重ねる", "泡まみれで擦る"),
    37: ("足先", "脚", "足で熱を分けてもらう", "足で扱く"),
    38: ("脚の間", "太もも", "太ももに挟まれる", "脚で挟む"),
    39: ("腰", "お尻", "そこへ押しつけられる", "お尻で挟む"),
    42: ("肌", "そこ", "針の刺激が重なる", "針を当てる"),
    43: ("目元", "目元", "目隠しをされる", "目隠しをされる"),
    45: ("喉", "口元", "口を塞がれる", "口を塞がれる"),
    46: ("お腹の奥", "お尻", "奥から押される", "そこへ器具を入れる"),
    53: ("身体", "お腹", "見られながら触れられる", "カメラを向ける"),
    54: ("肌", "外気", "人目のある場所で触れられる", "外で触る"),
    56: ("息", "肌", "外で抱かれる", "こんな場所で抱く"),
    57: ("視線", "身体", "見せながら可愛がる", "見られたまま触る"),
    58: ("肌", "身体", "湯気のなかで見つめられる", "風呂場で見る"),
    59: ("胸の奥", "肌", "新妻みたいに扱われる", "妻の真似をする"),
    61: ("舌", "口元", "舌で丁寧に触れられる", "そこを舐める"),
    63: ("息", "肌", "%LOCALS%と舌を重ねる", "%LOCALS%と触れあう"),
    65: ("腰", "脚", "%LOCALS%と一緒に抱かれる", "%LOCALS%と擦りあう"),
    66: ("口元", "口", "%LOCALS%と口を重ねる", "%LOCALS%と口で受ける"),
    67: ("舌", "口元", "二本を口で可愛がる", "両側から口を寄せる"),
    68: ("足先", "脚", "足で触れられる", "足を重ねる"),
    69: ("舌", "身体", "あんたと舌を絡める", "互いに舐めあう"),
    71: ("舌", "肌", "%LOCALS%と互いに舐める", "%LOCALS%と舐めあう"),
    75: ("耳元", "身体", "言葉で追いつめられる", "そんな言葉を聞かせる"),
    80: ("喉", "口", "喉の奥まで受け止める", "口の奥まで押しこむ"),
    85: ("喉", "身体", "苦しさまで受け止める", "急に力をかける"),
    90: ("後ろ", "お尻", "見られながら開かれる", "そこを触る"),
    110: ("指先", "後ろ", "あんたの後ろをほぐす", "そこをほぐす"),
    130: ("あんたの目元", "あんたの視界", "あんたに目隠しをする", "あんたに目隠しをする"),
    131: ("あんたの手首", "あんたの身体", "あんたの手首を縛る", "あんたを動けないようにする"),
    132: ("あんたの口元", "あんたの声", "あんたの口を塞ぐ", "あんたの口を塞いで縛る"),
    181: ("守りたい気持ち", "準備", "ちゃんと用意してくれる", "ちゃんと用意する"),
    182: ("手元", "身体", "ちゃんと守られながら触れる", "用意して触る"),
    183: ("口元", "手元", "こぼさず受け止める", "手元に残す"),
    184: ("口元", "手元", "%LOCALS%の熱を受け取る", "%LOCALS%のものを受け取る"),
    185: ("唇", "口元", "口移しで熱を分けあう", "口移しをする"),
    186: ("唇", "身体", "薬の苦さまで甘くなる", "薬を飲ませる"),
    187: ("胸の奥", "身体", "先のことまで考えて抱かれる", "薬を用意する"),
    196: ("後ろ", "お尻", "あんたの形を受け入れる", "そこへ入れる"),
    197: ("背中", "肌", "一緒に湯へ入る", "背中を流す"),
    198: ("腕", "足取り", "外を歩きながら寄り添う", "外を一緒に歩く"),
    199: ("胸の奥", "肌", "妻みたいに甘える", "嫁の真似をする"),
    200: ("胸", "胸元", "胸を重ねて抱きあう", "胸を押しつける"),
    201: ("指先", "手", "指を口で可愛がる", "指を口に入れる"),
    203: ("指先", "後ろ", "%LOCALS%を丁寧に診る", "%LOCALS%の後ろを診る"),
    204: ("後ろ", "お尻", "あんたを受け入れる", "そこへ入れさせる"),
    205: ("視線", "身体", "見せながら自分で乱れる", "自分で触るところを見せる"),
    160: ("舌", "肌", "%LOCALS%と舌を重ねる", "%LOCALS%と舐めあう"),
    189: ("口元", "口", "%LOCALS%と口を重ねる", "%LOCALS%と口で受ける"),
    188: ("身体", "腰", "%LOCALS%と互いに受け入れる", "%LOCALS%と重なる"),
    255: ("奥", "身体", "%LOCALS%と奥を重ねる", "%LOCALS%と深く重なる"),
    256: ("奥", "お腹", "奥の手前を押される", "そこを正確に押す"),
    257: ("肌", "足元", "剃られながら見つめられる", "刃を肌に当てる"),
    390: ("手", "気持ち", "遊びながら手をつなぐ", "ゲームを一緒にする"),
    11: ("身体の奥", "肌", "振動を抱えたまま甘える", "機械を当てる"),
    13: ("後ろ", "お尻", "後ろまで震えが届く", "そこへ振動を入れる"),
    14: ("そこ", "肌", "先をじらされる", "先へ当てる"),
    15: ("胸", "胸元", "胸をじらされる", "そこへ触れる"),
    16: ("胸の奥", "胸", "吸われるように揺さぶられる", "胸へ器具を当てる"),
}


SIMPLE_STYLES: tuple[tuple[str, str, str, str], ...] = (
    (
        "ん……{love_action}と、あんたの熱まで近くなるねぇ。声を出しても、もう知らないよ……♪",
        "ふふ……{love_focus}がじわじわ熱くなるねぇ。あんた、まだ手をゆるめちゃ嫌だよ……♪",
        "おやまぁ……{normal_action}とは、よく思いついたねぇ。あたしまで震えてるじゃないか……んっ♪",
        "あっ……{normal_focus}を狙うとは、なかなかやるねぇ。少し待っておくれ、息が追いつかないよ……♪",
    ),
    (
        "んっ……{love_action}と、あたしの声まで引き出すつもりかい？　ふふ、責任を取っておくれよ……♪",
        "{love_focus}に熱が集まってくるねぇ……。あんたのそばだと、強がる気にもなれないよ……♪",
        "お、おやまぁ……{normal_action}とは大胆だねぇ。こんなに力が抜けるとは思わなかったよ……♪",
        "やれやれ……{normal_focus}が正直になっちまうねぇ。もう少しだけ、加減しておくれ……♪",
    ),
    (
        "ふぅ……{love_action}と、息がつまるほど嬉しくなるねぇ。もう一度、ゆっくりおくれ……♪",
        "{love_focus}がくすぐったくて、笑っていられないよ……。あんたの手、好きだねぇ♪",
        "あらやだ……{normal_action}のかい？　まったく、意外なところを突いてくるねぇ……♪",
        "んっ……{normal_focus}に触れられると、言葉が途切れちまうよ。ふふ、困ったねぇ……♪",
    ),
    (
        "あ……{love_action}なんてされたら、あたしまで若返った気分だよ。もう少し、近くでおくれ……♪",
        "{love_focus}が熱を持ってきたねぇ……。甘えたいって顔に出ちまってるかい？♪",
        "おやまぁ、{normal_action}とはねぇ。あたしの反応を見て楽しんでるんだろう？……んっ♪",
        "{normal_focus}へ来るたび、声がひとつ遅れるねぇ。急がず、そのまま続けておくれ……♪",
    ),
    (
        "ん……{love_action}と、身体が先に返事しちまうねぇ。あんた、嬉しそうな顔をしてるよ♪",
        "ふふ、{love_focus}がほどけていくねぇ……。あたしをこんなに甘やかすの、あんただけだよ♪",
        "あっ……{normal_action}なんて、ずいぶん手慣れてるじゃないか。おやまぁ、声まで出たよ……♪",
        "{normal_focus}が跳ねるたび、強がりがひとつずつ消えるねぇ。少しゆるめておくれ……♪",
    ),
    (
        "{love_action}と、あたしもつられて息が揺れるねぇ……。そう、そこだよ♪",
        "{love_focus}に残る熱、消さないでおくれよ。まだあんたを感じていたいねぇ……♪",
        "おや、{normal_action}んだねぇ……。ふふ、あたしをからかうつもりかい？　そう簡単には隠せないよ♪",
        "{normal_focus}が敏感になってるねぇ。ほら、言葉より先に声が出ちまう……♪",
    ),
    (
        "ん、んっ……{love_action}とは、ずいぶん贅沢だねぇ。あたし、もう待てないよ……♪",
        "ふふ……{love_focus}があんたを覚えちまうねぇ。もっと近くにいておくれよ……♪",
        "あらまぁ……{normal_action}と来たかい。思わず身をよじっちまったよ……♪",
        "{normal_focus}まで熱が回るねぇ。ほんの少しだけ、ゆっくりにできるかい？♪",
    ),
    (
        "{love_action}と、息が甘くなるねぇ……。あたしのこと、ちゃんと見ておくれ♪",
        "{love_focus}がじんと疼くよ。あんたに触られると、もっと欲が出るねぇ……♪",
        "お、おやまぁ……{normal_action}のかい。ふふ、急にそんな顔をするなんてねぇ♪",
        "{normal_focus}に来ると、つい声を飲み込んじまうよ。……ん、まだ続けるんだねぇ♪",
    ),
)


def make_simple_variants(command: int, profile: tuple[str, str, str, str]) -> tuple[str, ...]:
    love_focus, normal_focus, love_action, normal_action = profile
    style = SIMPLE_STYLES[command % len(SIMPLE_STYLES)]
    return tuple(
        template.format(
            love_focus=love_focus,
            normal_focus=normal_focus,
            love_action=love_action,
            normal_action=normal_action,
        )
        for template in style
    )


SIMPLE_EXTRA = {command: make_simple_variants(command, profile) for command, profile in SIMPLE_PROFILES.items()}

# 日常寄りのコマンドは、汎用の刺激語を当てるとまりの「一緒にいる嬉しさ」が薄れるため個別化。
SIMPLE_EXTRA.update({
    7: q(
        "ん……何もしないで、あんたの隣にいるだけで落ち着くねぇ。もう少し、このままでいようよ♪",
        "ふふ……体温が近いと、胸の奥まであったかくなるねぇ。今日は甘えてもいいかい？♪",
        "おやまぁ、お茶の前にそんなに寄るのかい。……ま、今日はゆっくりしておくれ♪",
        "あっ……隣にいるだけで、妙に離れがたくなるねぇ。困ったもんだよ、ふふ♪",
    ),
    197: q(
        "ふふ、一緒にお風呂かい。肩まであったまると、あんたの手まで近くに感じるねぇ……♪",
        "あんたと湯気の中にいると、のぼせる前から頬が熱くなっちまうよ……。もう少しそばにおいで♪",
        "おや、背中を流してくれるのかい。そんなに丁寧にされたら、出るのが惜しくなるねぇ♪",
        "あっ……肩に触れる手があったかいねぇ。もう少しだけ、ここにいようじゃないか♪",
    ),
    198: q(
        "ふふ、お外でデートかい。手をつないで歩くと、足取りまで浮ついちまうねぇ♪",
        "いい風だねぇ……あんたの肩が隣にあるだけで、どこまでも歩けそうだよ♪",
        "おや、お散歩かい。そんなに急がず、あたしの歩幅に合わせておくれねぇ♪",
        "あっ……人目があるのに、そんな近くに来るのかい。ふふ、悪くないねぇ♪",
    ),
    390: q(
        "ふふ、ゲームセンターかい。あんたと一緒なら、若い子の遊びも悪くないねぇ♪",
        "あっ……その顔は本気だねぇ。じゃあ、あたしが景品を取るところを見ておくれ♪",
        "おや、クレーンゲームかい。なに、あたしに任せておきな。昔取った杵柄ってねぇ♪",
        "ふふ、勝負するのかい？　負けたほうが甘いものを買うってのはどうだい♪",
    ),
    43: q(
        "ん……目隠しをされると、あんたの気配ばかり近くなるねぇ。ちゃんとそばにいておくれよ♪",
        "見えないぶん、触れられるたびに身体が先に返事しちまうねぇ。ふふ、困ったねぇ……♪",
        "お、おやまぁ……目隠しをされるのかい。何をされるか分からないと、落ち着かないねぇ……♪",
        "見えないまま触られると、声を出す前に息が止まっちまうよ。優しくしておくれねぇ♪",
    ),
    45: q(
        "んーっ……口を塞がれると、声の代わりに身体が騒いじまうねぇ。あんた、よく見ておくれ♪",
        "喋れないまま甘やかされるのも、妙に恥ずかしくて悪くないねぇ……んっ♪",
        "お、おやまぁ……口枷をされるとはねぇ。こんな声しか出せないじゃないか……♪",
        "んーっ……外しておくれと言いたいのに、息しか漏れないねぇ。まったく、困ったもんだよ♪",
    ),
    130: q(
        "ん……見えないあいだ、あたしの声だけを頼りにしておくれ。ほら、どこに触れてるか分からないだろう？♪",
        "ふふ、目元を覆われて不安かい？　大丈夫、あたしがそばでたっぷり可愛がってあげるねぇ♪",
        "おやまぁ、見えないと手も出せないねぇ。あたしの言うことを、よく聞いておくれ♪",
        "動けないわけじゃないのに、目が隠れるだけで素直になるんだねぇ。かわいいもんだよ♪",
    ),
    131: q(
        "ふふ、手首を預けておくれ。あんたが逃げられないと、あたしも安心して可愛がれるねぇ♪",
        "ん……そのまま動けないでおくれ。あたしの手に、あんたを任せてもらうよ……♪",
        "おや、腕を出しな。護身術の縛り方、あんたで試してみようかねぇ♪",
        "あらまぁ、ずいぶんおとなしくなったねぇ。縛られたぶん、あたしの言うことを聞いておくれ♪",
    ),
    132: q(
        "ん……声の代わりに、目で返事をしておくれ。あんたの顔、よく見てるからねぇ♪",
        "喋れないあんたを、あたしが好きなだけ甘やかすんだよ。よしよし、じっとしておいで♪",
        "おや、口を開けておくれ。これでしばらく、減らず口は聞けないねぇ♪",
        "んーっ、って声しか出ないかい？　ふふ、あたしが外すまで、そのまま可愛がられておいで♪",
    ),
    181: q(
        "ふふ、ちゃんと準備してくれるんだねぇ。そういうところ、あんたらしくて好きだよ♪",
        "ん……あたしを大事にする気なら、遠慮なく甘えておくれ。ほら、ゆっくりでいいからねぇ♪",
        "おやまぁ、そこまで用意がいいとはねぇ。あたしを困らせる気はないんだろう？♪",
        "ふふ、ちゃんと守るつもりかい。感心だねぇ、じゃあ遠慮なく付きあってあげようかねぇ♪",
    ),
})


CUSTOM_EXTRA: dict[int, tuple[str, ...]] = {
    280: q(
        "ふふ、部員のいない部室で二人きりかい。ラケットより、あんたの手のほうが気になるねぇ……♪",
        "ん……声を落とすほど、近くにいるのが嬉しくなるねぇ。もう少し、そばにおいでよ……♪",
        "おやまぁ、こんなところで甘えるのかい。誰か来たら、あたしが叱っておくれよ？　ふふ♪",
        "部室で寄り添うなんて、困ったさんだねぇ。……でも、今は離れなくていいよ♪",
    ),
    281: q(
        "夜のコートで二人きりかい。冷えた手を、あたしのところで温めておくれよ……♪",
        "星より近くにあんたの顔があるねぇ。ふふ、ラリーより息が乱れるじゃないか……♪",
        "ナイターが消えたあとに残るのは、あんたの気配だけだねぇ。おやまぁ、静かだよ♪",
        "夜風に当たってると、妙に大胆になっちまうねぇ。帰る前に、少しだけ付きあっておくれよ♪",
    ),
    282: q(
        "誰もいない夜の家で、あんたと食卓を囲めるなんて……胸の奥が、やっとあったかいよ♪",
        "食事のあとも帰したくないねぇ。あたしの寂しさまで、あんたの体温でほどけちまうよ……♪",
        "おや、家まで来たのかい。ふふ、夕飯だけのつもりだったなら、少し困らせちまうねぇ♪",
        "独りの夜にあんたがいると、静かなのに落ち着かないねぇ……お茶でも飲んでいきなよ♪",
    ),
    283: q(
        "夕暮れの縁側で肩が触れると、虫の声まで遠くなるねぇ。あんた、こっちを向いておくれよ♪",
        "ふふ、涼むだけのはずが、手を離すほうが寂しくなっちまったねぇ……♪",
        "おやまぁ、ご近所に見つかったらお説教だよ。……だから、声は小さくしておくれねぇ♪",
        "縁側でそんな目をするのかい。まったく、年寄りをからかうのが上手だねぇ……♪",
    ),
    284: q(
        "星空の下であんたと並ぶと、胸の奥まで広くなるねぇ。今夜は帰りたくないよ……♪",
        "コートの端で手を重ねるだけなのに、試合よりどきどきするじゃないか……♪",
        "夜のコートで二人きりかい。汗の匂いはご愛敬だよ、ふふ、こっちへおいで♪",
        "こんな時間まで付きあわせちまったねぇ。……もう少しだけ、あたしの隣にいておくれよ♪",
    ),
    410: q(
        "紅葉を見ながら、あんたと一句かい。景色より、隣の顔に気を取られちまうねぇ♪",
        "ふふ、筆を持つ手が触れるたび、言葉より先に胸が騒ぐよ……♪",
        "吟行なんて渋い遊びに付きあうのかい。おやまぁ、あんたも物好きだねぇ♪",
        "一句ひねるより、あんたの返事を聞くほうが楽しみだねぇ。ゆっくり歩こうか♪",
    ),
    411: q(
        "落ち葉を踏む音と、あんたの息が重なるねぇ。秋ってのは人を甘くするよ……♪",
        "句を考えてるふりをして、あんたの指ばかり見ちまうねぇ……困ったもんだよ♪",
        "おや、そんな近くで季語を探すのかい。あたしの顔に書いてあるかねぇ？♪",
        "歩き疲れたなら、あたしの肩を使いなよ。ふふ、今日は特別に貸してあげる♪",
    ),
    412: q(
        "あんたと並んで詠むと、同じ紅葉でも別の色に見えるねぇ……♪",
        "声を聞きながら句を直すなんて、集中できないじゃないか。責任を取っておくれよ♪",
        "おやまぁ、あんたの句は素直だねぇ。あたしのことまで詠んでないだろうね？♪",
        "一休みしてお茶にしようか。あんたとなら、何杯でも付きあうよ♪",
    ),
    413: q(
        "甘いものを分けると、口元まで近くなるねぇ。ふふ、もう一口おくれよ……♪",
        "餡の甘さより、あんたの息のほうが残るなんてねぇ。年甲斐もなく欲張りだよ♪",
        "おや、あたしのぶんまで選んでくれたのかい。良い子だねぇ、飴ちゃんもあげよう♪",
        "甘いものを食べたら、少し歩こうか。あんまり見つめると、あたしが照れちまうよ♪",
    ),
    414: q(
        "夕暮れの句より、あんたの声のほうが胸に残るねぇ。もう少し聞かせておくれよ♪",
        "帰り道を急ぐのが惜しいよ。あたしの隣、もう少しだけ空けておいておくれ……♪",
        "おやまぁ、最後まで付きあってくれたのかい。今日は良い日になったねぇ♪",
        "日が落ちる前に帰らなくちゃねぇ。……でも、手はつないだままでいいよ♪",
    ),
}


ADDITIONAL10: dict[int, tuple[str, tuple[str, ...]]] = {
    60: ("助手にキスさせる", (
        "%LOCALS%の唇を借りるのかい？　ふふ、転校生くんに見られてると、あたしまで熱くなるねぇ……♪",
        "ちゅ……。%LOCALS%、もう少しだけ。あんたの目があると、妙に欲しくなるよ……♪",
        "あらまぁ、二人ぶん甘やかすつもりかい。よしよし、順番に可愛がっておくれねぇ♪",
        "おや、%LOCALS%にキスをさせるのかい。あんたも一緒に、ちゃんと見ておくれよ♪",
        "ん……。女の子同士の口づけを見てるのかい？　そんな顔をされると、からかいたくなるねぇ♪",
        "ふふ、見てるだけで済むと思ったのかい。あんたにも、あとで甘いご褒美をあげようねぇ♪",
    )),
    62: ("ダブル素股", (
        "%LOCALS%とあんたの熱が両側から来るねぇ……。あたし、どちらを見ればいいのかねぇ♪",
        "んっ……腰が勝手に逃げるのに、離れたくはないんだよ。困った身体だねぇ……♪",
        "ふふ、二人がかりで甘えるのかい。あたしを挟んで、仲良くしておくれよ♪",
        "お、おやまぁ……脚の間がいっぱいだねぇ。急がず、息を合わせておくれよ……♪",
        "%LOCALS%も、あんたも、そんな顔をするんじゃないよ。こっちまで声が出ちまうじゃないか♪",
        "やれやれ、逃げ道がないねぇ。……ま、今日はあたしも退くつもりはないけどさ♪",
    )),
    76: ("双頭バイブ", (
        "%LOCALS%が動くたび、つないだバイブの震えがあたしの奥まで返ってくるねぇ……。変な感じだよ♪",
        "んっ……動くなら、ゆっくりおくれ。あんたの揺れが、そのままあたしの中に来るんだから……♪",
        "ふふ、一本のバイブでつながってると、逃げることもできないねぇ。あんたと同じ波を、もっと感じていたいよ……♪",
        "ひゃっ……%LOCALS%の動きが、そのままこっちへ届くじゃないか。急に変えないでおくれ……♪",
        "あっ……つないだところが擦れるたび、奥までびりっと来るねぇ。息を合わせて、もう少し続けようか♪",
        "止まると、まだ中に残った震えが惜しくなるねぇ。離れられないまま、ゆっくり動いておくれよ……♪",
    )),
    78: ("母乳飲み", (
        "ん……そんなに夢中で飲まれると、胸の奥までくすぐったいねぇ。もっと甘えておくれよ♪",
        "あっ……音まで近いねぇ。舌が触れるたび、あたしの喉まで鳴りそうだよ……♪",
        "ふふ、まだ欲しいのかい？　そんな顔をされたら、あたしのほうが離せなくなるねぇ♪",
        "おやまぁ、本当に口をつけるのかい。……まったく、甘えん坊さんだねぇ♪",
        "んっ……顔を上げなくていいよ。夢中な顔、もう少し近くで見せておくれ♪",
        "離れたあとも胸が熱いねぇ。もう一度ほしい顔をしてるじゃないか、困った子だよ♪",
    )),
    79: ("乳搾り", (
        "んっ……絞られるたび、胸の奥まできゅっとなるねぇ。あんたの手、ずるいよ……♪",
        "あっ……そこは強いねぇ。ふふ、手つきまで覚えちまったのかい？♪",
        "あんまり丁寧にされると、あたしまで可愛がられてる気分だよ。もう少し、おくれ♪",
        "おやまぁ、そんなふうに確かめるのかい。恥ずかしいけど、手は止めないでおくれよ……♪",
        "量なんか数えなくていいよ。あたしの顔を見て、ゆっくり続けなねぇ♪",
        "こぼしたら、ちゃんと片づけるんだよ？　……ふふ、そんなに慌てなくてもいいさ♪",
    )),
    84: ("Gスポット刺激", (
        "そこ……っ、あっ、声が先に出ちまうねぇ。あんた、そんなところを覚えたのかい……♪",
        "ん、ぁ……奥で跳ねるたび、余裕がほどけるよ。見ないでおくれ、でも止めないで……♪",
        "ふふ、そこを探すのかい。あたしの弱いところ、見つけた顔をしてるねぇ♪",
        "あっ……待っておくれ、そこは効くねぇ。少しだけゆっくり、そうそう……♪",
        "もう、手つきが迷わないじゃないか。あたしまで教えた甲斐があるねぇ……んっ♪",
        "やれやれ、声が隠せないよ。困ったさんだねぇ、責任を取っておくれ♪",
    )),
    86: ("強制放尿", (
        "やだよぉ……っ、こんなところで、あたしまで止められないなんて……。そばにいておくれ……♪",
        "あ、あんたの前で……っ。恥ずかしいのに、身体が言うことを聞かないねぇ……♪",
        "おやまぁ、急にそんなことをするのかい。笑うんじゃないよ、あたしだって困ってるんだからねぇ♪",
        "やれやれ……見ないでおくれよ。でも、そばにはいておくれねぇ……♪",
        "あたしの失敗を面白がるんじゃないよ。……まったく、顔が熱くてたまらないねぇ♪",
        "止まらないじゃないか……。困ったねぇ、終わるまで手を握っておくれよ♪",
    )),
    202: ("乳首合わせ", (
        "%CALLNAME:ASSI%さんの熱が重なると、胸の奥まで息が揃うねぇ……♪",
        "ん……擦れるたびに、あたしまでつられて震えちまうよ。見られると余計に恥ずかしいねぇ♪",
        "%CALLNAME:ASSI%さんと一緒かい。ふふ、女の子同士で甘えるのも悪くないねぇ♪",
        "おやまぁ、胸を重ねるのかい。二人ぶんの体温で、あたしまでぼうっとするよ……♪",
        "そんなに急がないでおくれ。呼吸を合わせると、もっと気持ちよくなるからねぇ♪",
        "ふふ、あんたは見てるだけかい？　その顔なら、あとでたっぷり可愛がってあげようねぇ♪",
    )),
    258: ("助手顔面騎乗", (
        "%CALLNAME:ASSI%さんが顔の上で、あたしはあんたの上かい……。息が足りないねぇ、でも離れたくないよ♪",
        "ん……腰と%CALLNAME:ASSI%さんの熱が同時に来るねぇ。あたしを二の次にしちゃ嫌だよ……♪",
        "三人で甘えるのかい。ふふ、あたしを真ん中にして、最後まで支えておくれよ♪",
        "お、おやまぁ……上も下も欲張りだねぇ。あたしの顔を潰さないように頼むよ……♪",
        "%CALLNAME:ASSI%さんの重みと、あんたの腰が一緒に来ると……声、隠せないねぇ♪",
        "やれやれ、忙しいったらないよ。けど、誰も離れちゃ駄目だからねぇ……♪",
    )),
    318: ("頭を撫でてもらう", (
        "……ん。あんたの手、妙に落ち着くねぇ。今だけは、何も言わずにそばにいておくれよ♪",
        "ふふ……撫でられるの、子供みたいで嫌なのに。もう少し続けてほしいねぇ……♪",
        "頭を撫でるのかい？　慰めるつもりなら、余計なことは言わずにやっておくれよ♪",
        "まったく、急に優しくするんじゃないよ。……でも、手は止めないでおくれねぇ♪",
        "よしよしされるのは、あんたのほうじゃないかい？　ふふ、今日はあたしが甘えるよ♪",
        "あぁ……そこ、気持ちいいねぇ。あたしを眠らせる気かい、困った子だよ♪",
    )),
}


ITEM_REMOVE_EXTRA: dict[int, tuple[str, ...]] = {
    11: (
        "ふぅ……抜けても、まだ奥がびりびりしてるねぇ。あんた、名残惜しい顔をしてるよ♪",
        "ん……急に静かになると、身体だけが続きを待っちまうねぇ。少し抱いておくれ♪",
        "あぁ、外したのかい？　ふふ、震えが消えるまで、あんたの手を貸しておくれねぇ♪",
        "おやまぁ、もう外すのかい。まだ身体が勝手に揺れてるじゃないか……♪",
        "ふぅ……静かになったと思ったら、胸までどきどきしてるねぇ。困ったもんだよ♪",
        "やれやれ、店じまいかい？　あたしの足元がふらつくぶん、ちゃんと支えておくれよ♪",
    ),
    13: (
        "ん……抜けたあとも、後ろが熱を抱えてるねぇ。あんたの手でゆっくり落ち着かせておくれ♪",
        "ふふ、まだじんじんしてるよ。あたしをこんなに甘やかした責任、最後まで見ておくれねぇ♪",
        "あぁ……外したのに、身体がまだ覚えてるねぇ。もう少し、そばにいておくれよ♪",
        "おや、もう取るのかい？　後ろが変な感じで、歩けるかどうかわからないよ……♪",
        "ふぅ……あたしの顔を見るんじゃないよ。まだ熱が引かなくて、うまく笑えないんだからねぇ♪",
        "やれやれ、ずいぶん大胆な置き土産だねぇ。次はもう少し、優しくしておくれよ♪",
    ),
    14: (
        "ふぅ……外れても、先がきゅっと残ってるねぇ。あんた、もう一度触れたくなってるかい？♪",
        "んっ……急に楽になると、かえって物足りないよ。もう少しだけ、指を置いておくれ……♪",
        "あぁ、取ったのかい？　ふふ、あたしの弱いところを散々覚えさせたねぇ♪",
        "おやまぁ、外すのが遅いじゃないか。まだそこが跳ねて、変な声が出そうだよ……♪",
        "ふぅ……先がじんじんしてるねぇ。笑ってごまかすには、ちょいと効きすぎたよ♪",
        "やれやれ、これで終わりかい？　余韻くらいは、ゆっくり味わわせておくれねぇ♪",
    ),
    15: (
        "ん……胸から離れても、まだあんたの手の形が残ってるねぇ。ふふ、名残惜しいよ♪",
        "あぁ……外したとたん、乳首がさびしがってるじゃないか。もう少し撫でておくれよ♪",
        "ふぅ、あたしの胸をこんなに熱くしておいて、先に終わるのかい？　困った人だねぇ♪",
        "おやまぁ、もう取るのかい。胸の奥まで響いたぶん、ちゃんと顔を見ていておくれ♪",
        "んっ……まだ服を戻す気にはなれないねぇ。そこだけ、あんたの熱が残ってるよ♪",
        "やれやれ、ずいぶん可愛がってくれたじゃないか。次はもう少し、ゆっくり頼むよ♪",
    ),
    16: (
        "ふぅ……吸われたあとの胸が、まだ勝手にきゅっとなるねぇ。あんたの手で落ち着かせておくれ♪",
        "ん……外しても、熱がぽたぽた残ってるみたいだよ。見ないでおくれ、でも離れないでねぇ♪",
        "あぁ、もう終わりかい？　胸の奥まで甘く疲れちまったよ。よしよししておくれ♪",
        "おやまぁ、取ったとたんに息が抜けたねぇ。こんな顔にさせて、責任を取っておくれよ♪",
        "ふぅ……まだ張った感じが消えないねぇ。あたしを笑うんじゃないよ、手を貸しておくれ♪",
        "やれやれ、外したのに胸が覚えてるじゃないか。あんた、ずいぶん上手に残していったねぇ♪",
    ),
    17: (
        "ふぅ……抜けたところが、まだあんたの形を覚えてるねぇ。少し、抱いていておくれよ♪",
        "ん……急に空くと、身体が戸惑っちまうねぇ。ふふ、もう一度なんて言わないよ……たぶんね♪",
        "あぁ、外したのかい？　ここまで乱されると、あたしも強がれないねぇ。そばにいておくれ♪",
        "おやまぁ、もう抜くのかい。まだ腰が勝手に追いかけてるじゃないか……♪",
        "ふぅ……あんたの好きにされたあとだと、静かなのが妙に寂しいねぇ。困ったもんだよ♪",
        "やれやれ、骨抜きにしておいて店じまいかい？　帰る前に、ちゃんとよしよししておくれねぇ♪",
    ),
}


def find_selectcom(lines: list[str], command: int) -> int:
    pattern = re.compile(rf"^(?:IF|ELSEIF) SELECTCOM == {command}$")
    for index, line in enumerate(lines):
        if pattern.match(line):
            return index
    raise ValueError(f"SELECTCOM {command} が見つかりません")


def find_matching_endif(lines: list[str], start: int) -> int:
    depth = 0
    for index in range(start, len(lines)):
        stripped = lines[index].lstrip()
        if re.match(r"IF\b", stripped):
            depth += 1
        elif re.match(r"ENDIF\b", stripped):
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"IF {start + 1} のENDIFが見つかりません")


def wrap_print(lines: list[str], print_index: int, extra1: str, extra2: str) -> None:
    original = lines[print_index]
    base_indent = original[: len(original) - len(original.lstrip())]
    if not original.lstrip().startswith("PRINTFORM"):
        raise ValueError(f"PRINTFORMではありません: {print_index + 1}")
    print_indent = base_indent + "\t"
    lines[print_index : print_index + 1] = [
        f"{base_indent}IF A == 0",
        f"{print_indent}{original.lstrip()}",
        f"{base_indent}ELSEIF A == 1",
        f'{print_indent}PRINTFORMW 「{extra1}」',
        f"{base_indent}ELSE",
        f'{print_indent}PRINTFORMW 「{extra2}」',
        f"{base_indent}ENDIF",
    ]


def wrap_talent_branches(lines: list[str], start: int, end: int, variants: tuple[str, ...]) -> None:
    talent_index = next((i for i in range(start, end) if re.match(r"^\s*IF TALENT:TARGET:153$", lines[i])), None)
    if talent_index is None:
        raise ValueError(f"SELECTCOM {start + 1} に恋人分岐がありません")
    talent_indent = lines[talent_index][: len(lines[talent_index]) - len(lines[talent_index].lstrip())]
    else_index = next((i for i in range(talent_index + 1, end) if lines[i] == f"{talent_indent}ELSE"), None)
    if else_index is None:
        raise ValueError(f"SELECTCOM {start + 1} の恋人/通常ELSEがありません")
    end_talent = next((i for i in range(else_index + 1, end) if lines[i] == f"{talent_indent}ENDIF"), None)
    if end_talent is None:
        raise ValueError(f"SELECTCOM {start + 1} のTALENT終端がありません")
    love_prints = [i for i in range(talent_index + 1, else_index) if "PRINTFORM" in lines[i]]
    normal_prints = [i for i in range(else_index + 1, end_talent) if "PRINTFORM" in lines[i]]
    if len(love_prints) != 1 or len(normal_prints) != 1:
        raise ValueError(f"SELECTCOM {start + 1} のPRINTFORM数が想定外です: {love_prints}/{normal_prints}")
    wrap_print(lines, normal_prints[0], variants[2], variants[3])
    wrap_print(lines, love_prints[0], variants[0], variants[1])


def add_rand3_to_simple(lines: list[str], command: int, variants: tuple[str, ...]) -> None:
    start = find_selectcom(lines, command)
    end = find_matching_endif(lines, start)
    block = lines[start : end + 1]
    if any("RAND:" in line for line in block):
        raise ValueError(f"SELECTCOM {command} はすでにRAND済みです")
    lines.insert(start + 1, "\tA = RAND:3")
    wrap_talent_branches(lines, start, end + 1, variants)


def add_rand3_to_custom(lines: list[str], command: int, variants: tuple[str, ...]) -> None:
    start = find_selectcom(lines, command)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^ELSEIF SELECTCOM == \d+$", lines[i]) or lines[i] == "ENDIF":
            end = i
            break
    if "RAND:" in lines[start : end + 1]:
        raise ValueError(f"独自SELECTCOM {command} はすでにRAND済みです")
    lines.insert(start + 1, "\tA = RAND:3")
    wrap_talent_branches(lines, start, end + 1, variants)


def find_matching_else(lines: list[str], start: int, end: int) -> int:
    depth = 0
    for index in range(start, end):
        stripped = lines[index].strip()
        if re.match(r"IF\b", stripped):
            depth += 1
        elif stripped == "ELSE" and depth == 1:
            return index
        elif stripped == "ENDIF":
            depth -= 1
    raise ValueError(f"IF {start + 1} の対応するELSEが見つかりません")


def add_rand3_to_item_removal(lines: list[str], command: int, variants: tuple[str, ...]) -> None:
    start = find_selectcom(lines, command)
    end = find_matching_endif(lines, start)
    equip_index = next(
        (i for i in range(start + 1, end) if lines[i].strip() == f"IF TEQUIP:{command}"),
        None,
    )
    if equip_index is None:
        raise ValueError(f"SELECTCOM {command} のTEQUIP分岐が見つかりません")
    remove_else = find_matching_else(lines, equip_index, end)
    equip_indent = lines[equip_index][: len(lines[equip_index]) - len(lines[equip_index].lstrip())]
    if any("A = RAND:3" in line for line in lines[remove_else + 1 : end]):
        raise ValueError(f"SELECTCOM {command} の取り外し側はすでにRAND済みです")
    lines.insert(remove_else + 1, f"{equip_indent}A = RAND:3")
    wrap_talent_branches(lines, remove_else + 2, end + 2, variants)


def additional_block(command: int, label: str, variants: tuple[str, ...]) -> list[str]:
    return [
        f";--- COM{command} {label}（追加10コマンド） ---",
        f"IF SELECTCOM == {command}",
        "\tA = RAND:3",
        "\tIF TALENT:TARGET:85",
        "\t\t;恋慕",
        "\t\tIF A == 0",
        f'\t\t\tPRINTFORMW 「{variants[0]}」',
        "\t\tELSEIF A == 1",
        f'\t\t\tPRINTFORMW 「{variants[1]}」',
        "\t\tELSE",
        f'\t\t\tPRINTFORMW 「{variants[2]}」',
        "\t\tENDIF",
        "\tELSE",
        "\t\t;非恋慕",
        "\t\tIF A == 0",
        f'\t\t\tPRINTFORMW 「{variants[3]}」',
        "\t\tELSEIF A == 1",
        f'\t\t\tPRINTFORMW 「{variants[4]}」',
        "\t\tELSE",
        f'\t\t\tPRINTFORMW 「{variants[5]}」',
        "\t\tENDIF",
        "\tENDIF",
        "ENDIF",
        "",
    ]


def revise_orgasm(lines: list[str]) -> int:
    start = next(i for i, line in enumerate(lines) if line.strip() == "@CHAR_ORGASM_53")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "RETURN 0")
    zone = "five"
    slot = 0
    revised = 0
    focus = {
        "five": ("身体じゅう", "いろんなところ", "身体じゅう"),
        "multi": ("あちこち", "いろんなところ", "身体じゅう"),
        "V": ("奥", "中", "あたしの奥"),
        "A": ("後ろ", "お尻", "そこ"),
        "C": ("そこ", "先っぽ", "触れられたところ"),
        "B": ("胸", "乳首", "そこ"),
        "M": ("唇", "唇", "口元"),
    }

    def make_text(tier: str, love: bool, part: str, index: int) -> str:
        a, b, c = focus[part]
        if tier == "max":
            if love:
                values = (
                    f"あ、あんたぁ……っ。{a}、だめ、いっぺんに来たら……わたし、ほどける……っ。ぎゅってしておくれよぉ……♪",
                    f"やだよぉ……頭が真っ白だねぇ……。{b}まで、あんたの熱でいっぱいで、もう、ひとりじゃいられないよぉ……♪",
                    f"ん、んんっ……！　{c}、もう限界だよぉ……。お願い、離れないでおくれ……あたし、甘えたいんだよぉ……♪",
                )
            else:
                values = (
                    f"お、おやまぁ……っ。{a}まで一緒に来るなんて聞いてないよぉ……。立ってられないから、支えておくれ……♪",
                    f"あ、あれぇ……？　{b}が勝手に跳ねて……。こんな声、止められないよぉ……っ♪",
                    f"やだねぇ……っ。{c}まで、そんなに……。あたし、もう笑ってごまかせないよぉ……♪",
                )
        elif tier == "strong":
            if love:
                values = (
                    f"んっ……{a}、いいねぇ……。じんじんして、あんたの手を離したくないよ……♪",
                    f"ふぅ……だめだねぇ、年甲斐もなく……。{b}に触れられるたび、もっと欲しくなっちまうよ……♪",
                    f"あっ……そんな顔で見ないでおくれよ。{c}、まだ震えてるんだから……ふふ、責任を取っておくれ♪",
                )
            else:
                values = (
                    f"おやまぁ……っ。{a}まで響くんだねぇ……。ちょいと、ゆっくりにしておくれ……♪",
                    f"あっ、待っておくれ……。{b}に響くと、声が隠せないねぇ……っ♪",
                    f"やれやれ……。{c}が熱くて、余裕がなくなっちまうよ……。もう少しだけ、付きあっておくれ……♪",
                )
        else:
            if love:
                values = (
                    f"……ん。ふふ、{a}の余韻が残ってるねぇ。あんたのそばだと、安心して力が抜けるよ……♪",
                    f"まだ震えてるねぇ……。{b}を、もう少しだけ味わっていたいよ……♪",
                    f"あぁ……{c}がまだ満たされてるねぇ。あんた、よしよししておくれよ……♪",
                )
            else:
                values = (
                    f"ふぅ……今の、効いたねぇ。{a}がまだ熱いよ、あんた、なかなかやるじゃないか……♪",
                    f"やれやれ……声が出ちまったねぇ。{b}がまだじんじんしてるよ、ふふ♪",
                    f"あぁ……{a}までふわっと力が抜けちまったよ。ちょいと休ませておくれ……♪",
                )
        return values[index]

    for i in range(start + 1, end):
        stripped = lines[i].strip()
        if stripped == "IF A == 0":
            slot = 0
        elif stripped == "ELSEIF A == 1":
            slot = 1
        if stripped.startswith(";--- 複絶頂"):
            zone = "multi"
        elif stripped.startswith(";--- 単絶頂"):
            zone = "C"
        elif stripped.startswith(";--- V"):
            zone = "V"
        elif stripped.startswith(";--- A"):
            zone = "A"
        elif stripped.startswith(";--- C"):
            zone = "C"
        elif stripped.startswith(";--- B"):
            zone = "B"
        elif stripped.startswith(";--- M"):
            zone = "M"
        if "PRINTFORMW 「" not in lines[i]:
            continue
        comment = ""
        for j in range(i - 1, max(start, i - 8), -1):
            if lines[j].lstrip().startswith(";"):
                comment = lines[j].strip()
                break
        if not comment.startswith((";恋人", ";通常")):
            continue
        if "最強" in comment:
            tier = "max"
        elif "・強・" in comment:
            tier = "strong"
        else:
            tier = "normal"
        love = comment.startswith(";恋人")
        indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
        lines[i] = f'{indent}PRINTFORMW 「{make_text(tier, love, zone, slot)}」'
        slot = min(slot + 1, 2)
        revised += 1
    return revised


def main() -> None:
    if not BACKUP_PATH.exists():
        raise FileNotFoundError(BACKUP_PATH)
    original = BACKUP_PATH.read_bytes().decode("cp932")
    lines = original.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if MARKER in original:
        raise RuntimeError("既に生成済みです。バックアップからERBを復元して再実行してください")

    revised = revise_orgasm(lines)
    for command, variants in SIMPLE_EXTRA.items():
        add_rand3_to_simple(lines, command, variants)
    for command, variants in CUSTOM_EXTRA.items():
        add_rand3_to_custom(lines, command, variants)
    for command, variants in ITEM_REMOVE_EXTRA.items():
        add_rand3_to_item_removal(lines, command, variants)

    insert_at = next((i for i, line in enumerate(lines) if line.startswith("@TRAIN_MESSAGE_B280_53")), len(lines))
    extra = [MARKER, "; 追加10コマンド：まりの保護者の余裕、甘えたい本音、年甲斐のない揺れを各3分岐", ""]
    for command, (label, variants) in ADDITIONAL10.items():
        extra.extend(additional_block(command, label, variants))
    lines[insert_at:insert_at] = extra

    output = "\r\n".join(lines)
    if not output.endswith("\r\n"):
        output += "\r\n"
    COM_PATH.write_bytes(output.encode("cp932"))
    print(
        f"CHAR53: 絶頂口上{revised}件を反応中心に改訂、通常口上RAND:3化{len(SIMPLE_EXTRA) + len(CUSTOM_EXTRA)}枠、"
        f"追加10コマンド、道具取り外しRAND:3化{len(ITEM_REMOVE_EXTRA)}枠を実装しました。"
    )


if __name__ == "__main__":
    main()
