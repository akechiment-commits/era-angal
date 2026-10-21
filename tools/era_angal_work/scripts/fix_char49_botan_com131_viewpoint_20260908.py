"""CHAR49 COM131の行為者視点を明示する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB"
OLD = 'PRINTFORMW 「縛られると急に素直になるんだ……。転校生くん、逃げられないなら、わたしの質問にちゃんと答えてね♪」'
NEW = 'PRINTFORMW 「わたしが縛ると急に素直になるんだ……。転校生くん、逃げられないなら、わたしの質問にちゃんと答えてね♪」'


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    if data.count(OLD) != 1:
        raise RuntimeError(f"expected one occurrence, found {data.count(OLD)}")
    PATH.write_bytes(data.replace(OLD, NEW).replace("\n", "\r\n").encode("cp932"))
    print("fixed COM131 viewpoint")


if __name__ == "__main__":
    main()
