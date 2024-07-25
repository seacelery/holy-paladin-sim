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

    "Quick Emerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg",
    "Deadly Emerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg",
    "Masterful Emerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg",
    "Versatile Emerald": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg",

    "Quick Ruby": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg",
    "Deadly Ruby": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg",
    "Masterful Ruby": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg",
    "Versatile Ruby": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg",

    "Quick Onyx": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg",
    "Deadly Onyx": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg",
    "Masterful Onyx": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg",
    "Versatile Onyx": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg",

    "Quick Sapphire": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg",
    "Deadly Sapphire": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg",
    "Masterful Sapphire": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg",
    "Versatile Sapphire": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg",

    "Cubic Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg",
    "Elusive Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg",
    "Insightful Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg",
    "Culminating Blasphemite": "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg",
};

const groupedGems = {
    "Emerald": {
        "label": "Haste",
        "gems": [
            ["Quick Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+227 Haste"],
            ["Deadly Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Haste", "+127 Crit"],
            ["Masterful Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Haste", "+127 Mastery"],
            ["Versatile Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Haste", "+127 Versatility"],
            ["Cubic Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg", "+121 Intellect"],
        ]
    },
    "Ruby": {
        "label": "Crit",
        "gems": [
            ["Quick Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Crit", "+127 Haste"],
            ["Deadly Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+227 Crit"],
            ["Masterful Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Crit", "+127 Mastery"],
            ["Versatile Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Crit", "+127 Versatility"],
            ["Elusive Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg", "+121 Intellect"],
        ]
    },
    "Onyx": {
        "label": "Mastery",
        "gems": [
            ["Quick Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Mastery", "+127 Haste"],
            ["Deadly Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Mastery", "+127 Crit"],
            ["Masterful Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+227 Mastery"],
            ["Versatile Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Mastery", "+127 Versatility"],
            ["Insightful Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg", "+121 Intellect"],         
        ]
    },
    "Sapphire": {
        "label": "Versatility",
        "gems": [
            ["Quick Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Versatility", "+127 Haste"],
            ["Deadly Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Versatility", "+127 Crit"],
            ["Masterful Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Versatility", "+127 Mastery"],
            ["Versatile Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+227 Versatility"],
            ["Culminating Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg", "+121 Intellect"],
        ]
    },
};

const ptrGroupedGems = {
    "Emerald": {
        "label": "Haste",
        "gems": [
            ["Quick Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+227 Haste"],
            ["Deadly Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Haste", "+127 Crit"],
            ["Masterful Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Haste", "+127 Mastery"],
            ["Versatile Emerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Haste", "+127 Versatility"],
            ["Cubic Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_stone_01.jpg", "+121 Intellect"],
        ]
    },
    "Ruby": {
        "label": "Crit",
        "gems": [
            ["Quick Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Crit", "+127 Haste"],
            ["Deadly Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+227 Crit"],
            ["Masterful Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Crit", "+127 Mastery"],
            ["Versatile Ruby", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Crit", "+127 Versatility"],
            ["Elusive Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_gem_x4_metagem_cut.jpg", "+121 Intellect"],
        ]
    },
    "Onyx": {
        "label": "Mastery",
        "gems": [
            ["Quick Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Mastery", "+127 Haste"],
            ["Deadly Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Mastery", "+127 Crit"],
            ["Masterful Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+227 Mastery"],
            ["Versatile Onyx", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+190 Mastery", "+127 Versatility"],
            ["Insightful Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/inv_misc_metagem_b.jpg", "+121 Intellect"],         
        ]
    },
    "Sapphire": {
        "label": "Versatility",
        "gems": [
            ["Quick Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+190 Versatility", "+127 Haste"],
            ["Deadly Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+190 Versatility", "+127 Crit"],
            ["Masterful Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+190 Versatility", "+127 Mastery"],
            ["Versatile Sapphire", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+227 Versatility"],
            ["Culminating Blasphemite", "https://wow.zamimg.com/images/wow/icons/large/item_cutmetagemb.jpg", "+121 Intellect"],
        ]
    },
};

export { itemsToIconsMap, groupedGems, ptrGroupedGems };