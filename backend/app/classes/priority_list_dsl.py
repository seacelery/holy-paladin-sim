def parse_condition(condition_str, abilities_list):
    parts = condition_str.split("💀")
    action_name = parts[0].strip()
    if action_name in abilities_list:
        print("awawawa")
    condition = parts[1].strip()
    condition_parts = condition.split(" ")
    attribute, operator, value = condition_parts[0], condition_parts[1], condition_parts[2]
    
    return action_name, attribute, operator, value
    
def condition_to_lambda(action_name, attribute, operator, value):
    if attribute == "cooldown":
        return lambda: f"self.paladin.abilities['{action_name}'].{attribute} {operator} {value}"
    