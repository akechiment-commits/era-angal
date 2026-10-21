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
            pass  # already comment, we handled header above
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

    # 5. Lines 1149-1264: Execution blocks
    elif 1149 <= line_no <= 1264:
        new_lines.append(';' + line)

    else:
        new_lines.append(line)

# Convert all lines to CRLF and write in cp932
output_text = "".join(new_lines).replace('\r\n', '\n').replace('\n', '\r\n')
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'wb') as f:
    f.write(output_text.encode('cp932'))
print("Updated ERB/SHOP_ITEM_ショップアイテム定義.ERB")

# Update CSV/Item.csv
with open('CSV/Item.csv', 'r', encoding='cp932') as f:
    item_lines = f.readlines()

new_item_lines = []
for line in item_lines:
    if line.startswith('86,') or line.startswith('87,'):
        new_item_lines.append(';' + line)
    else:
        new_item_lines.append(line)

output_item = "".join(new_item_lines).replace('\r\n', '\n').replace('\n', '\r\n')
with open('CSV/Item.csv', 'wb') as f:
    f.write(output_item.encode('cp932'))
print("Updated CSV/Item.csv")

# Update CSV/Talent.csv
with open('CSV/Talent.csv', 'r', encoding='cp932') as f:
    talent_lines = f.readlines()

new_talent_lines = []
for line in talent_lines:
    if line.startswith('181,') or line.startswith('182,'):
        new_talent_lines.append(';' + line)
    else:
        new_talent_lines.append(line)

output_talent = "".join(new_talent_lines).replace('\r\n', '\n').replace('\n', '\r\n')
with open('CSV/Talent.csv', 'wb') as f:
    f.write(output_talent.encode('cp932'))
print("Updated CSV/Talent.csv")
