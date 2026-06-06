# eraあんガル 開発セッション案内

このリポジトリは **eraあんガル**（eratohoJ を君咲学院71キャラ向けに改造したゲーム）の開発リポジトリです。

## ⛔ ERB を書く前に必ず目を通す致命的ルール（この節は毎回必ず読め）

以下は過去に実際に踏み抜いた罠。**コード1行書く前にこの節全体を読み返すこと**。
「別ファイルを読め」では守られないと証明済みなので、核心はここに全部書く。

### ルール A: 文字列代入 `=` は**リテラル代入**。クォートが混入する

```erb
LOCALS = "face_"              ; ← LOCALS の中身は 「"face_"」 （7文字、クォート込み！）
LOCALS += TOSTR(A) + ".png"   ; ← += は式モードなのでクォート剥がれる
; 結果: 「"face_"64.png」 （先頭にクォートが残る → ファイル見つからず失敗）
```

**正しい書き方（どちらか使う）**:
```erb
LOCALS '= @"face_{A}.png"     ; '= + @"..." 書式代入（推奨）
; または
LOCALS = ""                   ; "" だけは空文字扱いの特例
LOCALS += "face_"             ; += は式モードなのでクォート剥がれる
LOCALS += TOSTR(A) + ".png"
```

### ルール B: 実装前に必ず**既存 ERB を grep する**

「自分で設計する前にプロジェクト内で同じことをしている場所を探す」。例:
- 顔グラ表示 → `ERB/EVENT_S_特殊イベント.ERB:1225` (CSV リソース + HTML_PRINT 方式が既に動いている)
- キャラループ → `REPEAT CHARANUM` パターンを既存から引く
- 引数付き関数定義 → 既存の `@関数名, ARG` 宣言を見てから真似る

`Grep` で関連キーワード（例: `HTML_PRINT`, `SPRITECREATE`, `GCREATEFROMFILE`）を先に走らせること。
**外部リポジトリ（erablue_resort 等）より自プロジェクトのコードを優先**する。

### ルール C: CSV / ERB ファイルは必ず **Shift-JIS (cp932) + CRLF**

- UTF-8 で保存するとエンジンが全部無視する（face.csv 事件の原因）
- LF 改行だと Windows エンジンが誤動作する可能性

### ルール D: 関数定義に引数宣言がなければ `CALL 関数名, ARG` は失敗する

```erb
@MYFUNC, ARG, ARGS    ; ← 引数を受ける側に宣言が必要
```

宣言なしで `CALL MYFUNC, 1, "foo"` は「引数が多すぎます」エラー。

### ルール E: HTML_PRINT の第2引数の使い分け

- CSV リソース名 (`<img src='face_01'>`) を描画 → `HTML_PRINT str`（**引数なし**）
- `SPRITECREATE` で作った名前付きスプライトを描画 → `HTML_PRINT str, 1`

混同すると文字列がそのまま表示されるか、何も出ない。

### ルール F: `GCREATE` を `GCREATEFROMFILE` の前に呼ばない

### ルール G: ERB / CSV ファイルの編集には **Edit ツールを絶対に使うな**

Edit ツールは cp932 ファイルを UTF-8 で上書きする。日本語が全文字化けしてエンジンが解析不能になる（SOURCE ERB 事件の原因）。

**ERB / CSV の読み書きは必ず Python スクリプト経由**:
```python
# 読み込み
with open('ERB/foo.ERB', 'rb') as f:
    text = f.read().decode('cp932')

# 書き込み（CRLF で）
with open('ERB/foo.ERB', 'wb') as f:
    f.write(text.encode('cp932'))
```

`GCREATE 0, 512, 512` → `GCREATEFROMFILE 0, "xxx.png"` と書くと、ファイル読み込み失敗時も
`GCREATED(0) == 1` を返してしまい、空白バッファから SPRITECREATE → 何も映らない。
**そもそも顔グラ表示は CSV + HTML_PRINT で足りる。GCREATEFROMFILE は原則使うな**
（動的ファイル名が必要な時だけ）。

---

## セッション開始時に必ずやること

1. 上の「⛔ ERB を書く前に必ず目を通す致命的ルール」節を読み直す
2. `TECHNICAL_PLAN.md` を読んで現在の進捗・設計を把握する（作業完了のたびに進捗を更新すること）
3. `資料/EmueraEE_リファレンス.md` と `資料/Emuera_ERB構文リファレンス.md` を読む（上の致命的ルールに載っていない細則がある）
4. 作業は**作業ブランチ上**で行う（`master` で直接作業しない）
   - セッションで指定された作業ブランチ（`claude/*` 等）を使う。指定がなければ作業用ブランチを切る
   - セッション開始時に作業ブランチを最新化する（`git fetch origin` → 作業ブランチを `origin/master` 相当に追従）
   - **`master` へ渡すのは「作業が一段落したとき」または「ユーザーから要求があったとき」だけ**。それ以外は勝手に master へマージ・プッシュしない
   - 作業ブランチへのコミット・プッシュは随時行ってよい（確認不要）。`master` への反映は上記タイミングでのみ
   - `master` へ反映する際は、作業ブランチから `origin/master` へファストフォワード（または通常マージ）で渡す。force push は事前確認必須
   - ⚠**ローカル `master` ブランチを信用するな（「旧ローカルmaster」事件）**⚠：ローカル `master` はセッション開始のクローン時点で固定され、その後 origin/master が並行 force-update されても**自動では追従しない**（`git fetch` が更新するのは `origin/master` だけ）。古いまま `git checkout master` すると陳腐化したテンプレを作業ツリーに掴み、grep/比較が狂う。
     - **master を参照・反映するときは必ず最初に `git fetch origin master` し、`origin/master` を唯一の真実として扱う**（ローカル `master` の指す先は無視する）。
     - master の中身を見たいだけなら `git show origin/master:<path>` を使い、**`git checkout master` で作業ツリーを切り替えてから grep/比較するのは厳禁**。
     - master へ反映する直前は `git fetch origin master` → `git reset --hard origin/master`（または `git branch -f master origin/master`）で**ローカル master を origin/master に強制同期してから**着手する。
5. ファイルの読み書きはすべて **Shift-JIS (cp932)** エンコーディングで行う

## 重要な前提知識

- **エンジン**: `Emuera1820.exe`（ERBスクリプトインタープリタ、変更不要）
- **ERBファイル**: ゲームロジック・テキスト（Shift-JIS）
- **CSVファイル**: キャラ・パラメータ定義（Shift-JIS）
- **71キャラ**: 君咲学院の生徒、`CSV/Chara1〜71.csv` に定義済み

## 作業ルール

- **コードを読まずに書かない。必ず既存コードを確認してから変更する**
- **コンテキストが残り少ない場合、その旨を伝えて区切りを提案する**
- **調査の前に必ずリポジトリ内のデータを確認する**
  - キャラ情報: `tools/character_data.csv`, `tools/debug_list.html`（cno→キャラ名マッピング全71件収録）
  - カードデータ: `tools/card_data.csv`, `tools/all_bundles.txt`
  - ★**原作セリフの全件**: `tools/output/<キャラ名>.txt`（先頭に「全○○件」と明記＝そのキャラの全セリフ）。**原作精査・場面/趣味/事件/口調の根拠取りは、この全件ファイルと `tools/scenarios/`（原典スクリプト）を必ず読む**
  - ⚠`tools/prompt_*.txt` は**約120件のサンプル抜粋＋自動生成プロフィール**にすぎない。「120件で全部」ではない（実数は同ファイルの「セリフ総数」欄を見よ＝数百〜数千行）。さらに自動プロフィールの**一人称・語尾は不正確**（例: ゆゆは「一人称: うち」と誤記載だが、全件精査では一人称＝自分の名前「ゆゆ」）。**原作判断の根拠に prompt_*.txt を使わない**
  - `tools/output/*_分析.txt`・`*_関係性分析.txt` 等のAI派生分析も誤り混入の可能性。ヒント止まりとし、必ず全件(`output/<名>.txt`)・原典(`scenarios/`)で裏取りする
  - ウェブ検索・外部サイト参照は**リポジトリ内に該当データが存在しないと確認してから**行うこと
