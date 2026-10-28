# -*- coding: utf-8 -*-
"""
Apply feedback features:
1. Unconscious favor drop:
   - Accumulate penalty in TFLAG:895 during train turns without real-time deduction/messages.
   - Deduct all at once in AFTERTRA_調教後処理.ERB (@EVENTEND) when consciousness returns.
   - Register TFLAG 895, 896, 897 in CSV/Tflag.csv.
   - Reset in EVENT_TRAIN_調教イベント処理.ERB.
2. School outing (校内巡り):
   - Exclude resting characters (BASE:0 <= 0) from encounter candidates.
   - If no candidates available, treat room/classroom as empty and show message + solo event.
3. Deck battle (校内定期戦):
   - Restrict resting characters from being added to deck.
   - Auto-remove resting characters from deck if they enter recovery (@CHECK_DECK_RECOVERY_EXCLUSION).
   - Hook in AFTERTRA (@EVENTEND) and SHOP (@SHOW_SHOP).
"""

def update_tflag_csv():
    path = 'CSV/Tflag.csv'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target = "900,雑草"
    addition = """895,気絶調教好感度ペナルティ累積値,;非親密時に気絶・衰弱相手へコマンドを重ねた場合の好感度低下累積値（調教終了時に一括減算）
896,気絶調教中処女喪失フラグ,;非親密時に気絶中に処女を喪失したか判定用フラグ
897,気絶調教中膣内射精回数,;非親密時に気絶中に膣内射精された回数判定用フラグ
"""
    if "895,気絶調教好感度ペナルティ累積値" not in content:
        if target not in content:
            raise ValueError(f"Target not found in {path}")
        content = content.replace(target, addition + target, 1)
        with open(path, 'w', encoding='cp932', newline='\r\n') as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"Already updated {path}")

def update_event_train():
    path = 'ERB/EVENT_TRAIN_調教イベント処理.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target = """TFLAG:999 = 0
TFLAG:301 = 0
TFLAG:898 = 0
TFLAG:899 = 0
TFLAG:895 = 0
TFLAG:896 = 0
TFLAG:897 = 0
TFLAG:51 = 0
TFLAG:995 = 0"""

    if target not in content:
        old_target = """TFLAG:999 = 0
TFLAG:301 = 0
TFLAG:898 = 0
TFLAG:899 = 0
TFLAG:51 = 0
TFLAG:995 = 0"""
        if old_target not in content:
            raise ValueError(f"Target not found in {path}")
        content = content.replace(old_target, target, 1)
        with open(path, 'w', encoding='cp932', newline='\r\n') as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"Already updated {path}")

def update_event_s():
    path = 'ERB/EVENT_S_特殊イベント.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target_comment = ";気絶中はターン経過しても好感度は上昇しない（非親密時は調教中の行為を累積し、調教終了時に一括低下）"
    if target_comment in content:
        print(f"Already updated {path}")
        return

    old_target = """;気絶中はターン経過しても好感度は上昇しない（非親密時はコマンドを重ねるごとに好感度低下）
IF TFLAG:899 || BASE:TARGET:0 <= 0\t; 【[気絶継続中] / TARGET:[体力]<=0】
\t; 非常に親密かどうかの判定
\t; 恋慕(85), 妄信(86), 親愛(88), 相愛(89), 恋人(153), 服従(180)のいずれかを所持、
\t; または [親密]Lv10以上 かつ [好感度]3000以上
\tLOCAL:80 = 0
\tSIF TALENT:TARGET:85 || TALENT:TARGET:86 || TALENT:TARGET:88 || TALENT:TARGET:89 || TALENT:TARGET:153 || TALENT:TARGET:180
\t\tLOCAL:80 = 1
\tSIF ABL:TARGET:0 >= 10 && CFLAG:TARGET:2 >= 3000
\t\tLOCAL:80 = 1

\t; 非常に親密な場合は好感度低下なし（既存仕様通り0変動）
\tIF LOCAL:80 == 1
\t\tR = 0
\t\tTFLAG:30 = 0
\t\tRETURN 0
\tENDIF

\t; --- 非常に親密でない場合：意識のない相手への行為による好感度低下 ---
\tLOCAL:81 = 0

\t; 「何もしない(SELECTCOM == 7)」はペナルティなし
\tIF SELECTCOM != 7
\t\t; 1. 基礎コマンドペナルティ
\t\t; 性交・道具・苦痛・排泄・羞恥・ハード系コマンドは重いペナルティ
\t\tIF IS_V_INSERT_COM(SELECTCOM) || IS_A_INSERT_COM(SELECTCOM) || (SELECTCOM >= 60 && SELECTCOM <= 79) || (SELECTCOM >= 40 && SELECTCOM <= 59) || (SELECTCOM >= 80 && SELECTCOM <= 89) || (SELECTCOM >= 140 && SELECTCOM <= 159) || (SELECTCOM >= 280 && SELECTCOM <= 284)
\t\t\tLOCAL:81 = 50 + RAND:21
\t\tELSE
\t\t\tLOCAL:81 = 20 + RAND:11
\t\tENDIF

\t\t; 素質補正
\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\tTIMES LOCAL:81 , 1.50
\t\tSIF TALENT:TARGET:11\t; 反抗的
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:15\t; プライド高い
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:32\t; 抑圧
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:34\t; 抵抗
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\tTIMES LOCAL:81 , 0.60
\t\tSIF TALENT:TARGET:22\t; 感情乏しい
\t\t\tTIMES LOCAL:81 , 0.80
\t\tSIF TALENT:TARGET:76\t; 淫乱
\t\t\tTIMES LOCAL:81 , 0.50

\t\t; 2. 処女喪失ペナルティ（大幅低下）
\t\tIF TFLAG:3 == 1
\t\t\tLOCAL:82 = 700 + RAND:201
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:82 += 400
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:82 = LOCAL:82 * 6 / 10
\t\t\tLOCAL:81 += LOCAL:82
\t\tENDIF

\t\t; 3. 膣内射精ペナルティ（追加低下）
\t\tIF TFLAG:302 > 0 && (TFLAG:703 == 1 || TFLAG:703 == 9 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 1))
\t\t\tLOCAL:83 = 350 + RAND:151
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 200
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:83 = LOCAL:83 * 7 / 10
\t\t\tLOCAL:81 += LOCAL:83
\t\t; アナル射精ペナルティ
\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 2 || TFLAG:703 == 10 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 2))
\t\t\tLOCAL:83 = 250 + RAND:101
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 150
\t\t\tLOCAL:81 += LOCAL:83
\t\tENDIF

\t\t; 好感度を減少
\t\tIF LOCAL:81 > 0
\t\t\tCFLAG:TARGET:2 -= LOCAL:81
\t\t\tIF TFLAG:3 == 1
\t\t\t\tPRINTFORML 意識のないまま純潔を奪われた%CALLNAME:TARGET%の好感度が激しく低下した…！
\t\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 1 || TFLAG:703 == 9 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 1))
\t\t\t\tPRINTFORML 意識のない胎内に精液を注ぎ込まれた%CALLNAME:TARGET%の好感度が大きく低下した…！
\t\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 2 || TFLAG:703 == 10 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 2))
\t\t\t\tPRINTFORML 意識のない腸内に精液を注ぎ込まれた%CALLNAME:TARGET%の好感度が大きく低下した…！
\t\t\tELSE
\t\t\t\tPRINTFORML 意識を失った%CALLNAME:TARGET%への一方的な行為により、好感度が低下した…
\t\t\tENDIF
\t\t\tPRINTFORML 好感度低下:{LOCAL:81}
\t\t\tSIF ((FLAG:23 & 1p26) == 0) && FLAG:2 != 1
\t\t\t\tPRINTFORMW 好感度合計:{CFLAG:TARGET:2}
\t\tENDIF
\tENDIF

\tR = 0
\tTFLAG:30 = 0
\tRETURN 0
ENDIF"""

    replacement = """;気絶中はターン経過しても好感度は上昇しない（非親密時は調教中の行為を累積し、調教終了時に一括低下）
IF TFLAG:899 || BASE:TARGET:0 <= 0\t; 【[気絶継続中] / TARGET:[体力]<=0】
\t; 非常に親密かどうかの判定
\t; 恋慕(85), 妄信(86), 親愛(88), 相愛(89), 恋人(153), 服従(180)のいずれかを所持、
\t; または [親密]Lv10以上 かつ [好感度]3000以上
\tLOCAL:80 = 0
\tSIF TALENT:TARGET:85 || TALENT:TARGET:86 || TALENT:TARGET:88 || TALENT:TARGET:89 || TALENT:TARGET:153 || TALENT:TARGET:180
\t\tLOCAL:80 = 1
\tSIF ABL:TARGET:0 >= 10 && CFLAG:TARGET:2 >= 3000
\t\tLOCAL:80 = 1

\t; 非常に親密な場合は好感度低下なし（既存仕様通り0変動）
\tIF LOCAL:80 == 1
\t\tR = 0
\t\tTFLAG:30 = 0
\t\tRETURN 0
\tENDIF

\t; --- 非常に親密でない場合：意識のない相手への行為ペナルティを調教終了時用に累積 ---
\tLOCAL:81 = 0

\t; 「何もしない(SELECTCOM == 7)」はペナルティなし
\tIF SELECTCOM != 7
\t\t; 1. 基礎コマンドペナルティ
\t\t; 性交・道具・苦痛・排泄・羞恥・ハード系コマンドは重いペナルティ
\t\tIF IS_V_INSERT_COM(SELECTCOM) || IS_A_INSERT_COM(SELECTCOM) || (SELECTCOM >= 60 && SELECTCOM <= 79) || (SELECTCOM >= 40 && SELECTCOM <= 59) || (SELECTCOM >= 80 && SELECTCOM <= 89) || (SELECTCOM >= 140 && SELECTCOM <= 159) || (SELECTCOM >= 280 && SELECTCOM <= 284)
\t\t\tLOCAL:81 = 50 + RAND:21
\t\tELSE
\t\t\tLOCAL:81 = 20 + RAND:11
\t\tENDIF

\t\t; 素質補正
\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\tTIMES LOCAL:81 , 1.50
\t\tSIF TALENT:TARGET:11\t; 反抗的
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:15\t; プライド高い
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:32\t; 抑圧
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:34\t; 抵抗
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\tTIMES LOCAL:81 , 0.60
\t\tSIF TALENT:TARGET:22\t; 感情乏しい
\t\t\tTIMES LOCAL:81 , 0.80
\t\tSIF TALENT:TARGET:76\t; 淫乱
\t\t\tTIMES LOCAL:81 , 0.50

\t\t; 2. 処女喪失ペナルティ（大幅低下）
\t\tIF TFLAG:3 == 1
\t\t\tLOCAL:82 = 700 + RAND:201
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:82 += 400
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:82 = LOCAL:82 * 6 / 10
\t\t\tLOCAL:81 += LOCAL:82
\t\t\tTFLAG:896 = 1\t; 気絶調教中処女喪失を記録
\t\tENDIF

\t\t; 3. 膣内射精ペナルティ（追加低下）
\t\tIF TFLAG:302 > 0 && (TFLAG:703 == 1 || TFLAG:703 == 9 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 1))
\t\t\tLOCAL:83 = 350 + RAND:151
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 200
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:83 = LOCAL:83 * 7 / 10
\t\t\tLOCAL:81 += LOCAL:83
\t\t\tTFLAG:897 += 1\t; 気絶調教中膣内射精回数を記録
\t\t; アナル射精ペナルティ
\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 2 || TFLAG:703 == 10 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 2))
\t\t\tLOCAL:83 = 250 + RAND:101
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 150
\t\t\tLOCAL:81 += LOCAL:83
\t\tENDIF

\t\t; 調教中のターン内では表示・減算せず、TFLAG:895へ累積して調教終了時に一括減算
\t\tTFLAG:895 += LOCAL:81
\tENDIF

\tR = 0
\tTFLAG:30 = 0
\tRETURN 0
ENDIF"""

    if old_target not in content:
        raise ValueError(f"old_target not found in {path}")
    content = content.replace(old_target, replacement, 1)
    with open(path, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Updated {path}")

def update_aftertra():
    path = 'ERB/AFTERTRA_調教後処理.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target = '\tTRYCALLFORM CHAR_SESSION_END_{NO:TARGET}\nENDIF\n'
    addition = """\tTRYCALLFORM CHAR_SESSION_END_{NO:TARGET}
ENDIF

;-------------------------------------------------
; 意識喪失・気絶中の不本意行為に対する好感度一括低下処理
;-------------------------------------------------
IF TARGET >= 0 && TARGET < CHARANUM && TFLAG:895 > 0
\tDRAWLINE
\tIF TFLAG:896 == 1
\t\tPRINTFORML 目を覚ました%CALLNAME:TARGET%は、自らの純潔が意識のない間に奪われていたという取り返しのつかない現実に気づき、激しいショックと絶望に青ざめている…！
\tELSEIF TFLAG:897 > 0
\t\tPRINTFORML 意識を取り戻した%CALLNAME:TARGET%は、胎内に残る見覚えのない熱と注ぎ込まれた精液の感触に気づき、不信と嫌悪で身体を震わせている…！
\tELSE
\t\tPRINTFORML 意識を取り戻した%CALLNAME:TARGET%は、気を失っている間に不本意な行為を重ねられた身体の痕跡に気づき、強い不快感と不信感を抱いたようだ…
\tENDIF
\tCFLAG:TARGET:2 -= TFLAG:895
\tPRINTFORML 好感度低下:{TFLAG:895}
\tSIF ((FLAG:23 & 1p26) == 0) && FLAG:2 != 1
\t\tPRINTFORMW 好感度合計:{CFLAG:TARGET:2}
\tTFLAG:895 = 0
\tTFLAG:896 = 0
\tTFLAG:897 = 0
ENDIF

;-------------------------------------------------
; 衰弱療養キャラの校内定期戦デッキ自動除外チェック
;-------------------------------------------------
CALL CHECK_DECK_RECOVERY_EXCLUSION
"""

    if target not in content:
        raise ValueError(f"target not found in {path}")
    content = content.replace(target, addition, 1)
    with open(path, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Updated {path}")

def update_location_event():
    path = 'ERB/LOCATION_EVENT_場所遭遇・パートナー選択.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target = """; 誰もいなかった→ソロイベント
IF LOCAL:0 == 0
\tCALL LOCATION_SOLO_EVENT
\tRETURN RESULT
ENDIF"""

    replacement = """; 療養中（BASE:0 <= 0）のキャラを候補から除外
LOCAL:90 = 0
FOR LOCAL:91, 1, LOCAL:0 + 1
\tLOCAL:92 = LOCAL:(LOCAL:91)
\tLOCAL:93 = GETCHARA(LOCAL:92)
\t; 既に加入済みで、かつ体力が0以下（療養中）の場合は不在として除外
\tIF LOCAL:93 >= 0 && BASE:(LOCAL:93):0 <= 0
\t\tCONTINUE
\tENDIF
\tLOCAL:90 += 1
\tLOCAL:(LOCAL:90) = LOCAL:92
NEXT
LOCAL:0 = LOCAL:90

; 誰もいなかった（全員療養中または無人）→空室ソロイベント
IF LOCAL:0 == 0
\tPRINTFORML 中を覗いてみたが、誰もいないようだ……部屋は静まり返っている。
\tPRINTFORMW （所属する生徒は保健室で療養中などのため、空でした）
\tCALL LOCATION_SOLO_EVENT
\tRETURN RESULT
ENDIF"""

    if target not in content:
        raise ValueError(f"target not found in {path}")
    content = content.replace(target, replacement, 1)
    with open(path, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Updated {path}")

def update_deck_battle():
    path = 'ERB/DECK_BATTLE_校内定期戦.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    # 1. Add CHECK_DECK_RECOVERY_EXCLUSION to DECK_BATTLE
    target_init = """;初回のみFLAG:200-204を-1に初期化（デフォ値0はMASTERと被るため）
IF FLAG:206 == 0
\tREPEAT 5
\t\tFLAG:(200 + COUNT) = -1
\tREND
\tFLAG:206 = 1
ENDIF
DRAWLINE"""

    repl_init = """;初回のみFLAG:200-204を-1に初期化（デフォ値0はMASTERと被るため）
IF FLAG:206 == 0
\tREPEAT 5
\t\tFLAG:(200 + COUNT) = -1
\tREND
\tFLAG:206 = 1
ENDIF
CALL CHECK_DECK_RECOVERY_EXCLUSION
DRAWLINE"""

    if target_init not in content:
        raise ValueError(f"target_init not found in {path}")
    content = content.replace(target_init, repl_init, 1)

    # 2. Add CHECK_DECK_RECOVERY_EXCLUSION calls to SHOW_CURRENT_DECK, SHOW_DECK_SCORE, RUN_DECK_BATTLE
    content = content.replace(
        "@SHOW_CURRENT_DECK\nDRAWLINE",
        "@SHOW_CURRENT_DECK\nCALL CHECK_DECK_RECOVERY_EXCLUSION\nDRAWLINE",
        1
    )
    content = content.replace(
        "@EDIT_DECK\nDRAWLINE",
        "@EDIT_DECK\nCALL CHECK_DECK_RECOVERY_EXCLUSION\nDRAWLINE",
        1
    )
    content = content.replace(
        "@SHOW_DECK_SCORE\nCALL CARD_RECALC_BONUSES",
        "@SHOW_DECK_SCORE\nCALL CHECK_DECK_RECOVERY_EXCLUSION\nCALL CARD_RECALC_BONUSES",
        1
    )
    content = content.replace(
        "@RUN_DECK_BATTLE\nDRAWLINE",
        "@RUN_DECK_BATTLE\nCALL CHECK_DECK_RECOVERY_EXCLUSION\nDRAWLINE",
        1
    )

    # 3. In EDIT_DECK, show 療養中・編成不可 and block selection
    target_edit_list = """\tIF B
\t\tPRINTFORML [{A, 2}] ★%NAME:LOCAL%（親密{CFLAG:LOCAL:2}  学力Lv{ABL:LOCAL:88}  運動{ABL:LOCAL:93}  表現{ABL:LOCAL:94}  知識{ABL:LOCAL:95}）
\tELSE
\t\tPRINTFORML [{A, 2}]  %NAME:LOCAL%（親密{CFLAG:LOCAL:2}  学力Lv{ABL:LOCAL:88}  運動{ABL:LOCAL:93}  表現{ABL:LOCAL:94}  知識{ABL:LOCAL:95}）
\tENDIF"""

    repl_edit_list = """\tIF B
\t\tPRINTFORML [{A, 2}] ★%NAME:LOCAL%（親密{CFLAG:LOCAL:2}  学力Lv{ABL:LOCAL:88}  運動{ABL:LOCAL:93}  表現{ABL:LOCAL:94}  知識{ABL:LOCAL:95}）
\tELSEIF BASE:LOCAL:0 <= 0
\t\tPRINTFORML [{A, 2}]  %NAME:LOCAL%（衰弱療養中・編成不可）
\tELSE
\t\tPRINTFORML [{A, 2}]  %NAME:LOCAL%（親密{CFLAG:LOCAL:2}  学力Lv{ABL:LOCAL:88}  運動{ABL:LOCAL:93}  表現{ABL:LOCAL:94}  知識{ABL:LOCAL:95}）
\tENDIF"""

    if target_edit_list not in content:
        raise ValueError(f"target_edit_list not found in {path}")
    content = content.replace(target_edit_list, repl_edit_list, 1)

    target_select_z = """Z = LOCAL:(10 + RESULT)

;パーティ在籍確認"""

    repl_select_z = """Z = LOCAL:(10 + RESULT)

; 衰弱療養中のキャラは編成不可
IF BASE:Z:0 <= 0
\tPRINTFORMW %CALLNAME:Z%は体力が尽きて衰弱療養（お休み）中のため、デッキに編成できません。
\tCALL EDIT_DECK
\tRETURN 1
ENDIF

;パーティ在籍確認"""

    if target_select_z not in content:
        raise ValueError(f"target_select_z not found in {path}")
    content = content.replace(target_select_z, repl_select_z, 1)

    # 4. In AUTO_SELECT_DECK, skip resting characters
    target_auto = """\tFOR LOCAL, 0, CHARANUM
\t\tSIF LOCAL == MASTER
\t\t\tCONTINUE
\t\tSIF CFLAG:LOCAL:21 == 1\t; 【LOCAL:[別れ]==1】
\t\t\tCONTINUE"""

    repl_auto = """\tFOR LOCAL, 0, CHARANUM
\t\tSIF LOCAL == MASTER
\t\t\tCONTINUE
\t\tSIF CFLAG:LOCAL:21 == 1\t; 【LOCAL:[別れ]==1】
\t\t\tCONTINUE
\t\tSIF BASE:LOCAL:0 <= 0\t; 衰弱療養中（お休み）のキャラは自動選出から除外
\t\t\tCONTINUE"""

    if target_auto not in content:
        raise ValueError(f"target_auto not found in {path}")
    content = content.replace(target_auto, repl_auto, 1)

    # 5. Add @CHECK_DECK_RECOVERY_EXCLUSION function at the end
    deck_func = """
;---------------------------------------------------------
; 衰弱療養中・別れキャラのデッキ自動除外処理
;---------------------------------------------------------
@CHECK_DECK_RECOVERY_EXCLUSION
LOCAL:95 = 0
REPEAT 5
\tLOCAL = FLAG:(200 + COUNT)
\tIF LOCAL >= 0 && LOCAL < CHARANUM
\t\t; 別れ状態、または体力が0以下（療養中）の場合
\t\tIF CFLAG:LOCAL:21 == 1 || BASE:LOCAL:0 <= 0
\t\t\tPRINTFORML （%CALLNAME:LOCAL%は衰弱療養中のため、校内定期戦デッキから外れました）
\t\t\tFLAG:(200 + COUNT) = -1
\t\t\tLOCAL:95 = 1
\t\tENDIF
\tENDIF
REND
SIF LOCAL:95
\tFLAG:205 = 1
RETURN LOCAL:95
"""
    content += deck_func

    with open(path, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Updated {path}")

def update_shop():
    path = 'ERB/SHOP_ショップ.ERB'
    with open(path, 'r', encoding='cp932') as f:
        content = f.read()

    target = """CALL ALL_ACT_ABLE
;自動発動イベントチェック（試験・学校行事）
CALL CHECK_AUTO_EVENTS"""

    replacement = """CALL ALL_ACT_ABLE
;衰弱療養キャラのデッキ自動除外
CALL CHECK_DECK_RECOVERY_EXCLUSION
;自動発動イベントチェック（試験・学校行事）
CALL CHECK_AUTO_EVENTS"""

    if target not in content:
        raise ValueError(f"Target not found in {path}")
    content = content.replace(target, replacement, 1)
    with open(path, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Updated {path}")

if __name__ == '__main__':
    update_tflag_csv()
    update_event_train()
    update_event_s()
    update_aftertra()
    update_location_event()
    update_deck_battle()
    update_shop()
    print("All feedback features successfully applied!")
