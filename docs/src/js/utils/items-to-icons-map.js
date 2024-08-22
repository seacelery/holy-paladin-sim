const itemsToIconsMap = {
    "Energized Malygite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_blue.jpg",
    "Radiant Malygite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_blue.jpg",
    "Zen Malygite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_blue.jpg",
    "Stormy Malygite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_blue.jpg",

    "Crafty Alexstraszite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_red.jpg",
    "Radiant Alexstraszite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_red.jpg",
    "Sensei's Alexstraszite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_red.jpg",
    "Deadly Alexstraszite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_red.jpg",

    "Keen Neltharite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_black.jpg",
    "Sensei's Neltharite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_black.jpg",
    "Zen Neltharite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_black.jpg",
    "Fractured Neltharite": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_black.jpg",

    "Crafty Ysemerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg",
    "Keen Ysemerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg",
    "Quick Ysemerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg",
    "Energized Ysemerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg",

    "Resplendent Illimited Diamond": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_blue.jpg",
    "Fierce Illimited Diamond": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_green.jpg",
    "Inscribed Illimited Diamond": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_red.jpg",
    "Skillful Illimited Diamond": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_black.jpg",

    "Deluging Water Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_elemental_primal_water.jpg",
    "Exuding Steam Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_water.jpg",
    "Wild Spirit Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_elemental_primal_life.jpg",

    "Quick Emerald": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color2.jpg",
    "Deadly Emerald": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_2.jpg",
    "Masterful Emerald": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_3.jpg",
    "Versatile Emerald": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_1.jpg",

    "Quick Ruby": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_3.jpg",
    "Deadly Ruby": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color5.jpg",
    "Masterful Ruby": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_1.jpg",
    "Versatile Ruby": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_2.jpg",

    "Quick Onyx": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_3.jpg",
    "Deadly Onyx": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_2.jpg",
    "Masterful Onyx": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color1.jpg",
    "Versatile Onyx": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_1.jpg",

    "Quick Sapphire": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_3.jpg",
    "Deadly Sapphire": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_2.jpg",
    "Masterful Sapphire": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg",
    "Versatile Sapphire": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg",

    "Cubic Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg",
    "Elusive Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg",
    "Insightful Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg",
    "Culminating Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg",
};

const groupedGems = {
    // "Emerald": {
    //     "label": "Haste",
    //     "gems": [
    //         ["Quick Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color2.jpg", "+227 Haste"],
    //         ["Deadly Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_2.jpg", "+190 Haste", "+127 Crit"],
    //         ["Masterful Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_3.jpg", "+190 Haste", "+127 Mastery"],
    //         ["Versatile Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_1.jpg", "+190 Haste", "+127 Versatility"],
    //         ["Cubic Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg", "+121 Intellect"],
    //     ]
    // },
    // "Ruby": {
    //     "label": "Crit",
    //     "gems": [
    //         ["Quick Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_3.jpg", "+190 Crit", "+127 Haste"],
    //         ["Deadly Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color5.jpg", "+227 Crit"],
    //         ["Masterful Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_1.jpg", "+190 Crit", "+127 Mastery"],
    //         ["Versatile Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_2.jpg", "+190 Crit", "+127 Versatility"],
    //         ["Elusive Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg", "+121 Intellect", "+2% Movement Speed per unique gem colour"],
    //     ]
    // },
    // "Onyx": {
    //     "label": "Mastery",
    //     "gems": [
    //         ["Quick Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_3.jpg", "+190 Mastery", "+127 Haste"],
    //         ["Deadly Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_2.jpg", "+190 Mastery", "+127 Crit"],
    //         ["Masterful Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color1.jpg", "+227 Mastery"],
    //         ["Versatile Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_1.jpg", "+190 Mastery", "+127 Versatility"],
    //         ["Insightful Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg", "+121 Intellect", "+1% Max Mana per unique gem colour"],         
    //     ]
    // },
    // "Sapphire": {
    //     "label": "Versatility",
    //     "gems": [
    //         ["Quick Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_3.jpg", "+190 Versatility", "+127 Haste"],
    //         ["Deadly Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_2.jpg", "+190 Versatility", "+127 Crit"],
    //         ["Masterful Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg", "+190 Versatility", "+127 Mastery"],
    //         ["Versatile Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg", "+227 Versatility"],
    //         ["Culminating Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg", "+121 Intellect", "+0.15% Crit Effect per unique gem colour"],
    //     ]
    // },
    "Emerald": {
        "label": "Haste",
        "gems": [
            ["Quick Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color2.jpg", "+227 Haste"],
            ["Deadly Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_2.jpg", "+190 Haste", "+127 Crit"],
            ["Masterful Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_3.jpg", "+190 Haste", "+127 Mastery"],
            ["Versatile Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_1.jpg", "+190 Haste", "+127 Versatility"],
            ["Cubic Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg", "+121 Intellect"],
        ]
    },
    "Ruby": {
        "label": "Crit",
        "gems": [
            ["Quick Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_3.jpg", "+190 Crit", "+127 Haste"],
            ["Deadly Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color5.jpg", "+227 Crit"],
            ["Masterful Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_1.jpg", "+190 Crit", "+127 Mastery"],
            ["Versatile Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_2.jpg", "+190 Crit", "+127 Versatility"],
            ["Elusive Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg", "+121 Intellect", "+2% Movement Speed per unique gem colour"],
        ]
    },
    "Onyx": {
        "label": "Mastery",
        "gems": [
            ["Quick Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_3.jpg", "+190 Mastery", "+127 Haste"],
            ["Deadly Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_2.jpg", "+190 Mastery", "+127 Crit"],
            ["Masterful Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color1.jpg", "+227 Mastery"],
            ["Versatile Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_1.jpg", "+190 Mastery", "+127 Versatility"],
            ["Insightful Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg", "+121 Intellect", "+1% Max Mana per unique gem colour"],         
        ]
    },
    "Sapphire": {
        "label": "Versatility",
        "gems": [
            ["Quick Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_3.jpg", "+190 Versatility", "+127 Haste"],
            ["Deadly Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_2.jpg", "+190 Versatility", "+127 Crit"],
            ["Masterful Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg", "+190 Versatility", "+127 Mastery"],
            ["Versatile Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color3.jpg", "+227 Versatility"],
            ["Culminating Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg", "+121 Intellect", "+0.15% Crit Effect per unique gem colour"],
        ]
    },
};

const ptrGroupedGems = {
    "Emerald": {
        "label": "Haste",
        "gems": [
            ["Quick Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color2.jpg", "+227 Haste"],
            ["Deadly Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_2.jpg", "+190 Haste", "+127 Crit"],
            ["Masterful Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_3.jpg", "+190 Haste", "+127 Mastery"],
            ["Versatile Emerald", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color1_1.jpg", "+190 Haste", "+127 Versatility"],
            ["Cubic Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg", "+121 Intellect"],
        ]
    },
    "Ruby": {
        "label": "Crit",
        "gems": [
            ["Quick Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_3.jpg", "+190 Crit", "+127 Haste"],
            ["Deadly Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color5.jpg", "+227 Crit"],
            ["Masterful Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_1.jpg", "+190 Crit", "+127 Mastery"],
            ["Versatile Ruby", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color4_2.jpg", "+190 Crit", "+127 Versatility"],
            ["Elusive Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg", "+121 Intellect", "+2% Movement Speed per unique gem colour"],
        ]
    },
    "Onyx": {
        "label": "Mastery",
        "gems": [
            ["Quick Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_3.jpg", "+190 Mastery", "+127 Haste"],
            ["Deadly Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_2.jpg", "+190 Mastery", "+127 Crit"],
            ["Masterful Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color1.jpg", "+227 Mastery"],
            ["Versatile Onyx", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color2_1.jpg", "+190 Mastery", "+127 Versatility"],
            ["Insightful Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg", "+121 Intellect", "+1% Max Mana per unique gem colour"],         
        ]
    },
    "Sapphire": {
        "label": "Versatility",
        "gems": [
            ["Quick Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_3.jpg", "+190 Versatility", "+127 Haste"],
            ["Deadly Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_2.jpg", "+190 Versatility", "+127 Crit"],
            ["Masterful Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem-hybrid_color5_1.jpg", "+190 Versatility", "+127 Mastery"],
            ["Versatile Sapphire", "https://wow.zamimg.com/images/wow/icons/large/inv_jewelcrafting_cut-standart-gem_color3.jpg", "+227 Versatility"],
            ["Culminating Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg", "+121 Intellect", "+0.15% Crit Effect per unique gem colour"],
        ]
    },
};

export { itemsToIconsMap, groupedGems, ptrGroupedGems };