from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USERCOM = ROOT / "ERB" / "USERCOM_コマンド一覧表示.ERB"
INFO = ROOT / "ERB" / "INFO_情報表示.ERB"
DATE = ROOT / "ERB" / "COMF" / "COMF323.ERB"
AUTO = ROOT / "ERB" / "AUTO_TRAIN_オート調教.ERB"
PARTNER_TURN = ROOT / "ERB" / "PARTNER_TURN_パートナーターン.ERB"
COUNTER = ROOT / "ERB" / "COUNTERSYSTEM_カウンターシステム.ERB"
SOURCE = ROOT / "ERB" / "SOURCE_ソース計算・口上呼び出し.ERB"
REVMODE = ROOT / "ERB" / "REVMODE_リバースモード.ERB"
PASSIVE = ROOT / "ERB" / "PASSIVE_パッシブスキル.ERB"
EVENT_MESSAGE = ROOT / "ERB" / "EVENT_M_調教メッセージ.ERB"
EVENT_TEXT = ROOT / "ERB" / "EVENT_TEXT_イベントテキスト.ERB"
CONFIG_EX = ROOT / "ERB" / "CONFIG_EX_設定拡張.ERB"
SHOOT = ROOT / "ERB" / "EVENT_SHOOT_射精処理.ERB"
SYSTEM = ROOT / "ERB" / "SYSTEM_基本システム処理.ERB"
SELF_COMMAND = ROOT / "ERB" / "SELF_セルフコマンド.ERB"
REVMODE_ACTIVE_COMMAND = ROOT / "ERB" / "COMF" / "COMF500.ERB"
CFLAG_CSV = ROOT / "CSV" / "Cflag.csv"
ENDURANCE_GROWTH = ROOT / "ERB" / "ENDURANCE_GROWTH_主人公耐力成長.ERB"
SHOP_COM_ACT = ROOT / "ERB" / "SHOP_COM_ACT_ショップコマンド.ERB"
EVENT_TRAIN = ROOT / "ERB" / "EVENT_TRAIN_調教イベント処理.ERB"
COMABLE = ROOT / "ERB" / "COMF" / "COMABLE.ERB"


ENDURANCE_GROWTH_SOURCE = r''' ;============================================================
; 主人公の耐力成長
; パートナーを絶頂させた経験に、主人公自身の射精経験と耐力枯渇経験を加算する。
;============================================================
@MASTER_ENDURANCE_GROWTH
#FUNCTION
;CFLAG:2             パートナーを絶頂させた強度の累計（既存）
;CFLAG:1150          主人公の射精回数
;CFLAG:1151          主人公の累計射精量（ml）
;CFLAG:1152          耐力を0まで削られた成長ポイント
;CFLAG:1154          耐力0後のドライ絶頂成長ポイント
;CFLAG:1155          旧カウンタから成長ポイントへの移行済みフラグ
IF CFLAG:MASTER:1155 == 0
	CFLAG:MASTER:1152 *= 100
	CFLAG:MASTER:1154 *= 20
	CFLAG:MASTER:1155 = 1
ENDIF
;主人公自身の射精は、1回につき10点＋実射精量1mlにつき1点として反映する。
RETURNF CFLAG:MASTER:2 + CFLAG:MASTER:1150 * 10 + CFLAG:MASTER:1151 + CFLAG:MASTER:1152 + CFLAG:MASTER:1154

@FEMALE_ENDURANCE_GROWTH, ARG
#FUNCTION
;女性の絶頂経験はEXP:2として純粋に保持し、耐力枯渇の成長は別カウンタで加算する。
IF CFLAG:ARG:1155 == 0
	CFLAG:ARG:1153 *= 100
	CFLAG:ARG:1154 *= 20
	CFLAG:ARG:1155 = 1
ENDIF
RETURNF EXP:ARG:2 + CFLAG:ARG:1153 + CFLAG:ARG:1154
'''


AUTO_SOURCE = r''' ;============================================================
; オート調教
; 通常のCOM_ABLE判定を通過したコマンドを、通常COMの関数呼び出しで連続実行する。
; このEmuera版のCALLTRAINは実行不能になるため使用しない。
;============================================================

;-------------------------------------------------
; オート調教の回数選択
;-------------------------------------------------
@AUTO_TRAIN_SELECT
#DIM DYNAMIC LOCALCOUNT, 1

DRAWLINE
PRINTFORML 【パートナーに任せる】パートナーの状態に合わせて行動を選び、連続実行します
PRINTFORML [1] 3回
PRINTFORML [2] 5回
PRINTFORML [3] 10回
PRINTFORML [4] 最後まで
PRINTFORML [0] 戻る

INPUT
SELECTCASE RESULT
CASE 0
	RETURN 0
CASE 1
	LOCALCOUNT = 3
CASE 2
	LOCALCOUNT = 5
CASE 3
	LOCALCOUNT = 10
CASE 4
	;CALLTRAINで扱えるSELECTCOM配列の上限。通常の調教終了時は途中で終了する。
	LOCALCOUNT = 999
CASEELSE
	RESTART
ENDSELECT

;COM_ABLEを通常実行用の状態で評価して、SELECTCOM:0～を作る
CALL AUTO_TRAIN_BUILD_SEQUENCE, LOCALCOUNT
SIF RESULT <= 0
	RETURN 0

IF LOCALCOUNT >= 999
	PRINTFORML 【パートナーに任せる】最後まで任せます
ELSE
	PRINTFORML 【パートナーに任せる】{RESULT}回任せます
ENDIF

;連続実行中を示す専用印。
TFLAG:999 = 1
TFLAG:998 = LOCALCOUNT
CALL AUTO_TRAIN_CONTINUE
RETURN 0

;-------------------------------------------------
; 1コマンドずつ候補を再評価して連続実行する
; TFLAG:998=残り回数。999は「最後まで」の安全上限。
;-------------------------------------------------
@AUTO_TRAIN_CONTINUE

IF TFLAG:998 <= 0
	TFLAG:999 = 0
	PRINTFORML 【パートナーに任せる】ここで終わりにしました
	RETURN 0
ENDIF

;通常モードで相手の気力が尽きたら、通常操作と同じく一旦別れる。
;服を脱いでいない間は、無理にオートを継続してウフフへ移行させない。
IF TFLAG:44 == 0 && BASE:TARGET:1 <= 0
	TFLAG:999 = 0
	IF TIME == 0
		PRINTFORMW （%CALLNAME:TARGET%は疲れたようだ。%CALLNAME:MASTER%は今日はここで一旦別れることにした）
	ELSE
		PRINTFORMW （%CALLNAME:TARGET%は眠たそうにしている。%CALLNAME:MASTER%は今日はここで一旦別れることにした）
	ENDIF
	BEGIN AFTERTRAIN
ENDIF

;対象またはプレイヤーの体力が40％以下なら、限界になる前に区切る。
IF BASE:0 * 5 <= MAXBASE:0 * 2 || BASE:PLAYER:0 * 5 <= MAXBASE:PLAYER:0 * 2
	TFLAG:999 = 0
	PRINTFORML 【オート調教】体力を考慮して、%CALLNAME:TARGET%はここで一息つくことにした
	RETURN 0
ENDIF

CALL AUTO_TRAIN_BUILD_SEQUENCE, 1
IF RESULT <= 0
	TFLAG:999 = 0
	PRINTFORML %CALLNAME:TARGET%は続けられる行動がないため、ここで終わりにした
	RETURN 0
ENDIF

TFLAG:998 -= 1
CALL AUTO_TRAIN_EXECUTE, SELECTCOM:0
RETURN 0

;-------------------------------------------------
; CALLTRAINを介さず、通常COMと通常のソース処理を1手分だけ実行する。
;-------------------------------------------------
@AUTO_TRAIN_EXECUTE, ARG

;通常の入力で行われるターン開始時リセットを再現する。
REPEAT 30
	TFLAG:COUNT = 0
REND
TFLAG:100 = 0
TFLAG:540 = 0
TFLAG:DOTRAIN = 1
TFLAG:CALLTRAIN = 0
SELECTCOM = ARG

;COM内の実行判定・メッセージをそのまま利用する。
TRYCALLFORM COM{ARG}
;REVMODE側のソース処理は通常COMのソース計算一式を持つため、ここで1回だけ呼ぶ。
CALL REVMODE_SOURCE_CHECK
CALL AUTO_TRAIN_EVENTCOMEND

SIF TFLAG:999
	CALL AUTO_TRAIN_CONTINUE
RETURN 0

;-------------------------------------------------
; 実行列の組み立て
; ARG: 希望回数 / RESULT: 実際に登録した回数
;-------------------------------------------------
@AUTO_TRAIN_BUILD_SEQUENCE, ARG
#DIM DYNAMIC CANDIDATE_COUNT, 1
#DIM DYNAMIC WEIGHT_TOTAL, 1
#DIM DYNAMIC PICK, 1
#DIM DYNAMIC SLOT, 1
#DIM DYNAMIC INDEX, 1

VARSET F, 0
VARSET SELECTCOM, -1

;COM_ABLEは通常入力かDOTRAIN中でないと実行できない。
TFLAG:DOTRAIN = 1

;オート対象になり得る通常・調教コマンドを列挙し、現在実行可能なものだけ残す。
FOR INDEX, 0, 414
	SIF STRLENS(TRAINNAME:INDEX) == 0
		CONTINUE
	SIF AUTO_TRAIN_COMMAND_ALLOWED(INDEX) == 0
		CONTINUE
	SIF AUTO_TRAIN_COMMAND_READY(INDEX) == 0
		CONTINUE

	TFLAG:DOTRAIN = 1
	SELECTCOM = INDEX
	TRYCALLFORM COM_ABLE{INDEX}
	SIF RESULT == 0
		CONTINUE

	F:CANDIDATE_COUNT = INDEX
	CANDIDATE_COUNT += 1
NEXT

IF CANDIDATE_COUNT == 0
	TFLAG:DOTRAIN = 0
	PRINTFORML 実行可能な調教コマンドがありません
	RESULT = 0
	RETURN 0
ENDIF

;現在の素質・能力・経験を重みに反映して、同じ候補群から連続行動を作る。
;1コマンドごとにこの関数を呼び直すため、途中の状態変化も次の選択に反映される。
FOR SLOT, 0, ARG
	WEIGHT_TOTAL = 0
	FOR INDEX, 0, CANDIDATE_COUNT
		WEIGHT_TOTAL += AUTO_TRAIN_COMMAND_WEIGHT(F:INDEX)
	NEXT

	PICK = RAND:WEIGHT_TOTAL
	FOR INDEX, 0, CANDIDATE_COUNT
		PICK -= AUTO_TRAIN_COMMAND_WEIGHT(F:INDEX)
		IF PICK < 0
			SELECTCOM:SLOT = F:INDEX
			BREAK
		ENDIF
	NEXT
NEXT

;CALL元が実行回数を受け取るため、RETURN値として返す。
RETURN ARG

;-------------------------------------------------
; オート対象に含めるコマンドか
; アイテム使用・終了・入力を伴う行動は除外し、通常交流・調教系を対象にする。
;-------------------------------------------------
@AUTO_TRAIN_COMMAND_ALLOWED(ARG)
#FUNCTION

;お任せは「相手が自発的に選ぶ」扱い。実行可能な強引コマンドを無差別に混ぜない。
;関係が浅い間は、拒否や好感度低下を起こしにくい会話だけにする。
SIF ARG == 301
	RETURNF 1

;好感度が育てば、相手と一緒に行える穏やかな日常行動を解放する。
IF CFLAG:TARGET:2 >= 40 && GROUPMATCH(ARG, 300, 304, 305, 306, 307, 309, 310, 312, 313, 314, 315, 320, 321, 322, 390)
	RETURNF 1
ENDIF

;恋慕と合意が揃ってから、甘い言葉・スキンシップ・キス・デートを候補にする。
IF CFLAG:TARGET:2 >= 300 && TALENT:TARGET:85 && TALENT:TARGET:152 && GROUPMATCH(ARG, 303, 311, 323, 340, 341, 342)
	RETURNF 1
ENDIF

;性的な行為はウフフ中かつ、恋慕・合意・恋人（または淫乱）が揃う場合だけ。
IF TFLAG:44 && CFLAG:TARGET:2 >= 300 && TALENT:TARGET:85 && TALENT:TARGET:152 && (TALENT:TARGET:153 || TALENT:TARGET:76)
	SIF GROUPMATCH(ARG, 0, 1, 5, 6, 20, 21, 24, 25, 30, 31, 32, 33, 34, 36, 37, 63, 69, 120, 121, 122, 123, 124, 188, 193, 194, 195, 196)
		RETURNF 1
ENDIF
RETURNF 0

;-------------------------------------------------
; 現在の状態でお任せ候補にしてよいか
; 潤滑が足りないうちは性交・挿入系を候補にせず、まず前戯へ向かわせる。
;-------------------------------------------------
@AUTO_TRAIN_COMMAND_READY(ARG)
#FUNCTION

SIF AUTO_TRAIN_IS_SEXUAL_PENETRATION(ARG) && PALAM:3 < 500
	RETURNF 0
RETURNF 1

@AUTO_TRAIN_IS_SEXUAL_PENETRATION(ARG)
#FUNCTION

RETURNF GROUPMATCH(ARG, 8, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 34, 36, 63, 69, 120, 121, 122, 123, 124, 188, 193, 194, 195, 196, 204, 255, 256, 363, 365, 366, 381)

;-------------------------------------------------
; パートナーの性質・進行度に応じたコマンド重み
; 親密・欲望・感覚・奉仕精神・露出癖・サドっ気と各経験を反映する。
;-------------------------------------------------
@AUTO_TRAIN_COMMAND_WEIGHT(ARG)
#FUNCTION
#DIM DYNAMIC WEIGHT, 1

WEIGHT = 1

;親愛・スキンシップ系
IF GROUPMATCH(ARG, 0, 5, 6, 190, 200, 201, 202, 300, 301, 303, 304, 305, 306, 307, 311, 312, 315, 320, 321, 322, 323, 340, 341, 342, 370, 390, 393, 399)
	WEIGHT += ABL:0 / 2 + TALENT:恋慕 * 4
ENDIF

;潤滑が足りない間は前戯を優先して、自然に次の段階へ進める。
IF PALAM:3 < 500 && GROUPMATCH(ARG, 0, 1, 3, 5, 6, 8, 9, 30, 31, 32, 37, 78, 79, 190, 200, 201, 202, 340, 341, 342, 360, 361, 362, 372, 373, 380)
	WEIGHT += 6 + (500 - PALAM:3) / 100
ENDIF

;調教具・感覚を使う行動
IF GROUPMATCH(ARG, 10, 11, 13, 14, 15, 16, 17, 19, 76, 79, 110, 367)
	WEIGHT += (ABL:3 + ABL:4 + ABL:5) / 2
ENDIF

;奉仕系
IF (ARG >= 30 && ARG <= 39) || GROUPMATCH(ARG, 4, 31, 32, 37, 67, 68, 80, 189, 201, 373, 380)
	WEIGHT += ABL:6 + EXP:22 / 50
ENDIF

;性交・挿入系。欲望と各感覚が伸びるほど選びやすい。
IF (ARG >= 20 && ARG <= 29) || GROUPMATCH(ARG, 34, 36, 63, 69, 120, 121, 122, 123, 124, 188, 193, 194, 195, 196, 204, 255, 256, 363, 365, 366, 381)
	WEIGHT += ABL:1 + (ABL:3 + ABL:4 + ABL:5) / 2
ENDIF

;支配・羞恥系
IF GROUPMATCH(ARG, 40, 41, 42, 43, 44, 45, 46, 53, 54, 57, 71, 75, 85, 86, 130, 131, 132, 205, 257, 258, 371, 372)
	WEIGHT += ABL:15 + ABL:7
ENDIF

;露出・撮影は露出癖と調教の進行で増やす。
IF GROUPMATCH(ARG, 53, 54, 57, 85, 86)
	WEIGHT += ABL:7 + (ABL:1 + ABL:3 + ABL:4 + ABL:5) / 2
ENDIF

;最低値を保証する。
SIF WEIGHT < 1
	WEIGHT = 1
RETURNF WEIGHT

;-------------------------------------------------
; 非ウフフのオート中、合意があり欲情が十分なら自然に服を脱ぐ。
; 次の自動コマンドはCALLTRAINEND後に再評価され、ウフフ用候補へ切り替わる。
;-------------------------------------------------
@AUTO_TRAIN_EVENTCOMEND
#DIM DYNAMIC DESIRE_BORDER, 1

SIF TFLAG:999 == 0 || TFLAG:44 || TALENT:152 == 0
	RETURN 0

;恋慕・好感度が十分に育つまで、オート側からウフフへ誘導しない。
SIF TALENT:85 == 0 || CFLAG:TARGET:2 < 300 || (TALENT:153 == 0 && TALENT:76 == 0)
	RETURN 0

;欲望Lvが高いほど少ない欲情で誘いに乗る。最低値は200。
DESIRE_BORDER = 600 - ABL:1 * 60
SIF DESIRE_BORDER < 200
	DESIRE_BORDER = 200
SIF PALAM:5 < DESIRE_BORDER
	RETURN 0

PRINTFORMW %CALLNAME:TARGET%は昂った気持ちを隠しきれず、%CALLNAME:MASTER%を誘うように見つめた…
TFLAG:44 = 1
TFLAG:600 = 7
CALL KOJO_JUN
SIF TFLAG:44
	CALL GET_OUT_MOVIE
	TRYCALLFORM CHAR_UNDRESS_{NO:TARGET}
RETURN 0
'''


PARTNER_TURN_SOURCE = r''' ;============================================================
; パートナーのターン追加
; 通常の調教でプレイヤーが一手行った後、パートナーが自分で一手を選んで行う。
; 完全主導権モードの「誘い→リアクション選択」はそのまま残し、ここでは
; 二重入力にならないようリアクションまで自動で決める。
;============================================================
@EVENTCOMEND
#LATER

;設定OFF、完全主導権中、お任せ連続実行中、どちらかが限界の時には重ねない。
SIF (FLAG:62 & 16) == 0 || TFLAG:34 || TFLAG:999 || TARGET < 0 || BASE:TARGET:0 <= 0 || BASE:PLAYER:0 <= 0
	RETURN 0
;調教コマンドの終了時だけ発生させる。終了・設定などのユーザーコマンドは除外する。
SIF SELECTCOM < 0 || SELECTCOM > 414
	RETURN 0
CALL PARTNER_TURN_EXECUTE
RETURN 0

;-------------------------------------------------
; パートナーの追加行動を一手だけ実行する
;-------------------------------------------------
@PARTNER_TURN_EXECUTE

CALL PARTNER_TURN_SELECT
SIF TFLAG:53 <= 0
	RETURN 0

;通常ターンの消費値を引き継がない。PASSIVEMODE経由ではこの初期化が行われないため、
;前の行動のLOSEBASEが残ると、会話のような軽い行動まで過大に消耗してしまう。
LOSEBASE:0 = 0
LOSEBASE:1 = 0
DOWNBASE:MASTER:0 = 0
DOWNBASE:MASTER:4 = 0

DRAWLINE
PRINTFORML 【%CALLNAME:TARGET%のターン】
;相手が何をしたいかを示す既存のパッシブ用口上を使う。
CALL PASSIVEMODE_PASSIVEPHASE(TARGET)

;交流は自然に応じ、性的な誘いは積極的に受け入れる扱いにする。
SELECTCASE TFLAG:53
CASE 8, 9, 10, 12, 15, 21, 22, 23
	RESULT = 0
CASEELSE
	RESULT = 5
ENDSELECT
;SOURCE_CHECK側で体力・気力の消費量を半分にするための一時印。
TFLAG:543 = 1
CALL PASSIVEMODE_ACTIVEPHASE
TFLAG:543 = 0
RETURN 0

;-------------------------------------------------
; 相手が選べる行動を抽出する
; 関係が浅い間は談笑だけに限定し、親密度に応じて段階的に解放する。
;-------------------------------------------------
@PARTNER_TURN_SELECT
#DIM DYNAMIC ACTION, 1
#DIM DYNAMIC ACTION_COUNT, 1
#DIM DYNAMIC SLOT, 1
#DIM DYNAMIC TOTAL_WEIGHT, 1
#DIM DYNAMIC PICK, 1
#DIM DYNAMIC DOTRAIN_BACKUP, 1

VARSET F, 0
TFLAG:53 = 0
DOTRAIN_BACKUP = TFLAG:DOTRAIN
SKIPDISP 1
FOR ACTION, 0, 50
	TRYCCALLFORM PASSIVE_MESSAGE_{ACTION}
		TFLAG:53 = ACTION
		CALL PASSIVEMODE_PASSIVE_COMABLE
		SIF RESULT == 0
			CONTINUE
		;デートは通常COMが行き先入力を開くため、追加ターンでは選ばない。
		SIF ACTION == 29
			CONTINUE
		;押し倒し（脱衣を伴う演出）は相手ターンの候補にしない。
		;脱衣への移行は、非ウフフ時に欲情が閾値へ達したAUTO_TRAIN_EVENTCOMENDだけが行う。
		SIF ACTION == 30
			CONTINUE
		;追加ターンで連発すると単調になるため、頭を撫でるは候補にしない。
		SIF ACTION == 12
			CONTINUE
		;「～させる」系とぱふぱふは、相手の自発行動ではなくプレイヤーへ強く誘導する特殊演出。
		;追加ターンには載せない。
		SIF ACTION >= 43 && ACTION <= 46
			CONTINUE
		;非ウフフ時や着衣中でも、会話・キス・抱擁などの交流行動は候補に残す。
		;明確な性的行動だけをウフフ中かつ脱衣後に限定する。
		IF TFLAG:44 == 0 || UNDERWARED()
			SIF ACTION == 18 || ACTION >= 31
				CONTINUE
		ENDIF
		;関係が浅い間は、談笑だけにする。
		;既存の「見つめあう」は実行後の共通地の文が性的なので、恋慕まで封印する。
		SIF TALENT:TARGET:85 == 0 && ACTION != 22
			CONTINUE
		;恋慕後も、合意がなければ距離を詰める行為は自発しない。
		SIF TALENT:TARGET:152 == 0 && ACTION != 22
			CONTINUE
		;明確に性的な誘いは、恋慕・合意に加えて恋人または淫乱の段階から。
		;恋人なのに淫乱がないだけでキス以外が全落ちしないよう、お任せ側と条件を揃える。
		SIF (ACTION >= 18 && ACTION <= 42) && TALENT:TARGET:153 == 0 && TALENT:TARGET:76 == 0
			CONTINUE
		;相手主導の挿入は、恋人または淫乱に加え、潤滑が始まっており通常コマンドの実行条件を満たす時だけ。
		;実際のコマンド可否も確認してから候補に入れるため、装備・性別などの既存制限もそのまま尊重する。
		IF ACTION == 47
			SIF (TALENT:TARGET:153 == 0 && TALENT:TARGET:76 == 0) || PALAM:3 < PALAMLV:1
				CONTINUE
		ENDIF
		;パッシブ側の条件だけでなく、変換先の通常コマンドが現在のウフフ状態で
		;本当に実行可能かも照合する。会話・キス等の「ウフフ中は不可」を混入させない。
		;COM_ABLE_COMMONはTFLAG:53が立ったままだと通常COMを無条件で拒否するため、
		;行動番号はACTIONに保持したまま、一時的に通常入力相当の状態で判定する。
		SELECTCOM = PASSIVEMODE_CONVERT_PASSIVECOM(PREVCOM, TFLAG:53)
		TFLAG:53 = 0
		TFLAG:DOTRAIN = 1
		;COM_ABLEを持たないパッシブ内部用COMは、個別制限なしとして候補に残す。
		RESULT = 1
		TRYCALLFORM COM_ABLE{SELECTCOM}
		TFLAG:DOTRAIN = DOTRAIN_BACKUP
		TFLAG:53 = ACTION
		SIF RESULT == 0
			CONTINUE
		F:ACTION_COUNT = ACTION
		ACTION_COUNT += 1
	CATCH
		CONTINUE
	ENDCATCH
NEXT
SKIPDISP 0
TFLAG:DOTRAIN = DOTRAIN_BACKUP

IF ACTION_COUNT <= 0
	;ウフフ中は実行不能な会話へフォールバックさせず、相手ターンそのものを見送る。
	;非ウフフ時だけ、従来どおり談笑を安全な最低候補にする。
	IF TFLAG:44
		TFLAG:53 = 0
	ELSE
		TFLAG:53 = 22
	ENDIF
	RETURN 0
ENDIF

FOR SLOT, 0, ACTION_COUNT
	TOTAL_WEIGHT += PARTNER_TURN_ACTION_WEIGHT(F:SLOT)
NEXT
PICK = RAND:TOTAL_WEIGHT
FOR SLOT, 0, ACTION_COUNT
	PICK -= PARTNER_TURN_ACTION_WEIGHT(F:SLOT)
	IF PICK < 0
		TFLAG:53 = F:SLOT
		RETURN 0
	ENDIF
NEXT
TFLAG:53 = F:0
RETURN 0

;-------------------------------------------------
; 素質・能力・進行度に応じた重み
; 親密なら交流、欲望・感覚・奉仕・サド気が伸びれば性的な誘いを選びやすくする。
;-------------------------------------------------
@PARTNER_TURN_ACTION_WEIGHT, ARG
#FUNCTION
#DIM DYNAMIC WEIGHT, 1

WEIGHT = 1
;恋慕前は談笑だけにする。
IF TALENT:TARGET:85 == 0
	SIF ARG == 22
		WEIGHT = 12
	RETURNF WEIGHT
ENDIF
;ウフフ中のキス3種はすべて通常キス(COM6)へ変換される。
;同じ行動へ好感度の巨大な重みが3回乗らないよう、キス枠は低めかつ上限付きにする。
IF GROUPMATCH(ARG, 8, 9, 10)
	IF TFLAG:44
		WEIGHT += 2 + ABL:TARGET:0 / 2 + MIN(CFLAG:TARGET:2 / 20000, 6)
	ELSE
		WEIGHT += 5 + ABL:TARGET:0 + MIN(CFLAG:TARGET:2 / 5000, 12)
	ENDIF
ELSEIF GROUPMATCH(ARG, 12, 15, 21, 22, 23)
	;交流系も好感度を無制限に重みにしない。
	WEIGHT += 8 + ABL:TARGET:0 + MIN(CFLAG:TARGET:2 / 5000, 12)
ENDIF
IF ARG == 30
	WEIGHT += ABL:TARGET:1 + ABL:TARGET:15 + TALENT:TARGET:76 * 4
ENDIF
IF ARG >= 31 && ARG <= 46
	WEIGHT += 2 + ABL:TARGET:1 + ABL:TARGET:6 + (ABL:TARGET:3 + ABL:TARGET:4 + ABL:TARGET:5) / 2
	WEIGHT += TALENT:TARGET:76 * 5
ENDIF
IF ARG >= 35 && ARG <= 42
	WEIGHT += ABL:TARGET:15 + ABL:TARGET:7
ENDIF
;相手主導の騎乗位は条件を満たした後半だけ、欲情・奉仕・感覚が高いほど自然に選ばれやすい。
IF ARG == 47
	;他の性的行動と同じ能力値勾配を使い、少しだけ選ばれやすい程度にする。
	;旧基礎値500では候補総重量の大半を占め、実質的に騎乗位しか出なくなっていた。
	WEIGHT += 8 + ABL:TARGET:1 + ABL:TARGET:6 + (ABL:TARGET:3 + ABL:TARGET:4 + ABL:TARGET:5) / 2
	WEIGHT += TALENT:TARGET:76 * 5 + MIN(PALAM:5 / 5000, 12)
ENDIF
SIF WEIGHT < 1
	WEIGHT = 1
RETURNF WEIGHT
'''


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\n", "\r\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def migrate_endurance_option(text: str) -> str:
    """旧パートナーターン用bit4から、耐力専用bit17へ表記を正規化する。"""
    return text.replace("FLAG:62 & 16", "FLAG:62 & 1p17")


def main() -> None:
    text = read_cp932(USERCOM)
    show_anchor = '''IF TFLAG:34 == 0 && (FLAG:23 & 8)\r
\tPRINTC 主導権を決める[851]\r
\tCALL NEWLINE\r
ENDIF\r
'''
    old_show_block = show_anchor + ''';ウフフ中は通常の調教コマンドをパートナーAIに連続選択させられる\r
IF TFLAG:44 && TFLAG:34 == 0\r
\tPRINTC オート調教[852]\r
\tCALL NEWLINE\r
ENDIF\r
'''
    current_show_insert = show_anchor + ''';通常時・ウフフ中のどちらでも、パートナーAIに連続行動を任せられる\r
IF TFLAG:34 == 0\r
\tPRINTC オート調教[852]\r
\tCALL NEWLINE\r
ENDIF\r
'''
    show_insert = show_anchor + ''';通常時・ウフフ中のどちらでも、パートナーAIに連続行動を任せられる\r
IF TFLAG:34 == 0\r
\tPRINTC パートナーに任せる[852]\r
\tCALL NEWLINE\r
ENDIF\r
'''
    if old_show_block in text:
        text = text.replace(old_show_block, show_insert, 1)
    elif current_show_insert in text:
        text = text.replace(current_show_insert, show_insert, 1)
    elif show_insert not in text:
        raise SystemExit("show menu block not found")

    handle_anchor = '''ELSEIF RESULT == 860\r
\t;コンフィグ\r
\tCALL START_CONFIGURE\r
'''
    old_handle_block = '''ELSEIF RESULT == 852 && TFLAG:44 && TFLAG:34 == 0\r
\tCALL AUTO_TRAIN_SELECT\r
\tRETURN 1\r
''' + handle_anchor
    handle_insert = '''ELSEIF RESULT == 852 && TFLAG:34 == 0\r
\tCALL AUTO_TRAIN_SELECT\r
\tRETURN 1\r
''' + handle_anchor
    if old_handle_block in text:
        text = text.replace(old_handle_block, handle_insert, 1)
    elif handle_insert not in text:
        raise SystemExit("usercom handler block not found")
    calltrain_end = '''@CALLTRAINEND\r
TFLAG:CALLTRAIN = 0\r
'''
    auto_continue_block = ''';オート調教中なら、状態を再評価して次の1手へ進む。\r
SIF TFLAG:999\r
\tCALL AUTO_TRAIN_CONTINUE\r
'''
    # CALLTRAINは使用しない。旧版が残した継続呼び出しをすべて除去する。
    if calltrain_end in text:
        block_start = text.index(calltrain_end) + len(calltrain_end)
        block_end = block_start
        while text.startswith(auto_continue_block, block_end):
            block_end += len(auto_continue_block)
        text = text[:block_start] + text[block_end:]
    else:
        raise SystemExit("CALLTRAINEND anchor not found")
    write_cp932(USERCOM, text)

    info = read_cp932(INFO)
    status_reset = '''TFLAG:DOTRAIN = 0\r
TFLAG:CALLTRAIN = 0\r
'''
    status_reset_new = '''TFLAG:DOTRAIN = 0\r
;通常のCALLTRAINはここで終了扱いにするが、オート調教の連続実行中は維持する。\r
SIF TFLAG:999 == 0\r
\tTFLAG:CALLTRAIN = 0\r
'''
    if status_reset in info:
        info = info.replace(status_reset, status_reset_new, 1)
    elif status_reset_new not in info:
        raise SystemExit("SHOW_STATUS CALLTRAIN reset anchor not found")
    write_cp932(INFO, info)

    date = read_cp932(DATE)
    auto_date_continue = '''IF TFLAG:999 && TEQUIP:2 && MONEY > 2000 && TFLAG:44 == 0 && TFLAG:62 == 0\r
\t;オート中の再デートは、パートナーが次の行き先を決める。\r
\tFLAG:8 = TEQUIP:2\r
\tGOTO DATE_LOOP4\r
ENDIF\r
'''
    date_start = '''IF TEQUIP:2 && MONEY > 2000 && TFLAG:44 == 0 && TFLAG:62 == 0\r
'''
    while auto_date_continue + auto_date_continue in date:
        date = date.replace(
            auto_date_continue + auto_date_continue,
            auto_date_continue,
            1,
        )
    if auto_date_continue + date_start in date:
        pass
    elif date_start in date:
        date = date.replace(date_start, auto_date_continue + date_start, 1)
    else:
        raise SystemExit("COM323 auto date start anchor not found")

    manual_date_input = '''\t\tCALL GENSOUKYO_DATE\r
'''
    auto_date_input_prefix = '''\t\t;オート中は入力を出さず、パートナーが選んだ標準行き先へ向かう。\r
\t\tIF TFLAG:999\r
\t\t\tSIF LOCAL < 1 || LOCAL > 9\r
\t\t\t\tLOCAL = 1\r
\t\t\tTEQUIP:2 = LOCAL\r
\t\t\tTFLAG:17 = 1\r
\t\t\tCALL PLACE_NAME\r
\t\t\tPRINTFORML %CALLNAME:TARGET%は%STR:4%へ行きたいようだ\r
\t\tELSE\r
'''
    auto_date_input_suffix = '''\t\tENDIF\r
'''
    auto_date_input = auto_date_input_prefix + manual_date_input + auto_date_input_suffix
    # 既存の入力箇所は「主導権で行き先決定」と「強制行き先決定」の二つのIF内にある。
    # 領域丸ごとの復旧時は、その外側二段の終端も戻す。
    auto_date_repaired = auto_date_input + '''\tENDIF\r
ENDIF\r
'''
    # 旧版は置換後に残るCALL GENSOUKYO_DATEを再び置換し、同じIFを大量に入れ子にしていた。
    # さらに置換元が行頭アンカーでなかったため字下げとENDIF数まで壊れている版がある。
    # この入力部分の直後にある固定コメントを終端として、領域全体を正規形へ戻す。
    auto_date_marker = "\t\t;オート中は入力を出さず、パートナーが選んだ標準行き先へ向かう。"
    auto_date_start = date.find(auto_date_marker)
    if auto_date_start >= 0:
        auto_date_end_marker = ";何処も選択しなかった場合\r\n"
        auto_date_end = date.find(auto_date_end_marker, auto_date_start)
        if auto_date_end < 0:
            raise SystemExit("COM323 date selection end anchor not found")
        date = date[:auto_date_start] + auto_date_repaired + date[auto_date_end:]
    elif manual_date_input in date:
        date = date.replace(manual_date_input, auto_date_input, 1)
    else:
        raise SystemExit("COM323 date selection anchor not found")
    write_cp932(DATE, date)

    # パートナーのターン追加（FLAG:62 bit4）専用の耐力消費。
    # 通常調教では絶頂処理の後に強度を加味して直接減算し、REVMODEでは
    # 従来のDOWNBASE経路を利用する。耐力0での強制終了はどちらにも行わない。
    counter = migrate_endurance_option(read_cp932(COUNTER))
    legacy_female_exhaustion_growth = '''\t\t;女性側の最大耐力はEXP:2を参照する。枯渇経験も大きな成長として加算する。\r
\t\tEXP:(TFLAG:996):2 += 100\r
'''


    current_female_exhaustion_growth = '''\t\t;絶頂経験とは分けて、耐力枯渇回数だけを別カウンタへ記録する。\r
\t\tCFLAG:(TFLAG:996):1153 += 80 + RAND(41)\r
'''
    if legacy_female_exhaustion_growth in counter:
        counter = counter.replace(legacy_female_exhaustion_growth, current_female_exhaustion_growth, 1)
    # 旧版の固定成長値（回数）を、今回のランダム成長ポイント加算へ移行する。
    counter = counter.replace("CFLAG:MASTER:1152 += 1\r\n", "CFLAG:MASTER:1152 += 80 + RAND(41)\r\n")
    counter = counter.replace("CFLAG:(TFLAG:996):1153 += 1\r\n", "CFLAG:(TFLAG:996):1153 += 80 + RAND(41)\r\n")
    counter = counter.replace("CFLAG:(TFLAG:996):1154 += 1\r\n", "CFLAG:(TFLAG:996):1154 += 16 + RAND(9)\r\n")
    damage_call = ''';耐力減少量の算出\r
CALL COUNTER_EJAC_DAMAGE\r
'''
    damage_call_new = ''';通常調教の耐力減少は、絶頂強度確定後に処理する。\r
;REVMODEでは従来どおりDOWNBASEへ積み、同じオプションがONの時だけ適用する。\r
SIF TFLAG:34\r
\tCALL COUNTER_EJAC_DAMAGE\r
'''
    if damage_call in counter:
        counter = counter.replace(damage_call, damage_call_new, 1)
    elif damage_call_new not in counter:
        raise SystemExit("counter damage call anchor not found")

    old_counter_damage = '''@COUNTER_EJAC_DAMAGE\r
;基準値(TFLAG:302　1:射精　2:大量射精　4:超大量射精）\r
IF TFLAG:302 == 1\r
\tLOCAL = 100\r
ELSEIF TFLAG:302 == 2\r
\tLOCAL = 200\r
ELSE\r
\tLOCAL = 300\r
ENDIF\r
\r
;押し倒され中はダメージ倍\r
SIF TFLAG:51\r
\tLOCAL *= 2\r
\r
;耐力低下の処理。\r
DOWNBASE:(TFLAG:996):4 = LOCAL\r
'''
    new_counter_damage = '''@COUNTER_EJAC_DAMAGE\r
;REVMODE用。パートナーのターン追加をONにした場合だけ耐力を消費する。\r
;通常調教では、絶頂強度まで確定した後にPARTNER_TURN_ENDURANCE_DAMAGEが処理する。\r
SIF (FLAG:62 & 1p17) == 0 && TFLAG:997 == 0\r
\tRETURN 0\r
\r
;連射倍率は平方根に圧縮し、育成値が伸びても耐力消費だけが暴走しないようにする。\r
;射精量区分(1/2/4)と実測mlは従来どおり反映する。\r
LOCAL = 600 * TFLAG:302 * SQRT(TFLAG:714)\r
LOCAL += TFLAG:719 * TFLAG:302 * 2\r
SIF LOCAL < 1\r
\tLOCAL = 1\r
\r
;押し倒され中はダメージ倍\r
SIF TFLAG:51\r
\tLOCAL *= 2\r
\r
DOWNBASE:MASTER:4 = LOCAL\r
\r
;---------------------------------------------------------\r
;通常調教用。ARG～ARG:4はC/V/A/B/Mそれぞれの絶頂強度。\r
;射精量が極端、または強い多重絶頂ほど急激に耐力を失う。\r
;耐力0は強制終了条件にしない。\r
;---------------------------------------------------------\r
@PARTNER_TURN_ENDURANCE_DAMAGE, ARG, ARG:1, ARG:2, ARG:3, ARG:4\r
#DIM DYNAMIC DAMAGE, 1\r
#DIM DYNAMIC STRENGTH, 1\r
#DIM DYNAMIC ORGASM_COUNT, 1\r
\r
SIF (FLAG:62 & 1p17) == 0 || TFLAG:302 == 0 || P != MASTER\r
\tRETURN 0\r
\r
;連射倍率は平方根に圧縮し、射精量区分と実測mlを加算する。\r
DAMAGE = 600 * TFLAG:302 * SQRT(TFLAG:714)\r
DAMAGE += TFLAG:719 * TFLAG:302 * 2\r
\r
STRENGTH = MAX(ARG, ARG:1, ARG:2, ARG:3, ARG:4)\r
SIF ARG\r
\tORGASM_COUNT += 1\r
SIF ARG:1\r
\tORGASM_COUNT += 1\r
SIF ARG:2\r
\tORGASM_COUNT += 1\r
SIF ARG:3\r
\tORGASM_COUNT += 1\r
SIF ARG:4\r
\tORGASM_COUNT += 1\r
\r
;絶頂強度と多重絶頂も反映するが、育成速度を越えて急増しない倍率に抑える。\r
SIF STRENGTH || ORGASM_COUNT\r
\tDAMAGE = DAMAGE * (100 + STRENGTH * 2 + MAX(ORGASM_COUNT - 1, 0) * 10) / 100\r
SIF DAMAGE < 1\r
\tDAMAGE = 1\r
\r
PRINTFORML %CALLNAME:MASTER%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
BASE:MASTER:4 -= DAMAGE\r
SIF BASE:MASTER:4 < 0\r
\tBASE:MASTER:4 = 0\r
RETURN 0\r
'''
    if old_counter_damage in counter:
        counter = counter.replace(old_counter_damage, new_counter_damage, 1)
    elif "@COUNTER_EJAC_DAMAGE" not in counter or "@PARTNER_TURN_ENDURANCE_DAMAGE" not in counter:
        raise SystemExit("COUNTER_EJAC_DAMAGE block not found")
    # 旧版の線形倍率は、表示倍率が育つほど耐力ダメージだけが同じ速度で暴走する。
    # 表示倍率自体は維持しつつ、耐力負荷には平方根を使う正規形へ移行する。
    revmode_damage_linear = ''';射精量区分(1/2/4)、連射倍率、実測mlを反映する。\r
LOCAL = 20 * TFLAG:302 * TFLAG:714\r
'''
    revmode_damage_sqrt_legacy = ''';連射倍率は平方根に圧縮し、育成値が伸びても耐力消費だけが暴走しないようにする。\r
;射精量区分(1/2/4)と実測mlは従来どおり反映する。\r
LOCAL = 20 * TFLAG:302 * SQRT(TFLAG:714)\r
'''
    revmode_damage_sqrt = revmode_damage_sqrt_legacy.replace(
        "LOCAL = 20 * TFLAG:302",
        "LOCAL = 600 * TFLAG:302",
        1,
    )
    if revmode_damage_linear in counter:
        counter = counter.replace(revmode_damage_linear, revmode_damage_sqrt, 1)
    elif revmode_damage_sqrt_legacy in counter:
        counter = counter.replace(revmode_damage_sqrt_legacy, revmode_damage_sqrt, 1)
    elif revmode_damage_sqrt not in counter:
        raise SystemExit("REVMODE endurance damage curve anchor not found")
    normal_damage_linear = ''';基礎は射精量区分と連射倍率。実測mlも加算する。\r
DAMAGE = 20 * TFLAG:302 * TFLAG:714\r
'''
    normal_damage_sqrt_legacy = ''';連射倍率は平方根に圧縮し、射精量区分と実測mlを加算する。\r
DAMAGE = 20 * TFLAG:302 * SQRT(TFLAG:714)\r
'''
    normal_damage_sqrt = normal_damage_sqrt_legacy.replace(
        "DAMAGE = 20 * TFLAG:302",
        "DAMAGE = 600 * TFLAG:302",
        1,
    )
    if normal_damage_linear in counter:
        counter = counter.replace(normal_damage_linear, normal_damage_sqrt, 1)
    elif normal_damage_sqrt_legacy in counter:
        counter = counter.replace(normal_damage_sqrt_legacy, normal_damage_sqrt, 1)
    elif normal_damage_sqrt not in counter:
        raise SystemExit("normal endurance damage curve anchor not found")
    orgasm_damage_steep = ''';最強絶頂以上や多重絶頂は大きく跳ね上がる。大量に絞り出されれば致命的な消耗になる。\r
SIF STRENGTH || ORGASM_COUNT\r
\tDAMAGE = DAMAGE * (100 + STRENGTH * 10 + (ORGASM_COUNT - 1) * 25) / 100\r
'''
    orgasm_damage_balanced = ''';絶頂強度と多重絶頂も反映するが、育成速度を越えて急増しない倍率に抑える。\r
SIF STRENGTH || ORGASM_COUNT\r
\tDAMAGE = DAMAGE * (100 + STRENGTH * 2 + MAX(ORGASM_COUNT - 1, 0) * 10) / 100\r
'''
    if orgasm_damage_steep in counter:
        counter = counter.replace(orgasm_damage_steep, orgasm_damage_balanced, 1)
    elif orgasm_damage_balanced not in counter:
        raise SystemExit("orgasm endurance damage curve anchor not found")
    revmode_downbase_old = '''DOWNBASE:MASTER:4 = LOCAL\r
'''
    revmode_downbase_new = '''DOWNBASE:(TFLAG:996):4 = LOCAL\r
'''
    if revmode_downbase_old in counter:
        counter = counter.replace(revmode_downbase_old, revmode_downbase_new, 1)
    elif revmode_downbase_new not in counter:
        raise SystemExit("REVMODE endurance target anchor not found")
    write_cp932(COUNTER, counter)

    shoot = migrate_endurance_option(read_cp932(SHOOT))
    semen_cap_legacy = ''';オーバーフロー対策に、値が大きすぎる場合と、負の場合は調整を加える\r
IF BASE:PLAYER:2 > 100000000 || BASE:PLAYER:2 < 0\r
\tBASE:PLAYER:2 = 100000000\r
ENDIF\r
'''
    semen_cap_balanced = ''';育成の余地を確保しつつオーバーフローを防ぐ。負数は上限ではなく0へ戻す。\r
IF BASE:PLAYER:2 > 1000000000000000\r
\tBASE:PLAYER:2 = 1000000000000000\r
ELSEIF BASE:PLAYER:2 < 0\r
\tBASE:PLAYER:2 = 0\r
ENDIF\r
'''
    if semen_cap_legacy in shoot:
        shoot = shoot.replace(semen_cap_legacy, semen_cap_balanced, 1)
    elif semen_cap_balanced not in shoot:
        raise SystemExit("SAMEN_CHECK ejaculation gauge cap anchor not found")
    shooter_anchor = '''ELSE\r
\tP = PLAYER\r
ENDIF\r
\r
;射精する対象の設定\r
'''
    shooter_insert = '''ELSE\r
\tP = PLAYER\r
ENDIF\r
\r
;耐力消費の対象を射精した瞬間に記録する。後段の処理でPが変わっても判定を失わない。\r
TFLAG:994 = 0\r
TFLAG:996 = P\r
SIF (FLAG:62 & 1p17) || TFLAG:997\r
\tTFLAG:994 = 1\r
;耐力が尽きた射精者は、精を出さないまま快感だけを味わう。\r
IF TFLAG:994 && BASE:(TFLAG:996):4 <= 0 && TFLAG:302\r
\t;精を出せないまま搾られた回数も、絶頂経験とは別に耐力上限を鍛える。\r
\tCFLAG:(TFLAG:996):1154 += 16 + RAND(9)\r
\tE = 0\r
\tTFLAG:302 = 0\r
\tTFLAG:714 = 0\r
\tSIF EJAC > 0\r
\t\tBASE:(TFLAG:996):2 = EJAC - 1\r
\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML もう何も出せないのに、%CALLNAME:TARGET%の責めに%CALLNAME:(TFLAG:996)%の身体だけが震えている……\r
\tCASE 1\r
\t\tPRINTFORML 空になったはずの奥をなお弄ばれ、%CALLNAME:(TFLAG:996)%は声もなく絶頂だけを繰り返した……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は容赦なく快感を重ね、%CALLNAME:(TFLAG:996)%から残り香まで搾り取っていく……\r
\tCASEELSE\r
\t\tPRINTFORML これ以上は出せない。それでも続く刺激に、%CALLNAME:(TFLAG:996)%は力なく身体を跳ねさせた……\r
\tENDSELECT\r
\tRETURN 0\r
ENDIF\r
\r
;射精する対象の設定\r
'''
    if shooter_anchor in shoot:
        shoot = shoot.replace(shooter_anchor, shooter_insert, 1)
    elif "耐力消費の対象を射精した瞬間に記録する" not in shoot:
        raise SystemExit("SAMEN_SHOOT shooter anchor not found")
    shooter_option_legacy = '''TFLAG:994 = 0\r
SIF ((FLAG:62 & 1p17) || TFLAG:997) && (P == PLAYER || P == MASTER)\r
\tTFLAG:994 = 1\r
'''
    shooter_option_new = '''TFLAG:994 = 0\r
TFLAG:996 = P\r
SIF (FLAG:62 & 1p17) || TFLAG:997\r
\tTFLAG:994 = 1\r
;耐力が尽きた射精者は、精を出さないまま快感だけを味わう。\r
IF TFLAG:994 && BASE:(TFLAG:996):4 <= 0 && TFLAG:302\r
\tE = 0\r
\tTFLAG:302 = 0\r
\tTFLAG:714 = 0\r
\tSIF EJAC > 0\r
\t\tBASE:(TFLAG:996):2 = EJAC - 1\r
\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML もう何も出せないのに、%CALLNAME:TARGET%の責めに%CALLNAME:(TFLAG:996)%の身体だけが震えている……\r
\tCASE 1\r
\t\tPRINTFORML 空になったはずの奥をなお弄ばれ、%CALLNAME:(TFLAG:996)%は声もなく絶頂だけを繰り返した……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は容赦なく快感を重ね、%CALLNAME:(TFLAG:996)%から残り香まで搾り取っていく……\r
\tCASEELSE\r
\t\tPRINTFORML これ以上は出せない。それでも続く刺激に、%CALLNAME:(TFLAG:996)%は力なく身体を跳ねさせた……\r
\tENDSELECT\r
\tRETURN 0\r
ENDIF\r
\r
'''
    if shooter_option_legacy in shoot:
        shoot = shoot.replace(shooter_option_legacy, shooter_option_new, 1)
    elif "TFLAG:996 = P" not in shoot:
        raise SystemExit("SAMEN_SHOOT endurance option anchor not found")
    dry_growth_old = '''IF TFLAG:994 && BASE:(TFLAG:996):4 <= 0 && TFLAG:302\r
\tE = 0\r
'''
    dry_growth_new = '''IF TFLAG:994 && BASE:(TFLAG:996):4 <= 0 && TFLAG:302\r
\t;精を出せないまま搾られた回数も、絶頂経験とは別に耐力上限を鍛える。\r
\tCFLAG:(TFLAG:996):1154 += 16 + RAND(9)\r
\tE = 0\r
'''
    dry_growth_legacy = '''IF TFLAG:994 && BASE:(TFLAG:996):4 <= 0 && TFLAG:302\r
\t;精を出せないまま搾られた回数も、絶頂経験とは別に耐力上限を鍛える。\r
\tCFLAG:(TFLAG:996):1154 += 1\r
\tE = 0\r
'''
    if dry_growth_legacy in shoot:
        shoot = shoot.replace(dry_growth_legacy, dry_growth_new, 1)
    elif dry_growth_old in shoot:
        shoot = shoot.replace(dry_growth_old, dry_growth_new, 1)
    elif dry_growth_new not in shoot:
        raise SystemExit("dry endurance growth anchor not found")
    write_cp932(SHOOT, shoot)

    counter = migrate_endurance_option(read_cp932(COUNTER))
    old_damage_guard = '''SIF (FLAG:62 & 1p17) == 0 || TFLAG:302 == 0 || P != MASTER\r
\tRETURN 0\r
'''
    new_damage_guard = '''IF (FLAG:62 & 1p17) == 0 || TFLAG:302 == 0 || TFLAG:994 == 0\r
\tTFLAG:994 = 0\r
\tRETURN 0\r
ENDIF\r
'''
    if old_damage_guard in counter:
        counter = counter.replace(old_damage_guard, new_damage_guard, 1)
    elif new_damage_guard not in counter:
        raise SystemExit("partner endurance damage guard not found")
    damage_tail = '''SIF BASE:MASTER:4 < 0\r
\tBASE:MASTER:4 = 0\r
RETURN 0\r
'''
    damage_tail_new = '''SIF BASE:MASTER:4 < 0\r
\tBASE:MASTER:4 = 0\r
TFLAG:994 = 0\r
RETURN 0\r
'''
    if damage_tail in counter:
        counter = counter.replace(damage_tail, damage_tail_new, 1)
    elif damage_tail_new not in counter and "IF BEFORE_ENDURANCE > 0 && BASE:MASTER:4 == 0" not in counter and "IF BEFORE_ENDURANCE > 0 && BASE:(TFLAG:996):4 == 0" not in counter:
        raise SystemExit("partner endurance damage tail not found")

    # 耐力も、減算・表示の前に半額化する。後から値を戻す方式では表示が一致しない。
    partner_turn_endurance_anchor = '''SIF DAMAGE < 1\r
\tDAMAGE = 1\r
\r
PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
'''
    partner_turn_endurance_insert = '''SIF DAMAGE < 1\r
\tDAMAGE = 1\r
;パートナーの追加ターン中は、耐力の実消費量と表示をともに半額にする。\r
SIF TFLAG:543\r
\tDAMAGE = (DAMAGE + 1) / 2\r
\r
PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
'''
    partner_turn_endurance_anchor_with_load = partner_turn_endurance_anchor.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（射精量×{TFLAG:714}、負荷倍率×{SQRT(TFLAG:714)}、絶頂強度{STRENGTH}）",
        1,
    )
    partner_turn_endurance_insert_with_load = partner_turn_endurance_insert.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（射精量×{TFLAG:714}、負荷倍率×{SQRT(TFLAG:714)}、絶頂強度{STRENGTH}）",
        1,
    )
    partner_turn_endurance_anchor_clean = partner_turn_endurance_anchor.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（絶頂強度{STRENGTH}）",
        1,
    )
    partner_turn_endurance_insert_clean = partner_turn_endurance_insert.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（絶頂強度{STRENGTH}）",
        1,
    )
    if (
        partner_turn_endurance_insert in counter
        or partner_turn_endurance_insert_with_load in counter
        or partner_turn_endurance_insert_clean in counter
    ):
        pass
    elif partner_turn_endurance_anchor in counter:
        counter = counter.replace(partner_turn_endurance_anchor, partner_turn_endurance_insert, 1)
    elif partner_turn_endurance_anchor_with_load in counter:
        counter = counter.replace(
            partner_turn_endurance_anchor_with_load,
            partner_turn_endurance_insert_with_load,
            1,
        )
    elif partner_turn_endurance_anchor_clean in counter:
        counter = counter.replace(
            partner_turn_endurance_anchor_clean,
            partner_turn_endurance_insert_clean,
            1,
        )
    else:
        raise SystemExit("partner turn half-endurance counter anchor not found")
    write_cp932(COUNTER, counter)

    source = read_cp932(SOURCE)
    old_orgasm_tail = ''';絶頂強度を返す\r
;絶頂時口上フック\r
IF C || V || A || B || M\r
\tTFLAG:710 = LOCAL:5\r
\tTRYCALLFORM CHAR_ORGASM_{NO:TARGET}\r
ENDIF\r
RETURN C, V, A, B, M\r
'''
    new_orgasm_tail = ''';絶頂強度を返す\r
;絶頂時口上フック\r
IF C || V || A || B || M\r
\tTFLAG:710 = LOCAL:5\r
\tTRYCALLFORM CHAR_ORGASM_{NO:TARGET}\r
ENDIF\r
;パートナーのターン追加をONにした場合だけ、射精量と今回の絶頂強度から耐力を消費する。\r
CALL PARTNER_TURN_ENDURANCE_DAMAGE, C, V, A, B, M\r
RETURN C, V, A, B, M\r
'''
    if old_orgasm_tail in source:
        source = source.replace(old_orgasm_tail, new_orgasm_tail, 1)
    elif new_orgasm_tail not in source:
        raise SystemExit("ORGASM_PROCESS tail anchor not found")
    old_forced_end = ''';-------------------------------------------------\r
;MASTERの体力が限界の際の終了\r
;-------------------------------------------------\r
SIF BASE:MASTER:0 <= 500\r
\tCALL COUNTER_DOWN\r
\r
'''
    new_forced_end = ''';-------------------------------------------------\r
;主人公の体力・耐力による調教の強制終了は行わない。\r
;耐力はパートナーのターン追加をONにした際の消耗リソースとして0で止める。\r
;-------------------------------------------------\r
\r
'''
    if old_forced_end in source:
        source = source.replace(old_forced_end, new_forced_end, 1)
    elif new_forced_end not in source:
        raise SystemExit("normal forced-end anchor not found")

    # パートナーターンはSOURCE_CHECKの段階で半額へ補正する。
    # ここなら実際の減少値と「体力-/気力-」の表示値が常に一致する。
    partner_turn_cost_anchor = '''BASE:0 -= LOSEBASE:0\r
BASE:1 -= LOSEBASE:1\r
'''
    partner_turn_cost_insert = ''';パートナー主導の一手は、相手に無理をさせないペースで進む。\r
;表示前に補正するため、体力・気力の実消費量と表示をともに半額にする。\r
IF TFLAG:543\r
\tLOSEBASE:0 = (LOSEBASE:0 + 1) / 2\r
\tLOSEBASE:1 = (LOSEBASE:1 + 1) / 2\r
\tDOWNBASE:MASTER:0 = (DOWNBASE:MASTER:0 + 1) / 2\r
ENDIF\r
\r
BASE:0 -= LOSEBASE:0\r
BASE:1 -= LOSEBASE:1\r
'''
    # 旧版の補正ブロックは末尾のBASE減算を含んでいたため、先に取り除いて正規化する。
    # 旧版・新版が混在していても、補正コメントからBASE減算直前までをまとめて一つにする。
    partner_turn_cost_start = ";パートナー主導の一手は、相手に無理をさせないペースで進む。\r\n"
    start = source.find(partner_turn_cost_start)
    if start >= 0:
        end = source.find(partner_turn_cost_anchor, start)
        if end < 0:
            raise SystemExit("partner turn half-cost cleanup anchor not found")
        source = source[:start] + source[end:]
    if partner_turn_cost_anchor in source:
        source = source.replace(partner_turn_cost_anchor, partner_turn_cost_insert, 1)
    else:
        raise SystemExit("partner turn half-cost source anchor not found")
    write_cp932(SOURCE, source)

    revmode = migrate_endurance_option(read_cp932(REVMODE))
    rev_start = ''';コンフィグを保存\r
PRICONFIG = FLAG:62\r
;パートナーのターンを削除\r
CLEARBIT FLAG:62, 4\r
'''
    rev_start_new = ''';コンフィグを保存\r
PRICONFIG = FLAG:62\r
;パートナーのターン追加がONだったかを保持する。REVMODE中は同ビットを一時的に消すため。\r
TFLAG:997 = FLAG:62 & 1p17\r
;パートナーのターンを削除\r
CLEARBIT FLAG:62, 4\r
'''
    if rev_start in revmode:
        revmode = revmode.replace(rev_start, rev_start_new, 1)
    elif rev_start_new not in revmode:
        raise SystemExit("REVMODE config anchor not found")
    rev_end = ''';コンフィグを元に戻す\r
FLAG:62 = PRICONFIG\r
;PLAYERの体力が0以下\r
SIF BASE:MASTER:4 <= 0\r
\tCALL COUNTER_DOWN\r
;調教終了\r
BEGIN AFTERTRAIN\r
'''
    rev_end_new = ''';コンフィグを元に戻す\r
FLAG:62 = PRICONFIG\r
;耐力0は強制終了にしない。\r
TFLAG:997 = 0\r
;調教終了\r
BEGIN AFTERTRAIN\r
'''
    if rev_end in revmode:
        revmode = revmode.replace(rev_end, rev_end_new, 1)
    elif rev_end_new not in revmode:
        raise SystemExit("REVMODE forced-end anchor not found")
    # パートナーターンはPASSIVEMODEからREVMODE_SOURCE_CHECKを通る。
    # 通常のSOURCE_CHECKだけを補正してもここには反映されないため、同じく減算・表示前に半額化する。
    revmode_half_anchor = ''';体力・気力の減少\r
BASE:0 -= LOSEBASE:0\r
BASE:1 -= LOSEBASE:1\r
'''
    revmode_half_insert = ''';体力・気力の減少\r
;パートナー主導の一手は、体力・気力・耐力の実消費量と表示をともに半額にする。\r
IF TFLAG:543\r
\tLOSEBASE:0 = (LOSEBASE:0 + 1) / 2\r
\tLOSEBASE:1 = (LOSEBASE:1 + 1) / 2\r
\tDOWNBASE:MASTER:4 = (DOWNBASE:MASTER:4 + 1) / 2\r
ENDIF\r
BASE:0 -= LOSEBASE:0\r
BASE:1 -= LOSEBASE:1\r
'''
    revmode_half_start = ";パートナー主導の一手は、体力・気力・耐力の実消費量と表示をともに半額にする。\r\n"
    start = revmode.find(revmode_half_start)
    if start >= 0:
        end = revmode.find("BASE:0 -= LOSEBASE:0\r\nBASE:1 -= LOSEBASE:1\r\n", start)
        if end < 0:
            raise SystemExit("REVMODE half-cost cleanup anchor not found")
        revmode = revmode[:start] + revmode[end:]
    if revmode_half_anchor in revmode:
        revmode = revmode.replace(revmode_half_anchor, revmode_half_insert, 1)
    else:
        raise SystemExit("REVMODE half-cost anchor not found")
    write_cp932(REVMODE, revmode)

    passive = read_cp932(PASSIVE)
    passive_old_narration = '''PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に他愛の無い話をかけてきた…\r
'''
    passive_new_narration = '''PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に他愛のない話をしてきた…\r
'''
    if passive_old_narration in passive:
        passive = passive.replace(passive_old_narration, passive_new_narration, 1)
    elif passive_new_narration not in passive:
        raise SystemExit("partner talk narration anchor not found")

    passive_intimate_gate_old = ''';淫乱がないとハード系コマンドはダメ\r
SIF TALENT:76 == 0 && TFLAG:53 >= 31\r
	RETURN 0\r
'''
    passive_intimate_gate_new = ''';恋人でも淫乱でもない場合はハード系コマンドを選ばない\r
SIF TALENT:76 == 0 && TALENT:153 == 0 && TFLAG:53 >= 31\r
	RETURN 0\r
'''
    if passive_intimate_gate_old in passive:
        passive = passive.replace(passive_intimate_gate_old, passive_intimate_gate_new, 1)
    elif passive_intimate_gate_new not in passive:
        raise SystemExit("passive intimate action gate anchor not found")

    passive_name_old = '''TSTR:46 = ぱふぱふ\r
\r
;----------------------------------------------------------------\r
'''
    passive_name_new = '''TSTR:46 = ぱふぱふ\r
TSTR:47 = 騎乗位\r
\r
;----------------------------------------------------------------\r
'''
    if passive_name_old in passive:
        passive = passive.replace(passive_name_old, passive_name_new, 1)
    elif passive_name_new not in passive:
        raise SystemExit("partner insertion name anchor not found")

    passive_convert_old = '''CASE 42\r
\t;アナル舐め\r
\tRETURNF 9\r
;手で愛撫させる\r
'''
    passive_convert_new = '''CASE 42\r
\t;アナル舐め\r
\tRETURNF 9\r
;騎乗位\r
CASE 47\r
\t;騎乗位\r
\tRETURNF 34\r
;手で愛撫させる\r
'''
    if passive_convert_old in passive:
        passive = passive.replace(passive_convert_old, passive_convert_new, 1)
    elif passive_convert_new not in passive:
        raise SystemExit("partner insertion conversion anchor not found")

    # 非ウフフ時は通常のキス3種、ウフフ中は既存の通常「キスする」コマンドを使う。
    # キス性交へ変換しない。通常キスはウフフ中に実行できないため、候補判定で自然に外れる。
    passive_kiss_old = ''';バードキス\r
CASE 8\r
\t;バードキス\r
\tRETURNF 340\r
;ソフトキス\r
CASE 9\r
\t;ソフトキス\r
\tRETURNF 341\r
;ディープキス\r
CASE 10\r
\t;ディープキス\r
\tRETURNF 342\r
;頭を撫でる\r
'''
    passive_kiss_new = ''';キス\r
CASE 8, 9, 10\r
\tIF TFLAG:44\r
\t\tSELECTCASE ARG:0\r
\t\tCASE 20, 120\r
\t\t\t;キス正常位\r
\t\t\tRETURNF 120\r
\t\tCASE 21, 121\r
\t\t\t;キス後背位\r
\t\t\tRETURNF 121\r
\t\tCASE 24, 122\r
\t\t\t;キス対面座位\r
\t\t\tRETURNF 122\r
\t\tCASE 25, 123\r
\t\t\t;キス背面座位\r
\t\t\tRETURNF 123\r
\t\tCASE 34, 124\r
\t\t\t;キス騎乗位\r
\t\t\tRETURNF 124\r
\t\tCASEELSE\r
\t\t\t;対応するキス体位が無い場合は通常キス。COM_ABLEで候補から外れる。\r
\t\t\tRETURNF 340\r
\t\tENDSELECT\r
\tELSE\r
\t\tSELECTCASE TFLAG:53\r
\t\tCASE 8\r
\t\t\tRETURNF 340\r
\t\tCASE 9\r
\t\t\tRETURNF 341\r
\t\tCASEELSE\r
\t\t\tRETURNF 342\r
\t\tENDSELECT\r
\tENDIF\r
;頭を撫でる\r
'''
    passive_kiss_simple = ''';キス\r
CASE 8, 9, 10\r
\tIF TFLAG:44\r
\t\t;ウフフ中用の通常キス\r
\t\tRETURNF 6\r
\tELSE\r
\t\tSELECTCASE TFLAG:53\r
\t\tCASE 8\r
\t\t\tRETURNF 340\r
\t\tCASE 9\r
\t\t\tRETURNF 341\r
\t\tCASEELSE\r
\t\t\tRETURNF 342\r
\t\tENDSELECT\r
\tENDIF\r
;頭を撫でる\r
'''
    if passive_kiss_old in passive:
        passive = passive.replace(passive_kiss_old, passive_kiss_simple, 1)
    elif passive_kiss_new in passive:
        passive = passive.replace(passive_kiss_new, passive_kiss_simple, 1)
    elif passive_kiss_simple not in passive:
        raise SystemExit("partner wufu kiss conversion anchor not found")

    # 性器擦り合いは、男性器を持つ主人公には素股を実行して射精ゲージも加算する。
    # 貝合わせ(COM63)のままだと主人公側の快感・射精判定がなく、太ももでの愛撫の描写と食い違う。
    passive_rub_old = '''CASE 40\r
\t;貝あわせ\r
\tRETURNF 63\r
;顔面騎乗クンニ\r
'''
    passive_rub_new = '''CASE 40\r
\tIF PENIS(PLAYER)\r
\t\t;男性器がある場合は素股\r
\t\tRETURNF 33\r
\tELSE\r
\t\t;女性器同士なら貝あわせ\r
\t\tRETURNF 63\r
\tENDIF\r
;顔面騎乗クンニ\r
'''
    if passive_rub_old in passive:
        passive = passive.replace(passive_rub_old, passive_rub_new, 1)
    elif passive_rub_new not in passive:
        raise SystemExit("partner genital-rubbing conversion anchor not found")

    passive_message_old = ''';ぱふぱふ\r
@PASSIVE_MESSAGE_46\r
PRINTFORM %CALLNAME:TARGET%は%CALLNAME:PLAYER%の顔を両側から\r
IF TALENT:109\r
'''
    passive_message_new = ''';騎乗位\r
@PASSIVE_MESSAGE_47\r
PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の上に跨り、ゆっくりと腰を下ろしてきた…\r
\r
;ぱふぱふ\r
@PASSIVE_MESSAGE_46\r
PRINTFORM %CALLNAME:TARGET%は%CALLNAME:PLAYER%の顔を両側から\r
IF TALENT:109\r
'''
    passive_message_head = ''';騎乗位\r
@PASSIVE_MESSAGE_47\r
PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の上に跨り、ゆっくりと腰を下ろしてきた…\r
\r
'''
    # 初回生成時に同じアンカーを含むため、先に既存の挿入済みブロックを判定する。
    # 旧版で二重に入ったものもここで一つに正規化する。
    while passive_message_head + passive_message_head in passive:
        passive = passive.replace(passive_message_head + passive_message_head, passive_message_head, 1)
    if passive_message_new in passive:
        pass
    elif passive_message_old in passive:
        passive = passive.replace(passive_message_old, passive_message_new, 1)
    else:
        raise SystemExit("partner insertion message anchor not found")

    # 通常のパッシブ処理は、実COMの前に射精ゲージを予測分だけ減らす。
    # 追加パートナーターンでは直後に同じCOMを実行するため、この減算でゲージが
    # 負になると旧SAMEN_CHECKでは上限へ補正され、射精量倍率が異常に跳ね上がっていた。
    # TFLAG:543 は追加ターンの実行中だけ立つ印なので、その時だけ事前減算を省く。
    passive_drain_old = '''IF PENIS(PLAYER)\r
\tSELECTCASE ARG:1\r
'''
    passive_drain_new = '''IF PENIS(PLAYER) && TFLAG:543 == 0\r
\tSELECTCASE ARG:1\r
'''
    if passive_drain_old in passive:
        passive = passive.replace(passive_drain_old, passive_drain_new, 1)
    elif passive_drain_new not in passive:
        raise SystemExit("partner turn ejaculation-gauge anchor not found")
    write_cp932(PASSIVE, passive)

    event_message = read_cp932(EVENT_MESSAGE)
    old_hand_ejac_narration = '''\t\tSIF EXP:20 == 0\r
\t\t\tPRINT 驚きの表情をうかべる\r
\t\tSIF ABL:11 > 2\r
\t\t\tPRINT 恍惚の表情をうかべる\r
'''
    new_hand_ejac_narration = '''\t\tIF ABL:11 > 2\r
\t\t\tPRINTFORM %CALLNAME:TARGET%は恍惚の表情を浮かべ、\r
\t\tELSEIF EXP:20 == 0\r
\t\t\tPRINTFORM %CALLNAME:TARGET%は驚いた表情を浮かべ、\r
\t\tENDIF\r
'''
    if old_hand_ejac_narration in event_message:
        event_message = event_message.replace(old_hand_ejac_narration, new_hand_ejac_narration)
    elif new_hand_ejac_narration not in event_message:
        raise SystemExit("hand ejaculation narration anchor not found")
    custom_com413_dispatch_old = '''ELSEIF SELECTCOM == 413\r
\tCALL TRAIN_MESSAGE_A414\r
ELSEIF SELECTCOM == 414\r
\tCALL TRAIN_MESSAGE_A414\r
'''
    custom_com413_dispatch_new = '''ELSEIF SELECTCOM == 413\r
\tCALL TRAIN_MESSAGE_A413\r
ELSEIF SELECTCOM == 414\r
\tCALL TRAIN_MESSAGE_A414\r
'''
    if custom_com413_dispatch_old in event_message:
        event_message = event_message.replace(
            custom_com413_dispatch_old,
            custom_com413_dispatch_new,
            1,
        )
    elif custom_com413_dispatch_new not in event_message:
        raise SystemExit("custom COM413 message dispatch anchor not found")
    write_cp932(EVENT_MESSAGE, event_message)

    comable = read_cp932(COMABLE)
    custom_command_migration_old = ''';【旧セーブ救済】独自コマンド(COM280-284/410-414)の有効化データ補完\r
; ロード時(@EVENTLOAD)から呼ぶ。CSVにコマンド名(CSTR:80-89)が定義されている枠\r
; だけ CFLAG:69 の対応bitを立て、ランタイムのコマンド名が空なら補完する。\r
; ★素質(TALENT)・能力(ABL)・経験・珠など他のデータは一切変更しない。\r
; SETBITと空欄補完のみのため、何度呼ばれても安全（冪等）。\r
; COM280-284→bit0-4 / COM410-414→bit5-9（CSTR:80-89に対応）。\r
;------------------------------------------------------------\r
@DOKUJI_COM_MIGRATE\r
REPEAT CHARANUM\r
\tFOR LOCAL, 0, 10\r
\t\tLOCAL:1 = 80 + LOCAL\r
\t\tCSVCSTR NO:COUNT, LOCAL:1, 0\r
\t\tIF RESULTS != ""\r
\t\t\tSETBIT CFLAG:COUNT:69, LOCAL\r
\t\t\tSIF CSTR:COUNT:(LOCAL:1) == ""\r
\t\t\t\tCSTR:COUNT:(LOCAL:1) = %RESULTS%\r
\t\tENDIF\r
\tNEXT\r
REND\r
'''
    custom_command_migration_new = ''';【旧セーブ救済】独自コマンド(COM280-284/410-414)の有効化データ同期\r
; ロード時(@EVENTLOAD)から呼ぶ。CSVにコマンド名(CSTR:80-89)が定義されている枠\r
; だけ CFLAG:69 の対応bitを立て、保存済みの旧コマンド名も現在のCSV定義へ同期する。\r
; ★素質(TALENT)・能力(ABL)・経験・珠など他のデータは一切変更しない。\r
; SETBITとCSVからの再代入のみのため、何度呼ばれても安全（冪等）。\r
; COM280-284→bit0-4 / COM410-414→bit5-9（CSTR:80-89に対応）。\r
;------------------------------------------------------------\r
@DOKUJI_COM_MIGRATE\r
REPEAT CHARANUM\r
\tFOR LOCAL, 0, 10\r
\t\tLOCAL:1 = 80 + LOCAL\r
\t\tCSVCSTR NO:COUNT, LOCAL:1, 0\r
\t\tIF RESULTS != ""\r
\t\t\tSETBIT CFLAG:COUNT:69, LOCAL\r
\t\t\tCSTR:COUNT:(LOCAL:1) = %RESULTS%\r
\t\tENDIF\r
\tNEXT\r
REND\r
'''
    if custom_command_migration_old in comable:
        comable = comable.replace(
            custom_command_migration_old,
            custom_command_migration_new,
            1,
        )
    elif custom_command_migration_new not in comable:
        raise SystemExit("custom command save migration anchor not found")
    write_cp932(COMABLE, comable)

    event_text = read_cp932(EVENT_TEXT)
    cunnilingus_context_old = '''ELSEIF SELECTCOM == 1\r
\tA = UP:0\r
'''
    cunnilingus_context_extra = '''\t;パートナーターンでは、既に積み上がった経験・潤滑・欲情も地の文の段階へ反映する。\r
\t;行為中なのに初体験のような反応へ戻らないよう、低い一時値を現在の状態で補正する。\r
\tIF TFLAG:543\r
\t\tIF EXP:40 >= 100 || PALAM:3 >= PALAMLV:3 || PALAM:5 >= PALAMLV:3\r
\t\t\tSIF A < 3000\r
\t\t\t\tA = 3000\r
\t\tELSEIF EXP:40 >= 20 || PALAM:3 >= PALAMLV:2 || PALAM:5 >= PALAMLV:2\r
\t\t\tSIF A < 1000\r
\t\t\t\tA = 1000\r
\t\tENDIF\r
\tENDIF\r
'''
    cunnilingus_context_new = cunnilingus_context_old + cunnilingus_context_extra
    # 旧版は置換後にも旧アンカーが残るため、実行回数ぶん補正ブロックが重複していた。
    # 既存の重複を一つへ正規化してから、未挿入時だけ追加する。
    while cunnilingus_context_extra + cunnilingus_context_extra in event_text:
        event_text = event_text.replace(
            cunnilingus_context_extra + cunnilingus_context_extra,
            cunnilingus_context_extra,
            1,
        )
    if cunnilingus_context_new in event_text:
        pass
    elif cunnilingus_context_old in event_text:
        event_text = event_text.replace(cunnilingus_context_old, cunnilingus_context_new, 1)
    else:
        raise SystemExit("partner cunnilingus context anchor not found")
    write_cp932(EVENT_TEXT, event_text)

    info = migrate_endurance_option(read_cp932(INFO))
    old_endurance_ui = '''IF (FLAG:62 & 4096) || TFLAG:34\r
\tPRINTFORM 体力（%NAME:PLAYER%）\r
\tCALL PRINT_BAR_0, BASE:PLAYER:0, MAXBASE:PLAYER:0, 32\r
\tPRINTFORML ({BASE:PLAYER:0,4}/{MAXBASE:PLAYER:0,4})\r
ENDIF\r
'''
    new_endurance_ui = '''IF (FLAG:62 & 1p17) || TFLAG:34 || TFLAG:997\r
\tPRINTFORM 耐力（%NAME:PLAYER%）\r
\tCALL PRINT_BAR_0, BASE:PLAYER:4, MAXBASE:PLAYER:4, 32\r
\tPRINTFORML ({BASE:PLAYER:4,4}/{MAXBASE:PLAYER:4,4})\r
ENDIF\r
'''
    current_endurance_ui = '''IF (FLAG:62 & 1p17) || TFLAG:34 || TFLAG:997\r
\tPRINTFORM 体力（%NAME:PLAYER%）\r
\tCALL PRINT_BAR_0, BASE:PLAYER:0, MAXBASE:PLAYER:0, 32\r
\tPRINTFORML ({BASE:PLAYER:0,4}/{MAXBASE:PLAYER:0,4})\r
ENDIF\r
'''
    if old_endurance_ui in info:
        info = info.replace(old_endurance_ui, new_endurance_ui, 1)
    elif current_endurance_ui in info:
        info = info.replace(current_endurance_ui, new_endurance_ui, 1)
    elif new_endurance_ui not in info:
        raise SystemExit("endurance status display anchor not found")
    write_cp932(INFO, info)

    config_ex = read_cp932(CONFIG_EX)
    old_description = '''TSTR:204 = パートナーのターンを追加しました。コマンド選択前にパートナーの行動が追加されます\r
'''
    coupled_description = '''TSTR:204 = パートナーのターンを追加しました。主人公の射精時に耐力を消費します\r
'''
    new_description = '''TSTR:204 = パートナーのターンを追加しました\r
'''
    if old_description in config_ex:
        config_ex = config_ex.replace(old_description, new_description, 1)
    elif coupled_description in config_ex:
        config_ex = config_ex.replace(coupled_description, new_description, 1)
    elif new_description not in config_ex:
        raise SystemExit("partner turn config description anchor not found")
    endurance_config_rows = {
        "TSTR:17 = ": "TSTR:17 = 射精時の耐力消費",
        "TSTR:117 = ": "TSTR:117 = 射精時に耐力を消費しないように設定しました",
        "TSTR:217 = ": "TSTR:217 = 射精時に耐力を消費するように設定しました",
    }
    event_config_start = config_ex.index("@SET_CONFIGURE_TSTR_62")
    next_config_start = config_ex.find("@SET_CONFIGURE_TSTR_", event_config_start + 1)
    if next_config_start < 0:
        next_config_start = len(config_ex)
    config_prefix = config_ex[:event_config_start]
    config_section = config_ex[event_config_start:next_config_start]
    config_suffix = config_ex[next_config_start:]
    # 旧スクリプトが他の設定グループの同じ行番号を触った場合も、ここで空欄へ戻す。
    for old_row, new_row in endurance_config_rows.items():
        config_prefix = config_prefix.replace(new_row + "\r\n", old_row + "\r\n")
        if old_row + "\r\n" in config_section:
            config_section = config_section.replace(old_row + "\r\n", new_row + "\r\n", 1)
        elif new_row not in config_section:
            raise SystemExit(f"endurance config row not found: {old_row}")
    config_ex = config_prefix + config_section + config_suffix
    write_cp932(CONFIG_EX, config_ex)

    # 主人公自身の射精経験も最大耐力の成長に反映する。
    cflag_csv = read_cp932(CFLAG_CSV)
    cflag_rows = '''1150,主人公射精回数（耐力成長）\r
1151,主人公射精量（耐力成長）\r
1152,耐力枯渇成長ポイント\r
1153,女性耐力枯渇成長ポイント\r
1154,ドライ絶頂成長ポイント\r
1155,耐力成長ポイント移行済み\r
'''
    if "1150,主人公射精回数（耐力成長）" not in cflag_csv:
        cflag_csv = cflag_csv.rstrip("\r\n") + "\r\n" + cflag_rows
    else:
        cflag_csv = cflag_csv.replace("1152,耐力枯渇回数（耐力成長）", "1152,耐力枯渇成長ポイント")
        cflag_csv = cflag_csv.replace("1153,女性耐力枯渇回数（耐力成長）", "1153,女性耐力枯渇成長ポイント")
        cflag_csv = cflag_csv.replace("1154,ドライ絶頂回数（耐力成長）", "1154,ドライ絶頂成長ポイント")
        if "1155,耐力成長ポイント移行済み" not in cflag_csv:
            cflag_csv = cflag_csv.rstrip("\r\n") + "\r\n1155,耐力成長ポイント移行済み\r\n"
    write_cp932(CFLAG_CSV, cflag_csv)

    system = read_cp932(SYSTEM)
    forced_partner_end_start = "IF BASE:0 <= 0 && TALENT:128\r\n"
    forced_partner_end_next = "ELSEIF TFLAG:44 == 0 && BASE:1 <= 300 && CFLAG:27\r\n"
    forced_partner_end = '''IF BASE:0 <= 0 && TALENT:128
	PRINTW ＜リザレクション＞
	EXP:50 += 3
	PRINTL 異常経験＋３
	BASE:0 = 1
	;体力0での強制終了。廃止済みの感情マークは付与せず、事後行為と追加パートナーターンを止める。
	TFLAG:301 = 1
	TFLAG:999 = 1
	PRINTFORMW （体力が限界に来ています。%CALLNAME:MASTER%は%CALLNAME:TARGET%にゆっくり休むよう伝えてから、一旦別れました）
	BEGIN AFTERTRAIN
ELSEIF BASE:0 <= 0
	BASE:0 = 1
	;体力0での強制終了。廃止済みの感情マークは付与せず、事後行為と追加パートナーターンを止める。
	TFLAG:301 = 1
	TFLAG:999 = 1
	PRINTFORMW （%CALLNAME:TARGET%は疲れ果てて気絶してしまった。%CALLNAME:MASTER%は%CALLNAME:TARGET%を寝床まで運び、一旦別れました）
	IF ABL:0 > 0 && TALENT:153 == 0
		ABL:0 -= 1
		PRINTFORML %CALLNAME:TARGET%の親密が１下がった
	ENDIF
	BEGIN AFTERTRAIN
'''
    forced_partner_end = forced_partner_end.replace("\n", "\r\n")
    forced_partner_end_pos = system.find(forced_partner_end_start)
    forced_partner_end_next_pos = system.find(forced_partner_end_next, forced_partner_end_pos)
    if forced_partner_end_pos < 0 or forced_partner_end_next_pos < 0:
        raise SystemExit("partner health forced-end anchors not found")
    system = (
        system[:forced_partner_end_pos]
        + forced_partner_end
        + system[forced_partner_end_next_pos:]
    )
    partner_turn_end_old = '''ELSEIF TFLAG:44 == 0 && BASE:1 <= 0\r
	;襲われ判定\r
'''
    partner_turn_end_new = '''ELSEIF TFLAG:44 == 0 && BASE:1 <= 0\r
	;このコマンドで時間終了が確定したため、#LATERのパートナーターンを抑止する。\r
	TFLAG:999 = 1\r
	;襲われ判定\r
'''
    if partner_turn_end_old in system:
        system = system.replace(partner_turn_end_old, partner_turn_end_new, 1)
    elif partner_turn_end_new not in system:
        raise SystemExit("partner turn end-of-session anchor not found")
    split_migration_anchor = ''';実績システムはFLAG(セーブ固有)へ全面移行済み（旧GLOBAL:199-899の互換移行処理は不要になったため削除）\r
'''
    split_migration = ''';パートナーのターン追加と、射精時の耐力消費を別設定へ分離する。
;既存セーブでは、従来のパートナーターン設定がONなら耐力消費も一度だけ引き継ぐ。
IF FLAG:63 == 20
	SIF FLAG:62 & 16
		FLAG:62 |= 1p17
	FLAG:63 = 21
ENDIF

;実績システムはFLAG(セーブ固有)へ全面移行済み（旧GLOBAL:199-899の互換移行処理は不要になったため削除）
'''
    split_migration = split_migration.replace("\n", "\r\n")
    # 一度追加済みならそのまま。旧版の補助スクリプトで重複していても一つに正規化する。
    migration_marker = ";パートナーのターン追加と、射精時の耐力消費を別設定へ分離する。\r\n"
    first_migration = system.find(migration_marker)
    while first_migration >= 0:
        duplicate_migration = system.find(migration_marker, first_migration + len(migration_marker))
        if duplicate_migration < 0:
            break
        next_migration = system.find(migration_marker, duplicate_migration + len(migration_marker))
        if next_migration < 0:
            next_migration = system.find(split_migration_anchor, duplicate_migration)
        if next_migration < 0:
            raise SystemExit("duplicate option migration end anchor not found")
        system = system[:duplicate_migration] + system[next_migration:]
    if migration_marker in system:
        pass
    elif split_migration_anchor in system:
        system = system.replace(split_migration_anchor, split_migration, 1)
    else:
        raise SystemExit("partner/endurance option migration anchor not found")
    initial_master_endurance = '''\t\tMAXBASE:COUNT:4 = MAXBASE:COUNT:0 * (100 + CFLAG:COUNT:2) / 100\r
'''
    initial_master_endurance_new = '''\t\tMAXBASE:COUNT:4 = MAXBASE:COUNT:0 * (100 + MASTER_ENDURANCE_GROWTH()) / 100\r
'''
    if initial_master_endurance in system:
        system = system.replace(initial_master_endurance, initial_master_endurance_new, 1)
    elif initial_master_endurance_new not in system:
        raise SystemExit("initial master endurance anchor not found")

    growth_comment_old = '\t\t;主人公限定で、パートナーを絶頂させた回数で最大耐力増加\r\n'
    growth_comment_new = '\t\t;主人公限定で、相手と主人公自身の絶頂経験で最大耐力増加\r\n'
    if growth_comment_old in system:
        growth_start = system.index(growth_comment_old)
    elif growth_comment_new in system:
        growth_start = system.index(growth_comment_new)
    else:
        raise SystemExit("master endurance growth comment anchor not found")
    female_branch_old = '\tELSE\r\n\t\t;耐力＝体力を基準値として、絶頂経験で増加'
    female_branch_new = '\tELSE\r\n\t\t;耐力＝体力を基準値として、絶頂経験と耐力枯渇経験で増加'
    if female_branch_old in system:
        growth_end = system.index(female_branch_old, growth_start)
    elif female_branch_new in system:
        growth_end = system.index(female_branch_new, growth_start)
    else:
        raise SystemExit("female endurance branch anchor not found")
    growth_block = system[growth_start:growth_end]
    if "CFLAG:COUNT:2" in growth_block:
        growth_block = growth_block.replace("CFLAG:COUNT:2", "MASTER_ENDURANCE_GROWTH()")
        growth_block = growth_block.replace(
            "主人公限定で、パートナーを絶頂させた回数で最大耐力増加",
            "主人公限定で、相手と主人公自身の絶頂経験で最大耐力増加",
        )
        system = system[:growth_start] + growth_block + system[growth_end:]
    elif "MASTER_ENDURANCE_GROWTH()" not in growth_block:
        raise SystemExit("master endurance growth anchor not found")

    initial_female_endurance = '''\t\tMAXBASE:COUNT:4 = MAXBASE:COUNT:0 * (100 + EXP:COUNT:2) / 100\r
'''
    initial_female_endurance_new = '''\t\tMAXBASE:COUNT:4 = MAXBASE:COUNT:0 * (100 + FEMALE_ENDURANCE_GROWTH(COUNT)) / 100\r
'''
    if initial_female_endurance in system:
        system = system.replace(initial_female_endurance, initial_female_endurance_new, 1)
    elif initial_female_endurance_new not in system:
        raise SystemExit("initial female endurance anchor not found")

    female_comment_old = '\t\t;耐力＝体力を基準値として、絶頂経験で増加\r\n'
    female_comment_new = '\t\t;耐力＝体力を基準値として、絶頂経験と耐力枯渇経験で増加\r\n'
    if female_comment_old in system:
        female_growth_start = system.index(female_comment_old)
    elif female_comment_new in system:
        female_growth_start = system.index(female_comment_new)
    else:
        raise SystemExit("female endurance growth comment anchor not found")
    female_growth_end = system.index('\tENDIF\r\n\r\n\tIF COUNT == MASTER', female_growth_start)
    female_growth_block = system[female_growth_start:female_growth_end]
    if "EXP:COUNT:2" in female_growth_block:
        female_growth_block = female_growth_block.replace("EXP:COUNT:2", "FEMALE_ENDURANCE_GROWTH(COUNT)")
        female_growth_block = female_growth_block.replace(
            "耐力＝体力を基準値として、絶頂経験で増加",
            "耐力＝体力を基準値として、絶頂経験と耐力枯渇経験で増加",
        )
        system = system[:female_growth_start] + female_growth_block + system[female_growth_end:]
    elif "FEMALE_ENDURANCE_GROWTH(COUNT)" not in female_growth_block:
        raise SystemExit("female endurance growth anchor not found")

    endurance_recovery_old = '''\tIF COUNT == MASTER\r
\t\t;主人公: 昼10%、夜20%\r
\t\tIF TIME == 0\r
\t\t\tA = MAXBASE:COUNT:0 / 10\r
\t\t\tB = 0\r
\t\tELSE\r
\t\t\tA = MAXBASE:COUNT:0 / 5\r
\t\t\tB = 0\r
\t\tENDIF\r
\tELSE\r
'''
    endurance_recovery_new = '''\tIF COUNT == MASTER\r
\t\t;主人公: 体力は昼10%、夜20%。耐力は昼夜切替20%、日付切替50%。\r
\t\tIF TIME == 0\r
\t\t\tA = MAXBASE:COUNT:0 / 10\r
\t\t\t;TIME==0は新しい日が始まる側。\r
\t\t\tB = MAXBASE:COUNT:4 / 2\r
\t\tELSE\r
\t\t\tA = MAXBASE:COUNT:0 / 5\r
\t\t\tB = MAXBASE:COUNT:4 / 5\r
\t\tENDIF\r
\tELSE\r
'''
    if endurance_recovery_old in system:
        system = system.replace(endurance_recovery_old, endurance_recovery_new, 1)
    elif endurance_recovery_new not in system:
        raise SystemExit("master endurance recovery anchor not found")
    write_cp932(SYSTEM, system)

    self_command = read_cp932(SELF_COMMAND)
    self_check_anchor = "@SELF_CHECK\r\n"
    self_check_guard = '''@SELF_CHECK
;体力0による強制終了時だけ、調教後行為をすべてスキップする。
SIF TFLAG:301
	RETURN 0
'''
    self_check_guard = self_check_guard.replace("\n", "\r\n")
    if self_check_guard not in self_command:
        if self_check_anchor not in self_command:
            raise SystemExit("SELF_CHECK anchor not found")
        self_command = self_command.replace(self_check_anchor, self_check_guard, 1)

    after_v_old = ''';体力余って、[恋慕]がないとダメ\r
SIF BASE:0 < 500 || TALENT:TARGET:85 == 0 || TFLAG:301\r
	RETURN 0\r
'''
    after_v_new = ''';[恋慕]がない場合、または体力0による強制終了時は実行しない。\r
SIF TALENT:TARGET:85 == 0 || TFLAG:301\r
	RETURN 0\r
'''
    if after_v_old in self_command:
        self_command = self_command.replace(after_v_old, after_v_new, 1)
    elif after_v_new not in self_command:
        raise SystemExit("AFTER_V_CHECK health anchor not found")

    after_s_health_limit = ''';体力が500未満だと半分になる\r
IF BASE:0 <= 500\r
	A /= 2\r
	;Aが6回以上だったら5回以下にする\r
	SIF A > 6\r
		A %= 6\r
	;Aが0だった場合1にする\r
	SIF A < 1\r
		A = 1\r
ENDIF\r
\r
'''
    if after_s_health_limit in self_command:
        self_command = self_command.replace(after_s_health_limit, "", 1)
    elif "BASE:0 <= 500" in self_command:
        raise SystemExit("AFTER_S_CHECK health limit format changed")

    after_l_old = ''';体力必要\r
SIF BASE:0 < 500 || TFLAG:301\r
	RETURN 0\r
'''
    after_l_new = ''';体力0による強制終了時は実行しない。\r
SIF TFLAG:301\r
	RETURN 0\r
'''
    if after_l_old in self_command:
        self_command = self_command.replace(after_l_old, after_l_new, 1)
    elif after_l_new not in self_command:
        raise SystemExit("AFTER_L_CHECK health anchor not found")

    after_minor_health_limit = ''';体力余っていないとダメ\r
SIF BASE:0 < 300\r
	RETURN 0\r
'''
    minor_health_limit_count = self_command.count(after_minor_health_limit)
    if minor_health_limit_count:
        if minor_health_limit_count != 2:
            raise SystemExit("unexpected AFTER_KISS/SERVICE health limit count")
        self_command = self_command.replace(after_minor_health_limit, "")
    elif "BASE:0 < 300" in self_command:
        raise SystemExit("AFTER_KISS/SERVICE health limit format changed")

    self_check2_old = ''';恋慕で体力が500以上有って夜じゃなきゃダメ\r
SIF TALENT:TARGET:85 == 0 || BASE:0 < 500 || TIME == 0\r
	RETURN 0\r
'''
    self_check2_new = ''';恋慕持ちで夜でなければ実行しない。体力による制限は設けない。\r
SIF TALENT:TARGET:85 == 0 || TIME == 0\r
	RETURN 0\r
'''
    if self_check2_old in self_command:
        self_command = self_command.replace(self_check2_old, self_check2_new, 1)
    elif self_check2_new not in self_command:
        raise SystemExit("SELF_CHECK2 health anchor not found")
    write_cp932(SELF_COMMAND, self_command)

    revmode_active_command = read_cp932(REVMODE_ACTIVE_COMMAND)
    revmode_health_end_old = ''';ウフフ中\r
IF TFLAG:44 && BASE:0 < 500\r
	PRINTFORMW （体力が限界に来ています。%CALLNAME:MASTER%は%CALLNAME:TARGET%にゆっくり休むよう伝えてから、一旦別れました）\r
	BEGIN AFTERTRAIN\r
;非ウフフ中\r
'''
    revmode_health_end_new = ''';ウフフ中。パートナーの体力が0になったときだけ強制終了する。\r
IF TFLAG:44 && BASE:0 <= 0\r
	BASE:0 = 1\r
	TFLAG:301 = 1\r
	TFLAG:999 = 1\r
	PRINTFORMW （体力が限界に来ています。%CALLNAME:MASTER%は%CALLNAME:TARGET%にゆっくり休むよう伝えてから、一旦別れました）\r
	BEGIN AFTERTRAIN\r
;非ウフフ中\r
'''
    if revmode_health_end_old in revmode_active_command:
        revmode_active_command = revmode_active_command.replace(
            revmode_health_end_old,
            revmode_health_end_new,
            1,
        )
    elif revmode_health_end_new not in revmode_active_command:
        raise SystemExit("REVMODE active health forced-end anchor not found")
    write_cp932(REVMODE_ACTIVE_COMMAND, revmode_active_command)

    # 調教を開始する時点で、前回の調教終了時に立てた抑止フラグを解除する。
    event_train = read_cp932(EVENT_TRAIN)
    event_train_anchor = '''@EVENTTRAIN\r
#PRI\r
'''
    event_train_insert = '''@EVENTTRAIN\r
#PRI\r
;前回の調教終了時に立てた、強制終了・追加パートナーターン抑止フラグを戻す。\r
TFLAG:999 = 0\r
TFLAG:301 = 0\r
'''
    event_train_reset_old = ''';前回の調教終了時に立てた、追加パートナーターン抑止フラグを戻す。\r
TFLAG:999 = 0\r
'''
    event_train_reset = ''';前回の調教終了時に立てた、強制終了・追加パートナーターン抑止フラグを戻す。\r
TFLAG:999 = 0\r
TFLAG:301 = 0\r
'''
    if event_train_reset_old in event_train:
        event_train = event_train.replace(event_train_reset_old, event_train_reset, 1)
    first_event_train_insert = event_train.find(event_train_reset)
    while first_event_train_insert >= 0:
        duplicate_event_train_insert = event_train.find(event_train_reset, first_event_train_insert + len(event_train_reset))
        if duplicate_event_train_insert < 0:
            break
        event_train = event_train[:duplicate_event_train_insert] + event_train[duplicate_event_train_insert + len(event_train_reset):]
    if event_train_reset in event_train:
        pass
    elif event_train_anchor in event_train:
        event_train = event_train.replace(event_train_anchor, event_train_insert, 1)
    else:
        raise SystemExit("EVENTTRAIN partner turn reset anchor not found")
    write_cp932(EVENT_TRAIN, event_train)

    shoot = migrate_endurance_option(read_cp932(SHOOT))
    dry_orgasm_anchor = '''TFLAG:719 = A - B + RAND:C\r
SIF TFLAG:719 < 1\r
\tTFLAG:719 = 1\r
\r
'''
    dry_orgasm_insert = '''TFLAG:719 = A - B + RAND:C\r
SIF TFLAG:719 < 1\r
\tTFLAG:719 = 1\r
\r
;パートナーのターン追加中に耐力が尽きたら、精を出さないドライ絶頂へ切り替える。\r
TFLAG:995 = 0\r
IF ((FLAG:62 & 1p17) || TFLAG:997) && BASE:MASTER:4 <= 0 && TFLAG:302\r
\tTFLAG:995 = 1\r
\tE = 0\r
\tTFLAG:302 = 0\r
\tTFLAG:714 = 0\r
\tSIF EJAC > 0\r
\t\tBASE:PLAYER:2 = EJAC - 1\r
\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML もう何も出せないのに、%CALLNAME:TARGET%の責めに%CALLNAME:MASTER%の身体だけが震えている……\r
\tCASE 1\r
\t\tPRINTFORML 空になったはずの奥をなお弄ばれ、%CALLNAME:MASTER%は声もなく絶頂だけを繰り返した……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は容赦なく快感を重ね、%CALLNAME:MASTER%から残り香まで搾り取っていく……\r
\tCASEELSE\r
\t\tPRINTFORML これ以上は出せない。それでも続く刺激に、%CALLNAME:MASTER%は力なく身体を跳ねさせた……\r
\tENDSELECT\r
\tRETURN 0\r
ENDIF\r
\r
'''
    legacy_dry_orgasm_line = '''\tPRINTFORML %CALLNAME:MASTER%は達しても、耐力が尽きていて精を出せない……（ドライ絶頂）\r
'''
    dry_orgasm_narration = '''\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML もう何も出せないのに、%CALLNAME:TARGET%の責めに%CALLNAME:MASTER%の身体だけが震えている……\r
\tCASE 1\r
\t\tPRINTFORML 空になったはずの奥をなお弄ばれ、%CALLNAME:MASTER%は声もなく絶頂だけを繰り返した……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は容赦なく快感を重ね、%CALLNAME:MASTER%から残り香まで搾り取っていく……\r
\tCASEELSE\r
\t\tPRINTFORML これ以上は出せない。それでも続く刺激に、%CALLNAME:MASTER%は力なく身体を跳ねさせた……\r
\tENDSELECT\r
'''
    if dry_orgasm_insert in shoot:
        pass
    elif legacy_dry_orgasm_line in shoot:
        pass
    elif dry_orgasm_anchor in shoot:
        pass
    else:
        raise SystemExit("dry orgasm anchor not found")
    if legacy_dry_orgasm_line in shoot:
        shoot = shoot.replace(legacy_dry_orgasm_line, dry_orgasm_narration, 1)
    # 旧版の補助スクリプトを複数回走らせた環境で、同じドライ絶頂ブロックが
    # 残っていても一つに正規化する。
    dry_orgasm_block = dry_orgasm_insert[len(dry_orgasm_anchor):]
    first_dry_orgasm = shoot.find(dry_orgasm_block)
    while first_dry_orgasm >= 0:
        duplicate_dry_orgasm = shoot.find(dry_orgasm_block, first_dry_orgasm + len(dry_orgasm_block))
        if duplicate_dry_orgasm < 0:
            break
        shoot = shoot[:duplicate_dry_orgasm] + shoot[duplicate_dry_orgasm + len(dry_orgasm_block):]
    # 射精者を確定できないSAMEN_CHECK側の旧ドライ絶頂処理は削除する。
    # 射精者を判定したSAMEN_SHOOT側で処理するため、助手操作でも消費先を誤らない。
    old_dry_start = shoot.find(";パートナーのターン追加中に耐力が尽きたら、精を出さないドライ絶頂へ切り替える。\r\n")
    if old_dry_start >= 0:
        old_dry_end = shoot.find(";---------------------------------------------------------\r\n;射精場所選択", old_dry_start)
        if old_dry_end < 0:
            raise SystemExit("legacy dry orgasm end anchor not found")
        shoot = shoot[:old_dry_start] + shoot[old_dry_end:]

    ejaculation_growth_anchor = '''IF P == PLAYER || P == MASTER\r
\tFLAG:5040 += TFLAG:719\r
\tFLAG:(5800 + NO:T) += TFLAG:719\r
ENDIF\r
'''
    ejaculation_growth_insert = '''IF P == PLAYER || P == MASTER\r
\tFLAG:5040 += TFLAG:719\r
\tFLAG:(5800 + NO:T) += TFLAG:719\r
\t;パートナーのターン追加中の主人公射精は、回数と実射精量で最大耐力を鍛える。\r
\tSIF TFLAG:994 && TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1150 += 1\r
\tSIF TFLAG:994 && TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1151 += TFLAG:719\r
ENDIF\r
'''
    legacy_ejaculation_growth = '''\tSIF TFLAG:994\r
\t\tCFLAG:MASTER:1150 += 1\r
\tSIF TFLAG:994\r
\t\tCFLAG:MASTER:1151 += TFLAG:719\r
'''
    current_ejaculation_growth = '''\tSIF TFLAG:994 && TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1150 += 1\r
\tSIF TFLAG:994 && TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1151 += TFLAG:719\r
'''
    if legacy_ejaculation_growth in shoot:
        shoot = shoot.replace(legacy_ejaculation_growth, current_ejaculation_growth, 1)
    elif ejaculation_growth_insert in shoot:
        pass
    elif ejaculation_growth_anchor in shoot:
        shoot = shoot.replace(ejaculation_growth_anchor, ejaculation_growth_insert, 1)
    else:
        raise SystemExit("ejaculation growth anchor not found")
    write_cp932(SHOOT, shoot)

    counter = migrate_endurance_option(read_cp932(COUNTER))
    damage_vars = '''#DIM DYNAMIC DAMAGE, 1\r
#DIM DYNAMIC STRENGTH, 1\r
#DIM DYNAMIC ORGASM_COUNT, 1\r
'''
    damage_vars_new = '''#DIM DYNAMIC DAMAGE, 1\r
#DIM DYNAMIC STRENGTH, 1\r
#DIM DYNAMIC ORGASM_COUNT, 1\r
#DIM DYNAMIC BEFORE_ENDURANCE, 1\r
'''
    if damage_vars_new in counter:
        pass
    elif damage_vars in counter:
        counter = counter.replace(damage_vars, damage_vars_new, 1)
    else:
        raise SystemExit("endurance damage variables anchor not found")
    while counter.count("#DIM DYNAMIC BEFORE_ENDURANCE, 1\r\n") > 1:
        counter = counter.replace("#DIM DYNAMIC BEFORE_ENDURANCE, 1\r\n", "", 1)
    damage_apply = '''PRINTFORML %CALLNAME:MASTER%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
BASE:MASTER:4 -= DAMAGE\r
SIF BASE:MASTER:4 < 0\r
\tBASE:MASTER:4 = 0\r
TFLAG:994 = 0\r
'''
    damage_apply_new = '''PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
BEFORE_ENDURANCE = BASE:(TFLAG:996):4\r
BASE:(TFLAG:996):4 -= DAMAGE\r
SIF BASE:(TFLAG:996):4 < 0\r
\tBASE:(TFLAG:996):4 = 0\r
IF BEFORE_ENDURANCE > 0 && BASE:(TFLAG:996):4 == 0\r
\t;限界まで絞り出された経験は、通常の射精経験より大きく耐力上限を鍛える。\r
\tIF TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1152 += 80 + RAND(41)\r
\tELSE\r
\t\t;絶頂経験とは分けて、耐力枯渇回数だけを別カウンタへ記録する。\r
\t\tCFLAG:(TFLAG:996):1153 += 80 + RAND(41)\r
\tENDIF\r
\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML %CALLNAME:TARGET%に何度も搾り立てられ、%CALLNAME:(TFLAG:996)%は最後の一滴まで空にされた……\r
\tCASE 1\r
\t\tPRINTFORML 容赦なく快感を重ねられ、%CALLNAME:(TFLAG:996)%の身体はもう何も残せず震えている……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は限界を悟ってなお手を緩めず、%CALLNAME:(TFLAG:996)%を力尽きるまで弄び抜いた……\r
\tCASEELSE\r
\t\tPRINTFORML 絞り出されたあとの鈍い余韻に、%CALLNAME:(TFLAG:996)%はぐったりと身を委ねた……\r
\tENDSELECT\r
ENDIF\r
TFLAG:994 = 0\r
'''
    legacy_exhaustion_narration = '''\tPRINTFORML %CALLNAME:MASTER%は耐力を使い果たした……限界を越えた経験が刻まれる\r
'''
    exhaustion_narration = '''\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML %CALLNAME:TARGET%に何度も搾り立てられ、%CALLNAME:(TFLAG:996)%は最後の一滴まで空にされた……\r
\tCASE 1\r
\t\tPRINTFORML 容赦なく快感を重ねられ、%CALLNAME:(TFLAG:996)%の身体はもう何も残せず震えている……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は限界を悟ってなお手を緩めず、%CALLNAME:(TFLAG:996)%を力尽きるまで弄び抜いた……\r
\tCASEELSE\r
\t\tPRINTFORML 絞り出されたあとの鈍い余韻に、%CALLNAME:(TFLAG:996)%はぐったりと身を委ねた……\r
\tENDSELECT\r
'''
    if damage_apply_new in counter:
        pass
    elif legacy_exhaustion_narration in counter:
        pass
    elif "IF BEFORE_ENDURANCE > 0 && BASE:MASTER:4 == 0" in counter:
        pass
    elif "IF BEFORE_ENDURANCE > 0 && BASE:(TFLAG:996):4 == 0" in counter:
        pass
    elif damage_apply in counter:
        counter = counter.replace(damage_apply, damage_apply_new, 1)
    else:
        raise SystemExit("endurance damage application anchor not found")
    if legacy_exhaustion_narration in counter:
        counter = counter.replace(legacy_exhaustion_narration, exhaustion_narration, 1)
    legacy_exhaustion_random = '''\tSELECTCASE RAND(4)\r
\tCASE 0\r
\t\tPRINTFORML %CALLNAME:TARGET%に何度も搾り立てられ、%CALLNAME:MASTER%は最後の一滴まで空にされた……\r
\tCASE 1\r
\t\tPRINTFORML 容赦なく快感を重ねられ、%CALLNAME:MASTER%の身体はもう何も残せず震えている……\r
\tCASE 2\r
\t\tPRINTFORML %CALLNAME:TARGET%は限界を悟ってなお手を緩めず、%CALLNAME:MASTER%を力尽きるまで弄び抜いた……\r
\tCASEELSE\r
\t\tPRINTFORML 絞り出されたあとの鈍い余韻に、%CALLNAME:MASTER%はぐったりと身を委ねた……\r
\tENDSELECT\r
'''
    if legacy_exhaustion_random in counter:
        counter = counter.replace(legacy_exhaustion_random, exhaustion_narration, 1)
    # 既存セーブ向けの旧「主人公固定」耐力消費を、射精者本人へ移行する。
    legacy_actor_damage = '''PRINTFORML %CALLNAME:MASTER%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
BEFORE_ENDURANCE = BASE:MASTER:4\r
BASE:MASTER:4 -= DAMAGE\r
SIF BASE:MASTER:4 < 0\r
\tBASE:MASTER:4 = 0\r
IF BEFORE_ENDURANCE > 0 && BASE:MASTER:4 == 0\r
\t;限界まで絞り出された経験は、通常の射精経験より大きく耐力上限を鍛える。\r
\tCFLAG:MASTER:1152 += 80 + RAND(41)\r
'''
    current_actor_damage = '''PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r
BEFORE_ENDURANCE = BASE:(TFLAG:996):4\r
BASE:(TFLAG:996):4 -= DAMAGE\r
SIF BASE:(TFLAG:996):4 < 0\r
\tBASE:(TFLAG:996):4 = 0\r
IF BEFORE_ENDURANCE > 0 && BASE:(TFLAG:996):4 == 0\r
\t;限界まで絞り出された経験は、通常の射精経験より大きく耐力上限を鍛える。\r
\tIF TFLAG:996 == MASTER\r
\t\tCFLAG:MASTER:1152 += 80 + RAND(41)\r
\tELSE\r
\t\t;絶頂経験とは分けて、耐力枯渇回数だけを別カウンタへ記録する。\r
\t\tCFLAG:(TFLAG:996):1153 += 80 + RAND(41)\r
\tENDIF\r
'''
    current_actor_damage_with_load = current_actor_damage.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（射精量×{TFLAG:714}、負荷倍率×{SQRT(TFLAG:714)}、絶頂強度{STRENGTH}）",
        1,
    )
    current_actor_damage_clean = current_actor_damage.replace(
        "（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）",
        "（絶頂強度{STRENGTH}）",
        1,
    )
    if legacy_actor_damage in counter:
        counter = counter.replace(legacy_actor_damage, current_actor_damage, 1)
    elif (
        current_actor_damage not in counter
        and current_actor_damage_with_load not in counter
        and current_actor_damage_clean not in counter
    ):
        raise SystemExit("endurance actor migration anchor not found")
    damage_display = "PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（絶頂強度{STRENGTH}）\r\n"
    damage_display_with_multiplier = "PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、絶頂強度{STRENGTH}）\r\n"
    damage_display_with_load = "PRINTFORML %CALLNAME:(TFLAG:996)%の耐力-{DAMAGE}（射精量×{TFLAG:714}、負荷倍率×{SQRT(TFLAG:714)}、絶頂強度{STRENGTH}）\r\n"
    if damage_display_with_load in counter:
        counter = counter.replace(damage_display_with_load, damage_display, 1)
    elif damage_display_with_multiplier in counter:
        counter = counter.replace(damage_display_with_multiplier, damage_display, 1)
    elif damage_display not in counter:
        raise SystemExit("endurance damage display anchor not found")
    write_cp932(COUNTER, counter)

    # 待機中動作の性行為は対象に精液経験を与えるため、主人公側にも射精経験を記録する。
    shop_com_act = read_cp932(SHOP_COM_ACT)
    standby_sex_old = '''\t\tCFLAG:MASTER:2 += S\r
\t\tCFLAG:COUNT:2 += S*5\r
'''
    standby_sex_new = '''\t\tCFLAG:MASTER:2 += S\r
\t\t;待機中の性行為も射精を伴う扱いにする。主人公の射精経験を取りこぼさない。\r
\t\tEXP:MASTER:3 += S\r
\t\tCALL TURNEND_COM_PRINT, "EXP", 3, S\r
\t\tCFLAG:COUNT:2 += S*5\r
'''
    if standby_sex_old in shop_com_act:
        shop_com_act = shop_com_act.replace(standby_sex_old, standby_sex_new, 1)
    elif standby_sex_new not in shop_com_act:
        raise SystemExit("standby sex ejaculation experience anchor not found")
    write_cp932(SHOP_COM_ACT, shop_com_act)

    write_cp932(ENDURANCE_GROWTH, ENDURANCE_GROWTH_SOURCE.lstrip())

    write_cp932(AUTO, AUTO_SOURCE.lstrip())
    write_cp932(PARTNER_TURN, PARTNER_TURN_SOURCE.lstrip())
    print(f"updated {USERCOM}")
    print(f"created {AUTO}")
    print(f"created {PARTNER_TURN}")


if __name__ == "__main__":
    main()
