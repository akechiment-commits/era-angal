"""Apply the event menu/resume fix, preserving CP932 and CRLF."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def replace_once(text, old, new):
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new, 1)


def main():
    data_path = ROOT / 'ERB/EVENT_BOARD_DATA_イベントデータ.ERB'
    board_path = ROOT / 'ERB/EVENT_BOARD_イベントボード周回.ERB'
    data = data_path.read_bytes().decode('cp932').replace('\r\n', '\n')
    board = board_path.read_bytes().decode('cp932').replace('\r\n', '\n')
    data = replace_once(data, '@LOAD_MONTH_EVENTS(ARG)\nSELECTCASE',
        '@LOAD_MONTH_EVENTS(ARG)\n;前月の表示名・種別を残さない。表示番号と保存スロットは入口で対応付ける。\nREPEAT 6\n\tTSTR:(100 + COUNT) =\n\tTFLAG:(100 + COUNT) = 0\nREND\nSELECTCASE')
    data = replace_once(data, 'TSTR:105 = "帰宅部争奪戦"\n\tTFLAG:105 = 1',
        'TSTR:104 = "帰宅部争奪戦"\n\tTFLAG:104 = 1')
    data = replace_once(data, '; MAIN_STORY_HOME_CLUB_7_MONTH_END\n\tRETURN 6',
        '; MAIN_STORY_HOME_CLUB_7_MONTH_END\n\tRETURN 5')
    data = replace_once(data, '\t\tRETURN 55\n\tENDIF\n\tRETURN 27 + FLAG:68',
        '\t\tRETURN 55\n\tENDIF\n\t;旧7月の欠番は8月の物語IDへ流さない。\n\tSIF FLAG:68 == 4\n\t\tRETURN -1\n\tRETURN 27 + FLAG:68')
    board = replace_once(board, ';   FLAG:15070 = プレイヤーレベル（0は未初期化、通常は1以上）',
        ';   FLAG:15300～15347 = イベント別進行状態（6枠×8項目、15050～15057の保存先）\n;   FLAG:15348 = イベント別進行状態の初期化済みフラグ\n;   FLAG:15070 = プレイヤーレベル（0は未初期化、通常は1以上）') if board.count(';   FLAG:15070 = プレイヤーレベル（0は未初期化、通常は1以上）') == 1 else board.replace(';   FLAG:15071 = 現在レベル内のプレイヤー経験値', ';   FLAG:15300～15347 = イベント別進行状態（6枠×8項目、15050～15057の保存先）\n;   FLAG:15348 = イベント別進行状態の初期化済みフラグ\n;   FLAG:15071 = 現在レベル内のプレイヤー経験値', 1)
    board = replace_once(board, ';選択中イベントだけが使う共有進行状態も月替わりで破棄する。',
        ';保存した全イベントの進行状態も月替わりで破棄する。\nREPEAT 48\n\tFLAG:(15300 + COUNT) = 0\nREND\nFLAG:15348 = 1\n\n;選択中イベントだけが使う共有進行状態も月替わりで破棄する。')
    helpers = ''';イベント表示番号から保存スロットへ変換する（いずれも0始まり）。
;7月の帰宅部争奪戦は表示5番、保存は従来どおり6枠目。
@EVENT_BOARD_MENU_SLOT(ARG, ARG:1)
IF ARG == 7 && ARG:1 == 4
	RETURN 5
ENDIF
RETURN ARG:1

;旧セーブに残る選択中イベントの進捗を一度だけ取り込む。
@EVENT_BOARD_STATE_INIT
SIF FLAG:15348 > 0
	RETURN 0
CALL EVENT_BOARD_STATE_SAVE
FLAG:15348 = 1
RETURN 1

@EVENT_BOARD_STATE_SAVE
#DIM DYNAMIC STATE_OFFSET, 1
#DIM DYNAMIC STATE_BASE, 1
SIF FLAG:68 < 0 || FLAG:68 >= 6
	RETURN 0
STATE_BASE = 15300 + FLAG:68 * 8
FOR STATE_OFFSET, 0, 8
	FLAG:(STATE_BASE + STATE_OFFSET) = FLAG:(15050 + STATE_OFFSET)
NEXT
RETURN 1

@EVENT_BOARD_STATE_LOAD
#DIM DYNAMIC STATE_OFFSET, 1
#DIM DYNAMIC STATE_BASE, 1
SIF FLAG:68 < 0 || FLAG:68 >= 6
	RETURN 0
STATE_BASE = 15300 + FLAG:68 * 8
FOR STATE_OFFSET, 0, 8
	FLAG:(15050 + STATE_OFFSET) = FLAG:(STATE_BASE + STATE_OFFSET)
NEXT
RETURN 1

'''
    board = replace_once(board, '@EVENT_BOARD_MAIN\n', helpers + '@EVENT_BOARD_MAIN\n')
    board = replace_once(board, 'CALL EVENT_BOARD_MONTHLY_RESET\n\n;今月',
        'CALL EVENT_BOARD_MONTHLY_RESET\nCALL EVENT_BOARD_STATE_INIT\n\n;今月')
    board = replace_once(board, 'FLAG:68 = LOCAL:8\t;イベントインデックス保存(0-5)',
        'CALL EVENT_BOARD_MENU_SLOT, DAY:8, LOCAL:8\nFLAG:68 = RESULT\t;保存スロット(0-5)。表示番号とは分けて既存セーブを維持する。')
    board = replace_once(board, ''';ミッション状態・エリア進捗・すごろく盤面位置クリア（新規開始）
;FLAG:15055/FLAG:33はイベント別ではない共有変数のため、切り替え時にリセットしないと
;前のイベントの進捗%・盤面位置が新しいイベントに持ち越されてしまう
FLAG:15051 = 0
FLAG:15052 = 0
FLAG:15053 = 0
FLAG:15055 = 0
FLAG:15050 = 0
$BOARD_LOOP
''', ''';選んだイベント固有の進行状態を復元する。
CALL EVENT_BOARD_STATE_LOAD
$BOARD_LOOP
;各操作の結果を保存する。退出・別イベントへの切替後もここから再開する。
CALL EVENT_BOARD_STATE_SAVE
''')
    for path, text in ((data_path, data), (board_path, board)):
        path.write_bytes(text.replace('\n', '\r\n').encode('cp932'))


if __name__ == '__main__':
    main()
