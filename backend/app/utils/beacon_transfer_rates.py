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
    "Light of Dawn": single_beacon_transfer_aoe,
    "Glimmer of Light": single_beacon_transfer_aoe,
    "Light's Hammer": single_beacon_transfer_aoe
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
    "Light of Dawn": double_beacon_transfer_aoe,
    "Glimmer of Light": double_beacon_transfer_aoe,
    "Light's Hammer": double_beacon_transfer_aoe
}