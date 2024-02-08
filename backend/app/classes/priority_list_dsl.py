def parse_condition(condition_str):
    parts = condition_str.split("|")
    action_name = parts[0].strip()

    all_conditions = []
    current_group = []

    for part in parts[1:]:
        part = part.strip()

        condition = {"keyword": ""}

        if "active" in part:
            condition["keyword"] = "active"
            condition["name"] = part.rsplit(" ", 1)[0]
            
        elif "stacks" in part:
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "duration" in part:
            part_split = part.rsplit(" ", 3)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "charges" in part:
            part_split = part.rsplit(" ", 3)
            print(part_split)
            condition["name"] = part_split[0]
            condition["keyword"] = part_split[1]
            condition["operator"] = part_split[2]
            condition["value"] = part_split[3]
            
        elif "Mana" in part:
            part_split = part.split(" ")
            condition["keyword"] = part_split[0]
            condition["operator"] = part_split[1]
            condition["value"] = part_split[2]
            
        elif "Race" in part:
            part_split = part.split(" ")
            print(part_split)
            condition["keyword"] = part_split[0]
            condition["operator"] = part_split[1]
            condition["value"] = " ".join(part_split[2:])

        # "and" & first condition adds to the current group
        if "and" in part or not current_group:
            current_group.append(condition)
        else:
            # "or" starts a new group
            if current_group:
                all_conditions.append(current_group)
            current_group = [condition]

    # append final group
    if current_group:
        all_conditions.append(current_group)

    return action_name, all_conditions
    
def condition_to_lambda(all_conditions):
    def condition_lambda(self):
        # print(all_conditions)
        for group in all_conditions:
            group_result = True
            
            for condition in group:
                result = False
                
                if condition["keyword"] == "active":
                    result = condition["name"] in self.paladin.active_auras
                    
                elif condition["keyword"] == "Mana":
                    mana = self.paladin.mana
                    value = (float(condition["value"].replace("%", "")) / 100) * self.paladin.max_mana if "%" in condition["value"] else float(condition["value"])
                    result = compare_values(mana, condition["operator"], value)
                    
                elif condition["keyword"] == "Race":
                    race = self.paladin.race
                    result = race == condition["value"]
                    
                elif condition["keyword"] == "stacks":
                    if condition["name"] in self.paladin.active_auras:
                        stacks = self.paladin.active_auras[condition["name"]].current_stacks
                        value = float(condition["value"])
                        result = compare_values(stacks, condition["operator"], value)
                        
                elif condition["keyword"] == "duration":
                    if condition["name"] in self.paladin.active_auras:
                        duration = self.paladin.active_auras[condition["name"]].duration
                        value = float(condition["value"])
                        result = compare_values(duration, condition["operator"], value)
                        
                elif condition["keyword"] == "charges":
                    charges = self.paladin.abilities[condition["name"]].current_charges
                    value = int(condition["value"])
                    result = compare_values(charges, condition["operator"], value)
                        
                else:
                    result = True

                # if any condition's result is false, the whole group's result is false
                if not result:
                    group_result = False
                    break

            # if the group's result is true, the whole thing is true
            if group_result:
                return True

        return False

    return condition_lambda
     
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
    