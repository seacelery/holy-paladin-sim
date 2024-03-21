const flasks = {
    "Phial of Tepid Versatility":  {effect: "Increases your Versatility by 745", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_black.jpg"},
    "Phial of Elemental Chaos":  {
        effect: "Infuse yourself with the power of the elements, granting you a random elemental boon that changes every 60 sec Each boon increases a secondary stat by 652 and grants a bonus effect.<br><br>Elemental Chaos: Air - Increases your Haste by 652 and movement speed by 10%.<br>Elemental Chaos: Fire - Increases your Critical Strike by 652 and your damage dealt by critical strikes by 2%.<br>Elemental Chaos: Earth - Increases your Mastery by 652 and reduces your damage taken by 5%.<br>Elemental Chaos: Frost - Increases your Versatility by 652 and your healing done by critical strikes by 2%.", 
        image: "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_orange.jpg"
    },
    "Iced Phial of Corrupting Rage": {effect: "Gain Corrupting Rage which grants 1118 Critical Strike rating After suffering 400% of your health in damage, you are afflicted with Overwhelming Rage instead which causes you to take 25% of your health as Nature damage over 15 sec, after which the cycle begins anew", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_red.jpg"},
};

const foodItems = {
    "Grand Banquet of the Kalu'ak": {effect: "Increases your Intellect by 75", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_10_grandbanquet.jpg"},
    "Timely Demise": {effect: "Increases your Haste by 105", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_seedbatteredfishplate.jpg"},
    "Filet of Fangs": {effect: "Increases your Critical Strike by 105", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_cooked_eternalblossomfish.jpg"},
    "Seamoth Surprise": {effect: "Increases your Versatility by 105", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_82.jpg"},
    "Salt-Baked Fishcake": {effect: "Increases your Mastery by 105", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_deepfriedmossgill.jpg"},
    "Feisty Fish Sticks": {effect: "Increases your Haste and Critical Strike by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_164_fish_seadog.jpg"},
    "Aromatic Seafood Platter": {effect: "Increases your Haste and Versatility by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_drogbarstylesalmon.jpg"},
    "Sizzling Seafood Medley": {effect: "Increases your Haste and Mastery by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_draenor_sturgeonstew.jpg"},
    "Revenge, Served Cold": {effect: "Increases your Versatility and Critical Strike by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_100_revengeservedcold_color02.jpg"},
    "Thousandbone Tongueslicer": {effect: "Increases your Mastery and Critical Strike by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_154_fish_77.jpg"},
    "Great Cerulean Sea": {effect: "Increases your Mastery and Versatility by 67", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_white.jpg"},
};

const weaponImbues = {
    "Buzzing Rune": {effect: "Increases your Critical Strike by 310", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_08.jpg"},
    "Chirping Rune": {effect: "Your healing spells have a high chance to heal your target for an additional 7987 healing", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_09.jpg"},
    "Howling Rune": {effect: "Increases your Haste by 310", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_05.jpg"},
    "Hissing Rune": {effect: "Increases your Mastery by 310", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_09.jpg"},
};

const augmentRunes = {
    "Draconic Augment Rune": {effect: "Increases your Intellect by 87", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting3_rainbowprism_color2.jpg"},
};

const raidBuffs = {
    "Arcane Intellect": {effect: "Increases your Intellect by 5%", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_magicalsentry.jpg"},
    "Mark of the Wild": {effect: "Increases your Versatility by 3%", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_regeneration.jpg"},
    "Close to Heart": {effect: "Your allies within 10 yards take 8% increased healing", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_offhand_1h_pvppandarias2_c_01.jpg"},
    "Retribution Aura": {effect: "When any party or raid member within 40 yds takes more than 30% of their health in damage in a single hit, each member gains 5% increased damage and healing, decaying over 30 sec.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg"},
};

const externalBuffs = {
    "Power Infusion": {effect: "Increases your Haste by 20% for 15 seconds", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_powerinfusion.jpg"},
    "Innervate": {effect: "Your spells do not consume mana for 8 seconds", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_lightning.jpg"},
    "Source of Magic": {effect: "The evoker restores 0.25% maximum mana to you when they cast an empowered spell", image: "https://render.worldofwarcraft.com/eu/icons/56/ability_evoker_blue_01.jpg"},
};

const potions = {
    "Aerated Mana Potion": {effect: "Restores 27600 mana", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape1_blue.jpg"},
    "Elemental Potion of Ultimate Power": {effect: "Increases your Intellect by 886 for 30 seconds", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_dpotion_b20.jpg"},
};

export { flasks, foodItems, weaponImbues, augmentRunes, raidBuffs, externalBuffs, potions };