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
};

const groupedGems = {
    "Ysemerald": {
        "label": "Haste",
        "gems": [
            ["Quick Ysemerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_green.jpg", "+88 Haste"],
            ["Crafty Ysemerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_green.jpg", "+70 Haste", "+33 Crit"],
            ["Keen Ysemerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_green.jpg", "+70 Haste", "+33 Mastery"],
            ["Energized Ysemerald", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_green.jpg", "+70 Haste", "+33 Versatility"],
            ["Fierce Illimited Diamond", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_green.jpg", "+66 Haste", "+75 Intellect"],
        ]
    },
    "Alexstraszite": {
        "label": "Crit",
        "gems": [
            ["Crafty Alexstraszite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_red.jpg", "+70 Crit", "+33 Haste"],
            ["Deadly Alexstraszite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_red.jpg", "+88 Crit"],
            ["Sensei's Alexstraszite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_red.jpg", "+70 Crit", "+33 Mastery"],  
            ["Radiant Alexstraszite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_red.jpg", "+70 Crit", "+33 Versatility"],            
            ["Inscribed Illimited Diamond", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_red.jpg", "+66 Crit", "+75 Intellect"],
        ]
    },
    "Neltharite": {
        "label": "Mastery",
        "gems": [
            ["Keen Neltharite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_black.jpg", "+70 Mastery", "+33 Haste"],
            ["Sensei's Neltharite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_black.jpg", "+70 Mastery", "+33 Crit"],
            ["Fractured Neltharite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_black.jpg", "+88 Mastery"],
            ["Zen Neltharite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_black.jpg", "+70 Mastery", "+33 Versatility"],
            ["Skillful Illimited Diamond", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_black.jpg", "+66 Mastery", "+75 Intellect"],           
        ]
    },
    "Malygite": {
        "label": "Versatility",
        "gems": [
            ["Energized Malygite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_air_cut_blue.jpg", "+70 Versatility", "+33 Haste"],
            ["Radiant Malygite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_fire_cut_blue.jpg", "+70 Versatility", "+33 Crit"],
            ["Zen Malygite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_earth_cut_blue.jpg", "+70 Versatility", "+33 Mastery"],
            ["Stormy Malygite", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem2standard_frost_cut_blue.jpg", "+88 Versatility"],
            ["Resplendent Illimited Diamond", "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_gem3primal_cut_blue.jpg", "+66 Versatility", "+75 Intellect"],
        ]
    },
};

export { itemsToIconsMap, groupedGems };