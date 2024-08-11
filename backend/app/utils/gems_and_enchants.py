import pprint

pp = pprint.PrettyPrinter(width=200)
        
def convert_enchants_to_stats(enchants_list):
    formatted_enchants = []
    
    for enchant in enchants_list:
        enchant_parts = enchant.split("|")

        if len(enchant_parts) > 1 and "Incandescent Essence" in enchant_parts[1]:
            formatted_enchants.append("Incandescent Essence")
            
        formatted_enchant = enchant_parts[0].split(": ")
        if len(formatted_enchant) == 1:
            formatted_enchant = formatted_enchant[0].strip()
        else:
            formatted_enchant = formatted_enchant[1].strip()
        formatted_enchants.append(formatted_enchant)
        
    return formatted_enchants

def return_enchants_stats(player, formatted_enchants, bonus_effect_enchants, stat_values_from_equipment):
    mana_enchant_count = 0
    
    for enchant in formatted_enchants:
        if enchant == "Waking Stats":
            stat_values_from_equipment["intellect"] += 150
        elif enchant == "Reserve of Intellect":
            stat_values_from_equipment["intellect"] += 111
            mana_enchant_count += 1
        elif enchant == "Crystalline Radiance":
            stat_values_from_equipment["intellect"] += 745
        elif enchant == "Council's Intellect":
            stat_values_from_equipment["intellect"] += 630
            mana_enchant_count += 1
        elif enchant == "+177 Intellect & +5% Mana":
            stat_values_from_equipment["intellect"] += 177
            mana_enchant_count += 1
        elif enchant == "+177 Intellect & 131 Stamina":
            stat_values_from_equipment["intellect"] += 177
            stat_values_from_equipment["stamina"] += 131
        elif enchant == "Daybreak Spellthread":
            stat_values_from_equipment["intellect"] += 340
            mana_enchant_count += 1
        elif enchant == "Sunset Spellthread":
            stat_values_from_equipment["intellect"] += 340
            stat_values_from_equipment["stamina"] += 92
        elif enchant == "Weavercloth Spellthread":
            stat_values_from_equipment["intellect"] += 249
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
        elif enchant == "Chant of Leeching Fangs":
            stat_values_from_equipment["leech"] += 1020
        elif enchant == "+200 Leech":
            stat_values_from_equipment["leech"] += 200
        elif enchant == "Chant of Armored Leech":
            stat_values_from_equipment["leech"] += 2040
        elif enchant == "Watcher's Loam":
            stat_values_from_equipment["stamina"] += 131
        elif enchant == "Defender's March":
            stat_values_from_equipment["stamina"] += 131
        elif enchant == "Shadowed Belt Clasp":
            stat_values_from_equipment["stamina"] += 106
        elif enchant == "Radiant Haste":
            stat_values_from_equipment["haste"] += 315
        elif enchant == "Radiant Critical Strike":
            stat_values_from_equipment["crit"] += 315
        elif enchant == "Radiant Versatility":
            stat_values_from_equipment["versatility"] += 315
        elif enchant == "Radiant Mastery":
            stat_values_from_equipment["mastery"] += 315
        elif enchant == "Cursed Haste":
            stat_values_from_equipment["haste"] += 390
            stat_values_from_equipment["versatility"] -= 115
        elif enchant == "Cursed Critical Strike":
            stat_values_from_equipment["crit"] += 390
            stat_values_from_equipment["haste"] -= 115
        elif enchant == "Cursed Versatility":
            stat_values_from_equipment["versatility"] += 390
            stat_values_from_equipment["mastery"] -= 115
        elif enchant == "Cursed Mastery":
            stat_values_from_equipment["mastery"] += 390
            stat_values_from_equipment["crit"] -= 115
        
            
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
        elif enchant == "Authority of Fiery Resolve":
            bonus_effect_enchants.append("Authority of Fiery Resolve")
        elif enchant == "Authority of Radiant Power":
            bonus_effect_enchants.append("Authority of Radiant Power")
        elif enchant == "Oathsworn's Tenacity":
            bonus_effect_enchants.append("Oathsworn's Tenacity")
        elif enchant == "Stonebound Artistry":
            bonus_effect_enchants.append("Stonebound Artistry")
        elif enchant == "Stormrider's Fury":
            bonus_effect_enchants.append("Stormrider's Fury")
        elif enchant == "Council's Guile":
            bonus_effect_enchants.append("Council's Guile")
           
    if mana_enchant_count > 0: 
        player.max_mana = player.base_mana + player.base_mana * mana_enchant_count * 0.05
        player.mana = player.base_mana + player.base_mana * mana_enchant_count * 0.05
            
    return stat_values_from_equipment, bonus_effect_enchants

def return_gem_stats(player, gems_from_equipment, stat_values_from_equipment):   
    player.gem_counts = {
        "Ysemerald": 0,
        "Alexstraszite": 0,
        "Neltharite": 0,
        "Malygite": 0,
        "Emerald": 0,
        "Sapphire": 0,
        "Ruby": 0,
        "Onyx": 0,
    }
    
    player.gem_types = {
        "Fire": 0,
        "Frost": 0,
        "Air": 0,
        "Earth": 0
    }
    
    player.total_elemental_gems = 0
    
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
            player.gem_counts["Ysemerald"] += 1
            player.gem_types["Fire"] += 1
            player.total_elemental_gems += 1
        elif gem == "Energized Ysemerald":
            stat_values_from_equipment["haste"] += 70
            stat_values_from_equipment["versatility"] += 33
            player.gem_counts["Ysemerald"] += 1
            player.gem_types["Frost"] += 1
            player.total_elemental_gems += 1
        elif gem == "Keen Ysemerald":
            stat_values_from_equipment["haste"] += 70
            stat_values_from_equipment["mastery"] += 33
            player.gem_counts["Ysemerald"] += 1
            player.gem_types["Earth"] += 1
            player.total_elemental_gems += 1
        elif gem == "Quick Ysemerald":
            stat_values_from_equipment["haste"] += 88
            player.gem_counts["Ysemerald"] += 1
            player.gem_types["Air"] += 1
            player.total_elemental_gems += 1
            
        elif gem == "Keen Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["haste"] += 33
            player.gem_counts["Neltharite"] += 1
            player.gem_types["Air"] += 1
            player.total_elemental_gems += 1
        elif gem == "Sensei's Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["crit"] += 33
            player.gem_counts["Neltharite"] += 1
            player.gem_types["Fire"] += 1
            player.total_elemental_gems += 1
        elif gem == "Zen Neltharite":
            stat_values_from_equipment["mastery"] += 70
            stat_values_from_equipment["versatility"] += 33
            player.gem_counts["Neltharite"] += 1
            player.gem_types["Frost"] += 1
            player.total_elemental_gems += 1
        elif gem == "Fractured Neltharite":
            stat_values_from_equipment["mastery"] += 88
            player.gem_counts["Neltharite"] += 1
            player.gem_types["Earth"] += 1
            player.total_elemental_gems += 1
            
        elif gem == "Crafty Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["haste"] += 33
            player.gem_counts["Alexstraszite"] += 1
            player.gem_types["Air"] += 1
            player.total_elemental_gems += 1
        elif gem == "Radiant Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["versatility"] += 33
            player.gem_counts["Alexstraszite"] += 1
            player.gem_types["Frost"] += 1
            player.total_elemental_gems += 1
        elif gem == "Sensei's Alexstraszite":
            stat_values_from_equipment["crit"] += 70
            stat_values_from_equipment["mastery"] += 33
            player.gem_counts["Alexstraszite"] += 1
            player.gem_types["Earth"] += 1
            player.total_elemental_gems += 1
        elif gem == "Deadly Alexstraszite":
            stat_values_from_equipment["crit"] += 88
            player.gem_counts["Alexstraszite"] += 1
            player.gem_types["Fire"] += 1
            player.total_elemental_gems += 1
            
        elif gem == "Energized Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["haste"] += 33
            player.gem_counts["Malygite"] += 1
            player.gem_types["Air"] += 1
            player.total_elemental_gems += 1
        elif gem == "Radiant Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["crit"] += 33
            player.gem_counts["Malygite"] += 1
            player.gem_types["Fire"] += 1
            player.total_elemental_gems += 1
        elif gem == "Zen Malygite":
            stat_values_from_equipment["versatility"] += 70
            stat_values_from_equipment["mastery"] += 33
            player.gem_counts["Malygite"] += 1
            player.gem_types["Earth"] += 1
            player.total_elemental_gems += 1
        elif gem == "Stormy Malygite":
            stat_values_from_equipment["versatility"] += 88
            player.gem_counts["Malygite"] += 1
            player.gem_types["Frost"] += 1
            player.total_elemental_gems += 1
            
        # ptr
        elif gem == "Deadly Emerald":
            stat_values_from_equipment["haste"] += 147
            stat_values_from_equipment["crit"] += 49
            player.gem_counts["Emerald"] += 1
        elif gem == "Versatile Emerald":
            stat_values_from_equipment["haste"] += 147
            stat_values_from_equipment["versatility"] += 49
            player.gem_counts["Emerald"] += 1
        elif gem == "Masterful Emerald":
            stat_values_from_equipment["haste"] += 147
            stat_values_from_equipment["mastery"] += 49
            player.gem_counts["Emerald"] += 1
        elif gem == "Quick Emerald":
            stat_values_from_equipment["haste"] += 176
            player.gem_counts["Emerald"] += 1
            
        elif gem == "Deadly Ruby":
            stat_values_from_equipment["crit"] += 176
            player.gem_counts["Ruby"] += 1
        elif gem == "Versatile Ruby":
            stat_values_from_equipment["crit"] += 147
            stat_values_from_equipment["versatility"] += 49
            player.gem_counts["Ruby"] += 1
        elif gem == "Masterful Ruby":
            stat_values_from_equipment["crit"] += 147
            stat_values_from_equipment["mastery"] += 49
            player.gem_counts["Ruby"] += 1
        elif gem == "Quick Ruby":
            stat_values_from_equipment["crit"] += 147
            stat_values_from_equipment["haste"] += 49
            player.gem_counts["Ruby"] += 1
            
        elif gem == "Deadly Onyx":
            stat_values_from_equipment["mastery"] += 147
            stat_values_from_equipment["crit"] += 49
            player.gem_counts["Onyx"] += 1
        elif gem == "Versatile Onyx":
            stat_values_from_equipment["mastery"] += 147
            stat_values_from_equipment["versatility"] += 49
            player.gem_counts["Onyx"] += 1
        elif gem == "Masterful Onyx":
            stat_values_from_equipment["mastery"] += 176
            player.gem_counts["Onyx"] += 1
        elif gem == "Quick Onyx":
            stat_values_from_equipment["mastery"] += 147
            stat_values_from_equipment["haste"] += 49
            player.gem_counts["Onyx"] += 1
            
        elif gem == "Deadly Sapphire":
            stat_values_from_equipment["versatility"] += 147
            stat_values_from_equipment["crit"] += 49
            player.gem_counts["Sapphire"] += 1
        elif gem == "Versatile Sapphire":
            stat_values_from_equipment["versatility"] += 176
            player.gem_counts["Sapphire"] += 1
        elif gem == "Masterful Sapphire":
            stat_values_from_equipment["versatility"] += 147
            stat_values_from_equipment["mastery"] += 49
            player.gem_counts["Sapphire"] += 1
        elif gem == "Quick Sapphire":
            stat_values_from_equipment["versatility"] += 147
            stat_values_from_equipment["haste"] += 49
            player.gem_counts["Sapphire"] += 1
        
        elif gem == "Cubic Blasphemite":
            stat_values_from_equipment["intellect"] += 181
        elif gem == "Elusive Blasphemite":
            stat_values_from_equipment["intellect"] += 181
        elif gem == "Insightful Blasphemite":
            stat_values_from_equipment["intellect"] += 181
        elif gem == "Culminating Blasphemite":
            stat_values_from_equipment["intellect"] += 181 
      
    unique_gem_colours = sum(1 for gem in ["Emerald", "Sapphire", "Onyx", "Ruby"] if player.gem_counts[gem] > 0)  
            
    if "Insightful Blasphemite" in gems_from_equipment:
        player.max_mana = player.mana + player.base_mana * unique_gem_colours * 0.01
        player.mana = player.max_mana
        
    if "Culminating Blasphemite" in gems_from_equipment:
        player.crit_healing_modifier += unique_gem_colours * 0.0015
        player.base_crit_healing_modifier += unique_gem_colours * 0.0015
        
    # print(stat_values_from_equipment)
    # print(player.gem_counts)
        
    return stat_values_from_equipment