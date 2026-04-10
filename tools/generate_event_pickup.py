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
    erb_content = f.read().decode('cp932')

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

# --- 既存の @LOAD_EVENT_PICKUP_CHARS / @LOAD_EVENT_PICKUP_CARDS を除去して追記 ---
for func_name in ['@LOAD_EVENT_PICKUP_CHARS', '@LOAD_EVENT_PICKUP_CARDS']:
    # コメントブロックを含む関数全体を除去（;---〜から次の@関数の直前まで）
    erb_content = re.sub(
        r'\n;-+\n(?:;[^\n]*\n)*' + re.escape(func_name) + r'\([^\n]*\n.*?(?=\n@|\Z)',
        '', erb_content, flags=re.DOTALL
    )

new_content = erb_content.rstrip() + '\n' + '\n'.join(lines) + '\n'
with open(erb_path, 'wb') as f:
    f.write(new_content.encode('cp932'))
print("ERB更新完了: LOAD_EVENT_PICKUP_CARDS")
