"""残っているRAND3未完了5枠を、各キャラ固有の原作口調で補完する。"""

from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools/backups/remaining_rand3_20260904"


CASES = {
    30: {
        "source": "ゆう",
        "command": 17,
        "variants": {
            "on_lover": (
                "「わたしがこんな顔をするところ、ちゃんと覚えておいてくださいねぇ？　あとで忘れたふりは、許しませんよぉ♪」",
                "「ひゃっ……このままでは、わたしのお昼寝時間がなくなっちゃいますよぉ。ほら、そろそろ返してくださいなぁ♪」",
            ),
            "on_normal": (
                "「あぁっ、これが道具の力ですかぁ……。わたし、こんなに簡単に負けるつもりじゃなかったんですけどぉ!?」",
                "「わたしの許可なく、勝手に働くなんて……この道具、ずいぶん生意気ですねぇ？」",
            ),
            "off_lover": (
                "「あの……外したあと、手を繋いでいてくださいぃ。ひとりだと、まだふらふらしちゃいますから……」",
                "「この余韻まで、あなたのものってことにしておきますよぉ。返してほしくなったら言ってくださいねぇ♪」",
            ),
            "off_normal": (
                "「あら、これで満足ですかぁ？　わたしは平気……と言いたいところですけど、膝が笑ってますねぇ」",
                "「ふぅ……今日はここまでにしておきましょうかぁ。次は、もう少し上手に隠れてくださいねぇ？」",
            ),
        },
    },
    44: {
        "source": "ひよの",
        "command": 17,
        "variants": {
            "on_lover": (
                "「ふぇ……わたし、ちゃんと立っていられてますかぁ？　転校生さんが見てると、余計に力が抜けちゃいますぅ……♪」",
                "「はわわっ、これ以上は……わたし、ほんとに変になっちゃいますぅ。もう外してくださいぃ……！」",
            ),
            "on_normal": (
                "「あっ、あのっ、これ、わたしの意志じゃないですぅ！　勝手に動かすの、反則ですよぉ……！」",
                "「ふぇぇ……笑わないでくださいぃ。外せるなら、今すぐお願いしたいですぅ……！」",
            ),
            "off_lover": (
                "「はぅ……静かになったのに、胸のどきどきだけ残ってますぅ。転校生さん、笑わないでくださいね……」",
                "「えへへ……こんなに甘やかされると、またお願いしたくなっちゃいますぅ。秘密にしてくださいね？」",
            ),
            "off_normal": (
                "「ふぅ……お、終わったんですよねぇ？　わたし、しばらく動けそうにないですぅ……」",
                "「はわわ、まだ頭がふわふわですぅ……。お水をくださいぃ、ちゃんとお礼しますからぁ……」",
            ),
        },
    },
    45: {
        "source": "れいか",
        "command": 17,
        "variants": {
            "on_lover": (
                "「まあ……このわたくしが、道具ひとつに翻弄されるなんて。お兄さま、責任を持ってご覧なさい♪」",
                "「ふふ、声を隠すつもりでしたのに……あなたの前では、どうにも格好がつきませんわね♪」",
            ),
            "on_normal": (
                "「な、なんて屈辱……！　このわたくしが、玩具ごときに振り回されるなんて認めませんわっ！」",
                "「そ、そんなに見ないでくださる？　乱れた姿など、誰にも見せるつもりはありませんのに……！」",
            ),
            "off_lover": (
                "「ふふ……こんな姿を見られたことより、あなたが笑ってくださったことのほうが印象に残りそうですわ♪」",
                "「ふふ……このことは、円城寺家の秘密にしておきましょう。お兄さま、口外は許しませんわよ♪」",
            ),
            "off_normal": (
                "「はぁ……っ、わたくしをここまで疲れさせるなんて。片づけまで、きちんとなさいませ……」",
                "「もう十分ですわ……。これ以上は円城寺れいかの名誉に関わりますもの。早く外してくださいませ……！」",
            ),
        },
    },
    46: {
        "source": "みづき",
        "command": 17,
        "variants": {
            "on_lover": (
                "「おまえにだけは、こんなところ見せてもいいと思ってた……って、言わせるなよな！　ふっふ♪」",
                "「ふっふ……これがあれば、みなちゃんにも自慢できるか？　いや、するわけないだろっ♪」",
            ),
            "on_normal": (
                "「じ、自分で止められないの、悔しいぞ……！　こんな負け方、暗黒の覇者には似合わないからなっ！」",
                "「うぅ、止めろって言ってるのに……！　あとで絶対、覚えてろよ転校生……っ」",
            ),
            "off_lover": (
                "「まだ身体に電気が残ってるみたいだ……。おまえ、こんなの平気な顔で使うなよな……ふっふ♪」",
                "「あったかい……って、ちがうぞ！　べつに気に入ったわけじゃないからな♪」",
            ),
            "off_normal": (
                "「ふーっ……やっと静かになったな。わたしの覇者パワー、まだ残ってるぞ！」",
                "「こんな道具に負けたまま終われるかっ。次はちゃんと攻略してやるからな！」",
            ),
        },
    },
    67: {
        "source": "ましろ",
        "command": 90,
        "variants": {
            "lover": (
                "「ふむ、ここが弱いところか！　私の応援で、もっと元気にしてやるぞ☆」",
                "「おまえの反応、チア部の応援よりわかりやすいぞ☆　次はどんな顔をするのか、楽しみだな！」",
            ),
            "normal": (
                "「おぉ、反応したな！　そこが弱点か……ふむ、覚えておくぞ☆」",
                "「私に任せておけ！　そんな顔をしていても、最後まで元気にしてやるからな！」",
            ),
        },
    },
}


def command_span(text: str, command: int) -> tuple[int, int]:
    marker = f";--- COM{command}"
    start = text.index(marker)
    next_heading = re.search(r"^;--- COM", text[start + len(marker):], re.MULTILINE)
    heading_end = start + len(marker) + next_heading.start() if next_heading else len(text)
    next_return = re.search(r"^RETURN 0\s*$", text[start:heading_end], re.MULTILINE)
    end = start + next_return.start() if next_return else heading_end
    return start, end


def print_value(line: str) -> str:
    match = re.match(r"^\s*PRINTFORM(?:L|W)?\s+(.*)$", line)
    if not match:
        raise ValueError(f"PRINTFORMを読めません: {line!r}")
    return match.group(1)


def three(old: str, additions: tuple[str, str], indent: str = "\t\t\t") -> list[str]:
    return [
        f"{indent}IF A == 0",
        f"{indent}\tPRINTFORMW {old}",
        f"{indent}ELSEIF A == 1",
        f"{indent}\tPRINTFORMW {additions[0]}",
        f"{indent}ELSE",
        f"{indent}\tPRINTFORMW {additions[1]}",
        f"{indent}ENDIF",
    ]


def expand_com17(block: str, variants: dict[str, tuple[str, str]]) -> str:
    lines = block.splitlines()
    prints = [print_value(line) for line in lines if re.match(r"^\s*PRINTFORM(?:L|W)?\s+", line)]
    if len(prints) != 4:
        raise ValueError(f"COM17の既存台詞数が4ではありません: {len(prints)}")
    heading = lines[0]
    on_comment = next((line.strip() for line in lines if "装着" in line), ";装着")
    off_comment = next((line.strip() for line in lines if "取り外し" in line), ";取り外し")
    body = [
        heading,
        "IF SELECTCOM == 17",
        "\tA = RAND:3",
        "\tIF TEQUIP:17",
        f"\t\t{on_comment}",
        "\t\tIF TALENT:TARGET:153",
        *three(prints[0], variants["on_lover"], "\t\t\t"),
        "\t\tELSE",
        *three(prints[1], variants["on_normal"], "\t\t\t"),
        "\t\tENDIF",
        "\tELSE",
        f"\t\t{off_comment}",
        "\t\tIF TALENT:TARGET:153",
        *three(prints[2], variants["off_lover"], "\t\t\t"),
        "\t\tELSE",
        *three(prints[3], variants["off_normal"], "\t\t\t"),
        "\t\tENDIF",
        "\tENDIF",
        "ENDIF",
    ]
    return "\n".join(body) + "\n"


def expand_com90(block: str, variants: dict[str, tuple[str, str]]) -> str:
    lines = block.splitlines()
    prints = [print_value(line) for line in lines if re.match(r"^\s*PRINTFORM(?:L|W)?\s+", line)]
    if len(prints) != 2:
        raise ValueError(f"COM90の既存台詞数が2ではありません: {len(prints)}")
    heading = lines[0]
    body = [
        heading,
        "IF SELECTCOM == 90",
        "\tA = RAND:3",
        "\tIF TALENT:TARGET:153",
        "\t\tIF A == 0",
        "\t\t\t;恋人",
        f"\t\t\tPRINTFORMW {prints[0]}",
        "\t\tELSEIF A == 1",
        f"\t\t\tPRINTFORMW {variants['lover'][0]}",
        "\t\tELSE",
        f"\t\t\tPRINTFORMW {variants['lover'][1]}",
        "\t\tENDIF",
        "\tELSE",
        "\t\tIF A == 0",
        "\t\t\t;通常",
        f"\t\t\tPRINTFORMW {prints[1]}",
        "\t\tELSEIF A == 1",
        f"\t\t\tPRINTFORMW {variants['normal'][0]}",
        "\t\tELSE",
        f"\t\t\tPRINTFORMW {variants['normal'][1]}",
        "\t\tENDIF",
        "\tENDIF",
        "ENDIF",
    ]
    return "\n".join(body) + "\n"


def main() -> int:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for number, case in CASES.items():
        target = next(ROOT.glob(f"ERB/CHAR/CHAR_{number:02d}_*_COM.ERB"))
        source = ROOT / "tools/output" / f"{case['source']}.txt"
        source_text = source.read_text(encoding="utf-8-sig")
        if not source_text.startswith(f"# {case['source']}（全"):
            raise RuntimeError(f"原作ヘッダー確認失敗: {source}")
        backup = BACKUP_DIR / target.name
        if not backup.exists():
            shutil.copy2(target, backup)
        text = backup.read_bytes().decode("cp932").replace("\r\n", "\n")
        start, end = command_span(text, case["command"])
        block = text[start:end]
        if case["command"] == 17:
            replacement = expand_com17(block, case["variants"])
        else:
            replacement = expand_com90(block, case["variants"])
        text = text[:start] + replacement + text[end:]
        target.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
        print(f"CHAR{number:02d} COM{case['command']}: RAND3化")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
