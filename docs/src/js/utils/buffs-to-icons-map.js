const buffsToIconsMap = {
    // paladin buffs
    "Afterimage": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Aura Mastery": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_auramastery.jpg",
    "Avenging Crusader": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_veneration.jpg",
    "Avenging Crusader (Awakening)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_veneration.jpg",
    "Avenging Wrath": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_avenginewrath.jpg",
    "Avenging Wrath (Awakening)": "custom-icons/avenging-wrath-awakening.png",
    "Awakening": "https://render.worldofwarcraft.com/eu/icons/56/inv_helm_plate_raidpaladin_n_01.jpg",
    "Awakening Ready": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_judgementofthepure.jpg",
    "Barrier of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_barrieroffaith.jpg",
    "Beacon of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconsoflight.jpg",
    "Beacon of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconoflight.jpg",
    "Beacon of Virtue": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconofinsight.jpg",
    "Bestow Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_sheathoflight.jpg",
    "Blessed Assurance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_blessedlife.jpg",
    "Blessing of An'she": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holynova.jpg",
    "Blessing of Autumn": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_autumn.jpg",
    "Blessing of Dawn": "https://render.worldofwarcraft.com/eu/icons/56/achievement_zone_valeofeternalblossoms.jpg",
    "Blessing of Dusk": "https://render.worldofwarcraft.com/eu/icons/56/achievement_zone_newshadowmoonvalley.jpg",
    "Blessing of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconoflight.jpg",
    "Blessing of Spring": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_spring.jpg",
    "Blessing of Summer": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_summer.jpg",
    "Blessing of Winter": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_winter.jpg",
    "Blessing of the Forge": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_lightsmithpaladin_sacredweapon.jpg",
    "Dawnlight": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_heraldofthesunpaladin_dawnlight.jpg",
    "Dawnlight (HoT)": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_heraldofthesunpaladin_dawnlight.jpg",
    "Divine Favor": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_heal.jpg",
    "Divine Guidance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_lightsgrace.jpg",
    "Divine Purpose": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divinepurpose.jpg",
    "Divine Resonance": "https://render.worldofwarcraft.com/eu/icons/56/ability_mount_goatmountwhite.jpg",
    "Embrace of Pa'ku": "https://render.worldofwarcraft.com/eu/icons/56/ability_racial_embraceoftheloa_paku.jpg",
    "Empyrean Legacy": "https://render.worldofwarcraft.com/eu/icons/56/item_holyspark.jpg",
    "Empyrean Legacy Cooldown": "custom-icons/empyrean-legacy-cooldown.png",
    "Eternal Flame": "https://render.worldofwarcraft.com/eu/icons/56/inv_torch_thrown.jpg",
    "Eternal Flame (HoT)": "https://render.worldofwarcraft.com/eu/icons/56/inv_torch_thrown.jpg",
    "Fading Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_shadow_sealofkings.jpg",
    "Fireblood": "https://render.worldofwarcraft.com/eu/icons/56/ability_racial_fireblood.jpg",
    "First Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_lightsgrace.jpg",
    "Gift of the Naaru": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyprotection.jpg",
    "Gleaming Rays": "https://wow.zamimg.com/images/wow/icons/large/spell_priest_power-word.jpg",
    "Glimmer of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_toweroflight.jpg",
    "Hand of Divinity": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_vindication.jpg",
    "Holy Bulwark": "https://render.worldofwarcraft.com/eu/icons/56/inv_shield_1h_artifactnorgannon_d_06.jpg",
    "Holy Reverberation": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_holybolts01.jpg",
    "Infusion of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_infusionoflight.jpg",
    "Liberation": "https://wow.zamimg.com/images/wow/icons/large/ability_paladin_bladeofjusticeblue.jpg",
    "Light of the Martyr": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
    "Maraad's Dying Breath": "https://render.worldofwarcraft.com/eu/icons/56/paladin_icon_speedoflight.jpg",
    "Merciful Auras": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_blessedlife.jpg",
    "Morning Star": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_persecution.jpg",
    "Overflowing Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyguidance.jpg",
    "Power of the Silver Hand": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_blessedhands.jpg",
    "Power of the Silver Hand Stored Healing": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_blessedhands.jpg",
    "Pure Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_sacredcleansing.jpg",
    "Relentless Inquisitor": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_mindvision.jpg",
    "Rising Sunlight": "https://render.worldofwarcraft.com/eu/icons/56/spell_priest_divinestar_holy.jpg",
    "Rite of Adjuration": "https://render.worldofwarcraft.com/eu/icons/56/inv_inscription_armorscroll02.jpg",
    "Rite of Sanctification": "https://render.worldofwarcraft.com/eu/icons/56/inv_inscription_weaponscroll01.jpg",
    "Sacred Weapon": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_artifactnorgannon_d_06.jpg",
    "Saved by the Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Strength of Conviction": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_eyeforaneye.jpg",
    "Solar Grace": "https://render.worldofwarcraft.com/eu/icons/56/ability_malkorok_blightofyshaarj_yellow.jpg",
    "Sun's Avatar": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_holyavenger.jpg",
    "Sun's Avatar Active": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_holyavenger.jpg",
    "Sun Sear": "https://render.worldofwarcraft.com/eu/icons/56/spell_priest_burningwill.jpg",
    "Time Warp": "https://render.worldofwarcraft.com/eu/icons/56/ability_mage_timewarp.jpg",
    "Tyr's Deliverance": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_2h_artifactsilverhand_d_01.jpg",
    "Tyr's Deliverance (self)": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_2h_artifactsilverhand_d_01.jpg",
    "Tyr's Deliverance (target)": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_2h_artifactsilverhand_d_01.jpg",
    "Unending Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holybolt.jpg",
    "Untempered Dedication": "https://render.worldofwarcraft.com/eu/icons/56/achievement_admiral_of_the_light.jpg",
    "Veneration": "https://render.worldofwarcraft.com/eu/icons/56/ability_crown_of_the_heavens_icon.jpg",

    // consumables
    "Elemental Potion of Ultimate Power": "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_dpotion_b20.jpg",
    "Slumbering Soul Serum": "https://wow.zamimg.com/images/wow/icons/large/inv_flask_green.jpg",
    "Tempered Potion": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_potiona4.jpg",
    "Phial of Tepid Versatility": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_black.jpg",
    "Phial of Elemental Chaos": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_orange.jpg",
    "Elemental Chaos: Air": "https://render.worldofwarcraft.com/eu/icons/56/ability_druid_galewinds.jpg",
    "Elemental Chaos: Fire": "https://render.worldofwarcraft.com/eu/icons/56/ability_mage_livingbomb.jpg",
    "Elemental Chaos: Earth": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_volatileearth.jpg",
    "Elemental Chaos: Frost": "https://wow.zamimg.com/images/wow/icons/large/spell_frost_ice-shards.jpg",
    "Iced Phial of Corrupting Rage": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape2_red.jpg",
    "Corrupting Rage": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_shamanrage.jpg",
    "Flask of Saving Graces": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_potione4.jpg",
    "Saving Graces": "https://wow.zamimg.com/images/wow/icons/large/inv_pet_achievement_captureapetatlessthan5health.jpg",
    "Flask of Alchemical Chaos": "https://wow.zamimg.com/images/wow/icons/large/inv_potion_orange.jpg",
    "Alchemical Chaos: Air": "https://render.worldofwarcraft.com/eu/icons/56/ability_druid_galewinds.jpg",
    "Alchemical Chaos: Fire": "https://render.worldofwarcraft.com/eu/icons/56/ability_mage_livingbomb.jpg",
    "Alchemical Chaos: Earth": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_volatileearth.jpg",
    "Alchemical Chaos: Frost": "https://wow.zamimg.com/images/wow/icons/large/spell_frost_ice-shards.jpg",
    "Flask of Tempered Aggression": "https://wow.zamimg.com/images/wow/icons/large/inv_potion_red.jpg",
    "Flask of Tempered Mastery": "https://wow.zamimg.com/images/wow/icons/large/inv_potion_purlple.jpg",
    "Flask of Tempered Swiftness": "https://wow.zamimg.com/images/wow/icons/large/inv_potion_green.jpg",
    "Flask of Tempered Versatility": "https://wow.zamimg.com/images/wow/icons/large/inv_potion_blue.jpg",
    "Draconic Augment Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting3_rainbowprism_color2.jpg",
    "Crystallized Augment Rune": "https://wow.zamimg.com/images/wow/icons/large/inv_10_enchanting_crystal_color5.jpg",
    "Grand Banquet of the Kalu'ak": "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_10_grandbanquet.jpg",
    "Timely Demise": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_seedbatteredfishplate.jpg",
    "Filet of Fangs": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_cooked_eternalblossomfish.jpg",
    "Seamoth Surprise": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_82.jpg",
    "Salt-Baked Fishcake": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_deepfriedmossgill.jpg",
    "Feisty Fish Sticks": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_164_fish_seadog.jpg",
    "Aromatic Seafood Platter": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_drogbarstylesalmon.jpg",
    "Sizzling Seafood Medley": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_draenor_sturgeonstew.jpg",
    "Revenge, Served Cold": "https://render.worldofwarcraft.com/eu/icons/56/inv_cooking_100_revengeservedcold_color02.jpg",
    "Thousandbone Tongueslicer": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_154_fish_77.jpg",
    "Great Cerulean Sea": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_159_fish_white.jpg",
    "Buzzing Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_08.jpg",
    "Chirping Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_09.jpg",
    "Howling Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_05.jpg",
    "Hissing Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_09.jpg",
    "Algari Mana Oil": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_potiond1.jpg",
    "Oil of Beledar's Grace": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_potiond5.jpg",
    "Potion Bomb of Power": "https://wow.zamimg.com/images/wow/icons/large/inv_10_engineering_explosives_1_color2.jpg",

    // raid buffs
    "Arcane Intellect": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_magicalsentry.jpg",
    "Mark of the Wild": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_regeneration.jpg",
    "Close to Heart": "https://render.worldofwarcraft.com/eu/icons/56/inv_offhand_1h_pvppandarias2_c_01.jpg",
    "Retribution Aura ": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg",
    "Retribution Aura": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg",
    "Skyfury": "https://wow.zamimg.com/images/wow/icons/large/inv_offhand_1h_artifactdoomhammer_d_02.jpg",
    "Mana Spring Totem": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_manaregentotem.jpg",
    "Mana Tide Totem": "https://render.worldofwarcraft.com/eu/icons/56/ability_shaman_manatidetotem.jpg",
    "Symbol of Hope": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_symbolofhope.jpg",

    // external buffs
    "Source of Magic": "https://render.worldofwarcraft.com/eu/icons/56/ability_evoker_blue_01.jpg",
    "Power Infusion": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_powerinfusion.jpg",
    "Innervate": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_lightning.jpg",
    "Shifting Sands": "https://render.worldofwarcraft.com/eu/icons/56/ability_evoker_masterytimewalker.jpg",
    "Ebon Might": "https://render.worldofwarcraft.com/eu/icons/56/spell_sarkareth.jpg",

    // trinkets
    "Mirror of Fractured Tomorrows": "https://render.worldofwarcraft.com/eu/icons/56/achievement_dungeon_ulduarraid_misc_06.jpg",
    "Coagulated Genesaur Blood": "https://render.worldofwarcraft.com/eu/icons/56/ability_creature_poison_06.jpg",
    "Sea Star": "https://render.worldofwarcraft.com/eu/icons/56/inv_datacrystal05.jpg",
    "Sustaining Alchemist Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_alchemystone_color2.jpg",
    "Alacritous Alchemist Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_alchemystone_color1.jpg",
    "Neltharion's Call to Chaos": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_dragon_trinket_5_red.jpg",
    "Screaming Black Dragonscale": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rubysanctum2.jpg",
    "Rashok's Molten Heart": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_trinket6oih_orb4.jpg",
    "Ominous Chromatic Essence": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_orb_blue.jpg",
    "Emerald Coach's Whistle": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_head_dragon_green.jpg",
    "Spoils of Neltharus": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
    "Broodkeeper's Promise": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_trinket_3_omni.jpg",
    "Echoing Tyrstone": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",

    "Time-Breaching Talon ": "https://render.worldofwarcraft.com/eu/icons/56/spell_chargepositive.jpg",
    "Time-Breaching Talon  ": "https://render.worldofwarcraft.com/eu/icons/56/spell_chargenegative.jpg",

    "Incarnate's Mark of Fire": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_necklace_1_omni.jpg",
    "Inspired by Frost and Earth": "https://render.worldofwarcraft.com/eu/icons/56/spell_shaman_spiritlink.jpg",

    "Pip's Emerald Friendship Badge": "https://render.worldofwarcraft.com/eu/icons/56/10_2_raidability_green.jpg",
    "Best Friends with Pip": "https://render.worldofwarcraft.com/eu/icons/56/inv_achievement_raidemeralddream_dreamcouncil.jpg",
    "Best Friends with Pip Empowered": "https://render.worldofwarcraft.com/eu/icons/56/inv_achievement_raidemeralddream_dreamcouncil.jpg",
    "Best Friends with Aerwyn": "https://render.worldofwarcraft.com/eu/icons/56/ui_darkshore_warfront_alliance_dryad.jpg",
    "Best Friends with Aerwyn Empowered": "https://render.worldofwarcraft.com/eu/icons/56/ui_darkshore_warfront_alliance_dryad.jpg",
    "Best Friends with Urctos": "https://render.worldofwarcraft.com/eu/icons/56/spell_druid_bearhug.jpg",
    "Best Friends with Urctos Empowered": "https://render.worldofwarcraft.com/eu/icons/56/spell_druid_bearhug.jpg",

    "Idol of the Dreamer": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon1_color2.jpg",
    "Idol of the Dreamer Empowered": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon1_color2.jpg",
    "Idol of the Life-Binder": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon2_color2.jpg",
    "Idol of the Life-Binder Empowered": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon2_color2.jpg",
    "Idol of the Earth-Warder": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_statue_color5.jpg",
    "Idol of the Earth-Warder Empowered": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_statue_color5.jpg",
    "Idol of the Spell-Weaver": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon3_color1.jpg",
    "Idol of the Spell-Weaver Empowered": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon3_color1.jpg",
    
    "Smoldering Seedling": "https://render.worldofwarcraft.com/eu/icons/56/inv_treepet.jpg",
    "Smoldering Seedling active": "https://render.worldofwarcraft.com/eu/icons/56/inv_treepet.jpg",

    "Blossom of Amirdrassil": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Absorb": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Large HoT": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Small HoT": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",

    "Nymue's Unraveling Spindle": "https://render.worldofwarcraft.com/eu/icons/56/inv_cloth_outdooremeralddream_d_01_buckle.jpg",

    "Voice from Beyond": "https://wow.zamimg.com/images/wow/icons/large/inv_cosmicvoid_nova.jpg",
    "The Silent Star": "https://wow.zamimg.com/images/wow/icons/large/inv_cosmicvoid_debuff.jpg",

    "High Speaker's Accretion Rift": "https://wow.zamimg.com/images/wow/icons/large/inv_magic_swirl_color3.jpg",
    "High Speaker's Accretion Intellect": "https://wow.zamimg.com/images/wow/icons/large/inv_magic_swirl_color3.jpg",
    "Unbound Changeling": "https://wow.zamimg.com/images/wow/icons/large/inv_pet_spectralporcupinegreen.jpg",
    "Empowering Crystal of Anub'ikkaj": "https://wow.zamimg.com/images/wow/icons/large/inv_arathordungeon_fragment_color5.jpg",
    "Harvester's Edict": "https://wow.zamimg.com/images/wow/icons/large/inv_11_0_dungeon_oldgodstatuepiece_purple.jpg",
    "Ara-Kara Sacbrood": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_mercurialegg_red.jpg",
    "Imperfect Ascendancy Serum": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_dpotion_a25.jpg",
    "Gale of Shadows": "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_gathershadows.jpg",
    
    "Deliberate Incubation": "https://wow.zamimg.com/images/wow/icons/large/inv_10_specialreagentfoozles_coolegg_red.jpg",
    "Reckless Incubation": "https://wow.zamimg.com/images/wow/icons/large/inv_10_specialreagentfoozles_coolegg_green.jpg",
    "Ovinax's Mercurial Egg": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_mercurialegg_purple.jpg",
    "Ovinax's Mercurial Egg Paused": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_mercurialegg_purple.jpg",

    "Cryptic Instructions": "https://wow.zamimg.com/images/wow/icons/large/ability_racial_etherealconnection.jpg",
    "Ethereal Powerlink": "https://wow.zamimg.com/images/wow/icons/large/inv_etherealraid_communicator_color1.jpg",

    "Spymaster's Web Stacks": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_nightelfspyglass.jpg",
    "Spymaster's Web": "https://wow.zamimg.com/images/wow/icons/large/ability_spy.jpg",

    "Fateweaved Needle": "https://wow.zamimg.com/images/wow/icons/large/inv_knife_1h_nerubianraid_d_02.jpg",
    "Sureki Zealot's Insignia": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelry_necklace_113.jpg",

    // enchants
    "Sophic Devotion": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_titan.jpg",
    "Authority of Radiant Power": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_holyfire_orb.jpg",
    "Council's Guile": "https://wow.zamimg.com/images/wow/icons/large/ability_gift_of_earth.jpg",
    "Stormrider's Fury": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_stormlordsfavor.jpg",
    "Stonebound Artistry": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_stonetablet_10.jpg",
    "Oathsworn's Tenacity": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_rune_14.jpg",

    // embellishments
    "Potion Absorption Inhibitor": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_food_legion_gooamber_drop.jpg",
    "Verdant Tether": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_tailoring_tailoringconsumable_color4.jpg",
    "Verdant Conduit": "https://render.worldofwarcraft.com/eu/icons/56/inv_trinket_ardenweald_01_orange.jpg",
    "Dreamtender's Charm": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_trinket_stonedragon3_color3.jpg",
    "Magazine of Healing Darts": "https://render.worldofwarcraft.com/eu/icons/56/inv_gizmo_runichealthinjector.jpg",
    "Bronzed Grip Wrappings": "https://render.worldofwarcraft.com/eu/icons/56/inv_holiday_tow_spicebandage.jpg",
    
    "Elemental Lariat": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_jewelcrafting_necklace_necklace1_color3.jpg",
    "Elemental Lariat - Haste": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_air.jpg",
    "Elemental Lariat - Crit": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_fire.jpg",
    "Elemental Lariat - Mastery": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_earth.jpg",
    "Elemental Lariat - Versatility": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_elementalcombinedfoozles_frost.jpg",
    "Allied Chestplate of Generosity": "https://render.worldofwarcraft.com/eu/icons/56/inv_chest_plate_raidwarriorprimalist_d_01.jpg",
    "Allied Wristguards of Companionship": "https://render.worldofwarcraft.com/eu/icons/56/inv_bracer_plate_raidwarriorprimalist_d_01.jpg",
    "Allied Wristgaurds of Companionship": "https://render.worldofwarcraft.com/eu/icons/56/inv_bracer_plate_raidwarriorprimalist_d_01.jpg",

    "Dawnthread Lining": "https://wow.zamimg.com/images/wow/icons/large/inv_10_tailoring_embroiderythread_color1.jpg",
    "Duskthread Lining": "https://wow.zamimg.com/images/wow/icons/large/inv_10_tailoring_tailoringconsumable_color3.jpg",
    "Prismatic Null Stone": "https://wow.zamimg.com/images/wow/icons/large/inv_enchant_prismaticsphere.jpg",
    "Writhing Armor Banding": "https://wow.zamimg.com/images/wow/icons/large/inv_10_skinning_craftedoptionalreagent_studdedleatherswatch_color2.jpg",
    "Energy Distribution Beacon": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_enggizmos_24.jpg",
    "Blessed Weapon Grip": "https://wow.zamimg.com/images/wow/icons/large/spell_holy_weaponmastery.jpg"
}; 

export { buffsToIconsMap };