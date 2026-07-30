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
from collections import defaultdict
from pathlib import Path

CARD_CSV = Path("card_data.csv")
OUT_CSV  = Path("../CSV/Card.csv")
OUT_ERB  = Path("../ERB/CARD_DATA_カードデータ定義.ERB")

# レア度 → ボーナス値
# 1=N, 2=R, 3=HR, 4=SR, 5=UR, 6=MR
RARITY_BONUS = {1: 8, 2: 20, 3: 36, 4: 60, 5: 100, 6: 160}
RARITY_LABEL = {1:"N", 2:"R", 3:"HR", 4:"SR", 5:"UR", 6:"MR"}

SPORTS = {"ラクロス","バレー","バスケ","サッカー","テニス","陸上","体操","水泳","剣道","空手",
          "柔道","ソフトボール","卓球","アーチェリー","弓道","バドミントン"}
ARTS   = {"吹奏楽","演劇","合唱","軽音","美術","写真","放送","ダンス","文芸"}
STUDY  = {"科学","数学","化学","天文","囲碁","将棋","料理研究","茶道","書道","生物"}


def load_cards():
    if not CARD_CSV.exists():
        print(f"ERROR: {CARD_CSV} が見つかりません。先に scrape_cards.py を実行してください。")
        return []
    with open(CARD_CSV, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def get_card_id(card):
    return int(card.get("id") or card["card_id"])


def get_card_character_name(card):
    if card.get("char_name"):
        return card["char_name"].strip()
    # 現行card_data.csvは「[衣装名]キャラ名」のcard_nameとchar_noを持つ。
    return card["card_name"].rsplit("]", 1)[-1].strip()


def build_char_id_map(cards):
    """CharaNN_名前.csv のファイル名からキャラNo（CSV番号）を取得する"""
    import re
    chara_dir = Path("../CSV")
    name_to_id = {}
    for p in chara_dir.glob("Chara*.csv"):
        m = re.match(r"Chara(\d+)_(.+)\.csv", p.name)
        if m:
            csv_no = int(m.group(1))
            char_name = m.group(2)
            name_to_id[char_name] = csv_no
    if not name_to_id:
        # フォールバック: character_data.csv の行番号を使う
        char_data = Path("character_data.csv")
        if char_data.exists():
            with open(char_data, encoding="utf-8-sig") as f:
                for i, row in enumerate(csv.DictReader(f), 1):
                    name = row.get("name", "").strip()
                    if name:
                        name_to_id[name] = i
        else:
            names = list(dict.fromkeys(get_card_character_name(c) for c in cards))
            name_to_id = {n: i for i, n in enumerate(names, 1)}
    return name_to_id


def build_bonus_type_map():
    char_data = Path("character_data.csv")
    name_to_bonus = {}
    if char_data.exists():
        with open(char_data, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                name = row.get("name", "").strip()
                club = row.get("club", "")
                btype = 3
                for s in SPORTS:
                    if s in club: btype = 1; break
                else:
                    for a in ARTS:
                        if a in club: btype = 0; break
                    else:
                        for st in STUDY:
                            if st in club: btype = 2; break
                if name:
                    name_to_bonus[name] = btype
    # 現行card_data.csvはキャラ名列を持たないため、CSV番号でも引けるようにする。
    import re
    for path in Path("../CSV").glob("Chara*.csv"):
        match = re.match(r"Chara(\d+)_(.+)\.csv", path.name)
        if match and match.group(2) in name_to_bonus:
            name_to_bonus[int(match.group(1))] = name_to_bonus[match.group(2)]
    return name_to_bonus


def write_era_csv(cards):
    lines = [f"{get_card_id(c)},{c['card_name']}" for c in cards]
    with open(OUT_CSV, "w", encoding="cp932", newline="\r\n") as f:
        f.write(";カードID,カード名\n")
        f.write("\n".join(lines) + "\n")
    print(f"出力: {OUT_CSV} ({len(lines)}件)")


def write_era_erb(cards, char_map, bonus_map=None):
    if bonus_map is None:
        bonus_map = {}

    # データ構造を構築
    card_info = {}        # card_seq_id → (char_id, rarity, btype, bval)
    chars_by_rarity = defaultdict(list)          # rarity → [char_id, ...]（重複なし・ソート済み）
    cards_by_char_rarity = defaultdict(list)     # (char_id, rarity) → [card_seq_id, ...]

    for c in cards:
        cid     = get_card_id(c)
        char_name = get_card_character_name(c)
        char_id = int(c["char_no"]) if c.get("char_no") else char_map.get(char_name, 0)
        rarity  = int(c["rarity"])
        btype   = (int(c["bonus_type"]) if "bonus_type" in c and c.get("bonus_type","") != ""
                   else bonus_map.get(char_id, bonus_map.get(char_name, 3)))
        bval    = RARITY_BONUS.get(rarity, 2)
        card_name = c.get("card_name", char_name)
        card_info[cid] = (char_id, rarity, btype, bval, card_name)
        if char_id > 0:
            cards_by_char_rarity[(char_id, rarity)].append(cid)
            if char_id not in chars_by_rarity[rarity]:
                chars_by_rarity[rarity].append(char_id)

    for r in chars_by_rarity:
        chars_by_rarity[r].sort()

    L = []  # ERB行リスト

    # ヘッダー
    L += [
        ";==================================================",
        "; CARD_DATA_カードデータ定義.ERB  (自動生成 - 編集不要)",
        ";",
        "; @CARD_GET_DATA      ARG:0=カードID → RESULT:0-3",
        "; @CARD_GET_CHARS_FOR_RARITY  ARG:0=レア度",
        ";   → LOCAL:0..N-1=キャラNoリスト, LOCAL:9=件数",
        "; @CARD_GET_CHARPOOL  ARG:0=キャラNo ARG:1=レア度（完全一致）",
        ";   → LOCAL:0..N-1=カードIDリスト, LOCAL:9=件数",
        ";==================================================",
        "",
    ]

    # @CARD_GET_DATA
    L += [
        "@CARD_GET_DATA(ARG)",
        ";ARG:0=カードID -> RESULT:1=キャラNo RESULT:2=レア RESULT:3=ボーナスタイプ RESULT:4=ボーナス値",
        ";              -> STR:0=カード名",
        ";注意: RETURN N が RESULT:0 を上書きするため、データはRESULT:1以降に格納",
        "RESULT:1 = 0",
        "RESULT:2 = 0",
        "RESULT:3 = 0",
        "RESULT:4 = 0",
        "STR:0 =",
        f"IF ARG:0 < 1 || ARG:0 > {len(cards)}",
        "\tRETURN 0",
        "ENDIF",
        "SELECTCASE ARG:0",
    ]
    for cid in sorted(card_info):
        char_id, rarity, btype, bval, card_name = card_info[cid]
        L.append(f"CASE {cid}")
        L.append(f"\tRESULT:1 = {char_id}")
        L.append(f"\tRESULT:2 = {rarity}")
        L.append(f"\tRESULT:3 = {btype}")
        L.append(f"\tRESULT:4 = {bval}")
        L.append(f"\tSTR:0 = {card_name}")
    L += ["ENDSELECT", "RETURN 1", ""]

    # @CARD_GET_CHARS_FOR_RARITY  （静的配列 — 高速）
    L += [
        ";--------------------------------------------------",
        "; @CARD_GET_CHARS_FOR_RARITY ARG:0=レア度(1-6)",
        "; そのレア度のカードを持つキャラNo一覧を返す",
        "; GLOBAL:2001..N=キャラNoリスト  GLOBAL:2000=件数",
        ";--------------------------------------------------",
        "@CARD_GET_CHARS_FOR_RARITY(ARG)",
        "LOCAL:9 = 0",
        "SELECTCASE ARG:0",
    ]
    for rarity in sorted(chars_by_rarity):
        char_list = chars_by_rarity[rarity]
        L.append(f"CASE {rarity}  ;{RARITY_LABEL.get(rarity, str(rarity))}: {len(char_list)}人")
        for i, cid in enumerate(char_list):
            L.append(f"\tGLOBAL:{2001 + i} = {cid}")
        L.append(f"\tGLOBAL:2000 = {len(char_list)}")
    L += ["ENDSELECT", "RETURN GLOBAL:2000", ""]

    # @CARD_GET_CHARPOOL  （静的配列 — 高速）
    L += [
        ";--------------------------------------------------",
        "; @CARD_GET_CHARPOOL ARG:0=キャラNo ARG:1=レア度（完全一致）",
        "; そのキャラのそのレア度のカードID一覧を返す",
        "; GLOBAL:2101..N=カードIDリスト  GLOBAL:2100=件数",
        ";--------------------------------------------------",
        "@CARD_GET_CHARPOOL(ARG, ARG:1)",
        "GLOBAL:2100 = 0",
        "SELECTCASE ARG:0",
    ]
    all_chars = sorted(set(k[0] for k in cards_by_char_rarity))
    for char_id in all_chars:
        rarities_for_char = sorted(k[1] for k in cards_by_char_rarity if k[0] == char_id)
        L.append(f"CASE {char_id}")
        L.append(f"\tSELECTCASE ARG:1")
        for rarity in rarities_for_char:
            pool = cards_by_char_rarity[(char_id, rarity)]
            L.append(f"\tCASE {rarity}  ;{RARITY_LABEL.get(rarity,'?')}: {len(pool)}枚")
            for i, card_seq in enumerate(pool):
                L.append(f"\t\tGLOBAL:{2101 + i} = {card_seq}")
            L.append(f"\t\tGLOBAL:2100 = {len(pool)}")
        L.append(f"\tENDSELECT")
    L += ["ENDSELECT", "RETURN GLOBAL:2100", ""]

    # 統計コメント
    total_combos = len(cards_by_char_rarity)
    L.insert(1, f"; 総カード数: {len(cards)}  キャラ数: {len(all_chars)}  (キャラ×レア)組合せ数: {total_combos}")

    text = "\r\n".join(L) + "\r\n"
    with open(OUT_ERB, "w", encoding="cp932", newline="") as f:
        f.write(text)
    print(f"出力: {OUT_ERB}  ({len(cards)}カード, {len(all_chars)}キャラ, {total_combos}プール)")

    # デバッグ: レア度×キャラ数の表
    print("\nレア度別キャラ数:")
    for r in sorted(chars_by_rarity):
        print(f"  {RARITY_LABEL.get(r,r)}: {len(chars_by_rarity[r])}人")


def update_card_count_limits(total):
    """SHOP.ERBとCARD_COLLECTION.ERBのハードコードされたカード上限を更新する"""
    import re
    targets = [
        (Path("../ERB/SHOP_ショップ.ERB"),
         r"IF LOCAL:5 > \d+\n\tGOTO CHAR_CARD_END",
         f"IF LOCAL:5 > {total}\n\tGOTO CHAR_CARD_END"),
        (Path("../ERB/CARD_COLLECTION_カードコレクション.ERB"),
         r"IF LOCAL:5 > \d+\n\tGOTO LIST_END",
         f"IF LOCAL:5 > {total}\n\tGOTO LIST_END"),
    ]
    for path, pattern, replacement in targets:
        if not path.exists():
            continue
        with open(path, "rb") as f:
            content = f.read().decode("cp932").replace("\r\n", "\n")
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            with open(path, "wb") as f:
                f.write(new_content.replace("\n", "\r\n").encode("cp932"))
            print(f"カード上限を{total}に更新: {path.name}")


def main():
    print("=== ERA カードデータ生成 ===\n")
    cards = load_cards()
    if not cards:
        return
    char_map  = build_char_id_map(cards)
    bonus_map = build_bonus_type_map()
    print(f"カード数: {len(cards)}, キャラ数: {len(set(int(c['char_no']) for c in cards))}")
    write_era_csv(cards)
    write_era_erb(cards, char_map, bonus_map)
    update_card_count_limits(len(cards))
    print("\n完了。")


if __name__ == "__main__":
    main()
