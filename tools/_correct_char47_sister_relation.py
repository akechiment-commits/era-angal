from pathlib import Path


target = Path(r"ERB\CHAR\CHAR_47_双葉みなづき_COM.ERB")
text = target.read_bytes().decode("cp932")

old = "「お姉ちゃんのベッドの隣で、君といるの、変な気分だね。……でも、ひとりで待つよりずっといいや」"
new = "「みづちゃんのベッドの隣で、君といるの、変な気分だね。……でも、ひとりで待つよりずっといいや」"
if old not in text:
    raise SystemExit("sister-room sentence not found")
text = text.replace(old, new, 1)

if "みなづきのベッド" in text or "みなづきが姉" in text or "みなづきは姉" in text:
    raise SystemExit("reversed sibling relation remains")
if "みづきが妹" in text or "みづちゃんが妹" in text:
    raise SystemExit("reversed sibling relation remains")

target.write_bytes(text.encode("cp932"))
