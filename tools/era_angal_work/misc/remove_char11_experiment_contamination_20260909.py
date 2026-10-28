"""CHAR11の原作にない「実験」解釈を、設定・プロンプト・口上から除去する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FILES = {
    ROOT / "ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB": "cp932",
    ROOT / "tools/CHAR_11_氷野くるみ_設定.txt": "utf-8",
    ROOT / "tools/v3prompt/prompt_くるみ_v3.txt": "utf-8",
}

REPLACEMENTS = {
    "また今度、実験させてくださいね♪": "また今度、料理を作らせてくださいね♪",
    "甘やかされる実験も好きかもしれません～": "甘やかされるのも好きかもしれません～",
    "わたしの力加減、実験してみますか？": "わたしの力加減、どうでしょう？",
    "わたしの『実験』、成功してるみたいです☆": "わたしの世話焼き、うまくいってるみたいです☆",
    "わたしの料理実験みたいに、まずは安全確認からです☆": "わたしの手料理みたいに、まずは無理しないでくださいね☆",
    "わたし、実験の記録が長くなっちゃいます♪": "わたし、知らない感覚の話が長くなっちゃいます♪",
    "夕飯はわたしの実験料理です～♪": "夕飯はわたしの手料理です～♪",
    "お料理の実験を始めてもいいですか？": "お料理を作ってもいいですか？",
    "今日はわたしの好きな実験をさせてもらいますＹＯ☆": "今日はわたしの好きなことに付き合ってもらいますＹＯ☆",
    "ごはんは実験料理、お風呂は薬草風呂にしちゃいますね♪": "ごはんはわたしの手料理、お風呂は薬草風呂にしちゃいますね♪",
    "わたしのほうまで触られると、実験が続けられません……": "わたしのほうまで触られると、続けていられません……",
    "わたしまで触られて、頭の中が実験どころじゃないです～っ": "わたしまで触られて、頭の中がそれどころじゃないです～っ",
}

SETTING_REPLACEMENTS = {
    "スコップ携帯・実験好き（突撃☆くるみのクッキング\r\n     →「くるみの実験」のノリ）で性的にも能動的・実験的に攻める。献身的(63)":
        "スコップ携帯・壊滅的な料理も笑顔で振る舞う善意の暴走（突撃☆くるみのクッキング）で性的にも能動的に動く。献身的(63)",
    "大胆さ。支配的に偉ぶるのでなく「善意・遊び・実験の延長で押す」のが核。":
        "大胆さ。支配的に偉ぶるのでなく「善意・遊びの延長で押す」のが核。",
    "料理実験の第一回ゲスト・力仕事の頼みの綱・保健委員会の頼れる先輩・":
        "善意の手料理を食べる第一回ゲスト・力仕事の頼みの綱・保健委員会の頼れる先輩・",
    "暴走・実験のノリ。受け＝処女・キス未経験で本番は崩れる初心のギャップ。":
        "暴走・善意のノリ。受け＝処女・キス未経験で本番は崩れる初心のギャップ。",
}

PROMPT_REPLACEMENTS = {
    "料理実験の第一回ゲスト": "善意の手料理を食べる第一回ゲスト",
    "料理実験の被害者": "善意の手料理を食べさせられる相手",
}


def replace_exact(path: Path, encoding: str, replacements: dict[str, str]) -> int:
    text = path.read_bytes().decode(encoding)
    changed = 0
    for old, new in replacements.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{path}: expected one occurrence of {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    path.write_bytes(text.encode(encoding))
    return changed


def main() -> int:
    changed = 0
    changed += replace_exact(next(path for path in FILES if path.name.endswith("_COM.ERB")), "cp932", REPLACEMENTS)
    setting = ROOT / "tools/CHAR_11_氷野くるみ_設定.txt"
    changed += replace_exact(setting, "cp932", SETTING_REPLACEMENTS)
    prompt = ROOT / "tools/v3prompt/prompt_くるみ_v3.txt"
    changed += replace_exact(prompt, "utf-8", PROMPT_REPLACEMENTS)
    print(f"removed/reframed {changed} experiment-contaminated terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
