"""漢字語の吃り表現を読み辞書と照合する安全側の監査。

ひらがな＋「、」＋漢字を機械的に置換すると、通常の文の区切りまで壊すため、
読みが登録済みの語だけを検査し、修正表に登録した不一致だけを --fix で直す。
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


# 読みは「吃りで残る先頭の音」と照合するため、語頭部分だけ登録する。
KNOWN_READINGS = {
    "女の子": "おんな",
    "女の子同士": "おんな",
    "先輩": "せんぱい",
    "転校生": "てんこうせい",
    "何": "なに",
    "今日": "きょう",
    "一緒": "いっしょ",
    "二本": "にほん",
    "両方": "りょうほう",
    "乳首": "ちくび",
    "初めて": "はじめて",
}

# 自動修正は読みが確定したものだけに限定する。
CONFIRMED_REPAIRS = {
    "じょ、女の子": "お、女の子",
    "じょ、女の子同士": "お、女の子同士",
}

# 「あ、転校生」「ぼく、先輩」のような通常の文の区切りを、吃りと誤認しない。
# 読み不一致でも、これらは自動修正候補にしない。
NON_STUTTER_PREFIXES = {
    "あ", "あっ", "あぁ", "あの", "い", "う", "うう", "うっ", "え", "えっ", "えへ",
    "お", "か", "ここ", "これ", "それ", "た", "ちょ", "つ", "て", "でも", "と",
    "な", "なに", "ね", "ねぇ", "は", "ひゃ", "ふぁ", "ふふ", "へ", "ほ", "ぼく",
    "ま", "また", "み", "もう", "や", "よ", "り", "る", "れ", "わ", "ん", "んっ", "っ", "すき",
}


def audit(path: Path, fix: bool) -> int:
    raw = path.read_bytes()
    text = raw.decode("cp932")
    issues: list[tuple[int, str, str, str]] = []
    fixed = 0

    for line_number, line in enumerate(text.splitlines(), 1):
        for term, reading in sorted(KNOWN_READINGS.items(), key=lambda item: -len(item[0])):
            pattern = re.compile(rf"(?:^|[「『（\\s　。！？…～])(?P<prefix>[ぁ-んー]{{1,2}})、{re.escape(term)}")
            for match in pattern.finditer(line):
                prefix = match.group("prefix")
                if prefix in NON_STUTTER_PREFIXES:
                    continue
                if reading.startswith(prefix):
                    continue
                fragment = f"{prefix}、{term}"
                replacement = CONFIRMED_REPAIRS.get(fragment)
                issues.append((line_number, fragment, reading, replacement or "要目視"))

    if fix:
        new_text = text
        for before, after in CONFIRMED_REPAIRS.items():
            new_text = new_text.replace(before, after)
        if new_text != text:
            path.write_bytes(new_text.replace("\n", "\r\n").encode("cp932"))
            fixed = sum(text.count(before) for before in CONFIRMED_REPAIRS)

    print(f"対象: {path}")
    if issues:
        for line_number, fragment, reading, replacement in issues:
            print(f"[候補] {line_number}行目: {fragment} / 語頭読み={reading} / 対応={replacement}")
    else:
        print("[OK] 登録済み漢字語の吃り読み不一致なし")
    if fix:
        print(f"自動修正: {fixed}件")
    return len(issues)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()
    raise SystemExit(audit(args.path, args.fix) if not args.fix else 0)


if __name__ == "__main__":
    main()
