const embellishmentsData = {
    "No embellishment": "",
    "Potion Absorption Inhibitor": {"name": "Potion Absorption Inhibitor", "description": "Increase the duration of Dragon Isles potions by 50%.", "id": 371700, "type": "embellishment"},
    "Magazine of Healing Darts": {"name": "Magazine of Healing Darts", "description": "When you heal you sometimes fire a Healing Dart.", "id": 385347, "type": "embellishment"},
    "Blue Silken Lining": {"name": "Blue Silken Lining", "description": "While above 90% health, gain Mastery.", "id": 387335, "type": "embellishment"},
    "Bronzed Grip Wrappings": {"name": "Bronzed Grip Wrappings", "description": "Your damaging and healing spells and abilities have a chance to echo in time, dealing up to 1296 Arcane damage or 2159 healing with their echo.", "id": 396442, "type": "embellishment"},
    "Shadowflame-Tempered Armor Patch": {"name": "Shadowflame-Tempered Armor Patch", "description": "Dealing damage can inflict stacking Shadowflame damage.", "id": 406251, "type": "embellishment"},
    "Dreamtender's Charm": {"name": "Dreamtender's Charm", "description": "Gain stacking Critical Strike while above 70% health.", "id": 420750, "type": "embellishment"},
    "Verdant Conduit": {"name": "Verdant Conduit", "description": "Spells and abilities sometimes provide secondary stats.", "id": 418523, "type": "embellishment"},
    "Verdant Tether": {"name": "Verdant Tether", "description": "Your healing abilities have the chance to tether you to a friendly ally, granting Versatility for both players based on distance.", "id": 426554, "type": "embellishment"},
};

const itemSlotBonuses = {
    "Main Hand": {"enchants": ["No enchant", "Sophic Devotion", "Dreaming Devotion"], "embellishments": embellishmentsData},
    "Off Hand":  {"enchants": [], "embellishments": embellishmentsData},
    "Head": {"enchants": [], "embellishments": embellishmentsData},
    "Necklace":  {"enchants": [], "embellishments": embellishmentsData},
    "Shoulders": {"enchants": [], "embellishments": embellishmentsData},
    "Cloak":  {"enchants": ["No enchant", "Regenerative Leech", "Graceful Avoidance"], "embellishments": embellishmentsData},
    "Gloves": {"enchants": [], "embellishments": embellishmentsData},
    "Body":  {"enchants": ["No enchant", "Waking Stats", "Reserve of Intellect"], "embellishments": embellishmentsData},
    "Bracers": {"enchants": ["No enchant", "+200 Leech", "+200 Avoidance"], "embellishments": embellishmentsData},
    "Belt":  {"enchants": [], "embellishments": embellishmentsData},
    "Legs": {"enchants": ["No enchant", "+177 Intellect & +131 Stamina", "+177 Intellect & +5% Mana"], "embellishments": embellishmentsData},
    "Boots":  {"enchants": ["No enchant", "Plainsrunner's Breeze", "Watcher's Loam"], "embellishments": embellishmentsData},
    "Ring 1": {"enchants": ["No enchant", "+82 Haste", "+82 Critical Strike", "+82 Mastery", "+82 Versatility"], "embellishments": embellishmentsData},
    "Ring 2":  {"enchants": ["No enchant", "+82 Haste", "+82 Critical Strike", "+82 Mastery", "+82 Versatility"], "embellishments": embellishmentsData},
    "Trinket 1": {"enchants": [], "embellishments": embellishmentsData},
    "Trinket 2":  {"enchants": [], "embellishments": embellishmentsData},
};

const craftedItems = {
    "Obsidian Seared Hexsword": embellishmentsData,
    "Obsidian Seared Runeaxe": embellishmentsData,
    "Signet of Titanic Insight": embellishmentsData,
    "Primal Molten Sabatons": embellishmentsData,
    "Torc of Passed Time": embellishmentsData
};

const embellishmentItems = {
    "Elemental Lariat":  {"name": "Elemental Lariat", "description": "Your spells and abilities have a chance to empower one of your socketed elemental gems, granting 84 of their associated stat. Lasts 5 sec and an additional 1 sec per elemental gem.", "id": 375323},
    "Allied Chestplate of Generosity": {"name": "Allied Chestplate of Generosity", "description": "Your spells and abilities have a chance to rally you and your 4 closest allies within 30 yards to victory for 10 sec, increasing Versatility by 43.", "id": 378134},
    "Allied Wristguard of Companionship": {"name": "Allied Wristgaurds of Companionship", "description": "Grants 8 Versatility for every ally in a 30 yard radius, stacking up to 4 times.", "id": 395959}
};

export { itemSlotBonuses, embellishmentsData, embellishmentItems, craftedItems };