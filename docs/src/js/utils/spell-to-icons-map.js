const spellToIconsMap = {
    // paladin abilities
    "Afterimage": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Afterimage (Eternal Flame)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Afterimage (Word of Glory)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Arcane Torrent": "https://render.worldofwarcraft.com/eu/icons/56/spell_shadow_teleport.jpg",
    "Aura Mastery": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_auramastery.jpg",
    "Authority of Fiery Resolve": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_healingaura.jpg",
    "Avenging Wrath": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_avenginewrath.jpg",
    "Avenging Crusader": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_veneration.jpg",
    "Avenging Crusader (Crusader Strike)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusaderstrike.jpg",
    "Avenging Crusader (Judgment)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_righteousfury.jpg",
    "Barrier of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_barrieroffaith.jpg",
    "Barrier of Faith (Holy Shock)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Barrier of Faith (Flash of Light)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_flashheal.jpg",
    "Barrier of Faith (Holy Light)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_surgeoflight.jpg",
    "Beacon of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconsoflight.jpg",
    "Beacon of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconoflight.jpg",
    "Beacon of Virtue": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconofinsight.jpg",
    "Blessing of Autumn": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_autumn.jpg",
    "Blessing of Spring": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_spring.jpg",
    "Blessing of Summer": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_summer.jpg",
    "Blessing of the Seasons": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_autumn.jpg",
    "Blessing of Winter": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_winter.jpg",
    "Consecration": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_innerfire.jpg",
    "Crusader Strike": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusaderstrike.jpg",
    "Crusader's Reprieve": "https://render.worldofwarcraft.com/eu/icons/56/inv_sword_07.jpg",
    "Dawnlight": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_heraldofthesunpaladin_dawnlight.jpg",
    "Dawnlight (HoT)": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_heraldofthesunpaladin_dawnlight.jpg",
    "Dawnlight (AoE)": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_heraldofthesunpaladin_dawnlight.jpg",
    "Daybreak": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Divine Favor": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_heal.jpg",
    "Divine Guidance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_lightsgrace.jpg",
    "Divine Revelations (Holy Light)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_infusionoflight.jpg",
    "Divine Revelations (Judgment)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_infusionoflight.jpg",
    "Divine Toll": "https://render.worldofwarcraft.com/eu/icons/56/ability_bastion_paladin.jpg",
    "Embrace of Akunda": "https://render.worldofwarcraft.com/eu/icons/56/ability_racial_embraceoftheloa_akuna.jpg",
    "Eternal Flame": "https://render.worldofwarcraft.com/eu/icons/56/inv_torch_thrown.jpg",
    "Eternal Flame (HoT)": "https://render.worldofwarcraft.com/eu/icons/56/inv_torch_thrown.jpg",
    "Fading Light": "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_sealofkings.jpg",
    "Fireblood": "https://render.worldofwarcraft.com/eu/icons/56/ability_racial_fireblood.jpg",
    "Flash of Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_flashheal.jpg",
    "Gift of the Naaru": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyprotection.jpg",
    "Glimmer of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_toweroflight.jpg",
    "Glimmer of Light (Daybreak)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_toweroflight.jpg",
    "Golden Path": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_cascade.jpg",
    "Greater Judgment": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_righteousfury.jpg",
    "Hammer and Anvil": "https://wow.zamimg.com/images/wow/icons/large/inv_10_blacksmithing_consumable_repairhammer_color1.jpg",
    "Hammer of Wrath": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_hammerofwrath.jpg",
    "Hand of Divinity": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_vindication.jpg",
    "Holy Armament": "https://wow.zamimg.com/images/wow/icons/large/inv_ability_lightsmithpaladin_holybulwark.jpg",
    "Holy Bulwark": "https://render.worldofwarcraft.com/eu/icons/56/inv_shield_1h_artifactnorgannon_d_06.jpg",
    "Holy Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_surgeoflight.jpg",
    "Holy Prism": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_holyprism.jpg",
    "Holy Reverberation": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_holybolts01.jpg",
    "Holy Shock": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Holy Shock (Divine Resonance)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Holy Shock (Divine Toll)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Holy Shock (Rising Sunlight)": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Judgment": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_righteousfury.jpg",
    "Judgment of Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divineprovidence.jpg",
    "Lay on Hands": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_layonhands.jpg",
    "Light of Dawn": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_lightofdawn.jpg",
    "Light's Hammer": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_lightshammer.jpg",
    "Light of the Martyr": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
    "Light of the Martyr ": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
    "Merciful Auras": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_blessedlife.jpg",
    "Overflowing Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyguidance.jpg",
    "Radiant Aura": "https://wow.zamimg.com/images/wow/icons/large/inv_staff_2h_artifacttome_d_06.jpg",
    "Reclamation (Crusader Strike)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_longarmofthelaw.jpg",
    "Reclamation (Holy Shock)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_longarmofthelaw.jpg",
    "Resplendent Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_voidshift.jpg",
    "Rite of Adjuration": "https://render.worldofwarcraft.com/eu/icons/56/inv_inscription_armorscroll02.jpg",
    "Sacred Weapon": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_artifactnorgannon_d_06.jpg",
    "Sacred Weapon 1": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_artifactnorgannon_d_06.jpg",
    "Sacred Weapon 2": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_artifactnorgannon_d_06.jpg",
    "Sacred Word": "https://wow.zamimg.com/images/wow/icons/large/inv_mace_1h_artifactnorgannon_d_06.jpg",
    "Saved by the Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Saved by the Light (Word of Glory)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Saved by the Light (Eternal Flame)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Saved by the Light (Light of Dawn)": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Seal of Mercy": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_greaterblessingofsalvation.jpg",
    "Sun's Avatar": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_holyavenger.jpg",
    "Sun Sear": "https://render.worldofwarcraft.com/eu/icons/56/spell_priest_burningwill.jpg",
    "Tirion's Devotion": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_revivechampion.jpg",
    "Touch of Light": "https://render.worldofwarcraft.com/eu/icons/56/achievment_raid_houroftwilight.jpg",
    "Tyr's Deliverance": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_2h_artifactsilverhand_d_01.jpg",
    "Truth Prevails": "https://wow.zamimg.com/images/wow/icons/large/spell_holy_spiritualguidence.jpg",
    "Veneration": "https://render.worldofwarcraft.com/eu/icons/56/ability_crown_of_the_heavens_icon.jpg",
    "Word of Glory": "https://render.worldofwarcraft.com/eu/icons/56/inv_helmet_96.jpg",

    // consumables
    "Aerated Mana Potion": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_alchemy_bottle_shape1_blue.jpg",
    "Elemental Potion of Ultimate Power": "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_dpotion_b20.jpg",
    "Potion": "https://render.worldofwarcraft.com/eu/icons/56/trade_alchemy_dpotion_b20.jpg",
    "Chirping Rune": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_rune_09.jpg",
    "Algari Mana Potion": "https://wow.zamimg.com/images/wow/icons/large/inv_flask_blue.jpg",
    "Grotesque Vial": "https://render.worldofwarcraft.com/eu/icons/56/inv_summerfest_firepotion.jpg",
    "Slumbering Soul Serum": "https://wow.zamimg.com/images/wow/icons/large/inv_flask_green.jpg",
    "Tempered Potion": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_potiona4.jpg",

    // trinkets
    "Mirror of Fractured Tomorrows": "https://render.worldofwarcraft.com/eu/icons/56/achievement_dungeon_ulduarraid_misc_06.jpg",
    "Restorative Sands": "https://render.worldofwarcraft.com/eu/icons/56/spell_quicksand.jpg",
    "Smoldering Seedling": "https://render.worldofwarcraft.com/eu/icons/56/inv_treepet.jpg",
    "Blossom of Amirdrassil": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Absorb": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Large HoT": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Blossom of Amirdrassil Small HoT": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_herb_starflower.jpg",
    "Nymue's Unraveling Spindle": "https://render.worldofwarcraft.com/eu/icons/56/inv_cloth_outdooremeralddream_d_01_buckle.jpg",
    "Conjured Chillglobe": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_specialreagentfoozles_primalistrune_frost.jpg",
    "Rashok's Molten Heart": "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_trinket6oih_orb4.jpg",
    "Time-Breaching Talon": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_explorer_trinket_3_color3.jpg",
    "Spoils of Neltharus": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_dragon_trinket_4_bronze.jpg",
    "Broodkeeper's Promise": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_primalist_trinket_3_omni.jpg",
    "Miniature Singing Stone": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_dungeonjewelry_centaur_trinket_1_color1.jpg",
    "Echoing Tyrstone": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
    "Siphoning Phylactery Shard": "https://wow.zamimg.com/images/wow/icons/large/inv_enchanting_70_chaosshard.jpg",
    "High Speaker's Accretion": "https://wow.zamimg.com/images/wow/icons/large/inv_cosmicvoid_nova.jpg",
    "Viscous Coaglam": "https://wow.zamimg.com/images/wow/icons/large/spell_priest_shadoworbs.jpg",
    "Ovinax's Mercurial Egg": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_mercurialegg_purple.jpg",
    "Creeping Coagulum": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_creepingcoagulum_purple.jpg",
    "Gruesome Syringe": "https://wow.zamimg.com/images/wow/icons/large/inv_raid_gruesomesyringe_red.jpg",
    "Sureki Zealot's Insignia": "https://wow.zamimg.com/images/wow/icons/large/inv_jewelry_necklace_113.jpg",
    "Treacherous Transmitter": "https://wow.zamimg.com/images/wow/icons/large/inv_etherealraid_communicator_color1.jpg",
    "Imperfect Ascendancy Serum": "https://wow.zamimg.com/images/wow/icons/large/trade_alchemy_dpotion_a25.jpg",
    "Corrupted Egg Shell": "https://wow.zamimg.com/images/wow/icons/large/inv_misc_cat_trinket09.jpg",

    // enchants
    "Dreaming Devotion": "https://render.worldofwarcraft.com/eu/icons/56/item_herbd.jpg",
    "Larodar's Fiery Reverie": "https://render.worldofwarcraft.com/eu/icons/56/10_2_raidability_burningroots.jpg",

    // embellishments
    "Magazine of Healing Darts": "https://render.worldofwarcraft.com/eu/icons/56/inv_gizmo_runichealthinjector.jpg",
    "Bronzed Grip Wrappings": "https://render.worldofwarcraft.com/eu/icons/56/inv_holiday_tow_spicebandage.jpg",

    // misc
    "Wait": "https://render.worldofwarcraft.com/eu/icons/56/inv_gauntlets_06.jpg",
    "Leech": "https://render.worldofwarcraft.com/eu/icons/56/spell_shadow_lifedrain02.jpg",
    "Source of Magic": "https://render.worldofwarcraft.com/eu/icons/56/ability_evoker_blue_01.jpg",
    "Mana Spring Totem": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_manaregentotem.jpg",
    "Symbol of Hope": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_symbolofhope.jpg",
    "Mana Tide Totem": "https://render.worldofwarcraft.com/eu/icons/56/ability_shaman_manatidetotem.jpg",
};

export { spellToIconsMap };