# -*- coding: utf-8 -*-
"""Differentiate default effects for unique commands COM280-284 / COM410-414."""
from pathlib import Path

SRC_NAME = {
    0: "快Ｃ", 1: "快Ｖ", 2: "快Ａ", 3: "情愛", 4: "性行動", 5: "達成感",
    6: "痛み", 7: "中毒充足", 8: "不潔", 9: "接触", 10: "液体追加",
    11: "欲情追加", 12: "露出", 13: "屈従", 14: "逸脱", 15: "反感追加",
    16: "恭順追加", 17: "快Ｂ", 18: "歓楽", 19: "家務", 20: "征服",
    21: "受動", 22: "懐疑", 23: "不安", 24: "快Ｍ",
}

# ウフフ: 5枠とも V性交処理は共通のまま。SOURCE/LOSEBASE だけ差分化。
UFUFU = {
    280: {
        "title": "バランス本番（基準）",
        "lose0": 200, "lose1": 400,
        "sources": {9: 5000, 18: 4000, 0: 3000, 1: 3000},
        "note": "接触・歓楽・快C/Vのバランス型。既存デフォルトに近い基準値。",
    },
    281: {
        "title": "快楽特化",
        "lose0": 220, "lose1": 450,
        "sources": {0: 4500, 1: 4500, 17: 3500, 9: 4000, 18: 3000, 11: 2000},
        "note": "快C/V/Bと欲情を厚く。気力消費多め。",
    },
    282: {
        "title": "背徳・露出",
        "lose0": 180, "lose1": 420,
        "sources": {12: 4500, 14: 3000, 23: 2500, 9: 3500, 0: 2500, 1: 2500, 18: 3500},
        "note": "露出・逸脱・不安を足し、接触/快感は控えめ。スリリング寄り。",
    },
    283: {
        "title": "情愛本番",
        "lose0": 160, "lose1": 350,
        "sources": {3: 5000, 18: 5000, 21: 3000, 9: 4000, 0: 2000, 1: 2500, 24: 2000},
        "note": "情愛・歓楽・受動を厚く。快感は控えめ、キス感(快M)を少し。",
    },
    284: {
        "title": "激しめ本番",
        "lose0": 280, "lose1": 500,
        "sources": {0: 4000, 1: 5000, 13: 3500, 20: 3000, 9: 4500, 18: 2500, 6: 1500},
        "note": "体力/気力消費大。快V強め＋屈従/征服＋軽い痛み。",
    },
}

# 純愛: キス経験は共通加算（414のみ+2）。SOURCE/LOSEBASE を差分化。
PURE = {
    410: {
        "title": "甘々デート（基準）",
        "lose0": 150, "lose1": 350,
        "sources": {3: 5000, 18: 4000, 9: 3000, 24: 2500, 21: 2000},
        "kiss": 1,
        "note": "情愛・歓楽中心の基準型。既存デフォルトに近い。",
    },
    411: {
        "title": "スキンシップ",
        "lose0": 120, "lose1": 300,
        "sources": {9: 5000, 21: 4000, 3: 3500, 18: 3000, 24: 2000},
        "kiss": 1,
        "note": "接触・受動を厚く。触れ合い重視。",
    },
    412: {
        "title": "褒め・承認",
        "lose0": 100, "lose1": 250,
        "sources": {5: 5000, 16: 4000, 3: 3500, 18: 3500, 21: 1500},
        "kiss": 1,
        "note": "達成感・恭順を厚く。認める・褒められるデート。",
    },
    413: {
        "title": "癒し",
        "lose0": 50, "lose1": 150,
        "sources": {3: 4000, 18: 4500, 21: 3500, 9: 2500, 24: 1500},
        "kiss": 1,
        "note": "体力/気力消費を抑え、情愛・歓楽・受動で癒す。",
    },
    414: {
        "title": "ディープキス",
        "lose0": 130, "lose1": 320,
        "sources": {24: 5500, 3: 3500, 9: 3500, 18: 3000, 21: 2000},
        "kiss": 2,
        "note": "快M最大。キス経験+2。",
    },
}


def build_source_block(sources: dict) -> str:
    lines = []
    for k in sorted(sources.keys()):
        lines.append(f"SOURCE:{k} = {sources[k]}\t;{SRC_NAME.get(k, '?')}")
    return "\n".join(lines)


def write_cp932(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(text.replace("\n", "\r\n").encode("cp932"))


def patch_ufufu(n: int, spec: dict) -> bool:
    path = Path(f"ERB/COMF/COMF{n}.ERB")
    text = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    old = (
        "CALL TRAIN_MESSAGE_B\n"
        ";デフォルト効果（独自ウフフ共通・キャラ個別関数で上書き可能）\n"
        "LOSEBASE:0 += 200\n"
        "LOSEBASE:1 += 400\n"
        "SOURCE:9 = 5000\n"
        "SOURCE:18 = 4000\n"
        "SOURCE:0 = 3000\n"
        "SOURCE:1 = 3000\n"
        ";キャラ固有処理（ソース上書き等）\n"
        f"TRYCALLFORM COM{n}_" + "{NO:TARGET}"
    )
    src = build_source_block(spec["sources"])
    new = (
        "CALL TRAIN_MESSAGE_B\n"
        f";デフォルト効果（独自ウフフ COM{n}：{spec['title']}）\n"
        f";{spec['note']}\n"
        f";キャラ個別で上書きする場合は COM{n}_<NO> で SOURCE/LOSEBASE を再設定\n"
        f"LOSEBASE:0 += {spec['lose0']}\t;体力\n"
        f"LOSEBASE:1 += {spec['lose1']}\t;気力\n"
        f"{src}\n"
        ";キャラ固有処理（ソース上書き等）\n"
        f"TRYCALLFORM COM{n}_" + "{NO:TARGET}"
    )
    if old not in text:
        print(f"FAIL COM{n}: old block not found")
        idx = text.find("CALL TRAIN_MESSAGE_B")
        print(repr(text[idx:idx + 280]))
        return False
    write_cp932(path, text.replace(old, new, 1))
    print(f"OK COM{n} {spec['title']}")
    return True


def patch_pure(n: int, spec: dict) -> bool:
    path = Path(f"ERB/COMF/COMF{n}.ERB")
    text = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    old = (
        "CALL TRAIN_MESSAGE_B\n"
        ";デフォルト効果（独自純愛共通・キャラ個別関数で上書き可能）\n"
        "LOSEBASE:0 += 150\n"
        "LOSEBASE:1 += 350\n"
        "SOURCE:3 = 5000\n"
        "SOURCE:18 = 4000\n"
        "SOURCE:9 = 3000\n"
        "SOURCE:24 = 2500\n"
        "SOURCE:21 = 2000\n"
        ";キス経験を加算\n"
        "PRINTFORML %EXPNAME:96%＋１\n"
        "EXP:96 += 1\n"
        "EXP:PLAYER:96 += 1\n"
        ";キャラ固有処理（ソース上書き等）\n"
        f"TRYCALLFORM COM{n}_" + "{NO:TARGET}"
    )
    src = build_source_block(spec["sources"])
    kiss = spec["kiss"]
    if kiss == 1:
        kiss_block = (
            ";キス経験を加算\n"
            "PRINTFORML %EXPNAME:96%＋１\n"
            "EXP:96 += 1\n"
            "EXP:PLAYER:96 += 1"
        )
    else:
        # 表示は全角数字で既存の「＋１」表記に合わせる
        kiss_disp = "２" if kiss == 2 else str(kiss)
        kiss_block = (
            f";キス経験を加算（{spec['title']}）\n"
            f"PRINTFORML %EXPNAME:96%＋{kiss_disp}\n"
            f"EXP:96 += {kiss}\n"
            f"EXP:PLAYER:96 += {kiss}"
        )
    new = (
        "CALL TRAIN_MESSAGE_B\n"
        f";デフォルト効果（独自純愛 COM{n}：{spec['title']}）\n"
        f";{spec['note']}\n"
        f";キャラ個別で上書きする場合は COM{n}_<NO> で SOURCE/LOSEBASE を再設定\n"
        f"LOSEBASE:0 += {spec['lose0']}\t;体力\n"
        f"LOSEBASE:1 += {spec['lose1']}\t;気力\n"
        f"{src}\n"
        f"{kiss_block}\n"
        ";キャラ固有処理（ソース上書き等）\n"
        f"TRYCALLFORM COM{n}_" + "{NO:TARGET}"
    )
    if old not in text:
        print(f"FAIL COM{n}: old block not found")
        idx = text.find("CALL TRAIN_MESSAGE_B")
        print(repr(text[idx:idx + 350]))
        return False
    write_cp932(path, text.replace(old, new, 1))
    print(f"OK COM{n} {spec['title']} kiss+{kiss}")
    return True


def main() -> None:
    ok = True
    for n, s in UFUFU.items():
        ok = patch_ufufu(n, s) and ok
    for n, s in PURE.items():
        ok = patch_pure(n, s) and ok
    print("ALL OK" if ok else "SOME FAILED")


if __name__ == "__main__":
    main()
