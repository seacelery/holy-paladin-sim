single_beacon_transfer_st = 0.35
single_beacon_transfer_aoe = single_beacon_transfer_st * 0.5
double_beacon_transfer_st = single_beacon_transfer_st * 0.7
double_beacon_transfer_aoe = double_beacon_transfer_st * 0.5

beacon_transfer_rates_single_beacon = {
    "Holy Shock": single_beacon_transfer_st,
    "Holy Shock (Divine Toll)": single_beacon_transfer_st,
    "Holy Shock (Divine Resonance)": single_beacon_transfer_st,
    "Holy Shock (Rising Sunlight)": single_beacon_transfer_st,
    "Flash of Light": single_beacon_transfer_st,
    "Holy Light": single_beacon_transfer_st,
    "Word of Glory": single_beacon_transfer_st,
    "Tyr's Deliverance": single_beacon_transfer_st,
    "Resplendent Light": single_beacon_transfer_st,
    "Afterimage": single_beacon_transfer_st,
    "Holy Reverberation": single_beacon_transfer_st,
    "Seal of the Crusader": single_beacon_transfer_st,
    "Golden Path": single_beacon_transfer_st,
    "Light of the Martyr": single_beacon_transfer_st,
    "Veneration": single_beacon_transfer_st,
    "Merciful Auras": single_beacon_transfer_st,
    "Avenging Crusader (Judgment)": single_beacon_transfer_st,
    "Avenging Crusader (Crusader Strike)": single_beacon_transfer_st,
    "Light of Dawn": single_beacon_transfer_aoe,
    "Glimmer of Light": single_beacon_transfer_aoe,
    "Light's Hammer": single_beacon_transfer_aoe,
    "Holy Prism": single_beacon_transfer_aoe
}

beacon_transfer_rates_double_beacon = {
    "Holy Shock": double_beacon_transfer_st,
    "Holy Shock (Divine Toll)": double_beacon_transfer_st,
    "Holy Shock (Divine Resonance)": double_beacon_transfer_st,
    "Holy Shock (Rising Sunlight)": double_beacon_transfer_st,
    "Flash of Light": double_beacon_transfer_st,
    "Holy Light": double_beacon_transfer_st,
    "Word of Glory": double_beacon_transfer_st,
    "Tyr's Deliverance": double_beacon_transfer_st,
    "Resplendent Light": double_beacon_transfer_st,
    "Afterimage": double_beacon_transfer_st,
    "Holy Reverberation": double_beacon_transfer_st,
    "Seal of the Crusader": double_beacon_transfer_st,
    "Golden Path": double_beacon_transfer_st,
    "Light of the Martyr": double_beacon_transfer_st,
    "Veneration": double_beacon_transfer_st,
    "Merciful Auras": double_beacon_transfer_st,
    "Avenging Crusader (Judgment)": double_beacon_transfer_st,
    "Avenging Crusader (Crusader Strike)": double_beacon_transfer_st,
    "Light of Dawn": double_beacon_transfer_aoe,
    "Glimmer of Light": double_beacon_transfer_aoe,
    "Light's Hammer": double_beacon_transfer_aoe,
    "Holy Prism": double_beacon_transfer_aoe
}

beacon_transfer = {
    "Holy Shock": "single_target",
    "Holy Shock (Divine Toll)": "single_target",
    "Holy Shock (Divine Resonance)": "single_target",
    "Holy Shock (Rising Sunlight)": "single_target",
    "Flash of Light": "single_target",
    "Holy Light": "single_target",
    "Word of Glory": "single_target",
    "Eternal Flame": "single_target",
    "Eternal Flame (HoT)": "single_target",
    "Dawnlight (HoT)": "single_target",
    "Tyr's Deliverance": "single_target",
    "Resplendent Light": "single_target",
    "Afterimage": "single_target",
    "Holy Reverberation": "single_target",
    "Seal of the Crusader": "single_target",
    "Golden Path": "single_target",
    "Light of the Martyr": "single_target",
    "Veneration": "single_target",
    "Merciful Auras": "single_target",
    "Avenging Crusader (Judgment)": "single_target",
    "Avenging Crusader (Crusader Strike)": "single_target",
    "Light of Dawn": "aoe",
    "Glimmer of Light": "aoe",
    "Light's Hammer": "aoe",
    "Holy Prism": "aoe",
    "Dawnlight (AoE)": "aoe"
}