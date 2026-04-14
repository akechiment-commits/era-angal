# EmueraEM+EE グラフィックスリファレンス（eraあんガル用）

このゲームでは Emuera1820.exe の代わりに **EmueraEM+EE** を使用することで顔グラ等の画像表示が可能になる。  
EmueraEM+EE は Emuera1824 をベースに evilmask 氏が拡張したバージョン。

---

## 1. resources/ フォルダの構成

```
resources/
├── face.csv       ← スプライト定義（リソース名 → ファイル名マッピング）
├── face_01.png    ← 画像ファイル（cnoXX順で命名）
├── face_02.png
└── ...
```

対応フォーマット: **bmp / jpg / png**

---

## 2. スプライト定義 CSV の書式

`resources/` 内の CSV ファイル（例: `face.csv`）でリソース名とファイルを対応付ける。

```
;コメント（;で始まる行は無視）
リソース名,ファイル名[,x,y,width,height]
```

- `x,y,width,height` は省略可。省略時は画像全体を1スプライトとして使用
- CSV は **Shift-JIS** で保存すること（Emuera エンジン要件）

例（このゲームの face.csv）:
```
face_01,face_37.png   ; Chara1（三善かなえ）の顔グラ → cno=37 のファイル
face_02,face_38.png   ; Chara2（北川ゆき）→ cno=38
```

**重要**: `リソース名` が ERB から参照するときの名前。`ファイル名` は実際の画像ファイル名。

---

## 3. HTML_PRINT による画像表示（★このゲームで使用中）

```erb
LOCALS = "<img src='リソース名' height='150px'>"
HTML_PRINT LOCALS
```

### 書式

```
HTML_PRINT 文字列変数
```

文字列に HTML を書いて HTML_PRINT に渡すと画面に描画される。`<img src='xxx'>` の `src` にはスプライト CSV で定義したリソース名を指定する。

### このゲームの実装例（ERB/EVENT_S_特殊イベント.ERB）

```erb
;ARG:0 = キャラ番号（1-71）
LOCALS += "<img src='face_"
IF ARG:0 < 10
    LOCALS += "0"
ENDIF
LOCALS += TOSTR(ARG:0)
LOCALS += "' height='150px'><br><br><br><br><br><br><br><br><br><br><br><br>"
HTML_PRINT LOCALS
```

リソース名は `face_01` ～ `face_71`（2桁ゼロ埋め）。`face.csv` でキャラ番号 → cno番号付き画像ファイルへマッピングされている。

### 画像回り込み対策

`HTML_PRINT` は画像の後ろにテキストが回り込む。`<br>` を複数追加して次のテキストとの間を空けること。画像高さ 150px の場合、`<br>` × 8〜12 個程度が目安。

---

## 4. GCREATEFROMFILE（グラフィックIDを直接扱う場合）

```erb
GCREATEFROMFILE グラフィックID, "ファイルパス", [0/1]
```

- 第3引数 `0`（または省略）: `resources/` フォルダからの相対パス
- 第3引数 `1`（非ゼロ）: exe ファイルのあるフォルダからの相対パス
- 読み込み後は `GDISP` 等で描画

```erb
GCREATEFROMFILE 0, "resources/face_01.png", 1
GDISP 0, 0, 0, 100, 150
```

---

## 5. SPRITELOAD / SPRITECREATED

CSV 定義のスプライトをコードから明示的にロード・確認する命令。

```erb
SPRITELOAD "リソース名"          ; スプライトをロード
SPRITECREATED("リソース名")     ; ロード済みなら1、未ロードなら0
```

HTML_PRINT でのインライン表示では通常 SPRITELOAD は不要（エンジンが自動ロード）。

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
2. **resources/ CSV は Shift-JIS** で保存（ERB ファイルと同様）
3. **リソース名は大文字小文字を区別しない**（emuera.config の設定による）
4. **画像ファイルは resources/ フォルダ直下**に置く（サブフォルダ不可）
5. **face.csv を編集したらエンジン再起動**が必要（起動時に読み込まれる）

---

## 9. 未使用コマンド（参考）

EmueraEM+EE には他にも以下のグラフィック命令がある（このゲームでは未使用）:

| 命令 | 概要 |
|------|------|
| `GCREATE` | グラフィックバッファを作成 |
| `GDISPOSE` | グラフィックバッファを解放 |
| `GFILL` | バッファを色で塗りつぶす |
| `GDRAWG` | バッファ間コピー |
| `GSETCOLOR` | 描画色設定 |
| `PRINT_IMG` | 別形式の画像プリント命令 |
| `HTML_TAGSAVE` | HTML をファイルに保存 |
| `ANIME` スプライト定義 | CSV で複数フレームのアニメーション定義 |
