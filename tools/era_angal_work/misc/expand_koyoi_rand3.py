from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_28_星海こよい_COM.ERB")
COMMAND_PREFIXES = ("IF SELECTCOM == ", "ELSEIF SELECTCOM == ")


def leading(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]


def is_code_rand(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("A = RAND:") or stripped.startswith("SELECTCASE RAND(")


def command_ranges(lines: list[str]):
    starts = [i for i, line in enumerate(lines) if line.startswith(COMMAND_PREFIXES)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        number = int(lines[start].split("==", 1)[1].strip())
        yield number, start, end


def matching_relation(lines: list[str], start: int) -> tuple[int, int]:
    base_indent = len(leading(lines[start]))
    depth = 0
    else_at = -1
    for pos in range(start, len(lines)):
        stripped = lines[pos].strip()
        if stripped.startswith("IF "):
            depth += 1
        elif stripped == "ELSE" and depth == 1:
            else_at = pos
        elif stripped == "ENDIF":
            depth -= 1
            if depth == 0:
                if else_at < 0:
                    raise RuntimeError(f"relationship branch has no ELSE at line {start + 1}")
                return else_at, pos
    raise RuntimeError(f"relationship branch has no ENDIF at line {start + 1}")


def suffixes(body: list[str], romantic: bool) -> tuple[str, str]:
    text = "".join(body)
    if romantic:
        if any(word in text for word in ("星", "空", "天文")):
            return "……えへへ、きれいやなぁ", "……もう少し、隣におってな"
        if any(word in text for word in ("指", "舐", "口", "入", "擦", "胸", "尻", "腰", "お腹")):
            return "……うち、もう止まれへん", "……転校生くん、優しくしてな"
        return "……えへへ、落ちつくわぁ", "……もう少しだけ、こうしてて"
    if "見" in text:
        return "……見んといてや", "……ほんま、どないしょ"
    if any(word in text for word in ("怖", "あかん", "恥ずか")):
        return "……堪忍してぇ", "……うち、心臓もたへんわぁ"
    return "……うち、どないしたらえぇのん", "……笑わんといてな"


def decorate(body: list[str], romantic: bool, suffix: str) -> list[str]:
    result = list(body)
    print_positions = [
        pos
        for pos, line in enumerate(result)
        if line.lstrip().startswith(("PRINTFORML", "PRINTFORMW", "PRINTFORM "))
    ]
    if not print_positions:
        raise RuntimeError("relationship branch contains no PRINTFORM line")
    pos = print_positions[-1]
    line = result[pos]
    quote = line.rfind("」")
    if quote >= 0:
        result[pos] = line[:quote] + suffix + line[quote:]
    else:
        result[pos] = line + suffix
    return result


def indent_body(body: list[str], amount: int) -> list[str]:
    prefix = "\t" * amount
    return [prefix + line if line else line for line in body]


def wrap_relation(lines: list[str], start: int, else_at: int, end: int) -> list[str]:
    relation_indent = leading(lines[start])
    body_romantic = lines[start + 1 : else_at]
    body_normal = lines[else_at + 1 : end]
    r1, r2 = suffixes(body_romantic, romantic=True)
    n1, n2 = suffixes(body_normal, romantic=False)

    def normal_branch_body(body: list[str], s1: str, s2: str) -> list[str]:
        inner = relation_indent + "\t"
        result = [inner + "IF A == 0"]
        result += indent_body(body, 2)
        result += [inner + "ELSEIF A == 1"]
        result += indent_body(decorate(body, False, s1), 2)
        result += [inner + "ELSE"]
        result += indent_body(decorate(body, False, s2), 2)
        result += [inner + "ENDIF"]
        return result

    result = [lines[start], relation_indent + "\tIF A == 0"]
    result += indent_body(body_romantic, 2)
    result += [relation_indent + "\tELSEIF A == 1"]
    result += indent_body(decorate(body_romantic, True, r1), 2)
    result += [relation_indent + "\tELSE"]
    result += indent_body(decorate(body_romantic, True, r2), 2)
    result += [relation_indent + "\tENDIF", relation_indent + "ELSE"]
    result += normal_branch_body(body_normal, n1, n2)
    result += [relation_indent + "ENDIF"]
    return result


def expand_segment(segment: list[str]) -> list[str]:
    header = segment[0]
    segment = list(segment)
    segment.insert(1, leading(header) + "\tA = RAND:3")

    relation_starts = [
        pos for pos, line in enumerate(segment) if line.strip() == "IF TALENT:TARGET:153"
    ]
    if not relation_starts:
        raise RuntimeError(f"no TARGET:153 relation branch under {header}")

    for start in reversed(relation_starts):
        else_at, end = matching_relation(segment, start)
        replacement = wrap_relation(segment, start, else_at, end)
        segment[start : end + 1] = replacement
    return segment


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    had_crlf = "\r\n" in text
    lines = text.splitlines()
    changed = []
    ranges = list(command_ranges(lines))
    for number, start, end in reversed(ranges):
        segment = lines[start:end]
        if any(is_code_rand(line) for line in segment):
            continue
        expanded = expand_segment(segment)
        lines[start:end] = expanded
        changed.append(number)

    if changed:
        newline = "\r\n" if had_crlf else "\n"
        TARGET.write_bytes((newline.join(lines) + newline).encode("cp932"))
    print(f"expanded={sorted(changed)}")


if __name__ == "__main__":
    main()
