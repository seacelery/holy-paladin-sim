const talentsToIcons = {
    // class talents
    "Lay on Hands": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_layonhands.jpg",
    "Blessing of Freedom": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofvalor.jpg",
    "Hammer of Wrath" : "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_hammerofwrath.jpg",
    "Improved Cleanse": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_purify.jpg",
    "Auras of the Resolute": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_devotionaura.jpg",
    "Obduracy": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_speedoflight.jpg",
    "Auras of Swift Vengeance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_crusade.jpg",
    "Turn Evil": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_turnevil.jpg",
    "Fist of Justice": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_fistofjustice.jpg",
    "Divine Steed": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_divinesteed.jpg",
    "Greater Judgment": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_righteousfury.jpg",
    "Repentance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_prayerofhealing.jpg",
    "Blinding Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_blindinglight.jpg",
    "Cavalier": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_divinesteed.jpg",
    "Seasoned Warhorse": "https://render.worldofwarcraft.com/eu/icons/56/spell_nature_swiftness.jpg",
    "Rebuke": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_rebuke.jpg",
    "Holy Aegis": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_touchedbylight.jpg",
    "Avenging Wrath": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_avenginewrath.jpg",
    "Justification": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_empoweredsealsrighteous.jpg",
    "Punishment": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_rebuke.jpg",
    "Golden Path": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_cascade.jpg",
    "Echoing Blessings": "https://render.worldofwarcraft.com/eu/icons/56/achievement_dungeon_heroic_gloryoftheraider.jpg",
    "Blessing of Sacrifice": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofsacrifice.jpg",
    "Sanctified Plates": "https://render.worldofwarcraft.com/eu/icons/56/inv_chest_plate_raidpaladin_s_01.jpg",
    "Blessing of Protection": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofprotection.jpg",
    "Lightforged Blessing": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_circleofrenewal.jpg",
    "Seal of Mercy": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_greaterblessingofsalvation.jpg",
    "Afterimage": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Sacrifice of the Just": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofsacrifice.jpg",
    "Recompense": "https://render.worldofwarcraft.com/eu/icons/56/ability_racial_foregedinflames.jpg",
    "Unbreakable Spirit": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyguidance.jpg",
    "Improved Blessing of Protection": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofprotection.jpg",
    "Crusader's Reprieve": "https://render.worldofwarcraft.com/eu/icons/56/inv_sword_07.jpg",
    "Strength of Conviction": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_eyeforaneye.jpg",
    "Judgment of Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divineprovidence.jpg",
    "Seal of Might": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofwrath.jpg",
    "Divine Purpose": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divinepurpose.jpg",
    "Seal of Alacrity": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofvengeance.jpg",
    "Incandescence": "https://render.worldofwarcraft.com/eu/icons/56/inv_summerfest_firespirit.jpg",
    "Touch of Light": "https://render.worldofwarcraft.com/eu/icons/56/achievment_raid_houroftwilight.jpg",
    "Faith's Armor": "https://render.worldofwarcraft.com/eu/icons/56/inv_shield_1h_newplayer_a_01.jpg",
    "Of Dusk and Dawn": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_lightofdawn.jpg",
    "Divine Toll": "https://render.worldofwarcraft.com/eu/icons/56/ability_bastion_paladin.jpg",
    "Seal of the Crusader": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holysmite.jpg",
    "Seal of Order": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_sealofwisdom.jpg",
    "Fading Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_shadow_sealofkings.jpg",
    "Divine Resonance": "https://render.worldofwarcraft.com/eu/icons/56/ability_mount_goatmountwhite.jpg",
    "Quickened Invocation": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_pureofheart.jpg",
    "Vanguard's Momentum": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_speedoflight.jpg",

    // spec talents
    "Holy Shock": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_searinglight.jpg",
    "Glimmer of Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_toweroflight.jpg",
    "Light of Dawn": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_lightofdawn.jpg",
    "Light's Conviction": "https://render.worldofwarcraft.com/eu/icons/56/paladin_holy.jpg",
    "Aura Mastery": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_auramastery.jpg",
    "Beacon of the Lightbringer": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_clarityofpurpose.jpg",
    "Moment of Compassion": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_flashheal.jpg",
    "Resplendent Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_voidshift.jpg",
    "Tirion's Devotion": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_revivechampion.jpg",
    "Unending Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holybolt.jpg",
    "Awestruck": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_blindinglight2.jpg",
    "Holy Infusion": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightoftheprotector.jpg",
    "Divine Favor": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_heal.jpg",
    "Hand of Divinity": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_vindication.jpg",
    "Glistening Radiance": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_divinecircle.jpg",
    "Unwavering Spirit": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_fanaticism.jpg",
    "Protection of Tyr": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_auramastery.jpg",
    "Imbued Infusions": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_flashoflight.jpg",
    "Light of the Martyr": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_lightofthemartyr.jpg",
    "Illumination": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_cascade.jpg",
    "Blessed Focus": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_inquisition.jpg",
    "Saved by the Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_savedbythelight.jpg",
    "Light's Hammer": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_lightshammer.jpg",
    "Holy Prism": "https://render.worldofwarcraft.com/eu/icons/56/spell_paladin_holyprism.jpg",
    "Power of the Silver Hand": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_blessedhands.jpg",
    "Light's Protection": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_absolution.jpg",
    "Overflowing Light": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holyguidance.jpg",
    "Shining Righteousness": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holynova.jpg",
    "Divine Revelations": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_infusionoflight.jpg",
    "Commanding Light": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconoflight.jpg",
    "Righteous Judgment": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_holybolts01.jpg",
    "Breaking Dawn": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_rune.jpg",
    "Tower of Radiance": "https://render.worldofwarcraft.com/eu/icons/56/inv_helm_plate_raidpaladinmythic_q_01.jpg",
    "Divine Glimpse": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_healingaura.jpg",
    "Untempered Dedication": "https://render.worldofwarcraft.com/eu/icons/56/achievement_admiral_of_the_light.jpg",
    "Beacon of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconsoflight.jpg",
    "Beacon of Virtue": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_beaconofinsight.jpg",
    "Veneration": "https://render.worldofwarcraft.com/eu/icons/56/ability_crown_of_the_heavens_icon.jpg",
    "Avenging Wrath: Might": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_avenginewrath.jpg",
    "Avenging Crusader": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_veneration.jpg",
    "Reclamation": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_longarmofthelaw.jpg",
    "Barrier of Faith": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_barrieroffaith.jpg",
    "Maraad's Dying Breath": "https://render.worldofwarcraft.com/eu/icons/56/paladin_icon_speedoflight.jpg",
    "Daybreak": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_aspiration.jpg",
    "Crusader's Might": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_swiftretribution.jpg",
    "Merciful Auras": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_blessedlife.jpg",
    "Blessing of Summer": "https://render.worldofwarcraft.com/eu/icons/56/ability_ardenweald_paladin_summer.jpg",
    "Relentless Inquisitor": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_mindvision.jpg",
    "Tyr's Deliverance": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_2h_artifactsilverhand_d_01.jpg",
    "Rising Sunlight": "https://render.worldofwarcraft.com/eu/icons/56/spell_priest_divinestar_holy.jpg",
    "Glorious Dawn": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_holyavenger.jpg",
    "Sanctified Wrath": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_judgementsofthejust.jpg",
    "Awakening": "https://render.worldofwarcraft.com/eu/icons/56/inv_helm_plate_raidpaladin_n_01.jpg",
    "Inflorescence of the Sunwell": "https://render.worldofwarcraft.com/eu/icons/56/spell_lfieblood.jpg",
    "Empyrean Legacy": "https://render.worldofwarcraft.com/eu/icons/56/item_holyspark.jpg",
    "Boundless Salvation": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_selflesshealer.jpg",

    // lightsmith talents
    "Holy Bulwark": "https://render.worldofwarcraft.com/eu/icons/56/inv_shield_1h_artifactnorgannon_d_06.jpg",
    "Rite of Sanctification": "https://render.worldofwarcraft.com/eu/icons/56/inv_inscription_weaponscroll01.jpg",
    "Rite of Adjuration": "https://render.worldofwarcraft.com/eu/icons/56/inv_inscription_armorscroll02.jpg",
    "Solidarity": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_heroism.jpg",
    "Divine Guidance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_lightsgrace.jpg",
    "Blessed Assurance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_blessedlife.jpg",
    "Laying Down Arms": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_infusionoflight.jpg",
    "Divine Inspiration": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_flashoflight.jpg",
    "Forewarning": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_gaurdedbythelight.jpg",
    "Fear No Evil": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_senseundead.jpg",
    "Excoriation": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_sanctifiedwrath.jpg",
    "Shared Resolve": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_devotionaura.jpg",
    "Valiance": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_47.jpg",
    "Hammer and Anvil": "https://render.worldofwarcraft.com/eu/icons/56/inv_10_blacksmithing_consumable_repairhammer_color1.jpg",
    "Blessing of the Forge": "https://render.worldofwarcraft.com/eu/icons/56/inv_mace_1h_artifactnorgannon_d_06.jpg",

    // herald of the sun talents
    "Dawnlight": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_flashoflight.jpg",
    "Morning Star": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_persecution.jpg",
    "Gleaming Rays": "https://wow.zamimg.com/images/wow/icons/large/spell_priest_power-word.jpg",
    "Eternal Flame": "https://render.worldofwarcraft.com/eu/icons/56/inv_torch_thrown.jpg",
    "Luminosity": "https://render.worldofwarcraft.com/eu/icons/56/inv_qirajidol_sun.jpg",
    "Illumine": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divineillumination.jpg",
    "Will of the Dawn": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_divineprovidence.jpg",
    "Blessing of An'she": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_holynova.jpg",
    "Lingering Radiance": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_mindvision.jpg",
    "Sun Sear": "https://render.worldofwarcraft.com/eu/icons/56/spell_priest_burningwill.jpg",
    "Aurora": "https://render.worldofwarcraft.com/eu/icons/56/spell_holy_rune.jpg",
    "Solar Grace": "https://render.worldofwarcraft.com/eu/icons/56/ability_malkorok_blightofyshaarj_yellow.jpg",
    "Second Sunrise": "https://render.worldofwarcraft.com/eu/icons/56/ability_priest_halo.jpg",
    "Sun's Avatar": "https://render.worldofwarcraft.com/eu/icons/56/ability_paladin_holyavenger.jpg"
};

export { talentsToIcons };