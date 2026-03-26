#!/usr/bin/env python3
"""
eraあんガル キャラクターCSV自動生成スクリプト
character_data.csv + character_profiles.json から
CSV/Chara1.csv〜Chara71.csv を生成する
"""

import csv
import json
import os
import re

# ============================
# 定数・マッピング定義
# ============================

# ABL インデックス（学園向け）
ABL = {
    '勉強': 0,
    '運動': 1,
    '音楽': 2,
    '芸術': 3,
    '社交': 4,
    '料理': 5,
    '特技': 6,
}

# タレント（素質）インデックス
TALENT = {
    # 基本処女フラグ（システム互換）
    '処女': 0,
    # 性格系
    '臆病': 10,
    '反抗的': 11,
    '気丈': 12,
    '素直': 13,
    '大人しい': 14,
    'プライド高い': 15,
    '生意気': 16,
    'プライド低い': 17,
    'ツンデレ': 18,
    # 精神系
    '自制心': 20,
    '無関心': 21,
    '感情乏しい': 22,
    '好奇心旺盛': 23,
    '保守的': 24,
    '楽観的': 25,
    '悲観的': 26,
    '一線越えない': 27,
    '目立ちたがり': 28,
    # 追加性格
    '真面目': 30,
    '天然': 31,
    '世話焼き': 32,
    'リーダー': 33,
    'マイペース': 34,
    '恥じらい': 35,
    '負けず嫌い': 37,
    # 学園特性
    '運動部員': 60,
    '文化部員': 61,
    '生徒会': 62,
    '委員会活動': 63,
    '帰宅部': 64,
    'スポーツ万能': 65,
    '芸術肌': 66,
    '料理上手': 68,
    '楽器上手': 69,
    '動物好き': 72,
}

# クラス→クラス番号マッピング
CLASS_ORDER = ['1-A', '1-B', '1-C', '2-A', '2-B', '2-C', '3-A', '3-B', '3-C']

# 運動系部活リスト
SPORTS_CLUBS = {
    'ラクロス部', 'ソフトボール部', 'チアリーディング部', 'テニス部',
    'バスケットボール部', 'バレー部', '柔道部', '剣道部', '弓道部',
    '水泳部', '陸上部', '空手部',
}

# 音楽系部活リスト
MUSIC_CLUBS = {'吹奏楽部', '合唱部', '軽音部'}

# 芸術系部活リスト
ART_CLUBS = {'美術部', '演劇部', '放送部', '文芸部', '新聞部'}

# 料理系部活リスト
COOKING_CLUBS = {'料理研究部', '茶道部'}

# その他文化部リスト
CULTURE_CLUBS = {'オカルト研究部', 'パソコン部', '園芸部', '天文部', '生物部'}

# 部活→運動ABL初期値
SPORTS_ABL = {
    '柔道部': 4, '空手部': 4, '剣道部': 4, '弓道部': 3,
    'バスケットボール部': 4, 'バレー部': 4, 'ソフトボール部': 3,
    'テニス部': 3, 'ラクロス部': 3, 'チアリーディング部': 3,
    '陸上部': 3, '水泳部': 3,
}

# 部活→音楽ABL初期値
MUSIC_ABL = {
    '吹奏楽部': 4, '合唱部': 3, '軽音部': 3,
}

# 部活→芸術ABL初期値
ART_ABL = {
    '美術部': 4, '演劇部': 3, '放送部': 2,
    '文芸部': 3, '新聞部': 2,
}

# 部活→料理ABL初期値
COOKING_ABL = {
    '料理研究部': 4, '茶道部': 3,
}

# 部活→体力
CLUB_STAMINA = {
    '柔道部': 3000, '空手部': 3000, '剣道部': 2800, '弓道部': 2500,
    'バスケットボール部': 3000, 'バレー部': 2800, 'ソフトボール部': 2600,
    'テニス部': 2600, 'ラクロス部': 2600, 'チアリーディング部': 2500,
    '陸上部': 2800, '水泳部': 2700,
    '吹奏楽部': 1800, '合唱部': 1600, '軽音部': 1600,
    '美術部': 1600, '演劇部': 1700, '放送部': 1500,
    '文芸部': 1400, '新聞部': 1500, '料理研究部': 1600, '茶道部': 1400,
    'オカルト研究部': 1400, 'パソコン部': 1300, '園芸部': 1500,
    '天文部': 1400, '生物部': 1500, '帰宅部': 1200,
}

# クラス→勉強ABL傾向
CLASS_STUDY = {
    '1-A': 3, '2-A': 2, '3-A': 3,
    '1-B': 2, '2-B': 1, '3-B': 2,
    '1-C': 1, '2-C': 2, '3-C': 2,
}


def load_profiles(path):
    """character_profiles.json を名前→プロフィールの辞書に変換"""
    with open(path, encoding='utf-8') as f:
        profiles = json.load(f)
    return {p['name']: p for p in profiles}


def get_first_name(full_name):
    """フルネームから名（下の名前）を抽出"""
    # 外国名（スペースなし、カタカナ）はそのまま
    if '・' in full_name:
        return full_name.split('・')[0]
    # 日本名：姓+名の場合、名を返す
    # ほとんどが2文字姓+2文字名のパターン
    # character_profilesは「ひまり」のような下の名前
    return full_name


def infer_callname(full_name, profiles):
    """キャラの「呼び名」を決定（プロフィールの名からひらがなキー照合）"""
    # profiles は「ひまり」「なつみ」等のひらがなキー
    # character_data の名前から最も近いものを探す
    # 簡易実装：フルネームをそのまま使う
    return full_name


def determine_talents(row, profile):
    """キャラ情報からタレントIDリストを決定"""
    talents = []
    club = row.get('club', '')
    cls = row.get('class', '')
    committee = row.get('committee', '')
    intro = (row.get('intro', '') + row.get('old_intro', '')).lower()
    tone = profile.get('tone', '中立') if profile else '中立'
    keywords = profile.get('keywords', {}) if profile else {}
    kw = list(keywords.keys())

    # 運動部・文化部判定
    if club in SPORTS_CLUBS:
        talents.append(TALENT['運動部員'])
        if club in ('柔道部', '空手部', '剣道部', 'バスケットボール部', 'バレー部'):
            talents.append(TALENT['負けず嫌い'])
    elif club in MUSIC_CLUBS | ART_CLUBS | COOKING_CLUBS | CULTURE_CLUBS:
        talents.append(TALENT['文化部員'])
    elif club == '帰宅部':
        talents.append(TALENT['帰宅部'])

    # 音楽系タレント
    if club in MUSIC_CLUBS:
        talents.append(TALENT['楽器上手'])

    # 料理上手
    if club in COOKING_CLUBS or '料理' in row.get('hobbies', ''):
        talents.append(TALENT['料理上手'])

    # 動物好き
    if '動物' in intro or 'ペット' in intro or 'うさぎ' in intro or '猫' in intro or '犬' in intro:
        talents.append(TALENT['動物好き'])

    # 委員会活動
    if committee:
        talents.append(TALENT['委員会活動'])

    # 生徒会・クラス代表系キャラ判定（intro テキストから）
    if '生徒会' in intro:
        talents.append(TALENT['生徒会'])

    # 性格タレント（トーン+キーワードから）
    if tone == '明るい':
        talents.append(TALENT['楽観的'])
        if '好き' in kw and keywords.get('好き', 0) >= 50:
            talents.append(TALENT['素直'])
    elif tone == '暗い':
        talents.append(TALENT['悲観的'])
    else:  # 中立
        pass

    # introテキストベースの性格判定
    if 'ツンデレ' in intro or 'ツン' in intro:
        talents.append(TALENT['ツンデレ'])
    if '世話焼き' in intro or '世話を焼く' in intro:
        talents.append(TALENT['世話焼き'])
    if '几帳面' in intro or '真面目' in intro or '丁寧' in intro:
        talents.append(TALENT['真面目'])
    if '天然' in intro or '不思議' in intro:
        talents.append(TALENT['天然'])
    if '部長' in intro or 'リーダー' in intro or '会長' in intro:
        talents.append(TALENT['リーダー'])
    if 'マイペース' in intro or '独自' in intro:
        talents.append(TALENT['マイペース'])
    if 'プライド' in intro or '自信家' in intro or '高飛車' in intro:
        talents.append(TALENT['プライド高い'])
    if '気丈' in intro or '勝気' in intro:
        talents.append(TALENT['気丈'])
    if '大人しい' in intro or '無口' in intro or '内気' in intro:
        talents.append(TALENT['大人しい'])
    if '好奇心' in intro:
        talents.append(TALENT['好奇心旺盛'])
    if '目立' in intro:
        talents.append(TALENT['目立ちたがり'])

    # 重複除去して返す
    return list(dict.fromkeys(talents))


def determine_abl(row, profile):
    """ABL初期値を {abl_id: value} で返す"""
    club = row.get('club', '')
    cls = row.get('class', '')
    hobbies = row.get('hobbies', '')
    intro = row.get('intro', '') + row.get('old_intro', '')
    tone = profile.get('tone', '中立') if profile else '中立'

    abl = {}

    # 勉強
    study_base = CLASS_STUDY.get(cls, 1)
    if '勉強' in hobbies or '読書' in hobbies:
        study_base = min(study_base + 1, 4)
    abl[ABL['勉強']] = study_base

    # 運動
    sport_val = SPORTS_ABL.get(club, 0)
    if sport_val == 0 and '運動' in hobbies:
        sport_val = 1
    abl[ABL['運動']] = sport_val

    # 音楽
    music_val = MUSIC_ABL.get(club, 0)
    if music_val == 0 and ('音楽' in hobbies or '歌' in hobbies or 'ピアノ' in hobbies):
        music_val = 2
    abl[ABL['音楽']] = music_val

    # 芸術
    art_val = ART_ABL.get(club, 0)
    if art_val == 0 and ('絵' in hobbies or '工作' in hobbies or '手芸' in hobbies):
        art_val = 2
    abl[ABL['芸術']] = art_val

    # 社交
    social_val = 1
    if tone == '明るい':
        social_val = 2
    if '生徒会' in intro or '委員' in row.get('committee', ''):
        social_val = max(social_val, 2)
    if tone == '暗い' or '大人しい' in intro or '無口' in intro:
        social_val = max(0, social_val - 1)
    abl[ABL['社交']] = social_val

    # 料理
    cooking_val = COOKING_ABL.get(club, 0)
    if cooking_val == 0 and ('料理' in hobbies or 'お菓子' in hobbies or '調理' in hobbies):
        cooking_val = 2
    elif cooking_val == 0 and '料理' in intro:
        cooking_val = 1
    abl[ABL['料理']] = cooking_val

    # 特技 (主に趣味ベース)
    abl[ABL['特技']] = 1

    return {k: v for k, v in abl.items() if v > 0}


def determine_base_stats(row):
    """基礎ステータス（体力・精神力）を決定"""
    club = row.get('club', '')
    intro = row.get('intro', '') + row.get('old_intro', '')

    # 体力
    stamina = CLUB_STAMINA.get(club, 1500)
    if '虚弱' in intro or '病弱' in intro:
        stamina = 800

    # 精神力（クラスと性格から）
    spirit = 1200
    if '1-A' == row.get('class') or '3-A' == row.get('class'):
        spirit = 1500
    if '気力' in intro or '精神' in intro:
        spirit += 200

    return stamina, spirit


def determine_compat(row, all_chars):
    """相性（幼馴染・従姉妹・親友）リスト → {char_id: bonus}"""
    compat = {}
    intro = row.get('intro', '') + row.get('old_intro', '')
    name = row.get('name', '')

    for other in all_chars:
        if other['name'] == name:
            continue
        other_name = other['name']
        # 苗字または名前がintroに含まれる場合
        # 簡易判定：片方のキャラ名が相手のintroに登場
        other_short = other_name  # 名前をそのまま使う
        if other_short in intro:
            compat[other['id']] = 120
    return compat


def make_cstr(row):
    """CSTRカスタム文字列リスト → [(idx, text)]"""
    return [
        (0, row.get('club', '')),
        (1, row.get('class', '')),
        (2, row.get('birthday', '')),
        (3, row.get('blood_type', '')),
        (4, row.get('hobbies', '')),
        (5, row.get('fav_color', '')),
    ]


def generate_chara_csv(char_id, row, profile, all_chars, output_dir):
    """1キャラ分のChara CSV を生成してファイルに書き込む"""
    name = row['name']
    callname = name  # 呼び名はフルネーム（後で調整可）

    talents = determine_talents(row, profile)
    abl = determine_abl(row, profile)
    stamina, spirit = determine_base_stats(row)
    compat = determine_compat(row, all_chars)
    cstrs = make_cstr(row)

    lines = []
    lines.append(f'番号,{char_id}')
    lines.append(f'名前,{name}')
    lines.append(f'呼び名,{callname}')
    lines.append(f'基礎,0,{stamina}')
    lines.append(f'基礎,1,{spirit}')

    for t in talents:
        lines.append(f'素質,{t}')

    for abl_id, val in sorted(abl.items()):
        lines.append(f'能力,{abl_id},{val}')

    for other_id, bonus in sorted(compat.items()):
        lines.append(f'相性,{other_id},{bonus}')

    for idx, text in cstrs:
        if text:
            lines.append(f'CSTR,{idx},{text}')

    # CP932 でファイル書き込み
    filepath = os.path.join(output_dir, f'Chara{char_id}.csv')
    with open(filepath, 'w', encoding='cp932', errors='replace') as f:
        f.write('\n'.join(lines) + '\n')

    return filepath


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    csv_dir = os.path.join(repo_root, 'CSV')

    char_csv_path = os.path.join(script_dir, 'character_data.csv')
    profiles_path = os.path.join(script_dir, 'character_profiles.json')

    # キャラデータ読み込み
    with open(char_csv_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        chars = list(reader)

    # クラス順にソートしてIDを割り当て
    def class_sort_key(r):
        cls = r.get('class', 'Z')
        try:
            idx = CLASS_ORDER.index(cls)
        except ValueError:
            idx = 99
        return (idx, r.get('name', ''))

    chars.sort(key=class_sort_key)

    # IDを1-71で割り当て
    for i, ch in enumerate(chars):
        ch['id'] = i + 1

    # プロフィール読み込み（名前の短縮形→プロフィール）
    profiles_by_fullname = {}
    if os.path.exists(profiles_path):
        with open(profiles_path, encoding='utf-8') as f:
            profiles = json.load(f)
        # プロフィールはひらがな名で管理されているので、
        # character_data の名前と照合するため姓名を分解して探す
        profiles_by_shortname = {p['name']: p for p in profiles}

        for ch in chars:
            full = ch['name']
            # 姓+名の場合、名だけでマッチング試行
            # 例: 「三善かなえ」→「かなえ」
            matched = None
            # まずフルネームで試す
            if full in profiles_by_shortname:
                matched = profiles_by_shortname[full]
            else:
                # 名（後半部分）でマッチング
                # 日本名は姓2-3文字+名2文字パターンが多い
                for cut in range(2, len(full)):
                    short = full[cut:]
                    if short in profiles_by_shortname:
                        matched = profiles_by_shortname[short]
                        break
                # カタカナ名（クー・カロア等）
                if matched is None and '・' in full:
                    first = full.split('・')[0]
                    if first in profiles_by_shortname:
                        matched = profiles_by_shortname[first]
            profiles_by_fullname[full] = matched

    print(f'キャラ数: {len(chars)}')
    print()

    generated = 0
    for ch in chars:
        profile = profiles_by_fullname.get(ch['name'])
        filepath = generate_chara_csv(ch['id'], ch, profile, chars, csv_dir)
        print(f'[{ch["id"]:2d}] {ch["name"]} ({ch["class"]}) → {os.path.basename(filepath)}')
        generated += 1

    print(f'\n✓ {generated}件生成完了')

    # ID→名前マッピングも出力（後で参照用）
    mapping_path = os.path.join(script_dir, 'chara_id_mapping.txt')
    with open(mapping_path, 'w', encoding='utf-8') as f:
        f.write('ID,名前,クラス,部活\n')
        for ch in chars:
            f.write(f'{ch["id"]},{ch["name"]},{ch["class"]},{ch["club"]}\n')
    print(f'IDマッピング: {mapping_path}')


if __name__ == '__main__':
    main()
