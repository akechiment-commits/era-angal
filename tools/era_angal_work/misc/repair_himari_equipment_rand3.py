"""CHAR61の装着系RAND3差分とCOM17を補修する。"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
COM_PATH = ROOT / "ERB" / "CHAR" / "CHAR_61_鶴海ひまり_COM.ERB"
MARKER = ";=== HIMARI EQUIPMENT RAND3 REPAIR START ==="


def load_generator():
    spec = importlib.util.spec_from_file_location("himari_generator", TOOLS / "add_himari_rand3_and_additional10.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("ひまり生成器を読み込めません")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def speech(indent: str, text: str) -> str:
    return f'{indent}PRINTFORMW 「{text}」'


EQUIPMENT_OFF: dict[int, tuple[str, str, str, str]] = {
    11: (
        "抜くのかあ……急に静かになると、身体が名残惜しそうにするのだぞお♪",
        "んっ、外れた……でも、余韻が残っているから、もう少し抱いていてくれ",
        "おお、止まった……って、急に抜くなあ、びっくりするではないかあっ",
        "ふう、やっと静かになったぞお。次は心の準備をさせてからにするのだあ",
    ),
    13: (
        "抜けるときも奥が引っぱられるみたいだ……ゆっくり、余韻まで受け止めてくれ",
        "静かになったのに、身体だけまだ震えてる……おまえ、もう一度などと言うなよお♪",
        "おお、外れた……後ろの違和感が消えるまで、急に動くなあ",
        "ふうっ、終わったかあ？　会長の心臓まで驚かせるなよおっ",
    ),
    14: (
        "外すと、さっきまでの刺激が嘘みたいに遠くなる……もう少しだけ触れていてくれ",
        "んっ、外れた……でも、身体がまだ続きを待ってるぞお",
        "取れたかあ……急に静かになると、そこだけ取り残されたみたいだぞお",
        "ふう、もう外すのか？　次はもっとゆっくり装着するのだあ",
    ),
    15: (
        "外れると胸がふっと軽くなる……でも、さっきの余韻をもう少し味わいたいなあ♪",
        "んっ、離れた……おまえの指で撫でてくれたら、もっと落ち着くのだあ",
        "外すぞお？　ひゃっ、急に引っぱるなあ、そこは敏感なのだぞおっ",
        "ふう、やっと自由になった……胸の先まで会長を驚かせるなあ",
    ),
    16: (
        "外すのかあ……胸がまだ吸われているみたいに疼くぞお♪",
        "んっ、止まった……残った熱まで、おまえの手でゆっくり落ち着かせてくれ",
        "おお、止まったかあ？　急に外すと、びっくりして声が出るぞおっ",
        "ふう……やっと静かになったのだあ。次は説明を聞いてから使うのだぞお",
    ),
}


COM17_VARIANTS = (
    (
        "んっ、奥がじわっと熱くなる……装着したばかりなのに、私の身体はもうおまえを待っているぞお♪",
        "ひゃっ、動くたびに腰が跳ねる……このままでは、せえとかいちょおの宣言が最後まで言えんのだあ",
        "こ、これは大胆すぎるのだあ!?　つけただけでこんなに存在を主張するとは聞いてないぞおっ",
        "んっ、むずむずする……おまえ、まずは弱くして、私が慣れる時間をよこすのだあ",
    ),
    (
        "外すのかあ……胸の奥まで残った感覚が、静かになるのを惜しんでいるぞお♪",
        "んっ、もう終わり？　おまえの手で、最後の震えまで落ち着かせてくれ",
        "おお、止まった……って、急に外すなあ、びっくりして声が出るぞおっ",
        "ふう、静かになったなあ。次に使うなら、せえとかいちょおへ先に説明するのだあ",
    ),
)


def replace_equipment_off(block: list[str], variants: tuple[str, str, str, str]) -> None:
    talent_indices = [i for i, line in enumerate(block) if line.strip() == "IF TALENT:TARGET:153"]
    if len(talent_indices) != 2:
        raise RuntimeError(f"装着系のTALENT分岐数が2ではありません: {len(talent_indices)}")
    start = talent_indices[1]
    end = len(block)
    depth = 1
    else_at = None
    for i in range(start + 1, len(block)):
        stripped = block[i].strip()
        if stripped.startswith("IF "):
            depth += 1
        elif stripped == "ENDIF":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        elif stripped == "ELSE" and depth == 1:
            else_at = i
            break
    if else_at is None:
        raise RuntimeError("装着系の通常分岐が見つかりません")
    rand_branches = [i for i in range(start, else_at) if block[i].strip() == "ELSEIF A == 1"]
    normal_base = [i for i in range(else_at + 1, end) if block[i].strip() == "ELSEIF A == 1"]
    if len(rand_branches) != 1 or len(normal_base) != 1:
        raise RuntimeError("装着系のA==1分岐を特定できません")
    a1_love = rand_branches[0]
    a1_normal = normal_base[0]
    for a1, new_a1, new_a2 in (
        (a1_love, variants[0], variants[1]),
        (a1_normal, variants[2], variants[3]),
    ):
        indent = block[a1 + 1][: len(block[a1 + 1]) - len(block[a1 + 1].lstrip())]
        block[a1 + 1] = speech(indent, new_a1)
        else_index = next(i for i in range(a1 + 1, end) if block[i].strip() == "ELSE")
        indent2 = block[else_index + 1][: len(block[else_index + 1]) - len(block[else_index + 1].lstrip())]
        block[else_index + 1] = speech(indent2, new_a2)


def main() -> None:
    text = COM_PATH.read_bytes().decode("cp932")
    if MARKER in text:
        print("CHAR61装着系の補修は適用済みです。")
        return
    module = load_generator()
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    # 既に追加済みのオン状態と重ならないよう、各装着COMの取り外し側だけ差し替える。
    for command_id in sorted(EQUIPMENT_OFF):
        ranges = [item for item in module.command_ranges(lines) if item[0] == command_id]
        if len(ranges) != 1:
            raise RuntimeError(f"COM{command_id}の範囲が一意ではありません")
        _, start, end = ranges[0]
        block = lines[start:end]
        replace_equipment_off(block, EQUIPMENT_OFF[command_id])
        lines[start:end] = block

    # COM17は旧来の装着/取り外し口上にRANDがなかったため、オン/オフを独立にRAND3化する。
    ranges = [item for item in module.command_ranges(lines) if item[0] == 17]
    if len(ranges) != 1:
        raise RuntimeError("COM17の範囲が一意ではありません")
    _, start, end = ranges[0]
    # COM17の直後にはSELECTCOMではなくCHAR_VIRGIN等の別口上が続くため、
    # command_rangesの終端をこのルーチン内のRETURN 0に補正する。
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "RETURN 0")
    block = lines[start:end]
    talent_indices = [i for i, line in enumerate(block) if line.strip() == "IF TALENT:TARGET:153"]
    if len(talent_indices) != 2:
        raise RuntimeError(f"COM17のTALENT分岐数が2ではありません: {len(talent_indices)}")
    for index in reversed(range(len(talent_indices))):
        talent_index = talent_indices[index]
        end_index = module.find_matching_if(block, talent_index)
        block[talent_index:end_index] = module.wrap_talent(block, talent_index, COM17_VARIANTS[index])
    lines[start:end] = block

    insert_at = next(i for i, line in enumerate(lines) if line.strip() == "RETURN 0")
    lines[insert_at:insert_at] = [MARKER, "; 装着/取り外しの状態差分とCOM17を補修。", ""]
    COM_PATH.write_bytes(("\r\n".join(lines) + "\r\n").encode("cp932"))
    print("CHAR61: 装着系5種の取り外し分岐とCOM17を補修しました。")


if __name__ == "__main__":
    main()
