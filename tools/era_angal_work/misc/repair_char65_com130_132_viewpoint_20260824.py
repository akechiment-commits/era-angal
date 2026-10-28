from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_65_時国そら_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR65_before_viewpoint_repair_20260824" / TARGET.name


REPAIRS = {
    "ゆん、ゆん……。ん……目隠し、されると……。あなたの手の、感触だけ……どきどきする……♪":
        "ゆん、ゆん……。見えないあなたの息、近くなったね。わたしの声、ちゃんと聞こえてる？♪",
    "ん……見えない……。こわいけど……そばにいて？":
        "ゆん、ゆん……。あなた、もう見えないね。こわくないよ、わたしの声を聞いて？",
    "んーっ……。し、喋れない……（声が、くぐもっちゃう）……んっ……ゆんゆん……":
        "ゆん、ゆん……。あなたの声が止まったね……。指を握ってくれると、ちゃんと返事が聞こえるよ",
    "んーっ……！　く、口に……。んっ……":
        "ゆん、ゆん……。あなた、声が出ないね……。苦しかったら、首を振って教えて？",
    "話せなくなるのは、少し怖いね……苦しくないか、目を見せて":
        "あなたが話せなくなるのは、少し怖いね……苦しくないか、目で教えて",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        BACKUP.write_bytes(raw)
    changed = 0
    for old, new in REPAIRS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected exactly one occurrence, got {count}: {old}")
        text = text.replace(old, new, 1)
        changed += 1
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))
    print(f"viewpoint_repairs={changed}/5")


if __name__ == "__main__":
    main()
