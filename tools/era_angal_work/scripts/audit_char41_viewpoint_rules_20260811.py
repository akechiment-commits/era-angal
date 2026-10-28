"""CHAR41で行為者と対象者が反転しやすいコマンドの視点契約を監査する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_41_悠木ともこ_COM.ERB"


RULES = {
    37: {
        "required": ["キャラ奉仕", "キャラが足でプレイヤーを扱く"],
        "forbidden": ["転校生さんの足", "転校生さんを足で"],
    },
    67: {
        "required": ["キャラ受け", "プレイヤーがふたなりのキャラに足コキ", "転校生さんの足", "わたしのものを足で"],
        "forbidden": ["わたしの足を", "足さばき", "足の置き場", "足元ばかり"],
    },
    66: {
        "required": ["AITE_YOBI, 41, ASSI", "転校生さんと%CALLNAME:ASSI%"],
        "forbidden": [],
    },
    130: {
        "required": ["転校生さんに目隠し"],
        "forbidden": [],
    },
    131: {
        "required": ["転校生さんを縛", "転校生さんを拘束"],
        "forbidden": [],
    },
    132: {
        "required": ["声が出せない転校生さん"],
        "forbidden": [],
    },
    258: {
        "required": ["転校生さんに跨がるわたしの下", "%LOCALS%が転校生さんの顔"],
        "forbidden": ["わたしの顔の下"],
    },
}


def block_text(lines: list[str], command: int) -> str:
    starts = [i for i, line in enumerate(lines) if line.strip() == f"IF SELECTCOM == {command}"]
    if len(starts) != 1:
        raise RuntimeError(f"COM{command}の開始位置が一意ではありません: {len(starts)}件")
    if_start = starts[0]
    start = next(
        (i for i in range(if_start - 1, -1, -1) if lines[i].startswith(f";--- COM{command} ")),
        if_start,
    )
    end = next(
        (i for i in range(if_start + 1, len(lines)) if lines[i].strip().startswith("IF SELECTCOM == ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def main() -> None:
    text = COM_PATH.read_bytes().decode("cp932")
    lines = text.splitlines()
    errors: list[str] = []
    for command, rule in RULES.items():
        block = block_text(lines, command)
        for phrase in rule["required"]:
            if phrase not in block:
                errors.append(f"COM{command}: 必須視点語がない: {phrase}")
        for phrase in rule["forbidden"]:
            if phrase in block:
                errors.append(f"COM{command}: 禁止視点語が残っている: {phrase}")
    if errors:
        raise SystemExit("視点契約違反\n" + "\n".join(errors))
    print(f"CHAR41視点契約: OK ({len(RULES)}コマンド)")


if __name__ == "__main__":
    main()
