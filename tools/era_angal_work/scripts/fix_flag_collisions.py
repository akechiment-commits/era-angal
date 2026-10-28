from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ERB = ROOT / "ERB"
FLAG_CSV = ROOT / "CSV" / "Flag.csv"


def read_erb(path: Path) -> str:
    return path.read_bytes().decode("cp932")


def write_erb(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(text.replace("\n", "\r\n").encode("cp932"))


def document_flag_csv() -> None:
    text = FLAG_CSV.read_bytes().decode("cp932")
    marker = ";-----あんガル追加システム専用領域（J-50）-----"
    if marker in text:
        return
    block = """

;-----あんガル追加システム専用領域（J-50）-----
;15000～15004 ガチャ通貨（ダイヤ、ブロンズ、シルバー、ゴールド、プラチナ）
;15005～15007 学校行事補助値、ログイン最終受取日
;15010～15015 イベント別エリア番号
;15020～15025 イベント別月内報酬受取数
15030,子ども手当最終支給期間,;DAY:7/10+1。0は移行前
15031,子宝図鑑解放
15040,学校行事元TARGET
15041,学校行事一時追加状態
;15050～15055 イベントボード共有進行状態
;15060～15065 体育祭・文化祭・クイズの実施年と優勝回数
15099,追加FLAG領域移行バージョン
;15100～15200 調合素材発見状態
;16000～16002 調教セッション集計
;16010～16509 調教セッション使用コマンド印
"""
    write_erb(FLAG_CSV, text.rstrip("\r\n") + block)


def replace_exact(text: str, old: str, new: str, expected: int | None = None) -> str:
    count = text.count(old)
    if expected is not None and count != expected:
        raise RuntimeError(f"expected {expected} occurrences of {old!r}, found {count}")
    return text.replace(old, new)


def migrate_static_low_flags() -> None:
    mapping = {
        112: 15000,  # キミサキダイヤ
        113: 15001,  # ブロンズチケット
        114: 15002,  # シルバーチケット
        115: 15003,  # ゴールドチケット
        116: 15004,  # プラチナチケット
        117: 15005,  # 学校行事の実施年
        118: 15006,  # 学校行事の難度
        119: 15007,  # ログインボーナス最終受取日
        121: 15030,  # 子ども手当の最終支給期間
        122: 15031,  # 子宝図鑑解放
        198: 15040,  # 学校行事用一時TARGET
        199: 15041,  # 学校行事用一時追加状態
        50: 15060,  # 体育祭実施年
        51: 15061,  # 文化祭実施年
        52: 15062,  # 体育祭優勝回数
        53: 15063,  # 文化祭大成功回数
        54: 15064,  # クイズ選手権実施年
        55: 15065,  # クイズ選手権優勝回数
    }
    pattern = re.compile(r"(?<![A-Z])FLAG:(" + "|".join(map(str, mapping)) + r")\b")
    for path in ERB.rglob("*.ERB"):
        text = read_erb(path)
        updated = pattern.sub(lambda match: f"FLAG:{mapping[int(match.group(1))]}", text)
        if updated != text:
            write_erb(path, updated)


def migrate_event_board_ranges() -> None:
    path = ERB / "EVENT_BOARD_イベントボード周回.ERB"
    text = read_erb(path)
    if "FLAG:(15010 + COUNT)" in text:
        return
    replacements = {
        "FLAG:(98 + COUNT)": "FLAG:(15010 + COUNT)",
        "A = FLAG:68 + 98": "A = FLAG:68 + 15010",
        "FLAG:(104 + COUNT) = 0\t;イベント別マイルストーン達成数\r\n": "",
        "FLAG:(120 + COUNT)": "FLAG:(15020 + COUNT)",
        "A = 120 + FLAG:68": "A = 15020 + FLAG:68",
        "LOCAL:0 = 120 + FLAG:68": "LOCAL:0 = 15020 + FLAG:68",
        "LOCAL:1 = 120 + FLAG:68": "LOCAL:1 = 15020 + FLAG:68",
        "FLAG:(127 + COUNT) = 0\t;旧累計PTを消去（以後は月間PTへ一本化）\r\n": "",
    }
    for old, new in replacements.items():
        text = replace_exact(text, old, new)
    text = replace_exact(
        text,
        ";   FLAG:71～76 = 今月各イベントポイント（月初リセット）",
        ";   FLAG:71～76 = 今月各イベントポイント（月初リセット）\r\n"
        ";   FLAG:15010～15015 = イベント別エリア番号\r\n"
        ";   FLAG:15020～15025 = 今月イベント別報酬受取数",
        expected=1,
    )
    write_erb(path, text)


def migrate_event_board_work_flags() -> None:
    path = ERB / "EVENT_BOARD_イベントボード周回.ERB"
    text = read_erb(path)
    mapping = {33: 15050, 34: 15051, 35: 15052, 36: 15053, 37: 15054, 38: 15055}
    pattern = re.compile(r"(?<![A-Z])FLAG:(" + "|".join(map(str, mapping)) + r")\b")
    text = pattern.sub(lambda match: f"FLAG:{mapping[int(match.group(1))]}", text)
    text = text.replace("FLAG:32 = 0\r\n", "")
    text = text.replace(";   FLAG:32  = 未使用（廃止）\r\n", "")
    text = text.replace(
        "\tFLAG:(71 + COUNT) = 0\t;イベント別月間PT\r\n"
        "\tFLAG:(15010 + COUNT) = 1\t;イベント別エリア番号\r\n"
        "\t\tFLAG:(15020 + COUNT) = 0\t;イベント別報酬受取数\r\n"
        "\tREND",
        "\tFLAG:(71 + COUNT) = 0\t;イベント別月間PT\r\n"
        "\tFLAG:(15010 + COUNT) = 1\t;イベント別エリア番号\r\n"
        "\tFLAG:(15020 + COUNT) = 0\t;イベント別報酬受取数\r\n"
        "REND",
    )
    write_erb(path, text)

    ending = ERB / "ENDING_エンディング・ゲーム終了判定.ERB"
    text = read_erb(ending)
    start_marker = "\t;月変わり検出 → イベントポイント月次リセット＆報酬\r\n"
    end_marker = "\t;月次定期戦（毎ターン通るここで確実に発火）\r\n"
    if start_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    text = text.replace("\t\t\tFLAG:31 = 0\r\n", "")
    text = text.replace("\t\t\tFLAG:32 = 0\r\n", "")
    text = text.replace("FLAG:31 = 0\t;月変わり検出リセット\r\n", "")
    text = text.replace("FLAG:32 = 0\t;月次イベントPTリセット\r\n", "")
    text = text.replace("FLAG:33 = 0\t;月次学期リセット", "FLAG:15050 = 0\t;すごろく盤面位置リセット")
    write_erb(ending, text)

    stage = ERB / "STAGE_学期進行・試験システム.ERB"
    text = read_erb(stage)
    text = text.replace(
        "PRINTFORML 今月イベントPT:{FLAG:32}　体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}",
        "PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}",
    )
    text = text.replace("\t\tFLAG:31 = 0\r\n", "")
    text = text.replace("\t\tFLAG:32 = 0\r\n", "")
    write_erb(stage, text)


def migrate_material_flags() -> None:
    path = ERB / "COMF" / "COMF310.ERB"
    text = read_erb(path)
    text = text.replace("FLAG:(3000+LOCAL)", "FLAG:(15100+LOCAL)")
    text = text.replace("FLAG:(3000+(LOCAL:2))", "FLAG:(15100+(LOCAL:2))")
    text = text.replace("FLAG:(2100+A)", "FLAG:(14200+A)")
    write_erb(path, text)


def migrate_training_work_flags() -> None:
    mapping = {"FLAG:400": "FLAG:16000", "FLAG:401": "FLAG:16001", "FLAG:402": "FLAG:16002"}
    for relative in ("AFTERTRA_調教後処理.ERB", "USERCOM_コマンド一覧表示.ERB"):
        path = ERB / relative
        text = read_erb(path)
        for old, new in mapping.items():
            text = re.sub(re.escape(old) + r"\b", new, text)
        text = text.replace("FLAG:(500 + SELECTCOM)", "FLAG:(16010 + SELECTCOM)")
        text = text.replace("FLAG:(500 + LOCAL:0)", "FLAG:(16010 + LOCAL:0)")
        text = text.replace(
            "FLAG:(500+SELECTCOM)を使用済みマーク",
            "FLAG:(16010+SELECTCOM)を使用済みマーク",
        )
        write_erb(path, text)


def add_migration_calls() -> None:
    shop = ERB / "SHOP_ショップ.ERB"
    text = read_erb(shop)
    if "CALL CUSTOM_FLAG_MIGRATION" not in text:
        text = replace_exact(
            text,
            "CALL SAVEDATA_CONVERT\r\n;グローバル変数読み込み",
            "CALL SAVEDATA_CONVERT\r\n"
            ";追加システムが旧予約領域へ書き込んでいたセーブを一度だけ移行\r\n"
            "CALL CUSTOM_FLAG_MIGRATION\r\n"
            ";グローバル変数読み込み",
            expected=1,
        )
        write_erb(shop, text)

    system = ERB / "SYSTEM_基本システム処理.ERB"
    text = read_erb(system)
    if "CALL CUSTOM_FLAG_MIGRATION" not in text:
        text = replace_exact(
            text,
            "FLAG:15007 = 0\r\nLOADGLOBAL",
            ";ニューゲームでもログイン報酬の前に新フラグ領域を初期化\r\n"
            "CALL CUSTOM_FLAG_MIGRATION\r\n"
            "FLAG:15007 = 0\r\n"
            "LOADGLOBAL",
            expected=1,
        )
        write_erb(system, text)


def rewrite_child_allowance() -> None:
    path = ERB / "EVENT_MORNING_朝のイベント.ERB"
    text = read_erb(path)
    if "FLAG:15030 = 最終支給期間+1" in text:
        return
    start = text.index(";-------------------------------------------------\r\n; 子ども手当")
    function_start = text.index("@CHILD_ALLOWANCE_CHECK", start)
    end = text.index("@NINSSINXTU", function_start)
    replacement = """;-------------------------------------------------\r
; 子ども手当（毎月＝ゲーム内10日ごとに1回支給）\r
;   FLAG:15030 = 最終支給期間+1（0は移行前）\r
;   FLAG:15031 = 子宝図鑑解放\r
;   全キャラの累計出産数(EXP:61)に応じて資金＋キミサキダイヤ少量\r
;   ※金額はLOCAL:2/LOCAL:3の係数で調整可\r
;-------------------------------------------------\r
@CHILD_ALLOWANCE_CHECK\r
LOCAL:0 = DAY:7 / 10 + 1\r
;累計出産数を集計\r
LOCAL:1 = 0\r
REPEAT CHARANUM\r
\tLOCAL:1 += EXP:COUNT:61\r
REND\r
;子供がいれば子宝図鑑を解放（既存セーブ救済）\r
SIF LOCAL:1 > 0\r
\tFLAG:15031 = 1\r
;移行前のセーブは現在期間を支給済みとして登録し、重複支給を防ぐ\r
IF FLAG:15030 == 0\r
\tFLAG:15030 = LOCAL:0\r
\tRETURN 0\r
ENDIF\r
SIF FLAG:15030 == LOCAL:0\r
\tRETURN 0\r
FLAG:15030 = LOCAL:0\r
SIF LOCAL:1 <= 0\r
\tRETURN 0\r
;支給額（資金=人数×10000 / ダイヤ=人数×1）\r
LOCAL:2 = LOCAL:1 * 10000\r
LOCAL:3 = LOCAL:1\r
MONEY += LOCAL:2\r
FLAG:15000 += LOCAL:3\r
DRAWLINE\r
PRINTFORML ★ 子ども手当 ★\r
PRINTFORML 学院の子ども{LOCAL:1}人ぶんの手当が支給されました\r
PRINTFORML 　資金 ＋{LOCAL:2}\r
PRINTFORML 　キミサキダイヤ ＋{LOCAL:3}\r
DRAWLINE\r
WAIT\r
RETURN 0\r
"""
    text = text[:start] + replacement + text[end:]
    write_erb(path, text)


def create_migration_erb() -> None:
    path = ERB / "FLAG_MIGRATION_フラグ領域移行.ERB"
    lines = [
        ";============================================================",
        "; 追加システム用FLAG領域の一度きり移行",
        "; 旧FLAG:101～199はキャラ別口上存在判定の予約領域。",
        "; 追加機能が誤って使用していた値を15000番台へ退避してから予約領域を復元する。",
        ";============================================================",
        "",
        "@CUSTOM_FLAG_MIGRATION",
        "SIF FLAG:15099 >= 1",
        "\tRETURN 0",
        "",
        ";ガチャ通貨・学校行事・ログインボーナス",
        "FLAG:15000 = FLAG:112",
        "FLAG:15001 = FLAG:113",
        "FLAG:15002 = FLAG:114",
        "FLAG:15003 = FLAG:115",
        "FLAG:15004 = FLAG:116",
        "FLAG:15005 = FLAG:117",
        "FLAG:15006 = FLAG:118",
        "FLAG:15007 = FLAG:119",
        "",
        ";イベント別のエリア番号と月内報酬受取数",
        "REPEAT 6",
        "\tFLAG:(15010 + COUNT) = FLAG:(98 + COUNT)",
        "\tFLAG:(15020 + COUNT) = FLAG:(120 + COUNT)",
        "REND",
        "",
        ";イベントボード共有進行状態",
        "FOR LOCAL, 0, 6",
        "\tFLAG:(15050 + LOCAL) = FLAG:(33 + LOCAL)",
        "NEXT",
        "",
        ";学校行事の実施年・優勝回数",
        "FOR LOCAL, 0, 6",
        "\tFLAG:(15060 + LOCAL) = FLAG:(50 + LOCAL)",
        "NEXT",
        "",
        ";調合素材の発見状態。旧3001～3100はカード所持数と重複していたため分離する。",
        "FOR LOCAL, 0, 101",
        "\tFLAG:(15100 + LOCAL) = FLAG:(3000 + LOCAL)",
        "NEXT",
        "",
        ";子ども関連は旧121/122を信用できないため、実データから復元する。",
        "LOCAL:0 = 0",
        "REPEAT CHARANUM",
        "\tLOCAL:0 += EXP:COUNT:61",
        "REND",
        "FLAG:15030 = DAY:7 / 10 + 1",
        "SIF LOCAL:0 > 0",
        "\tFLAG:15031 = 1",
        "",
        ";現行コードにはKOJO_NEXT_PLAY_nがないため、予約領域は全て未使用状態へ戻す。",
        "FOR LOCAL, 101, 200",
        "\tFLAG:LOCAL = 0",
        "NEXT",
        "",
        "FLAG:15099 = 1",
        "RETURN 1",
        "",
    ]
    text = "\n".join(lines)
    write_erb(path, text)


def main() -> None:
    migrate_static_low_flags()
    migrate_event_board_ranges()
    migrate_event_board_work_flags()
    migrate_material_flags()
    migrate_training_work_flags()
    add_migration_calls()
    rewrite_child_allowance()
    create_migration_erb()
    document_flag_csv()
    print("flag collision fixes applied")


if __name__ == "__main__":
    main()
