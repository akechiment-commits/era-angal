"""現行CHAR52から今回の4行だけを逆変換し、監査前バックアップを作る。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_52_湖南やこ_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR52_before_personality_overlap_audit_20260908/CHAR_52_湖南やこ_COM.ERB"

REPLACEMENTS = {
    "「%LOCALS%、ちゃんと息をして……っ。そんなふうに鳴かれたら、あたしの演出まで狂うじゃない……っ」":
        "「あぁ、%LOCALS%感じてる……あたしも、夢中になっちゃう……っ」",
    "「ふん、幕が下りるまで離さないわよ。%LOCALS%、そんなに震えて……あたしのほうまで、調子が狂うじゃない……っ」":
        "「奥まで突いたら……あたしも、もう……っ」",
    "「胸を合わせて……っ。ふん、こんな近さで平気な顔なんて無理よ。あたしのほうまで、熱くなるじゃない……」":
        "「谷間でこすれて……っ。べ、べつに、気持ちよくなんか……」",
    "「ちょっと、そんなに押しつけたら……っ。べ、べつに逃げないけど、あたしのペースを乱すんじゃないわよ……っ」":
        "「そんなにされたら……っ。ふん、あたしも、もう……っ」",
}


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    for current, original in REPLACEMENTS.items():
        if text.count(current) != 1:
            raise RuntimeError(f"expected one current line, got {text.count(current)}: {current!r}")
        text = text.replace(current, original, 1)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(text.encode("cp932"))
    print(f"wrote reconstructed pre-edit backup: {BACKUP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
