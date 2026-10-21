from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "ERB/CHAR/CHAR_22_鯱いかり_COM.ERB": [
        ('PRINTFORMW 「見えなくても、ししょ～の手なら匂いと熱でわかるし……離れたらすぐ名前を呼んでほしいし」',
         'PRINTFORMW 「ししょ～、目を隠しておくし？　にしし、あたしの声だけ聞いてるの、ちょっと楽しいし♪」'),
        ('PRINTFORMW 「目隠しされる側だし!?　先輩、触る場所を黙って変えたらびっくりして噛みつくし～っ！」',
         'PRINTFORMW 「先輩、これで見えないし？　あたしが近づいてもびっくりしないように、声はかけるし～っ！」'),
        ('PRINTFORMW 「動けないぶん、ししょ～へ全部任せるし……あたしが不安になる前に何度でも触れてほしいし」',
         'PRINTFORMW 「ししょ～、動かないでほしいし？　あたしがちゃんと押さえてるから、安心して任せてほしいし♪」'),
        ('PRINTFORMW 「ほんとに身体が動かないし！　先輩、勝ち誇る前に苦しくないか確かめるしっ！」',
         'PRINTFORMW 「先輩、苦しくないか確かめながら押さえるし！　変なところで強がらず、すぐ言ってほしいしっ！」'),
        ('PRINTFORMW 「んむっ……（ししょ～にしか聞こえない声でも、全部受け止めてほしいし。目ぇそらしちゃ駄目だし）」',
         'PRINTFORMW 「ししょ～、声が出しにくくても目で返事できるし？　あたし、ちゃんと見てるから安心してほしいし♪」'),
        ('PRINTFORMW 「んんーっ！（先輩、返事できないときだけ質問するのは卑怯だし！　外したら覚えてるし～っ！）」',
         'PRINTFORMW 「先輩、声が出しにくいなら目で合図してほしいし？　苦しかったら、あたしがすぐ外すしっ！」'),
    ],
    "ERB/CHAR/CHAR_65_時国そら_COM.ERB": [
        ('PRINTFORMW 「ん……縛られて、動けない……。あなたに、委ねるしかないの……ゆん♪」',
         'PRINTFORMW 「ゆん、ゆん……あなたが動けない。わたしの声は聞こえる？　そばにいるから、安心して……♪」'),
        ('PRINTFORMW 「ひゃ……っ。う、動けない……っ。恥ずかしい……」',
         'PRINTFORMW 「ひゃ……っ。動けないんだね……。苦しかったら、ゆん、ゆんって返して。わたし、すぐにほどくから……」'),
    ],
    "ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB": [
        ('PRINTFORMW 「んっ、口を塞がれるのは私じゃないのか！？　うう、ちゃんと苦しくないようにするぞ！」',
         'PRINTFORMW 「んっ、声が出せないんだな！？　うう、苦しくないか？　団長、ちゃんと目を見てるからな！」'),
    ],
}

def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))

def main() -> None:
    total = 0
    for relative, pairs in REPLACEMENTS.items():
        path = ROOT / relative
        text = read_cp932(path)
        for old, new in pairs:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{relative}: expected one occurrence, got {count}: {old}")
            text = text.replace(old, new, 1)
            total += 1
        write_cp932(path, text)
        print(f"updated {relative}: {len(pairs)} lines")
    print(f"total updated lines: {total}")

if __name__ == "__main__":
    main()

