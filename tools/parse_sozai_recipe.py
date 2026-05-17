#!/usr/bin/env python3
"""
Parse material/recipe data from eraあんガル ERB/CSV files and produce a markdown reference.
"""

import re
import os
import glob


def parse_chara_names(csv_dir):
    """Parse character names from Chara CSV filenames."""
    chara_names = {}
    pattern = os.path.join(csv_dir, 'Chara*.csv')
    for path in glob.glob(pattern):
        fname = os.path.basename(path)
        # Match Chara{no}_{name}.csv or Chara{no}.csv
        m = re.match(r'Chara(\d+)_(.+)\.csv', fname)
        if m:
            no = int(m.group(1))
            name = m.group(2)
            chara_names[no] = name
        else:
            m2 = re.match(r'Chara(\d+)\.csv', fname)
            if m2:
                no = int(m2.group(1))
                # Try reading inside the CSV for name
                try:
                    with open(path, 'rb') as f:
                        text = f.read().decode('cp932')
                    for line in text.splitlines():
                        # NAME,三善かなえ style
                        lm = re.match(r'^\s*名前\s*,\s*(.+)', line)
                        if lm:
                            chara_names[no] = lm.group(1).strip()
                            break
                    if no not in chara_names:
                        chara_names[no] = f'キャラ{no}'
                except Exception:
                    chara_names[no] = f'キャラ{no}'
    return chara_names


def parse_sozai_search_by_chara(erb_path):
    """Parse character_no -> item_no mapping from COMF309.ERB."""
    with open(erb_path, 'rb') as f:
        text = f.read().decode('cp932')
    lines = text.splitlines()

    # Find @SOZAI_SEARCH_BY_CHARA function
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('@SOZAI_SEARCH_BY_CHARA'):
            start = i
            break

    if start is None:
        raise ValueError('Could not find @SOZAI_SEARCH_BY_CHARA in ' + erb_path)

    mapping = {}  # chara_no -> item_no
    current_case = None

    for line in lines[start:]:
        line_stripped = line.strip()
        # Stop at next function definition
        if line_stripped.startswith('@') and 'SOZAI_SEARCH_BY_CHARA' not in line_stripped:
            break
        # CASE N
        m = re.match(r'^CASE\s+(\d+)\s*$', line_stripped)
        if m:
            current_case = int(m.group(1))
            continue
        # TFLAG:NNN = 1
        m2 = re.match(r'^TFLAG:(\d+)\s*=\s*1\s*$', line_stripped)
        if m2 and current_case is not None:
            item_no = int(m2.group(1))
            mapping[current_case] = item_no
            current_case = None

    return mapping


def parse_item_csv(csv_path, min_no=850, max_no=992):
    """Parse item names from Item.csv for items in [min_no, max_no]."""
    with open(csv_path, 'rb') as f:
        text = f.read().decode('cp932')

    items = {}  # item_no -> item_name
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(';'):
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[0].strip().isdigit():
            no = int(parts[0].strip())
            if min_no <= no <= max_no:
                items[no] = parts[1].strip()
    return items


def parse_recipe_names(erb_path):
    """Parse recipe index -> name from @RECIPE_NAME in COMF310.ERB."""
    with open(erb_path, 'rb') as f:
        text = f.read().decode('cp932')
    lines = text.splitlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip() == '@RECIPE_NAME':
            start = i
            break

    if start is None:
        raise ValueError('Could not find @RECIPE_NAME')

    recipes = {}  # recipe_no -> name
    for line in lines[start:]:
        line_stripped = line.strip()
        # Stop at next function
        if line_stripped.startswith('@') and 'RECIPE_NAME' not in line_stripped:
            break
        # STR:2002 = 蓬莱の薬
        m = re.match(r'^STR:(\d+)\s*=\s*(.+)$', line_stripped)
        if m:
            no = int(m.group(1))
            name = m.group(2).strip()
            if no not in recipes:  # keep first assignment (for conditional names)
                recipes[no] = name

    return recipes


def parse_recipe_ingredients(erb_path):
    """Parse recipe ingredients from @RECIPE_BOOK_LIST_NAME in COMF310.ERB."""
    with open(erb_path, 'rb') as f:
        text = f.read().decode('cp932')
    lines = text.splitlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip() == '@RECIPE_BOOK_LIST_NAME':
            start = i
            break

    if start is None:
        raise ValueError('Could not find @RECIPE_BOOK_LIST_NAME')

    ingredients = {}  # recipe_no -> list of ingredient strings
    current_recipe = None
    in_known_block = False  # inside ELSEIF FLAG:A == 1 || FLAG:A == 2 block
    depth = 0  # track IF/ENDIF nesting after the function start

    # We need to parse the structure:
    # IF A == 2001
    #   IF FLAG:A == 1 || FLAG:A == 2
    #     PRINTFORML ...
    #   ...
    # ELSEIF A == 2185
    #   ...
    # ELSEIF FLAG:A == 1 || FLAG:A == 2
    #   IF A == 2001
    #     PRINTFORML ...
    #   ELSEIF A == 2002
    #     PRINTFORML ...
    #
    # Strategy: parse the ELSEIF FLAG:A section (big block starting at ELSEIF FLAG:A == 1 || FLAG:A == 2)
    # which contains ELSEIF A == XXXX followed by PRINTFORML lines

    # Find the main ELSEIF FLAG:A block
    lines_section = lines[start:]

    # Find position of "ELSEIF FLAG:A == 1 || FLAG:A == 2" (the main known-block)
    main_block_start = None
    for idx, line in enumerate(lines_section):
        ls = line.strip()
        if re.match(r'^ELSEIF\s+FLAG:A\s*==\s*1\s*\|\|\s*FLAG:A\s*==\s*2\s*$', ls):
            main_block_start = idx
            break

    if main_block_start is None:
        # fallback: parse all PRINTFORML lines after each ELSEIF A == XXXX
        pass

    # Parse the main block
    current_recipe = None
    recipe_lines = {}

    for line in lines_section[main_block_start:] if main_block_start else lines_section:
        ls = line.strip()
        # Stop at ELSE or ENDIF at depth 0 (the closing of ELSEIF FLAG:A block)
        if ls in ('ELSE', 'ENDIF'):
            if current_recipe is not None:
                pass
            break

        # Match ELSEIF A == XXXX or IF A == XXXX within the block
        m = re.match(r'^(?:ELSEIF|IF)\s+A\s*==\s*(\d+)\s*$', ls)
        if m:
            current_recipe = int(m.group(1))
            if current_recipe not in recipe_lines:
                recipe_lines[current_recipe] = []
            continue

        # Match PRINTFORML lines
        if ls.startswith('PRINTFORML ') and current_recipe is not None:
            content = ls[len('PRINTFORML '):].strip()
            if content:
                recipe_lines[current_recipe].append(content)

    # Also handle special early cases (IF A == 2001 / ELSEIF A == 2185 at top)
    # Only add to recipe_lines if not already set by the main block.
    # Also skip ？？？ lines (unknown ingredient placeholders).
    for idx, line in enumerate(lines_section):
        ls = line.strip()
        if main_block_start and idx >= main_block_start:
            break
        m = re.match(r'^(?:ELSEIF|IF)\s+A\s*==\s*(\d+)\s*$', ls)
        if m:
            current_recipe = int(m.group(1))
            continue
        if ls.startswith('PRINTFORML ') and current_recipe is not None:
            content = ls[len('PRINTFORML '):].strip()
            # Skip unknown/placeholder lines
            if content and '？' not in content:
                if current_recipe not in recipe_lines:
                    recipe_lines[current_recipe] = []
                recipe_lines[current_recipe].append(content)

    return recipe_lines


def main():
    base = '/home/user/era-angal'
    csv_dir = os.path.join(base, 'CSV')
    erb309 = os.path.join(base, 'ERB/COMF/COMF309.ERB')
    erb310 = os.path.join(base, 'ERB/COMF/COMF310.ERB')
    item_csv = os.path.join(base, 'CSV/Item.csv')
    output_path = os.path.join(base, 'tools/sozai_recipe_list.md')

    print('Parsing character names...')
    chara_names = parse_chara_names(csv_dir)
    print(f'  Found {len(chara_names)} characters')

    print('Parsing chara -> sozai mapping from COMF309.ERB...')
    chara_to_item = parse_sozai_search_by_chara(erb309)
    print(f'  Found {len(chara_to_item)} mappings')

    print('Parsing item names from Item.csv...')
    items = parse_item_csv(item_csv, 850, 992)
    print(f'  Found {len(items)} items in range 850-992')

    print('Parsing recipe names from COMF310.ERB...')
    recipe_names = parse_recipe_names(erb310)
    print(f'  Found {len(recipe_names)} recipe names')

    print('Parsing recipe ingredients from COMF310.ERB...')
    recipe_ingredients = parse_recipe_ingredients(erb310)
    print(f'  Found {len(recipe_ingredients)} recipes with ingredients')

    # Build markdown
    lines_out = []
    lines_out.append('# eraあんガル 素材・レシピ一覧')
    lines_out.append('')
    lines_out.append('> 自動生成ファイル（`tools/parse_sozai_recipe.py` で生成）')
    lines_out.append('')

    # Section 1: キャラ別専用素材一覧
    lines_out.append('## キャラ別専用素材一覧')
    lines_out.append('')
    lines_out.append('| キャラNo | キャラ名 | 専用素材（ITEM番号） | 素材名 |')
    lines_out.append('|----------|----------|---------------------|--------|')

    for chara_no in sorted(chara_to_item.keys()):
        item_no = chara_to_item[chara_no]
        chara_name = chara_names.get(chara_no, f'キャラ{chara_no}')
        item_name = items.get(item_no, f'ITEM:{item_no}')
        lines_out.append(f'| {chara_no} | {chara_name} | {item_no} | {item_name} |')

    lines_out.append('')

    # Section 2: レシピ一覧
    lines_out.append('## レシピ一覧（素材→成果物）')
    lines_out.append('')

    # Sort recipe_names by key
    all_recipe_nos = sorted(recipe_names.keys())

    for rno in all_recipe_nos:
        rname = recipe_names[rno]
        ingr_list = recipe_ingredients.get(rno, [])
        ingr_str = ' / '.join(ingr_list) if ingr_list else '（不明）'
        lines_out.append(f'### {rno}: {rname}')
        lines_out.append('')
        if ingr_list:
            for il in ingr_list:
                lines_out.append(f'- {il}')
        else:
            lines_out.append('- （素材情報なし）')
        lines_out.append('')

    md_content = '\n'.join(lines_out)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f'\nOutput written to: {output_path}')
    print(f'Total characters mapped: {len(chara_to_item)}')
    print(f'Total recipes: {len(recipe_names)}')
    print(f'Recipes with known ingredients: {len(recipe_ingredients)}')

    # Print some samples
    print('\n--- Sample chara->sozai mappings ---')
    for cno in sorted(chara_to_item.keys())[:10]:
        ino = chara_to_item[cno]
        print(f'  Chara {cno} ({chara_names.get(cno, "?")}) -> ITEM:{ino} ({items.get(ino, "?")})')

    print('\n--- Sample recipes ---')
    for rno in sorted(recipe_names.keys())[:10]:
        ingr = recipe_ingredients.get(rno, [])
        print(f'  {rno}: {recipe_names[rno]} -> {" / ".join(ingr) if ingr else "?"}')


if __name__ == '__main__':
    main()
