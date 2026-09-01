# 口上編集の正典ファイル

長い会話の記憶に依存して視点や口調を取り違えないための作業用資料です。

## キャラ仕様表

`CHAR_TEMPLATE.json` を `CHAR_61_名前.json` のようにコピーし、次の資料を全文確認して埋めます。

1. `tools/CHAR_NN_名前_設定.txt`
2. `tools/CHAR_NN_名前_整合記録.txt`
3. `tools/output/名前.txt`
4. `tools/output/名前_転校生.txt`
5. `ERB/CHAR/CHAR_NN_名前_COM.ERB`

設定・分析から想像した口癖ではなく、原作全文で実際に使われている一人称、呼称、語尾、記号、感情の崩れ方を記録します。`forbidden_patterns` には、過去にそのキャラで発生した誤口調や使わない変化形を入れます。

## コマンド視点契約

`tools/koujo_integrity_contracts.json` が、追加10コマンドと視点事故の多いコマンドの正しい参加者・向きを定義します。台詞を書く前に、対象COMの実装（原則 `ERB/COMF/COMF<ID>.ERB`）と照合します。

## 監査

```text
python tools/audit_koujo_integrity.py
python tools/audit_koujo_integrity.py --char 61 --require-spec --strict
python tools/audit_koujo_integrity.py --duplicates
```

`--write-manifest` で作成した `tools/koujo_manifest.json` は、既存のCOM注釈とコマンド枠を基準化します。以後、注釈の削除・改名・既存コマンド枠の消失をエラーにします。新規コマンドの追加は許可します。

この監査は口調の良し悪しを自動判定するものではありません。人間の声・視点・状況の意味を仕様表に残し、機械で構造破壊と明白な取り違えを先に止めるためのものです。
