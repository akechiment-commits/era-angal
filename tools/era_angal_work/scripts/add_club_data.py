#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全71キャラのChara CSVに部活データ（CSTR:25=部活名、フラグ:25=部活タイプ）を追加するスクリプト
部活タイプ: 0=帰宅部, 1=運動部, 2=表現部, 3=知識部
"""
import csv
import os
import re
import sys

# 部活→タイプマッピング
SPORTS = {
    'ラクロス部', '陸上部', 'バレー部', 'テニス部', '剣道部',
    'チアリーディング部', '柔道部', 'ソフトボール部', 'バスケットボール部',
    '水泳部', '弓道部', '空手部'
}
EXPRESSION = {'軽音部', '吹奏楽部', '演劇部', '合唱部'}
KNOWLEDGE = {
    '美術部', 'オカルト研究部', '料理研究部', '文芸部', '茶道部',
    '園芸部', '新聞部', '放送部', '生物部', 'パソコン部', '天文部'
}

def get_club_type(club_name):
    if club_name in SPORTS:
        return 1
    elif club_name in EXPRESSION:
        return 2
    elif club_name in KNOWLEDGE:
        return 3
    else:
        return 0  # 帰宅部・不明

# character_data.csv を読み込み（名前→部活 のマッピング）
char_data_path = os.path.join(os.path.dirname(__file__), 'character_data.csv')
char_clubs = {}
with open(char_data_path, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['name'].strip()
        club = row['club'].strip()
        char_clubs[name] = club

csv_dir = os.path.join(os.path.dirname(__file__), '..', 'CSV')
updated = 0
skipped = 0

for n in range(1, 72):
    csv_path = os.path.join(csv_dir, f'Chara{n}.csv')
    if not os.path.exists(csv_path):
        print(f'SKIP: Chara{n}.csv not found')
        skipped += 1
        continue

    # Shift-JISで読み込み
    with open(csv_path, encoding='cp932') as f:
        content = f.read()

    # 名前行から名前取得
    m = re.search(r'^名前,(.+)$', content, re.MULTILINE)
    if not m:
        print(f'SKIP: Chara{n}.csv - 名前行なし')
        skipped += 1
        continue
    char_name = m.group(1).strip()

    # character_data.csvから部活取得
    club_name = char_clubs.get(char_name)
    if club_name is None:
        print(f'WARN: Chara{n}.csv ({char_name}) - character_data.csvに見つからない')
        club_name = '帰宅部'
    club_type = get_club_type(club_name)

    # すでに追加済みかチェック
    if 'CSTR,25,' in content:
        # 上書き
        content = re.sub(r'CSTR,25,.+', f'CSTR,25,{club_name}', content)
        content = re.sub(r'フラグ,25,\d+', f'フラグ,25,{club_type}', content)
        print(f'UPDATE: Chara{n}.csv ({char_name}) -> {club_name}(type={club_type})')
    else:
        # CSTR,24 の行の直後に CSTR,25 を挿入
        content = re.sub(r'(CSTR,24,.+)', rf'\1\nCSTR,25,{club_name}', content)
        # フラグ,12 の行の前後かEOFにフラグ,25を追加
        # フラグ行が既にある場合は最後のフラグ行の後に追加
        flag_matches = list(re.finditer(r'^フラグ,\d+,.+$', content, re.MULTILINE))
        if flag_matches:
            last_flag = flag_matches[-1]
            insert_pos = last_flag.end()
            content = content[:insert_pos] + f'\nフラグ,25,{club_type}' + content[insert_pos:]
        else:
            # フラグ行がなければCSTR,25の後に追加
            content = re.sub(r'(CSTR,25,.+)', rf'\1\nフラグ,25,{club_type}', content)
        print(f'ADD: Chara{n}.csv ({char_name}) -> {club_name}(type={club_type})')

    # Shift-JISで書き戻し
    with open(csv_path, 'w', encoding='cp932') as f:
        f.write(content)
    updated += 1

print(f'\n完了: {updated}件更新, {skipped}件スキップ')
