"""CHAR_32 安条まいの独自口上RAND:3化と追加10コマンド生成。

ERBはCP932/CRLFで管理されているため、このスクリプト自体はUTF-8で保持し、
読み書きの境界で明示的に変換する。既にマーカーがある場合は無変更で終了する。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_32_安条まい_COM.ERB"
BACKUP_PATH = ROOT / "tools/backups/CHAR32_before_rand3_and_additional10_20260810/CHAR_32_安条まい_COM.ERB"
MARKER = ";=== MAI RAND3 AND MISSING COMMANDS START ==="


# 各独自コマンドは現行のA=0を原文として保持し、A=1/A=2を追加する。
# 値は (恋慕追加2本, 通常追加2本) の順。
CUSTOM_EXTRA: dict[int, tuple[list[str], list[str]]] = {
    280: (
        [
            "街の明かりより、あんたの顔見てるほうが落ち着くんだけど……なんでだろ。あたし、けっこう単純じゃん♪",
            "バイトの帰りにこんな寄り道、青春って感じでよくない？　今日はあんたを独占ってことで♪",
        ],
        [
            "ここ、裏道でも人は来るからね。あんた、急に動くと目立つって。まったく大胆なんだから。",
            "次のシフトまで時間あるけど、あたしを連れ回すなら飲み物くらい買ってよね。世話焼きにも燃料はいるんだよ♪",
        ],
    ),
    281: (
        [
            "休憩の短い時間でも、あんたといるとちゃんと息ができるな。……もう少しだけ、ここにいていい？",
            "シフトに戻る前に、あたしのことだけ見て。今日のご褒美、これで足りるっしょ♪",
        ],
        [
            "タイムカード押す時間、忘れないでよ？　あたしが怒られるのはごめんだからね。",
            "休憩室は休む場所。無茶してまで付き合わなくていいってば、あんたまで倒れたら面倒じゃん。",
        ],
    ),
    282: (
        [
            "声を抑えてるあんた、なんか新鮮。……でも、あたしの服を乱すなら最後まで責任持ってよね♪",
            "鏡に映るあたしより、あんたの目のほうが気になる。そんなに見たいなら、ちゃんと似合うって言って？",
        ],
        [
            "更衣室は段取りが命なんだから、服を床に置かない。あたしが世話焼きだからって甘えすぎ。",
            "誰か来たら終わりだよ？　ほら、制服直して。あんたのほうが慌ててるじゃん、あはは♪",
        ],
    ),
    283: (
        [
            "今日は晩ご飯を一人で食べなくていいんだね。……あんたがいるだけで、部屋の音が増えるみたい。",
            "家族の話は苦手だけど、あんたには聞いてほしい。あたし、寂しいって言えるくらいには頼ってるからさ。",
        ],
        [
            "冷蔵庫のもの、勝手に食べていいのはあたしが出した分だけ。家主のルール、覚えといて。",
            "部屋だからって好き放題はなし。あたしのベッドをじろじろ見るなって、恥ずいじゃん。",
        ],
    ),
    284: (
        [
            "バイトでくたくたでも、あんたが待ってるなら来てよかったって思える。……少しだけ、肩貸して♪",
            "今日の売上も片付けも終わり。あとはあんたに甘える時間って、ちゃんと予定に入れてたんだよ。",
        ],
        [
            "裏路地は近道でも、周りを見て歩く。あんたを守るのも帰宅部の仕事だからね。",
            "待っててくれたのは嬉しいけど、次からは店の前で連絡して。捜索する羽目になったら大変じゃん。",
        ],
    ),
    410: (
        [
            "流行りのスイーツを見つけるのも得意だけど、今日いちばん当たりなのはあんたと歩けたことかな♪",
            "SNSに載せる写真、あんたが隣にいると盛れるね。……この一枚は、あたしだけの思い出にしよ。",
        ],
        [
            "食べ歩きは計画的に。財布と胃袋の残量、どっちも見ながら回るのがプロってもんだよ。",
            "新作を見つけたら教えるから、あんたは列の最後尾を確保。付き添いにも役割分担はあるっしょ。",
        ],
    ),
    411: (
        [
            "一緒に食べると、ただのバーガーでも賑やかな食卓みたい。あたし、こういうの欲しかったんだよね。",
            "ポテトの最後の一本、あんたにあげる。……その代わり、次はあたしの好きな店に付き合って♪",
        ],
        [
            "ソース付けすぎ。ほら、ナプキン使って。あんたの世話まで焼くのがデートの仕事じゃないんだけどな。",
            "飲み物はこぼさない、包み紙は分別。楽しく食べた後まできれいにするのが安条まいちゃん流ね。",
        ],
    ),
    412: (
        [
            "このぬいぐるみ、あんたのために取ったんだから大事にしてよ。……あたしが一番に選んだ証拠♪",
            "勝てたのはあんたが見ててくれたからかも。次は二人で遊べる台、探そっか。",
        ],
        [
            "その台は力じゃなくてタイミング。ほら、あたしの手元見て。転校生、ちゃんと覚えてよ。",
            "景品に釣られて散財は禁止。次のゲーム代はあたしが計算するから、あんたは反省担当ね。",
        ],
    ),
    413: (
        [
            "この服、あんたが選んだなら着て帰ろうかな。……あたしを一番にしてくれる感じ、悪くないじゃん♪",
            "あんたの好みを聞くの、意外と楽しい。次はあたしが選ぶから、逃げないでよね。",
        ],
        [
            "流行ってだけで買うと後悔するよ？　着回しまで考えて選ぶのが、本当におしゃれってやつ。",
            "あんたの服も一緒に見よ。サイズと色を確認して、明日から使えるコーデにしたげる。",
        ],
    ),
    414: (
        [
            "夕焼けって派手じゃないのに、今日のことをちゃんと残してくれるね。あんたの隣、あたし好きかも。",
            "普通の一日を楽しいって思えるの、あんたとだからかな。次の予定、もう決めちゃっていい？",
        ],
        [
            "遊び疲れたなら無理に歩かない。帰るまでが付き添いなんだから、あたしの指示に従って。",
            "今日は解散、でも次の休みは空けといてよ。退屈させない係、まだ辞める気ないからね。",
        ],
    ),
}


# (見出し, 恋慕3本, 通常3本)。恋慕判定は追加コマンド共通の85を使う。
NEW_COMMANDS: dict[int, tuple[str, list[str], list[str]]] = {
    60: (
        "助手にキス",
        [
            "%LOCALS%の唇、あんたに見られながらだと余計に熱くなるじゃん。……でも、目をそらさないでよ♪",
            "%LOCALS%とキスするなら、あたしが先に空気を作る。ほら、見てて。これも帰宅部のサービス……じゃなくて、あたしの本気。",
            "%LOCALS%に触れる前から、あんたの視線が気になってる。終わったら、あたしのほうにもちゃんと構ってよね。",
        ],
        [
            "%LOCALS%、口を開けて。あたしが合わせるから、焦らなくていいよ。あんたは見て覚えな。",
            "キスくらいで固まらないの。%LOCALS%も緊張してるから、あたしが仕切る。しっかり息してよね。",
            "%LOCALS%の顔、真っ赤じゃん。あたしの教え方が上手すぎるってことかな？　あんたも感想くらい言いなよ。",
        ],
    ),
    62: (
        "二本同時素股",
        [
            "%LOCALS%とあたしで、あんたを挟むんだね。息を合わせて、あんたが気持ちよくなる順番まで考えてるから♪",
            "片方だけ見てたら、もう片方が拗ねるよ？　%LOCALS%もあたしも、あんたの反応を独占したいんだから。",
            "動きが重なると、%LOCALS%の熱とあたしの熱が一つになるみたい。あんた、ちゃんと受け止めてよね。",
        ],
        [
            "%LOCALS%、合図したら同じ速さ。あたしが数えるから、あんたは力を抜いて。こういうのも段取りが大事。",
            "片方ずつ欲張ると危ないよ。%LOCALS%と相談して、あんたがまだ余裕ある範囲で続けるからね。",
            "ほら、%LOCALS%とタイミング合わせて。あんたが動くとずれるんだから、主役は受け身でいてよ。",
        ],
    ),
    76: (
        "助手と双頭バイブ",
        [
            "%LOCALS%と一緒に震えるの、思ったより負けたくなくなるね。あたしの声、聞き逃さないでよ♪",
            "右と左で刺激が違うじゃん。%LOCALS%、先に限界になったら、あたしがちゃんと受け止めるから。",
            "二人とも余裕がなくなってきたね。%LOCALS%の熱、あたしが最後まで感じてる。",
        ],
        [
            "%LOCALS%、合図はあたしに合わせて。強さを上げるなら同時、ずらすとびっくりするから。",
            "あたしは平気って言いたいけど、これ、思ったより効くね。%LOCALS%、声を出しても笑わないから。",
            "二人で使うなら片付けまで二人分。%LOCALS%、終わったら道具を拭いて、あたしは記録するね。",
        ],
    ),
    78: (
        "母乳飲み",
        [
            "ん……あんたが欲しがるなら、ちゃんと飲ませてあげる。あたしのこと、近くで感じてよね♪",
            "そんなに急がなくていいって。あたしが抱いてるから、好きなだけ甘えて。……今だけは世話焼きじゃなくて恋人でいたいな。",
            "飲んでる顔を見てると、あんたにあたしを預けてもいいって思える。こぼさないで、全部受け取ってよ。",
        ],
        [
            "直接飲むなら、あたしの合図を聞く。急に吸ったらむせるから、そこはちゃんと守って。",
            "母乳が出るからって、飲み物みたいに扱わないでよ？　あたしの身体なんだから、丁寧にね。",
            "飲んだら水分も取って。あんたの面倒を見るところまでが、このコマンドのセットだから。",
        ],
    ),
    79: (
        "乳搾り",
        [
            "手で搾られると、飲むのとは違う恥ずかしさがあるじゃん。あんたになら、こうして預けてもいいけど♪",
            "そこ、やさしく押して。あたしの身体のこと、あんたの手で覚えていってよ。",
            "搾った分はあんたが大事にして。あたしの頑張りも、甘いご褒美も、全部持って帰っていいから。",
        ],
        [
            "手順を言うから聞いて。根元からゆっくり、痛かったらすぐ止める。あたしは我慢大会しないよ。",
            "強く握れば出るってもんじゃないの。世話焼きのあたしが教えるから、焦らないで。",
            "搾ったらこぼさず片付ける。あんた、仕事を始めたら最後まで責任持つんだよ。",
        ],
    ),
    84: (
        "Gスポット刺激",
        [
            "そこがあたしの弱いところだって、もう覚えたんだ。……あんたに探されると、強がれなくなるじゃん♪",
            "ちょっと待ってって言っても、嫌って意味じゃないからね。あたしの息が戻るまで、手は離さないで。",
            "もっと欲しいって言うの、あんたの前なら恥ずくない。あたしを一番にしてくれるなら、最後まで付き合って。",
        ],
        [
            "場所は合ってるけど、急に強くしない。あたしの反応を見て、探るように動かしてよ。",
            "そこ、効くけど説明はできるよ。角度を少し変えて、あたしが頷いたら続ける。わかった？",
            "ふっふっふ、あたしの弱点を見つけたつもり？　でも扱いが雑なら、お仕置きだからね。",
        ],
    ),
    86: (
        "強制放尿",
        [
            "止めたいのに止まらない……あんたの前でこんな姿、見せるつもりじゃなかった。だから、最後までそばにいて。",
            "恥ずかしいけど、あんたが見捨てないって思えるなら、ちゃんと受け止める。……終わったら抱きしめてよ。",
            "こんなことであたしの価値を決めないで。あたしはあたし、ただ今だけは、あんたの手を離したくない。",
        ],
        [
            "ふざけんな、身体の都合を笑い話にしないでよ。見てるなら、片付けまで手伝って。",
            "止められないのはあたしの意思じゃない。だから、勝手に触らず、言われた通りにして。",
            "屈辱なのはわかってる。でも、ここで取り乱したら余計に危ない。水と着替え、すぐ用意して。",
        ],
    ),
    202: (
        "助手と乳首合わせ",
        [
            "%LOCALS%の胸、近いと熱が混ざるね。あたし、こんなに素直になるのは久しぶりかも♪",
            "%LOCALS%、そこ……いい。あたしの反応、ちゃんと覚えて。次はもっと息を合わせようよ。",
            "胸を重ねるだけなのに、%LOCALS%の心臓まで聞こえる。あたし、もう少しこのままでいたいな。",
        ],
        [
            "%LOCALS%、高さを合わせて。急ぐと擦れて痛いから、胸を押しつける角度を少し下げて。",
            "比較するつもりはないけど、%LOCALS%もなかなかやるじゃん。あたしも負けないから、ちゃんと動いて。",
            "終わったら汗を拭こう。胸を合わせるだけでも疲れるんだから、無理はなしね。",
        ],
    ),
    258: (
        "助手の顔騎乗を受けながら正常位",
        [
            "%LOCALS%があんたの顔にまたがって、あたしはあんたの中で揺れてる。どっちも感じてるって、わかる？♪",
            "%LOCALS%の熱があんたの顔に触れるたび、あたしの身体まで跳ねる。あんた、全部まとめて受け止めてよ。",
            "上ではあたしが動いて、下では%LOCALS%があんたを包んでる。……こんなに欲張りになるの、あんたのせいだからね。",
        ],
        [
            "%LOCALS%、あんたの顔に体重をかけすぎない。あたしも上で動くから、苦しくなったらちゃんと言って。",
            "顔を塞がれても、あんたの動きはあたしに伝わってる。%LOCALS%と息を合わせて、勝手に止まらないでよ。",
            "二人分を同時に受けるのは楽じゃないっしょ？　あたしが数えるから、%LOCALS%もあんたも無理しない。",
        ],
    ),
    318: (
        "頭を撫でる",
        [
            "よしよし、今日もみんなの面倒見て疲れたね。……今だけは、あたしがあんたの一番近くで支えるから♪",
            "帰宅部の部長みたいな顔してるけど、あんたも甘えていいんだよ。ほら、頭こっち。撫でられるの、嫌じゃないっしょ？",
            "何でも一人で抱えるなって言ったでしょ。あたしが頭を撫でてる間くらい、あたしだけを頼ってよね。",
        ],
        [
            "はい、頭出して。人の心配ばっかりしてる転校生は、まず自分を休ませる。これは帰宅部の決定事項。",
            "今日の頑張り、ちゃんと見てたよ。だから撫でてるだけ。変な期待したら、お仕置きだからね♪",
            "一人で背負うの禁止。あたしたちが支えるって決めたんだから、今は黙って目を閉じてな。",
        ],
    ),
}


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def find_matching_endif(lines: list[str], start: int) -> int:
    depth = 0
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("IF "):
            depth += 1
        elif stripped == "ENDIF":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"ENDIFが見つかりません: {start + 1}行目")


def print_lines(lines: list[str], prefix: str) -> list[str]:
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("PRINTFORM"):
            result.append(prefix + stripped)
    if not result:
        raise ValueError("PRINTFORM系の原文が見つかりません")
    return result


def render_random_talent(
    indent: str,
    talent_lines: list[str],
    normal_lines: list[str],
    extra_talent: list[str],
    extra_normal: list[str],
) -> list[str]:
    """既存台詞をA=0に置き、A=1/A=2を追加した内側分岐を作る。"""

    control = indent + "\t"
    speech = indent + "\t\t"
    result = [
        f"{indent}A = RAND:3",
        f"{indent}IF TALENT:TARGET:153",
        f"{control}IF A == 0",
    ]
    result.extend(print_lines(talent_lines, speech))
    result.extend(
        [
            f"{control}ELSEIF A == 1",
            f'{speech}PRINTFORMW 「{extra_talent[0]}」',
            f"{control}ELSE",
            f'{speech}PRINTFORMW 「{extra_talent[1]}」',
            f"{control}ENDIF",
            f"{indent}ELSE",
            f"{control}IF A == 0",
        ]
    )
    result.extend(print_lines(normal_lines, speech))
    result.extend(
        [
            f"{control}ELSEIF A == 1",
            f'{speech}PRINTFORMW 「{extra_normal[0]}」',
            f"{control}ELSE",
            f'{speech}PRINTFORMW 「{extra_normal[1]}」',
            f"{indent}\tENDIF",
            f"{indent}ENDIF",
        ]
    )
    return result


def custom_chain_modifications(lines: list[str]) -> list[tuple[int, int, list[str]]]:
    modifications = []
    for first, last in ((280, 284), (410, 414)):
        outer_start = next(
            (i for i, line in enumerate(lines) if line.strip() == f"IF SELECTCOM == {first}"),
            None,
        )
        if outer_start is None:
            raise ValueError(f"COM{first}の独自コマンド連鎖が見つかりません")
        outer_end = find_matching_endif(lines, outer_start)
        branch_starts = [
            (i, int(match.group(1)))
            for i in range(outer_start, outer_end + 1)
            if (match := re.match(r"(?:IF|ELSEIF) SELECTCOM == (\d+)\s*$", lines[i].strip()))
        ]
        expected = list(range(first, last + 1))
        if [command for _, command in branch_starts] != expected:
            raise ValueError(f"COM{first}-{last}の分岐が想定外です: {branch_starts}")

        for branch_index, (branch_start, command) in enumerate(branch_starts):
            branch_end = (
                branch_starts[branch_index + 1][0]
                if branch_index + 1 < len(branch_starts)
                else outer_end
            )
            talent_start = next(
                (
                    i
                    for i in range(branch_start, branch_end)
                    if lines[i].strip() == "IF TALENT:TARGET:153"
                ),
                None,
            )
            if talent_start is None:
                raise ValueError(f"COM{command}にTALENT:TARGET:153分岐がありません")
            talent_end = find_matching_endif(lines, talent_start)
            if talent_end >= branch_end:
                raise ValueError(f"COM{command}の恋慕分岐が閉じていません")
            else_index = next(
                (i for i in range(talent_start + 1, talent_end) if lines[i].strip() == "ELSE"),
                None,
            )
            if else_index is None:
                raise ValueError(f"COM{command}の通常分岐がありません")
            indent = lines[talent_start][: len(lines[talent_start]) - len(lines[talent_start].lstrip())]
            replacement = render_random_talent(
                indent,
                lines[talent_start + 1 : else_index],
                lines[else_index + 1 : talent_end],
                CUSTOM_EXTRA[command][0],
                CUSTOM_EXTRA[command][1],
            )
            modifications.append((talent_start, talent_end + 1, replacement))
    return modifications


def render_new_command(command: int, label: str, love: list[str], normal: list[str]) -> list[str]:
    assistant = command in {60, 62, 76, 202, 258}
    result = [
        f";--- COM{command} {label}（追加10コマンド） ---",
        f"IF SELECTCOM == {command}",
    ]
    if assistant:
        result.extend(
            [
                "\tCALL AITE_YOBI, 32, ASSI",
                '\tLOCALS \'= @"%RESULTS%"',
            ]
        )
    result.extend(
        [
            "\tA = RAND:3",
            "\tIF TALENT:TARGET:85",
            "\t\tIF A == 0",
            f'\t\t\tPRINTFORMW 「{love[0]}」',
            "\t\tELSEIF A == 1",
            f'\t\t\tPRINTFORMW 「{love[1]}」',
            "\t\tELSE",
            f'\t\t\tPRINTFORMW 「{love[2]}」',
            "\t\tENDIF",
            "\tELSE",
            "\t\tIF A == 0",
            f'\t\t\tPRINTFORMW 「{normal[0]}」',
            "\t\tELSEIF A == 1",
            f'\t\t\tPRINTFORMW 「{normal[1]}」',
            "\t\tELSE",
            f'\t\t\tPRINTFORMW 「{normal[2]}」',
            "\t\tENDIF",
            "\tENDIF",
            "ENDIF",
            "",
        ]
    )
    return result


def additional_commands_block() -> list[str]:
    result = [MARKER, "; 安条まい：助手呼称はAITE_YOBIで解決し、恋慕はTALENT:TARGET:85。"]
    for command, (label, love, normal) in NEW_COMMANDS.items():
        result.extend(render_new_command(command, label, love, normal))
    return result


def main() -> None:
    rebuild_from_backup = "--rebuild-from-backup" in sys.argv[1:]
    source_path = BACKUP_PATH if rebuild_from_backup else COM_PATH
    raw = source_path.read_bytes().decode("cp932")
    text = normalize(raw)
    if MARKER in text and not rebuild_from_backup:
        print("既にCHAR_32追加ブロックがあります。無変更で終了します。")
        return
    lines = text.split("\n")
    modifications = custom_chain_modifications(lines)

    virgin_index = next(
        (i for i, line in enumerate(lines) if line.strip() == "@CHAR_VIRGIN_32"),
        None,
    )
    if virgin_index is None:
        raise ValueError("@CHAR_VIRGIN_32が見つかりません")
    return_index = next(
        (i for i in range(virgin_index - 1, -1, -1) if lines[i].strip() == "RETURN 0"),
        None,
    )
    if return_index is None:
        raise ValueError("@CHAR_VIRGIN_32直前のRETURN 0が見つかりません")
    modifications.append((return_index, return_index, additional_commands_block()))

    updated = lines[:]
    for start, end, replacement in sorted(modifications, key=lambda item: item[0], reverse=True):
        updated[start:end] = replacement
    result = "\n".join(updated).rstrip("\n") + "\n"

    encoded = result.encode("cp932")
    if not BACKUP_PATH.exists():
        BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
        BACKUP_PATH.write_bytes(COM_PATH.read_bytes())
    COM_PATH.write_bytes(encoded.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR_32 安条まい: 独自10枠をRAND:3化し、追加10コマンドを挿入しました。")
    print(f"更新: {COM_PATH}")


if __name__ == "__main__":
    main()
