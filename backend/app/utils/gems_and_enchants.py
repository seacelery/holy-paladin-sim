import pprint

pp = pprint.PrettyPrinter(width=200)
        
def convert_enchants_to_stats(enchants_list):
    formatted_enchants = []
    
    for enchant in enchants_list:
        enchant_parts = enchant.split("|")
        formatted_enchant = enchant_parts[0].split(": ")
        if len(formatted_enchant) == 1:
            formatted_enchant = formatted_enchant[0].strip()
        else:
            formatted_enchant = formatted_enchant[1].strip()
        formatted_enchants.append(formatted_enchant)
        
    return formatted_enchants

def return_enchants_stats(player, formatted_enchants, bonus_effect_enchants, stat_values_from_equipment):
    for enchant in formatted_enchants:
        if enchant == "Waking Stats":
            stat_values_from_equipment["intellect"] += 150
        elif enchant == "Reserve of Intellect":
            stat_values_from_equipment["intellect"] += 111
            player.max_mana += player.base_mana * 0.05
            player.mana += player.base_mana * 0.05
        elif enchant == "+177 Intellect & +5% Mana":
            stat_values_from_equipment["intellect"] += 177
            player.max_mana += player.base_mana * 0.05
            player.mana += player.base_mana * 0.05
        elif enchant == "+177 Intellect & 131 Stamina":
            stat_values_from_equipment["intellect"] += 177
            stat_values_from_equipment["stamina"] += 131
        elif enchant == "+82 Versatility":
            stat_values_from_equipment["versatility"] += 82
        elif enchant == "+82 Haste":
            stat_values_from_equipment["haste"] += 82
        elif enchant == "+82 Mastery":
            stat_values_from_equipment["mastery"] += 82
        elif enchant == "+82 Critical Strike":
            stat_values_from_equipment["crit"] += 82
        elif enchant == "Regenerative Leech":
            stat_values_from_equipment["leech"] += 125
        elif enchant == "+200 Leech":
            stat_values_from_equipment["leech"] += 200
        elif enchant == "Watcher's Loam":
            stat_values_from_equipment["stamina"] += 131
        elif enchant == "Shadowed Belt Clasp":
            stat_values_from_equipment["stamina"] += 106
            
        elif enchant == "Sophic Devotion":
            bonus_effect_enchants.append("Sophic Devotion")
        elif enchant == "Dreaming Devotion":
            bonus_effect_enchants.append("Dreaming Devotion")
        elif enchant == "Shadowflame Wreath":
            bonus_effect_enchants.append("Shadowflame Wreath")
        elif enchant == "Frozen Devotion":
            bonus_effect_enchants.append("Frozen Devotion")
        elif enchant == "Incandescent Essence":
            bonus_effect_enchants.append("Incandescent Essence")
            
    return stat_values_from_equipment, bonus_effect_enchants

def return_gem_stats(player, gems_from_equipment, stat_values_from_equipment):    
    for gem in gems_from_equipment:
        if gem == "Resplendent Illimited Diamond":
            stat_values_from_equipment["intellect"] += 75
            stat_values_from_equipment["versatility"] += 66
        elif gem == "Fierce Illimited Diamond":
            stat_values_from_equipment["intellect"] += 75
            stat_values_from_equipment["haste"] += 66
        elif gem == "Inscribed Illimited Diamond":
            stat_values_from_equipment["intellect"] += 75
            stat_values_from_equipment["crit"] += 66
        elif gem == "Skillful Illimited Diamond":
            stat_values_from_equipment["intellect"] += 75
            stat_values_from_equipment["mastery"] += 66
            
        elif gem == "Crafty Ysemerald":
            stat_values_from_equipment["haste"] += 70
            stat_values_from_equipment["crit"] += 33
        elif gem == "Energized Ysemerald":
            stat_values_from_equipment["haste"] += 70
            stat_values_from_equipment["versatility"] += 33
        elif gem == "Keen Ysemerald":
            stat_values_from_equipment["haste"] += 70
            stat_values_from_equipment["mastery"] += 33
        elif gem == "Quick Ysemerald":
            stat_values_from_equipment["haste"] += 88
            
        elif gem == "Keen Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["haste"] += 33
        elif gem == "Sensei's Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["crit"] += 33
        elif gem == "Zen Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["versatility"] += 33
        elif gem == "Fractured Neltharite":
            stat_values_from_equipment["mastery"] += 88
            
        elif gem == "Crafty Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["haste"] += 33
        elif gem == "Radiant Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["versatility"] += 33
        elif gem == "Sensei's Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["mastery"] += 33
        elif gem == "Deadly Alexstraszite":
            stat_values_from_equipment["crit"] += 88
            
        elif gem == "Energized Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["haste"] += 33
        elif gem == "Radiant Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["crit"] += 33
        elif gem == "Zen Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["mastery"] += 33
        elif gem == "Stormy Malygite":
            stat_values_from_equipment["versatility"] += 88
        
    return stat_values_from_equipment