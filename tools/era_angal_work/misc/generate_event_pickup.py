#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# イベントカードリストからピックアップカードIDのERBを生成

import re, os, csv, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))

def normalize(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('！', '!').replace('？', '?').replace('＊', '*')
    s = s.replace('＆', '&').replace('　', ' ')
    return s

# --- card_name -> card_id マップ ---
card_name_to_id = {}
with open(os.path.join(BASE, 'card_data.csv'), encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        name = row['card_name'].strip()
        cid = int(row['card_id'])
        card_name_to_id[name] = cid

# --- event_card_list.txt を解析 ---
# キーは正規化済みイベント名
event_cards = {}  # 正規化イベント名 -> [cardID, ...]
event_display_names = {}  # 正規化イベント名 -> 図鑑表示用イベント名
current_event = None
with open(os.path.join(BASE, 'event_card_list.txt'), encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        if line and not line.startswith(' ') and not line.startswith('\t'):
            # 日付（2014/03/31）と種別[親愛度]を除去
            raw = re.sub(r'[（(][\d/]+[）)]\s*(?:\[.+?\])?', '', line).strip()
            event_name = normalize(raw)
            current_event = event_name
            event_cards[current_event] = []
            # ERBはcp932で保存するため、結合文字を含まない正規化済みの表記を使う。
            event_display_names[current_event] = event_name
        elif current_event and line.strip():
            m = re.match(r'\s*(\[.+?\].+)', line)
            if m:
                card_name = m.group(1).strip()
                cid = card_name_to_id.get(card_name)
                if cid:
                    event_cards[current_event].append(cid)
                else:
                    print(f"  未マッチ: {card_name}")

# --- EVENT_BOARD_DATA から 月/index -> イベント名 ---
erb_path = os.path.join(BASE, '../ERB/EVENT_BOARD_DATA_イベントデータ.ERB')
with open(erb_path, 'rb') as f:
    erb_content = f.read().decode('cp932').replace('\r\n', '\n')

month_events = {}
cur_month = None
idx = 0
for line in erb_content.replace('\r\n', '\n').split('\n'):
    m = re.match(r'CASE\s+(\d+)', line.strip())
    if m:
        v = int(m.group(1))
        if 1 <= v <= 12:
            cur_month = v
            idx = 0
        continue
    m = re.match(r'TSTR:\d+\s*=\s*"(.+)"', line.strip())
    if m and cur_month:
        month_events[(cur_month, idx)] = m.group(1)
        idx += 1

# --- マッチング確認（正規化して比較）---
matched = 0
for (month, idx2), ename in sorted(month_events.items()):
    norm_ename = normalize(ename)
    cards = event_cards.get(norm_ename, [])
    if cards:
        matched += 1
        print(f"  {month}月[{idx2}] {ename} → {len(cards)}枚: {cards[:3]}{'...' if len(cards)>3 else ''}")
    else:
        print(f"  {month}月[{idx2}] {ename} → なし")
print(f"\nマッチ: {matched}/{len(month_events)}")

# --- @LOAD_EVENT_PICKUP_CARDS ERB関数を生成 ---
lines = []
lines.append('')
lines.append(';--------------------------------------------------')
lines.append('; @LOAD_EVENT_PICKUP_CARDS ARG:0=月(1-12) ARG:1=index(0-5)')
lines.append('; GLOBAL:2199=件数 GLOBAL:2200〜=カードID')
lines.append('; ミッションクリア・マイルストーンのピックアップ用')
lines.append(';--------------------------------------------------')
lines.append('@LOAD_EVENT_PICKUP_CARDS(ARG, ARG:1)')
lines.append('LOCAL:9 = (ARG:0 - 1) * 6 + ARG:1')
lines.append('GLOBAL:2199 = 0')
lines.append('SELECTCASE LOCAL:9')

for (month, idx2), ename in sorted(month_events.items()):
    n = (month - 1) * 6 + idx2
    cards = event_cards.get(normalize(ename), [])[:7]
    lines.append(f'CASE {n}\t;{month}月[{idx2}] {ename}')
    if cards:
        for i, c in enumerate(cards):
            lines.append(f'\tGLOBAL:{2200+i} = {c}')
        lines.append(f'\tGLOBAL:2199 = {len(cards)}')
    else:
        lines.append(f'\tGLOBAL:2199 = 0')

lines.append('ENDSELECT')
lines.append('RETURN GLOBAL:2199')

# --- 通常ガチャ用：イベント報酬カードの判定関数を生成 ---
# イベント一覧に載る全カードを対象にする。ピックアップ対象外の
# ボックス報酬・最終イベント報酬も含まれるため、通常ガチャの重み付けに使える。
event_card_ids = sorted({cid for cards in event_cards.values() for cid in cards})
predicate_lines = []
predicate_lines.append('')
predicate_lines.append(';--------------------------------------------------')
predicate_lines.append('; @EVENT_BOARD_IS_EVENT_CARD ARG:0=カードID')
predicate_lines.append('; イベント報酬カードなら1、通常カードなら0を返す')
predicate_lines.append('; tools/event_card_list.txt から自動生成')
predicate_lines.append(';--------------------------------------------------')
predicate_lines.append('@EVENT_BOARD_IS_EVENT_CARD(ARG)')
predicate_lines.append('SELECTCASE ARG:0')
for start in range(0, len(event_card_ids), 12):
    card_ids = ', '.join(map(str, event_card_ids[start:start + 12]))
    predicate_lines.append(f'CASE {card_ids}')
    predicate_lines.append('\tRETURN 1')
predicate_lines.append('ENDSELECT')
predicate_lines.append('RETURN 0')

# --- 図鑑用：イベント報酬カードの入手先を生成 ---
event_card_sources = {}
for event_name, card_ids in event_cards.items():
    for card_id in card_ids:
        event_card_sources.setdefault(card_id, []).append(event_display_names[event_name])

source_lines = []
source_lines.append('')
source_lines.append(';--------------------------------------------------')
source_lines.append('; @EVENT_BOARD_GET_CARD_SOURCE ARG:0=カードID')
source_lines.append('; RESULTSにイベント名を入れ、イベント報酬カードなら1を返す')
source_lines.append('; tools/event_card_list.txt から自動生成')
source_lines.append(';--------------------------------------------------')
source_lines.append('@EVENT_BOARD_GET_CARD_SOURCE(ARG)')
source_lines.append('RESULTS = ""')
source_lines.append('SELECTCASE ARG:0')
for event_name in sorted(event_cards):
    card_ids = event_cards[event_name]
    if not card_ids:
        continue
    display_name = event_display_names[event_name]
    for start in range(0, len(card_ids), 12):
        source_lines.append(f"CASE {', '.join(map(str, card_ids[start:start + 12]))}")
        source_lines.append(f'\tRESULTS = "イベント「{display_name}」"')
        source_lines.append('\tRETURN 1')
source_lines.append('ENDSELECT')
source_lines.append('RETURN 0')

# --- 既存の @LOAD_EVENT_PICKUP_CHARS / @LOAD_EVENT_PICKUP_CARDS を除去して追記 ---
for func_name in []:
    # コメントブロックを含む関数全体を除去（;---〜から次の@関数の直前まで）
    erb_content = re.sub(
        r'\n;-+\n(?:;[^\n]*\n)*' + re.escape(func_name) + r'\([^\n]*\n.*?(?=\n@|\Z)',
        '', erb_content, flags=re.DOTALL
    )
    # 旧生成物にはコメントなしで関数だけ置かれているものがあるため、こちらも除去する。
    erb_content = re.sub(
        r'^' + re.escape(func_name) + r'\([^\n]*\n.*?(?=^@|\Z)',
        '', erb_content, flags=re.DOTALL | re.MULTILINE
    )

def replace_function(content, function_name, body):
    pattern = r'^' + re.escape(function_name) + r'\([^\n]*\n.*?(?=^@|\Z)'
    if re.search(pattern, content, flags=re.DOTALL | re.MULTILINE):
        return re.sub(pattern, body.rstrip() + '\n', content, count=1, flags=re.DOTALL | re.MULTILINE)
    return content.rstrip() + '\n\n' + body + '\n'

pickup_body = '\n'.join(lines[lines.index('@LOAD_EVENT_PICKUP_CARDS(ARG, ARG:1)'):])
predicate_body = '\n'.join(predicate_lines[predicate_lines.index('@EVENT_BOARD_IS_EVENT_CARD(ARG)'):])
source_body = '\n'.join(source_lines[source_lines.index('@EVENT_BOARD_GET_CARD_SOURCE(ARG)'):])

erb_content = replace_function(erb_content, '@LOAD_EVENT_PICKUP_CARDS', pickup_body)
erb_content = replace_function(erb_content, '@EVENT_BOARD_IS_EVENT_CARD', predicate_body)
if '@EVENT_BOARD_GET_CARD_SOURCE(ARG)' in erb_content:
    erb_content = replace_function(erb_content, '@EVENT_BOARD_GET_CARD_SOURCE', source_body)
else:
    erb_content = erb_content.rstrip() + '\n' + '\n'.join(source_lines) + '\n'

new_content = erb_content
# 文字コード変換が失敗しても元のERBを壊さないよう、完成データを一時ファイル経由で置換する。
encoded_content = new_content.replace('\n', '\r\n').encode('cp932')
temp_path = erb_path + '.tmp'
with open(temp_path, 'wb') as f:
    f.write(encoded_content)
os.replace(temp_path, erb_path)
print(f"ERB更新完了: LOAD_EVENT_PICKUP_CARDS / EVENT_BOARD_IS_EVENT_CARD ({len(event_card_ids)}枚)")
