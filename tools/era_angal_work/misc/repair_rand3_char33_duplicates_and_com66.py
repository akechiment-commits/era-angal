"""CHAR_33のRAND分岐重複とCOM66視点を修正する。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_33_柊るな_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR33_before_duplicate_repair_20260810" / TARGET.name
MARKER = ";=== LUNA RAND3 DUPLICATE REPAIR AND COM66 VIEWPOINT 20260810 ==="
FINAL_MARKER = ";=== LUNA RAND3 DIALOGUE DIVERSIFICATION COMPLETE 20260810 ==="


DUPLICATE_REPAIRS = {
    (65, "love"): "んっ、%LOCALS%が震えるたび、ウチのほうが欲張りになってまう……もっと、声聞かせぃや♪",
    (196, "love"): "ひゃっ……%LOCALS%の熱、近ぅて……っ。そんなん見せられたら、ウチまで触りたなるやん……♪",
    (198, "love"): "自分と歩くん、なんや落ち着くなぁ……迷子になっても、ウチが見つけたるわ♪",
    (201, "love"): "ぺろ……っ、自分の指、こんな味するんやな。もう一回、こっち寄こしぃや♪",
    (160, "love"): "ちゅ……っ、%LOCALS%の舌、もっと奥まで来ぃや。ウチも逃がさへんからな♪",
    (189, "love"): "ん、ちゅ……%LOCALS%の熱、口の中で跳ねとる……っ。負けるん、悔しいわ♪",
    (188, "love"): "あっ、同時に入ってくるん……っ。%LOCALS%、動き合わせぃや。ウチまで壊れてまう……♪",
    (255, "love"): "んっ、そこ狙うん反則や……っ。自分のせいで、ウチの悪党面、保たへんやろ……♪",
    (256, "love"): "んっ、いちばん奥まで来るん……っ。自分のせいで、ウチまで素直にされてまうやん……♪",
    (56, "normal"): "%CALLNAME:ASSI%の声、えらいことになっとるなぁ……。自分、手ぇ抜いたらあかんで、ウチが最後まで見とるからな♪",
    (69, "normal"): "ん、ちゅぱ……っ。咥えたまま舐めるん、息できへんやん……でも、止めたらあかんで♪",
    (110, "normal"): "こんなん丸見えにされるん、ほんま屈辱や……っ。見終わったら、ちゃんと目ぇ逸らしぃや？",
    (132, "normal"): "その口、もう黙っとき。……ふふ、声出されへんぶん、目ぇがよう喋っとるで♪",
    (182, "normal"): "ん……ゴムに残ったんまで、ウチに飲ませる気かいな？　最後まで責任もって見ときぃや♪",
    (183, "normal"): "%CALLNAME:ASSI%の分まで、ウチが片づけるんかいな……。しゃあない、今回だけ特別やで♪",
    (184, "normal"): "たっぷり残っとるやん……ん、見てるだけやと落ち着かへんし、飲んだるわ♪",
    (185, "normal"): "ん……こぼすなや、ゆっくり飲みぃ。……ふふ、そんな顔されたら、もう一口わけたなるやん♪",
    (186, "normal"): "こ、これ飲ませて、あとは知らん顔とか許さへんからな……っ。ウチの面倒、ちゃんと見ぃや、自分……っ",
    (187, "normal"): "飲んどかなあかんのやろ？　……次はこんな心配させるなや。ウチかて、怖かったんやから……",
    (199, "normal"): "嫁役やからって、何でも言うこと聞くと思うなや？　……でも、『おかえり』くらいは言うたるわ♪",
    (201, "normal"): "ん、指一本でええ顔すなや……っ。ほら、もうちょい近ぅ持ってきぃ♪",
    (205, "normal"): "自分、そんな必死な顔で見せるんか……。ふふ、最後まで隠さず見せてみぃや♪",
    (160, "normal"): "ん……%LOCALS%の舌、ここやで。ウチばっかりにさせんと、ちゃんと返してや♪",
    (255, "normal"): "ひゃっ、そこ当たるたび、変な声出そうになるやん……っ。自分、わざとやろ？",
    (390, "normal"): "景品ほしいんか？　よっしゃ、ウチの腕前見せたるわ。取れたら自分にも分けたる♪",
}

# 完全一致ではないが、A=0の言い換えに留まっていた分岐も、場面の反応が
# 変わるように書き換える。キーは (COM番号, RAND出現順, 恋慕/通常) 。
NEAR_REWRITE_REPAIRS = {
    (19, 1, "normal"): "んっ、増えるたびに体の中が騒がしくなる……。自分、抜くタイミングまでちゃんと見ててや？",
    (26, 1, "normal"): "正面から見つめたまま来るん、逃げ道なくて困るわ……っ。腕、もっと強うしてや……",
    (27, 1, "normal"): "後ろから来るなら、せめて声かけぇや……っ。急に深ぅされたら、ほんまにびっくりするやろ！",
    (28, 1, "normal"): "抱きしめたまま動くん、ずるいわ……っ。耳元で囁かれたら、力抜けてまうやん……",
    (29, 1, "normal"): "背中預けたままやと、どこに当たっとるか余計わかってまう……っ。そんなに急かすなや……",
    (45, 1, "normal"): "んーっ……！　口塞がれたまま笑うなや！　外したら、まずその顔をどつくからな……っ",
    (46, 1, "normal"): "お腹の中、ぐるぐるして怖い……っ。自分、終わるまで手ぇを離したら許さへんで……",
    (54, 1, "normal"): "ここ、人に見られたらほんま終わりやで……っ。物音したら、ウチを抱えて走りぃや！",
    (57, 1, "love"): "こんな姿を自分に預けるん、ほんまはまだ恥ずかしいねん……。だから、笑わんといてな……♪",
    (57, 1, "normal"): "見るな言うても見るんやろ？　……せやったら、せめて可愛いと思っときぃや。口に出したら噛むで♪",
    (58, 1, "love"): "湯気の向こうに自分がおると、悪いことしてるみたいで落ち着かへん……。もう少しだけ、ここにおろや♪",
    (58, 1, "normal"): "熱ぅなったらのぼせるで？　……って言いながら、先に離れるんは惜しいなぁ……",
    (61, 1, "normal"): "%LOCALS%、その顔やめぇや……。次に舌が触れたら、ウチも手加減せぇへんからな♪",
    (65, 1, "normal"): "%LOCALS%、まだ強がるんか？　その震え、ウチには隠せへんで。もっと素直に鳴きぃや♪",
    (67, 1, "love"): "足先で触れられるたび、変なところまで熱くなる……。転校生、ゆっくりでええから続けて……♪",
    (67, 1, "normal"): "足で弄るんがそんなに楽しいんか？　……っ、出そうになっても笑うなや、ほんまに！",
    (68, 1, "normal"): "二人の舌が同じ場所に来ると、順番わからんくなるなぁ……。ほれ、自分、ちゃんと味わいぃ♪",
    (69, 1, "love"): "ん、息が重なる……っ。自分の熱を咥えたまま、ウチのことまで欲しがるん、欲張りやなぁ♪",
    (71, 1, "love"): "見せるだけのつもりやったのに、そんな目で見られたら隠せへんやん……。ちゃんと、優しゅう見てや♪",
    (71, 1, "normal"): "見るなら黙って見ときぃや！　実況みたいに騒いだら、秘密基地から叩き出すで……っ",
    (75, 1, "love"): "言葉で追い詰められるん、悔しいのに嫌やない……。もう一言だけ、ウチに聞かせて……♪",
    (75, 1, "normal"): "口で勝った気になるなや！　……でも、次の言葉はちょっとだけ期待してるからな♪",
    (80, 1, "love"): "喉の奥まで来るん、息が続かへん……っ。自分、急がずにウチの様子見ぃや……♪",
    (80, 1, "normal"): "んぐっ……！　苦しい言うてるやろ、手加減を覚えぃや！　……っ、でも止まったらそれはそれで困る……",
    (85, 1, "normal"): "そないに見張られたら、出るもんも出ぇへんやろ……っ。顔そむけるくらいの礼儀は持ちぃや！",
    (90, 1, "love"): "自分のお尻、ほんまに触るんか……。ウチが手ぇを添えたるから、ゆっくり確かめてみぃ♪",
    (90, 1, "normal"): "そこを覗き込んで笑うなや！　……っ、手ぇつけた責任、最後まで取らせるからな……♪",
    (130, 1, "love"): "目ぇ隠したら、次に何されるか想像して震えときぃや♪　逃げても手ぇは離さへんで？",
    (130, 1, "normal"): "見えへんのが怖いんか？　ほな、ウチの声だけ頼りにして、大人しゅうしときぃや♪",
    (131, 1, "love"): "縛られた自分、えらい素直やなぁ……。ほどく代わりに、ウチのお願いひとつ聞いてもらおか♪",
    (131, 1, "normal"): "暴れたら紐が食い込むで！　……っ、でもその必死な顔、もう少し見せときぃや♪",
    (132, 1, "love"): "口枷つけたら、目ぇだけで返事してくるんやな……。ふふ、今日はそれで十分や♪",
    (181, 1, "normal"): "ちゃんとつけたん確認したで。終わったあとに勝手に外したら、ほんまに怒るからな♪",
    (185, 1, "love"): "ん……口の中で渡すん、思ったより近すぎるな……。自分、舌まで絡める気ぃか♪",
    (186, 1, "love"): "薬ひとつでそこまで期待するなや……っ。けど、もしもの時は自分も一緒に考えてや♪",
    (188, 1, "normal"): "%LOCALS%、動き早すぎや……っ。互いに合わせるんやろ、ウチだけ置いてくなや！",
    (189, 1, "normal"): "%LOCALS%の口、そこばっかり来るん反則や……っ。お互い様やからって、容赦すなや♪",
    (197, 1, "love"): "湯気でぼやけた自分の顔、なんや安心するわ……。背中、今日はウチが流したる♪",
    (197, 1, "normal"): "風呂場でまで親分扱いするなや～。タオル取ってくれたら、隣におるん許したる♪",
    (199, 1, "love"): "『おかえり』の練習なんかしたら、ほんまに帰りを待ちたくなるやん……。責任とりぃや♪",
    (200, 1, "normal"): "%LOCALS%の熱がじかに来るん、ちっこい胸でも隠せへんな……。笑うたら承知せぇへんで♪",
    (203, 1, "love"): "%LOCALS%、そこまで見たら、もう検分やなくて覗き魔やで？　……ふふ、逃げ道は塞いだる♪",
    (203, 1, "normal"): "%LOCALS%の顔、見ながらゆっくり確かめたろか。怖がらんでええ、ウチが手ぇ添えたる♪",
    (204, 1, "love"): "自分の背中、ウチの体温でいっぱいにしたろか……。逃げずに、ちゃんと受け止めぃ♪",
    (204, 1, "normal"): "お尻で強がっても、締まるたびにばればれやで？　……ほれ、腰引くなや♪",
    (205, 1, "love"): "自分が夢中で動いとるん、見てると胸がざわつくわ……。もっと近くで見せてみぃ♪",
    (257, 1, "love"): "剃られる前からそんなに緊張して、可愛いやっちゃな……。刃ぁはゆっくり当てたるから、力抜きぃ♪",
    (257, 1, "normal"): "こら、刃ぁを見て騒ぐなや！　ウチの肌に傷つけたら、ただやないからな……っ",
    (13, 1, "love"): "んっ、後ろで震えるの、思ったより落ち着かへん……転校生、手ぇ握って、ウチの顔だけ見とき♪",
    (13, 1, "normal"): "ケツに入れたまま見物すなや……っ。抜くんやったら、ゆっくりせぇ。怖がらせた責任とりぃや！",
    (13, 2, "love"): "抜けたのに、そこだけ熱いままや……。自分、笑わずに隣おって。今はそれでええから……♪",
    (13, 2, "normal"): "終わった顔して近づくなや！　……っ、でも離れられたら、それはそれで腹立つわ……",
    (14, 1, "love"): "指先でそこばっかり狙うん、反則や……っ。ウチの弱点、覚えた顔すな♪",
    (14, 1, "normal"): "ひゃっ、そこを繰り返すなや！　勝ち誇った顔したら、次は噛むで……っ",
    (14, 2, "love"): "まだ熱、引いてへん……。自分の手ぇが離れると、余計に意識してまうから、もう少しだけ……♪",
    (14, 2, "normal"): "外したあとまで疼かせといて、涼しい顔すなや！　……次はウチが仕返しする番やで……っ",
    (15, 1, "love"): "留め具より、自分の視線のほうが熱いわ……。そんなに見たいなら、最後まで目ぇ逸らすなや♪",
    (15, 1, "normal"): "胸を弄って遊ぶなや！　……っ、外すまでの時間くらい、ウチの顔見て反省しぃや……っ",
    (15, 2, "love"): "外れたのに、まだそこだけ覚えとる……。自分、責任もって手ぇで落ち着かせてや♪",
    (15, 2, "normal"): "やっと外れたんやから、もう触るな！　……っ、いや、そこにおるだけなら許したる……",
    (16, 1, "love"): "出てくるとこ、そんな真面目に見んといて……っ。恥ずかしいけど、目ぇ逸らされたら寂しいやん♪",
    (16, 1, "normal"): "止めろ言うてるのに、記録みたいに眺めるなや！　……っ、ほんまに困っとるんやからな！",
    (16, 2, "love"): "外した途端に力抜けた……。転校生、笑わずに背中さすって。今だけ甘えさせてや……♪",
    (16, 2, "normal"): "もう十分や、服着せぃや！　……っ、終わったあとまで面白がったら、ほんまにどつくで……",
    (17, 1, "love"): "道具に腰を預けてるみたいで、なんや悔しいわ……。転校生、ちゃんとウチの目ぇ見てや♪",
    (17, 1, "normal"): "勝手に腰が動くん、見世物ちゃうで！　強さ戻して、ウチの言うこと聞きぃや……っ",
    (17, 2, "love"): "まだ体の奥が追いついてへん……。自分、急に離れんと、落ち着くまで隣におって……♪",
    (17, 2, "normal"): "静かになったからって勝った顔すなや！　次はウチがその道具、使いこなしたるからな……っ",
    (9, 1, "love"): "そこ、舌でなぞるん反則や……っ。自分の秘密まで覗かれとる気分になるわ……♪",
    (11, 1, "normal"): "ひ、ひゃっ……！　急に動かすなや、心臓まで揺れるやろ！　……っ、外すまで黙って抱いときぃや……",
    (38, 1, "love"): "尻で挟んだまま、そんな顔で見上げるなや……。動くたびにウチまで欲しくなるやん♪",
    (39, 1, "love"): "道具を握るんはウチやけど、気持ちよくするんは自分の役目やで？　ほら、声聞かせぃ♪",
    (42, 1, "normal"): "針先見えたら余計怖いやろ！　いきなり構えるなや、まずウチの手ぇ握ってからにせぇ……っ",
    (56, 1, "love"): "%CALLNAME:ASSI%、ええ声出しよるなぁ……。自分、ウチの前で格好つけんと、最後まで面倒見たれや♪",
    (59, 1, "normal"): "嫁さんごっこいうても、ウチは飯炊き係ちゃうで？　……せやけど、自分の帰りくらいは待ったるわ♪",
    (85, 1, "love"): "見られるんは恥ずかしいけど、目ぇ逸らされたら余計不安になる……。自分だけは、ちゃんとここにおって♪",
    (182, 1, "love"): "ゴムの中身まで欲しい顔すなや……。ん、そこまで頼られたら、ウチも断れへんけど♪",
    (183, 1, "love"): "%CALLNAME:ASSI%の分を口にするん、仕事みたいに言うなや……。ちゃんと顔見て、いただきます言いぃ♪",
    (183, 1, "normal"): "後始末まで押しつけるんかいな……。%CALLNAME:ASSI%、次は自分で片づけぇや。今回は特別やからな♪",
    (184, 1, "love"): "マスターのん、まだ温かい……。見てるだけの自分も、こっち来て礼言いぃ♪",
    (196, 1, "normal"): "ひっ、奥まで来るなん反則や……っ。%LOCALS%、見下ろす暇あるなら、ゆっくり動きぃや……",
    (200, 1, "love"): "胸合わせてるだけやのに、%LOCALS%の鼓動まで近ぅ聞こえる……。じっとしてられへんな♪",
    (9, 1, "normal"): "そこは見せるための場所ちゃうやろ……っ。舐めるなら、せめて優しゅうして。乱暴にしたら噛むで……",
    (38, 1, "normal"): "お尻で挟んだまま、勝手に腰振るなや！　……っ、気持ちええ顔すな、こっちまで調子狂うやろ♪",
    (413, 1, "normal"): "イカサマ見抜いたら、素直に負けを認めぃや！　……って、今の悔しそうな顔、ちょっと可愛いやん♪",
}


COM66_LINES = [
    "ん、ちゅ……っ、転校生と%LOCALS%の二本を一人で相手するんか。忙しいけど、どっちも可愛がったる♪",
    "お二人の熱、左右から重なるやん……自分ら、息合わせぃや。ウチがちゃんと相手したるから♪",
    "二人の声を聞きながらやと、胸までいっぱいになるわ……ウチのことも、ちゃんと見ときぃや♪",
    "ほれ、転校生と%LOCALS%の二本やろ？　ウチ一人で舐めたるわ、感謝しぃや♪",
    "二人とも、急かすなや。ウチの合図で順番に来ぃや、こぼしたら承知せぇへんで♪",
    "片方ずつでもええで……って、どっちも欲しい顔すなや。欲張り子分め♪",
]


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def command_block(lines: list[str], command: int) -> tuple[int, int]:
    start = next(
        i for i, line in enumerate(lines)
        if re.fullmatch(rf"(?:IF|ELSEIF) SELECTCOM == {command}", line.strip())
    )
    next_start = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"(?:IF|ELSEIF) SELECTCOM == \d+\s*$", lines[i].strip())),
        next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "RETURN 0"),
    )
    return start, next_start


def outer_talent_else(lines: list[str], start: int, end: int) -> tuple[int, int]:
    talent = next(i for i in range(start, end) if lines[i].strip() == "IF TALENT:TARGET:153")
    depth = 1
    for i in range(talent + 1, end):
        token = lines[i].strip().split(" ", 1)[0]
        if token == "IF":
            depth += 1
        elif token == "ENDIF":
            depth -= 1
        elif token == "ELSE" and depth == 1:
            return talent, i
    raise ValueError("恋慕/通常分岐のELSEが見つかりません")


def replace_a1_line(
    lines: list[str],
    start: int,
    end: int,
    branch: str,
    dialogue: str,
    rand_index: int = 1,
) -> None:
    rand_lines = [i for i in range(start, end) if re.search(r"\bA\s*=\s*RAND:3\b", lines[i])]
    if len(rand_lines) < rand_index:
        raise ValueError(f"COM{start}のRAND出現順が見つかりません: {rand_index}")
    rand_start = rand_lines[rand_index - 1]
    rand_end = rand_lines[rand_index] if rand_index < len(rand_lines) else end
    talent, outer_else = outer_talent_else(lines, rand_start, rand_end)
    branch_start, branch_end = (talent, outer_else) if branch == "love" else (outer_else, rand_end)
    a1 = next(i for i in range(branch_start, branch_end) if lines[i].strip() == "ELSEIF A == 1")
    branch_else = next(i for i in range(a1 + 1, branch_end) if lines[i].strip() == "ELSE")
    speech = [i for i in range(a1 + 1, branch_else) if "PRINTFORM" in lines[i]]
    if len(speech) != 1:
        raise ValueError(f"COM分岐のA=1台詞が1本ではありません: {speech}")
    prefix = lines[speech[0]].split("PRINTFORMW", 1)[0]
    lines[speech[0]] = f'{prefix}PRINTFORMW 「{dialogue}」'


def repair_com66(lines: list[str]) -> None:
    start, end = command_block(lines, 66)
    header = next(i for i in range(start, end) if lines[i].strip() == "IF SELECTCOM == 66")
    if not any(lines[i].strip().startswith("CALL AITE_YOBI") for i in range(start, end)):
        lines[header + 1 : header + 1] = ["\tCALL AITE_YOBI, 33, ASSI", '\tLOCALS \'= @"%RESULTS%"']
        start, end = command_block(lines, 66)
    speech = [i for i in range(start, end) if "PRINTFORMW" in lines[i]]
    if len(speech) != 6:
        raise ValueError(f"COM66の台詞本数が想定外です: {len(speech)}")
    for index, dialogue in zip(speech, COM66_LINES):
        prefix = lines[index].split("PRINTFORMW", 1)[0]
        lines[index] = f'{prefix}PRINTFORMW 「{dialogue}」'


def main() -> None:
    force_repair = "--fix-remaining" in __import__("sys").argv[1:]
    raw = TARGET.read_bytes()
    text = normalize(raw.decode("cp932"))
    if FINAL_MARKER in text and not force_repair:
        print("CHAR_33の完全重複・近似コピペ修正とCOM66視点修正は適用済みです。無変更で終了します。")
        return
    lines = text.split("\n")
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        BACKUP.write_bytes(raw)

    for (command, branch), dialogue in DUPLICATE_REPAIRS.items():
        start, end = command_block(lines, command)
        replace_a1_line(lines, start, end, branch, dialogue)
    for (command, rand_index, branch), dialogue in NEAR_REWRITE_REPAIRS.items():
        start, end = command_block(lines, command)
        replace_a1_line(lines, start, end, branch, dialogue, rand_index)
    repair_com66(lines)

    if MARKER not in text:
        marker_line = next(i for i, line in enumerate(lines) if line.strip() == ";--- COM65 助手を犯させる ---")
        lines.insert(marker_line, MARKER)
    if FINAL_MARKER not in lines:
        marker_line = next(i for i, line in enumerate(lines) if line.strip() == ";--- COM65 助手を犯させる ---")
        lines.insert(marker_line, FINAL_MARKER)
    output = "\r\n".join(lines).rstrip("\r\n") + "\r\n"
    TARGET.write_bytes(output.encode("cp932"))
    print("CHAR_33の完全重複25件と近似コピペ分岐を追加修正し、COM66 Wフェラ視点も統一しました。")


if __name__ == "__main__":
    main()
