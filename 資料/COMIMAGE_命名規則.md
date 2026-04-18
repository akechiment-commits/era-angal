# コマンド画像 ファイル命名規則

## フォルダ構造

```
resources/
└── chara_XX/               ← XX はキャラ番号 (01〜71)
    ├── {名前}.png           ← 通常
    └── {名前}_renbo.png     ← 恋慕時（存在すれば優先、なければ通常版を使用）
```

例: キャラ1（三善かなえ）の「会話」コマンド画像
```
resources/chara_01/kaiwa.png
resources/chara_01/kaiwa_renbo.png
```

---

## コマンドID → ファイル名語幹 対応表

| SELECTCOM | コマンド名 | ファイル名語幹 |
|---|---|---|
| 300 | 一緒に勉強する | `benkyou` |
| 301 | 会話 | `kaiwa` |
| 302 | プレゼント | `present` |
| 303 | スキンシップ | `skinship` |
| 304 | まったりする | `mattari` |
| 305 | 掃除当番 | `souji` |
| 306 | 髪梳き | `kamisuki` |
| 307 | 櫛で梳かす | `kushi` |
| 309 | 素材探し | `sozai` |
| 310 | 調合 | `chogou` |
| 311 | 甘い言葉 | `amaikotoba` |
| 312 | 頭を撫でる | `atama` |
| 313 | 願掛け | `negai` |
| 314 | 炬燵にあたる | `kotatsu` |
| 315 | お散歩する | `osanpo` |
| 316 | 髪を梳いて貰う | `kamikashite` |
| 320 | 学食に行く | `gakushoku` |
| 321 | 遊びに行く | `asobi` |
| 322 | ストリートライブ | `live` |
| 323 | デート | `date` |
| 340 | バードキス | `bird_kiss` |
| 341 | ソフトキス | `soft_kiss` |
| 342 | ディープキス | `deep_kiss` |
| 370 | 抱き合う | `dakiawu` |
| 391 | 衣装替え | `ishou` |
| 393 | 見つめあう | `mitsumeau` |
| 399 | 告白する | `kokuhaku` |

上記以外のコマンドは現在未定義。ファイルを置いても表示されない。
追加する場合は `ERB/COMIMAGE_コマンド画像表示.ERB` の SELECTCASE に追記する。

---

## 恋慕分岐ルール

- `TALENT:TARGET:85`（恋慕）が 1 のとき → `{名前}_renbo.png` を優先
- `_renbo.png` が存在しない場合 → `{名前}.png` にフォールバック
- `{名前}.png` も存在しない場合 → 何も表示しない（エラーなし）

将来追加予定の分岐軸（未実装）:
- ランダムバリエーション（`_01` / `_02` / `_03` サフィックス）
- 恋人フラグ（`TALENT:TARGET:153`）
- コマンド成否（`TFLAG:18`）

---

## 備考

- 画像形式: png / jpg / bmp いずれも可
- 画像サイズ: 高さ 150px で表示（それ以外のサイズでも自動スケール）
- 実装ファイル: `ERB/COMIMAGE_コマンド画像表示.ERB`
- 呼び出し元: `ERB/EVENT_M_マスターイベント.ERB` → `@TRAIN_MESSAGE_B`
