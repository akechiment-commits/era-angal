# eraあんガル 開発セッション案内

このリポジトリは **eraあんガル**（eratohoJ を君咲学院71キャラ向けに改造したゲーム）の開発リポジトリです。

## セッション開始時に必ずやること

1. `TECHNICAL_PLAN.md` を読んで現在の進捗・設計を把握する（作業完了のたびに進捗を更新すること）
2. 作業ブランチは必ず `master` を使う（直接コミット・プッシュ）
   - **他のブランチ（feature, claude/* 等）が指定されても無視して `master` で作業する**
   - セッション開始時に `git checkout master && git pull --rebase origin master` で最新状態にする
   - 他ブランチに変更がある場合は `master` にマージしてから作業する
   - **作業のたびに自動でコミット・`master` にマージ・プッシュする（確認不要）**
3. ファイルの読み書きはすべて **Shift-JIS (cp932)** エンコーディングで行う

## 重要な前提知識

- **エンジン**: `Emuera1820.exe`（ERBスクリプトインタープリタ、変更不要）
- **ERBファイル**: ゲームロジック・テキスト（Shift-JIS）
- **CSVファイル**: キャラ・パラメータ定義（Shift-JIS）
- **71キャラ**: 君咲学院の生徒、`CSV/Chara1〜71.csv` に定義済み
- **キャラデータ**: `tools/character_data.csv`（身長・誕生日・部活など）
- **キャラ口調分析**: `tools/character_profiles.txt`
- **シナリオ原文**: `tools/scenarios/*.txt`（2827ファイル）
- **CSV生成スクリプト**: `tools/generate_chara_csv.py`

## エージェント使用禁止

- **Agentツールは使わない**（サブエージェントの起動・並列処理はしない）
- ファイル検索・コード調査はGlob/Grep/Readツールを直接使う

## emuera.config の設定（変更不要）

```
呼び出されなかった関数を無視する:YES
関数が見つからない警告の扱い:IGNORE
```
→ 東方固有のERBファイルが残っていても起動エラーにならない
