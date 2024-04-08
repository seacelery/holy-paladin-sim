const itemDataEffects = [
    {
        "id": 193004,
        "name": "Idol of the Spell-Weaver",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon3_color1.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Idol of the Spell-Weaver",
                "id": 376640,
                "description": "Equip: Your spells and abilities have a chance to grant *44 Versatility per Malygite you have equipped. Upon reaching 18 stacks, all stacks are consumed and you gain *750 secondary stats, split evenly for 15 sec.\r\n",
                "effect_values": [
                    {"base_value": 44, "effect_type": "scalar", "effect_coefficient": 0.049358, "allocation_type": "rating_multiplier"},
                    {"base_value": 750, "effect_type": "scalar", "effect_coefficient": 0.839092, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 329
        },
        "limit": "Unique-Equipped: Idol of the Aspects (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193005,
        "name": "Idol of the Dreamer",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon1_color2.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Idol of the Dreamer",
                "id": 376638,
                "description": "Equip: Your spells and abilities have a chance to grant *44 Haste per Ysemerald you have equipped. Upon reaching 18 stacks, all stacks are consumed and you gain *750 secondary stats, split evenly for 15 sec.\r\n",
                "effect_values": [
                    {"base_value": 44, "effect_type": "scalar", "effect_coefficient": 0.049358, "allocation_type": "rating_multiplier"},
                    {"base_value": 750, "effect_type": "scalar", "effect_coefficient": 0.839092, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 329
        },
        "limit": "Unique-Equipped: Idol of the Aspects (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193006,
        "name": "Idol of the Earth-Warder",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_statue_color5.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Idol of the Earth-Warder",
                "id": 376636,
                "description": "Equip: Your spells and abilities have a chance to grant *44 Mastery per Neltharite you have equipped. Upon reaching 18 stacks, all stacks are consumed and you gain *750 secondary stats, split evenly for 15 sec.",
                "effect_values": [
                    {"base_value": 44, "effect_type": "scalar", "effect_coefficient": 0.049358, "allocation_type": "rating_multiplier"},
                    {"base_value": 750, "effect_type": "scalar", "effect_coefficient": 0.839092, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 329
        },
        "limit": "Unique-Equipped: Idol of the Aspects (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193003,
        "name": "Idol of the Life-Binder",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon2_color2.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Idol of the Life-Binder",
                "id": 376642,
                "description": "Equip: Your spells and abilities have a chance to grant *44 Critical Strike per Alexstraszite you have equipped. Upon reaching 18 stacks, all stacks are consumed and you gain *750 secondary stats, split evenly for 15 sec.",
                "effect_values": [
                    {"base_value": 44, "effect_type": "scalar", "effect_coefficient": 0.049358, "allocation_type": "rating_multiplier"},
                    {"base_value": 750, "effect_type": "scalar", "effect_coefficient": 0.839092, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 329
        },
        "limit": "Unique-Equipped: Idol of the Aspects (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 133201,
        "name": "Sea Star",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_datacrystal05.jpg",
        "base_item_level": 428,
        "quality": "Rare",
        "effects": [
            {
                "name": "Leviathan's Wisdom",
                "id": 91136,
                "description": "Equip: Your spells have a chance to invigorate the star, increasing your Intellect by *1,431 for 15 sec.",
                "effect_values": [
                    {"base_value": 1431, "effect_type": "scalar", "effect_coefficient": 1.415952, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Versatility": 572
        },
        "limit": "Unique-Equipped: Sea Star (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207168,
        "name": "Pip's Emerald Friendship Badge",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/10_2_raidability_green.jpg",
        "base_item_level": 441,
        "quality": "Epic",
        "effects": [
            {
                "name": "Pip's Emerald Friendship Badge",
                "id": 422858,
                "description": "Equip: Join the Dream Team, gaining *236 of Pip's Mastery, Urctos's Versatility, or Aerwynn's Critical Strike based on your current Best Friend.\r\n\r\nYour spells and abilities have a chance to tag in a random new Best Friend, granting you their passive bonus and empowering it to *2,829 before diminishing over 12 sec.",
                "effect_values": [
                    {"base_value": 236, "effect_type": "linear", "scale_factor": 1.051111111, "base_item_level": 441},
                    {"base_value": 2829, "effect_type": "scalar", "effect_coefficient": 2.328225, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 570
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 110004,
        "name": "Coagulated Genesaur Blood",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/ability_creature_poison_06.jpg",
        "base_item_level": 44,
        "quality": "Rare",
        "effects": [
            {
                "name": "Coagulated Genesaur Blood",
                "id": 429244,
                "description": "Equip: Your spells have a chance to stir the Primal blood, granting *25 Critical Strike for 10 sec.",
                "effect_values": [
                    {"base_value": 25, "effect_type": "scalar", "effect_coefficient": 1.830916, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 5
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 191491,
        "name": "Sustaining Alchemist Stone",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_alchemystone_color2.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Sustaining Alchemist Stone",
                "id": 375844,
                "description": "Equip: Your spells and abilities have a chance to increase your primary stat by *925 for 10 sec and extend the duration of your active phial by 60 sec.",
                "effect_values": [
                    {"base_value": 925, "effect_type": "scalar", "effect_coefficient": 1.405902, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Versatility": 447
        },
        "limit": "Unique-Equipped: Alchemist Stone (1)",
        "enchantments": [],
        "gems": [],
    },
    {
        "id": 191492,
        "name": "Alacritous Alchemist Stone",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_alchemystone_color1.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Alacritous Alchemist Stone",
                "id": 375626,
                "description": "Equip: Your spells and abilities have a chance to increase your primary stat by *772 for 10 sec and reduce the cooldown of your combat potions by 10 sec.",
                "effect_values": [
                    {"base_value": 772, "effect_type": "scalar", "effect_coefficient": 1.172515, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Haste": 447
        },
        "limit": "Unique-Equipped: Alchemist Stone (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 202116,
        "name": "Alacritous Alchemist Stone",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_alchemystone_color1.jpg",
        "base_item_level": 405,
        "quality": "Epic",
        "effects": [
            {
                "name": "Alacritous Alchemist Stone",
                "id": 375626,
                "description": "Equip: Your spells and abilities have a chance to increase your primary stat by *772 for 10 sec and reduce the cooldown of your combat potions by 10 sec.",
                "effect_values": [
                    {"base_value": 772, "effect_type": "scalar", "effect_coefficient": 1.172515, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Haste": 510
        },
        "limit": "Unique-Equipped: Alchemist Stone (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 133201,
        "name": "Sea Star",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_datacrystal05.jpg",
        "base_item_level": 428,
        "quality": "Rare",
        "effects": [
            {
                "name": "Leviathan's Wisdom",
                "id": 91136,
                "description": "Equip: Your spells have a chance to invigorate the star, increasing your Intellect by *1,431 for 15 sec.",
                "effect_values": [
                    {"base_value": 1431, "effect_type": "scalar", "effect_coefficient": 1.415952, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Versatility": 572
        },
        "limit": "Unique-Equipped: Sea Star (1)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 156036,
        "name": "Eye of the Broodmother",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_eye_02.jpg",
        "base_item_level": 35,
        "quality": "Epic",
        "effects": [
            {
                "name": "Eye of the Broodmother",
                "id": 65007,
                "description": "Equip: Your spells grant *1 Intellect for 10 sec, stacking up to 5 times.",
                "effect_values": [
                    {"base_value": 1, "effect_type": "scalar", "effect_coefficient": 0.10503, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Critical Strike": 5
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207170,
        "name": "Smoldering Seedling",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_treepet.jpg",
        "base_item_level": 441,
        "quality": "Epic",
        "effects": [
            {
                "name": "Smoldering Seedling",
                "id": 422083,
                "description": "Use: Replant the Seedling and attempt to put out its flames for 12 sec. Healing the Seedling also heals up to 5 injured allies for the same amount, split evenly. Healing is increased for each ally until *481,562 additional healing is provided.<br><br>If the Seedling is still alive after 12 sec, receive *630 Mastery for 10 sec as thanks. (2 Min Cooldown)",
                "effect_values": [
                    {"base_value": 481562, "effect_type": "scalar", "effect_coefficient": 561.229515, "allocation_type": "flat_healing"},
                    {"base_value": 630, "effect_type": "scalar", "effect_coefficient": 0.518729, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 570
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207171,
        "name": "Blossom of Amirdrassil",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
        "base_item_level": 441,
        "quality": "Epic",
        "effects": [
            {
                "name": "Blossom of Amirdrassil",
                "id": 423418,
                "description": "Equip: Healing an ally below 80% health grants them Blossom of Amirdrassil, healing for *210,597 over 6 sec. This effect may occur once per minute.<br><br>If the target is above 95% health when this effect expires, the Blossom spreads to 3 injured allies to heal for *105,294 over 6 sec. If the target is not fully healed, the Blossom blooms to absorb *315,890 damage instead.",
                "effect_values": [
                    {"base_value": 210597, "effect_type": "scalar", "effect_coefficient": 40.9063 * 6, "allocation_type": "flat_healing"},
                    {"base_value": 105294, "effect_type": "scalar", "effect_coefficient": 20.45229 * 6, "allocation_type": "flat_healing"},
                    {"base_value": 315890, "effect_type": "scalar", "effect_coefficient": 368.1498, "allocation_type": "flat_healing"}
                ]
            }
        ],
        "stats": {
            "Haste": 608
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207581,
        "name": "Mirror of Fractured Tomorrows",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/achievement_dungeon_ulduarraid_misc_06.jpg",
        "base_item_level": 421,
        "quality": "Epic",
        "effects": [
            {
                "name": "Mirror of Fractured Tomorrows",
                "id": 418527,
                "description": "Use: Gaze into the mirror's depths, inviting a version of your future self to fight alongside you for 20 sec, casting healing spells for *25,000. In addition, you grant yourself *2,789 of your highest secondary stat. (3 Min Cooldown)",
                "effect_values": [
                    {"base_value": 25000, "effect_type": "scalar", "effect_coefficient": 34.791132, "allocation_type": "flat_healing"},
                    {"base_value": 2789, "effect_type": "linear", "scale_factor": 13.684, "base_item_level": 421},
                ]
            }
        ],
        "stats": {
            "Intellect": 473
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 190526,
        "name": "Allied Wristguard of Companionship",
        "item_slot": "Wrist",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_bracer_plate_raidwarriorprimalist_d_01.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Allied Wristgaurds of Companionship", 
                "description": "Grants *46 Versatility for every ally in a 30 yard radius, stacking up to 4 times.", 
                "id": 395959,
                "type": "embellishment",
                "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 382, "base_value": 46, "effect_coefficient": 0.052152, "effect_type": "scalar"}]
            }
        ],
        "stats": {
            "Intellect": 195,
            "Stamina": 590,
            "Critical Strike": 146,
            "Haste": 206
        },
        "limit": "Unique-Equipped: Embellished (2)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193001,
        "name": "Elemental Lariat",
        "item_slot": "Neck",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_necklace_necklace1_color3.jpg",
        "base_item_level": 382,
        "quality": "Epic",
        "effects": [
            {
                "name": "Elemental Lariat", 
                "description": "Your spells and abilities have a chance to empower one of your socketed elemental gems, granting *407 of their associated stat. Lasts 5 sec and an additional 1 sec per elemental gem.", 
                "id": 375323,
                "type": "embellishment",
                "effect_values": [{"allocation_type": "rating_multiplier_jewellery", "base_item_level": 382, "base_value": 407, "effect_coefficient": 0.458195, "effect_type": "scalar"}]
            }
        ],
        "stats": {
            "Stamina": 590,
            "Versatility": 438,
            "Mastery": 438
        },
        "limit": "Unique-Equipped: Embellished (2)",
        "enchantments": [],
        "gems": []
    },
    {
        "id": 208615,
        "name": "Nymue's Unraveling Spindle",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_cloth_outdooremeralddream_d_01_buckle.jpg",
        "base_item_level": 441,
        "quality": "Epic",
        "effects": [
            {
                "name": "Nymue's Unraveling Spindle",
                "id": 422956,
                "description": "Use: Channel to unravel your target's essence, dealing 223,000 Nature damage over 3 sec and granting you up to *2,750 Mastery for 18 sec. \r\n\r\nDamage increased by 30% against immobilized targets. (2 Min Cooldown)",
                "effect_values": [
                    {"base_value": 2750, "effect_type": "scalar", "effect_coefficient": 2.263035, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 570
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 194300,
        "name": "Conjured Chillglobe",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_specialreagentfoozles_primalistrune_frost.jpg",
        "base_item_level": 389,
        "quality": "Epic",
        "effects": [
            {
                "name": "Conjured Chillglobe",
                "id": 396391,
                "description": "Use: If your mana is above 65%, toss the Chillglobe at your target, inflicting *51,980 Frost damage.\r\n\r\nIf your mana is below 65%, instead drink from the Chillglobe to restore *3,521 mana instantly. (1 Min Cooldown)",
                "effect_values": [
                    {"base_value": 51981, "effect_type": "scalar", "effect_coefficient": 133.4993, "allocation_type": "flat_healing"},
                    {"base_value": 3521, "effect_type": "scalar", "effect_coefficient": 9.0419, "allocation_type": "flat_healing"},
                ]
            }
        ],
        "stats": {
            "Intellect": 351
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
];

export default itemDataEffects;