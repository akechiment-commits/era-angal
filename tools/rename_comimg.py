#!/usr/bin/env python3
"""
コマンド画像リネームツール
resources/chara_XX/ 内の画像を正しいコマンド名に改名する

使い方:
  python rename_comimg.py list                          # コマンド名一覧を表示
  python rename_comimg.py scan <キャラ番号>              # フォルダ内ファイルを一覧
  python rename_comimg.py rename <キャラ番号> <元ファイル名> <コマンド名語幹> [renbo]
  python rename_comimg.py batch <キャラ番号> <マッピングCSV>

例:
  python rename_comimg.py rename 1 img001.png kaiwa
  python rename_comimg.py rename 1 img002.png kaiwa renbo
  python rename_comimg.py batch 1 my_renames.csv

マッピングCSV の書式（1行1件、コメント行は ; で始める）:
  img001.png,kaiwa
  img002.png,kaiwa,renbo
  img003.png,benkyou
"""

import sys
import os
import shutil

# SELECTCOM → (コマンド名, ファイル名語幹) の完全マッピング
COMMANDS = [
    # 純愛コミュニケーション系 (COM300-399)
    (300, "一緒に勉強する", "benkyou"),
    (301, "会話", "kaiwa"),
    (302, "プレゼント", "present"),
    (303, "スキンシップ", "skinship"),
    (304, "まったりする", "mattari"),
    (305, "掃除当番", "souji"),
    (306, "髪梳き", "kamisuki"),
    (307, "櫛で梳かす", "kushi"),
    (309, "素材探し", "sozai"),
    (310, "調合", "chogou"),
    (311, "甘い言葉", "amaikotoba"),
    (312, "頭を撫でる", "atama"),
    (313, "願掛け", "negai"),
    (314, "炬燵にあたる", "kotatsu"),
    (315, "お散歩する", "osanpo"),
    (316, "髪を梳いて貰う", "kamikashite"),
    (320, "学食に行く", "gakushoku"),
    (321, "遊びに行く", "asobi"),
    (322, "ストリートライブ", "live"),
    (323, "デート", "date"),
    (340, "バードキス", "bird_kiss"),
    (341, "ソフトキス", "soft_kiss"),
    (342, "ディープキス", "deep_kiss"),
    (360, "胸愛撫（着衣）", "mune_aibu_cha"),
    (361, "愛撫（着衣）", "aibu_cha"),
    (362, "指挿入れ（着衣）", "yubi_cha"),
    (363, "着衣挿入", "insert_cha"),
    (364, "着衣Ｇスポット刺激", "gspot_cha"),
    (365, "着衣後背位", "doggy_cha"),
    (366, "着衣騎乗位", "cowgirl_cha"),
    (367, "着衣ローター", "roter_cha"),
    (368, "炬燵かがり", "kotatsu_kagari"),
    (370, "抱き合う", "dakiawu"),
    (371, "オムツ", "omutsu"),
    (372, "尻愛撫", "shiri_aibu_cha"),
    (373, "フェラチオ（着衣）", "fellatio_cha"),
    (380, "フェラする（着衣）", "fellatio_s"),
    (381, "セックスさせる（着衣）", "sex_s"),
    (390, "ゲームセンター", "game_center"),
    (391, "衣装替え", "ishou"),
    (392, "衣装破り", "ishou_yaburi"),
    (393, "見つめあう", "mitsumeau"),
    (399, "告白する", "kokuhaku"),
    # ウフフ通常系 (COM0-257)
    (0,  "愛撫", "aibu"),
    (1,  "クンニ", "kunni"),
    (2,  "アナル愛撫", "anal_aibu"),
    (3,  "自慰", "jii"),
    (4,  "フェラする", "fela"),
    (5,  "胸愛撫", "mune_aibu"),
    (6,  "キスする", "kisu"),
    (7,  "何もしない", "nanimosinai"),
    (8,  "指挿入れ", "yubi"),
    (9,  "アナル舐め", "anal_name"),
    (10, "ローター", "roter"),
    (18, "シャワー", "shower"),
    (19, "アナルビーズ", "anal_beads"),
    (20, "正常位", "missionary"),
    (21, "後背位", "doggy"),
    (22, "アナルセックス", "anal_sex"),
    (23, "逆レイプ", "gyaku_rape"),
    (24, "対面座位", "taimen"),
    (25, "背面座位", "haimen"),
    (26, "正常位アナル", "missionary_anal"),
    (27, "後背位アナル", "doggy_anal"),
    (28, "対面座位アナル", "taimen_anal"),
    (29, "背面座位アナル", "haimen_anal"),
    (30, "手淫", "shuin"),
    (31, "フェラチオ", "fellatio"),
    (32, "パイズリ", "paizuri"),
    (33, "素股", "sumata"),
    (34, "騎乗位", "cowgirl"),
    (35, "泡踊り", "awa_odori"),
    (36, "騎乗位アナル", "cowgirl_anal"),
    (37, "足扱き", "ashidaki"),
    (38, "尻素股", "shiri_sumata"),
    (39, "オナホ手淫", "onaho"),
    (40, "スパンキング", "spanking"),
    (41, "鞭", "muchi"),
    (42, "針", "hari"),
    (43, "アイマスク", "eyemask"),
    (44, "縄", "nawa"),
    (45, "ボールギャグ", "ball_gag"),
    (46, "浣腸器＋プラグ", "kanchou"),
    (50, "ローション", "lotion"),
    (51, "媚薬", "biyaku"),
    (52, "利尿剤", "rinyou"),
    (53, "ビデオカメラ", "video"),
    (54, "野外プレイ", "outdoor"),
    (56, "助手を犯す", "joshu_okasu"),
    (57, "羞恥プレイ", "shuchi"),
    (58, "お風呂場プレイ", "ofuro"),
    (59, "新妻プレイ", "niizuma"),
    (61, "クンニ強制", "kunni_kyosei"),
    (63, "貝あわせ", "kaiawase"),
    (65, "助手を犯させる", "joshu_okasaseru"),
    (66, "Ｗフェラ", "w_fela"),
    (67, "足コキする", "ashikoki"),
    (68, "ダブルフェラ", "double_fela"),
    (71, "秘貝開帳", "hikaichoukai"),
    (75, "言葉責め", "kotoba_seme"),
    (80, "イラマチオ", "irrumatio"),
    (85, "放尿", "hounyou"),
    (90, "アナル愛撫させる", "anal_aibu_sase"),
    (110, "クスコ", "kusuko"),
    (120, "キス正常位", "kiss_missionary"),
    (121, "キス後背位", "kiss_doggy"),
    (122, "キス対面座位", "kiss_taimen"),
    (123, "キス背面座位", "kiss_haimen"),
    (124, "キス騎乗位", "kiss_cowgirl"),
    (130, "目隠しされる", "mekakushi"),
    (131, "拘束される", "kousoku"),
    (132, "口枷される", "kuchikase"),
    (181, "コンドーム", "condom"),
    (182, "コンドーム精飲(P)", "condom_seiin_p"),
    (183, "コンドーム精飲(A)", "condom_seiin_a"),
    (184, "コンドーム精飲(M)", "condom_seiin_m"),
    (185, "口移し", "kuchiwatashi"),
    (186, "排卵誘発剤", "hairan"),
    (187, "緊急避妊薬", "hinin"),
    (190, "優しくする", "yasashiku"),
    (191, "手淫する", "shuin_suru"),
    (192, "パイズリする", "paizuri_suru"),
    (193, "正常位させる", "missionary_sase"),
    (194, "後背位させる", "doggy_sase"),
    (195, "騎乗位する", "cowgirl_suru"),
    (196, "ペニバン挿入", "peniban"),
    (197, "お風呂を楽しむ", "ofuro_enjoy"),
    (198, "お外を楽しむ", "outdoor_enjoy"),
    (199, "お嫁さんで楽しむ", "niizuma_enjoy"),
    (200, "乳の揉み合い", "chichi_momi"),
    (201, "指フェラ", "yubi_fela"),
    (203, "クスコされる", "kusuko_sareru"),
    (204, "アナルに入れさせる", "anal_iresa"),
    (205, "自慰見せつけ", "jii_misetsuke"),
    (255, "挿入Ｇスポ責め", "insert_gspot"),
    (256, "挿入子宮口責め", "insert_shikyu"),
    (257, "剃毛プレイ", "teimou"),
    # 独自コマンド
    (280, "独自ウフフ①", "com280"),
    (281, "独自ウフフ②", "com281"),
    (282, "独自ウフフ③", "com282"),
    (283, "独自ウフフ④", "com283"),
    (284, "独自ウフフ⑤", "com284"),
    (410, "独自純愛①", "com410"),
    (411, "独自純愛②", "com411"),
    (412, "独自純愛③", "com412"),
    (413, "独自純愛④", "com413"),
    (414, "独自純愛⑤", "com414"),
]

STEM_TO_INFO = {stem: (cid, jname) for cid, jname, stem in COMMANDS}
VALID_EXTS = {".png", ".jpg", ".jpeg", ".bmp"}


def repo_root():
    """このスクリプトの1つ上がリポジトリルート"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def chara_folder(chara_num):
    return os.path.join(repo_root(), "resources", f"chara_{int(chara_num):02d}")


def cmd_list(_args):
    """コマンド名一覧を表示"""
    print(f"{'COM':>5}  {'コマンド名':<20}  ファイル名語幹")
    print("-" * 55)
    for cid, jname, stem in sorted(COMMANDS, key=lambda x: x[0]):
        print(f"  {cid:>3}  {jname:<20}  {stem}")


def cmd_scan(args):
    """キャラフォルダ内のファイルを一覧表示"""
    if not args:
        print("使い方: scan <キャラ番号>")
        sys.exit(1)
    folder = chara_folder(args[0])
    if not os.path.isdir(folder):
        print(f"フォルダが存在しません: {folder}")
        sys.exit(1)

    files = sorted(f for f in os.listdir(folder)
                   if os.path.splitext(f)[1].lower() in VALID_EXTS)
    if not files:
        print(f"{folder} に画像ファイルがありません")
        return

    known_stems = {stem for _, _, stem in COMMANDS}
    print(f"{'ファイル名':<35}  状態")
    print("-" * 55)
    for f in files:
        stem = os.path.splitext(f)[0].removesuffix("_renbo")
        if stem in known_stems:
            cid, jname = STEM_TO_INFO[stem]
            suffix = "（恋慕）" if f.endswith("_renbo" + os.path.splitext(f)[1]) else ""
            print(f"  {f:<33}  ✓ COM{cid} {jname}{suffix}")
        else:
            print(f"  {f:<33}  ？ 未マッピング")


def do_rename(src_path, dst_path):
    """実際のリネーム（移動）処理"""
    if not os.path.exists(src_path):
        print(f"  エラー: 元ファイルが存在しません: {src_path}")
        return False
    if os.path.exists(dst_path):
        print(f"  警告: コピー先が既に存在します: {dst_path}")
        ans = input("  上書きしますか？ [y/N]: ").strip().lower()
        if ans != "y":
            print("  スキップ")
            return False
    os.rename(src_path, dst_path)
    print(f"  {os.path.basename(src_path)} → {os.path.basename(dst_path)}")
    return True


def cmd_rename(args):
    """1ファイルをリネーム"""
    if len(args) < 3:
        print("使い方: rename <キャラ番号> <元ファイル名> <コマンド名語幹> [renbo]")
        print("例:     rename 1 img001.png kaiwa")
        print("例:     rename 1 img002.png kaiwa renbo")
        sys.exit(1)

    chara_num, src_name, stem = args[0], args[1], args[2]
    renbo = len(args) >= 4 and args[3].lower() == "renbo"

    if stem not in STEM_TO_INFO:
        print(f"エラー: 未知のコマンド語幹: {stem}")
        print("  python rename_comimg.py list で有効な語幹を確認してください")
        sys.exit(1)

    cid, jname = STEM_TO_INFO[stem]
    folder = chara_folder(chara_num)
    ext = os.path.splitext(src_name)[1].lower() or ".png"
    dst_stem = f"{stem}_renbo" if renbo else stem
    dst_name = dst_stem + ext

    src_path = os.path.join(folder, src_name)
    dst_path = os.path.join(folder, dst_name)

    suffix = "（恋慕）" if renbo else "（通常）"
    print(f"COM{cid} {jname}{suffix}")
    do_rename(src_path, dst_path)


def cmd_batch(args):
    """CSVファイルからまとめてリネーム"""
    if len(args) < 2:
        print("使い方: batch <キャラ番号> <マッピングCSV>")
        print()
        print("CSVの書式（; でコメント）:")
        print("  元ファイル名,コマンド名語幹[,renbo]")
        print("  img001.png,kaiwa")
        print("  img002.png,kaiwa,renbo")
        sys.exit(1)

    chara_num, csv_path = args[0], args[1]
    folder = chara_folder(chara_num)

    if not os.path.exists(csv_path):
        # スクリプトと同じフォルダも探す
        alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_path)
        if os.path.exists(alt):
            csv_path = alt
        else:
            print(f"CSVファイルが見つかりません: {csv_path}")
            sys.exit(1)

    ok = err = 0
    with open(csv_path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith(";") or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                print(f"  行{lineno}: 書式エラー（スキップ）: {line}")
                err += 1
                continue
            src_name = parts[0]
            stem = parts[1]
            renbo = len(parts) >= 3 and parts[2].lower() == "renbo"

            if stem not in STEM_TO_INFO:
                print(f"  行{lineno}: 未知の語幹 '{stem}'（スキップ）")
                err += 1
                continue

            ext = os.path.splitext(src_name)[1].lower() or ".png"
            dst_name = (f"{stem}_renbo" if renbo else stem) + ext
            if do_rename(os.path.join(folder, src_name),
                         os.path.join(folder, dst_name)):
                ok += 1
            else:
                err += 1

    print(f"\n完了: {ok}件成功 / {err}件失敗")


CMDS = {"list": cmd_list, "scan": cmd_scan, "rename": cmd_rename, "batch": cmd_batch}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        sys.exit(0)
    CMDS[sys.argv[1]](sys.argv[2:])
