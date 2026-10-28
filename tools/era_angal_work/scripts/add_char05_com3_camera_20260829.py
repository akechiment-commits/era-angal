"""CHAR05・桃智あすかのCOM3に、原作準拠の撮影時差分を追加する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_05_桃智あすか_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR05_before_com3_camera_20260829/CHAR_05_桃智あすか_COM.ERB"
REWRITE_BACKUP = ROOT / "tools/backups/CHAR05_before_com3_camera_rewrite_20260829/CHAR_05_桃智あすか_COM.ERB"

CAMERA_LINES = (
    "「え、カメラで撮るんすか先輩!?　見られながらするのとは違って、あとに残ると思うと……マジで恥ずかしいっす……♪」",
    "「うっす……レンズが向いてると、先輩が見てるだけのときより心臓が跳ねるっす。あたしの顔まで映るんすよね……♪」",
    "「先輩、ちゃんと撮れてるんすか……？　いちばん恥ずかしいところが残ると思うと、手ぇが止まりそうで……でも、もう止まらないっす♪」",
    "「うひゃっ、カメラまであるんすか!?　先輩に見られるだけでも無理なのに、これ、記録に残るんすよね!?」",
    "「や、やっぱり撮られるのは恥ずかしいっす……！　あとで見返すとか、あたし絶対むりっすからねっ!?」",
    "「うにに……レンズがこっち向いてると、手ぇが変になるっす……。見ないでほしいのに、カメラがあるほうが意識しちゃうっす……！」",
)

OLD_CAMERA_LINES = (
    "「先輩が見てるなら、あたし、もっと頑張れるっす……。今日は先輩専用っすよ♪」",
    "「うっす☆　見られてると燃えてくるっすね！　あたしの本気、ちゃんと見ててくださいっす♪」",
    "「あたしのこと、いっぱい見てほしいっす……。先輩の前なら、これぐらいへっちゃらっすよ♪」",
    "「えっ、見てるんすか先輩!?　自分でしてるとこなんて、マジ恥ずかしいっすぅ！」",
    "「ちょ、そんなに見ないでほしいっす！　あたし、どこ見ればいいかわかんないっすよ～っ！」",
    "「うにに……こんなところまで見られたら、心臓が試合みたいに跳ねるっす！」",
)


def read_lines() -> list[str]:
    return TARGET.read_bytes().decode("cp932").splitlines()


def write_lines(lines: list[str]) -> None:
    TARGET.write_bytes("\r\n".join(lines).encode("cp932") + b"\r\n")


def add_camera(lines: list[str]) -> list[str]:
    start = next(i for i, line in enumerate(lines) if line.startswith(";--- COM3 "))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith(";--- COM4 "))
    block = lines[start:end]
    if any(line.strip() == "IF TEQUIP:53" for line in block):
        for old, new in zip(OLD_CAMERA_LINES, CAMERA_LINES):
            lines[start:end] = [line.replace(old, new) for line in lines[start:end]]
        return lines

    selector = next(i for i, line in enumerate(block) if line == "IF SELECTCOM == 3")
    outer_end = max(i for i in range(selector + 1, len(block)) if block[i] == "ENDIF")
    normal_body = block[selector + 1 : outer_end]
    camera = [
        "\t;--- ビデオ撮影中 ---",
        "\tIF TEQUIP:53",
        "\t\tA = RAND:3",
        "\t\tIF TALENT:TARGET:153",
        "\t\t\tIF A == 0",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[0]}",
        "\t\t\tELSEIF A == 1",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[1]}",
        "\t\t\tELSE",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[2]}",
        "\t\t\tENDIF",
        "\t\tELSE",
        "\t\t\tIF A == 0",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[3]}",
        "\t\t\tELSEIF A == 1",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[4]}",
        "\t\t\tELSE",
        f"\t\t\t\tPRINTFORMW {CAMERA_LINES[5]}",
        "\t\t\tENDIF",
        "\t\tENDIF",
        "\tELSE",
        "\t\t;--- 通常 ---",
    ]
    camera.extend(("\t" + line) if line else line for line in normal_body)
    camera.append("\tENDIF")
    lines[start:end] = block[: selector + 1] + camera + block[outer_end:]
    return lines


def main() -> None:
    original = TARGET.read_bytes()
    lines = read_lines()
    before = list(lines)
    updated = add_camera(lines)
    if updated == before:
        print("変更なし: CHAR05 COM3の撮影時分岐は既に反映済み")
        return
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(original)
    if any(old in line for old in OLD_CAMERA_LINES for line in before):
        REWRITE_BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if not REWRITE_BACKUP.exists():
            REWRITE_BACKUP.write_bytes(original)
    write_lines(updated)
    print("更新: CHAR05 COM3に撮影時RAND3を追加")


if __name__ == "__main__":
    main()
