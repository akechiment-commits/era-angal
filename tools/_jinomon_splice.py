# -*- coding: utf-8 -*-
# 独自コマンドの地の文枠（空テンプレ）を5場面展開へ差し込むヘルパー。
# 使い方: import して splice(path, ufufu, junai) を呼ぶ。
#   ufufu/junai = [(com, 場面名, 地の文, 恋人口上, 通常口上), ...5件]
# ※ブロックA(範囲共通口上)は触らない。Block Bの空テンプレのみ置換。
import re

def _blk(com, scene, ji, koi, tu, first):
    head = "IF" if first else "ELSEIF"
    return (f"{head} SELECTCOM == {com}\r\n"
            f"\t;◆地の文（場面: {scene}）\r\n"
            f"\tPRINTFORMW {ji}\r\n"
            f"\tIF TALENT:TARGET:153\r\n"
            f"\t\tPRINTFORMW {koi}\r\n"
            f"\tELSE\r\n"
            f"\t\tPRINTFORMW {tu}\r\n"
            f"\tENDIF\r\n")

def _expand(items):
    s=""
    for k,it in enumerate(items):
        s+=_blk(*it, first=(k==0))
    return s+"ENDIF\r\n"

def splice(path, ufufu, junai):
    b=open(path,'rb').read().decode('cp932')
    for lead, items in ((280, ufufu), (410, junai)):
        pat=re.compile(rf'IF SELECTCOM == {lead}\r\n\t;◆地の文枠（場面:.*?\r\n\t;PRINTFORMW \r\nENDIF\r\n', re.S)
        m=pat.search(b)
        if not m:
            raise SystemExit(f'[{path}] テンプレ{lead}が見つからない')
        b=b[:m.start()]+_expand(items)+b[m.end():]
    open(path,'wb').write(b.encode('cp932'))
    ifc=len(re.findall(r'(?m)^\t*ELSEIF |^\t*IF ', b))
    enc=len(re.findall(r'(?m)^\t*ENDIF', b))
    # IF と ENDIF の対応（ELSEIFはIFに属すので別数える必要なし）
    pure_if=len(re.findall(r'(?m)^\t*IF ', b))
    return f'OK {path}  IF={pure_if} ENDIF={enc} ' + ('balanced' if pure_if==enc else '★不一致')
