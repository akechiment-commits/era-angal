#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# イベントカードリストからピックアップキャラERBを生成

import re, os, glob

# --- キャラ名 → No ---
name_to_no = {}
for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '../CSV/Chara*.csv'))):
    base = os.path.basename(path).replace('Chara','').replace('.csv','')
    m = re.match(r'^(\d+)', base)
    if not m: continue
    no = int(m.group(1))
    if no == 0: continue
    with open(path, 'rb') as f:
        for line in f:
            line = line.decode('cp932').strip()
            if line.startswith('名前,'):
                name = line.split(',')[1].strip()
                name_to_no[name] = no
                break

# --- event_card_list.txt を解析 ---
list_path = os.path.join(os.path.dirname(__file__), 'event_card_list.txt')
event_chars = {}  # イベント名 -> [charNo, ...]
current_event = None
with open(list_path, encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        # イベント名行（インデント無し、[で始まらない）
        if line and not line.startswith(' ') and not line.startswith('\t'):
            # 日付部分を除去
            event_name = re.sub(r'[（(][\d/]+[）)]', '', line).strip()
            current_event = event_name
            event_chars[current_event] = []
        elif current_event and line.strip():
            # [カード名]キャラ名
            m = re.match(r'\s*\[.*?\](.+)', line)
            if m:
                char_name = m.group(1).strip()
                no = name_to_no.get(char_name)
                if no and no not in event_chars[current_event]:
                    event_chars[current_event].append(no)

# --- EVENT_BOARD_DATA から 月/index -> イベント名 を取得 ---
erb_path = os.path.join(os.path.dirname(__file__), '../ERB/EVENT_BOARD_DATA_イベントデータ.ERB')
with open(erb_path, 'rb') as f:
    erb_content = f.read().decode('cp932')

# TSTR:100〜105 の = "..." を月ごとに取得
month_events = {}  # (month, idx) -> event_name
cur_month = None
idx = 0
for line in erb_content.split('\n'):
    m = re.match(r'CASE\s+(\d+)', line.strip())
    if m:
        cur_month = int(m.group(1))
        idx = 0
        continue
    m = re.match(r'TSTR:\d+\s*=\s*"(.+)"', line.strip())
    if m and cur_month and 1 <= cur_month <= 12:
        month_events[(cur_month, idx)] = m.group(1)
        idx += 1

print(f"月別イベント数: {len(month_events)}")
print(f"カードリストイベント数: {len(event_chars)}")

# マッチング確認
matched = 0
for (month, idx), ename in sorted(month_events.items()):
    chars = event_chars.get(ename, [])
    print(f"  {month}月[{idx}] {ename} → {len(chars)}キャラ: {chars}")
    if chars: matched += 1
print(f"マッチ: {matched}/{len(month_events)}")

# --- ERB関数を生成 ---
lines = []
lines.append('')
lines.append(';--------------------------------------------------')
lines.append('; @LOAD_EVENT_PICKUP_CHARS ARG:0=月(1-12) ARG:1=index(0-5)')
lines.append('; GLOBAL:2199=件数 GLOBAL:2200〜=キャラNo')
lines.append('; ミッションクリア・マイルストーンのピックアップ用')
lines.append(';--------------------------------------------------')
lines.append('@LOAD_EVENT_PICKUP_CHARS(ARG, ARG:1)')
lines.append('LOCAL:9 = (ARG:0 - 1) * 6 + ARG:1')
lines.append('GLOBAL:2199 = 0')
lines.append('SELECTCASE LOCAL:9')

for (month, idx), ename in sorted(month_events.items()):
    n = (month - 1) * 6 + idx
    chars = event_chars.get(ename, [])[:7]  # 最大7人
    lines.append(f'CASE {n}\t;{month}月[{idx}] {ename}')
    if chars:
        for i, c in enumerate(chars):
            lines.append(f'\tGLOBAL:{2200+i} = {c}')
        lines.append(f'\tGLOBAL:2199 = {len(chars)}')
    else:
        lines.append(f'\tGLOBAL:2199 = 0\t;ピックアップなし')

lines.append('ENDSELECT')
lines.append('RETURN GLOBAL:2199')

# --- ERBファイルに追記 ---
# 既存の @LOAD_EVENT_PICKUP_CHARS があれば削除
if '@LOAD_EVENT_PICKUP_CHARS' in erb_content:
    # 既存関数を削除
    erb_content = re.sub(
        r'\n;--------------------------------------------------\n; @LOAD_EVENT_PICKUP_CHARS.*?(?=\n@|\Z)',
        '', erb_content, flags=re.DOTALL
    )

new_content = erb_content.rstrip() + '\n' + '\n'.join(lines) + '\n'
with open(erb_path, 'wb') as f:
    f.write(new_content.encode('cp932'))

print("ERB更新完了")
