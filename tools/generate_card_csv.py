#!/usr/bin/env python3
"""
card_data.csv から ERA用の CSV/Card.csv と ERB/CARD_DATA_カードデータ定義.ERB を生成する

使い方:
  cd tools
  python generate_card_csv.py

入力: tools/card_data.csv
出力:
  ../CSV/Card.csv            (カード名表示用)
  ../ERB/CARD_DATA_カードデータ定義.ERB  (ゲームロジック用)
"""

import csv
from pathlib import Path

CARD_CSV  = Path("card_data.csv")
OUT_CSV   = Path("../CSV/Card.csv")
OUT_ERB   = Path("../ERB/CARD_DATA_カードデータ定義.ERB")

# ボーナスタイプ → 補正説明
BONUS_TYPE_NAME = {0: "表現力", 1: "運動力", 2: "学力", 3: "好感度"}

# レア度 → ボーナス値
RARITY_BONUS = {1: 2, 2: 5, 3: 12, 4: 22, 5: 35}

# キャラ名 → ERA キャラNo. (CSV/Chara*.csv の番号に対応)
# scrape_chardata.py で取得したキャラ順に合わせて調整が必要
CHAR_NAME_TO_ID = {}  # 空のまま自動生成


def load_cards() -> list[dict]:
    if not CARD_CSV.exists():
        print(f"ERROR: {CARD_CSV} が見つかりません。先に scrape_cards.py を実行してください。")
        return []
    with open(CARD_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_char_id_map(cards: list[dict]) -> dict[str, int]:
    """キャラ名 → ERA番号 マップを生成"""
    char_data = Path("character_data.csv")
    name_to_id = {}
    if char_data.exists():
        with open(char_data, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                name = row.get("name", "").strip()
                if name:
                    name_to_id[name] = i
    else:
        names = list(dict.fromkeys(c["char_name"] for c in cards))
        name_to_id = {n: i for i, n in enumerate(names, 1)}
    return name_to_id


def build_bonus_type_map() -> dict[str, int]:
    """キャラ名 → ボーナスタイプ（部活から推定）"""
    char_data = Path("character_data.csv")
    SPORTS = {"ラクロス","バレー","バスケ","サッカー","テニス","陸上","体操","水泳","剣道","柔道","ソフトボール","卓球","アーチェリー","弓道","バドミントン"}
    ARTS   = {"吹奏楽","演劇","合唱","軽音","美術","写真","放送","ダンス","文芸"}
    STUDY  = {"科学","数学","化学","天文","囲碁","将棋","料理研究","茶道","書道","生物"}
    name_to_bonus = {}
    if char_data.exists():
        with open(char_data, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                name = row.get("name","").strip()
                club = row.get("club","")
                btype = 3  # デフォルト：好感度
                for s in SPORTS:
                    if s in club:
                        btype = 1; break
                else:
                    for a in ARTS:
                        if a in club:
                            btype = 0; break
                    else:
                        for st in STUDY:
                            if st in club:
                                btype = 2; break
                if name:
                    name_to_bonus[name] = btype
    return name_to_bonus


def write_era_csv(cards: list[dict]):
    """CSV/Card.csv: ERA カード名表示用"""
    lines = []
    for c in cards:
        cid  = int(c["id"])
        name = c["card_name"]
        # ERBのCSVNAME:カードID = カード名
        lines.append(f"{cid},{name}")

    with open(OUT_CSV, "w", encoding="cp932", newline="\r\n") as f:
        f.write(";カードID,カード名\n")
        f.write("\n".join(lines) + "\n")
    print(f"出力: {OUT_CSV} ({len(lines)}件)")


def write_era_erb(cards: list[dict], char_map: dict[str, int], bonus_map: dict[str, int] = None):
    if bonus_map is None:
        bonus_map = {}
    """ERB/CARD_DATA_カードデータ定義.ERB: カードデータ取得関数"""
    lines = [
        ";==================================================",
        "; CARD_DATA_カードデータ定義.ERB",
        "; カードの静的データ定義",
        ";",
        "; @CARD_GET_DATA ARG:0=カードID",
        ";   RESULT:0 = キャラNo",
        ";   RESULT:1 = レア度(1-5)",
        ";   RESULT:2 = ボーナスタイプ(0=表現/1=運動/2=学力/3=好感度)",
        ";   RESULT:3 = ボーナス値",
        ";==================================================",
        "",
        "@CARD_GET_DATA",
        ";ARG:0=カードID -> RESULT:0-3",
        "RESULT:0 = 0",
        "RESULT:1 = 0",
        "RESULT:2 = 0",
        "RESULT:3 = 0",
        f"IF ARG:0 < 1 || ARG:0 > {len(cards)}",
        "\tRETURN 0",
        "ENDIF",
        "SELECTCASE ARG:0",
    ]

    for c in cards:
        cid      = int(c["id"])
        char_id  = char_map.get(c["char_name"], 0)
        rarity   = int(c["rarity"])
        btype    = int(c["bonus_type"]) if "bonus_type" in c and c["bonus_type"] != "" else bonus_map.get(c["char_name"], hash(c["char_name"]) % 4)
        bval     = RARITY_BONUS.get(rarity, 2)
        lines.append(f"CASE {cid}")
        lines.append(f"\tRESULT:0 = {char_id}")
        lines.append(f"\tRESULT:1 = {rarity}")
        lines.append(f"\tRESULT:2 = {btype}")
        lines.append(f"\tRESULT:3 = {bval}")

    lines += [
        "ENDSELECT",
        "RETURN 1",
        "",
        ";--------------------------------------------------",
        "; @CARD_GET_CHARPOOL ARG:0=キャラNo ARG:1=最小レア度",
        "; そのキャラの指定レア度以上のカードIDリストを",
        "; LOCAL:0-N に格納して LOCAL:9 に件数を返す",
        ";--------------------------------------------------",
        "@CARD_GET_CHARPOOL",
        "LOCAL:9 = 0",
    ]

    # キャラ別カードプール
    from collections import defaultdict
    char_cards = defaultdict(list)
    for c in cards:
        cid     = int(c["id"])
        char_id = char_map.get(c["char_name"], 0)
        rarity  = int(c["rarity"])
        char_cards[(char_id, rarity)].append(cid)

    lines.append(f"FOR LOCAL:8, 0, {len(cards)}")
    lines.append("\tCALL CARD_GET_DATA, LOCAL:8 + 1")
    lines.append("\tIF RESULT:0 == ARG:0 && RESULT:1 >= ARG:1")
    lines.append("\t\tLOCAL:LOCAL:9 = LOCAL:8 + 1")
    lines.append("\t\tLOCAL:9 += 1")
    lines.append("\tENDIF")
    lines.append("NEXT")
    lines.append("RETURN LOCAL:9")
    lines.append("")

    # ERB書き出し (cp932 + CRLF)
    text = "\r\n".join(lines) + "\r\n"
    with open(OUT_ERB, "w", encoding="cp932", newline="") as f:
        f.write(text)
    print(f"出力: {OUT_ERB} ({len(cards)}カード定義)")


def main():
    print("=== ERA カードデータ生成 ===\n")
    cards = load_cards()
    if not cards:
        return

    char_map  = build_char_id_map(cards)
    bonus_map = build_bonus_type_map()
    print(f"カード数: {len(cards)}, キャラ数: {len(set(c['char_name'] for c in cards))}")

    write_era_csv(cards)
    write_era_erb(cards, char_map, bonus_map)
    print("\n完了。generate後にgit add/commit/pushしてください。")


if __name__ == "__main__":
    main()
