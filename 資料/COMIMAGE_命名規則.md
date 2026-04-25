# コマンド画像 仕様・使い方ガイド

実装ファイル: `ERB/COMIMAGE_コマンド画像表示.ERB`
ツール: `tools/comimage_gui.py` / `tools/rename_comimg.py`

---

## フォルダ構造

```
resources/
  chara_XX/                      <- XX はキャラ番号 01～71
    {語幹}_1.png               <- 通常ランダム枠1
    {語幹}_2.png               <- 通常ランダム枠2
    {語幹}_3.png               <- 通常ランダム枠3
    {語幹}_renbo_1.png         <- 恋慕ランダム枠1
    {語幹}_renbo_2.png         <- 恋慕ランダム枠2
    {語幹}_renbo_3.png         <- 恋慕ランダム枠3
```

例: キャラ29（春風なな）の「正常位」コマンド
```
resources/chara_29/missionary_1.png
resources/chara_29/missionary_2.png
resources/chara_29/missionary_3.png
resources/chara_29/missionary_renbo_1.png
resources/chara_29/missionary_renbo_2.png
resources/chara_29/missionary_renbo_3.png
```

---

## 選択ロジック

```
コマンド実行時
  |
  +-- 恋慕フラグ (TALENT:TARGET:85) が立っている？
        YES -> renbo_1 / renbo_2 / renbo_3 から存在するものを収集
               1枚以上あれば -> その中からランダム選択して表示
               1枚もなければ -> 通常フォールバック（下記）
        NO  -> _1 / _2 / _3 から存在するものを収集
               1枚以上あれば -> その中からランダム選択して表示
               0枚           -> 何も表示しない（エラーなし）
```

- 3枚すべて設定すれば均等に1/3ずつ、2枚なら1/2ずつ、1枚なら固定
- 番号なし（`{語幹}.png`）は使われない（旧形式）
- 対応拡張子: `.png` / `.jpg` / `.jpeg` / `.bmp`
- 表示サイズ: 高さ 400px（自動スケール）

---

## GUI ツールの使い方（推奨）

### セットアップ（初回のみ）

```
pip install tkinterdnd2 Pillow
```

- `tkinterdnd2` なし -> ダブルクリックでファイルダイアログを開く（DnD不可）
- `Pillow` なし -> サムネイル非表示（色で設定有無を確認）

### 起動

```
python tools/comimage_gui.py
```

### 操作手順

1. 上部「キャラ」ドロップダウンでキャラクターを選択（01～71）
2. 上部「バリアント」で設定したいスロットを選択
   - 通常_1 / 通常_2 / 通常_3  ... 通常時ランダム枠
   - 恋慕_1 / 恋慕_2 / 恋慕_3  ... 恋慕時ランダム枠
3. 画像ファイルをコマンドスロットにドラッグ＆ドロップ
   - ダブルクリックでもファイルダイアログが開く
4. 自動的に resources/chara_XX/{語幹}_{サフィックス}.ext へコピーされる

### スロットの色

  暗いグレー  ... 未設定（現在のバリアントに画像なし）
  濃いグリーン ... 設定済み
  サムネイル表示 ... Pillow があるとプレビュー表示

---

## CLI ツールの使い方

### ファイル一覧確認

```
python tools/rename_comimg.py scan 29
```

### コマンド名語幹一覧

```
python tools/rename_comimg.py list
```

### 手動リネーム（既存ファイルを正しい名前に変換）

```
python tools/rename_comimg.py rename 29 img001.png missionary
```

---

## コマンドID -> ファイル名語幹 対応表（全147コマンド）

### 純愛コミュニケーション系 (COM300-399)

| SELECTCOM | コマンド名 | 語幹 |
|---|---|---|
| 300 | 一緒に勉強する | benkyou |
| 301 | 会話 | kaiwa |
| 302 | プレゼント | present |
| 303 | スキンシップ | skinship |
| 304 | まったりする | mattari |
| 305 | 掃除当番 | souji |
| 306 | 髪梳き | kamisuki |
| 307 | 櫛で梳かす | kushi |
| 309 | 素材探し | sozai |
| 310 | 調合 | chogou |
| 311 | 甘い言葉 | amaikotoba |
| 312 | 頭を撫でる | atama |
| 313 | 願掛け | negai |
| 314 | 炬燵にあたる | kotatsu |
| 315 | お散歩する | osanpo |
| 316 | 髪を梳いて貰う | kamikashite |
| 320 | 学食に行く | gakushoku |
| 321 | 遊びに行く | asobi |
| 322 | ストリートライブ | live |
| 323 | デート | date |
| 340 | バードキス | bird_kiss |
| 341 | ソフトキス | soft_kiss |
| 342 | ディープキス | deep_kiss |
| 360 | 胸愛撫（着衣） | mune_aibu_cha |
| 361 | 愛撫（着衣） | aibu_cha |
| 362 | 指挿入れ（着衣） | yubi_cha |
| 363 | 着衣挿入 | insert_cha |
| 364 | 着衣Gスポット刺激 | gspot_cha |
| 365 | 着衣後背位 | doggy_cha |
| 366 | 着衣騎乗位 | cowgirl_cha |
| 367 | 着衣ローター | roter_cha |
| 368 | 炬燵かがり | kotatsu_kagari |
| 370 | 抱き合う | dakiawu |
| 371 | オムツ | omutsu |
| 372 | 尻愛撫 | shiri_aibu_cha |
| 373 | フェラチオ（着衣） | fellatio_cha |
| 380 | フェラする（着衣） | fellatio_s |
| 381 | セックスさせる（着衣） | sex_s |
| 390 | ゲームセンター | game_center |
| 391 | 衣装替え | ishou |
| 392 | 衣装破り | ishou_yaburi |
| 393 | 見つめあう | mitsumeau |
| 399 | 告白する | kokuhaku |

### ウフフ通常系 (COM0-257)

| SELECTCOM | コマンド名 | 語幹 |
|---|---|---|
| 0 | 愛撫 | aibu |
| 1 | クンニ | kunni |
| 2 | アナル愛撫 | anal_aibu |
| 3 | 自慰 | jii |
| 4 | フェラする | fela |
| 5 | 胸愛撫 | mune_aibu |
| 6 | キスする | kisu |
| 7 | 何もしない | nanimosinai |
| 8 | 指挿入れ | yubi |
| 9 | アナル舐め | anal_name |
| 10 | ローター | roter |
| 18 | シャワー | shower |
| 19 | アナルビーズ | anal_beads |
| 20 | 正常位 | missionary |
| 21 | 後背位 | doggy |
| 22 | アナルセックス | anal_sex |
| 23 | 逆レイプ | gyaku_rape |
| 24 | 対面座位 | taimen |
| 25 | 背面座位 | haimen |
| 26 | 正常位アナル | missionary_anal |
| 27 | 後背位アナル | doggy_anal |
| 28 | 対面座位アナル | taimen_anal |
| 29 | 背面座位アナル | haimen_anal |
| 30 | 手淫 | shuin |
| 31 | フェラチオ | fellatio |
| 32 | パイズリ | paizuri |
| 33 | 素股 | sumata |
| 34 | 騎乗位 | cowgirl |
| 35 | 泡踊り | awa_odori |
| 36 | 騎乗位アナル | cowgirl_anal |
| 37 | 足扱き | ashidaki |
| 38 | 尻素股 | shiri_sumata |
| 39 | オナホ手淫 | onaho |
| 40 | スパンキング | spanking |
| 41 | 鞭 | muchi |
| 42 | 針 | hari |
| 43 | アイマスク | eyemask |
| 44 | 縄 | nawa |
| 45 | ボールギャグ | ball_gag |
| 46 | 浣腸器+プラグ | kanchou |
| 50 | ローション | lotion |
| 51 | 媚薬 | biyaku |
| 52 | 利尿剤 | rinyou |
| 53 | ビデオカメラ | video |
| 54 | 野外プレイ | outdoor |
| 56 | 助手を犯す | joshu_okasu |
| 57 | 羞恥プレイ | shuchi |
| 58 | お風呂場プレイ | ofuro |
| 59 | 新妻プレイ | niizuma |
| 61 | クンニ強制 | kunni_kyosei |
| 63 | 貝あわせ | kaiawase |
| 65 | 助手を犯させる | joshu_okasaseru |
| 66 | Wフェラ | w_fela |
| 67 | 足コキする | ashikoki |
| 68 | ダブルフェラ | double_fela |
| 71 | 秘貝開帳 | hikaichoukai |
| 75 | 言葉責め | kotoba_seme |
| 80 | イラマチオ | irrumatio |
| 85 | 放尿 | hounyou |
| 90 | アナル愛撫させる | anal_aibu_sase |
| 110 | クスコ | kusuko |
| 120 | キス正常位 | kiss_missionary |
| 121 | キス後背位 | kiss_doggy |
| 122 | キス対面座位 | kiss_taimen |
| 123 | キス背面座位 | kiss_haimen |
| 124 | キス騎乗位 | kiss_cowgirl |
| 130 | 目隠しされる | mekakushi |
| 131 | 拘束される | kousoku |
| 132 | 口枷される | kuchikase |
| 181 | コンドーム | condom |
| 182 | コンドーム精飲(P) | condom_seiin_p |
| 183 | コンドーム精飲(A) | condom_seiin_a |
| 184 | コンドーム精飲(M) | condom_seiin_m |
| 185 | 口移し | kuchiwatashi |
| 186 | 排卵誘発剤 | hairan |
| 187 | 緊急避妊薬 | hinin |
| 190 | 優しくする | yasashiku |
| 191 | 手淫する | shuin_suru |
| 192 | パイズリする | paizuri_suru |
| 193 | 正常位させる | missionary_sase |
| 194 | 後背位させる | doggy_sase |
| 195 | 騎乗位する | cowgirl_suru |
| 196 | ペニバン挿入 | peniban |
| 197 | お風呂を楽しむ | ofuro_enjoy |
| 198 | お外を楽しむ | outdoor_enjoy |
| 199 | お嫁さんで楽しむ | niizuma_enjoy |
| 200 | 乳の揉み合い | chichi_momi |
| 201 | 指フェラ | yubi_fela |
| 203 | クスコされる | kusuko_sareru |
| 204 | アナルに入れさせる | anal_iresa |
| 205 | 自慰見せつけ | jii_misetsuke |
| 255 | 挿入Gスポ責め | insert_gspot |
| 256 | 挿入子宮口責め | insert_shikyu |
| 257 | 剃毛プレイ | teimou |

### 独自コマンド

| SELECTCOM | コマンド名 | 語幹 |
|---|---|---|
| 280 | 独自ウフフ1 | com280 |
| 281 | 独自ウフフ2 | com281 |
| 282 | 独自ウフフ3 | com282 |
| 283 | 独自ウフフ4 | com283 |
| 284 | 独自ウフフ5 | com284 |
| 410 | 独自純愛1 | com410 |
| 411 | 独自純愛2 | com411 |
| 412 | 独自純愛3 | com412 |
| 413 | 独自純愛4 | com413 |
| 414 | 独自純愛5 | com414 |
