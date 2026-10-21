from pathlib import Path


path = next(Path(__file__).resolve().parents[3].glob("ERB/CHAR/CHAR_50*_COM.ERB"))
raw = path.read_bytes()
text = raw.decode("cp932")
lines = text.splitlines()
line_no = 3207
marker = "お風呂場でこんなことするの？"
replacement = "「お～、湯気の向こうであんたの顔が近いわさ……にゃはは、滑らないようにしっかり掴まっててよ～う♪」"
old_line = lines[line_no - 1]
if marker not in old_line or "PRINTFORMW" not in old_line:
    raise RuntimeError(f"想定文が見つかりません: {line_no}")
prefix = old_line[: old_line.index("PRINTFORMW")]
lines[line_no - 1] = prefix + "PRINTFORMW " + replacement
path.write_bytes(("\r\n".join(lines) + "\r\n").encode("cp932"))
print("CHAR50 COM58: 1行を書き換えました")
