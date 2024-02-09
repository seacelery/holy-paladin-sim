def parse_condition(condition_str):
    parts = condition_str.split("|")
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

        condition = {"keyword": "", "extra_condition": ""}
        
        # print("part", part)

        if " inactive" in part:
            condition["keyword"] = "inactive"
            condition["name"] = part.rsplit(" ", 1)[0]
            
        elif " not active" in part:
            condition["keyword"] = "inactive"
            condition["name"] = part.rsplit(" ", 2)[0]
            
        elif " active" in part:
            condition["keyword"] = "active"
            condition["name"] = part.rsplit(" ", 1)[0]
            
        elif "stacks " in part:
            print("a")
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "duration " in part:
            print("b")
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "cooldown " in part:
            print("awawaw")
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]     
            condition["keyword"] = part_split[1]    
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
                
        elif "charges " in part:
            print("c")
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "Mana " in part or "mana " in part:
            print("d")
            part_split = part.split(" ")
            condition["keyword"] = part_split[0]
            condition["operator"] = part_split[1]
            condition["value"] = part_split[2]
            
        elif "Holy Power " in part or "holy power " in part:
            print("d")
            part_split = part.split(" ")
            condition["keyword"] = " ".join(part_split[0:2])
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
                        
        elif "Race " in part or "race " in part:
            print("e")
            part_split = part.split(" ")
            condition["keyword"] = part_split[0]
            condition["operator"] = part_split[1]
            condition["value"] = " ".join(part_split[2:])
            
        elif "Time " in part or "time " in part:
            print("f")
            part_split = part.split(" ")
            condition["keyword"] = part_split[0]
            condition["operator"] = part_split[1]
            condition["value"] = " ".join(part_split[2:])
            
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
                # print(condition["keyword"])
                
                if condition["keyword"] == "active":
                    result = condition["name"] in sim_instance.paladin.active_auras
                    
                elif condition["keyword"] == "inactive":
                    result = condition["name"] not in sim_instance.paladin.active_auras
                    print(condition, result)
                    
                elif condition["keyword"].lower() == "mana":
                    mana = sim_instance.paladin.mana
                    value = (float(condition["value"].replace("%", "")) / 100) * sim_instance.paladin.max_mana if "%" in condition["value"] else float(condition["value"])
                    result = compare_values(mana, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "holy power":
                    holy_power = sim_instance.paladin.holy_power
                    value = int(condition["value"])
                    result = compare_values(holy_power, condition["operator"], value)
                    
                elif condition["keyword"].lower() == "race":
                    race = sim_instance.paladin.race
                    result = race == condition["value"]
                    
                elif condition["keyword"] == "stacks":
                    if condition["name"] in sim_instance.paladin.active_auras:
                        stacks = sim_instance.paladin.active_auras[condition["name"]].current_stacks
                        value = float(condition["value"])
                        result = compare_values(stacks, condition["operator"], value)
                        
                elif condition["keyword"] == "duration":
                    if condition["name"] in sim_instance.paladin.active_auras:
                        duration = sim_instance.paladin.active_auras[condition["name"]].duration
                        value = float(condition["value"])
                        result = compare_values(duration, condition["operator"], value)
                        
                elif condition["keyword"] == "charges":
                    charges = sim_instance.paladin.abilities[condition["name"]].current_charges
                    value = int(condition["value"])
                    result = compare_values(charges, condition["operator"], value)
                    
                elif condition["keyword"] == "cooldown":
                    cooldown = sim_instance.paladin.abilities[condition["name"]].remaining_cooldown
                    value = float(condition["value"])
                    result = compare_values(cooldown, condition["operator"], value)
                      
                elif condition["keyword"].lower() == "time":
                    time = sim_instance.elapsed_time
                    value = float(condition["value"])
                    result = compare_values(time, condition["operator"], value)
                         
                else:
                    result = True
                
                # extra conditions
                if condition["extra_condition"] == "potion":
                    result = result and sim_instance.paladin.abilities["Potion"].check_potion_cooldown(sim_instance.elapsed_time)

                # if any condition's result is false, the whole group's result is false
                if not result:
                    group_result = False
                    break

            # if the group's result is true, the whole thing is true
            if group_result:
                return True

        return False

    return lambda_func
    
def compare_values(value1, operator, value2):
    if operator == "<":
        return value1 < value2
    elif operator == "<=":
        return value1 <= value2
    elif operator == "=":
        return value1 == value2
    elif operator == "!=":
        return value1 != value2
    elif operator == ">":
        return value1 > value2
    elif operator == ">=":
        return value1 >= value2
    return False   