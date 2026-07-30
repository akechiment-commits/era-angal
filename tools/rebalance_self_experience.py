from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELATIVE = "ERB/SELF_セルフコマンド.ERB"


def read_cp932() -> str:
    return (ROOT / RELATIVE).read_bytes().decode("cp932").replace("\r\n", "\n")


def write_cp932(text: str) -> None:
    data = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    (ROOT / RELATIVE).write_bytes(data)


def section(text: str, start_label: str, end_label: str | None) -> tuple[int, int, str]:
    start = text.index(start_label)
    end = text.index(end_label, start) if end_label else len(text)
    return start, end, text[start:end]


def replace_section(
    text: str, start_label: str, end_label: str | None, transform
) -> str:
    start, end, body = section(text, start_label, end_label)
    return text[:start] + transform(body) + text[end:]


def remove_growth_cap(body: str, limit: int, label: str) -> str:
    old = f""";回数と経験は上限{limit}
S:1 = S
SIF S >= {limit}
	S = {limit}
"""
    new = """;回数と経験は能力に応じて上限なく伸びる
S:1 = S
"""
    if old in body:
        return body.replace(old, new, 1)
    if new in body:
        return body
    raise RuntimeError(f"{label}: growth cap block not found")


def rebalance_after_v(body: str) -> str:
    body = remove_growth_cap(body, 12, "AFTER_V_CHECK")
    if body.count("S * 20") == 2 and body.count("S*20") == 1:
        body = body.replace("S * 20", "S * 4")
        body = body.replace("S*20", "S*4")
    elif body.count("S * 4") != 2 or body.count("S*4") != 1:
        raise RuntimeError("AFTER_V_CHECK: experience multiplier pattern mismatch")
    return body


def rebalance_after_l(body: str) -> str:
    if body.count("N*20") == 3:
        body = body.replace("N*20", "N*4")
    elif body.count("N*4") != 3:
        raise RuntimeError("AFTER_L_CHECK: experience multiplier pattern mismatch")
    return body


def remove_after_s_cap(body: str) -> str:
    old = """;回数と経験は上限12
A:1 = A
SIF A >= 12
	A = 12
"""
    new = """;回数と経験は能力に応じて上限なく伸びる
A:1 = A
"""
    if old in body:
        return body.replace(old, new, 1)
    if new in body:
        return body
    raise RuntimeError("AFTER_S_CHECK: growth cap block not found")


def remove_night_cap(body: str, label: str) -> str:
    return remove_growth_cap(body, 9, label)


def rebalance_yobai(body: str) -> str:
    body = remove_night_cap(body, "SELF_YOBAI")
    pairs = (
        ("EXP:40 += S * 20", "EXP:40 += S * 10"),
        ("EXP:MASTER:40 += S * 20", "EXP:MASTER:40 += S * 10"),
        ("%EXPNAME:40%＋{S*20}", "%EXPNAME:40%＋{S*10}"),
    )
    for old, new in pairs:
        if old in body:
            body = body.replace(old, new, 1)
        elif new not in body:
            raise RuntimeError("SELF_YOBAI: experience multiplier pattern mismatch")
    return body


def rebalance_kiss_yobai(body: str) -> str:
    body = remove_night_cap(body, "SELF_KISSYOBAI")
    pairs = (
        ("EXP:40 += S * 10", "EXP:40 += S * 5"),
        ("EXP:MASTER:40 += S * 10", "EXP:MASTER:40 += S * 5"),
        ("%EXPNAME:40%＋{S*10}", "%EXPNAME:40%＋{S*5}"),
    )
    for old, new in pairs:
        if old in body:
            body = body.replace(old, new, 1)
        elif new not in body:
            raise RuntimeError("SELF_KISSYOBAI: experience multiplier pattern mismatch")
    return body


def validate(text: str) -> None:
    _, _, after_v = section(text, "@AFTER_V_CHECK", "@AFTER_S_CHECK")
    if "S * 20" in after_v or "S*20" in after_v:
        raise RuntimeError("immediate post-training multiplier remains x20")
    if after_v.count("S * 4") != 2 or after_v.count("S*4") != 1:
        raise RuntimeError("immediate post-training multiplier is not consistently x4")

    _, _, after_l = section(text, "@AFTER_L_CHECK", "@AFTER_KISS_CHECK")
    if "N*20" in after_l or after_l.count("N*4") != 3:
        raise RuntimeError("assistant post-training multiplier is not consistently x4")

    for start_label, end_label in (
        ("@AFTER_V_CHECK", "@AFTER_S_CHECK"),
        ("@AFTER_S_CHECK", "@AFTER_L_CHECK"),
        ("@SELF_YOBAI", "@SELF_KISSYOBAI"),
        ("@SELF_KISSYOBAI", "@SELF_SOINE"),
        ("@SELF_SOINE", None),
    ):
        _, _, body = section(text, start_label, end_label)
        if ";回数と経験は上限" in body:
            raise RuntimeError(f"{start_label}: growth cap remains")

    _, _, yobai = section(text, "@SELF_YOBAI", "@SELF_KISSYOBAI")
    for line in (
        "EXP:40 += S * 10",
        "EXP:MASTER:40 += S * 10",
        "%EXPNAME:40%＋{S*10}",
    ):
        if yobai.count(line) != 1:
            raise RuntimeError("all-night encounter multiplier is not consistently x10")
    _, _, kiss = section(text, "@SELF_KISSYOBAI", "@SELF_SOINE")
    for line in (
        "EXP:40 += S * 5",
        "EXP:MASTER:40 += S * 5",
        "%EXPNAME:40%＋{S*5}",
    ):
        if kiss.count(line) != 1:
            raise RuntimeError("all-night kiss multiplier is not consistently x5")
    _, _, sleep = section(text, "@SELF_SOINE", None)
    if sleep.count("S * 2") != 2 or sleep.count("S*2") != 1:
        raise RuntimeError("sleepover x2 multiplier changed unexpectedly")


def main() -> None:
    text = read_cp932()
    text = replace_section(text, "@AFTER_V_CHECK", "@AFTER_S_CHECK", rebalance_after_v)
    text = replace_section(text, "@AFTER_S_CHECK", "@AFTER_L_CHECK", remove_after_s_cap)
    text = replace_section(text, "@AFTER_L_CHECK", "@AFTER_KISS_CHECK", rebalance_after_l)
    text = replace_section(
        text,
        "@SELF_YOBAI",
        "@SELF_KISSYOBAI",
        rebalance_yobai,
    )
    text = replace_section(
        text,
        "@SELF_KISSYOBAI",
        "@SELF_SOINE",
        rebalance_kiss_yobai,
    )
    text = replace_section(
        text,
        "@SELF_SOINE",
        None,
        lambda body: remove_night_cap(body, "SELF_SOINE"),
    )
    validate(text)
    write_cp932(text)
    print("Rebalanced post-training experience without growth caps.")


if __name__ == "__main__":
    main()
