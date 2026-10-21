#!/usr/bin/env python3
"""キャラCSVに部活素質（運動/表現/知識）を設定するスクリプト"""

# 部活→素質マッピング
# (運動素質, 表現素質, 知識素質)
CLUB_MAP = {
    # 運動部
    'ラクロス部':           (3, 0, 0),
    'テニス部':             (2, 0, 0),
    'バレー部':             (3, 0, 0),
    'チアリーディング部':   (2, 2, 0),  # ダンス=表現もある
    '水泳部':               (3, 0, 0),
    '陸上部':               (3, 0, 0),
    '剣道部':               (3, 0, 0),
    '柔道部':               (3, 0, 0),
    'ソフトボール部':       (3, 0, 0),
    'バスケットボール部':   (3, 0, 0),
    '弓道部':               (2, 0, 1),  # 精神統一=知識面も
    '空手部':               (3, 0, 0),
    # 表現系文化部
    '軽音部':               (0, 3, 0),
    '吹奏楽部':             (0, 2, 0),
    '合唱部':               (0, 3, 0),
    '演劇部':               (0, 3, 0),
    '放送部':               (0, 2, 1),
    '新聞部':               (0, 1, 2),  # 取材・文章=知識寄り
    # 知識系文化部
    '文芸部':               (0, 1, 2),  # 創作=少し表現
    '美術部':               (0, 2, 1),  # 美術は表現寄り
    '天文部':               (0, 0, 3),
    'オカルト研究部':       (0, 0, 2),
    '料理研究部':           (0, 0, 1),  # 料理素質は別枠
    '茶道部':               (0, 1, 2),  # 作法・文化=知識+表現
    '園芸部':               (0, 0, 2),
    '生物部':               (0, 0, 3),
    'パソコン部':           (0, 0, 3),
    # 帰宅部
    '帰宅部':               (0, 0, 0),
}

# キャラ個別補正（キャラ名 → (運動補正, 表現補正, 知識補正)）
# character_data.csvとcharacter_profiles.txtから判断
INDIVIDUAL_ADJUST = {
    # 怪力持ち: 運動+1
    '熊沢ひめの': (1, 0, 0),     # 怪力、テニス部だが力が強い
    '大虎いさみ': (1, 0, 0),     # 怪力、柔道部
    # 運動音痴: 運動を0に固定（後で処理）
    '小鳩あずさ': (0, 0, 0),     # 運動音痴、テニス部だが…
    '夢路まりあ': (0, 0, 0),     # 運動音痴、帰宅部、裁縫好き→表現+1
    # 趣味・特技による補正
    '八朔つゆり': (0, 1, 0),     # 帰宅部だがピアノ弾ける→表現
    '安条まい': (0, 1, 0),       # 帰宅部、SNS=表現的
    '峰山しおん': (0, 0, 2),     # 帰宅部、読書家→知識
    '瀬川かえで': (0, 0, 1),     # 帰宅部、頭は回る
    '桃智あすか': (0, 0, 1),     # バスケ部だが華道もやる→知識+1
    '神樹はじめ': (0, 0, 1),     # 弓道部、料理好き→知識+1
    '柊るな': (0, 0, 1),         # ラクロス部、ナンプレ好き→知識+1
    '梅園かな': (0, 1, 0),       # バレー部、バレエもやる→表現+1
    '藤猪しずく': (0, 0, 1),     # 軽音部、音楽通→知識+1
    '月永るか': (0, 1, 0),       # 軽音部、作詩→表現+1
    '天宮るり': (0, 1, 0),       # 天文部、写真が趣味→表現+1
    '笹芽ひよの': (0, 1, 0),     # 新聞部、写真が趣味→表現+1
    '四方みつる': (0, 0, 1),     # 陸上部、読書好き→知識+1
    '鶯木こはる': (1, 0, 0),     # 料理研究部だが狩りが趣味→運動+1
    '岩戸サン': (1, 0, 0),       # 陸上部、身体能力高い→運動+1
    '龍泉寺レンレン': (1, 0, 0), # 空手部、拳法が趣味→運動+1
    '花音ことり': (1, 0, 0),     # チア部、ダンス→既に運動2/表現2、さらに運動+1
    '花丘まり': (1, 0, 0),       # テニス部、テニスが趣味→本気度高い
    '鯱いかり': (1, 0, 0),       # 水泳部、泳ぐのが趣味→本気度高い
    '榊むつみ': (1, 0, 0),       # 陸上部、ランニングが趣味→本気度高い
    '藍乃あいか': (0, 0, 1),     # 文芸部、読書/猫→知識+1
    '久坂あやめ': (0, 0, 1),     # 生物部、ペットの世話→知識+1
    '冴木もも': (0, 0, 1),       # 美術部、生き物観察→知識+1
    '深鳥ふみ': (0, 0, 1),       # 新聞部、読書好き→知識+1
}

# 運動音痴キャラ（運動素質を0に固定）
UNDOU_ONCHI = ['小鳩あずさ', '夢路まりあ']


def process_chara(chara_num, name, club):
    """キャラの部活素質値を決定"""
    base = CLUB_MAP.get(club, (0, 0, 0))
    sports, perform, knowledge = base

    # 個別補正
    adj = INDIVIDUAL_ADJUST.get(name, (0, 0, 0))
    sports += adj[0]
    perform += adj[1]
    knowledge += adj[2]

    # 運動音痴は運動素質0固定
    if name in UNDOU_ONCHI:
        sports = 0

    # 夢路まりあ: 裁縫好き→表現+1を個別補正で入れてなかった
    if name == '夢路まりあ':
        perform = 1

    return sports, perform, knowledge


def update_chara_csv(chara_num, sports, perform, knowledge, perform_skill=0):
    """キャラCSVに部活素質を追加/更新。perform_skill=旧歌唱技能の値"""
    filepath = f'CSV/Chara{chara_num}.csv'
    with open(filepath, 'rb') as f:
        content = f.read()

    lines = content.decode('cp932').split('\n')
    new_lines = []
    # 既存の能力,51/52/54/55/56と能力,91/92/93/94/95を除去
    remove_abls = {'51', '52', '54', '55', '56', '91', '92', '93', '94', '95'}

    inserted = False
    for line in lines:
        stripped = line.strip()
        # 旧ABLを除去
        if stripped.startswith('能力,'):
            parts = stripped.split(',')
            if len(parts) >= 2 and parts[1] in remove_abls:
                continue
        new_lines.append(line)

        # 最後の能力行の後、またはフラグ行の前に挿入
        if not inserted and stripped.startswith('能力,'):
            # 次の行が能力行でなければここに挿入
            pass

    # 挿入位置を決定: 最後の「能力,」行の後
    insert_idx = -1
    for i, line in enumerate(new_lines):
        if line.strip().startswith('能力,'):
            insert_idx = i

    # 能力行がない場合、「素質,」の最後の後に
    if insert_idx == -1:
        for i, line in enumerate(new_lines):
            if line.strip().startswith('素質,'):
                insert_idx = i

    # 挿入する行を作成（値が0のものは省略）
    abl_lines = []
    if sports > 0:
        abl_lines.append(f'能力,54,{sports}')
    if perform > 0:
        abl_lines.append(f'能力,55,{perform}')
    if knowledge > 0:
        abl_lines.append(f'能力,56,{knowledge}')
    if perform_skill > 0:
        abl_lines.append(f'能力,94,{perform_skill}')

    if abl_lines and insert_idx >= 0:
        for j, abl_line in enumerate(abl_lines):
            new_lines.insert(insert_idx + 1 + j, abl_line)

    result = '\n'.join(new_lines)
    with open(filepath, 'wb') as f:
        f.write(result.encode('cp932'))


def migrate_old_abl(chara_num):
    """旧歌唱素質(52)→表現素質(55), 旧歌唱技能(92)→表現技能(94)に移行"""
    filepath = f'CSV/Chara{chara_num}.csv'
    with open(filepath, 'rb') as f:
        content = f.read()

    text = content.decode('cp932')
    # 能力,52,X → 能力,55,X に変換（表現素質に統合）
    # ただし55が既にある場合は大きい方を取る
    lines = text.split('\n')
    val_52 = 0
    val_92 = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('能力,52,'):
            val_52 = int(stripped.split(',')[2])
        if stripped.startswith('能力,92,'):
            val_92 = int(stripped.split(',')[2])

    new_lines = []
    for line in lines:
        stripped = line.strip()
        # 旧52/92を除去（update_chara_csvで55/94として再設定される）
        if stripped.startswith('能力,52,') or stripped.startswith('能力,92,'):
            continue
        new_lines.append(line)

    result = '\n'.join(new_lines)
    with open(filepath, 'wb') as f:
        f.write(result.encode('cp932'))

    return val_52, val_92


# メイン処理
import csv
import io

# character_data.csv読み込み
with open('tools/character_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    char_data = {row['name']: row for row in reader}

# キャラ番号→名前のマッピング
chara_names = {}
for i in range(1, 72):
    filepath = f'CSV/Chara{i}.csv'
    try:
        with open(filepath, 'rb') as f:
            content = f.read().decode('cp932')
        for line in content.split('\n'):
            if line.strip().startswith('名前,'):
                chara_names[i] = line.strip().split(',')[1]
                break
    except:
        pass

# 処理実行
print(f"{'No':>3} {'名前':<12} {'部活':<16} {'運動':>2} {'表現':>2} {'知識':>2} {'移行'}")
print("-" * 65)

for num in sorted(chara_names.keys()):
    name = chara_names[num]
    data = char_data.get(name, {})
    club = data.get('club', '帰宅部')

    # 旧歌唱/撮影の移行
    old_52, old_92 = migrate_old_abl(num)

    # 部活素質の決定
    sports, perform, knowledge = process_chara(num, name, club)

    # 旧歌唱素質が表現素質より大きければ採用
    if old_52 > perform:
        perform = old_52

    # CSV更新（旧歌唱技能→表現技能も一緒に設定）
    update_chara_csv(num, sports, perform, knowledge, perform_skill=old_92)

    migrate_note = ""
    if old_52 > 0 or old_92 > 0:
        migrate_note = f"(旧歌唱{old_52}/{old_92}→表現)"

    print(f"{num:>3} {name:<12} {club:<16} {sports:>2} {perform:>2} {knowledge:>2} {migrate_note}")

print("\n完了!")
