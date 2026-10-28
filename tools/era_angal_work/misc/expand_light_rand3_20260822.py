from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCKS = {
    "ERB/CHAR/CHAR_31_夢路まりあ_COM.ERB": (
        ";--- COM17 オナホール ---",
        'IF SELECTCOM == 17',
        '''IF SELECTCOM == 17
\tIF TEQUIP:17
\t\t;装着（トグル後なので TEQUIPオン＝今装着した）
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ん、ぁっ、わ、わたくし、はしたなく……。主よ、お赦しを……けれど、止められないのです……っ♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あ、んっ……転校生さん、そんなに優しくされたら……わたくし、もっとと願ってしまいます……主よ♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ふぁ……身体の奥まで熱が広がって……転校生さん、わたくしの手を、離さないでくださいませ……♪」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ひっ! な、何ですかこれ……! は、腰が、はしたなくうねって……い、いけません、こんな……っ!?」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「ひゃっ……こ、これは、わたくしの身体が勝手に……はわわ、どうか笑わないでくださいませ……！」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あ、ぁ……こんなに熱くなるなんて……主よ、わたくし、どうして止められないのでしょう……」
\t\t\tENDIF
\t\tENDIF
\tELSE
\t\t;取り外し
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ふぁ……わたくし、まだ、火照って……。あぁ、あなたは、わたくしを堕落させる御方……でも、嫌いには、なれません」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「ふぅ……外れても、熱だけは残るのですね。転校生さん、もう少しだけ抱きしめていてくださいませ……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あぁ……まだ身体が覚えております。主よ、こんな余韻まで愛おしいと思うわたくしを、お赦しくださいませ……」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ぬ、もう、限界でございます……! このような淫らな器具で、聖女を堕とすなんて……あなたという御方は、ほんとうに、罪深い」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あ……外れたのに、まだ胸がどきどきしております。こ、これ以上は、心の準備が追いつきません……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ふぅ……お、お手伝いはいたしますけれど、どうか今は、わたくしの顔をあまりご覧にならないでくださいませ……」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    ),
    "ERB/CHAR/CHAR_57_岩戸サン_COM.ERB": (
        ";--- COM17 オナホール ---",
        'IF SELECTCOM == 17',
        '''IF SELECTCOM == 17
\tIF TEQUIP:17
\t\t;装着（トグル後なので TEQUIPオン＝今装着した）
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「んっ……あ……きみのてで、あたしのここも……ん……なんだか、ふわふわ、する……いいよ、そのまま……♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「……きみの手で、呼吸までゆっくりになるね。もう少しだけ、このままで……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あ……声、出てた？　きみがいると、静かにしてるのも難しいね……」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「わ……っ、しごかれて……こ、こしが、かってに……ん……とめられないよ……あたしの、いしと、かんけいなく……？」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「……あ、だめ。力が抜けてく……きみ、急がなくていいから……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ん……熱いね。こんなふうになるとは、思ってなかった……きみ、見てるの……？」
\t\t\tENDIF
\t\tENDIF
\tELSE
\t\t;取り外し
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ふ……ぞくって、きちゃった……きみに、ここまで、ほぐされちゃうなんて……あたし、かなわないなぁ……♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「……離れたあとも、熱が残ってる。きみのそばにいると、静かなままでも満たされるね……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ふぅ……あたし、まだ動きたくないかも。きみの気配が、近くにあるから……」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ふぅ……すごいなぁ、きみ……あたしのこと、こんなにも……ん、きみとは、いい、はしり仲間に、なれそう……♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「……終わったのに、身体がまだ覚えてる。あたし、しばらく動けないかも……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あ……まだ、ふわふわするね。きみ、こういうときは、そっとしておくもの……？」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    ),
    "ERB/CHAR/CHAR_58_天宮るり_COM.ERB": (
        ";--- COM17 オナホール ---",
        'IF SELECTCOM == 17',
        '''IF SELECTCOM == 17
\tIF TEQUIP:17
\t\t;装着（トグル後なので TEQUIPオン＝今装着した）
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ん、あ！ るるる♪ あなたの手で、るりのこれも、見知らぬ快が、駆け巡ります、いい、もっと♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あ、っ……あなたの手、熱いです。知らない星を見つけたみたいに、身体が揺れています……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ふふ……これは、観測を続けるべき反応ですね。あなた、もう少し近くにいてください☆」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ぬ、扱かれて！ こ、腰が、勝手に、律動を！ 制御、不能、るりの、意志を超えた、うねりが☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「ひゃっ……！　いまの、声に出てしまいました？　笑わないでくださいね、転校生のひと……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あ……思考より先に、身体が答えてしまいます。これは、少し困った現象ですね☆」
\t\t\tENDIF
\t\tENDIF
\tELSE
\t\t;取り外し
\t\tIF TALENT:TARGET:153
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ふ、ぞくり、と、痺れました。あなたに、ここまで、導かれるとは。るり、まだ、修練が、足りませんね♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「ふぅ……離れたあとも、身体がまだ覚えています。あなた、もう一度だけ抱いてくれますか……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あ……終わったのに、熱が消えません。るるる……これは、少し長い余韻ですね☆」
\t\t\tENDIF
\t\tELSE
\t\t\tA = RAND:3
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「ふぅ、大した、腕前です。るりを、ここまで、揺さぶるとは。あなたとは、良い、探究仲間に、なれそうです☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あ……離れたのに、まだ揺れています。転校生のひと、これは、どういう現象でしょう……？」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「ふふ……観測終了。ですが、記録はまだ続いています。るり、忘れませんから☆」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    ),
    "ERB/CHAR/CHAR_71_棗ひびき_COM.ERB": (
        ";--- COM200 乳の揉み合い ---",
        'IF SELECTCOM == 200',
        '''IF SELECTCOM == 200
\t;  ▼【視点】キャラ攻め/相互＝乳同士を擦り合わせる女性同士。相手は助手/他女子（女性同士の行為）
\t;  ▼ 女性同士が乳を揉み合うプレイ
\t;  ※相手は助手か他の女子（女性同士の行為）
\tIF TALENT:TARGET:153
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「ん、お互いの胸を……っ。ふふ、揉み合うの、面白いっちね♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「%LOCALS%の胸、やわらかいっちね。うちも負けないように、ぎゅっとするっち♪」
\t\tELSE
\t\t\tPRINTFORMW 「うひゃ……っ、こうしてくっつくと、笑ってる場合じゃなくなるっち。%LOCALS%、もう少しだけ……いいっちか？」
\t\tENDIF
\tELSE
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「ん、揉み合いっちか。あはは、相手のおっぱい、けっこう柔らかいっちね♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……%LOCALS%の胸が触れるたび、うちの息まで変になるっち。これ、思ったより近いっちね……」
\t\tELSE
\t\t\tPRINTFORMW 「ふふ、手も胸もどこに置くか迷うっち。%LOCALS%、ゆっくり合わせていくっちよ♪」
\t\tENDIF
\tENDIF
ENDIF''',
    ),
}

def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))

def main() -> None:
    for relative, (marker, anchor, replacement) in BLOCKS.items():
        path = ROOT / relative
        text = read_cp932(path)
        start = text.find(marker)
        if start < 0:
            raise SystemExit(f"marker not found: {relative} {marker}")
        body_start = text.find(anchor, start)
        if body_start < 0:
            raise SystemExit(f"anchor not found: {relative} {anchor}")
        separators = [pos for pos in (text.find("\n;--- ", body_start + 1), text.find("\n;===", body_start + 1)) if pos >= 0]
        if not separators:
            raise SystemExit(f"next block not found: {relative}")
        body_end = min(separators) + 1
        old_body = text[body_start:body_end]
        if old_body.count(anchor) != 1:
            raise SystemExit(f"unexpected block shape: {relative}")
        text = text[:body_start] + replacement + "\n" + text[body_end:]
        write_cp932(path, text)
        print(f"updated {relative}")

if __name__ == "__main__":
    main()

