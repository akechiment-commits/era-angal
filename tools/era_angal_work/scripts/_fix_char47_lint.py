from pathlib import Path


path = Path(r"ERB\CHAR\CHAR_47_双葉みなづき_COM.ERB")
text = path.read_bytes().decode("cp932")
old = "「ふふ、%LOCALS%に満たされていくの、分かるよ。お姉さんの反応、ちゃんと見ててね♪」"
new = "「ふふ、%LOCALS%に満たされていくの、分かるよ。お姉さんの反応、そばで感じててね♪」"
if old not in text:
    raise SystemExit("target sentence not found")
path.write_bytes(text.replace(old, new, 1).encode("cp932"))
