# -*- coding: utf-8 -*-
"""
Logic simulation for unconscious favor penalty
"""

def calc_command_penalty(selectcom, tflag_3, tflag_302, tflag_703,
                         is_intimate, chaste, defiant, pride, suppressed,
                         resist, unconcerned, lack_emotion, lewd):
    if is_intimate:
        return 0, "Intimate: No penalty"

    if selectcom == 7:
        return 0, "Do nothing: No penalty"

    is_invasive = (selectcom in range(60, 80) or selectcom in range(40, 60)
                   or selectcom in range(80, 90) or selectcom in range(140, 160)
                   or selectcom in range(280, 285))
    base = 60 if is_invasive else 25

    # trait modifiers
    val = float(base)
    if chaste:
        val *= 1.50
    if defiant:
        val *= 1.20
    if pride:
        val *= 1.20
    if suppressed:
        val *= 1.20
    if resist:
        val *= 1.20
    if unconcerned:
        val *= 0.60
    if lack_emotion:
        val *= 0.80
    if lewd:
        val *= 0.50

    total = int(val)

    # Virginity loss
    if tflag_3 == 1:
        v_pen = 800
        if chaste:
            v_pen += 400
        if unconcerned:
            v_pen = int(v_pen * 0.6)
        total += v_pen

    # Vaginal ejaculation
    if tflag_302 > 0 and tflag_703 in (1, 9):
        ejac_pen = 400
        if chaste:
            ejac_pen += 200
        if unconcerned:
            ejac_pen = int(ejac_pen * 0.7)
        total += ejac_pen

    return total, "Non-intimate: Penalty applied"

print("--- Unconscious Command Simulation ---")
# 1. Intimate character
p, msg = calc_command_penalty(60, 1, 1, 1, is_intimate=True, chaste=False, defiant=False, pride=False, suppressed=False, resist=False, unconcerned=False, lack_emotion=False, lewd=False)
print("Intimate character (Sex + Virginity + Ejaculation):", p, msg)

# 2. Non-intimate normal character: soft command
p, msg = calc_command_penalty(0, 0, 0, 0, is_intimate=False, chaste=False, defiant=False, pride=False, suppressed=False, resist=False, unconcerned=False, lack_emotion=False, lewd=False)
print("Non-intimate (Soft touch):", p, msg)

# 3. Non-intimate normal character: invasive sex command without ejaculation
p, msg = calc_command_penalty(60, 0, 0, 0, is_intimate=False, chaste=False, defiant=False, pride=False, suppressed=False, resist=False, unconcerned=False, lack_emotion=False, lewd=False)
print("Non-intimate (Sex without virginity/ejaculation):", p, msg)

# 4. Non-intimate normal character: taking virginity + ejaculation
p, msg = calc_command_penalty(60, 1, 1, 1, is_intimate=False, chaste=False, defiant=False, pride=False, suppressed=False, resist=False, unconcerned=False, lack_emotion=False, lewd=False)
print("Non-intimate (Virginity loss + Ejaculation):", p, msg)

# 5. Non-intimate chaste character: taking virginity + ejaculation
p, msg = calc_command_penalty(60, 1, 1, 1, is_intimate=False, chaste=True, defiant=False, pride=False, suppressed=False, resist=False, unconcerned=False, lack_emotion=False, lewd=False)
print("Non-intimate Chaste (Virginity loss + Ejaculation):", p, msg)
