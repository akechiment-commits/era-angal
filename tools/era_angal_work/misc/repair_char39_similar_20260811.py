from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_39_冴木もも_COM.ERB"
REPLACEMENTS = {
    "%LOCALS%、こっちおいで。あたしのを、ゆっくり受け入れて……顔、上げててね♪":
        "あたしの息がかかるくらい、もっと近くへ来て。%LOCALS%の顔を見ながら、ゆっくり合わせたいな♪",
    "美術室でこんなこと？　裸のデッサンなら平気なのに、あんたに触られると顔が熱いなぁ……！":
        "美術室で？　筆洗いの音まで近く聞こえるよ。誰か来たら、あたしの顔が先に作品みたいに赤くなるからね……！",
}


def main() -> None:
    raw = COM_PATH.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count == 0:
            print(f"未適用または修正済み: {old[:20]}")
            continue
        if count != 1:
            raise ValueError(f"想定外の置換件数 {count}: {old}")
        text = text.replace(old, new)
    COM_PATH.write_bytes(text.encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR39の近似重複候補2件を別口上へ修正しました。")


if __name__ == "__main__":
    main()
