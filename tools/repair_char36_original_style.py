from collections import Counter
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_36_遠見ちか_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR36_before_rand3_and_additional10_20260810/CHAR_36_遠見ちか_COM.ERB"

SPECIAL_REPLACEMENTS = {
    "面倒が増えるじゃないですぅ！": "面倒が増えるんですよぉ！",
    "ふぇっ、何ですぅ、この音!?": "ふぇっ、何ですかぁ、この音!?",
    "顔を見ながら後ろですぅ……": "顔を見ながら、後ろからなんですぅ……",
    "抱きしめられたまま後ろですぅ……": "抱きしめられたまま、後ろからなんですぅ……",
    "この格好で後ろですぅ!?": "この格好で後ろからですかぁ!?",
    "ヘルプマンの口から、わたしの口へですぅ……": "ヘルプマンの口から、わたしの口へ……",
    "お腹の奥がきゅっとするかもですぅ？": "お腹の奥がきゅっとするかもしれないですよぉ？",
    "残ってるですぅ": "残ってるんですぅ",
    "外れたですぅ": "外れたんですぅ",
    "強くなったですぅ": "強くなったんですぅ",
    "速くなったですぅ": "速くなったんですぅ",
    "変になりそうですぅ": "変になりそうなんですぅ",
    "たっぷり甘やかされたですぅ": "たっぷり甘やかしてもらったんですぅ",
    "ありがとですぅ": "ありがとぉ",
    "お口でたぁっぷり奉仕ですぅ☆": "お口でたぁっぷり可愛がりますよぉ☆",
    "開帳ですぅ♪": "開いてきちゃうんですぅ♪",
    "仕組みがあるんですぅ♪": "仕組みがあるんですねぇ♪",
    "仕組みがあるんですよぉ♪": "仕組みがあるんですねぇ♪",
    "途中でやめるのも悪いですぅ": "途中でやめるのも、もったいないですぅ",
    "ますかぁ？": "ますよぉ？",
    "してくれますかぁ♪": "してくれますよぉ？♪",
    "頼りますかぁ……": "頼りますよぉ……",
    "使いますかぁ♪": "使いますよぉ？♪",
    "ふぁい、何もしないんですかぁ。": "はい、何もしないんですかぁ。",
    "ふぁい、見ておきますよぉ。": "はい、見ておきますよぉ。",
    "くださいぃ": "くださぁい",
    "ありがとぉ♪": "ありがとう……♪",
    "にょおっ": "にょっ",
    "%LOCALS%とお互いのをくわえるんですねぇ……。顔が近いですけど、わたし、すぐ慣れると思いますよぉ♪": "ん、ぺろ……顔が近くて、%LOCALS%の息まで頬にかかりますよぉ。わたし、ゆっくり合わせますからねぇ♪",
}


def normalize_dialogue(line: str) -> str:
    for old, new in SPECIAL_REPLACEMENTS.items():
        line = line.replace(old, new)
    line = line.replace("ですぅ？", "ですかぁ？")
    line = line.replace("ますぅ？", "ますかぁ？")
    line = re.sub(r"(?<!ん)ですぅ", "ですよぉ", line)
    line = line.replace("ますぅ", "ますよぉ")
    return line


def main() -> None:
    current = TARGET.read_text(encoding="cp932").splitlines()
    original_counts = Counter(BACKUP.read_text(encoding="cp932").splitlines())
    changed: list[tuple[str, str]] = []
    output: list[str] = []
    for line in current:
        if original_counts[line]:
            original_counts[line] -= 1
            output.append(line)
            continue
        new_line = normalize_dialogue(line)
        if new_line != line:
            changed.append((line, new_line))
        output.append(new_line)
    if not changed:
        raise RuntimeError("no newly authored line was normalized")
    TARGET.write_bytes("\r\n".join(output).encode("cp932") + b"\r\n")
    print(f"normalized {len(changed)} newly authored Chika lines")


if __name__ == "__main__":
    main()
