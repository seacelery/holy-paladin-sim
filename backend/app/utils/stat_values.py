live_stat_conversions = {
    "haste": 660,
    "crit": 700,
    "mastery": 466.67,
    "versatility": 780,
    "leech": 1000
}

live_diminishing_returns_values = {
    "haste": [19800, 26400, 33000, 39600, 46200, 52800, 59400, 66000, 72600, 79200],
    "crit": [21000, 28000, 35000, 42000, 49000, 56000, 63000, 70000, 77000, 84000],
    "mastery": [21000, 28000, 35000, 42000, 49000, 56000, 63000, 70000, 77000, 84000],
    "versatility": [23400, 31200, 39000, 46800, 54600, 62400, 70200, 78000, 85800, 93600],
    "leech": [(live_stat_conversions["leech"] / 100) * i for i in range(1, 3000)]
}

ptr_stat_conversions = {
    "haste": 660,
    "crit": 700,
    "mastery": 466.67,
    "versatility": 780,
    "leech": 1000
}

ptr_diminishing_returns_values = {
    "haste": [19800, 26400, 33000, 39600, 46200, 52800, 59400, 66000, 72600, 79200],
    "crit": [21000, 28000, 35000, 42000, 49000, 56000, 63000, 70000, 77000, 84000],
    "mastery": [21000, 28000, 35000, 42000, 49000, 56000, 63000, 70000, 77000, 84000],
    "versatility": [23400, 31200, 39000, 46800, 54600, 62400, 70200, 78000, 85800, 93600],
    "leech": [(ptr_stat_conversions["leech"] / 100) * i for i in range(1, 3000)]
}

def calculate_stat_percent_with_dr(caster, stat, rating, flat_percent):
    if caster.ptr:
        stat_conversions = ptr_stat_conversions
        diminishing_returns_values = ptr_diminishing_returns_values
    else:
        stat_conversions = live_stat_conversions
        diminishing_returns_values = live_diminishing_returns_values
    
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
    
    if stat == "haste":
        rating_to_percent = (((1 + rating_to_percent / 100) * caster.multiplicative_haste) - 1) * 100  
    rating_to_percent += flat_percent
    
    return rating_to_percent

def calculate_leech_percent_with_dr(caster, stat, rating, flat_percent):
    if caster.ptr:
        stat_conversions = ptr_stat_conversions
        diminishing_returns_values = ptr_diminishing_returns_values
    else:
        stat_conversions = live_stat_conversions
        diminishing_returns_values = live_diminishing_returns_values
    
    dr_values = diminishing_returns_values["leech"]
    remainder = 0
    current_range_index = 0
    
    for i in range(len(dr_values)):
        current_dr_value = dr_values[i]
        if rating - current_dr_value < 0:
            remainder = rating - dr_values[i - 1]
            current_range_index = i - 1
            break
    
    if rating >= dr_values[0]:
        rating_to_percent = dr_values[0] / stat_conversions["leech"]
        
        for i in range(current_range_index):
            rating_to_percent += ((dr_values[1] - dr_values[0]) / stat_conversions["leech"]) * (1 - ((i + 1) * 0.00015))
        
        rating_to_percent += (remainder / stat_conversions["leech"]) * (1 - ((current_range_index + 1) * 0.00015))
    else:
        rating_to_percent = rating / stat_conversions["leech"]
            
    rating_to_percent += flat_percent
    
    return rating_to_percent

def update_stat_with_multiplicative_percentage(caster, stat, percentage, add_percentage=True):
    if add_percentage:
        if stat == "haste":
            caster.haste = (((caster.haste / 100 + 1) * (1 + percentage / 100)) - 1) * 100
            caster.haste_multiplier *= (1 + percentage / 100)
            caster.multiplicative_haste *= (1 + percentage / 100)
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
            caster.multiplicative_haste /= (1 + percentage / 100)
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