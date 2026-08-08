from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
ERB = ROOT / "ERB"
CSV = ROOT / "CSV"


class CheckFailure(AssertionError):
    pass


def read_cp932(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_bytes().decode("cp932").replace("\r\n", "\n")
    except UnicodeDecodeError as exc:
        raise CheckFailure(f"{relative_path}: CP932で読めません: {exc}") from exc


def function_body(text: str, name: str) -> str:
    pattern = re.compile(rf"^@{re.escape(name)}(?:\s|\(|,|$)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        raise CheckFailure(f"関数 @{name} が見つかりません")
    next_label = re.search(r"^@", text[match.end() :], re.MULTILINE)
    end = match.end() + next_label.start() if next_label else len(text)
    return text[match.start() : end]


def require(text: str, fragment: str, context: str) -> None:
    if fragment not in text:
        raise CheckFailure(f"{context}: 必須処理がありません: {fragment}")


def forbid(text: str, fragment: str, context: str) -> None:
    if fragment in text:
        raise CheckFailure(f"{context}: 廃止済み処理が残っています: {fragment}")


def count_top_level_arguments(arguments: str) -> int:
    arguments = arguments.strip()
    if not arguments:
        return 0
    depth = 0
    quoted = False
    count = 1
    index = 0
    while index < len(arguments):
        char = arguments[index]
        if char == '"':
            if quoted and index + 1 < len(arguments) and arguments[index + 1] == '"':
                index += 2
                continue
            quoted = not quoted
        elif not quoted:
            if char in "([{":
                depth += 1
            elif char in ")]}" and depth:
                depth -= 1
            elif char == "," and depth == 0:
                count += 1
        index += 1
    return count


def check_source_encoding_and_newlines() -> str:
    paths = sorted(
        path
        for directory in (ERB, CSV)
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in {".erb", ".csv"}
    )
    if not paths:
        raise CheckFailure("ERB/CSVファイルが見つかりません")

    errors: list[str] = []
    lf_only_paths: list[Path] = []
    for path in paths:
        relative = path.relative_to(ROOT)
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{relative}: UTF-8 BOM")
            continue
        try:
            raw.decode("cp932")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: CP932 decode error ({exc})")
            continue
        if b"\n" in raw.replace(b"\r\n", b""):
            lf_only_paths.append(relative)

    # 既存移植元にはLFのままのファイルが残っている。全件の機械変換は巨大差分に
    # なるため、今回の回帰対象（生成スクリプトで保守する主要ファイル）を必須化する。
    critical_crlf = {
        Path("ERB/PARTNER_TURN_パートナーターン.ERB"),
        Path("ERB/EVENT_BOARD_イベントボード周回.ERB"),
        Path("ERB/SYSTEM_基本システム処理.ERB"),
        Path("ERB/SELF_セルフコマンド.ERB"),
        Path("ERB/SHOP_ショップ.ERB"),
        Path("ERB/INFO_情報表示.ERB"),
    }
    for relative in sorted(critical_crlf.intersection(lf_only_paths)):
        errors.append(f"{relative}: 重要生成物にLF-only改行を含む")

    if errors:
        preview = "\n  ".join(errors[:20])
        suffix = f"\n  ...ほか{len(errors) - 20}件" if len(errors) > 20 else ""
        raise CheckFailure(f"文字コード／改行違反:\n  {preview}{suffix}")
    return (
        f"ERB/CSV {len(paths)}ファイルがCP932、重要生成物{len(critical_crlf)}件がCRLF"
        f"（既存LF改行: {len(lf_only_paths)}件）"
    )


def check_graphics_api_arity() -> str:
    targets = [
        ("ERB/EVENT_BOARD_イベントボード周回.ERB", "cp932"),
        ("tools/enhance_sugoroku_ui.py", "utf-8"),
    ]
    calls = 0
    errors: list[str] = []
    for relative, encoding in targets:
        text = (ROOT / relative).read_text(encoding=encoding)
        for line_number, line in enumerate(text.splitlines(), 1):
            code = line.split(";", 1)[0]
            match = re.search(r"\bGDRAWG\s+(.+)", code)
            if not match:
                continue
            calls += 1
            argument_count = count_top_level_arguments(match.group(1))
            if argument_count < 10:
                errors.append(
                    f"{relative}:{line_number}: GDRAWGは{argument_count}引数（最低10引数）"
                )
    if errors:
        raise CheckFailure("\n  ".join(errors))
    if calls < 2:
        raise CheckFailure("現行ERBと生成元のGDRAWG呼び出しを両方確認できません")
    return f"GDRAWG {calls}箇所が10引数以上"


def check_partner_turn_contract() -> str:
    text = read_cp932("ERB/PARTNER_TURN_パートナーターン.ERB")
    select = function_body(text, "PARTNER_TURN_SELECT")
    event_end = function_body(text, "EVENTCOMEND")
    system = read_cp932("ERB/SYSTEM_基本システム処理.ERB")
    system_end = function_body(system, "EVENTCOMEND")

    for fragment in (
        "SELECTCOM = PASSIVEMODE_CONVERT_PASSIVECOM(PREVCOM, TFLAG:53)",
        "TFLAG:53 = 0",
        "TFLAG:DOTRAIN = 1",
        "TRYCALLFORM COM_ABLE{SELECTCOM}",
        "TFLAG:DOTRAIN = DOTRAIN_BACKUP",
        "TFLAG:53 = ACTION",
        "TALENT:TARGET:153 == 0 && TALENT:TARGET:76 == 0",
        "IF ACTION_COUNT <= 0",
        "IF TFLAG:44",
    ):
        require(select, fragment, "PARTNER_TURN_SELECT")

    require(event_end, "BASE:TARGET:0 <= 0 || BASE:PLAYER:0 <= 0", "追加ターン終了境界")
    require(system_end, "IF BASE:0 <= 0 && TALENT:128", "体力0終了境界")
    require(system_end, "ELSEIF BASE:0 <= 0", "体力0終了境界")
    require(system_end, "TFLAG:301 = 1", "体力0時の事後行為抑止")
    require(system_end, "TFLAG:999 = 1", "体力0時の追加ターン抑止")
    forbid(system_end, "BASE:0 < 500", "体力1～499継続")
    return "候補変換・COM_ABLE・恋人/淫乱・体力0/1境界"


def check_event_month_reset_contract() -> str:
    board_text = read_cp932("ERB/EVENT_BOARD_イベントボード周回.ERB")
    reset = function_body(board_text, "EVENT_BOARD_MONTHLY_RESET")
    main = function_body(board_text, "EVENT_BOARD_MAIN")
    shop = read_cp932("ERB/SHOP_ショップ.ERB")
    show_shop = function_body(shop, "SHOW_SHOP")

    for fragment in (
        "MONTH_KEY = DAY:3 * 100 + DAY:8",
        "REPEAT 6",
        "FLAG:(71 + COUNT) = 0",
        "FLAG:(15010 + COUNT) = 1",
        "FLAG:(15020 + COUNT) = 0",
        "REPEAT 18",
        "FLAG:(78 + COUNT) = 1",
        "FLAG:15050 = 0",
        "FLAG:15055 = 0",
        "FLAG:15056 = 0",
        "FLAG:15057 = 0",
        "FLAG:67 = MONTH_KEY",
    ):
        require(reset, fragment, "EVENT_BOARD_MONTHLY_RESET")
    require(main, "CALL EVENT_BOARD_MONTHLY_RESET", "イベント入口")
    require(show_shop, "CALL YOUBI", "メインメニュー年月計算")
    require(show_shop, "CALL EVENT_BOARD_MONTHLY_RESET", "メインメニュー月次リセット")
    if show_shop.index("CALL YOUBI") > show_shop.index("CALL EVENT_BOARD_MONTHLY_RESET"):
        raise CheckFailure("SHOW_SHOP: 年月計算より前に月次リセットを呼んでいます")
    return "6イベント・18ミッション・共有状態を年月キーで初期化"


def check_event_story_milestone_contract() -> str:
    sys.path.insert(0, str(ROOT / "tools"))
    import add_event_story_presentations  # noqa: PLC0415

    _, recollections, milestones = add_event_story_presentations.load_story_texts()
    for milestone, recollection in zip(milestones, recollections):
        speakers = [stage[0] for stage in milestone[1:]] + [recollection[1]]
        if len(set(speakers)) != 4:
            raise CheckFailure(
                f"{milestone[0]}: 中間3人＋完走1人の話者が重複しています: {speakers}"
            )

    board = read_cp932("ERB/EVENT_BOARD_イベントボード周回.ERB")
    progress = function_body(board, "EVENT_BOARD_SHOW_PROGRESS_DIALOGUE")
    overview = function_body(board, "EVENT_BOARD_SHOW_OVERVIEW")
    completion = function_body(board, "EVENT_BOARD_SHOW_COMPLETION_DIALOGUE")
    reached = function_body(board, "EVENT_BOARD_SHOW_REACHED_PROGRESS")
    claim = function_body(board, "EVENT_BOARD_CLAIM_REWARDS")
    cycle = function_body(board, "EVENT_BOARD_STORY_CYCLE_RESET")
    mission_clear = function_body(board, "EVENT_BOARD_MISSION_CLEAR")
    area_complete = function_body(board, "EVENT_BOARD_AREA_COMPLETE")
    sugoroku = function_body(board, "EVENT_BOARD_SUGOROKU_ADVANCE")
    random_drop = function_body(board, "EVENT_BOARD_RANDOM_DROP")

    for body, label in (
        (overview, "イベント概要"),
        (progress, "イベント中間シナリオ"),
        (completion, "イベント完走"),
    ):
        if not re.search(r"(?m)^FORCEWAIT$", body):
            raise CheckFailure(f"{label}: 強制停止FORCEWAITがありません")
        if re.search(r"(?m)^WAIT$", body):
            raise CheckFailure(f"{label}: 右クリックで飛ばせるWAITが残っています")

    reset_position = progress.index("RESETCOLOR")
    first_dialogue_position = progress.index("CALL EVENT_BOARD_SHOW_PROGRESS_5000, ARG:0")
    if reset_position > first_dialogue_position:
        raise CheckFailure("イベント中間シナリオ: 台詞までヘッダ色が残っています")

    for threshold, stage, flag in (
        (5000, 1, 5016),
        (10000, 2, 5017),
        (15000, 3, 5018),
    ):
        stage_body = function_body(board, f"EVENT_BOARD_SHOW_PROGRESS_{threshold}")
        case_count = len(re.findall(r"^CASE \d+\t;", stage_body, re.MULTILINE))
        dialogue_count = len(re.findall(r"^\tPRINTL .+「.+」", stage_body, re.MULTILINE))
        if case_count != 52 or dialogue_count != 52:
            raise CheckFailure(
                f"{threshold}PT台詞: CASE={case_count}, 台詞={dialogue_count}（各52件必須）"
            )
        require(
            progress,
            f"CALL EVENT_BOARD_SHOW_PROGRESS_{threshold}, ARG:0",
            f"{threshold}PT表示分岐",
        )
        require(cycle, f"FLAG:{flag} = 0", f"{threshold}PT開催年リセット")
        require(reached, f"STORY_CURRENT_PT >= {threshold}", f"{threshold}PT既存セーブ追いつき")
        require(
            reached,
            f"CALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, STORY_EVENT_INDEX, {stage}",
            f"{threshold}PT既存セーブ表示",
        )
        require(reached, f"SETBIT FLAG:{flag}, STORY_EVENT_INDEX", f"{threshold}PT追いつき記録")

        call_position = reached.index(
            f"CALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, STORY_EVENT_INDEX, {stage}"
        )
        set_position = reached.index(f"SETBIT FLAG:{flag}, STORY_EVENT_INDEX")
        if set_position < call_position:
            raise CheckFailure(f"{threshold}PT: 台詞表示前に表示済みビットを立てています")

    require(
        mission_clear,
        "PRINTFORML 現在のイベントPT:{FLAG:B}\nCALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
        "ミッションクリアPT加算",
    )
    require(
        area_complete,
        ";エリア踏破アイテム抽選（おにぎり15% / ドーナッツ15% / ガチャチケット70%）\n"
        "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
        "エリア踏破PT加算",
    )
    for fragment, label in (
        ("PRINTFORMW ◆ 周回ボーナス！", "すごろく周回PT加算"),
    ):
        start = sugoroku.index(fragment)
        next_call = sugoroku.find("CALL EVENT_BOARD_SHOW_REACHED_PROGRESS", start)
        if next_call < 0 or next_call - start > 180:
            raise CheckFailure(f"{label}: PT加算直後の中間台詞判定がありません")
    require(
        random_drop,
        "PRINTFORML 　→ イベントPT +{LOCAL:0}\nCALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
        "ランダムドロップPT加算",
    )
    for body, label in (
        (mission_clear, "ミッションクリア"),
        (area_complete, "エリア踏破"),
        (sugoroku, "すごろく"),
        (random_drop, "ランダムドロップ"),
    ):
        malformed_calls = [
            line
            for line in body.splitlines()
            if "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS" in line
            and line.strip() != "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS"
        ]
        if malformed_calls:
            raise CheckFailure(f"{label}: 到達判定CALLの行が壊れています: {malformed_calls}")
    require(claim, "SETBIT FLAG:5004, LOCAL:9", "イベント完走記録")
    require(cycle, "IF FLAG:5019 < 1", "中間台詞セーブ移行")
    require(cycle, "FLAG:5019 = 1", "中間台詞セーブ移行完了")
    require(
        function_body(board, "EVENT_BOARD_MAIN"),
        "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
        "イベント選択時の既存セーブ追いつき",
    )
    if claim.count("CALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9") != 1:
        raise CheckFailure("報酬受取処理の完走台詞呼び出しは1箇所だけである必要があります")
    return "52イベント×3段階、全PT加算経路で到達判定・4話者重複なし・年次再表示・完走分岐"


def check_sugoroku_bonus_contract() -> str:
    board = read_cp932("ERB/EVENT_BOARD_イベントボード周回.ERB")
    sugoroku = function_body(board, "EVENT_BOARD_SUGOROKU_ADVANCE")

    for fragment, label in (
        ("LOCAL:7 = RAND:3", "スタート3種ルーレット"),
        ("LOCAL:4 = 80 + RAND:81", "スタートPT抽選"),
        ("LOCAL:4 = 100 + RAND:5 * 25", "スタートEXP抽選（25刻み）"),
        ("LOCAL:7 = RAND:4", "ボーナス4種ルーレット"),
        ("LOCAL:4 = 150 + RAND:101", "小ボーナスPT抽選"),
        ("LOCAL:4 = 200 + RAND:3 * 50", "小ボーナスEXP抽選（50刻み）"),
        ("FLAG:15057 += 20", "小ボーナスの次回ミッション支援予約"),
        ("LOCAL:4 = 350 + RAND:201", "大ボーナスPT抽選"),
        ("LOCAL:4 = 400 + RAND:5 * 50", "大ボーナスEXP抽選（50刻み）"),
        ("FLAG:15057 += 50", "大ボーナスの次回ミッション支援予約"),
        ("FLAG:15057 = 80", "ミッション支援予約の上限"),
        ("FLAG:15056 += 2", "大ボーナスの無料サイコロ2回"),
        ("IF FLAG:15056 > 0", "無料サイコロ消費"),
        ("LOCAL:0 = 0", "無料サイコロの体力消費なし"),
        ("CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4 * 10", "抽選EXPの実値換算"),
    ):
        require(sugoroku, fragment, label)

    start_begin = sugoroku.index("; EVENT_SUGOROKU_START_BONUS_BEGIN")
    start_end = sugoroku.index("; EVENT_SUGOROKU_START_BONUS_END", start_begin)
    large_begin = sugoroku.index("; EVENT_SUGOROKU_LARGE_BONUS_BEGIN")
    large_end = sugoroku.index("; EVENT_SUGOROKU_LARGE_BONUS_END", large_begin)
    start_block = sugoroku[start_begin:start_end]
    large_block = sugoroku[large_begin:large_end]
    if start_block.count("CALL EVENT_BOARD_SHOW_REACHED_PROGRESS") != 2:
        raise CheckFailure("スタート・小ボーナスの各PT抽選に到達判定が必要です")
    if large_block.count("CALL EVENT_BOARD_SHOW_REACHED_PROGRESS") != 1:
        raise CheckFailure("大ボーナスの各PT抽選に到達判定が必要です")
    for block, label in ((start_block, "スタート・小"), (large_block, "大")):
        for overlapping_reward in ("BASE:MASTER", "ITEM:", "FLAG:15001", "FLAG:15002"):
            forbid(block, overlapping_reward, f"{label}ボーナスの専用マスとの重複")
        forbid(block, "FLAG:15051 +=", f"{label}ボーナスの進行中ミッション即時支援")
        forbid(block, "CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4\n", f"{label}ボーナスのEXP十分の一化")

    if sugoroku.count("CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4 * 10") != 3:
        raise CheckFailure("スタート・小・大のEXP抽選は表示値と同じEXPを加算する必要があります")
    for malformed_percent in (
        "+20%（予約",
        "+50%（予約",
        "{FLAG:15057}%",
    ):
        forbid(sugoroku, malformed_percent, "支援率表示の%エスケープ")

    pending_support = function_body(board, "EVENT_BOARD_APPLY_PENDING_MISSION_SUPPORT")
    for fragment, label in (
        ("LOCAL:0 = FLAG:15052 * FLAG:15057 / 100", "予約支援率の進捗換算"),
        ("FLAG:15051 += LOCAL:0", "新規ミッションへの初期進捗"),
        ("FLAG:15057 = 0", "予約支援の一度きり消費"),
    ):
        require(pending_support, fragment, label)
    if board.count("CALL EVENT_BOARD_APPLY_PENDING_MISSION_SUPPORT") != 6:
        raise CheckFailure("通常・特大・緊急の全6ミッション発生経路に予約支援を接続する必要があります")
    return "PT・EXP・次回ミッション予約支援・無料サイコロのランダム抽選（回復・品・券との重複なし）"


def check_player_overcap_contract() -> str:
    board = read_cp932("ERB/EVENT_BOARD_イベントボード周回.ERB")
    add_exp = function_body(board, "EVENT_BOARD_PLAYER_ADD_EXP")
    shop = read_cp932("ERB/SHOP_ショップ.ERB")
    show_shop = function_body(shop, "SHOW_SHOP")
    info = read_cp932("ERB/INFO_情報表示.ERB")
    life_limit = function_body(info, "LIFE_LIMIT_MAXBASE")

    require(add_exp, "MAXBASE:MASTER:0 += 10", "イベントLvアップ")
    require(add_exp, "BASE:MASTER:0 += MAXBASE:MASTER:0", "イベントLvアップ超過回復")
    require(add_exp, "BASE:MASTER:1 += MAXBASE:MASTER:1", "イベントLvアップ超過回復")
    require(show_shop, "LOCAL:92 = BASE:MASTER:0", "ショップ遷移時の超過値退避")
    require(show_shop, "SIF LOCAL:92 > BASE:MASTER:0", "ショップ遷移時の超過値復元")
    forbid(life_limit, "BASE:MASTER:0 > MAXBASE:MASTER:0", "主人公体力の超過保持")
    forbid(life_limit, "BASE:MASTER:1 > MAXBASE:MASTER:1", "主人公気力の超過保持")
    return "Lvアップ加算回復・ショップ遷移・上限処理"


def check_flag_allocations() -> str:
    sys.path.insert(0, str(ROOT / "tools"))
    import audit_flag_collisions  # noqa: PLC0415

    errors = audit_flag_collisions.check_allocations() + audit_flag_collisions.check_sources()
    if errors:
        raise CheckFailure("\n  ".join(errors))
    return f"{len(audit_flag_collisions.ALLOCATIONS)}領域に重複なし"


def log_freshness_note() -> str | None:
    log = ROOT / "emuera.log"
    if not log.exists():
        return "emuera.logなし（実機確認は未実施）"
    newest_source = max(
        path.stat().st_mtime
        for directory in (ERB, CSV)
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in {".erb", ".csv"}
    )
    if log.stat().st_mtime < newest_source:
        return "emuera.logは現行ERB/CSVより古いため、過去エラーを現行不具合とみなさないこと"
    return None


def main() -> int:
    checks: list[tuple[str, Callable[[], str]]] = [
        ("文字コード・改行", check_source_encoding_and_newlines),
        ("描画API", check_graphics_api_arity),
        ("パートナーターン", check_partner_turn_contract),
        ("イベント月次遷移", check_event_month_reset_contract),
        ("イベント中間シナリオ", check_event_story_milestone_contract),
        ("すごろくボーナス", check_sugoroku_bonus_contract),
        ("主人公の超過回復", check_player_overcap_contract),
        ("FLAG領域", check_flag_allocations),
    ]
    failures = 0
    for label, check in checks:
        try:
            detail = check()
        except Exception as exc:  # 各検査を最後まで実行し、失敗をまとめて表示する。
            failures += 1
            print(f"[NG] {label}: {exc}")
        else:
            print(f"[OK] {label}: {detail}")

    note = log_freshness_note()
    if note:
        print(f"[NOTE] {note}")

    if failures:
        print(f"回帰チェック: NG（{failures}/{len(checks)}件失敗）")
        return 1
    print(f"回帰チェック: OK（{len(checks)}/{len(checks)}件成功）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
