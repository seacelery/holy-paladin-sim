const embellishmentsData = {
    "No embellishment": "",
    // "Potion Absorption Inhibitor": {
    //     "name": "Potion Absorption Inhibitor", 
    //     "description": "Increase the duration of Dragon Isles potions by 50%.", 
    //     "id": 371700, 
    //     "type": "embellishment"
    // },
    // "Magazine of Healing Darts": {
    //     "name": "Magazine of Healing Darts", 
    //     "description": "Your healing spells and abilities have a chance to fire a Healing Dart toward an ally target. The first ally hit will be healed for *12185.", 
    //     "id": 385347, 
    //     "type": "embellishment", 
    //     "effect_values": [{"allocation_type": "flat_damage", "base_item_level": 330, "base_value": 12185, "effect_coefficient": 76.17424, "effect_type": "scalar"}]
    // },
    // "Blue Silken Lining": {
    //     "name": "Blue Silken Lining", 
    //     "description": "Greatly improves the comfort of your gear, allowing you to enter a Zone of Focus while over 90% health, granting you *126 Mastery.", 
    //     "id": 387335, 
    //     "type": "embellishment", 
    //     "effect_values": [{"allocation_type": "flat_healing", "base_item_level": 330, "base_value": 126, "effect_coefficient": 0.389637, "effect_type": "scalar"}]
    // },
    // "Bronzed Grip Wrappings": {
    //     "name": "Bronzed Grip Wrappings", 
    //     "description": "Your damaging and healing spells and abilities have a chance to echo in time, dealing up to 3611 Arcane damage or *6018 healing with their echo.", 
    //     "id": 396442, 
    //     "type": "embellishment", 
    //     "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 330, "base_value": 12185, "effect_coefficient": 14.83545, "effect_type": "scalar"}]
    // },
    // "Shadowflame-Tempered Armor Patch": {
    //     "name": "Shadowflame-Tempered Armor Patch", 
    //     "description": "Dealing damage can inflict stacking Shadowflame damage.", 
    //     "id": 406251, 
    //     "type": "embellishment"},
    // "Dreamtender's Charm": {
    //     "name": "Dreamtender's Charm", 
    //     "description": "While above 70% health and in combat, you enter a Dreaming Trance and gain *4 Critical Strike. The trance will deepen every second and grant another stack, up to 20.", 
    //     "id": 420750, 
    //     "type": "embellishment",
    //     "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 330, "base_value": 4, "effect_coefficient": 0.010603, "effect_type": "scalar"}]
    // },
    // "Verdant Conduit": {
    //     "name": "Verdant Conduit", 
    //     "description": "A magical conduit tethers you to the Dream, granting a chance when using spells and abilities to embrace its power, gaining *79 of a random secondary stat for 10 sec.", 
    //     "id": 418523, 
    //     "type": "embellishment",
    //     "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 330, "base_value": 79, "effect_coefficient": 0.195571, "effect_type": "scalar"}]
    // },
    // "Verdant Tether": {
    //     "name": "Verdant Tether", 
    //     "description": "Your healing abilities have the chance to tether you to a friendly ally, granting both players between *46.5 to *93 Versatility. This effect increases the closer they are to each other.", 
    //     "id": 426554, 
    //     "type": "embellishment",
    //     "effect_values": [{"allocation_type": "rating_multiplier_jewellery", "base_item_level": 330, "base_value": 46.5, "effect_coefficient": 0.229097 / 2, "effect_type": "scalar"},
    //                       {"allocation_type": "rating_multiplier_jewellery", "base_item_level": 330, "base_value": 93, "effect_coefficient": 0.229097, "effect_type": "scalar"}]
    // },
    "Blessed Weapon Grip": {
        "name": "Blessed Weapon Grip", 
        "description": "Damaging a target has a chance bless your weapon, increasing your highest secondary stat by *220. The effect slowly fades over time.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 330, "base_value": 220, "effect_coefficient": 0.032211, "effect_type": "scalar"}]
    },
    "Captured Starlight": {
        "name": "Captured Starlight", 
        "description": "When damaged at low health, unleash starlight to shield yourself. The frequency this can occur increases with socketed gems.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Dawnthread Lining": {
        "name": "Dawnthread Lining", 
        "description": "While above 80% health, gain *756 Critical Strike.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 756, "effect_coefficient": .3643973, "effect_type": "scalar"}]
    },
    "Duskthread Lining": {
        "name": "Duskthread Lining", 
        "description": "While above 80% health, gain *756 Versatility.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 756, "effect_coefficient": .3643973, "effect_type": "scalar"}]
    },
    "Echoing Impact Seal": {
        "name": "Echoing Impact Seal", 
        "description": "", 
        "id": 0, 
        "type": "embellishment"
    },
    "Elemental Focusing Lens": {
        "name": "Elemental Focusing Lens", 
        "description": "Your damaging spells and abilities have a chance to deal *214 damage to your target. The magic school chosen is based upon your selection of socketed Khaz Algar gems.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Prismatic Null Stone": {
        "name": "Prismatic Null Stone", 
        "description": "Increases effectiveness of Blasphemite secondary effects by 50%.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Writhing Armor Banding": {
        "name": "Writhing Armor Banding", 
        "description": "Double the effects of your other Nerubian embellished item, positive and negative.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Darkmoon Sigil: Symbiosis": {
        "name": "Darkmoon Sigil: Symbiosis", 
        "description": "Every 10 seconds in combat take 1% of your maximum Health as Nature damage and gain a stack of Symbiosis, granting *131 Versatility for 20 sec  stacking up to 5 times.", 
        "id": 463232, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 131, "effect_coefficient": 0.08835853636, "effect_type": "scalar"}]
    },
    "Darkmoon Sigil: Ascension": {
        "name": "Darkmoon Sigil: Ascension", 
        "description": "Gain Ascendance every 8 seconds spent in combat. Ascendance grants *89 of a random secondary stat for 15 sec, stacking up to 10 times.", 
        "id": 463232, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 89, "effect_coefficient": 0.02280857228, "effect_type": "scalar"}]
    },
    "Energy Redistribution Beacon": {
        "name": "Energy Redistribution Beacon", 
        "description": "", 
        "id": 0, 
        "type": "embellishment"
    }
};

const ptrEmbellishmentsData = {
    "No embellishment": "",
    "Blessed Weapon Grip": {
        "name": "Blessed Weapon Grip", 
        "description": "Damaging a target has a chance bless your weapon, increasing your highest secondary stat by *220. The effect slowly fades over time.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 330, "base_value": 220, "effect_coefficient": 0.032211, "effect_type": "scalar"}]
    },
    "Captured Starlight": {
        "name": "Captured Starlight", 
        "description": "When damaged at low health, unleash starlight to shield yourself. The frequency this can occur increases with socketed gems.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Dawnthread Lining": {
        "name": "Dawnthread Lining", 
        "description": "While above 80% health, gain *756 Critical Strike.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 756, "effect_coefficient": .3643973, "effect_type": "scalar"}]
    },
    "Duskthread Lining": {
        "name": "Duskthread Lining", 
        "description": "While above 80% health, gain *756 Versatility.", 
        "id": 0, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 756, "effect_coefficient": .3643973, "effect_type": "scalar"}]
    },
    "Echoing Impact Seal": {
        "name": "Echoing Impact Seal", 
        "description": "", 
        "id": 0, 
        "type": "embellishment"
    },
    "Elemental Focusing Lens": {
        "name": "Elemental Focusing Lens", 
        "description": "Your damaging spells and abilities have a chance to deal *214 damage to your target. The magic school chosen is based upon your selection of socketed Khaz Algar gems.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Prismatic Null Stone": {
        "name": "Prismatic Null Stone", 
        "description": "Increases effectiveness of Blasphemite secondary effects by 50%.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Writhing Armor Banding": {
        "name": "Writhing Armor Banding", 
        "description": "Double the effects of your other Nerubian embellished item, positive and negative.", 
        "id": 0, 
        "type": "embellishment"
    },
    "Darkmoon Sigil: Symbiosis": {
        "name": "Darkmoon Sigil: Symbiosis", 
        "description": "Every 10 seconds in combat take 1% of your maximum Health as Nature damage and gain a stack of Symbiosis, granting *131 Versatility for 20 sec  stacking up to 5 times.", 
        "id": 463232, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 131, "effect_coefficient": 0.02280857228, "effect_type": "scalar"}]
    },
    "Darkmoon Sigil: Ascension": {
        "name": "Darkmoon Sigil: Ascension", 
        "description": "Gain Ascendance every 8 seconds spent in combat. Ascendance grants *89 of a random secondary stat for 15 sec, stacking up to 10 times.", 
        "id": 463232, 
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 602, "base_value": 89, "effect_coefficient": 0.02280857228, "effect_type": "scalar"}]
    },
    "Energy Redistribution Beacon": {
        "name": "Energy Redistribution Beacon", 
        "description": "", 
        "id": 0, 
        "type": "embellishment"
    }
};

const itemSlotBonuses = {
    "Main Hand": {"enchants": ["No enchant", "Authority of Air", "Authority of Fiery Resolve", "Authority of Radiant Power", "Authority of Storms", "Authority of the Depths", "Stonebound Artistry", "Oathsworn's Tenacity", "Stormrider's Fury", "Council's Guile"], "embellishments": ptrEmbellishmentsData},
    "Off Hand":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Head": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Necklace":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Shoulders": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Cloak":  {"enchants": ["No enchant", "Chant of Winged Grace", "Chant of Leeching Fangs", "Chant of Burrowing Rapidity"], "embellishments": ptrEmbellishmentsData},
    "Gloves": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Body":  {"enchants": ["No enchant", "Council's Intellect", "Crystalline Radiance"], "embellishments": ptrEmbellishmentsData},
    "Bracers": {"enchants": ["No enchant", "Chant of Armored Avoidance", "Chant of Armored Leech", "Chant of Armored Speed"], "embellishments": ptrEmbellishmentsData},
    "Belt":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Legs": {"enchants": ["No enchant", "Daybreak Spellthread", "Sunset Spellthread", "Weavercloth Spellthread"], "embellishments": ptrEmbellishmentsData},
    "Boots":  {"enchants": ["No enchant", "Cavalry's March", "Scout's March", "Defender's March"], "embellishments": ptrEmbellishmentsData},
    "Ring 1": {"enchants": ["No enchant", "Radiant Haste", "Radiant Critical Strike", "Radiant Mastery", "Radiant Versatility", "Cursed Haste", "Cursed Critical Strike", "Cursed Mastery", "Cursed Versatility"], "embellishments": ptrEmbellishmentsData},
    "Ring 2":  {"enchants": ["No enchant", "Radiant Haste", "Radiant Critical Strike", "Radiant Mastery", "Radiant Versatility", "Cursed Haste", "Cursed Critical Strike", "Cursed Mastery", "Cursed Versatility"], "embellishments": ptrEmbellishmentsData},
    "Trinket 1": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Trinket 2":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
};

const ptrItemSlotBonuses = {
    "Main Hand": {"enchants": ["No enchant", "Authority of Air", "Authority of Fiery Resolve", "Authority of Radiant Power", "Authority of Storms", "Authority of the Depths", "Stonebound Artistry", "Oathsworn's Tenacity", "Stormrider's Fury", "Council's Guile"], "embellishments": ptrEmbellishmentsData},
    "Off Hand":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Head": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Necklace":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Shoulders": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Cloak":  {"enchants": ["No enchant", "Chant of Winged Grace", "Chant of Leeching Fangs", "Chant of Burrowing Rapidity"], "embellishments": ptrEmbellishmentsData},
    "Gloves": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Body":  {"enchants": ["No enchant", "Council's Intellect", "Crystalline Radiance"], "embellishments": ptrEmbellishmentsData},
    "Bracers": {"enchants": ["No enchant", "Chant of Armored Avoidance", "Chant of Armored Leech", "Chant of Armored Speed"], "embellishments": ptrEmbellishmentsData},
    "Belt":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Legs": {"enchants": ["No enchant", "Daybreak Spellthread", "Sunset Spellthread", "Weavercloth Spellthread"], "embellishments": ptrEmbellishmentsData},
    "Boots":  {"enchants": ["No enchant", "Cavalry's March", "Scout's March", "Defender's March"], "embellishments": ptrEmbellishmentsData},
    "Ring 1": {"enchants": ["No enchant", "Radiant Haste", "Radiant Critical Strike", "Radiant Mastery", "Radiant Versatility", "Cursed Haste", "Cursed Critical Strike", "Cursed Mastery", "Cursed Versatility"], "embellishments": ptrEmbellishmentsData},
    "Ring 2":  {"enchants": ["No enchant", "Radiant Haste", "Radiant Critical Strike", "Radiant Mastery", "Radiant Versatility", "Cursed Haste", "Cursed Critical Strike", "Cursed Mastery", "Cursed Versatility"], "embellishments": ptrEmbellishmentsData},
    "Trinket 1": {"enchants": [], "embellishments": ptrEmbellishmentsData},
    "Trinket 2":  {"enchants": [], "embellishments": ptrEmbellishmentsData},
};

const craftedItems = {
    "Obsidian Seared Hexsword": embellishmentsData,
    "Obsidian Seared Runeaxe": embellishmentsData,
    "Signet of Titanic Insight": embellishmentsData,
    "Primal Molten Sabatons": embellishmentsData,
    "Primal Molten Breastplate": embellishmentsData,
    "Torc of Passed Time": embellishmentsData,
    "Elemental Lariat": "",
    "Charged Hexsword": embellishmentsData,
    "Charged Invoker": embellishmentsData,
    "Everforged Breastplate": embellishmentsData,
    "Everforged Helm": embellishmentsData,
    "Everforged Gauntlets": embellishmentsData,
    "Everforged Greatbelt": embellishmentsData,
    "Everforged Legplates": embellishmentsData,
    "Everforged Pauldrons": embellishmentsData,
    "Everforged Sabatons": embellishmentsData,
    "Everforged Vambraces": embellishmentsData,
    "Everforged Defender": embellishmentsData,
    "Fractured Gemstone Locket": "",
    "Binding of Binding": ""
};

const ptrCraftedItems = {
    "Obsidian Seared Hexsword": embellishmentsData,
    "Obsidian Seared Runeaxe": embellishmentsData,
    "Signet of Titanic Insight": embellishmentsData,
    "Primal Molten Sabatons": embellishmentsData,
    "Primal Molten Breastplate": embellishmentsData,
    "Torc of Passed Time": embellishmentsData,
    "Elemental Lariat": "",
    "Charged Hexsword": ptrEmbellishmentsData,
    "Charged Invoker": ptrEmbellishmentsData,
    "Everforged Breastplate": ptrEmbellishmentsData,
    "Everforged Helm": ptrEmbellishmentsData,
    "Everforged Gauntlets": ptrEmbellishmentsData,
    "Everforged Greatbelt": ptrEmbellishmentsData,
    "Everforged Legplates": ptrEmbellishmentsData,
    "Everforged Pauldrons": ptrEmbellishmentsData,
    "Everforged Sabatons": ptrEmbellishmentsData,
    "Everforged Vambraces": ptrEmbellishmentsData,
    "Everforged Defender": embellishmentsData,
    "Fractured Gemstone Locket": "",
    "Binding of Binding": ""
};

const embellishmentItems = {
    "Elemental Lariat":  {
        "name": "Elemental Lariat", 
        "description": "Your spells and abilities have a chance to empower one of your socketed elemental gems, granting *407 of their associated stat. Lasts 5 sec and an additional 1 sec per elemental gem.", 
        "id": 375323,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier_jewellery", "base_item_level": 382, "base_value": 407, "effect_coefficient": 0.458195, "effect_type": "scalar"}]
    },
    "Allied Chestplate of Generosity": {
        "name": "Allied Chestplate of Generosity", 
        "description": "Your spells and abilities have a chance to rally you and your 4 closest allies within 30 yards to victory for 10 sec, increasing Versatility by *191.", 
        "id": 378134,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "flat_damage", "base_item_level": 382, "base_value": 191, "effect_coefficient": 0.74681, "effect_type": "scalar"}]
    },
    "Allied Wristguard of Companionship": {
        "name": "Allied Wristgaurds of Companionship", 
        "description": "Grants *46 Versatility for every ally in a 30 yard radius, stacking up to 4 times.", 
        "id": 395959,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 382, "base_value": 46, "effect_coefficient": 0.052152, "effect_type": "scalar"}]
    },
    "Fractured Gemstone Locket": {
        "name": "Fractured Gemstone Locket", 
        "description": "", 
        "id": 0,
        "type": "embellishment",
        "effect_values": []
    },
    "Binding of Binding": {
        "name": "Binding of Binding", 
        "description": "", 
        "id": 0,
        "type": "embellishment",
        "effect_values": []
    }
};

const ptrEmbellishmentItems = {
    "Elemental Lariat":  {
        "name": "Elemental Lariat", 
        "description": "Your spells and abilities have a chance to empower one of your socketed elemental gems, granting *407 of their associated stat. Lasts 5 sec and an additional 1 sec per elemental gem.", 
        "id": 375323,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier_jewellery", "base_item_level": 382, "base_value": 407, "effect_coefficient": 0.458195, "effect_type": "scalar"}]
    },
    "Allied Chestplate of Generosity": {
        "name": "Allied Chestplate of Generosity", 
        "description": "Your spells and abilities have a chance to rally you and your 4 closest allies within 30 yards to victory for 10 sec, increasing Versatility by *191.", 
        "id": 378134,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "flat_damage", "base_item_level": 382, "base_value": 191, "effect_coefficient": 0.74681, "effect_type": "scalar"}]
    },
    "Allied Wristguard of Companionship": {
        "name": "Allied Wristgaurds of Companionship", 
        "description": "Grants *46 Versatility for every ally in a 30 yard radius, stacking up to 4 times.", 
        "id": 395959,
        "type": "embellishment",
        "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 382, "base_value": 46, "effect_coefficient": 0.052152, "effect_type": "scalar"}]
    },
    "Fractured Gemstone Locket": {
        "name": "Fractured Gemstone Locket", 
        "description": "", 
        "id": 0,
        "type": "embellishment",
        "effect_values": []
    },
    "Binding of Binding": {
        "name": "Binding of Binding", 
        "description": "", 
        "id": 0,
        "type": "embellishment",
        "effect_values": []
    }
};

export { itemSlotBonuses, ptrItemSlotBonuses, embellishmentsData, ptrEmbellishmentsData, embellishmentItems, ptrEmbellishmentItems, craftedItems, ptrCraftedItems };