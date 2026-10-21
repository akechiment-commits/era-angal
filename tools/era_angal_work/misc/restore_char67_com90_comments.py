from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = ";--- COM90 アナル愛撫させる ---\r\nIF SELECTCOM == 90"
new = """;--- COM90 アナル愛撫させる ---
;  ▼【視点】キャラ攻め＝キャラがプレイヤーのアナルを愛撫する（転校生がやられる側）
;  ※パートナーがプレイヤーのアナルを愛撫するコマンド
;  ※（プレイヤーがやられる側）
IF SELECTCOM == 90""".replace("\n", "\r\n")

assert text.count(old) == 1, "CHAR67 COM90 insertion anchor is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
