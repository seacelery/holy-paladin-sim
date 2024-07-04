from ..classes.auras_buffs import (
                                   PhialOfTepidVersatility, PhialOfElementalChaos, DraconicAugmentRune, GrandBanquetOfTheKaluakFood, 
                                   TimelyDemiseFood, FiletOfFangsFood, SeamothSurpriseFood, SaltBakedFishcakeFood, FeistyFishSticksFood, 
                                   AromaticSeafoodPlatterFood, SizzlingSeafoodMedleyFood, RevengeServedColdFood, ThousandboneTongueslicerFood, 
                                   GreatCeruleanSeaFood, BuzzingRune, ChirpingRune, HowlingRune, HissingRune, ArcaneIntellect, MarkOfTheWild, 
                                   CloseToHeart, RetributionAura, SourceOfMagic, PowerInfusion, Innervate, PotionAbsorptionInhibitor,
                                   AlliedChestplateOfGenerosity, AlliedWristguardOfCompanionship, VerdantConduit, VerdantTether, ElementalLariat,
                                   DreamtendersCharm, IcedPhialOfCorruptingRage, ManaSpringTotem, SymbolOfHope, MagazineOfHealingDarts,
                                   BronzedGripWrappings, ManaTideTotem, FlaskOfSavingGraces, FlaskOfTemperedAggression, FlaskOfAlchemicalChaos,
                                   FlaskOfTemperedMastery, FlaskOfTemperedSwiftness, FlaskOfTemperedVersatility, CrystallizedAugmentRune,
                                   AlgariManaOil, OilOfBeledarsGrace, Skyfury
                                  )

buff_class_map = {
    # flasks
    "Phial of Tepid Versatility": PhialOfTepidVersatility,
    "Phial of Elemental Chaos": PhialOfElementalChaos,
    "Iced Phial of Corrupting Rage": IcedPhialOfCorruptingRage,
    "Flask of Saving Graces": FlaskOfSavingGraces,
    "Flask of Tempered Aggression": FlaskOfTemperedAggression,
    "Flask of Alchemical Chaos": FlaskOfAlchemicalChaos,
    "Flask of Tempered Mastery": FlaskOfTemperedMastery,
    "Flask of Tempered Swiftness": FlaskOfTemperedSwiftness,
    "Flask of Tempered Versatility": FlaskOfTemperedVersatility,
    
    # augment runes
    "Draconic Augment Rune": DraconicAugmentRune,
    "Crystallized Augment Rune": CrystallizedAugmentRune,
    
    # food
    "Grand Banquet of the Kalu'ak": GrandBanquetOfTheKaluakFood,
    "Timely Demise": TimelyDemiseFood,
    "Filet of Fangs": FiletOfFangsFood,
    "Seamoth Surprise": SeamothSurpriseFood,
    "Salt-Baked Fishcake": SaltBakedFishcakeFood,
    "Feisty Fish Sticks": FeistyFishSticksFood,
    "Aromatic Seafood Platter": AromaticSeafoodPlatterFood,
    "Sizzling Seafood Medley": SizzlingSeafoodMedleyFood,
    "Revenge, Served Cold": RevengeServedColdFood,
    "Thousandbone Tongueslicer": ThousandboneTongueslicerFood,
    "Great Cerulean Sea": GreatCeruleanSeaFood,
    
    # weapon imbues
    "Buzzing Rune": BuzzingRune,
    "Howling Rune": HowlingRune,
    "Chirping Rune": ChirpingRune,
    "Hissing Rune": HissingRune,
    "Algari Mana Oil": AlgariManaOil,
    "Oil of Beledar's Grace": OilOfBeledarsGrace,
    
    # raid buffs
    "Arcane Intellect": ArcaneIntellect,
    "Mark of the Wild": MarkOfTheWild,
    "Close to Heart": CloseToHeart,
    "Skyfury": Skyfury,
    # "Retribution Aura": RetributionAura,
    "Symbol of Hope": SymbolOfHope,
    "Mana Spring Totem": ManaSpringTotem,
    "Mana Tide Totem": ManaTideTotem,
    
    # external buffs
    "Source of Magic": SourceOfMagic,
    "Innervate": Innervate,
    "Power Infusion": PowerInfusion,
    
    # embellishments
    "Potion Absorption Inhibitor": PotionAbsorptionInhibitor,
    "Verdant Tether": VerdantTether,
    "Verdant Conduit": VerdantConduit,
    "Dreamtender's Charm": DreamtendersCharm,
    "Magazine of Healing Darts": MagazineOfHealingDarts,
    "Bronzed Grip Wrappings": BronzedGripWrappings,
    
    "Elemental Lariat": ElementalLariat,
    "Allied Chestplate of Generosity": AlliedChestplateOfGenerosity,
    "Allied Wristgaurds of Companionship": AlliedWristguardOfCompanionship,
}