from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_36_遠見ちか_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR36_before_rand3_and_additional10_20260810" / "CHAR_36_遠見ちか_COM.ERB"

REPLACEMENTS = {
    "手伝ってあげたくなるですよぉ♪": "手伝ってあげたくなるんですよぉ♪",
    "反応が返ってくるですよぉ。": "反応が返ってくるんですよぉ。",
    "変な気分になるですよぉ。": "変な気分になるんですよぉ。",
    "効率がよくなるですよぉ♪": "効率がよくなるんですよぉ♪",
    "まだ拍手が聞こえるですぅ。": "まだ拍手が聞こえるんですぅ。",
    "暗い水槽の前って落ち着くですねぇ。": "暗い水槽の前って、落ち着くんですねぇ。",
    "いつもより近く見えるですよぉ……": "いつもより近く見えるんですよぉ……",
    "嬉しくなるですぅ。": "嬉しくなるんですぅ。",
    "%LOCALS%と重なると、熱がゆっくり返ってくるですぅ……": "%LOCALS%と重なると、熱がゆっくり返ってくるんですぅ……",
    "いっぱいになってるですぅ。": "いっぱいになってるんですぅ。",
    "身体の奥までヘルプマンの気配が続くですねぇ……": "身体の奥までヘルプマンの気配が続くんですねぇ……",
    "胸が擦れるたび、%LOCALS%の息が返ってくるですぅ。": "胸が擦れるたび、%LOCALS%の息が返ってくるんですぅ。",
    "あぅ、%LOCALS%の動きがわたしの奥にも返ってくるですぅ。": "あぅ、%LOCALS%の動きがわたしの奥にも返ってくるんですぅ。",
    "声が止まらないですぅ。": "声が止まらないんですぅ。",
    "息が細くなるですぅ。": "息が細くなるんですぅ。",
    "また強くなったですぅ……": "また強くなったんですぅ……",
    "声が変になるですぅ。": "声が変になるんですぅ。",
    "ぬ、抜けたですぅ……！": "ぬ、抜けたんですぅ……！",
    "仕組みがあるですぅ♪": "仕組みがあるんですぅ♪",
    "舌が触れたですぅ……！": "舌が触れたんですぅ……！",
    "震えも揃いそうですぅ♪": "震えも揃いそうですねぇ♪",
    "胸まで熱くなるですぅ。": "胸まで熱くなるんですぅ。",
    "声が途切れるですぅ……": "声が途切れるんですぅ……",
    "な、何ですかぁこれっ、止まらないですよぉ！　わたしの身体なのに、勝手なことしないでくださいぃ！": "な、何ですかぁこれっ、止まらないんですよぉ！　わたしの身体なのに、勝手なことしないでくださいぃ！",
    "眠くなるですねぇ。": "眠くなるんですねぇ。",
}


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
        new_line = line
        for old, new in REPLACEMENTS.items():
            new_line = new_line.replace(old, new)
        if new_line != line:
            changed.append((line, new_line))
        output.append(new_line)
    if len(changed) != 25:
        raise RuntimeError(f"expected 25 new lines to be polished, got {len(changed)}")
    TARGET.write_bytes("\r\n".join(output).encode("cp932") + b"\r\n")
    print(f"polished {len(changed)} newly authored sentence endings")


if __name__ == "__main__":
    main()
