stat_conversions = {
    "haste": 170,
    "crit": 180,
    "mastery": 120,
    "versatility": 205,
    "leech": 148
}

diminishing_returns_values = {
    "haste": [5100, 6800, 8500, 10200, 11900, 13600, 15300, 17000, 18700, 20400],
    "crit": [5400, 7200, 9000, 10800, 12600, 14400, 16200, 18000, 19800, 21600],
    "mastery": [5400, 7200, 9000, 10800, 12600, 14400, 16200, 18000, 19800, 21600],
    "versatility": [6150, 8200, 10250, 12300, 14350, 16400, 18450, 20500, 22550, 24600],
    "leech": [1480, 1480, 2220, 2220, 2960, 2960, 3700, 3700, 4440, 4440, 5180, 5180]
}

def calculate_stat_percent_with_dr(caster, stat, rating, flat_percent):
    dr_values = diminishing_returns_values[stat]
    remainder = 0
    current_range_index = 0
    
    for i in range(len(dr_values)):
        current_dr_value = dr_values[i]
        if rating - current_dr_value < 0:
            remainder = rating - dr_values[i - 1]
            current_range_index = i - 1
            break
    
    if rating >= dr_values[0]:
        rating_to_percent = dr_values[0] / stat_conversions[stat]
        
        for i in range(current_range_index):
            if i < 4:
                
                rating_to_percent += ((dr_values[1] - dr_values[0]) / stat_conversions[stat]) * (1 - ((i + 1) * 0.1))
            else:
                rating_to_percent += ((dr_values[1] - dr_values[0]) / stat_conversions[stat]) * (0.5)
        
        if current_range_index < 4:    
            rating_to_percent += (remainder / stat_conversions[stat]) * (1 - ((current_range_index + 1) * 0.1))
        else:
            rating_to_percent += (remainder / stat_conversions[stat]) * (0.6)
    else:
        rating_to_percent = rating / stat_conversions[stat]
    
    if stat == "mastery":
        if caster.is_talent_active("Seal of Might") and caster.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 1:
            rating_to_percent += 3
        elif caster.is_talent_active("Seal of Might") and caster.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 2:
            rating_to_percent += 6
    elif stat == "crit":
        if caster.is_talent_active("Holy Aegis") and caster.class_talents["row5"]["Holy Aegis"]["ranks"]["current rank"] == 1:
            rating_to_percent += 2
        elif caster.is_talent_active("Holy Aegis") and caster.class_talents["row5"]["Holy Aegis"]["ranks"]["current rank"] == 2:
            rating_to_percent += 4
    elif stat == "haste":
        if caster.is_talent_active("Seal of Alacrity") and caster.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 1:
            rating_to_percent = rating_to_percent * 1.02 + 2
        elif caster.is_talent_active("Seal of Alacrity") and caster.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 2:
            rating_to_percent = rating_to_percent * 1.04 + 4
            
    rating_to_percent += flat_percent
    
    return rating_to_percent

def update_stat_with_multiplicative_percentage(caster, stat, percentage, add_percentage=True):
    if add_percentage:
        if stat == "haste":
            caster.haste = (((caster.haste / 100 + 1) * (1 + percentage / 100)) - 1) * 100
            caster.haste_multiplier *= (1 + percentage / 100)
            caster.update_hasted_cooldowns_with_haste_changes()
        elif stat == "crit":
            caster.crit = (((caster.crit / 100 + 1) * (1 + percentage / 100)) - 1) * 100
            caster.crit_multiplier *= (1 + percentage / 100)
        elif stat == "mastery":
            caster.mastery = (((caster.mastery / 100 + 1) * (1 + percentage / 100)) - 1) * 100
            caster.mastery_multiplier *= (1 + percentage / 100)
        elif stat == "versatility":
            caster.versatility = (((caster.versatility / 100 + 1) * (1 + percentage / 100)) - 1) * 100
            caster.versatility_multiplier *= (1 + percentage / 100)
    else:
        if stat == "haste":
            caster.haste = (((caster.haste / 100 + 1) / (1 + percentage / 100)) - 1) * 100
            caster.haste_multiplier /= (1 + percentage / 100)
            caster.update_hasted_cooldowns_with_haste_changes()
        elif stat == "crit":
            caster.crit = (((caster.crit / 100 + 1) / (1 + percentage / 100)) - 1) * 100
            caster.crit_multiplier /= (1 + percentage / 100)
        elif stat == "mastery":
            caster.mastery = (((caster.mastery / 100 + 1) / (1 + percentage / 100)) - 1) * 100
            caster.mastery_multiplier /= (1 + percentage / 100)
        elif stat == "versatility":
            caster.versatility = (((caster.versatility / 100 + 1) / (1 + percentage / 100)) - 1) * 100
            caster.versatility_multiplier /= (1 + percentage / 100)