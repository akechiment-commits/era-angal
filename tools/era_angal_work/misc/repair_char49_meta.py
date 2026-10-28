from pathlib import Path


path = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB"
raw = path.read_bytes()
replacements = {
    "「%LOCALS%を舐めるの？　ふぅん、女の子同士でもこんなに反応するんだね」":
        "「%LOCALS%を舐めるの？　ふぅん、そんなに素直に反応するんだね」",
    "「女の子同士で同時に？　顔が近すぎて、息が合わないじゃない……っ」":
        "「二人同時なんて聞いてないよ！　顔が近すぎて、息が合わないじゃない……っ」",
    "「%LOCALS%と重なると、別々の鼓動がひとつに跳ねるね……。君、ちゃんと見てて♪」":
        "「%LOCALS%と重なると、別々の鼓動がひとつに跳ねるね……。そのまま、ゆっくり♪」",
    "「%LOCALS%の熱が胸越しに重なる……。君の視線まで近くて、逃げ場がないね♪」":
        "「%LOCALS%の熱が胸越しに重なる……。熱が近くて、逃げ場がないね♪」",
    "「張り合うつもりはないのに、二人の間で胸が揺れると、もっと見てほしくなる」":
        "「張り合うつもりはないのに、二人の間で胸が揺れると、もっと感じたくなる」",
}
for before, after in replacements.items():
    before_bytes = before.encode("cp932")
    after_bytes = after.encode("cp932")
    count = raw.count(before_bytes)
    if count > 1:
        raise RuntimeError(f"想定外の置換件数: {before}")
    if count == 1:
        raw = raw.replace(before_bytes, after_bytes)
path.write_bytes(raw)
print("CHAR49の視点監査用メタ表現を確認・修正しました。")
