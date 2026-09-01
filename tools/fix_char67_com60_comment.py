from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")
old = "; 助手がましろにキスする。転校生くんは見守る側。"
new = "; ましろが助手にキスする。転校生くんは見守る側。"
assert text.count(old) == 1, "CHAR67 COM60 viewpoint comment is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
