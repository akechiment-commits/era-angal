# -*- coding: utf-8 -*-
"""
Verification of deck exclusion and outing filtering logic
"""

def test_deck_exclusion_logic():
    print("=== Testing Deck Exclusion Logic ===")
    # Simulate characters
    chars = [
        {"name": "MASTER", "hp": 2000, "leave": 0},
        {"name": "かなえ", "hp": 1500, "leave": 0},
        {"name": "ゆき", "hp": -50, "leave": 0}, # Resting
        {"name": "ちよ", "hp": 1200, "leave": 0},
        {"name": "きこ", "hp": -100, "leave": 0}, # Resting
        {"name": "あすか", "hp": 1000, "leave": 0},
    ]

    # Current deck withゆき (index 2) and きこ (index 4)
    deck = [1, 2, 3, 4, 5]
    print("Initial Deck:", [chars[i]["name"] for i in deck])

    # Run exclusion
    removed = []
    for count in range(len(deck)):
        c_idx = deck[count]
        if c_idx >= 0 and c_idx < len(chars):
            if chars[c_idx]["leave"] == 1 or chars[c_idx]["hp"] <= 0:
                removed.append(chars[c_idx]["name"])
                deck[count] = -1

    print("Removed from deck:", removed)
    print("Deck after exclusion:", [chars[i]["name"] if i >= 0 else "(空き)" for i in deck])
    assert "ゆき" in removed
    assert "きこ" in removed
    assert deck[1] == -1
    assert deck[3] == -1
    print("Deck exclusion logic test PASSED!")

def test_outing_filter_logic():
    print("\n=== Testing Outing Filter Logic ===")
    # Suppose theater club members: 15 (長町やえ: hp=-20), 36 (遠見ちか: hp=-40), 54 (湖南やこ: hp=-10)
    club_members = [15, 36, 54]
    char_db = {
        15: {"hp": -20}, # Resting
        36: {"hp": 1200}, # Active
        54: {"hp": -10}, # Resting (like in screenshot)
    }

    # Filter logic
    valid = []
    for m in club_members:
        c_info = char_db.get(m)
        if c_info and c_info["hp"] <= 0:
            continue
        valid.append(m)

    print("Original members:", club_members)
    print("Valid members present in clubroom:", valid)
    assert 54 not in valid
    assert 15 not in valid
    assert 36 in valid

    # If all resting
    char_db[36]["hp"] = 0
    valid_empty = [m for m in club_members if char_db[m]["hp"] > 0]
    print("When all members resting:", valid_empty, "-> Room is empty (LOCAL:0 == 0)!")
    assert len(valid_empty) == 0
    print("Outing filter logic test PASSED!")

if __name__ == '__main__':
    test_deck_exclusion_logic()
    test_outing_filter_logic()
