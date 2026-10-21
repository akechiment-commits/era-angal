from pathlib import Path


REPLACEMENTS = {
    Path("ERB/CHAR/CHAR_08_丸子みさき_COM.ERB"): {
        "%CALLNAME:ASSI%が困ってますよ？　始めたなら、最後までちゃんと付き合ってあげてください！":
            "先輩っ、%CALLNAME:ASSI%の反応、ちゃんと拾ってください！　あたしが見てますから、無理はさせないで！",
        "%CALLNAME:ASSI%、痛くない？　無理ならすぐ止めようね。先輩も急に動かさないでください！":
            "%CALLNAME:ASSI%、嫌だったらすぐ合図してね。先輩、ラブじゃなくてリスペクトですから、急に動かさないで！",
    },
    Path("ERB/CHAR/CHAR_09_月永るか_COM.ERB"): {
        "%LOCALS%が困ってますよ？　始めたなら、最後までちゃんと付き合ってあげてください！":
            "せ、先輩……%LOCALS%の顔、ちゃんと見て。こ、こんなふうに黙られると、ぼくまで息が詰まるんです……",
        "%LOCALS%、痛くない？　無理ならすぐ止めようね。先輩も急に動かさないでください！":
            "%LOCALS%の息が乱れてます……せ、先輩、急がないで。ぼく、見ているだけでも胸が苦しいです……",
    },
}


def main() -> None:
    for path, replacements in REPLACEMENTS.items():
        text = path.read_bytes().decode("cp932")
        for old, new in replacements.items():
            assert text.count(old) == 1, (path, old, text.count(old))
            text = text.replace(old, new, 1)
        data = text.encode("cp932")
        with path.open("wb") as f:
            f.write(data)
        print(f"{path.name}: {len(replacements)}行を双方の原作声へリライト")


if __name__ == "__main__":
    main()
