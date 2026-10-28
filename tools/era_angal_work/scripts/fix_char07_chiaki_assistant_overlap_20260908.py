"""CHAR07の助手相手COMに残るCHAR09との本文重複を、ちあきの世話焼きで再構成する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"

REWRITES = {
    "「%CALLNAME:ASSI%と触れ合うと、同じところで震えるんですね……先輩、ちゃんと見ててください♪」": "「%CALLNAME:ASSI%と息を合わせると、身体まで同じリズムになるんですね……。あたし、連携の確認みたいで少し安心しました♪」",
    "%CALLNAME:ASSI%、痛くない？　無理ならすぐ止めようね。先輩も、急に動かさないでください！": "%CALLNAME:ASSI%、痛かったらすぐ言ってね。あたしが止めますから、先輩も勝手に動かさないでください！",
    "%CALLNAME:ASSI%が困ってますよ？　始めたなら、最後までちゃんと付き合ってあげてください！": "%CALLNAME:ASSI%が困ってますよ？　先輩、始めたなら最後まで面倒を見るのが筋ですからね！",
    "「お互いの熱が重なると、あたしまで大胆になっちゃいます……%CALLNAME:ASSI%、大丈夫？」": "「%CALLNAME:ASSI%の熱が近いと、あたしまで気持ちが急いじゃいます……。大丈夫？　無理ならすぐ止めようね♪」",
}


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    for old, new in REWRITES.items():
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"置換対象が一意でない: {count}件: {old}")
        text = text.replace(old, new, 1)
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print(f"CHAR07: 助手相手の重複 {len(REWRITES)}件を差別化")


if __name__ == "__main__":
    main()
