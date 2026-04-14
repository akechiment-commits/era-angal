# Emuera ERB 構文リファレンス（eraあんガル用）

実際のコード（ERB/内のファイル）から抽出した構文まとめ。

---

## 1. ファイル基本

- 文字コード: **Shift-JIS (cp932)**
- 拡張子: `.ERB`
- 1行1命令（複数命令を1行に書けない）
- コメント: `;` で始まる行、または行末の `;` 以降

```erb
;これはコメント
PRINTL テスト  ;行末コメントも可
```

---

## 2. 関数定義

```erb
@関数名
; 引数なし

@関数名, ARG, ARG:1
; カンマ区切りで引数（ARG:0=ARG, ARG:1...と対応）

@関数名(ARG, ARG:1)
; 括弧記法でも同じ。式中関数の場合はこちらを使うことが多い

@関数名, ARG, ARG:1 = 0
; デフォルト引数（省略時は0）

@関数名, ARGS, ARGS:1 = "/"
; 文字列引数（ARGS, ARGS:1...）。デフォルト値も使える
```

### 関数の種類

| ディレクティブ | 意味 |
|--------------|------|
| `#PRI` | イベント関数として優先して呼ばれる |
| `#LATER` | イベント関数として後から呼ばれる |
| `#FUNCTION` | 式中関数（整数を返す）。`RETURNF 値` で返す |
| `#FUNCTIONS` | 式中関数（文字列を返す）。`RETURNF "値"` で返す |
| `#SINGLE` | 同名関数が複数あっても1つだけ実行 |
| `#LOCALSIZE n` | LOCAL配列のサイズをn個に拡張 |
| `#LOCALSSIZE n` | LOCALS配列のサイズをn個に拡張 |
| `#DIM 変数名[, サイズ]` | 関数内ローカル変数を宣言 |
| `#DIMS 変数名[, サイズ]` | 関数内ローカル文字列変数を宣言 |

例:
```erb
@BARCOLORSET, ARGS
#FUNCTION
SELECTCASE ARGS
    CASE "赤"
        RETURNF 0xC07070
    CASEELSE
        RETURNF 0xC0C0C0
ENDSELECT

@NAME_CSV(ARG, ARG:1)
#FUNCTIONS
EXISTCSV ARG, ARG:1
SIF RESULT == 0
    RETURNF ""
CSVNAME ARG, ARG:1
RETURNF RESULTS
```

---

## 3. 変数

### 汎用変数（整数）

| 変数 | 意味 |
|------|------|
| `A` `B` `C` ... `Z` | 汎用整数変数（1文字）。グローバル |
| `LOCAL` | 関数ローカル変数（デフォルト16個: LOCAL:0〜LOCAL:15） |
| `LOCAL:n` | LOCAL配列のn番目 |
| `ARG` `ARG:n` | 関数引数（整数） |
| `RESULT` | 関数の戻り値、INPUT後の入力値 |
| `RESULT:n` | RESULT配列 |

### 汎用変数（文字列）

| 変数 | 意味 |
|------|------|
| `LOCALS` | 文字列ローカル変数（LOCALS:0〜） |
| `LOCALS:n` | LOCALS配列のn番目 |
| `ARGS` `ARGS:n` | 関数引数（文字列） |
| `RESULTS` | 文字列の戻り値 |
| `STR:n` | グローバル文字列変数 |

### キャラ変数（`変数:キャラ番号:インデックス`）

| 変数 | 意味 |
|------|------|
| `FLAG:n` | グローバルフラグ（整数配列） |
| `TFLAG:n` | ターン一時フラグ（毎ターンリセット）|
| `CFLAG:c:n` | キャラ別フラグ（c=キャラ登録番号） |
| `ABL:c:n` | キャラ能力値 |
| `PALAM:c:n` | キャラパラメータ |
| `EXP:c:n` | キャラ経験値 |
| `TALENT:c:n` | キャラ素質（0/1） |
| `MARK:c:n` | キャラマーク |
| `SOURCE:c:n` | ソース値 |
| `TEQUIP:c:n` | キャラ装備 |
| `MAXBASE:c:n` | キャラ能力最大値 |
| `BASE:c:n` | キャラ能力現在値 |
| `CSTR:c:n` | キャラ文字列変数 |
| `ITEM:n` | アイテム所持数 |
| `MONEY` | 所持金 |

キャラ番号に `TARGET`, `MASTER`, `COUNT` 等の変数も使える:
```erb
ABL:TARGET:0       ; TARGETキャラのABL:0
CFLAG:MASTER:81    ; MASTERキャラのCFLAG:81
TALENT:COUNT:10    ; REPEATのCOUNTキャラのTALENT:10
```

### 特殊変数（組み込み）

| 変数 | 意味 |
|------|------|
| `TARGET` | 現在対象のキャラ登録番号 |
| `MASTER` | 主人公の登録番号（通常0） |
| `ASSI` | アシスタントの登録番号 |
| `CHARANUM` | 現在パーティのキャラ数 |
| `COUNT` | REPEATループのカウンタ |
| `DAY` | 日数（総日数） |
| `DAY:1` | 日（月内日付） |
| `DAY:5` | 曜日 |
| `DAY:8` | 月 |
| `TIME` | 時間帯（0=昼, 1=夜） |
| `LINECOUNT` | 現在の行数カウンタ |
| `RAND:n` | 0〜n-1のランダム整数 |
| `NO:c` | キャラcのCSV番号（キャラNo） |
| `NAME:c` | キャラcの名前 |
| `CALLNAME:c` | キャラcの呼び名 |
| `NICKNAME:c` | キャラcのニックネーム |
| `TRAINNAME:n` | コマンド名n |
| `ABLNAME:n` | 能力名n |
| `PALAMNAME:n` | パラメータ名n |
| `TALENTNAME:n` | 素質名n |
| `SELECTCOM` | 現在選択中のコマンドID |
| `PLAYER` | プレイヤー番号（通常0） |
| `SAVESTR:n` | セーブデータ文字列 |

---

## 4. PRINT系命令

### 基本

| 命令 | 意味 |
|------|------|
| `PRINT 文字列` | 文字列を表示（改行なし） |
| `PRINTL 文字列` | 文字列を表示して改行 |
| `PRINTW 文字列` | 表示してキー待ち |
| `PRINTFORM 式` | 書式展開して表示（改行なし） |
| `PRINTFORML 式` | 書式展開して表示・改行 |
| `PRINTFORMW 式` | 書式展開して表示・キー待ち |
| `DRAWLINE` | 区切り線を表示 |
| `PUTFORM 式` | 画面に直接出力（ログに残らない） |

### SIF（条件付き単行実行）

```erb
SIF 条件
    命令
; 条件が真の場合のみ次の1行を実行（IFブロック不要）
```

### フォーム記法（PRINTFORM内）

```erb
%変数名%          ; 文字列変数の展開
{変数名}          ; 整数変数の展開
%変数名,幅%       ; 右詰め（幅文字分）
{変数名,幅}       ; 右詰め（整数）
{変数名,幅,LEFT}  ; 左詰め
%CALLNAME:TARGET% ; キャラ変数も展開可
{ABL:TARGET:0,4}  ; キャラ変数の整数展開
```

例:
```erb
PRINTFORML 【%NAME:TARGET% プロフィール】
PRINTFORM %ABLNAME:LOCAL,12%:LV{ABL:W:LOCAL,2}　
PRINTFORML 現在: %STR:10%　{DAY:8}月 {DAY:1}日
```

---

## 5. 制御構文

### IF文

```erb
IF 条件
    処理
ELSEIF 条件
    処理
ELSE
    処理
ENDIF
```

### SELECTCASE文

```erb
SELECTCASE 変数
    CASE 値
        処理
    CASE 値1, 値2
        処理
    CASE IS < 値
        処理
    CASE IS > 値
        処理
    CASEELSE
        処理
ENDSELECT
```

文字列のCASEも可:
```erb
SELECTCASE ARGS
    CASE "赤"
        ...
    CASEELSE
        ...
ENDSELECT
```

### FORループ

```erb
FOR 変数, 開始値, 終了値[, ステップ]
    処理
    CONTINUE   ; 次のループへスキップ
    BREAK      ; ループを抜ける
NEXT
```

### REPEATループ

```erb
REPEAT 回数
    ; COUNT が 0〜回数-1 の値を持つ
    処理
    CONTINUE
    BREAK
REND
```

`CHARANUM` と組み合わせてキャラ全員ループが定番:
```erb
REPEAT CHARANUM
    SIF COUNT == MASTER
        CONTINUE
    ; COUNT番のキャラに対して処理
REND
```

### WHILEループ

```erb
WHILE 条件
    処理
WEND
```

### GOTO・ラベル

```erb
$ラベル名
GOTO $ラベル名

; 入力ループの定番パターン:
$INPUT_LOOP
INPUT
IF RESULT < 0 || RESULT > 2
    GOTO INPUT_LOOP
ENDIF
```

### RETURN・RESTART

```erb
RETURN          ; 呼び出し元に戻る（戻り値なし）
RETURN 値       ; 呼び出し元にRESULTとして値を返す
RETURNF 値      ; 式中関数から値を返す（#FUNCTIONで宣言した関数）
RESTART         ; 現在の関数を最初から再実行
```

---

## 6. 関数呼び出し

| 命令 | 意味 |
|------|------|
| `CALL 関数名` | 関数を呼ぶ（存在しなければエラー） |
| `CALL 関数名, 引数1, 引数2` | 引数付き呼び出し |
| `TRYCALL 関数名` | 存在しない場合は無視 |
| `CALLFORM 式` | 関数名を式で組み立てて呼ぶ |
| `TRYCALLFORM 式` | 存在しない場合は無視 |
| `TRYCCALL 関数名` | TRYCALLと同じだがCATCH/ENDCATCHと組み合わせて使う |
| `TRYCCALLFORM 式` | TRYCALLFORMのCATCH版 |

```erb
; 動的な関数名でのCALL（キャラNoを埋め込む）
TRYCALLFORM DAILY_LIFE_MESSAGE_{NO:LOCAL}(LOCAL)
TRYCCALLFORM SELF_KOJO_K{ARG}

; CATCH（TRYCCALLで関数が存在しなかった場合の処理）
TRYCCALL 関数名
CATCH
    ; 関数が存在しなかった時の処理
ENDCATCH
```

---

## 7. 入力命令

| 命令 | 意味 |
|------|------|
| `INPUT` | 整数入力待ち → `RESULT` に格納 |
| `INPUTS` | 文字列入力待ち → `RESULTS` に格納 |
| `ONEINPUT` | 1キー入力（整数）|
| `ONEINPUTS` | 1キー入力（文字列）|
| `WAIT` | キー待ち（結果は捨てる）|
| `WAITANYKEY` | 任意キー待ち |

---

## 8. 演算

### 算術

```erb
A = B + C
A = B - C
A = B * C
A = B / C      ; 整数除算（切り捨て）
A = B % C      ; 剰余
A += 5
A -= 3
A *= 2
TIMES A, 1.50  ; A を1.50倍（整数に切り捨て）
```

### ビット演算

```erb
FLAG:23 |= 8        ; FLAG:23 の bit3 を立てる（OR代入）
FLAG:23 &= ~8       ; FLAG:23 の bit3 を消す
A = B & C           ; AND
A = B | C           ; OR
A = B ^ C           ; XOR
FLAG:62 |= 1p22     ; 1p22 = 2^22（ビットシフト記法）
```

### 比較・論理

```erb
IF A == B           ; 等しい
IF A != B           ; 等しくない
IF A < B
IF A <= B
IF A > B
IF A >= B
IF A && B           ; AND
IF A || B           ; OR
IF !A               ; NOT
```

---

## 9. 文字列操作

| 関数 | 意味 |
|------|------|
| `TOSTR(整数)` | 整数→文字列変換 |
| `TOINT(文字列)` | 文字列→整数変換 |
| `STRLEN(文字列)` | 文字列長（バイト数） |
| `STRLENS(文字列)` | 文字列長（文字数、全角=1） |
| `STRLENSU(文字列)` | 文字列長（Unicodeコードポイント数）|
| `STRFIND(文字列, 検索語)` | 検索語の位置（-1=見つからない） |
| `STRCOUNT(文字列, 検索語)` | 検索語の出現回数 |
| `CHARATU(文字列, n)` | n番目の文字を返す |
| `SUBSTRING(文字列, 開始, 長さ)` | 部分文字列（長さ-1で末尾まで）|
| `ISNUMERIC(文字列)` | 数値文字列なら1 |
| `ESCAPE(文字列)` | 特殊文字をエスケープ |
| `REPLACE(対象変数, 検索, 置換)` | 文字列置換（破壊的） |

### SPLIT命令

```erb
SPLIT 文字列, 区切り文字, LOCALS
; RESULT に分割数, LOCALS:0〜LOCALS:n-1 に各要素が入る
```

### AUTO_SPLIT_INT（組み込み関数）

```erb
LOCAL = AUTO_SPLIT_INT(LOCALS, "/", RAND:STRCOUNT(LOCALS, "/"))
; LOCALS から "/" 区切りのランダムな整数1つを取得
```

---

## 10. キャラ操作

| 命令 | 意味 |
|------|------|
| `EXISTCSV キャラNo, 0` | CSVが存在するか（RESULT=1/0） |
| `ADDCHARA キャラNo` | キャラをパーティに追加 |
| `DELCHARA 登録番号` | キャラをパーティから削除 |
| `GETCHARA キャラNo` | キャラの登録番号をRESULTに返す（居なければ-1）|
| `FINDCHARA 変数名, 値` | 変数が一致するキャラを検索 |
| `FINDELEMENT(配列, 値, 開始, 終了, 完全一致)` | 配列から値を検索してインデックスを返す |
| `CSVABL キャラNo, ABL番号, 0` | CSVのABL初期値をRESULTに返す |
| `CSVNAME キャラNo, 0` | CSVの名前をRESULTSに返す |
| `SORTCHARA` | キャラ一覧をソート |

---

## 11. 特殊命令

| 命令 | 意味 |
|------|------|
| `VARSET 変数[, 値[, 開始[, 終了]]]` | 変数を一括初期化（省略時0/"") |
| `DRAWLINE` | 区切り線を表示 |
| `BEGIN イベント名` | 特定フェーズへジャンプ（SHOP, AFTERTRAIN等）|
| `LOADGLOBAL` | グローバルデータをロード |
| `SAVEGLOBAL` | グローバルデータをセーブ |
| `TRYCALL GET_STRAINVALUE` | 存在しない場合は無視して続行 |

---

## 12. よく使うパターン

### 入力ループ

```erb
$INPUT_LOOP
INPUT
IF RESULT == 0
    CALL 処理A
ELSEIF RESULT == 1
    CALL 処理B
ELSEIF RESULT == 9
    RETURN 0
ELSE
    PRINTFORML 正しい値を入力してください
    GOTO INPUT_LOOP
ENDIF
```

### キャラ全員ループ（主人公除く）

```erb
REPEAT CHARANUM
    SIF COUNT == MASTER
        CONTINUE
    ; COUNT番のキャラに対して処理
    ABL:COUNT:0 += 1
REND
```

### 動的関数名でキャラ固有処理

```erb
; キャラNoに応じた関数を呼ぶ（存在しなければ共通処理）
TRYCCALLFORM DAILY_LIFE_MESSAGE_{NO:LOCAL}(LOCAL)
CATCH
    CALL DAILY_LIFE_MESSAGE(LOCAL)
ENDCATCH
```

### ビットフラグで複数ON/OFF管理

```erb
;設定をビット単位で管理するパターン
FLAG:23 |= 8        ; bit3 をON
FLAG:23 &= ~8       ; bit3 をOFF
IF (FLAG:23 & 8) == 0   ; bit3 がOFFの場合
IF FLAG:23 & 8          ; bit3 がONの場合
FLAG:62 |= 1p22     ; 2^22 ビットをON
```

### ランダムキャラ選択

```erb
; 条件を満たすキャラの番号を"/"区切りで貯めてランダムに選ぶ
VARSET LOCALS
FOR LOCAL, 0, CHARANUM
    SIF LOCAL == MASTER
        CONTINUE
    SIF CFLAG:LOCAL:21 == 0  ; 条件チェック
        LOCALS += TOSTR(LOCAL) + "/"
NEXT
SIF STRCOUNT(LOCALS, "/") == 0
    RETURN 0  ; 対象なし

LOCAL = AUTO_SPLIT_INT(LOCALS, "/", RAND:STRCOUNT(LOCALS, "/"))
```

### 引数付き式中関数

```erb
; 定義側
@CHARA_NOW(ARG)
#FUNCTION
GETCHARA ARG
IF RESULT > -1
    SIF CFLAG:RESULT:21
        RETURNF 2   ; 別れている
    RETURNF 1       ; 居る
ENDIF
RETURNF 0           ; 居ない

; 呼び出し側（式の中で使える）
IF CHARA_NOW(37) == 1
    PRINTFORML 居る
ENDIF
```

---

## 13. BEGIN に使えるフェーズ名

| フェーズ | 意味 |
|---------|------|
| `BEGIN SHOP` | ショップに移行 |
| `BEGIN AFTERTRAIN` | 調教後処理に移行 |
| `BEGIN TURNEND` | ターン終了処理に移行 |

---

## 14. よくあるバグパターン

1. **`==1` チェック不要**: `IF TALENT:T:10` で素質チェック可（0以外=真）
2. **文字列代入に `%...%` 不要**: `STR:10 = テスト` でOK。`%テスト%` は変数展開
3. **`RETURN` なしで関数終了**: 末尾到達でも自動RETURN。最後に必ずRETURNを書く習慣
4. **`LOCAL` のスコープ**: LOCAL は関数をまたがない。CALLした先では別のLOCALになる
5. **`REPEAT` のCOUNT**: REPEAT内でしか使えない。FOR内は指定した変数を使う
6. **TRYCCALLFORM後のCATCH**: CATCH...ENDCATCHを忘れると構文エラー
7. **`SIF` は1行のみ**: `SIF` の次の1行だけが条件付き。ブロックには使えない
