"""CHAR41追加口上の内容重複を、CHAR41固有の反応へ差し替える。"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_41_悠木ともこ_COM.ERB"
sys.path.insert(0, str(ROOT / "tools"))
import add_missing_rand3_char41 as source  # noqa: E402


def replace_dialogue_once(lines: list[str], old: str, new: str) -> None:
    hits = []
    for i, line in enumerate(lines):
        if old in line:
            hits.append(i)
    if not hits and any(new in line for line in lines):
        return
    if len(hits) != 1:
        raise RuntimeError(f"置換対象が一意ではありません: {old!r} ({len(hits)}件)")
    i = hits[0]
    lines[i] = lines[i].replace(old, new, 1)


def set_print_line(line: str, text: str) -> str:
    if "「" not in line:
        raise RuntimeError(f"PRINTFORM行ではありません: {line!r}")
    prefix = line.split("「", 1)[0]
    return prefix + "「" + text + "」"


def replace_simple_rand3(lines: list[str]) -> int:
    changed = 0
    for command, texts in source.EXTRA.items():
        starts = [i for i, line in enumerate(lines) if line.strip() == f"IF SELECTCOM == {command}"]
        if len(starts) != 1:
            raise RuntimeError(f"COM{command}の開始位置が一意ではありません: {len(starts)}件")
        start = starts[0]
        end = next(
            (i for i in range(start + 1, len(lines)) if lines[i].strip().startswith("IF SELECTCOM == ")),
            len(lines),
        )
        print_indices = [
            i for i in range(start, end) if "PRINTFORM" in lines[i] and "「" in lines[i]
        ]
        if len(print_indices) != 6:
            raise RuntimeError(f"COM{command}のRAND3口上数が想定外です: {len(print_indices)}件")
        # A=0は原作を保持し、[恋人A1, 恋人A2, 通常A1, 通常A2]だけを差し替える。
        replacement_indices = [print_indices[1], print_indices[2], print_indices[4], print_indices[5]]
        for i, text in zip(replacement_indices, texts):
            lines[i] = set_print_line(lines[i], text)
            changed += 1
    return changed


def replace_new_commands(lines: list[str]) -> int:
    marker = ";=== TOMOKO RAND3 AND ADDITIONAL10 START ==="
    start = lines.index(marker)
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "RETURN 0")
    changed = 0
    for command, (_label, love, normal) in source.NEW_COMMANDS.items():
        heading = f";--- COM{command} "
        starts = [i for i in range(start, end) if lines[i].startswith(heading)]
        if len(starts) != 1:
            raise RuntimeError(f"追加COM{command}の開始位置が一意ではありません: {len(starts)}件")
        block_start = starts[0]
        block_end = next(
            (i for i in range(block_start + 1, end) if lines[i].startswith(";--- COM")),
            end,
        )
        print_indices = [
            i for i in range(block_start, block_end) if "PRINTFORM" in lines[i] and "「" in lines[i]
        ]
        if len(print_indices) != 6:
            raise RuntimeError(f"追加COM{command}の口上数が想定外です: {len(print_indices)}件")
        texts = [x.replace("あなた", "転校生さん") for x in (*love, *normal)]
        for i, text in zip(print_indices, texts):
            lines[i] = set_print_line(lines[i], text)
            changed += 1
    return changed


def main() -> None:
    raw = COM_PATH.read_bytes()
    lines = raw.decode("cp932").replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    changed = replace_simple_rand3(lines)
    changed += replace_new_commands(lines)

    # RAND3ブロック以外の状態枝に残っていた、他キャラと同型の言い回し。
    direct_replacements = {
        "自制心が、少しずつほどけていきます……転校生さん、もう少しだけ、そばにいてください♪":
            "自制心を保つつもりでしたのに……転校生さんの手があると、刀を握るより簡単に崩れてしまいます♪",
        "外れても、身体がまだ追いかけていますね。……落ち着くまで、そばにいてください":
            "外れたあとも、身体だけが続きを探しています……転校生さん、落ち着くまで肩を貸してください",
        "動くたびに響いてしまう……わたしの顔を見て、加減を覚えてくださいね":
            "動くたびに防具の金具まで鳴りそうです……わたしの呼吸が乱れない速さを覚えてくださいね",
        "また強くなりました……道具のくせに、わたしの弱いところをよく知っていますね":
            "強さが一段上がるたび、弱い場所だけ正確に撫でられる……道具に負けるのは悔しいですね",
        "もう限界です！　このような道具に負けたこと、誰にも言ってはいけませんよ……っ":
            "もう限界です！　この小さな道具に負けたこと、誰にも話してはいけませんよ……っ",
        "やっと静かになりました。次はわたしが仕返ししますから、逃げてはいけません♪":
            "ようやく静かになりました……次はわたしの番です。仕返しを受ける覚悟はできていますね♪",
        "まだ出るからと続けてはいけません。今日はここまで、わたしが決めます！":
            "まだ続けられるからと欲張ってはいけません。今日はここで終わり、わたしが決めます！",
        "汗を拭うだけのつもりでしたのに、あなたの手が離れると寂しく感じてしまいます":
            "汗を拭うだけのつもりでしたのに、あなたの手が止まると、次の動きを待ってしまいます",
    }
    for old, new in direct_replacements.items():
        # q()由来の行は、既存ソースでは呼称が転校生さんに正規化済み。
        old = old.replace("あなた", "転校生さん")
        new = new.replace("あなた", "転校生さん")
        replace_dialogue_once(lines, old, new)
        changed += 1

    encoded = ("\r\n".join(lines) + "\r\n").encode("cp932")
    COM_PATH.write_bytes(encoded)
    print(f"CHAR41固有口上へ更新: {changed}行")


if __name__ == "__main__":
    main()
