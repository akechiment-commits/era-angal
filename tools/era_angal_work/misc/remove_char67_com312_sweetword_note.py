from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")
old = "; ▼【視点】PLAYERがましろの頭を撫でる。ましろは撫でられる側。COM311の甘い言葉は混ぜない。"
new = "; ▼【視点】PLAYERがましろの頭を撫でる。ましろは撫でられる側。"
assert text.count(old) == 1, "CHAR67 COM312 viewpoint note is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
