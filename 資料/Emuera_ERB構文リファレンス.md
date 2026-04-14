# Emuera ERB 構文リファレンス（eraあんガル用）

出典: erablue_resort（信頼できる外部ゲームソース）+ eratohoJ本体コード

---

## 1. ファイル基本

- 文字コード: **Shift-JIS (cp932)** または **UTF-8 BOM付き**（erablue_resortはUTF-8）
- 拡張子: `.ERB`（コード）、`.ERH`（共有ヘッダ、変数宣言のみ）
- 1行1命令
- コメント: `;` で始まる行、または行末 `;` 以降

`.ERH` ファイルは複数ERBから共有する変数・定数を宣言するだけのファイル。

---

## 2. 関数定義

```erb
@関数名
@関数名, ARG, ARG:1
@関数名(ARG, ARG:1)
@関数名, ARG, ARG:1 = 0        ;デフォルト引数
@関数名, ARGS, ARGS:1 = "/"    ;文字列引数
```

### ディレクティブ一覧

| ディレクティブ | 意味 |
|---|---|
| `#PRI` | イベント関数として優先実行 |
| `#LATER` | イベント関数として後から実行 |
| `#SINGLE` | 同名関数が複数あっても1つだけ実行 |
| `#FUNCTION` | 式中関数（整数を返す）→ `RETURNF 値` |
| `#FUNCTIONS` | 式中関数（文字列を返す）→ `RETURNF "値"` |
| `#LOCALSIZE n` | LOCAL配列サイズをn個に拡張 |
| `#LOCALSSIZE n` | LOCALS配列サイズをn個に拡張 |
| `#DIM 変数名[, サイズ]` | 関数内整数ローカル変数を宣言 |
| `#DIM 日本語名` | 日本語変数名も使用可 |
| `#DIM CONST 定数名 = 値` | 定数を宣言（変更不可） |
| `#DIMS 変数名[, サイズ]` | 関数内文字列ローカル変数を宣言 |
| `#DIMS DYNAMIC 変数名, サイズ` | 動的サイズの文字列配列 |

```erb
;定数宣言の例（ERHファイルに書くことが多い）
#DIM CONST 体格_普通 = 0
#DIM CONST 体格_長身 = 1

;日本語変数名の例
@LOST_VIRGIN(ARG, ARG:1, ARG:2)
#DIMS 喪失場所
#DIM  喪失時間
喪失時間 = DAY * 1440 + TIME
```

---

## 3. 変数

### 汎用変数

| 変数 | 意味 |
|---|---|
| `A`〜`Z` | 汎用整数（グローバル） |
| `LOCAL` `LOCAL:n` | 関数内整数ローカル（デフォルト16個） |
| `LOCALS` `LOCALS:n` | 関数内文字列ローカル |
| `ARG` `ARG:n` | 関数引数（整数） |
| `ARGS` `ARGS:n` | 関数引数（文字列） |
| `RESULT` `RESULT:n` | 整数の戻り値・INPUT結果 |
| `RESULTS` | 文字列の戻り値・INPUTS結果 |
| `STR:n` | グローバル文字列変数 |

### キャラ変数（`変数:キャラ番号:インデックス`）

| 変数 | 意味 |
|---|---|
| `FLAG:n` | グローバルフラグ |
| `TFLAG:n` | ターン一時フラグ（毎ターンリセット） |
| `CFLAG:c:n` | キャラ別フラグ |
| `ABL:c:n` | 能力値 |
| `PALAM:c:n` | パラメータ |
| `EXP:c:n` | 経験値 |
| `TALENT:c:n` | 素質（0/1） |
| `MARK:c:n` | マーク |
| `SOURCE:c:n` | ソース |
| `TEQUIP:c:n` | 装備 |
| `BASE:c:n` `MAXBASE:c:n` | 現在値・最大値 |
| `CSTR:c:n` | キャラ文字列変数 |
| `ITEM:n` | アイテム所持数 |
| `MONEY` | 所持金 |

インデックスに名前が使える（CSV定義名）:
```erb
TALENT:TARGET:処女
BASE:TARGET:ムード
CFLAG:LOCAL:現在位置
```

### 拡張変数（EmueraEM+EE）

| 変数 | 意味 |
|---|---|
| `TCVAR:c:n` または `TCVAR:c:名前` | ターンキャラ変数（毎ターンリセット、キャラ別） |
| `RCVAR:c:名前` | 永続キャラ変数（名前付きアクセス） |
| `RSTR:名前` | 名前付き結果文字列 |
| `SAVESTR:名前` | 名前付きセーブ文字列 |

### 特殊変数（組み込み）

| 変数 | 意味 |
|---|---|
| `TARGET` | 対象キャラ登録番号 |
| `MASTER` | 主人公登録番号 |
| `PLAYER` | プレイヤー番号 |
| `ASSI` | アシスタント登録番号 |
| `CHARANUM` | パーティキャラ数 |
| `COUNT` | REPEATループカウンタ |
| `DAY` | 総日数 |
| `TIME` | 時刻（分単位） |
| `RAND:n` | 0〜n-1のランダム整数 |
| `NO:c` | キャラcのCSV番号 |
| `NAME:c` | キャラcの名前 |
| `CALLNAME:c` | キャラcの呼び名 |
| `PREVCOM` | 直前に実行されたコマンドID |
| `SELECTCOM` | 現在選択中のコマンドID |

---

## 4. PRINT系命令

| 命令 | 意味 |
|---|---|
| `PRINT 文字列` | 表示（改行なし） |
| `PRINTL 文字列` | 表示・改行 |
| `PRINTW 文字列` | 表示・キー待ち |
| `PRINTFORM 式` | 書式展開して表示 |
| `PRINTFORML 式` | 書式展開して表示・改行 |
| `PRINTFORMW 式` | 書式展開して表示・キー待ち |
| `PRINTSL 文字列` | 選択ボタンとして表示 |
| `PUTFORM 式` | 画面出力（ログに残らない） |
| `DRAWLINE` | 区切り線 |
| `CLEARLINE n` | 直前n行を消去 |
| `BAR 現在値, 最大値, 長さ` | プログレスバー表示 |

### SIF（条件付き単行実行）

```erb
SIF 条件
    命令     ;この1行だけが条件付き。ブロックには使えない
```

### フォーム記法

```erb
%文字列変数%          ;文字列変数を展開
{整数変数}            ;整数変数を展開
%変数,幅%             ;右詰め
{変数,幅}             ;右詰め
{変数,幅,LEFT}        ;左詰め
%CALLNAME:TARGET%     ;キャラ変数も展開可
```

### `'=` 演算子（書式代入）

右辺をPRINTFORMと同じルールで展開してから代入する:

```erb
喪失場所 '= GETPLACENAME(CFLAG:ARG:現在マップ種別, CFLAG:ARG:現在位置)
ARGS '= REPLACE(ARGS, "\/+", "/")
```

### `@"..."` 書式文字列リテラル

ダブルクォート内で `{ }` `% %` 展開が使える文字列:

```erb
@"<font color='#{カラーパレット_HTML("薄ピンク")}'>テキスト</font>"
@"{元数値 % 補正値:1 / 補正値:0}"
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
    CASE n TO m          ;n以上m以下の範囲
        処理
    CASE IS < 値
        処理
    CASE IS > 値
        処理
    CASEELSE
        処理
ENDSELECT
```

文字列も使用可:
```erb
SELECTCASE SAVESTR:ゲームフェイズ管理
    CASE "通常モード"
        処理
    CASE "マッサージモード"
        処理
ENDSELECT
```

### FORループ

```erb
FOR 変数, 開始値, 終了値[, ステップ]
    CONTINUE
    BREAK
NEXT

;逆順の例
FOR LOCAL, 5, -1, -1
```

### REPEATループ

```erb
REPEAT 回数
    ; COUNT = 0〜回数-1
    CONTINUE
    BREAK
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
GOTO $ラベル名（またはGOTO ラベル名）
RESTART    ;現在の関数を最初から再実行
```

### RETURN

```erb
RETURN           ;戻り値なし
RETURN 値        ;RESULTに値を返す
RETURNF 値       ;式中関数から値を返す（#FUNCTION時）
```

---

## 6. 演算

### 算術

```erb
A = B + C
A = B - C
A = B * C
A = B / C        ;整数除算（切り捨て）
A = B % C        ;剰余
A += 5
A -= 3
A *= 2
A ++             ;インクリメント（1加算）
A --             ;デクリメント（1減算）
LOCAL:1 ++
TIMES A, 1.50    ;Aを1.50倍（整数切り捨て）
```

### 三項演算子

```erb
変数 = 条件 ? 真の値 # 偽の値

;例
ARG:1 = ARG:1 ? ARG:1 # TARGET
;（ARG:1が0以外ならARG:1、0ならTARGETを代入）
```

### ビット演算

```erb
FLAG:23 |= 8         ;OR代入
FLAG:23 &= ~8        ;AND代入（ビット消去）
A = B & C            ;AND
A = B | C            ;OR
A = B ^ C            ;XOR
FLAG:62 |= 1p22      ;1p22 = 2^22

;ビット操作関数
GETBIT(変数, ビット番号)    ;そのビットが1なら1を返す
SETBIT(変数, ビット番号)    ;そのビットを1にする
CLEARBIT(変数, ビット番号)  ;そのビットを0にする
CHKBIT(変数, ビット番号)    ;GETBITと同じ
```

### 組み込み数学関数

```erb
MIN(a, b)        ;小さい方を返す
MAX(a, b)        ;大きい方を返す
ABS(x)           ;絶対値
POWER(底, 指数)  ;べき乗（整数）
```

### 比較・論理

```erb
== != < <= > >=
&& ||
!A               ;NOT
```

---

## 7. 関数呼び出し

| 命令 | 意味 |
|---|---|
| `CALL 関数名[, 引数...]` | 呼び出し（存在しないとエラー） |
| `TRYCALL 関数名` | 存在しない場合は無視 |
| `CALLFORM 式` | 関数名を式で構築して呼び出し |
| `TRYCALLFORM 式` | 存在しない場合は無視 |
| `TRYCCALL 関数名` | CATCH/ENDCATCHと組み合わせて使う |
| `TRYCCALLFORM 式` | 同上、関数名を式で構築 |

```erb
;動的関数名
TRYCALLFORM DAILY_LIFE_{NO:LOCAL}(LOCAL)

;CATCH
TRYCCALLFORM KOJO_K{NO:TARGET}
CATCH
    CALL COMMON_KOJO    ;関数が存在しなかった時
ENDCATCH
```

---

## 8. 入力命令

| 命令 | 意味 |
|---|---|
| `INPUT` | 整数入力 → `RESULT` |
| `INPUTS` | 文字列入力 → `RESULTS` |
| `ONEINPUT` | 1キー入力（整数） |
| `ONEINPUTS` | 1キー入力（文字列） |
| `WAIT` | キー待ち |
| `WAITANYKEY` | 任意キー待ち |

---

## 9. 文字列操作

| 関数 | 意味 |
|---|---|
| `TOSTR(整数)` | 整数→文字列 |
| `TOINT(文字列)` | 文字列→整数 |
| `STRLEN(str)` | 文字列長（バイト数） |
| `STRLENS(str)` | 文字列長（文字数、全角=1） |
| `STRLENSU(str)` | 文字列長（Unicodeコードポイント数）|
| `STRFIND(str, 検索語[, 開始])` | 検索語の位置（-1=なし） |
| `STRCOUNT(str, 検索語)` | 出現回数 |
| `SUBSTRING(str, 開始, 長さ)` | 部分文字列（長さ-1で末尾まで） |
| `SUBSTRINGU(str, 開始, 長さ)` | 同上（Unicode単位） |
| `CHARATU(str, n)` | n番目の文字を返す |
| `ISNUMERIC(str)` | 数値文字列なら1 |
| `ESCAPE(str)` | 特殊文字をエスケープ |
| `REPLACE(str, 検索, 置換)` | 文字列置換（正規表現可） |

### SPLIT命令

```erb
SPLIT 文字列, 区切り文字, 格納先配列
;RESULTに分割数、格納先配列:0〜n-1に各要素
SPLIT ARGS, "_", LOCALS
IF ISNUMERIC(LOCALS) && TOINT(LOCALS) < 200
```

---

## 10. キャラ操作

| 命令 | 意味 |
|---|---|
| `EXISTCSV キャラNo, 0` | CSVが存在するか（RESULT=1/0） |
| `ADDCHARA キャラNo` | パーティに追加 |
| `DELCHARA 登録番号` | パーティから削除 |
| `GETCHARA キャラNo` | 登録番号をRESULTに（居なければ-1） |
| `FINDELEMENT(配列, 値, 開始, 終了, 完全一致)` | 配列検索 |
| `CSVABL キャラNo, ABL番号, 0` | CSVのABL初期値をRESULTに |
| `CSVNAME キャラNo, 0` | CSVの名前をRESULTSに |

---

## 11. 特殊命令

| 命令 | 意味 |
|---|---|
| `VARSET 変数[, 値[, 開始[, 終了]]]` | 一括初期化（省略時0/""）|
| `BEGIN フェーズ名` | 特定フェーズへジャンプ（SHOP等） |
| `LOADGLOBAL` | グローバルデータをロード |
| `SAVEGLOBAL` | グローバルデータをセーブ |
| `TOOLTIP_CUSTOM 1` | ツールチップ有効化 |
| `TOOLTIP_SETFONTSIZE n` | ツールチップフォントサイズ |
| `TOOLTIP_SETDURATION n` | ツールチップ表示時間（ms） |

---

## 12. よく使うパターン

### 入力ループ

```erb
$INPUT_LOOP
INPUT
IF RESULT == 0
    CALL 処理A
ELSEIF RESULT == 9
    RETURN 0
ELSE
    PRINTFORML 正しい値を入力してください
    GOTO INPUT_LOOP
ENDIF
```

### 選択肢（CHOICE関数パターン）

```erb
PRINTSL 質問文
FOR LOCAL, 0, 選択肢数
    PRINTFORML [{LOCAL}] - %選択肢テキスト%
NEXT
$INPUT_LOOP
INPUT
SELECTCASE RESULT
    CASE 0 TO LOCAL - 1
        ;有効な入力
    CASEELSE
        CLEARLINE 1
        GOTO INPUT_LOOP
ENDSELECT
```

### キャラ全員ループ（主人公除く）

```erb
REPEAT CHARANUM
    SIF COUNT == MASTER
        CONTINUE
    ABL:COUNT:0 += 1
REND
```

### FOR+CHARANUM（named indexで途中終了）

```erb
FOR LOCAL, 1, CHARANUM
    SIF TARGET:LOCAL < 1
        BREAK
    ;処理
NEXT
```

### ランダムキャラ選択

```erb
VARSET LOCALS
FOR LOCAL, 0, CHARANUM
    SIF LOCAL == MASTER
        CONTINUE
    SIF CFLAG:LOCAL:21 == 0
        LOCALS += TOSTR(LOCAL) + "/"
NEXT
SIF STRCOUNT(LOCALS, "/") == 0
    RETURN 0
LOCAL = AUTO_SPLIT_INT(LOCALS, "/", RAND:STRCOUNT(LOCALS, "/"))
```

### ビットフラグ管理

```erb
FLAG:23 |= 8            ;bit3 ON
FLAG:23 &= ~8           ;bit3 OFF
IF (FLAG:23 & 8) == 0   ;bit3 OFFの場合
GETBIT(FLAG:23, 3)      ;bit3チェック（0/1）
FLAG:62 |= 1p22         ;2^22をON
```

### 三項演算子

```erb
;ARG:1が0以外ならそのまま、0ならTARGETを代入
ARG:1 = ARG:1 ? ARG:1 # TARGET
;ARG:1が-1ならMASTER、それ以外はARG:1
ARG:1 = ARG:1 == -1 ? MASTER # ARG:1
```

---

## 13. よくあるバグパターン

1. **`SIF` は1行のみ**: `SIF` の次の1行だけが対象。ブロックには使えない
2. **`LOCAL` のスコープ**: CALLした先では別のLOCAL。引数で渡すこと
3. **`REPEAT` のCOUNT**: REPEAT内専用。FOR内は自分で指定した変数を使う
4. **`TRYCCALLFORM` 後のCATCH**: CATCH...ENDCATCHを忘れると構文エラー
5. **`==1` は不要**: `IF TALENT:T:処女` で0以外=真なのでそのままでOK
6. **文字列代入の `%..%` 不要**: `STR:10 = テスト` でOK。`%テスト%` は変数展開
7. **`++` の対象**: `A++` は不可。`A ++`（スペース必須）
8. **`CASE TO` の範囲**: `CASE n TO m` は `n <= x <= m` ではなく `n <= x < m`（要確認）
