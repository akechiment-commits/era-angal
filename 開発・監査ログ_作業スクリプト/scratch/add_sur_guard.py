# -*- coding: utf-8 -*-
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

target = '\tSUR \'= REPLACE(NAME:AI, CALLNAME:AI, "")\r\n\tSIF SUR == ""\r\n\t\tSUR \'= CALLNAME:AI\r\n'
replacement = '\tSUR \'= REPLACE(NAME:AI, CALLNAME:AI, "")\r\n\tSUR \'= REPLACE(SUR, "・", "")\r\n\tSIF SUR == ""\r\n\t\tSUR \'= CALLNAME:AI\r\n'

assert target in text
text = text.replace(target, replacement, 1)

with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(text.encode('cp932'))

print("SUR cleanup guard added successfully!")
