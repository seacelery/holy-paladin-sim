const classTalentsLive = [
    "", "Lay on Hands", "", "Blessing of Freedom", "", "Hammer of Wrath", "",
    "Improved Cleanse", "", "Auras of the Resolute", "Obduracy", "Auras of Swift Vengeance", "", "Turn Evil",
    "", "Fist of Justice", "", "Divine Steed", "", "Greater Judgment", "",
    "Repentance/Blinding Light", "", "Cavalier", "", "Seasoned Warhorse", "", "Rebuke",
    "", "Holy Aegis", "", "Avenging Wrath", "", "Justification", "Punishment",
    "Golden Path", "Echoing Blessings", "Blessing of Sacrifice", "Sanctified Plates", "Blessing of Protection", "", "Lightforged Blessing",
    "Seal of Mercy", "Afterimage", "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Improved Blessing of Protection", "Crusader's Reprieve", "",
    "Strength of Conviction", "Judgment of Light", "Seal of Might", "Divine Purpose", "Seal of Alacrity", "Incandescence/Touch of Light", "Faith's Armor",
    "", "Of Dusk and Dawn", "", "Divine Toll", "", "Seal of the Crusader", "",
    "", "Seal of Order/Fading Light", "", "Divine Resonance/Quickened Invocation", "", "Vanguard's Momentum", ""
];

const classTalentsPTR = [
    "", "Lay on Hands", "", "Blessing of Freedom", "", "Hammer of Wrath", "",
    "Improved Cleanse", "", "Auras of the Resolute", "Obduracy", "Crusader Aura", "", "Turn Evil",
    "", "Fist of Justice", "", "Divine Steed", "", "Greater Judgment", "",
    "Repentance/Blinding Light", "", "Cavalier", "", "Seasoned Warhorse", "", "Rebuke",
    "", "Holy Aegis", "", "Avenging Wrath", "", "Justification", "Punishment",
    "Golden Path", "Echoing Blessings", "Blessing of Sacrifice", "Sanctified Plates", "Blessing of Protection", "", "Lightforged Blessing",
    "Seal of Mercy", "Afterimage", "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Improved Blessing of Protection", "Touch of Light", "",
    "Strength of Conviction", "Judgment of Light", "Seal of Might", "Divine Purpose", "Seal of Alacrity", "Incandescence", "Faith's Armor",
    "", "Of Dusk and Dawn", "", "Divine Toll", "", "Seal of the Crusader", "",
    "", "Seal of Order/Fading Light", "", "Divine Resonance/Quickened Invocation", "", "Vanguard's Momentum", ""
];

const specTalentsLive = [
    "", "", "", "", "Holy Shock", "", "", "", "",
    "", "", "", "Glimmer of Light", "", "Light of Dawn", "", "", "", 
    "", "", "Light's Conviction", "", "Aura Mastery", "", "Beacon of the Lightbringer", "", "", 
    "", "Moment of Compassion/Resplendent Light", "", "Tirion's Devotion", "", "Unending Light", "", "Awestruck/Holy Infusion", "", 
    "Divine Favor/Hand of Divinity", "", "Glistening Radiance", "", "Unwavering Spirit/Protection of Tyr", "", "Imbued Infusions", "", "Light of the Martyr", 
    "", "Illumination/Blessed Focus", "Saved by the Light", "Light's Hammer/Holy Prism", "Power of the Silver Hand", "Light's Protection", "Overflowing Light", "Shining Righteousness", "", 
    "Divine Revelations", "", "Commanding Light", "Righteous Judgment", "Breaking Dawn", "Tower of Radiance", "Divine Glimpse", "", "Untempered Dedication", 
    "", "Beacon of Faith/Beacon of Virtue", "", "Veneration", "", "Avenging Wrath: Might/Avenging Crusader", "", "Reclamation/Barrier of Faith", "Maraad's Dying Breath", 
    "", "Daybreak", "Crusader's Might", "", "Merciful Auras/Blessing of Summer", "", "Relentless Inquisitor", "Tyr's Deliverance", "", 
    "", "Rising Sunlight", "", "Glorious Dawn", "Sanctified Wrath/Awakening", "Inflorescence of the Sunwell/Empyrean Legacy", "", "Boundless Salvation", "", 
];

const specTalentsPTR = [
    "", "", "", "", "Holy Shock", "", "", "", "",
    "", "", "", "Extrication", "", "Light of Dawn", "", "", "", 
    "", "", "Light's Conviction", "", "Aura Mastery", "", "Beacon of the Lightbringer", "", "", 
    "", "Moment of Compassion/Resplendent Light", "", "Tirion's Devotion", "", "Unending Light", "", "Awestruck/Holy Infusion", "", 
    "Divine Revelations", "", "Holy Prism/Barrier of Faith", "", "Unwavering Spirit/Protection of Tyr", "", "Imbued Infusions", "", "Light of the Martyr", 
    "", "Liberation", "Divine Favor/Hand of Divinity", "Saved by the Light", "Power of the Silver Hand", "Light's Protection", "Overflowing Light", "Shining Righteousness", "", 
    "Righteous Judgment", "", "Commanding Light", "Glistening Radiance", "Breaking Dawn", "Tower of Radiance", "Divine Glimpse", "", "Bestow Light", 
    "", "Beacon of Faith/Beacon of Virtue", "", "Veneration", "", "Avenging Wrath: Might/Avenging Crusader", "", "Tyr's Deliverance", "", 
    "Truth Prevails", "", "Crusader's Might", "", "Sanctified Wrath/Awakening", "", "Relentless Inquisitor", "", "Reclamation", 
    "", "Rising Sunlight", "", "Glorious Dawn", "Merciful Auras/Blessing of Summer", "Inflorescence of the Sunwell/Empyrean Legacy", "", "Boundless Salvation", "", 
];


let baseClassTalentsLive = {
    "row1": {
        "Lay on Hands": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Freedom": {"ranks": {"current rank": 0, "max rank": 1}},
        "Hammer of Wrath": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row2": {
        "Improved Cleanse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Auras of the Resolute": {"ranks": {"current rank": 0, "max rank": 1}},
        "Obduracy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Auras of Swift Vengeance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Turn Evil": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row3": {
        "Fist of Justice": {"ranks": {"current rank": 0, "max rank": 2}},
        "Divine Steed": {"ranks": {"current rank": 0, "max rank": 1}},
        "Greater Judgment": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Repentance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blinding Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Cavalier": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seasoned Warhorse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Rebuke": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row5": {
        "Holy Aegis": {"ranks": {"current rank": 0, "max rank": 2}},
        "Avenging Wrath": {"ranks": {"current rank": 0, "max rank": 1}},
        "Justification": {"ranks": {"current rank": 0, "max rank": 1}},
        "Punishment": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row6": {
        "Golden Path": {"ranks": {"current rank": 0, "max rank": 1}},
        "Echoing Blessings": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Sacrifice": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sanctified Plates": {"ranks": {"current rank": 0, "max rank": 2}},
        "Blessing of Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Lightforged Blessing": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row7": {
        "Seal of Mercy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Afterimage": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sacrifice of the Just": {"ranks": {"current rank": 0, "max rank": 1}},
        "Recompense": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unbreakable Spirit": {"ranks": {"current rank": 0, "max rank": 1}},
        "Improved Blessing of Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Crusader's Reprieve": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row8": {
        "Strength of Conviction": {"ranks": {"current rank": 0, "max rank": 2}},
        "Judgment of Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seal of Might": {"ranks": {"current rank": 0, "max rank": 2}},
        "Divine Purpose": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seal of Alacrity": {"ranks": {"current rank": 0,"max rank": 2}},
        "Incandescence": {"ranks": {"current rank": 0,"max rank": 1}},
        "Touch of Light": {"ranks": {"current rank": 0,"max rank": 1}},
        "Faith's Armor": {"ranks": {"current rank": 0,"max rank": 1}}
    },
    "row9": {
        "Of Dusk and Dawn": {"ranks": {"current rank": 0,"max rank": 1}},
        "Divine Toll": {"ranks": {"current rank": 0,"max rank": 1}},
        "Seal of the Crusader": {"ranks": {"current rank": 0,"max rank": 2}}
    },
    "row10": {
        "Seal of Order": {"ranks": {"current rank": 0,"max rank": 1}},
        "Fading Light": {"ranks": {"current rank": 0,"max rank": 1}},
        "Divine Resonance": {"ranks": {"current rank": 0,"max rank": 1}},
        "Quickened Invocation": {"ranks": {"current rank": 0,"max rank": 1}},
        "Vanguard's Momentum": {"ranks": {"current rank": 0,"max rank": 1}}
    }
};

let baseClassTalentsPTR = {
    "row1": {
        "Lay on Hands": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Freedom": {"ranks": {"current rank": 0, "max rank": 1}},
        "Hammer of Wrath": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row2": {
        "Improved Cleanse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Auras of the Resolute": {"ranks": {"current rank": 0, "max rank": 1}},
        "Obduracy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Crusader Aura": {"ranks": {"current rank": 0, "max rank": 1}},
        "Turn Evil": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row3": {
        "Fist of Justice": {"ranks": {"current rank": 0, "max rank": 2}},
        "Divine Steed": {"ranks": {"current rank": 0, "max rank": 1}},
        "Greater Judgment": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Repentance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blinding Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Cavalier": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seasoned Warhorse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Rebuke": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row5": {
        "Holy Aegis": {"ranks": {"current rank": 0, "max rank": 2}},
        "Avenging Wrath": {"ranks": {"current rank": 0, "max rank": 1}},
        "Justification": {"ranks": {"current rank": 0, "max rank": 1}},
        "Punishment": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row6": {
        "Golden Path": {"ranks": {"current rank": 0, "max rank": 1}},
        "Echoing Blessings": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Sacrifice": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sanctified Plates": {"ranks": {"current rank": 0, "max rank": 2}},
        "Blessing of Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Lightforged Blessing": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row7": {
        "Seal of Mercy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Afterimage": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sacrifice of the Just": {"ranks": {"current rank": 0, "max rank": 1}},
        "Recompense": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unbreakable Spirit": {"ranks": {"current rank": 0, "max rank": 1}},
        "Improved Blessing of Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Touch of Light": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row8": {
        "Strength of Conviction": {"ranks": {"current rank": 0, "max rank": 2}},
        "Judgment of Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seal of Might": {"ranks": {"current rank": 0, "max rank": 2}},
        "Divine Purpose": {"ranks": {"current rank": 0, "max rank": 1}},
        "Seal of Alacrity": {"ranks": {"current rank": 0,"max rank": 2}},
        "Incandescence": {"ranks": {"current rank": 0,"max rank": 1}},
        "Faith's Armor": {"ranks": {"current rank": 0,"max rank": 1}}
    },
    "row9": {
        "Of Dusk and Dawn": {"ranks": {"current rank": 0,"max rank": 1}},
        "Divine Toll": {"ranks": {"current rank": 0,"max rank": 1}},
        "Seal of the Crusader": {"ranks": {"current rank": 0,"max rank": 2}}
    },
    "row10": {
        "Seal of Order": {"ranks": {"current rank": 0,"max rank": 1}},
        "Fading Light": {"ranks": {"current rank": 0,"max rank": 1}},
        "Divine Resonance": {"ranks": {"current rank": 0,"max rank": 1}},
        "Quickened Invocation": {"ranks": {"current rank": 0,"max rank": 1}},
        "Vanguard's Momentum": {"ranks": {"current rank": 0,"max rank": 1}}
    }
};
        
let baseSpecTalentsLive = {
    "row1": {
        "Holy Shock": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row2": {
        "Glimmer of Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light of Dawn": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row3": {
        "Light's Conviction": {"ranks": {"current rank": 0, "max rank": 1}},
        "Aura Mastery": {"ranks": {"current rank": 0, "max rank": 1}},
        "Beacon of the Lightbringer": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Moment of Compassion": {"ranks": {"current rank": 0, "max rank": 1}},
        "Resplendent Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Tirion's Devotion": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unending Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Awestruck": {"ranks": {"current rank": 0, "max rank": 1}},
        "Holy Infusion": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row5": {
        "Divine Favor": {"ranks": {"current rank": 0, "max rank": 1}},
        "Hand of Divinity": {"ranks": {"current rank": 0, "max rank": 1}},
        "Glistening Radiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unwavering Spirit": {"ranks": {"current rank": 0, "max rank": 1}},
        "Protection of Tyr": {"ranks": {"current rank": 0, "max rank": 1}},
        "Imbued Infusions": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light of the Martyr": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row6": {
        "Illumination": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessed Focus": {"ranks": {"current rank": 0, "max rank": 1}},
        "Saved by the Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light's Hammer": {"ranks": {"current rank": 0, "max rank": 1}},
        "Holy Prism": {"ranks": {"current rank": 0, "max rank": 1}},
        "Power of the Silver Hand": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light's Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Overflowing Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Shining Righteousness": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row7": {
        "Divine Revelations": {"ranks": {"current rank": 0, "max rank": 1}},
        "Commanding Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Righteous Judgment": {"ranks": {"current rank": 0, "max rank": 1}},
        "Breaking Dawn": {"ranks": {"current rank": 0, "max rank": 2}},
        "Tower of Radiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Divine Glimpse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Untempered Dedication": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row8": {
        "Beacon of Faith": {"ranks": {"current rank": 0, "max rank": 1}},
        "Beacon of Virtue": {"ranks": {"current rank": 0, "max rank": 1}},
        "Veneration": {"ranks": {"current rank": 0, "max rank": 1}},
        "Avenging Wrath: Might": {"ranks": {"current rank": 0, "max rank": 1}},
        "Avenging Crusader": {"ranks": {"current rank": 0, "max rank": 1}},
        "Reclamation": {"ranks": {"current rank": 0, "max rank": 1}},
        "Barrier of Faith": {"ranks": {"current rank": 0, "max rank": 1}},
        "Maraad's Dying Breath": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row9": {
        "Daybreak": {"ranks": {"current rank": 0, "max rank": 1}},
        "Crusader's Might": {"ranks": {"current rank": 0, "max rank": 1}},
        "Merciful Auras": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Summer": {"ranks": {"current rank": 0, "max rank": 1}},
        "Relentless Inquisitor": {"ranks": {"current rank": 0, "max rank": 1}},
        "Tyr's Deliverance": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row10": {
        "Rising Sunlight": {"ranks": {"current rank": 0, "max rank": 1}},
        "Glorious Dawn": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sanctified Wrath": {"ranks": {"current rank": 0, "max rank": 1}},
        "Awakening": {"ranks": {"current rank": 0, "max rank": 1}},
        "Inflorescence of the Sunwell": {"ranks": {"current rank": 0, "max rank": 1}},
        "Empyrean Legacy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Boundless Salvation": {"ranks": {"current rank": 0, "max rank": 1}}
    }
};

let baseSpecTalentsPTR = {
    "row1": {
        "Holy Shock": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row2": {
        "Extrication": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light of Dawn": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row3": {
        "Light's Conviction": {"ranks": {"current rank": 0, "max rank": 1}},
        "Aura Mastery": {"ranks": {"current rank": 0, "max rank": 1}},
        "Beacon of the Lightbringer": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Moment of Compassion": {"ranks": {"current rank": 0, "max rank": 1}},
        "Resplendent Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Tirion's Devotion": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unending Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Awestruck": {"ranks": {"current rank": 0, "max rank": 1}},
        "Holy Infusion": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row5": {
        "Divine Revelations": {"ranks": {"current rank": 0, "max rank": 1}},
        "Hand of Divinity": {"ranks": {"current rank": 0, "max rank": 1}},
        "Unwavering Spirit": {"ranks": {"current rank": 0, "max rank": 1}},
        "Protection of Tyr": {"ranks": {"current rank": 0, "max rank": 1}},
        "Imbued Infusions": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light of the Martyr": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row6": {
        "Liberation": {"ranks": {"current rank": 0, "max rank": 1}},
        "Divine Favor": {"ranks": {"current rank": 0, "max rank": 1}},
        "Saved by the Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Barrier of Faith": {"ranks": {"current rank": 0, "max rank": 1}},
        "Holy Prism": {"ranks": {"current rank": 0, "max rank": 1}},
        "Power of the Silver Hand": {"ranks": {"current rank": 0, "max rank": 1}},
        "Light's Protection": {"ranks": {"current rank": 0, "max rank": 1}},
        "Overflowing Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Shining Righteousness": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row7": {
        "Righteous Judgment": {"ranks": {"current rank": 0, "max rank": 1}},
        "Commanding Light": {"ranks": {"current rank": 0, "max rank": 1}},
        "Glistening Radiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Breaking Dawn": {"ranks": {"current rank": 0, "max rank": 2}},
        "Tower of Radiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Divine Glimpse": {"ranks": {"current rank": 0, "max rank": 1}},
        "Bestow Light": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row8": {
        "Beacon of Faith": {"ranks": {"current rank": 0, "max rank": 1}},
        "Beacon of Virtue": {"ranks": {"current rank": 0, "max rank": 1}},
        "Veneration": {"ranks": {"current rank": 0, "max rank": 1}},
        "Avenging Wrath: Might": {"ranks": {"current rank": 0, "max rank": 1}},
        "Avenging Crusader": {"ranks": {"current rank": 0, "max rank": 1}},
        "Tyr's Deliverance": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row9": {
        "Truth Prevails": {"ranks": {"current rank": 0, "max rank": 1}},
        "Crusader's Might": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sanctified Wrath": {"ranks": {"current rank": 0, "max rank": 1}},
        "Awakening": {"ranks": {"current rank": 0, "max rank": 1}},
        "Relentless Inquisitor": {"ranks": {"current rank": 0, "max rank": 1}},
        "Reclamation": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row10": {
        "Rising Sunlight": {"ranks": {"current rank": 0, "max rank": 1}},
        "Glorious Dawn": {"ranks": {"current rank": 0, "max rank": 1}},
        "Merciful Auras": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of Summer": {"ranks": {"current rank": 0, "max rank": 1}},
        "Inflorescence of the Sunwell": {"ranks": {"current rank": 0, "max rank": 1}},
        "Empyrean Legacy": {"ranks": {"current rank": 0, "max rank": 1}},
        "Boundless Salvation": {"ranks": {"current rank": 0, "max rank": 1}}
    }
};

const classTalentsArrowsLive = {
    "down": [
        "Blessing of Freedom", "Obduracy", "Rebuke", "Holy Aegis", "Avenging Wrath", "Punishment", "Golden Path", "Echoing Blessings",
        "Blessing of Sacrifice", "Sanctified Plates", "Blessing of Protection", "Seal of Mercy", "Afterimage",
        "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Improved Blessing of Protection", "Crusader's Reprieve", "Judgment of Light",
        "Divine Purpose", "Incandescence/Touch of Light", "Of Dusk and Dawn", "Divine Toll", "Seal of the Crusader"
    ],
    "downLong": [
        "Lay on Hands", "Hammer of Wrath", "Improved Cleanse", "Turn Evil", "Fist of Justice", "Greater Judgment", "Repentance/Blinding Light",
        "Lightforged Blessing",
    ],
    "left": [
        "Lay on Hands", "Blessing of Freedom", "Hammer of Wrath", "Auras of the Resolute", "Auras of Swift Vengeance", "Turn Evil", "Fist of Justice", 
        "Cavalier", "Divine Steed", "Seasoned Warhorse", "Rebuke", "Holy Aegis", "Avenging Wrath", "Justification", "Blessing of Sacrifice", 
        "Blessing of Protection", "Lightforged Blessing", "Afterimage", "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Seal of Might", 
        "Seal of Alacrity", "Faith's Armor"
    ],
    "right": [
        "Lay on Hands", "Blessing of Freedom", "Hammer of Wrath", "Auras of the Resolute", "Auras of Swift Vengeance", "Divine Steed",
        "Greater Judgment", "Repentance/Blinding Light", "Cavalier", "Seasoned Warhorse", "Holy Aegis", "Avenging Wrath", "Justification",
        "Golden Path", "Blessing of Sacrifice", "Blessing of Protection", "Unbreakable Spirit", "Improved Blessing of Protection",
        "Crusader's Reprieve", "Strength of Conviction", "Seal of Might", "Seal of Alacrity"
    ]
};

const classTalentsArrowsPTR = {
    "down": [
        "Blessing of Freedom", "Obduracy", "Rebuke", "Holy Aegis", "Avenging Wrath", "Punishment", "Golden Path", "Echoing Blessings",
        "Blessing of Sacrifice", "Sanctified Plates", "Blessing of Protection", "Seal of Mercy", "Afterimage",
        "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Improved Blessing of Protection", "Touch of Light", "Judgment of Light",
        "Divine Purpose", "Incandescence", "Of Dusk and Dawn", "Divine Toll", "Seal of the Crusader"
    ],
    "downLong": [
        "Lay on Hands", "Hammer of Wrath", "Improved Cleanse", "Turn Evil", "Fist of Justice", "Greater Judgment", "Repentance/Blinding Light",
        "Lightforged Blessing",
    ],
    "left": [
        "Lay on Hands", "Blessing of Freedom", "Hammer of Wrath", "Auras of the Resolute", "Crusader Aura", "Turn Evil", "Fist of Justice", 
        "Cavalier", "Divine Steed", "Seasoned Warhorse", "Rebuke", "Holy Aegis", "Avenging Wrath", "Justification", "Blessing of Sacrifice", 
        "Blessing of Protection", "Lightforged Blessing", "Afterimage", "Sacrifice of the Just/Recompense", "Unbreakable Spirit", "Seal of Might", 
        "Seal of Alacrity", "Faith's Armor"
    ],
    "right": [
        "Lay on Hands", "Blessing of Freedom", "Hammer of Wrath", "Auras of the Resolute", "Crusader Aura", "Divine Steed",
        "Greater Judgment", "Repentance/Blinding Light", "Cavalier", "Seasoned Warhorse", "Holy Aegis", "Avenging Wrath", "Justification",
        "Golden Path", "Blessing of Sacrifice", "Blessing of Protection", "Unbreakable Spirit", "Improved Blessing of Protection",
        "Touch of Light", "Strength of Conviction", "Seal of Might", "Seal of Alacrity"
    ]
};

const specTalentsArrowsLive = {
    "down": [
        "Glistening Radiance", "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Saved by the Light", "Light's Hammer/Holy Prism",
        "Power of the Silver Hand", "Light's Protection", "Overflowing Light", "Righteous Judgment", "Tower of Radiance", "Untempered Dedication",
        "Beacon of Faith/Beacon of Virtue", "Reclamation/Barrier of Faith", "Daybreak", "Merciful Auras/Blessing of Summer", "Tyr's Deliverance",
    ],
    "downLong": [
        "Light's Conviction", "Aura Mastery", "Beacon of the Lightbringer", "Moment of Compassion/Resplendent Light", "Tirion's Devotion",
        "Unending Light", "Awestruck/Holy Infusion", "Divine Favor/Hand of Divinity", "Light of the Martyr", "Shining Righteousness"
    ],
    "left": [
        "Holy Shock", "Glimmer of Light", "Light of Dawn", "Light's Conviction", "Beacon of the Lightbringer", "Moment of Compassion/Resplendent Light",
        "Glistening Radiance", "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Illumination/Blessed Focus", "Light's Hammer/Holy Prism",
        "Light's Protection", "Shining Righteousness", "Commanding Light", "Breaking Dawn", "Divine Glimpse", "Untempered Dedication",
        "Veneration", "Avenging Wrath: Might/Avenging Crusader", "Reclamation/Barrier of Faith", "Maraad's Dying Breath", 
        "Merciful Auras/Blessing of Summer", "Relentless Inquisitor"
    ],
    "right": [
        "Holy Shock", "Glimmer of Light", "Light of Dawn", "Light's Conviction", "Beacon of the Lightbringer", "Awestruck/Holy Infusion",
        "Glistening Radiance", "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Illumination/Blessed Focus", "Light's Hammer/Holy Prism",
        "Light's Protection", "Divine Revelations", "Commanding Light", "Breaking Dawn", "Divine Glimpse", "Beacon of Faith/Beacon of Virtue",
        "Veneration", "Avenging Wrath: Might/Avenging Crusader", "Crusader's Might", "Merciful Auras/Blessing of Summer"
    ]
};

const specTalentsArrowsPTR = {
    "down": [
        "Glistening Radiance", "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Saved by the Light", "Holy Prism/Barrier of Faith",
        "Power of the Silver Hand", "Light's Protection", "Overflowing Light", "Divine Favor/Hand of Divinity", "Tower of Radiance",
        "Reclamation/Barrier of Faith", "Daybreak", "Sanctified Wrath/Awakening",
    ],
    "downLong": [
        "Light's Conviction", "Aura Mastery", "Beacon of the Lightbringer", "Moment of Compassion/Resplendent Light", "Tirion's Devotion",
        "Unending Light", "Awestruck/Holy Infusion", "Divine Revelations", "Light of the Martyr", "Shining Righteousness",
        "Tyr's Deliverance", "Beacon of Faith/Beacon of Virtue",
    ],
    "left": [
        "Holy Shock", "Extrication", "Light of Dawn", "Light's Conviction", "Beacon of the Lightbringer", "Moment of Compassion/Resplendent Light",
        "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Liberation", "Light's Hammer/Holy Prism",
        "Light's Protection", "Shining Righteousness", "Commanding Light", "Breaking Dawn", "Divine Glimpse", "Bestow Light",
        "Veneration", "Avenging Wrath: Might/Avenging Crusader", "Reclamation/Barrier of Faith", "Maraad's Dying Breath", 
        "Sanctified Wrath/Awakening", "Relentless Inquisitor", "Tyr's Deliverance", "Saved by the Light", "Beacon of Faith/Beacon of Virtue",
    ],
    "right": [
        "Holy Shock", "Extrication", "Light of Dawn", "Light's Conviction", "Beacon of the Lightbringer", "Awestruck/Holy Infusion",
        "Unwavering Spirit/Protection of Tyr", "Imbued Infusions", "Liberation", "Light's Hammer/Holy Prism",
        "Light's Protection", "Righteous Judgment", "Commanding Light", "Breaking Dawn", "Divine Glimpse", "Beacon of Faith/Beacon of Virtue",
        "Veneration", "Avenging Wrath: Might/Avenging Crusader", "Crusader's Might", "Sanctified Wrath/Awakening", "Tyr's Deliverance",
        "Saved by the Light"
    ]
};

const heroTalentsLightsmith = [
    "", "Holy Bulwark", "",
    "Rite of Sanctification/Rite of Adjuration", "Solidarity", "Divine Guidance/Blessed Assurance",
    "Laying Down Arms", "Divine Inspiration/Forewarning", "Fear No Evil/Excoriation",
    "Shared Resolve", "Valiance", "Hammer and Anvil",
    "", "Blessing of the Forge", ""
];

const heroTalentsHeraldOfTheSun = [
    "", "Dawnlight", "",
    "Morning Star/Gleaming Rays", "Eternal Flame", "Luminosity",
    "Illumine/Will of the Dawn", "Blessing of An'she/Lingering Radiance", "Sun Sear",
    "Aurora", "Solar Grace", "Second Sunrise",
    "", "Sun's Avatar", ""
];

let baseLightsmithTalents = {
    "row1": {
        "Holy Bulwark": {"ranks": {"current rank": 0, "max rank": 1}},
    },
    "row2": {
        "Rite of Sanctification": {"ranks": {"current rank": 0, "max rank": 1}},
        "Rite of Adjuration": {"ranks": {"current rank": 0, "max rank": 1}},
        "Solidarity": {"ranks": {"current rank": 0, "max rank": 1}},
        "Divine Guidance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessed Assurance": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row3": {
        "Laying Down Arms": {"ranks": {"current rank": 0, "max rank": 1}},
        "Divine Inspiration": {"ranks": {"current rank": 0, "max rank": 1}},
        "Forewarning": {"ranks": {"current rank": 0, "max rank": 1}},
        "Fear No Evil": {"ranks": {"current rank": 0, "max rank": 1}},
        "Excoriation": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Shared Resolve": {"ranks": {"current rank": 0, "max rank": 1}},
        "Valiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Hammer and Anvil": {"ranks": {"current rank": 0, "max rank": 1}},
    },
    "row5": {
        "Blessing of the Forge": {"ranks": {"current rank": 0, "max rank": 1}},
    },
};

const lightsmithTalentsArrows = {
    "down": [
        "Holy Bulwark", "Rite of Sanctification/Rite of Adjuration", "Solidarity", "Divine Guidance/Blessed Assurance",
        "Laying Down Arms", "Divine Inspiration/Forewarning", "Fear No Evil/Excoriation", "Valiance"
    ],
    "left": [
        "Holy Bulwark", "Hammer and Anvil"
    ],
    "right": [
        "Holy Bulwark", "Shared Resolve"
    ]
};

let baseHeraldOfTheSunTalents = {
    "row1": {
        "Dawnlight": {"ranks": {"current rank": 0, "max rank": 1}},
    },
    "row2": {
        "Morning Star": {"ranks": {"current rank": 0, "max rank": 1}},
        "Gleaming Rays": {"ranks": {"current rank": 0, "max rank": 1}},
        "Eternal Flame": {"ranks": {"current rank": 0, "max rank": 1}},
        "Luminosity": {"ranks": {"current rank": 0, "max rank": 1}},      
    },
    "row3": {
        "Illumine": {"ranks": {"current rank": 0, "max rank": 1}},
        "Will of the Dawn": {"ranks": {"current rank": 0, "max rank": 1}},
        "Blessing of An'she": {"ranks": {"current rank": 0, "max rank": 1}},
        "Lingering Radiance": {"ranks": {"current rank": 0, "max rank": 1}},
        "Sun Sear": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row4": {
        "Aurora": {"ranks": {"current rank": 0, "max rank": 1}},
        "Solar Grace": {"ranks": {"current rank": 0, "max rank": 1}},
        "Second Sunrise": {"ranks": {"current rank": 0, "max rank": 1}}
    },
    "row5": {
        "Sun's Avatar": {"ranks": {"current rank": 0, "max rank": 1}}
    },
};

const heraldOfTheSunTalentsArrows = {
    "down": [
        "Dawnlight", "Morning Star/Gleaming Rays", "Eternal Flame", "Luminosity", "Illumine/Will of the Dawn",
        "Blessing of An'she/Lingering Radiance", "Sun Sear", "Solar Grace"
    ],
    "left": [
        "Dawnlight", "Second Sunrise"
    ],
    "right": [
        "Dawnlight", "Aurora"
    ]
};
        
export { classTalentsLive, classTalentsPTR, specTalentsLive, specTalentsPTR, baseClassTalentsLive, baseClassTalentsPTR, baseSpecTalentsLive, baseSpecTalentsPTR, classTalentsArrowsLive, classTalentsArrowsPTR, specTalentsArrowsLive, specTalentsArrowsPTR, heroTalentsLightsmith, heroTalentsHeraldOfTheSun, baseLightsmithTalents, baseHeraldOfTheSunTalents, lightsmithTalentsArrows, heraldOfTheSunTalentsArrows };