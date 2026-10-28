from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "ERB/CHAR/CHAR_52_湖南やこ_COM.ERB": [
        (
            'IF TALENT:TARGET:153\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、屋台飯はその場で食べるのが一番よ。……あんたと食べ歩くと、なんでも美味しく感じるわね。次はどれにする？♪」\n\t\tENDIF',
            'IF TALENT:TARGET:153\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、屋台飯はその場で食べるのが一番よ。……あんたと食べ歩くと、なんでも美味しく感じるわね。次はどれにする？♪」\n\t\tELSEIF A == 1\n\t\t\tPRINTFORMW 「あんた、食べ歩きでもあたしの隣から離れないのね。……ふふん、悪くないわ♪」\n\t\tELSE\n\t\t\tPRINTFORMW 「ひとくちずつ選ぶの、案外いいわね。あんたとなら、次の店まで付きあってあげる」\n\t\tENDIF',
        ),
        (
            'ELSE\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、屋台か。……世界中を巡ったあたしが言うんだから、間違いないわよ。ほら、あんたも食べなさい。あたしの奢りよ、ふふん」\n\t\tENDIF',
            'ELSE\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、屋台か。……世界中を巡ったあたしが言うんだから、間違いないわよ。ほら、あんたも食べなさい。あたしの奢りよ、ふふん」\n\t\tELSEIF A == 1\n\t\t\tPRINTFORMW 「あんた、辛いのは平気？　無理なら、あたしが食べてあげるわよ。遠慮はいらないわ」\n\t\tELSE\n\t\t\tPRINTFORMW 「熱いうちに食べなさいよ。……ほら、そんな顔してないで、次の屋台へ行くわよ♪」\n\t\tENDIF',
        ),
    ],
    "ERB/CHAR/CHAR_53_花丘まり_COM.ERB": [
        (
            'IF TALENT:TARGET:153\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、汗を流したついでにねぇ。……湯気で、何も見えやしないよ。あんたと二人、のぼせちまいそうだねぇ♪」\n\t\tENDIF',
            'IF TALENT:TARGET:153\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「ふふ、汗を流したついでにねぇ。……湯気で、何も見えやしないよ。あんたと二人、のぼせちまいそうだねぇ♪」\n\t\tELSEIF A == 1\n\t\t\tPRINTFORMW 「湯気で顔が見えないのに、あんたの気配だけは近いねぇ。……ほら、もう少しこっちへおいで♪」\n\t\tELSE\n\t\t\tPRINTFORMW 「汗を流しに来たはずなのに、胸のあたりが別の熱で困っちまうねぇ……♪」\n\t\tENDIF',
        ),
        (
            'ELSE\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「おやおや、一緒に入ろうってのかい。……まったく、しょうのない子だねぇ。……ま、背中くらい流してやるよ」\n\t\tENDIF',
            'ELSE\n\t\tIF A == 0\n\t\t\tPRINTFORMW 「おやおや、一緒に入ろうってのかい。……まったく、しょうのない子だねぇ。……ま、背中くらい流してやるよ」\n\t\tELSEIF A == 1\n\t\t\tPRINTFORMW 「おやまぁ、そんなに近寄るのかい？　滑ると危ないから、ちゃんと手を貸しておくれ」\n\t\tELSE\n\t\t\tPRINTFORMW 「湯気のせいにして、変な顔を隠してるんじゃないだろうねぇ？　ふふ、正直におし♪」\n\t\tENDIF',
        ),
    ],
}

def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))

def main() -> None:
    for relative, pairs in REPLACEMENTS.items():
        path = ROOT / relative
        text = read_cp932(path)
        for old, new in pairs:
            if text.count(old) != 1:
                raise SystemExit(f"{relative}: expected one occurrence, got {text.count(old)}")
            text = text.replace(old, new, 1)
        write_cp932(path, text)
        print(f"updated {relative}")

if __name__ == "__main__":
    main()

