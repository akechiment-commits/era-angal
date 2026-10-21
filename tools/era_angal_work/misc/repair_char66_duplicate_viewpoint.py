from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_66_曽根セイラ_COM.ERB"


REPAIRS = [
    (365, '「んっ、背中に熱が重なると、振り向けないのに全部分かるけれど♪」',
        '「んっ、後ろから腰を支えられると、あたしの身体まで返事をするけれど♪」'),
    (365, '「ふぁ……耳元の声が近いわね。腰をつかまれると、あたしまで急いでしまう☆」',
        '「ふぁ……背中に回った腕が近いのね。顔を見なくても、転校生くんの気持ちが伝わる☆」'),
    (365, '「はうう、顔を見られないぶん、転校生くんの動きだけを追ってる……ずるいわ」',
        '「はうう、後ろから急に動かれると、声だけを頼りにするしかないの……もう少しゆっくりね？」'),
    (365, '「は、ひっ……顔が見えないっ。急に近づかれると、心臓が追いつかない……！」',
        '「は、ひっ……背中から来るの！？　まだ心の準備ができていないけれど、急には動かないで！」'),
    (365, '「んっ、背中しか見えないのに、触られる場所だけはっきり分かるけれど……」',
        '「んっ、後ろの気配だけで触られる場所が分かるの。転校生くん、あたしを置いていかないでね？」'),
    (365, '「ふぁ……振り向けないの、こんなに心細いのね。……でも、離れないで」',
        '「ふぁ……顔を見られないぶん、声を聞いていたいわ。あたしのそばから離れないで……」'),
    (27, '「ふぁ……振り向けないの、こんなに心細いのね。……でも、離れないで」',
        '「ふぁ……後ろから奥まで響くと、身体の中が急に熱くなるのね。転校生くん、手を離さないで……」'),
    (35, '「ふぁ……見えないところでそんなに探さないで。……でも、手は止めないで」',
        '「ふぁ……あたしが泡で洗ってあげるはずなのに、転校生くんの手のほうが先に迷子なのね？　ふふふ♪」'),
    (58, '「ふぁ……見えないところでそんなに探さないで。……でも、手は止めないで」',
        '「ふぁ……湯気で見えにくくても、転校生くんの手は分かるの。もう少し、背中から離れないでね……」'),
    (198, '「んっ、こんな場所で触れるの？　落ち着かないのに、離れたくもないけれど……」',
        '「んっ、風が吹くたびに誰か来ないか気になるけれど、転校生くんの手だけは分かるの……」'),
    (198, '「ふぁ……人の気配がするたび、身体が固まるわ。……手だけは離さないで」',
        '「ふぁ……明るい場所で顔を隠せないの、怖いのに。終わるまで手を握っていてくれる？」'),
    (199, '「ふぁ……冗談の役なのに、約束みたいに聞こえるのはどうしてかしら」',
        '「ふぁ……帰宅の挨拶だけなのに、胸が跳ねるのはおかしいわね。今日は普通に過ごすのだけれど……」'),
]


def replace_in_block(text: str, command: int, old: str, new: str) -> str:
    matches = list(re.finditer(rf"(?ms)^IF SELECTCOM == {command}\b.*?(?=^;--- COM|\Z)", text))
    if len(matches) != 1:
        raise SystemExit(f"COM{command} block count is {len(matches)}")
    match = matches[0]
    block = match.group(0)
    if block.count(old) != 1:
        raise SystemExit(f"COM{command} target count is {block.count(old)}: {old}")
    block = block.replace(old, new, 1)
    return text[: match.start()] + block + text[match.end() :]


def main() -> None:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    for command, old, new in REPAIRS:
        text = replace_in_block(text, command, old, new)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"CHAR66: repaired {len(REPAIRS)} duplicate/viewpoint lines")


if __name__ == "__main__":
    main()
