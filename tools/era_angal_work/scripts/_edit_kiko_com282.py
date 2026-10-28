from pathlib import Path

path = Path(r"ERB/CHAR/CHAR_04_早川きこ_COM.ERB")
raw = path.read_bytes().decode("cp932")
text = raw.replace("\r\n", "\n")

start = text.index("ELSEIF SELECTCOM == 282")
end = text.index("ELSEIF SELECTCOM == 283", start)
old = text[start:end]

new = """ELSEIF SELECTCOM == 282
\t;◆地の文（場面: 抱き枕）
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tIF A == 0
\t\t\tPRINTFORMW 「先輩、今日はあたしを抱き枕にしていいですよぉ……♪　えへへ、でも、本当はあたしが先輩をぎゅってしたいだけですぅ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ……先輩の体温が近いと、抱き枕みたいに落ち着くのに、胸はどきどきしますぅ……♪」
\t\tELSE
\t\t\tPRINTFORMW 「おろろ、抱きついたまま離れられなくなっちゃいましたぁ……。このまま先輩のそばで、眠ってもいいですかぁ……♪」
\t\tENDIF
\tELSE
\t\t;通常
\t\tIF A == 0
\t\t\tPRINTFORMW 「えっ、あたしを抱き枕にするんですかぁ!?　おろろ、そんなにぎゅってされたら、恥ずかしくて眠れませんよぉ……っ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ……先輩の腕、近いですぅ……。ふぇ、抱き枕って、こんなに顔が近くなるものなんですかぁ……？」
\t\tELSE
\t\t\tPRINTFORMW 「あ、あたしから抱きついてるみたいになってますぅ……っ。おろろ、ほどくタイミングが分からなくなっちゃいましたぁ……」
\t\tENDIF
\tENDIF
"""

if old.count("ELSEIF SELECTCOM == 282") != 1:
    raise SystemExit("COM282 target branch count mismatch")
text = text[:start] + new + text[end:]
path.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
