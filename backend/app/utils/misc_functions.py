from .beacon_transfer_rates import *

# def apply_holy_reverberation(caster, target, current_time, buff):
#     print(buff)
#     target.apply_buff_to_target(buff, current_time)
                
#     longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
#     if "Holy Reverberation" in target.target_active_buffs:
#         if len(target.target_active_buffs["Holy Reverberation"]) > 0:
#             caster.buff_events.append(f"{format_time(current_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
#         del target.target_active_buffs["Glimmer of Light"]


# formatting
def format_time(time):
    return "{:05.2f}".format(time)

def get_timestamp(event):
    timestamp_string = event.split(": ")[0]
    return float(timestamp_string)


# calculations & increments


def calculate_beacon_healing(spell_name, amount):
    return amount * beacon_transfer_rates_double_beacon.get(spell_name, 0)

def increment_holy_power(ability, caster):
    if caster.holy_power >= caster.max_holy_power:
        caster.holy_power = caster.max_holy_power
        caster.holy_power_wasted += ability.holy_power_gain
    else:
        caster.holy_power += ability.holy_power_gain      
    caster.holy_power_gained += ability.holy_power_gain
    add_to_holy_power_by_ability(caster.holy_power_by_ability, ability, caster)
    
def add_to_holy_power_by_ability(dict, ability, caster):
    caster.holy_power_by_ability[ability.name] = caster.holy_power_by_ability.get(ability.name, 0) + ability.holy_power_gain
    
# def increment_blessing_of_dawn_counter(caster, current_time):
#     caster.blessing_of_dawn_counter += 1
#     if caster.blessing_of_dawn_counter == 3:
#         caster.apply_buff_to_self(BlessingOfDawn(), current_time)


# data tracking functions
def append_spell_heal_event(array, spell_name, caster, target, amount, current_time, is_crit, spends_mana=False, is_absorb=False):
    if is_absorb:
        if spends_mana:
            if is_crit:
                array.append(f"{format_time(current_time)}: {spell_name} crit absorbed damage on {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
            else:
                array.append(f"{format_time(current_time)}: {spell_name} absorbed damage on {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
        else:
            if is_crit:
                array.append(f"{format_time(current_time)}: {spell_name} crit absorbed damage on {target.name} for {round(amount)}")
            else:
                array.append(f"{format_time(current_time)}: {spell_name} absorbed damage on {target.name} for {round(amount)}")
    else:
        if spends_mana:
            if is_crit:
                array.append(f"{format_time(current_time)}: {spell_name} crit healed {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
            else:
                array.append(f"{format_time(current_time)}: {spell_name} healed {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
        else:
            if is_crit:
                array.append(f"{format_time(current_time)}: {spell_name} crit healed {target.name} for {round(amount)}")
            else:
                array.append(f"{format_time(current_time)}: {spell_name} healed {target.name} for {round(amount)}")

def append_spell_damage_event(array, spell_name, caster, target, amount, current_time, is_crit, spends_mana=False):
    if spends_mana:
        if is_crit:
            array.append(f"{format_time(current_time)}: {spell_name} crit damaged {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
        else:
            array.append(f"{format_time(current_time)}: {spell_name} damaged {target.name} for {round(amount)}, mana: {caster.mana}, holy power before: {caster.holy_power}, holy power wasted: {caster.holy_power_wasted}")
    else:
        if is_crit:
            array.append(f"{format_time(current_time)}: {spell_name} crit damaged {target.name} for {round(amount)}")
        else:
            array.append(f"{format_time(current_time)}: {spell_name} damaged {target.name} for {round(amount)}")

def append_spell_beacon_event(array, source_spell_name, caster, target, spell_healing, beacon_healing, current_time):
    array.append(f"{format_time(current_time)}: Beacon of Light healed {target.name} for {round(beacon_healing)} ({source_spell_name}: {round(spell_healing)})")  
  
def append_spell_started_casting_event(array, caster, ability, current_time):
    array.append(f"{format_time(current_time)}: {caster.name} started casting {ability.name}")  
    
def append_spell_cast_event(array, ability, caster, current_time, target=None):
    if target is None:
        array.append(f"{format_time(current_time)}: {caster.name} cast {ability}")
        
    else:
        array.append(f"{format_time(current_time)}: {caster.name} cast {ability} on {target.name}")

def append_aura_applied_event(array, aura_name, caster, target, current_time, duration=None, current_stacks=1, max_stacks=1):
    if max_stacks > 1:
        if duration:
            array.append(f"{format_time(current_time)}: {aura_name} ({current_stacks}) applied to {target.name}: {round(duration, 2)}s duration")
        else:
            array.append(f"{format_time(current_time)}: {aura_name} ({current_stacks}) applied to {target.name}")
    else:
        if duration:
            array.append(f"{format_time(current_time)}: {aura_name} applied to {target.name}: {round(duration, 2)}s duration")
        else:
            array.append(f"{format_time(current_time)}: {aura_name} applied to {target.name}")
            
def append_aura_refreshed_event(array, aura_name, caster, target, current_time, duration=None):
    pass

def append_aura_removed_event(array, aura_name, caster, target, current_time, duration=None):
    if duration:
        array.append(f"{format_time(current_time)}: {aura_name} removed from {target.name} with {round(duration, 2)}s remaining")
    else:
        array.append(f"{format_time(current_time)}: {aura_name} removed from {target.name}")
        
def append_aura_stacks_decremented(array, aura_name, caster, current_time, stack_count, target=None, duration=None):
    if target:
        array.append(f"{format_time(current_time)}: {aura_name} ({stack_count}) on {target.name}: {round(duration, 2)}s remaining")
    else:
        array.append(f"{format_time(current_time)}: {aura_name} ({stack_count}): {round(duration, 2)}s remaining")

# ouput functions
def add_heal_to_most_relevant_events(array, time, spell, source, target=None, is_crit=None, heal_amount=None, 
                                     mana_spent=None, holy_power_gained=None, holy_power_spent=None):
    event = {
        "timestamp": time,
        "spell": spell,
        "source": source,
    }

    if target is not None:
        event["target"] = target
    if is_crit is not None:
        event["is_crit"] = is_crit
    if heal_amount is not None:
        event["heal_amount"] = heal_amount
    if mana_spent is not None:
        event["mana_spent"] = mana_spent
    if holy_power_gained is not None:
        event["holy_power_gained"] = holy_power_gained
    if holy_power_spent is not None:
        event["holy_power_spent"] = holy_power_spent

    array.append(event)

# ability breakdown
def update_spell_data_heals(spell_breakdown, spell_name, target, heal_amount, is_crit):
    spell_data = spell_breakdown[spell_name]
    spell_data["total_healing"] += heal_amount
    spell_data["crits"] += 1 if is_crit else 0
    spell_data["hits"] += 1
    
    if target.name not in spell_data["targets"]:
        spell_data["targets"][target.name] = {
            "healing": 0,
            "casts": 0,
            "crits": 0
        }
        
    target_data = spell_data["targets"][target.name]
    target_data["healing"] += heal_amount
    target_data["casts"] += 1
    target_data["crits"] += 1 if is_crit else 0
    
def update_spell_data_casts(spell_breakdown, spell_name, mana_spent=None, holy_power_gained=None, holy_power_spent=None):
    if spell_name not in spell_breakdown:
        spell_breakdown[spell_name] = {
            "total_healing": 0,
            "casts": 0,
            "hits": 0,
            "targets": {},
            "crits": 0,
            "mana_spent": 0,
            "holy_power_gained": 0,
            "holy_power_spent": 0
        }
    
    spell_data = spell_breakdown[spell_name]
    spell_data["casts"] += 1
    if mana_spent != 0 and mana_spent is not None:
        spell_data["mana_spent"] += mana_spent
    if holy_power_gained != 0 and holy_power_gained is not None:
        spell_data["holy_power_gained"] += holy_power_gained
    if holy_power_spent != 0 and holy_power_spent is not None:
        spell_data["holy_power_spent"] += holy_power_spent