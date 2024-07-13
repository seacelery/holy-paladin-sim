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
                    {"base_value": 210597, "effect_type": "scalar", "effect_coefficient": 44.99676 * 6, "allocation_type": "flat_healing"},
                    {"base_value": 105294, "effect_type": "scalar", "effect_coefficient": 22.49753 * 6, "allocation_type": "flat_healing"},
                    {"base_value": 315890, "effect_type": "scalar", "effect_coefficient": 404.9657, "allocation_type": "flat_healing"}
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
                "effect_values": [{"allocation_type": "rating_multiplier", "base_item_level": 382, "base_value": 407, "effect_coefficient": 0.458195, "effect_type": "scalar"}]
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
                "description": "Use: If your mana is above 65%, toss the Chillglobe at your target, inflicting *51,980 Frost damage.\r\n\r\nIf your mana is below 65%, instead drink from the Chillglobe to restore *4,590 mana instantly. (1 Min Cooldown)",
                "effect_values": [
                    {"base_value": 51981, "effect_type": "scalar", "effect_coefficient": 133.4993, "allocation_type": "flat_healing"},
                    {"base_value": 4590, "effect_type": "scalar", "effect_coefficient": 4.92373, "allocation_type": "rating_multiplier"},
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
    {
        "id": 204201,
        "name": "Neltharion's Call to Chaos",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_dragon_trinket_5_red.jpg",
        "base_item_level": 431,
        "quality": "Epic",
        "effects": [
            {
                "name": "Neltharion's Call to Chaos",
                "id": 403366,
                "description": "Equip: Your area effect spells and abilities have a chance to grant you *2,109 Intellect and increase damage you receive by 5% for 18 sec.",
                "effect_values": [
                    {"base_value": 2109, "effect_type": "scalar", "effect_coefficient": 1.900139, "allocation_type": "no_multiplier"},
                ]
            }
        ],
        "stats": {
            "Critical Strike": 580
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 194301,
        "name": "Whispering Incarnate Icon",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_necklace_1_omni.jpg",
        "base_item_level": 395,
        "quality": "Epic",
        "effects": [
            {
                "name": "Whispering Incarnate Icon",
                "id": 377452,
                "description": "Equip: Succumb to the Icon's whispers and become Infused with Fire, increasing your Haste by *445. \r\n\r\nFighting alongside allies who are Infused with Earth or Frost has a chance to grant you *241 of their Infusion's stat for 12 sec.\r\n\r\nInfusion based on your current specialization.",
                "effect_values": [
                    {"base_value": 483, "effect_type": "scalar", "effect_coefficient": 0.500103, "allocation_type": "no_multiplier"},
                    {"base_value": 133, "effect_type": "scalar", "effect_coefficient": 0.137528, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 372
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 202612,
        "name": "Screaming Black Dragonscale",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rubysanctum2.jpg",
        "base_item_level": 421,
        "quality": "Epic",
        "effects": [
            {
                "name": "Screaming Flight",
                "id": 401468,
                "description": "Equip: Your attacks and abilities have a chance to grant you ephemeral dragon wings, increasing your Critical Strike by *1,017 and your Leech by *283 for 15 sec.\r\n\r\n",
                "effect_values": [
                    {"base_value": 1017, "effect_type": "scalar", "effect_coefficient": 0.919472, "allocation_type": "rating_multiplier"},
                    {"base_value": 283, "effect_type": "scalar", "effect_coefficient": 0.256105, "allocation_type": "rating_multiplier"}
                ]
            },
        ],
        "stats": {
            "Intellect": 473
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 202614,
        "name": "Rashok's Molten Heart",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_trinket6oih_orb4.jpg",
        "base_item_level": 418,
        "quality": "Epic",
        "effects": [
            {
                "name": "Rashok's Molten Heart",
                "id": 401183,
                "description": "Equip: Your healing spells have a chance to awaken the Heart, restoring *1,494 mana over 10 sec and causing your healing spells to restore *13,591 additional health over 10 sec.\r\n\r\nOverhealing from this effect invigorates your target, granting them up to *421 Versatility for 12 sec.",
                "effect_values": [
                    {"base_value": 1494, "effect_type": "scalar", "effect_coefficient": 0.133174 * 10, "allocation_type": "rating_multiplier"},
                    {"base_value": 13591, "effect_type": "scalar", "effect_coefficient": 2.221365 * 10, "allocation_type": "flat_healing"},
                    {"base_value": 421, "effect_type": "scalar", "effect_coefficient": 0.347837, "allocation_type": "rating_multiplier"},
                ]
            }
        ],
        "stats": {
            "Intellect": 460
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 203729,
        "name": "Ominous Chromatic Essence",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_orb_blue.jpg",
        "base_item_level": 418,
        "quality": "Epic",
        "effects": [
            {
                "name": "Glimmering Chromatic Orb",
                "id": 401513,
                "description": "Equip: Resonate with the power of your sworn dragonflight, granting you *473 secondary stat. Allies sworn to a different dragonflight gain *52 secondary stat from your Resonance. You may only benefit from one Resonance per Flight. \r\n\r\n",
                "effect_values": [
                    {"base_value": 473, "effect_type": "scalar", "effect_coefficient": 0.434074, "allocation_type": "rating_multiplier"},
                    {"base_value": 52, "effect_type": "scalar", "effect_coefficient": 0.046006, "allocation_type": "rating_multiplier"}
                ]
            },
        ],
        "stats": {
            "Intellect": 460
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193718,
        "name": "Emerald Coach's Whistle",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_head_dragon_green.jpg",
        "base_item_level": 250,
        "quality": "Rare",
        "effects": [
            {
                "name": "Emerald Coach's Whistle",
                "id": 383798,
                "description": "Equip: Your helpful spells and abilities have a chance to pep up you and your Coached ally, granting you both *169 Mastery for 10 sec. \r\n",
                "effect_values": [
                    {"base_value": 169, "effect_type": "scalar", "effect_coefficient": 0.780421, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 96
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193791,
        "name": "Time-Breaching Talon",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
        "base_item_level": 250,
        "quality": "Rare",
        "effects": [
            {
                "name": "Time-Breaching Talon",
                "id": 385884,
                "description": "Use: Tear through time and steal power from your future self, gaining *498 Intellect for 20 sec, then losing *158 Intellect for 20 sec. (2 Min 30 Sec Cooldown)",
                "effect_values": [
                    {"base_value": 498, "effect_type": "scalar", "effect_coefficient": 3.477437, "allocation_type": "no_multiplier"},
                    {"base_value": 158, "effect_type": "scalar", "effect_coefficient": 1.391347, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "stats": {
            "Haste": 109
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193773,
        "name": "Spoils of Neltharus",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
        "base_item_level": 250,
        "quality": "Rare",
        "effects": [
            {
                "name": "Spoils of Neltharus",
                "id": 381768,
                "description": "Use: Open the spoils and loot the first item you find to gain its fleeting power, increasing a secondary stat by *547 for 20 sec. (2 Min Cooldown)",
                "effect_values": [
                    {"base_value": 547, "effect_type": "scalar", "effect_coefficient": 2.521002, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 96
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 204465,
        "name": "Voice of the Silent Star",
        "item_slot": "Back",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_cloth_raidpriestdragon_d_01_cape.jpg",
        "base_item_level": 431,
        "quality": "Epic",
        "effects": [
            {
                "name": "The Silent Star",
                "id": 409434,
                "description": "Equip: Whenever nearby allies take damage, the Voice has a chance to beckon you. Upon hearing its call 10 times you fully submit to its influence, stealing *117 of the 4 nearest allies' lowest secondary stat, and giving you the stolen amount plus *1,764 to your highest secondary stat for 8 sec.",
                "effect_values": [
                    {"base_value": 117, "effect_type": "scalar", "effect_coefficient": 0.101511, "allocation_type": "rating_multiplier"},
                    {"base_value": 1764, "effect_type": "scalar", "effect_coefficient": 1.519776, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 307,
            "Critical Strike": 313,
            "Haste": 144
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207788,
        "name": "Vakash, the Shadowed Inferno",
        "item_slot": "One-Hand",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_emeralddreamraid_d_01.jpg",
        "base_item_level": 441,
        "quality": "Epic",
        "effects": [
            {
                "name": "Hungering Shadowflame",
                "id": 424320,
                "description": "Equip: Your spells and abilities have a chance to draw on the corruption within, dealing an additional 16,099 Shadowflame damage to you and your target.\r\n\r\nDamage increased by 400% against enemies above 90% health."
            }
        ],
        "stats": {
            "Intellect": 1747,
            "Stamina": 1112,
            "Haste": 129,
            "Mastery": 297
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 194307,
        "name": "Broodkeeper's Promise",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_trinket_3_omni.jpg",
        "base_item_level": 411,
        "quality": "Epic",
        "effects": [
            {
                "name": "Broodkeeper's Promise",
                "id": 377462,
                "description": "Use: Designate another player to bond with, becoming their Guardian for 1 hour.\r\n\r\nWhile bonded, you and your ally gain *82 Versatility and restore *655 health per second. If you are within 15 yards of one another, these bonuses are increased. \r\n\r\nValid only for healer specializations.\r\n (5 Sec Cooldown)",
                "effect_values": [
                    {"base_value": 82, "effect_type": "scalar", "effect_coefficient": 0.096854 * 0.8, "allocation_type": "rating_multiplier"},
                    {"base_value": 655, "effect_type": "scalar", "effect_coefficient": 1.983667, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "stats": {
            "Intellect": 431
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 193678,
        "name": "Miniature Singing Stone",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_centaur_trinket_1_color1.jpg",
        "base_item_level": 250,
        "quality": "Rare",
        "effects": [
            {
                "name": "Miniature Singing Stone",
                "id": 388881,
                "description": "Use: Unleash the voice of Ohn'ahra to wrap an ally in wind, shielding them for *13,095 damage for 10 sec. When this effect ends the winds disperse and shield up to 4 nearby allies. (2 Min Cooldown)",
                "effect_values": [
                    {"base_value": 13488, "effect_type": "scalar", "effect_coefficient": 101.9246, "allocation_type": "flat_healing"}
                ]
            }
        ],
        "stats": {
            "Intellect": 96
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "id": 207552,
        "name": "Echoing Tyrstone",
        "item_slot": "Trinket",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
        "base_item_level": 421,
        "quality": "Epic",
        "effects": [
            {
                "name": "Echoing Tyrstone",
                "id": 417939,
                "description": "Use: Activate the Tyrstone, recording 30% of your healing done over the next 10 sec, up to *181,431 healing done. (2 Min Cooldown)<br><br>Equip: Whenever you or one of your allies falls below 35% health, the Tyrstone will summon an echo of your past self, healing them for the stored amount split among nearby allies and granting *209 Haste for 15 sec before the record is lost. Deals increased healing when healing multiple allies.",
                "effect_values": [
                    {"base_value": 181431, "effect_type": "scalar", "effect_coefficient": 283.4695, "allocation_type": "flat_healing"},
                    {"base_value": 209, "effect_type": "scalar", "effect_coefficient": 0.189052, "allocation_type": "no_multiplier"}
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
        "id": 195526,
        "name": "Seal of Filial Duty",
        "item_slot": "Finger",
        "icon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_ring_3_fire.jpg",
        "base_item_level": 405,
        "quality": "Epic",
        "effects": [
            {
                "name": "Broodkeeper's Barrier",
                "id": 394455,
                "description": "Equip: Dealing Fire damage has a chance to invigorate you, absorbing 43,270 damage for 6 seconds.\r\n"
            }
        ],
        "stats": {
            "Stamina": 800,
            "Haste": 267,
            "Mastery": 806
        },
        "limit": null,
        "enchantments": [],
        "gems": []
    },
    {
        "effects": [
            {
                "name": "Gruesome Syringe",
                "id": 444276,
                "description": "Equip: Your healing spells have a high chance to cause you to inject yourself with a charge of Volatile Serum. Multiple charges may overlap.\n\nIf an ally drops below 70% health, expel a charge to heal them for *159634. If unconsumed after 15 sec, charges catalyze to grant you *2894 Intellect for 10 sec instead.",
                "effect_values": [
                    {"base_value": 159634, "effect_type": "scalar", "effect_coefficient": 63.84856796265, "allocation_type": "flat_damage"},
                    {"base_value": 2894, "effect_type": "scalar", "effect_coefficient": 0.75579804182, "allocation_type": "no_multiplier"}
                ]
            }
        ],
        "name": "Gruesome Syringe",
        "item_slot": "Trinket",
        "base_item_level": 571,
        "quality": "Epic",
        "id": 212452,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_gruesomesyringe_red.jpg",
        "stats": {
            "Critical Strike": 1001
        },
        "gems": [],
        "enchantments": [],
        "limit": null
    },
    {
        "effects": [
            {
                "name": "Creeping Coagulum",
                "id": 444282,
                // 444271
                "description": "Use: Feed the Coagulum, redirecting 20% of all healing done until *766815.2 healing has been consumed. Once sated, the Coagulum bursts to heal 5 allies for *541371.531.\n\nLingering effluvia causes affected allies' next attacks to deal an additional 444,271 Shadow damage, increased based on overhealing done by the Coagulum. (1 Min, 30 Sec Cooldown)",
                "effect_values": [
                    {"base_value": 766815.2, "effect_type": "scalar", "effect_coefficient": 317.36041259766, "allocation_type": "flat_healing"},
                    {"base_value": 541371.531, "effect_type": "scalar", "effect_coefficient": 2.26054334641, "allocation_type": "flat_healing"}
                ]
            }
        ],
        "name": "Creeping Coagulum",
        "item_slot": "Trinket",
        "base_item_level": 571,
        "quality": "Epic",
        "id": 219917,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_creepingcoagulum_purple.jpg",
        "stats": {
            "Intellect": 1914
        },
        "gems": [],
        "enchantments": [],
        "limit": null
    },
    {
        "effects": [
            {
                "name": "Fateweaved Needle",
                "id": 443384,
                "description": "Equip: Your harmful and helpful spells have a chance to weave a Thread of Fate between your and you target for 5 sec. Tethered allies gain *282 bonus primary while the Thread holds and enemies take *2378 Cosmic Damage when the Thread breaks.",
                "effect_values": [
                    {"base_value": 282, "effect_type": "scalar", "effect_coefficient": 1.44092488289, "allocation_type": "no_multiplier"},
                    {"base_value": 2378, "effect_type": "scalar", "effect_coefficient": 24.16174125671, "allocation_type": "flat_healing"}
                ]
            }
        ],
        "name": "Fateweaved Mallet",
        "item_slot": "One-Hand",
        "base_item_level": 350,
        "quality": "Epic",
        "id": 219941,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/inv_mace_1h_nerubianraid_d_01.jpg",
        "stats": {
            "Intellect": 748
        },
        "gems": [],
        "enchantments": [],
        "limit": null
    },
    {
        "effects": [
            {
                "name": "Ovinax's Mercurial Egg",
                "id": 445066,
                "description": "Equip: Carefully balance the Egg's incubation. While stationary, gain *95 Intellect every 1 sec, up to 30 times. Diminishes while moving. While moving, gain *108 of your highest secondary stat every 1 sec, up to 30 times. Diminishes while stationary.\n\nAdditional stacks above 20 grant 60% reduced benefit.<br><br>Use: Suspend the Egg's incubation state for 20 sec. (2 Min Cooldown",
                "effect_values": [
                    {"base_value": 95, "effect_type": "scalar", "effect_coefficient": 0.02493842691, "allocation_type": "no_multiplier"},
                    {"base_value": 108, "effect_type": "scalar", "effect_coefficient": 0.05418000743, "allocation_type": "rating_multiplier"}
                ]
            }
        ],
        "name": "Ovinax's Mercurial Egg",
        "item_slot": "Trinket",
        "base_item_level": 571,
        "quality": "Epic",
        "id": 220305,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_mercurialegg_purple.jpg",
        "stats": {},
        "gems": [],
        "enchantments": [],
        "limit": null
    },
    {
        "effects": [
            {
                "name": "Empowering Crystal of Anub'ikkaj",
                "id": 449275,
                "description": "Equip: Your spells and abilities have a chance to let loose a nascent empowerment from the crystal, increasing a random secondary stat by *1392 for 20 sec.",
                "effect_values": [
                    {"base_value": 1392, "effect_type": "scalar", "effect_coefficient": 1.15159761906, "allocation_type": "rating_multiplier"},
                ]
            }
        ],
        "name": "Empowering Crystal of Anub'ikkaj",
        "item_slot": "Trinket",
        "base_item_level": 437,
        "quality": "Epic",
        "id": 219312,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/inv_arathordungeon_fragment_color5.jpg",
        "stats": {
            "intellect": 549
        },
        "gems": [],
        "enchantments": [],
        "limit": null
    },
    {
        "effects": [
            {
                "name": "Ascension",
                "id": 455482,
                "description": "Use: Drink from the vial and ascend over 1.5 sec before taking on a new more powerful form increasing your Intellect by *221 and all other stats by *140 but only for 20 sec.",
                "effect_values": [
                    {"base_value": 2256, "effect_type": "scalar", "effect_coefficient": 2.89916276932, "allocation_type": "no_multiplier"},
                    {"base_value": 1205, "effect_type": "scalar", "effect_coefficient": 1.22288262844, "allocation_type": "rating_multiplier"},
                ]
            }
        ],
        "name": "Imperfect Ascendancy Serum",
        "item_slot": "Trinket",
        "base_item_level": 400,
        "quality": "Epic",
        "id": 225654,
        "icon": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_dpotion_a25.jpg",
        "stats": {},
        "gems": [],
        "enchantments": [],
        "limit": null
    },
];

export default itemDataEffects;