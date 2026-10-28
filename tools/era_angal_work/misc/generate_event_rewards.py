#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_event_rewards.py
@LOAD_EVENT_REWARDS の全CASEブロックを生成してERBに書き込む

入力:
  tools/event_card_list.txt  (UTF-8)
  tools/card_data.csv        (UTF-8-BOM)
  ERB/EVENT_BOARD_DATA_イベントデータ.ERB  (cp932) ← 月/イベント定義を読む

出力:
  ERB/EVENT_BOARD_DATA_イベントデータ.ERB の @LOAD_EVENT_REWARDS を全上書き
"""

import re
import csv
import unicodedata

def nfc(s):
    return unicodedata.normalize('NFC', s)

CARD_LIST_PATH = 'tools/event_card_list.txt'
CARD_DATA_PATH = 'tools/card_data.csv'
ERB_PATH = 'ERB/EVENT_BOARD_DATA_イベントデータ.ERB'

RARITY_LABEL = {1: 'N', 2: 'R', 3: 'HR', 4: 'SR', 5: 'UR', 6: 'MR'}

# ===== PT シーケンス (60段階) =====
PT_SEQ = [
     200,  400,  700, 1000, 1300, 1600, 1900, 2200, 2500, 2800,  # 0-9
    3100, 3500, 3900, 4300, 4700, 5100, 5500, 5900, 6200, 6500,  # 10-19
    6800, 7100, 7400, 7700, 8000, 8300, 8600, 8900, 9200, 9500,  # 20-29
    9800, 10100, 10300, 10500, 10700, 11000, 11300, 11600, 12000, 12400,  # 30-39
   12800, 13200, 13500, 13800, 14100, 14400, 14700, 15000, 15400, 15800,  # 40-49
   16200, 16600, 17000, 17300, 17600, 17900, 18200, 18600, 19300, 20000,  # 50-59
]

# ===== カードスロット位置 (枚数→tier index リスト) =====
CARD_SLOTS = {
    7: [4, 11, 22, 33, 40, 47, 59],
    6: [4, 11, 22, 33, 47, 59],
    5: [11, 22, 33, 47, 59],
    4: [22, 33, 47, 59],
    3: [22, 47, 59],
    2: [33, 59],
    1: [59],
    0: [],
}

# ===== 非カードtierのデフォルトアイテム (tier index → (type, value, comment)) =====
# type: 1=おにぎり 2=カレー 3=ドーナツ 4=パフェ 5=ブロンズ 6=シルバー 7=ゴールド 8=ダイヤ 10=お弁当
# 12=ミルク(好感度+50) 13=キャンディ(好感度+200) 14=ケーキ(好感度+2000) 15=キミサキブースター
BASE = [
    (1,  3,  'おにぎり×3'),          #  0  200PT
    (3,  2,  'ドーナツ×2'),          #  1  400PT
    (2,  1,  'カレー×1'),            #  2  700PT
    (5,  1,  'ブロンズ×1'),          #  3  1000PT
    (5,  1,  'ブロンズ×1'),          #  4  1300PT  [card slot]
    (8,  5,  'ダイヤ×5'),            #  5  1600PT
    (12, 1,  'ミルク×1'),            #  6  1900PT  ← ミルク①
    (1,  5,  'おにぎり×5'),          #  7  2200PT
    (3,  3,  'ドーナツ×3'),          #  8  2500PT
    (5,  2,  'ブロンズ×2'),          #  9  2800PT
    (2,  2,  'カレー×2'),            # 10  3100PT
    (6,  1,  'シルバー×1'),          # 11  3500PT  [card slot]
    (8, 10,  'ダイヤ×10'),           # 12  3900PT
    (4,  1,  'パフェ×1'),            # 13  4300PT
    (1,  8,  'おにぎり×8'),          # 14  4700PT
    (12, 1,  'ミルク×1'),            # 15  5100PT  ← ミルク②
    (6,  1,  'シルバー×1'),          # 16  5500PT
    (8, 15,  'ダイヤ×15'),           # 17  5900PT
    (2,  3,  'カレー×3'),            # 18  6200PT
    (3,  5,  'ドーナツ×5'),          # 19  6500PT
    (5,  3,  'ブロンズ×3'),          # 20  6800PT
    (6,  1,  'シルバー×1'),          # 21  7100PT
    (6,  1,  'シルバー×1'),          # 22  7400PT  [card slot]
    (8, 20,  'ダイヤ×20'),           # 23  7700PT
    (6,  2,  'シルバー×2'),          # 24  8000PT
    (10, 1,  'お弁当×1'),            # 25  8300PT
    (7,  1,  'ゴールド×1'),          # 26  8600PT
    (12, 1,  'ミルク×1'),            # 27  8900PT  ← ミルク③
    (8, 25,  'ダイヤ×25'),           # 28  9200PT
    (6,  2,  'シルバー×2'),          # 29  9500PT
    (2,  4,  'カレー×4'),            # 30  9800PT
    (3,  8,  'ドーナツ×8'),          # 31  10100PT
    (6,  3,  'シルバー×3'),          # 32  10300PT
    (7,  1,  'ゴールド×1'),          # 33  10500PT  [card slot]
    (7,  1,  'ゴールド×1'),          # 34  10700PT
    (13, 1,  'キャンディ×1'),        # 35  11000PT  ← キャンディ①
    (7,  1,  'ゴールド×1'),          # 36  11300PT
    (8, 20,  'ダイヤ×20'),           # 37  11600PT
    (5,  5,  'ブロンズ×5'),          # 38  12000PT
    (6,  3,  'シルバー×3'),          # 39  12400PT
    (7,  2,  'ゴールド×2'),          # 40  12800PT  [card slot]
    (8, 25,  'ダイヤ×25'),           # 41  13200PT
    (6,  4,  'シルバー×4'),          # 42  13500PT
    (2,  2,  'カレー×2'),            # 43  13800PT
    (12, 1,  'ミルク×1'),            # 44  14100PT  ← ミルク④
    (8, 30,  'ダイヤ×30'),           # 45  14400PT
    (6,  5,  'シルバー×5'),          # 46  14700PT
    (7,  2,  'ゴールド×2'),          # 47  15000PT  [card slot]
    (1,  5,  'おにぎり×5'),          # 48  15400PT
    (13, 1,  'キャンディ×1'),        # 49  15800PT  ← キャンディ②
    (8, 30,  'ダイヤ×30'),           # 50  16200PT
    (6,  5,  'シルバー×5'),          # 51  16600PT
    (7,  3,  'ゴールド×3'),          # 52  17000PT
    (8, 35,  'ダイヤ×35'),           # 53  17300PT
    (3,  5,  'ドーナツ×5'),          # 54  17600PT
    (14, 1,  'ケーキ×1'),            # 55  17900PT  ← ケーキ(好感度+2000)
    (7,  3,  'ゴールド×3'),          # 56  18200PT
    (15, 1,  'キミサキブースター×1'), # 57  18600PT  ← キミサキブースター(1ループ1個)
    (8, 40,  'ダイヤ×40'),           # 58  19300PT
    (7,  3,  'ゴールド×3'),          # 59  20000PT  [card slot]
]

# ===== card_data.csv 読み込み =====
card_db = {}  # "[カード名]キャラ名" → (id, rarity)
with open(CARD_DATA_PATH, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        card_db[row['card_name']] = (int(row['card_id']), int(row['rarity']))

# ===== event_card_list.txt 読み込み =====
# full_event_name → [(card_id, rarity, card_str), ...]
event_cards = {}
cur_name = None
cur_cards = []

with open(CARD_LIST_PATH, encoding='utf-8') as f:
    for raw_line in f:
        line = raw_line.rstrip('\n')
        stripped = line.strip()
        if not stripped:
            if cur_name is not None:
                event_cards[cur_name] = cur_cards
            cur_name = None
            cur_cards = []
        elif line.startswith('  ') or line.startswith('\t'):
            # カード行: 先頭が空白
            card_str = stripped
            if card_str in card_db:
                cid, rarity = card_db[card_str]
                cur_cards.append((cid, rarity, card_str))
            else:
                print(f'  [WARN] card not in DB: {card_str}')
        else:
            if cur_name is not None:
                event_cards[cur_name] = cur_cards
            cur_name = nfc(stripped)
            cur_cards = []

if cur_name is not None:
    event_cards[cur_name] = cur_cards

# ===== ERB から LOAD_MONTH_EVENTS を解析 =====
with open(ERB_PATH, 'rb') as f:
    erb_content = f.read().decode('cp932')

idx_start = erb_content.find('@LOAD_MONTH_EVENTS(ARG)')
idx_end   = erb_content.find('@LOAD_EVENT_PICKUP_CARDS', idx_start)
month_block = erb_content[idx_start:idx_end]

# CASE N → [(slot_index, event_name), ...]
case_to_name = {}  # case_number(int) → erb_event_name
cur_month = None
for line in month_block.split('\n'):
    m = re.match(r'\s*CASE\s+(\d+)', line)
    if m:
        cur_month = int(m.group(1))
        continue
    m = re.search(r'TSTR:(\d+)\s*=\s*"(.+?)"', line)
    if m and cur_month is not None:
        tstr_num = int(m.group(1))
        slot = tstr_num - 100  # TSTR:100→slot0, TSTR:101→slot1 ...
        name = m.group(2)
        case_num = (cur_month - 1) * 6 + slot
        case_to_name[case_num] = name

print(f'ERBイベント数: {len(case_to_name)}')

# ===== ERBイベント名 → カードリストのマッチング =====
def find_cards(erb_name):
    """ERBのイベント名でevent_cardsを部分一致検索（NFC正規化）"""
    normalized = nfc(erb_name)
    for full_name, cards in event_cards.items():
        if normalized in full_name:  # full_nameはNFC済み
            return cards
    return None

# ===== 最終イベント用 71段階テーブル生成 =====
# ひまりUR(id:1674)を最後に固定、残り70枚はボックス(type 11)
FINAL_EVENT_NATSUMI_ID = 1671  # [特別な君と]三波なつみ (UR)
FINAL_EVENT_HIMARI_ID  = 1674  # [またね]鶴海ひまり (UR)

def make_final_tier_table():
    """
    最終イベント専用: 71段階
    tier 0-68 (69個): ボックスSR (type 11, value 0)  280PT刻み
    tier 69:           なつみUR (type 9, value 1671)  19700PT
    tier 70:           ひまりUR (type 9, value 1674)  20000PT
    """
    result = []
    for i in range(69):
        pt = 280 * (i + 1)
        result.append((pt, 11, 0, 'ボックスSR'))
    result.append((19700, 9, FINAL_EVENT_NATSUMI_ID, '[特別な君と]三波なつみ(UR)'))
    result.append((20000, 9, FINAL_EVENT_HIMARI_ID,  '[またね]鶴海ひまり(UR)'))
    return result

# ===== 報酬テーブル生成 =====
def make_tier_table(raw_cards):
    """
    raw_cards: [(card_id, rarity, name), ...] 順不同
    最大7枚を使用、レア度昇順でスロットに配置
    Returns: [(pt, type, value, comment), ...] 60要素
    """
    # レア度昇順ソート（同レアは元の順序維持）
    n_all = len(raw_cards)
    if n_all > 7:
        # 高レア優先で7枚選んでから昇順に並べ直す
        desc = sorted(raw_cards, key=lambda x: (-x[1],))
        selected = sorted(desc[:7], key=lambda x: x[1])
        note = f'（{n_all}枚中上位7枚を使用）'
    else:
        selected = sorted(raw_cards, key=lambda x: x[1])
        note = ''

    n = len(selected)
    slots = CARD_SLOTS.get(n, CARD_SLOTS[7])

    if note:
        print(f'  → {note}')

    slot_set = set(slots)
    card_iter = iter(selected)
    result = []

    for i in range(60):
        pt = PT_SEQ[i]
        if i in slot_set:
            cid, rarity, cstr = next(card_iter)
            rl = RARITY_LABEL.get(rarity, '?')
            result.append((pt, 9, cid, f'[{rl}]{cstr}'))
        else:
            t, v, comment = BASE[i]
            result.append((pt, t, v, comment))

    return result

# ===== ERBの @LOAD_EVENT_REWARDS ブロックを再生成 =====
lines = []
lines.append('@LOAD_EVENT_REWARDS(ARG, ARG:1)')
lines.append('LOCAL:9 = (ARG:0 - 1) * 6 + ARG:1')
lines.append('GLOBAL:2999 = 0')
lines.append('SELECTCASE LOCAL:9')

ok_count = 0
skip_count = 0

for case_num in sorted(case_to_name.keys()):
    erb_name = case_to_name[case_num]
    month = case_num // 6 + 1
    slot  = case_num % 6

    cards = find_cards(erb_name)
    if cards is None:
        print(f'[SKIP] CASE {case_num} {month}月[{slot}] {erb_name}: カードリスト未マッチ')
        skip_count += 1
        continue
    if not cards:
        print(f'[SKIP] CASE {case_num} {month}月[{slot}] {erb_name}: カード0枚')
        skip_count += 1
        continue

    # 最終イベントは特殊処理
    is_final = '最終イベント' in erb_name
    if is_final:
        print(f'CASE {case_num} {month}月[{slot}] {erb_name}: 最終イベント専用71段階')
        tiers = make_final_tier_table()
        tier_count = 71
    else:
        print(f'CASE {case_num} {month}月[{slot}] {erb_name}: {len(cards)}枚')
        tiers = make_tier_table(cards)
        tier_count = 60

    lines.append(f'CASE {case_num}\t;{month}月[{slot}] {erb_name}')
    for i, (pt, typ, val, comment) in enumerate(tiers):
        lines.append(f'\tGLOBAL:{3000+i} = {pt}\t;{comment}')
        lines.append(f'\tGLOBAL:{3100+i} = {typ}')
        lines.append(f'\tGLOBAL:{3200+i} = {val}')
    lines.append(f'\tGLOBAL:2999 = {tier_count}')
    ok_count += 1

lines.append('ENDSELECT')
lines.append('RETURN GLOBAL:2999')

new_func_text = '\r\n'.join(lines) + '\r\n'

print(f'\n生成完了: {ok_count}イベント / スキップ: {skip_count}イベント')

# ===== ERBの当該関数を置換 =====
func_start = '@LOAD_EVENT_REWARDS(ARG, ARG:1)'
func_end_marker = '\r\n\r\n'  # 次の空行まで

idx_fs = erb_content.find(func_start)
if idx_fs < 0:
    raise RuntimeError('@LOAD_EVENT_REWARDS が見つかりません')

# 関数末尾を探す（次の @ 定義または EOFまで）
idx_fe = erb_content.find('\r\n@', idx_fs + 1)
if idx_fe < 0:
    idx_fe = len(erb_content)
else:
    idx_fe += 2  # \r\n の手前まで (次の@の直前)

old_func = erb_content[idx_fs:idx_fe]
new_content = erb_content[:idx_fs] + new_func_text + '\r\n' + erb_content[idx_fe:]

with open(ERB_PATH, 'wb') as f:
    f.write(new_content.encode('cp932'))

print(f'書き込み完了: {ERB_PATH}')
