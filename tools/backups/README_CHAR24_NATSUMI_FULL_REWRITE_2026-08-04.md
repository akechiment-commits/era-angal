# CHAR24 三波なつみ COM口上 全体リライト前バックアップ

- 元ファイル: `ERB/CHAR/CHAR_24_三波なつみ_COM.ERB`
- バックアップ: `tools/backups/CHAR_24_三波なつみ_COM.before_full_rewrite_2026-08-04.ERB`
- 取得日: 2026-08-04
- 文字コード・改行: CP932 / CRLF
- SHA-256: `66970241B9393D16C2F93471C8E95B3E334A058162B246BE760C031311AF8D4F`

追加10コマンド（COM60/62/76/78/79/84/86/202/258/318）を実装した直後、
既存口上の全体リライトへ着手する前の状態を、バイト単位でそのまま退避したもの。

PowerShellで復元する場合:

```powershell
Copy-Item -LiteralPath 'tools/backups/CHAR_24_三波なつみ_COM.before_full_rewrite_2026-08-04.ERB' -Destination 'ERB/CHAR/CHAR_24_三波なつみ_COM.ERB' -Force
```
