from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_03_小野ちよ_COM.ERB"

OLD = [
    'PRINTFORMW 「目隠しされると…。先輩の気配だけで、ぞくっとしちゃう…。なんか楽しい…♪」',
    'PRINTFORMW 「見えないのこわい…。何されるかわからないから…ひぃん…っ」',
    'PRINTFORMW 「動けなくて…。先輩にゆだねるしかない気分…。ちょっとどきどきします…♪」',
    'PRINTFORMW 「縛られたら動けないよぉ…。解いてくださいぃ…ふぇ…っ」',
    'PRINTFORMW 「口を塞がれると声が…。先輩に全部見られちゃうけど、まあいっか…んっ…♪」',
    'PRINTFORMW 「口に入れないで…。うまく喋れなくて、こわい…ひぃん…っ」',
]

NEW = [
    'PRINTFORMW 「先輩、目を閉じててくださいね～？　えへへ、わたしの声、ちゃんと聞こえてますか……♪」',
    'PRINTFORMW 「あのう、先輩……怖くないですからね？　わたし、ここにいますよ～……♪」',
    'PRINTFORMW 「えへへ……先輩、そんなにそわそわして。もう少しだけ、わたしに任せてくださいね♪」',
    'PRINTFORMW 「あっ、きつくないですか？　痛かったら、すぐ言ってくださいね～っ」',
    'PRINTFORMW 「えへへ……先輩、おしゃべりできなくなっちゃった♪　そのぶん、目でちゃんと返事してくださいね～？」',
    'PRINTFORMW 「ふぇっ……声が出せないと困りますよね。苦しかったら、すぐ外しますからっ！」',
]

def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))

def main() -> None:
    text = read_cp932(TARGET)
    missing = [line for line in OLD if text.count(line) != 1]
    if missing:
        raise SystemExit("expected exactly one occurrence for: " + " | ".join(missing))
    for old, new in zip(OLD, NEW):
        text = text.replace(old, new, 1)
    write_cp932(TARGET, text)
    print("updated CHAR03 COM130-132: 6 lines")

if __name__ == "__main__":
    main()
