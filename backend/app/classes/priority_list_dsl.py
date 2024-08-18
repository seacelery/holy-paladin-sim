import re

def parse_condition(condition_str):
    parts = condition_str.split("|")
    if len(parts) == 1:
        parts.append("No condition")
    action_name = parts[0].strip()

    all_conditions = []
    current_group = []

    for i, part in enumerate(parts[1:]):
        part = part.strip()
        
        # "and" is skipped
        if part.lower() == "and":
            continue
        
        # "or" finishes the current group and starts a new one, then skips to the next condition
        if part.lower() == "or":
            if current_group:
                all_conditions.append(current_group)
            current_group = []
            continue

        condition = {"keyword": "", "extra_condition": "", "value": 0, "first_value": 0, "second_value": 0, "time_values": [], "operator": "", "multiple_comparisons": False}
        
        if re.search(r"[Tt]imers\s+=\s+\[\d+(?:\.\d+)?(?:\s*,\s*\d+(?:\.\d+)?)*\][+]", part):
            pattern = r"\b\d+(?:\.\d+)?\b"
            matches = re.findall(pattern, part)
            condition["time_values"] = [float(match) for match in matches]
            condition["keyword"] = "timers+"
        elif re.search(r"[Tt]imers\s+=\s+\[\d+(?:\.\d+)?(?:\s*,\s*\d+(?:\.\d+)?)*", part):
            pattern = r"\b\d+(?:\.\d+)?\b"
            matches = re.findall(pattern, part)
            condition["time_values"] = [float(match) for match in matches]
            condition["keyword"] = "timers"
        
        if re.search(r"\d+(\.\d+)?%?\s+[><=!]+\s+[\w\s]+[><=!]+\s+\d+(\.\d+)?%?", part) or re.search(r"(\d+(\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(\.\d+)?)\s*([><=!]+)\s*([\w\s]+)?\s+([cC]ooldown|[dD]uration|[tT]ime)\s*([><=!]+)\s*(\d+(\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(\.\d+)?)", part):
            condition["multiple_comparisons"] = True
                
            if "stacks " in part:
                pattern = r"(\d+)\s+([><=!]+)\s+(.*?)\s+[sS]tacks\s+([><=!]+)\s+(\d+)"
                match = re.match(pattern, part)
                condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                condition["keyword"] = "stacks"
                
            elif "duration " in part:
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)\s*([><=!]+)\s*([\w\s]+)\s+[dD]uration\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "duration"
                else:
                    pattern = r"(\d+(?:\.\d+)?|[gG][cC][dD])\s+([><=!]+)\s+(.*?)\s+[dD]uration\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "duration"
                
            elif "cooldown " in part:
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)\s*([><=!]+)\s*([\w\s]+)\s+[cC]ooldown\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "cooldown"
                else:
                    pattern = r"(\d+(?:\.\d+)?|[gG][cC][dD])\s+([><=!]+)\s+(.*?)\s+[cC]ooldown\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "cooldown"
                    
            elif "charges " in part:
                pattern = r"(\d+)\s+([><=!]+)\s+(.*?)\s+[cC]harges\s+([><=!]+)\s+(\d+)"
                match = re.match(pattern, part)
                condition["first_value"], condition["first_operator"], condition["name"], condition["second_operator"], condition["second_value"] = match.groups()
                condition["keyword"] = "charges"
                
            elif "Mana " in part or "mana " in part:
                pattern = r"(\d+(?:\.\d+)?%?)\s+([><=!]+)\s+[mM]ana\s+([><=!]+)\s+(\d+(?:\.\d+)?%?)"
                match = re.match(pattern, part)
                condition["first_value"], condition["first_operator"], condition["second_operator"], condition["second_value"] = match.groups()
                condition["keyword"] = "mana"
                
            elif "Holy Power " in part or "holy power " in part or "Holy power " in part:
                pattern = r"(\d+(?:\.\d+)?)\s+([><=!]+)\s+[hH]oly\s[pP]ower\s+([><=!]+)\s+(\d+(?:\.\d+)?)"
                match = re.match(pattern, part)
                condition["first_value"], condition["first_operator"], condition["second_operator"], condition["second_value"] = match.groups()
                condition["keyword"] = "holy power"
                
            elif "Time " in part or "time " in part:              
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)\s*([><=!]+)\s*[tT]ime\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD]|\d+(?:\.\d+)?)"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["first_value"], condition["first_operator"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "time"
                else:
                    pattern = r"(\d+(?:\.\d+)?|[gG][cC][dD])\s+([><=!]+)\s+[tT]ime\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["first_value"], condition["first_operator"], condition["second_operator"], condition["second_value"] = match.groups()
                    condition["keyword"] = "time"
                
            elif "Fight length " in part or "fight length " in part or "Fight Length " in part:
                pattern = r"(\d+(?:\.\d+)?)\s+([><=!]+)\s+Fight\s[lL]ength\s+([><=!]+)\s+(\d+(?:\.\d+)?)"
                match = re.match(pattern, part)
                condition["first_value"], condition["first_operator"], condition["second_operator"], condition["second_value"] = match.groups()
                condition["keyword"] = "fight length"
   
        else:
            if " inactive" in part:
                condition["keyword"] = "inactive"
                condition["name"] = part.rsplit(" ", 1)[0]
                
            elif " not active" in part:
                condition["keyword"] = "inactive"
                condition["name"] = part.rsplit(" ", 2)[0]
                
            elif " active" in part:
                condition["keyword"] = "active"
                condition["name"] = part.rsplit(" ", 1)[0]
                
            elif " not talented" in part:
                condition["keyword"] = "not talented"
                condition["name"] = part.rsplit(" ", 2)[0]
                
            elif " talented" in part:
                condition["keyword"] = "talented"
                condition["name"] = part.rsplit(" ", 1)[0]
                
            elif "stacks " in part:
                part_split = part.rsplit(" ", 3)
                condition["name"] = part_split[0]
                condition["keyword"] = part_split[1]
                condition["operator"] = part_split[2]
                condition["value"] = part_split[3]
                
            elif "duration " in part:
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"([\w\s]+)\s+[dD]uration\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD])"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["name"], condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "duration"
                else:
                    pattern = r"(.*?)\s+[dD]uration\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["name"], condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "duration"
                
            elif "cooldown " in part:
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"([\w\s]+)\s+[cC]ooldown\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD])"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["name"], condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "cooldown"
                else:
                    pattern = r"(.*?)\s+[cC]ooldown\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["name"], condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "cooldown"
                    
            elif "charges " in part:
                part_split = part.rsplit(" ", 3)
                condition["name"] = part_split[0]
                condition["keyword"] = part_split[1]
                condition["operator"] = part_split[2]
                condition["value"] = part_split[3]
                
            elif "Mana " in part or "mana " in part:
                part_split = part.split(" ")
                condition["keyword"] = part_split[0]
                condition["operator"] = part_split[1]
                condition["value"] = part_split[2]
                
            elif "Holy Power " in part or "holy power " in part or "Holy power " in part:
                part_split = part.split(" ")
                condition["keyword"] = " ".join(part_split[0:2])
                condition["operator"] = part_split[2]
                condition["value"] = part_split[3]
                            
            elif "Race " in part or "race " in part:
                part_split = part.split(" ")
                condition["keyword"] = part_split[0]
                condition["operator"] = part_split[1]
                condition["value"] = " ".join(part_split[2:])
                
            elif "Overhealing " in part or "overhealing " in part:
                part_split = part.rsplit(" ", 3)
                condition["name"] = part_split[0]
                condition["keyword"] = part_split[1]
                condition["operator"] = part_split[2]
                condition["value"] = part_split[3]
                
            elif "Time " in part or "time " in part:
                if re.search(r"gcd", part) and any(op in part for op in ["*", "+"]):
                    pattern = r"[tT]ime\s*([><=!]+)\s*(\d+(?:\.\d+)?\s*[*+]\s*[gG][cC][dD]|[gG][cC][dD])"
                    match = re.match(pattern, part, flags=re.IGNORECASE)
                    condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "time"
                else:
                    pattern = r"[tT]ime\s+([><=!]+)\s+(\d+(?:\.\d+)?|[gG][cC][dD])"
                    match = re.match(pattern, part)
                    condition["operator"], condition["value"] = match.groups()
                    condition["keyword"] = "time"
                
            elif "Fight length " in part or "fight length " in part or "Fight Length " in part:
                part_split = part.split(" ")
                condition["keyword"] = " ".join(part_split[0:2])
                condition["operator"] = part_split[2]
                condition["value"] = part_split[3]
                
            elif "Previous Ability" in part or "previous ability" in part or "Previous ability" in part:
                part_split = part.split(" ")
                condition["keyword"] = " ".join(part_split[0:2])
                condition["operator"] = part_split[2]
                condition["value"] = " ".join(part_split[3:])
                
        if "Potion" in action_name:
            condition["extra_condition"] = "potion"
            
        current_group.append(condition)

        if i + 2 >= len(parts) or parts[i + 2].strip().lower() not in ["and", "or"]:
            all_conditions.append(current_group)
            current_group = []

    # append final group
    if current_group:
        all_conditions.append(current_group)

    return action_name, all_conditions

def condition_to_lambda(sim_instance, all_conditions):
    def lambda_func():
        for group in all_conditions:
            group_result = True
            
            for condition in group:
                result = False
                    
                if "gcd" in str(condition["value"]).lower():
                    operator = re.search(r"[\+\-\*/]", str(condition["value"])).group() if re.search(r"[\+\-\*/]", str(condition["value"])) else "*"
                    operator_value = float(re.search(r"\d+", str(condition["value"])).group()) if re.search(r"\d+(?:\.\d+)?", str(condition["value"])) else 1
                    gcd_value = sim_instance.paladin.global_cooldown
                    value = evaluate_gcd(gcd_value, operator_value, operator)
                    condition["value"] = value
                    
                if "gcd" in str(condition["first_value"]).lower():
                    operator = re.search(r"[\+\-\*/]", str(condition["first_value"])).group() if re.search(r"[\+\-\*/]", str(condition["first_value"])) else "*"
                    operator_value = float(re.search(r"\d+", str(condition["first_value"])).group()) if re.search(r"\d+(?:\.\d+)?", str(condition["first_value"])) else 1
                    gcd_value = sim_instance.paladin.global_cooldown
                    value = evaluate_gcd(gcd_value, operator_value, operator)
                    condition["first_value"] = value
                    
                if "gcd" in str(condition["second_value"]).lower():
                    operator = re.search(r"[\+\-\*/]", str(condition["second_value"])).group() if re.search(r"[\+\-\*/]", str(condition["second_value"])) else "*"
                    operator_value = float(re.search(r"\d+", str(condition["second_value"])).group()) if re.search(r"\d+(?:\.\d+)?", str(condition["second_value"])) else 1
                    gcd_value = sim_instance.paladin.global_cooldown
                    value = evaluate_gcd(gcd_value, operator_value, operator)
                    condition["second_value"] = value
                
                if condition["keyword"].lower() == "timers":
                    result = False
                    for timer in condition["time_values"]:
                        result = compare_value_plus_gcds(timer, sim_instance.elapsed_time, sim_instance.paladin.hasted_global_cooldown)
                        if result:
                            break
                        
                elif condition["keyword"].lower() == "timers+":
                    result = False
                    for timer in condition["time_values"]:
                        if sim_instance.elapsed_time > timer + 3:
                            result = True
                        else:
                            result = compare_value_plus_gcds(timer, sim_instance.elapsed_time, sim_instance.paladin.hasted_global_cooldown)
                        if result:
                            break
                
                elif condition["keyword"].lower() == "active":
                    if condition["name"] in ["Beacon of Virtue", "Beacon of Faith"]:
                        condition["name"] = "Beacon of Light"
                    
                    in_target_buffs = False
                    for target in sim_instance.paladin.potential_healing_targets:
                        if condition["name"] in target.target_active_buffs:
                            in_target_buffs = True
                    result = condition["name"] in sim_instance.paladin.active_auras or in_target_buffs
                    
                elif condition["keyword"].lower() == "inactive":
                    if condition["name"] in ["Beacon of Virtue", "Beacon of Faith"]:
                        condition["name"] = "Beacon of Light"
                    
                    in_target_buffs = False
                    for target in sim_instance.paladin.potential_healing_targets:
                        if condition["name"] in target.target_active_buffs:
                            in_target_buffs = True
                    result = condition["name"] not in sim_instance.paladin.active_auras and not in_target_buffs
                    
                elif condition["keyword"].lower() == "talented":
                    talented = False
                    if sim_instance.paladin.is_talent_active(condition["name"]):
                        talented = True
                    result = talented
                    
                elif condition["keyword"].lower() == "not talented":
                    talented = False
                    if not sim_instance.paladin.is_talent_active(condition["name"]):
                        talented = True
                    result = talented
                    
                elif condition["keyword"].lower() == "mana":
                    mana = sim_instance.paladin.mana                 
                    if condition["multiple_comparisons"]:
                        value1 = (float(condition["first_value"].replace("%", "")) / 100) * sim_instance.paladin.max_mana if "%" in condition["first_value"] else float(condition["first_value"])
                        value2 = (float(condition["second_value"].replace("%", "")) / 100) * sim_instance.paladin.max_mana if "%" in condition["second_value"] else float(condition["second_value"])
                        result = compare_two_values(mana, value1, value2, condition["first_operator"], condition["second_operator"])
                    else:
                        value = (float(condition["value"].replace("%", "")) / 100) * sim_instance.paladin.max_mana if "%" in condition["value"] else float(condition["value"])
                        result = compare_single_value(mana, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "holy power":
                    holy_power = sim_instance.paladin.holy_power
                    if condition["multiple_comparisons"]:
                        result = compare_two_values(holy_power, float(condition["first_value"]), float(condition["second_value"]), condition["first_operator"], condition["second_operator"])
                    else:                      
                        value = int(condition["value"])
                        result = compare_single_value(holy_power, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "race":
                    race = sim_instance.paladin.race
                    result = race == condition["value"]
                    
                elif condition["keyword"].lower() == "previous ability":
                    previous_ability = sim_instance.previous_ability
                    result = previous_ability == condition["value"]
                    
                elif condition["keyword"].lower() == "stacks":    
                    if condition["name"] in sim_instance.paladin.active_auras:
                        stacks = sim_instance.paladin.active_auras[condition["name"]].current_stacks                    
                        if condition["multiple_comparisons"]:
                            result = compare_two_values(stacks, float(condition["first_value"]), float(condition["second_value"]), condition["first_operator"], condition["second_operator"])
                        else:                          
                            value = int(condition["value"])
                            result = compare_single_value(stacks, condition["operator"], value)
                        
                elif condition["keyword"].lower() == "duration":
                    if condition["name"] in sim_instance.paladin.active_auras:
                        duration = sim_instance.paladin.active_auras[condition["name"]].duration
                        if condition["multiple_comparisons"]:                        
                            result = compare_two_values(duration, float(condition["first_value"]), float(condition["second_value"]), condition["first_operator"], condition["second_operator"])
                        else:
                            value = float(condition["value"])
                            result = compare_single_value(duration, condition["operator"], value)
                                  
                elif condition["keyword"].lower() == "charges":
                    if condition["multiple_comparisons"]:
                        charges = sim_instance.paladin.abilities[condition["name"]].current_charges
                        result = compare_two_values(charges, float(condition["first_value"]), float(condition["second_value"]), condition["first_operator"], condition["second_operator"])
                    else:
                        charges = sim_instance.paladin.abilities[condition["name"]].current_charges
                        value = int(condition["value"])
                        result = compare_single_value(charges, condition["operator"], value)
                        
                elif condition["keyword"].lower() == "overhealing":
                    overhealing = sim_instance.overhealing[condition["name"]] * 100
                    value = float(condition["value"].replace("%", ""))
                    result = compare_single_value(overhealing, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "cooldown":
                    cooldown = sim_instance.paladin.abilities[condition["name"]].remaining_cooldown
                    if condition["multiple_comparisons"]:
                        result = compare_two_values(cooldown, float(condition["first_value"]), float(condition["second_value"]), condition["first_operator"], condition["second_operator"])
                    else:
                        value = float(condition["value"])
                        result = compare_single_value(cooldown, condition["operator"], value)
                      
                elif condition["keyword"].lower() == "time":
                    time = sim_instance.elapsed_time
                    if condition["multiple_comparisons"]:
                        value1 = float(condition["first_value"])
                        value2 = float(condition["second_value"])
                        result = compare_two_values(time, value1, value2, condition["first_operator"], condition["second_operator"])
                    else:
                        value = float(condition["value"])
                        result = compare_single_value(time, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "fight length":
                    fight_length = sim_instance.encounter_length
                    if condition["multiple_comparisons"]:                        
                        value1 = float(condition["first_value"])
                        value2 = float(condition["second_value"])
                        result = compare_two_values(fight_length, value1, value2, condition["first_operator"], condition["second_operator"])
                    else:
                        value = float(condition["value"])
                        result = compare_single_value(fight_length, condition["operator"], value)
                         
                else:
                    result = True
                
                # extra conditions
                if condition["extra_condition"] == "potion":
                    result = result and sim_instance.paladin.abilities["Potion"].check_potion_cooldown(sim_instance.paladin, sim_instance.elapsed_time)

                # if any condition's result is false, the whole group"s result is false
                if not result:
                    group_result = False
                    break

            # print(group_result)
            # if the group's result is true, the whole thing is true
            if group_result:
                return True

        return False

    return lambda_func

def compare_value_plus_gcds(value, current_time, gcd_value):
    return value <= current_time <= value + gcd_value * 10
    
def evaluate_gcd(gcd_value, operator_value, operator):
    if operator == "*":
        return operator_value * gcd_value
    elif operator == "+":
        return operator_value + gcd_value
 
def compare_two_values(property_value, value1, value2, operator1, operator2):
    if operator1 == "<" and operator2 == "<":
        return value1 < property_value < value2
    if operator1 == "<=" and operator2 == "<":
        return value1 <= property_value < value2
    if operator1 == "<" and operator2 == "<=":
        return value1 < property_value <= value2
    if operator1 == "<=" and operator2 == "<=":
        return value1 <= property_value <= value2
    
def compare_single_value(property_value, operator, value):
    if operator == "<":
        return property_value < value
    elif operator == "<=":
        return property_value <= value
    elif operator == "=":
        return property_value == value
    elif operator == "!=":
        return property_value != value
    elif operator == ">":
        return property_value > value
    elif operator == ">=":
        return property_value >= value
    return False   