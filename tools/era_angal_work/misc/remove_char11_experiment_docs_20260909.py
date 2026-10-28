"""CHAR11の設定・v3プロンプトから原作外の実験解釈を除去する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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
    for old, new in replacements.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{path}: expected one occurrence of {old!r}, got {count}")
        text = text.replace(old, new, 1)
    path.write_bytes(text.encode(encoding))
    return len(replacements)


def main() -> int:
    count = replace_exact(ROOT / "tools/CHAR_11_氷野くるみ_設定.txt", "utf-8", SETTING_REPLACEMENTS)
    count += replace_exact(ROOT / "tools/v3prompt/prompt_くるみ_v3.txt", "utf-8", PROMPT_REPLACEMENTS)
    print(f"removed/reframed {count} experiment-contaminated terms from docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
