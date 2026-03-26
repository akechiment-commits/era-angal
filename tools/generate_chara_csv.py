#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eraあんガル キャラクターCSV生成スクリプト
Chara1.csv〜Chara71.csvを生成する

素質番号の主なもの：
  0:処女  10:臆病  11:反抗的  12:気丈  13:素直  14:大人しい  15:プライド高い
  16:生意気  17:プライド低い  18:ツンデレ  20:自制心  21:無関心  22:感情乏しい
  23:好奇心  24:保守的  25:楽観的  26:悲観的  28:目立ちたがり
  30:貞操観念  31:貞操無頓着  35:恥じらい  37:弱味  40:痛みに弱い  41:痛みに強い
  42:濡れやすい  43:濡れにくい  52:舌使い  57:おもらし癖  58:淫具知識
  63:献身的  70:快感に素直  71:快感の否定  73:即落ち  74:淫壷  75:淫核
  76:淫乱  77:尻穴狂い  78:淫乳  79:マゾ  80:倒錯的  81:両刀
  82:男嫌い  83:サド  84:嫉妬  85:恋慕  87:小悪魔
  100:小柄体型  101:C鈍感  102:C敏感  103:V鈍感  104:V敏感
  105:A鈍感  106:A敏感  107:B鈍感  108:B敏感  109:貧乳  110:巨乳
  111:回復早い  112:回復遅い  113:魅力  151:キス未経験
  220:怪力  221:運動音痴  222:霊感  223:アイドル

能力番号：
  50:料理素質  51:撮影素質  52:歌唱素質  53:探索素質
  90:料理技能  92:歌唱技能

フラグ12 = 主導権基準値（正=主導権とりやすい, 負=とられやすい）
"""

import os

# ────────────────────────────────────────────────────────
# キャラクター定義
#   hp        : 基礎体力（運動部上位2500、運動部2000〜2200、普通1400〜1800、虚弱〜1000）
#   sp        : 基礎気力
#   talents   : 素質リスト（0=処女はほぼ全員に付ける）
#   initiative: フラグ12 主導権基準値
#   cooking   : 料理素質レベル(0〜3)
#   singing   : 歌唱素質レベル(0〜3)
# ────────────────────────────────────────────────────────
CHARA_DATA = [
    # ───── 1年A組 ─────
    dict(no=1,  name="三善かなえ",   nick="かなえ",
         hp=1500, sp=1200,
         talents=[0,11,15,18,20,30,35,102,151],          # C敏感：ツンデレ・恥じらい強め
         initiative=10, singing=2),

    dict(no=2,  name="北川ゆき",     nick="ゆき",
         hp=1200, sp=1000,
         talents=[0,10,14,35,30,26,102,108,151],          # C敏感+B敏感：臆病・大人しい全体的に敏感
         initiative=-20),

    dict(no=3,  name="小野ちよ",     nick="ちよ",
         hp=1500, sp=1200,
         talents=[0,13,14,25,35,30,42,104,108,151],       # V敏感+B敏感：濡れやすい・大人しい
         initiative=-15, cooking=2),

    dict(no=4,  name="早川きこ",     nick="きこ",
         hp=1500, sp=1200,
         talents=[0,13,25,35,30,108,151],                 # B敏感：素直・楽観的
         initiative=-15, singing=1),

    dict(no=5,  name="桃智あすか",   nick="あすか",
         hp=2000, sp=1500,
         talents=[0,23,25,13,30,35,105,151],              # A鈍感：活発・運動系
         initiative=5),

    dict(no=6,  name="藍乃あいか",   nick="あいか",
         hp=1200, sp=1000,
         talents=[0,10,35,26,30,102,108,151],             # C敏感+B敏感：臆病・悲観的
         initiative=-20),

    dict(no=7,  name="高原ちあき",   nick="ちあき",
         hp=1800, sp=1500,
         talents=[0,13,25,63,30,35,104,151],              # V敏感：素直・献身的
         initiative=0),

    # ───── 1年B組 ─────
    dict(no=8,  name="丸子みさき",   nick="みさき",
         hp=1500, sp=1500,
         talents=[0,28,25,30,35,105,151],                 # A鈍感：元気・活動的
         initiative=5),

    dict(no=9,  name="月永るか",     nick="るか",
         hp=1200, sp=1000,
         talents=[0,14,10,35,30,26,102,108,151],          # C敏感+B敏感：臆病・大人しい
         initiative=-20),

    dict(no=10, name="木之下ゆゆ",   nick="ゆゆ",
         hp=1300, sp=1100,
         talents=[0,13,25,17,35,30,109,108,151],          # B敏感：貧乳でも敏感
         initiative=-25),

    dict(no=11, name="氷野くるみ",   nick="くるみ",
         hp=1500, sp=1300,
         talents=[0,23,25,35,30,102,151],                 # C敏感：好奇心旺盛・恥じらい
         initiative=-5),

    dict(no=12, name="神樹いちか",   nick="いちか",
         hp=1800, sp=1400,
         talents=[0,23,25,30,35,151],                     # 特になし：平均的
         initiative=0),

    dict(no=13, name="羽森つばさ",   nick="つばさ",
         hp=1800, sp=1600,
         talents=[0,25,17,28,30,31,113,223,108,151],      # B敏感：アイドル・魅力的
         initiative=5, singing=3),

    dict(no=14, name="花音ことり",   nick="ことり",
         hp=1700, sp=1400,
         talents=[0,16,12,30,35,113,223,102,151],         # C敏感：生意気だが可憐
         initiative=10, singing=3),

    dict(no=15, name="長町やえ",     nick="やえ",
         hp=2000, sp=1800,
         talents=[0,13,25,100,30,35,111,104,151],         # V敏感：素直・小柄
         initiative=-5),

    # ───── 1年C組 ─────
    dict(no=16, name="大虎いさみ",   nick="いさみ",
         hp=2500, sp=1500,
         talents=[0,25,12,20,110,30,35,41,108,151],       # B敏感：巨乳
         initiative=20),

    dict(no=17, name="小鳩あずさ",   nick="あずさ",
         hp=1000, sp=1200,
         talents=[0,13,25,35,30,42,221,102,104,151],      # C敏感+V敏感：濡れやすい・大人しい
         initiative=-20),

    dict(no=18, name="熊沢ひめの",   nick="ひめの",
         hp=2200, sp=1300,
         talents=[0,25,13,100,30,35,220,105,151],         # A鈍感：怪力・体が丈夫
         initiative=5),

    dict(no=19, name="猫塚みけ",     nick="みけ",
         hp=1800, sp=1400,
         talents=[0,23,25,35,30,42,104,151],              # V敏感：濡れやすい・好奇心
         initiative=-5),

    dict(no=20, name="藤猪しずく",   nick="しずく",
         hp=1400, sp=1100,
         talents=[0,14,24,35,30,102,108,151],             # C敏感+B敏感：大人しい・保守的
         initiative=-15),

    dict(no=21, name="雉子すみれ",   nick="すみれ",
         hp=1400, sp=1200,
         talents=[0,15,20,24,27,30,35,107,151],           # B鈍感+一線越えない：プライド高・自制心・禁欲的
         initiative=10),

    dict(no=22, name="鯱いかり",     nick="いかり",
         hp=2200, sp=1600,
         talents=[0,11,23,28,30,31,70,41,107,151],        # B鈍感：気丈・痛みに強い
         initiative=20),

    dict(no=23, name="鶯木こはる",   nick="こはる",
         hp=2000, sp=1700,
         talents=[0,23,13,30,35,104,151],                 # V敏感：素直・好奇心
         initiative=0, cooking=2),

    # ───── 2年A組 ─────
    dict(no=24, name="三波なつみ",   nick="なつみ",
         hp=1700, sp=1600,
         talents=[0,13,25,63,30,35,108,151],              # B敏感：素直・献身的
         initiative=-5, cooking=3),

    dict(no=25, name="八朔つゆり",   nick="つゆり",
         hp=800,  sp=900,
         talents=[0,14,26,35,30,40,42,112,102,104,151],   # C敏感+V敏感：痛みに弱い・濡れやすい
         initiative=-25),

    dict(no=26, name="堀田さあや",   nick="さあや",
         hp=2000, sp=1500,
         talents=[0,12,20,13,35,30,105,151],              # A鈍感：気丈・自制心
         initiative=10),

    dict(no=27, name="夏野ゆり",     nick="ゆり",
         hp=1700, sp=1400,
         talents=[0,15,20,82,12,27,30,101,151],           # C鈍感+一線越えない：男嫌い・極度に禁欲的
         initiative=20, singing=2),

    dict(no=28, name="星海こよい",   nick="こよい",
         hp=1200, sp=1000,
         talents=[0,14,10,35,30,26,102,108,151],          # C敏感+B敏感：臆病・大人しい
         initiative=-25),

    dict(no=29, name="春風なな",     nick="なな",
         hp=2000, sp=1700,
         talents=[0,25,28,30,31,70,102,104,151],          # C敏感+V敏感：快感に素直
         initiative=5),

    dict(no=30, name="長居ゆう",     nick="ゆう",
         hp=1600, sp=1400,
         talents=[0,21,87,25,30,107,151],                 # B鈍感：無関心・小悪魔
         initiative=15, singing=2),

    # ───── 2年B組 ─────
    dict(no=31, name="夢路まりあ",   nick="まりあ",
         hp=1200, sp=1200,
         talents=[0,13,25,63,35,30,42,221,102,104,151],   # C敏感+V敏感：濡れやすい・献身的
         initiative=-20),

    dict(no=32, name="安条まい",     nick="まい",
         hp=1600, sp=1500,
         talents=[0,28,25,30,108,151],                    # B敏感：目立ちたがり
         initiative=10),

    dict(no=33, name="柊るな",       nick="るな",
         hp=2000, sp=1600,
         talents=[0,16,23,87,30,31,106,151],              # A敏感：貞操無頓着・経験あり気
         initiative=20),

    dict(no=34, name="桐島かいり",   nick="かいり",
         hp=1400, sp=1200,
         talents=[0,15,18,35,30,102,151],                 # C敏感：ツンデレ
         initiative=5, singing=2),

    dict(no=35, name="梅園かな",     nick="かな",
         hp=1900, sp=1400,
         talents=[0,15,12,11,30,35,107,151],              # B鈍感：気丈・プライド高
         initiative=15),

    dict(no=36, name="遠見ちか",     nick="ちか",
         hp=1600, sp=1300,
         talents=[0,16,11,35,30,101,151],                 # C鈍感：生意気・反抗的
         initiative=5),

    dict(no=37, name="龍泉寺レンレン", nick="レンレン",
         hp=2300, sp=1700,
         talents=[0,11,23,12,30,70,41,104,151],           # V敏感：快感に素直
         initiative=25),

    # ───── 2年C組 ─────
    dict(no=38, name="クー・カロア", nick="カロア",
         hp=2200, sp=1800,
         talents=[0,13,25,23,30,31,70,111,102,104,151],   # C敏感+V敏感：快感に素直
         initiative=5),

    dict(no=39, name="冴木もも",     nick="もも",
         hp=1300, sp=1200,
         talents=[0,21,22,30,35,100,101,107,151],         # C鈍感+B鈍感：無関心・感情乏しい
         initiative=-5),

    dict(no=40, name="夜霧はやて",   nick="はやて",
         hp=2300, sp=1800,
         talents=[0,12,25,63,30,35,41,105,151],           # A鈍感：気丈・痛みに強い
         initiative=20),

    dict(no=41, name="悠木ともこ",   nick="ともこ",
         hp=2000, sp=1500,
         talents=[0,12,20,30,35,107,151],                 # B鈍感：気丈・自制心
         initiative=15),

    dict(no=42, name="榊むつみ",     nick="むつみ",
         hp=2100, sp=1600,
         talents=[0,16,23,30,31,106,151],                 # A敏感：貞操無頓着・積極的
         initiative=15),

    dict(no=43, name="砂賀みどり",   nick="みどり",
         hp=1500, sp=1300,
         talents=[0,14,25,35,30,102,151],                 # C敏感：大人しい・恥じらい
         initiative=-10),

    dict(no=44, name="笹芽ひよの",   nick="ひよの",
         hp=1500, sp=1300,
         talents=[0,10,35,23,30,108,151],                 # B敏感：臆病・好奇心
         initiative=-15),

    # ───── 3年A組 ─────
    dict(no=45, name="円城寺れいか", nick="れいか",
         hp=1800, sp=1600,
         talents=[0,15,113,20,30,35,110,108,151],         # B敏感：巨乳
         initiative=20, singing=1),

    dict(no=46, name="双葉みづき",   nick="みづき",
         hp=1200, sp=1400,
         talents=[0,21,22,30,100,222,101,151],            # C鈍感：無関心・感情乏しい
         initiative=0),

    dict(no=47, name="双葉みなづき", nick="みなづき",
         hp=1200, sp=1300,
         talents=[0,14,24,30,35,100,222,102,151],         # C敏感：大人しい・繊細な霊感持ち
         initiative=-10),

    dict(no=48, name="四方みつる",   nick="みつる",         # 恋慕(85)削除：攻略後に付与
         hp=2200, sp=1700,
         talents=[0,13,113,30,35,102,108,151],            # C敏感+B敏感：素直・魅力的
         initiative=15),

    dict(no=49, name="小松ぼたん",   nick="ぼたん",
         hp=1900, sp=1500,
         talents=[0,13,25,30,35,104,151],                 # V敏感：素直・楽観的
         initiative=0),

    dict(no=50, name="山條ぎん",     nick="ぎん",
         hp=2400, sp=1800,
         talents=[0,12,79,23,30,37,40,80,106,151],        # A敏感+倒錯的：マゾ・SM系に反応
         initiative=-10),

    dict(no=51, name="御影かすみ",   nick="かすみ",
         hp=1600, sp=1300,
         talents=[0,21,22,30,107,151],                    # B鈍感：無関心・感情乏しい
         initiative=-5, cooking=3),

    dict(no=52, name="湖南やこ",     nick="やこ",
         hp=1800, sp=1600,
         talents=[0,12,11,16,30,83,105,151],              # A鈍感：サド・自分は感じない
         initiative=25),

    dict(no=53, name="花丘まり",     nick="まり",
         hp=2000, sp=1500,
         talents=[0,25,21,30,35,108,151],                 # B敏感：明るい・楽観的
         initiative=5),

    # ───── 3年B組 ─────
    dict(no=54, name="久坂あやめ",   nick="あやめ",
         hp=1700, sp=1400,
         talents=[0,12,23,30,35,104,151],                 # V敏感：好奇心・気丈
         initiative=15),

    dict(no=55, name="伊藤さくら",   nick="さくら",
         hp=1500, sp=1300,
         talents=[0,15,20,113,30,35,102,151],             # C敏感：魅力的・プライド高
         initiative=10),

    dict(no=56, name="八壁ひかる",   nick="ひかる",
         hp=2400, sp=1700,
         talents=[0,12,25,100,30,35,41,105,151],          # A鈍感：気丈・小柄・痛みに強い
         initiative=20),

    dict(no=57, name="岩戸サン",     nick="サン",
         hp=2300, sp=1600,
         talents=[0,12,20,21,30,35,107,151],              # B鈍感：無関心・自制心
         initiative=20),

    dict(no=58, name="天宮るり",     nick="るり",
         hp=1300, sp=1500,
         talents=[0,22,24,30,35,108,151],                 # B敏感：保守的・感情乏しいが胸は敏感
         initiative=0),

    dict(no=59, name="水嶌うしお",   nick="うしお",
         hp=2000, sp=1300,
         talents=[0,14,10,35,30,42,102,104,151],          # C敏感追加：臆病・濡れやすい
         initiative=-15),

    dict(no=60, name="瀬川かえで",   nick="かえで",
         hp=1700, sp=1600,
         talents=[0,15,83,87,30,36,52,80,105,151],        # A鈍感+倒錯的：サド・SM系で攻める側
         initiative=30),

    dict(no=61, name="鶴海ひまり",   nick="ひまり",
         hp=1400, sp=1600,
         talents=[0,13,25,23,35,30,108,151],              # B敏感：素直・楽観的
         initiative=-5),

    dict(no=62, name="黒森すず",     nick="すず",
         hp=1600, sp=1500,
         talents=[0,16,15,30,35,101,151],                 # C鈍感：生意気・プライド高
         initiative=10),

    # ───── 3年C組 ─────
    dict(no=63, name="八雲ちづる",   nick="ちづる",         # 恋慕(85)削除：攻略後に付与
         hp=1500, sp=1500,
         talents=[0,28,23,35,30,42,102,104,151],          # C敏感+V敏感：濡れやすい・目立ちたがり
         initiative=0),

    dict(no=64, name="峰山しおん",   nick="しおん",
         hp=1300, sp=1200,
         talents=[0,14,21,24,30,35,101,151],              # C鈍感：無関心・保守的
         initiative=-15),

    dict(no=65, name="時国そら",     nick="そら",
         hp=1200, sp=1500,
         talents=[0,22,21,30,35,222,107,151],             # B鈍感：感情乏しい・無関心
         initiative=-5),

    dict(no=66, name="曽根セイラ",   nick="セイラ",
         hp=900,  sp=1100,
         talents=[0,10,26,35,30,40,42,112,102,104,151],   # C敏感+V敏感：臆病・濡れやすい・痛みに弱い
         initiative=-25, singing=2),

    dict(no=67, name="日滝ましろ",   nick="ましろ",         # 淫乳(78)削除
         hp=2100, sp=1800,
         talents=[0,25,28,31,110,70,106,108,151],         # A敏感+B敏感：巨乳・快感に素直・経験あり
         initiative=5),

    dict(no=68, name="深鳥ふみ",     nick="ふみ",
         hp=1700, sp=1500,
         talents=[0,12,23,30,35,104,151],                 # V敏感：好奇心・気丈
         initiative=15),

    dict(no=69, name="神樹はじめ",   nick="はじめ",
         hp=1600, sp=1700,
         talents=[0,13,22,113,30,35,108,151],             # B敏感：素直・魅力的
         initiative=-5),

    dict(no=70, name="神無月ほとり", nick="ほとり",
         hp=1200, sp=1000,
         talents=[0,21,17,25,30,35,101,151],              # C鈍感：無関心・プライド低
         initiative=-20),

    dict(no=71, name="棗ひびき",     nick="ひびき",
         hp=2200, sp=1500,
         talents=[0,25,21,30,35,108,151],                 # B敏感：楽観的
         initiative=5),
]


def generate_chara_csv(chara, output_dir):
    no       = chara["no"]
    name     = chara["name"]
    nick     = chara["nick"]
    hp       = chara["hp"]
    sp       = chara["sp"]
    talents  = chara["talents"]
    init_val = chara.get("initiative", -10)
    cooking  = chara.get("cooking", 0)
    singing  = chara.get("singing", 0)

    lines = [
        f"番号,{no}",
        f"名前,{name}",
        f"呼び名,{nick}",
        f"基礎,0,{hp}",
        f"基礎,1,{sp}",
    ]

    for t in talents:
        lines.append(f"素質,{t}")

    if cooking > 0:
        lines.append(f"能力,50,{cooking}")
        lines.append(f"能力,90,{cooking}")
    if singing > 0:
        lines.append(f"能力,52,{singing}")
        lines.append(f"能力,92,{singing}")

    lines.append(f"フラグ,12,{init_val}")
    lines.append("CSTR,21,")
    lines.append("CSTR,22,")
    lines.append("CSTR,23,")
    lines.append("CSTR,24,")

    filepath = os.path.join(output_dir, f"Chara{no}.csv")
    with open(filepath, "w", encoding="cp932") as f:
        f.write("\n".join(lines) + "\n")

    return filepath


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir    = os.path.join(script_dir, "..", "CSV")

    generated = []
    for chara in CHARA_DATA:
        path = generate_chara_csv(chara, csv_dir)
        generated.append(path)
        print(f"  生成: {os.path.basename(path)}  ({chara['name']})")

    print(f"\n✓ {len(generated)} ファイル生成完了 → {os.path.abspath(csv_dir)}")
