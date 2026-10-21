"""CHAR67ましろの女性相手COMにある行為説明を実演へ直す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB"

REPLACEMENTS = {
    'PRINTFORMW 「ひゃっ、女の子同士でこんなに近く！？　うう、触れるたびに声が出るぞ……！」':
        'PRINTFORMW 「ひゃっ、こんなに近いのか！？　うう、触れるたびに声が出るぞ……！」',
    'PRINTFORMW 「わっ、胸を重ねるのか！？　うう、女の子同士でこんなに密着するとは……！」':
        'PRINTFORMW 「わっ、胸を重ねるのか！？　うう、密着すると鼓動まで聞こえるぞ……！」',
}


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        count = data.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, found {count}: {old}")
        data = data.replace(old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"fixed {len(REPLACEMENTS)} viewpoint explanation lines")


if __name__ == "__main__":
    main()
