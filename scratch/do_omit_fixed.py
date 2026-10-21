# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    line_no = i + 1  # 1-indexed

    # 1. Lines 201-216: Sales check
    if 201 <= line_no <= 216:
        if 'ITEMSALES:86 = 0' in line:
            new_lines.append(';赤い首輪（オミット：購入不可）\n')
            new_lines.append('ITEMSALES:86 = 0\n')
        elif 'ITEMSALES:87 = 0' in line:
            new_lines.append(';隷属の証（オミット：購入不可）\n')
            new_lines.append('ITEMSALES:87 = 0\n')
        elif line.strip() == '':
            new_lines.append(line)
        elif line.startswith(';'):
            pass  # already comment, header handled above
        else:
            new_lines.append(';' + line)

    # 2. Lines 575-578: Descriptions
    elif 575 <= line_no <= 578:
        new_lines.append(';' + line)

    # 3. Lines 582-586: Prompt text
    elif 582 <= line_no <= 586:
        if 'PRINTL 誰に使いますか？' in line:
            new_lines.append(line)
        else:
            new_lines.append(';' + line)

    # 4. Lines 625-628: Target filters
    elif 625 <= line_no <= 628:
        new_lines.append(';' + line)

    # 5. Lines 1149-1266: Execution blocks (both 86 and 87 including closing ENDIFs)
    elif 1149 <= line_no <= 1266:
        new_lines.append(';' + line)

    else:
        new_lines.append(line)

output_text = "".join(new_lines).replace('\r\n', '\n').replace('\n', '\r\n')
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'wb') as f:
    f.write(output_text.encode('cp932'))
print("Updated ERB/SHOP_ITEM_ショップアイテム定義.ERB")
