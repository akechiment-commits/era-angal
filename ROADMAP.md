# eraあんガル ロードマップ

最終更新：2026-04-14

---

## 現在の状態（完成済み）

### 開発環境・資料
- **CLAUDE.md** — 開発セッション案内。セッション開始時に必ず読む手順を整備済み
- **資料/EmueraEE_リファレンス.md** — エンジン画像表示仕様（HTML_PRINT/face.csv/GCREATEFROMFILE等）
- **資料/Emuera_ERB構文リファレンス.md** — ERB構文リファレンス（erablue_resort基準で作成）
- **erablue_resort/** — 高品質な参照用eraゲームソース（ERB構文の参考に使用）

### ゲーム本体（era-angal）

| フェーズ | 内容 | 状態 |
|---|---|---|
| Phase A | 東方要素除去・CSV整備（71キャラ分） | ✅ 完了 |
| Phase B | 学校生活システム（授業・部活・試験・学期進行） | ✅ 完了 |
| Phase C | キャラ口上システム | ❌ 破棄（全ファイル不使用） |
| Phase H | カードシステム（ガチャ・コレクション・定期戦） | ✅ 完了 |
| Phase I | イベントボード周回システム | ✅ 完了 |
| Phase J | バランス調整・UI改修 | ✅ 随時完了 |
| 顔グラCSV | resources/face.csv（Chara番号→cno対応） | ✅ 完了 |

---

## 残り作業（優先度順）

### 高優先度

| タスク | 概要 | 関連ファイル |
|---|---|---|
| **特殊能力選択廃止** | `@GET_FEAT`メニューを廃止し、最大体力・最大気力強化をスキルショップに追加（段階購入方式） | `TROPHY_トロフィー.ERB`, `Talent.csv` |
| **東方固有テキストの駆逐（残り）** | 好感度イベント・朝イベント等に残る東方テキストを汎用学園テキストに | `EVENT_S_*.ERB`, `EVENT_MORNING_*.ERB` |
| **キャラ素質の随時調整** | バランス確認しながら素質・ABL・体力気力を微調整 | `CSV/Chara*.csv` |

### 中優先度

| タスク | 概要 | 関連ファイル |
|---|---|---|
| **カードボーナスを授業・部活にも反映** | 現在は校内定期戦のみ。学校行事・部活技能成長にも加算 | `CLUB_ACTIVITY.ERB`, `SCHOOL_EVENT.ERB` |
| **71人分個別エンディングテキスト** | @ENDING_MARRIAGE_1〜71 / @ENDING_GRADUATE_1〜71 の個別テキスト追加 | `ENDING_エンディング・ゲーム終了判定.ERB` |
| **遭遇セリフ（2〜3年生）** | NO:24〜71の初回・再遭遇・パートナーセリフ実装 | `CHAR_DIALOG.ERB` |

### 低優先度

| タスク | 概要 |
|---|---|
| **顔グラ表示（Phase K）** | EmueraEM+EEへ移行後、resources/に画像を置いてHTML_PRINTで表示。face.csvは整備済み |
| **シナリオ実装** | 個別イベント（エンディング基盤は完成済み、個別テキスト追加待ち） |
| **カードアルバム（図鑑）** | コンプ率表示・全カード一覧 |
| **エリア上限設定** | イベントボードのエリア番号が現状無限に上昇 |
| **カードのショップ購入** | ポイント交換・直接購入機能 |

---

## 次回セッションで開発者（Claude）がやること

セッション開始時に必ず以下を読む:
1. `TECHNICAL_PLAN.md` — 詳細進捗・設計
2. `資料/EmueraEE_リファレンス.md` — 画像表示仕様
3. `資料/Emuera_ERB構文リファレンス.md` — ERB構文

その後、上記「残り作業」から高優先度タスクに着手する。

---

## Phase K: 顔グラ表示（準備済み、実施待ち）

- `resources/face.csv` — Chara番号→cno対応マッピング完成済み
- `resources/face_XX.png` — 画像ファイルは別途配置が必要
- EmueraEM+EEエンジンへの差し替えが前提

ERBでの表示コード（実装済み、EVENT_S_特殊イベント.ERBより）:
```erb
LOCALS += "<img src='face_"
IF ARG:0 < 10
    LOCALS += "0"
ENDIF
LOCALS += TOSTR(ARG:0)
LOCALS += "' height='150px'><br><br><br><br><br><br><br><br><br><br><br><br>"
HTML_PRINT LOCALS
```
