const flasks = {
    "Flask of Tempered Swiftness": {effect: "Increases your Haste by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_green.jpg"},
    "Flask of Tempered Aggression": {effect: "Increases your Critical Strike by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_red.jpg"},
    "Flask of Tempered Mastery": {effect: "Increases your Mastery by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_purlple.jpg"},
    "Flask of Tempered Versatility": {effect: "Increases your Versatility by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_blue.jpg"},
    "Flask of Alchemical Chaos": {effect: "Drink to increase a random secondary stat by 4,082 at the cost of 340 of two other secondary stats. These effects are randomized again every 30 sec.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_orange.jpg"},
    "Flask of Saving Graces": {effect: "Directly healing an ally player that is below 25% health grants 15% increased healing done for 10 sec.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potione4.jpg"}
};

const ptrFlasks = {
    "Flask of Tempered Swiftness": {effect: "Increases your Haste by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_green.jpg"},
    "Flask of Tempered Aggression": {effect: "Increases your Critical Strike by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_red.jpg"},
    "Flask of Tempered Mastery": {effect: "Increases your Mastery by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_purlple.jpg"},
    "Flask of Tempered Versatility": {effect: "Increases your Versatility by 3,323.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_blue.jpg"},
    "Flask of Alchemical Chaos": {effect: "Drink to increase a random secondary stat by 4,082 at the cost of 340 of two other secondary stats. These effects are randomized again every 30 sec.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_potion_orange.jpg"},
    "Flask of Saving Graces": {effect: "Directly healing an ally player that is below 25% health grants 15% increased healing done for 10 sec.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potione4.jpg"}
};

// const foodItems = {
//     "Grand Banquet of the Kalu'ak": {effect: "Increases your Intellect by 75.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_10_grandbanquet.jpg"},
//     "Timely Demise": {effect: "Increases your Haste by 105.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_seedbatteredfishplate.jpg"},
//     "Filet of Fangs": {effect: "Increases your Critical Strike by 105.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_cooked_eternalblossomfish.jpg"},
//     "Seamoth Surprise": {effect: "Increases your Versatility by 105.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_82.jpg"},
//     "Salt-Baked Fishcake": {effect: "Increases your Mastery by 105.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_deepfriedmossgill.jpg"},
//     "Feisty Fish Sticks": {effect: "Increases your Haste and Critical Strike by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_164_fish_seadog.jpg"},
//     "Aromatic Seafood Platter": {effect: "Increases your Haste and Versatility by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_drogbarstylesalmon.jpg"},
//     "Sizzling Seafood Medley": {effect: "Increases your Haste and Mastery by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_draenor_sturgeonstew.jpg"},
//     "Revenge, Served Cold": {effect: "Increases your Versatility and Critical Strike by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_100_revengeservedcold_color02.jpg"},
//     "Thousandbone Tongueslicer": {effect: "Increases your Mastery and Critical Strike by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_154_fish_77.jpg"},
//     "Great Cerulean Sea": {effect: "Increases your Mastery and Versatility by 67.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_white.jpg"},
// };

const foodItems = {
    "Feast of the Divine Day": {effect: "Increases your Intellect by 446.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_11_cooking_profession_feast_table01.jpg"},
    "The Sushi Special": {effect: "Increases your highest secondary stat by 469.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_tradeskill_cooking_feastofthewater.jpg"},
    "Stuffed Cave Peppers": {effect: "Increases your Intellect by 223 and your Stamina by 446.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_cooking_90_smuggledproduce.jpg"},
    "Marinated Tenderloins": {effect: "Increases your Mastery and Versatility by 235.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_misc_food_meat_cooked_02.jpg"},
    "Chippy Tea": {effect: "Increases your Mastery and Haste by 235.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_deepfriedmossgill.jpg"},
    "Deepfin Patty": {effect: "Increases your Haste and Critical Strike by 235.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_164_fish_seadog.jpg"},
    "Sweet and Spicy Soup": {effect: "Increases your Haste and Versatility by 235.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_drogbarstylesalmon.jpg"},
    "Fish and Chips": {effect: "Increases your Critical Strike and Versatility by 235.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_draenor_sturgeonstew.jpg"},
    "Salt Baked Seafood": {effect: "Increases your Mastery and Critical Strike by 235.", image: "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_100_revengeservedcold_color02.jpg"},
};

const weaponImbues = {
    "Algari Mana Oil": {effect: "Increases your Critical Strike and Haste by 272.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiond1.jpg"},
    "Oil of Beledar's Grace": {effect: " The oil has a chance to resonate with your healing, healing an additional 13,750 Health to the target.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiond5.jpg"},
};

const ptrWeaponImbues = {
    "Algari Mana Oil": {effect: "Increases your Critical Strike and Haste by 272.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiond1.jpg"},
    "Oil of Beledar's Grace": {effect: " The oil has a chance to resonate with your healing, healing an additional 13,750 Health to the target.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiond5.jpg"},
};

const augmentRunes = {
    "Crystallized Augment Rune": {effect: "Increases your Intellect by 733.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_10_enchanting_crystal_color5.jpg"},
};

const ptrAugmentRunes = {
    "Crystallized Augment Rune": {effect: "Increases your Intellect by 733.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_10_enchanting_crystal_color5.jpg"},
};

const raidBuffs = {
    "Arcane Intellect": {effect: "Increases your Intellect by 3%.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_magicalsentry.jpg"},
    "Mark of the Wild": {effect: "Increases your Versatility by 3%.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_regeneration.jpg"},
    // "Retribution Aura": {effect: "When any party or raid member within 40 yds takes more than 30% of their health in damage in a single hit, each member gains 5% increased damage and healing, decaying over 30 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg"},
    "Skyfury": {effect: "Increases your Mastery by 2%.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_offhand_1h_artifactdoomhammer_d_02.jpg"},
    "Symbol of Hope": {effect: "Bolster the morale of raid members within 40 yds. They each recover 30 sec of cooldown of a major defensive ability, and regain 10% of their missing mana, over 4 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_symbolofhope.jpg"},
    "Mana Spring Totem": {effect: "Lava Burst and Riptide casts restore 150 mana to you and 4 allies nearest to you within 40 yards.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_manaregentotem.jpg"},
    "Mana Tide Totem": {effect: "Your mana regeneration is increased by 80% for 8 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/ability_shaman_manatidetotem.jpg"}
};

const ptrRaidBuffs = {
    "Arcane Intellect": {effect: "Increases your Intellect by 3%.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_magicalsentry.jpg"},
    "Mark of the Wild": {effect: "Increases your Versatility by 3%.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_regeneration.jpg"},
    // "Retribution Aura": {effect: "When any party or raid member within 40 yds takes more than 30% of their health in damage in a single hit, each member gains 5% increased damage and healing, decaying over 30 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg"},
    "Skyfury": {effect: "Increases your Mastery by 2%.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_offhand_1h_artifactdoomhammer_d_02.jpg"},
    "Symbol of Hope": {effect: "Bolster the morale of raid members within 40 yds. They each recover 30 sec of cooldown of a major defensive ability, and regain 10% of their missing mana, over 4 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_symbolofhope.jpg"},
    "Mana Spring Totem": {effect: "Lava Burst and Riptide casts restore 150 mana to you and 4 allies nearest to you within 40 yards.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_manaregentotem.jpg"},
    "Mana Tide Totem": {effect: "Your mana regeneration is increased by 80% for 8 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/ability_shaman_manatidetotem.jpg"}
};

const externalBuffs = {
    "Power Infusion": {effect: "Increases your Haste by 20% for 15 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_powerinfusion.jpg"},
    "Innervate": {effect: "Your spells do not consume mana for 8 seconds.", image: "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_lightning.jpg"},
    "Source of Magic": {effect: "The evoker restores 0.25% maximum mana to you when they cast an empowered spell.", image: "https://render.worldofwarcraft.com/eu/icons/56/ability_evoker_blue_01.jpg"},
};

const potions = {
    "Algari Mana Potion": {effect: "Restores 270,000 mana.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_flask_blue.jpg"},
    "Slumbering Soul Serum": {effect: "Elevate your focus to restore 375,000 mana over 10 sec, but you are defenseless until your focus is broken.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_flask_green.jpg"},
    "Tempered Potion": {effect: "Gain the effects of all inactive Tempered Flasks, increasing their associated secondary stats by 2168 for 30 sec.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiona4.jpg"},
};

const ptrPotions = {
    "Algari Mana Potion": {effect: "Restores 270,000 mana.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_flask_blue.jpg"},
    "Slumbering Soul Serum": {effect: "Elevate your focus to restore 375,000 mana over 10 sec, but you are defenseless until your focus is broken.", image: "https://wow.zamimg.com/images/wow/icons/large/inv_flask_green.jpg"},
    "Tempered Potion": {effect: "Gain the effects of all inactive Tempered Flasks, increasing their associated secondary stats by 2168 for 30 sec.", image: "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_potiona4.jpg"},
}

export { flasks, ptrFlasks, foodItems, weaponImbues, ptrWeaponImbues, augmentRunes, ptrAugmentRunes, raidBuffs, ptrRaidBuffs, externalBuffs, potions, ptrPotions };