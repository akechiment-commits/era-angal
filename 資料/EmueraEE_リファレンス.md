# EmueraEM+EE グラフィックスリファレンス（eraあんガル用）

このゲームでは Emuera1820.exe の代わりに **EmueraEM+EE** を使用することで顔グラ等の画像表示が可能になる。
EmueraEM+EE は Emuera1824 をベースに evilmask 氏が拡張したバージョン。

---

## ⚠️ 最初に必ず読む: 文字列代入の罠

**このリファレンスで一番大事な節。顔グラが出ない時の 99% の原因。**

ERB の文字列代入には **3種類のモード** があり、挙動がまったく違う：

| 演算子 | モード | 例 | 結果 |
|---|---|---|---|
| `=`  | **リテラル代入**（右辺を生テキストとして保存）| `LOCALS = "face_"` | **`"face_"`** ← クォートごと保存！ |
| `=`  | リテラル代入（クォートなし）| `LOCALS = face_` | `face_` |
| `+=` | **式モード**（式として評価してから追加）| `LOCALS += "face_"` | `face_` が追加される（クォート剥がれる）|
| `'=` | **書式代入**（右辺を PRINTFORM と同じルールで展開）| `LOCALS '= @"face_{A}.png"` | `face_64.png`（A=64 展開）|

### 過去に踏み抜いた実例

```erb
LOCALS = "face_"          ; ← これが罠。LOCALS = 「"face_"」（5文字ではなく7文字）
LOCALS += TOSTR(A) + ".png"  ; ← += は式モードなのでクォート剥がれる
```

A=64 の時の結果 → **`"face_"64.png`** （先頭にクォートが混入、ファイル見つからず）

診断出力 `[画像NG: "face_"64.png]` でようやく気付いた。

### 正しい書き方（推奨パターン）

```erb
; パターン1: '= + @"..." 書式代入（一番安全）
LOCALS '= @"face_{A}.png"

; パターン2: += で初期化から組み立てる（EVENT_S で使用中）
LOCALS = ""                  ; 先に空にする（= でも "" は特殊で空になる）
LOCALS += "<img src='face_"
LOCALS += TOSTR(A)
LOCALS += "' height='150px'>"
HTML_PRINT LOCALS

; パターン3: リテラル代入（クォートなし、展開も不可）
LOCALS = face_               ; LOCALS = "face_" （5文字）
```

**ルール**: 文字列を組み立てる時は `'=` + `@"..."` か、`+=` を使う。`= "..."` は絶対に使わない。

---

## 1. resources/ フォルダの構成

```
resources/
├── face.csv       ← スプライト定義（リソース名 → ファイル名マッピング）
├── comimg.csv     ← コマンド別画像スプライト定義（未運用）
├── face_01.png    ← 画像ファイル
├── face_02.png
└── ...
```

対応フォーマット: **bmp / jpg / png**

---

## 2. スプライト定義 CSV の書式

`resources/` 内の CSV ファイル（例: `face.csv`）でリソース名と画像ファイルを対応付ける。

```
;コメント（;で始まる行は無視）
リソース名,ファイル名[,x,y,width,height]
```

- `x,y,width,height` は省略可。省略時は画像全体を1スプライトとして使用
- CSV は **Shift-JIS** で保存すること（Emuera エンジン要件）
- CSV は **CRLF 改行** で保存すること（Windows エンジン前提）

例（このゲームの face.csv）:
```
face_01,face_37.png   ; Chara1（三善かなえ）→ cno=37 のファイル
face_02,face_38.png   ; Chara2（北川ゆき）→ cno=38
```

**重要**: `リソース名` が ERB から `<img src='...'>` で参照する名前。`ファイル名` は実際の PNG ファイル名。

---

## 3. ★推奨方式：HTML_PRINT + CSV リソース名による画像表示

**このゲームで実際に動いている最シンプルな方式。顔グラはこれでいい。**

### 手順

1. `resources/face.csv` でリソース名 → ファイル名の対応を定義（Shift-JIS, CRLF）
2. 画像ファイルを `resources/` 直下に置く
3. ERB 側で `<img src='リソース名' height='NNpx'>` を文字列として組み立てる
4. `HTML_PRINT 文字列` で描画（**第2引数なし**）

### 実装例（ERB/EVENT_S_特殊イベント.ERB:1225 — 実際に動いているコード）

```erb
;ARG:0 = キャラ番号（1-71）
LOCALS = ""                           ; 空で初期化
LOCALS += "<img src='face_"
IF ARG:0 < 10
    LOCALS += "0"                     ; 2桁ゼロ埋め
ENDIF
LOCALS += TOSTR(ARG:0)
LOCALS += "' height='150px'><br><br><br><br><br><br><br><br><br><br><br><br>"
HTML_PRINT LOCALS
```

- リソース名は `face_01` ～ `face_71`（2桁ゼロ埋め）
- `face.csv` が起動時に読まれてリソース名が自動で使えるようになる（`SPRITELOAD` 不要）
- `HTML_PRINT LOCALS`（第2引数なし）で `<img>` がそのまま画像として描画される

### `'=` + `@"..."` 書式なら更に簡潔

```erb
IF A < 10
    LOCALS '= @"<img src='face_0{A}' height='150px'>"
ELSE
    LOCALS '= @"<img src='face_{A}' height='150px'>"
ENDIF
REPEAT 12
    LOCALS += "<br>"
REND
HTML_PRINT LOCALS
```

### 画像回り込み対策

`HTML_PRINT` で `<img>` を出すと、後続のテキストが画像の右側に回り込む。`<br>` を複数追加して次のテキストを画像の下に追いやる必要がある。画像高さ 150px なら `<br>` × 8〜12 個が目安。

### HTML_PRINT の第2引数

- **`HTML_PRINT str`** （引数なし）← **CSV リソース名を使う時はこれ**。`<img src='リソース名'>` が正しく描画される
- `HTML_PRINT str, 1` ← SPRITECREATE で作った**名前付きスプライト**を `<img src='スプライト名'>` で参照する時に使う

**教訓**: CSV リソース名なら第2引数なし。自分で作った名前付きスプライトなら `, 1`。混同すると何も出ないか、文字列がそのまま表示される。

---

## 4. ★非推奨：GCREATEFROMFILE + SPRITECREATE（手動ロード方式）

CSV 方式が使えない事情（動的なファイル名、webp 対応、アニメ等）がない限り**使うな**。コードが無駄に複雑になる。erablue_resort の動的グラ切り替えシステムがこの方式を使っている。

### 基本フロー

```erb
GCREATEFROMFILE バッファID, "ファイル名"            ; resources/ 相対パス（第3引数なしまたは0）
; 注: GCREATE で事前バッファ作成はしない（失敗時も GCREATED が 1 を返してしまう）
IF GCREATED(バッファID)
    SPRITECREATE "スプライト名", バッファID, 0, 0, GWIDTH(バッファID), GHEIGHT(バッファID)
    LOCALS '= @"<img src='スプライト名' height='150px'>"
    HTML_PRINT LOCALS, 1                          ; ★第2引数 1 必須
ENDIF
```

### 書式

```
GCREATEFROMFILE グラフィックID, "ファイルパス"[, 0/1]
```

- 第3引数省略 or `0`: `resources/` フォルダからの相対パス（`"face_01.png"` のように書く）
- 第3引数 `1`: exe ファイルからの相対パス（`"resources/face_01.png"` のように書く）

### 踏み抜いた罠

1. **GCREATE を事前に呼ぶな**: `GCREATE 0, 512, 512` を先に呼ぶと、`GCREATEFROMFILE` が失敗しても `GCREATED(0)` が 1 を返し、空白バッファから画像が出来上がる（→ 何も見えない）
2. **resources/ プレフィックスの混同**: 第3引数なしなら resources 相対なので `"face_01.png"`、第3引数 `1` なら exe 相対なので `"resources/face_01.png"`
3. **HTML_PRINT の第2引数忘れ**: SPRITECREATE で作った名前付きスプライトには `HTML_PRINT str, 1` が必要

### 使用例（このゲームの COMIMAGE）

将来的に動的ファイル名が必要になった場合のみ使う。現状の顔グラ表示は CSV 方式で十分。

---

## 5. SPRITELOAD / SPRITECREATED

CSV 定義のスプライトをコードから明示的にロード・確認する命令。

```erb
SPRITELOAD "リソース名"          ; スプライトをロード
SPRITECREATED("リソース名")      ; ロード済みなら1、未ロードなら0
```

**HTML_PRINT でのインライン表示では `SPRITELOAD` は不要**（エンジンが CSV 定義を起動時に読み込んで自動ロードする）。

---

## 6. face.csv のキャラ番号 → cno 対応

このゲームでは Chara CSV 番号（Chara1〜71）とゲーム内 ID（cno）が異なる。
`resources/face.csv` でこのマッピングを行っている。

- リソース名: `face_{Chara番号}` (2桁ゼロ埋め) 例: `face_01`
- ファイル名: `face_{cno}.png` 例: `face_37.png`

完全なマッピング表は `resources/face.csv` のコメント参照（各行にキャラ名・cnoを記載済み）。
cno の一覧は `tools/debug_list.html` に全71キャラ分が収録されている。

---

## 7. emuera.config 関連設定

現在のプロジェクトの `emuera.config`（抜粋）:

```
描画インターフェース:WINAPI
ウィンドウ幅:800
ウィンドウ高さ:700
```

EmueraEM+EE では `WINAPI` 描画のまま HTML_PRINT が使える。特別な設定変更は不要。

---

## 8. 注意事項

1. **Emuera1820.exe では HTML_PRINT の `<img>` が動作しない**。EmueraEM+EE が必要
2. **resources/ CSV は Shift-JIS + CRLF** で保存（ERB ファイルと同様）
3. **リソース名は大文字小文字を区別しない**（emuera.config の設定による）
4. **画像ファイルは resources/ フォルダ直下**に置く（サブフォルダ不可）
5. **face.csv を編集したらエンジン再起動**が必要（起動時に読み込まれる）
6. **文字列代入は `=` ではなく `+=` か `'=` を使う**（ゼロ番目の節参照）

---

## 9. 未使用コマンド（参考）

EmueraEM+EE には他にも以下のグラフィック命令がある（このゲームでは未使用）:

| 命令 | 概要 |
|------|------|
| `GCREATE` | グラフィックバッファを作成（GCREATEFROMFILE の前には呼ばない）|
| `GDISPOSE` | グラフィックバッファを解放 |
| `GFILL` | バッファを色で塗りつぶす |
| `GDRAWG` | バッファ間コピー |
| `GSETCOLOR` | 描画色設定 |
| `PRINT_IMG` | 別形式の画像プリント命令 |
| `HTML_TAGSAVE` | HTML をファイルに保存 |
| `ANIME` スプライト定義 | CSV で複数フレームのアニメーション定義 |

---

## 10. トラブルシューティング早見表

| 症状 | 原因 | 対処 |
|---|---|---|
| 何も表示されない | ファイル名にクォートが混入（`"face_"64.png`）| `=` を `+=` か `'=` に変える |
| `<img src='...'>` が文字列のまま表示 | HTML_PRINT の第2引数誤り | CSV リソース名なら引数なし、名前付きスプライトなら `,1` |
| `[画像NG: xxx.png]` 診断が出る | ファイルが resources/ に無い | ファイル配置を確認 |
| face.csv 編集したのに反映されない | エンジン未再起動 | Emuera を終了して再起動 |
| face.csv の日本語コメントが化ける | UTF-8 で保存した | Shift-JIS (cp932) + CRLF で保存し直す |
