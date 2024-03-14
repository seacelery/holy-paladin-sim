from ..classes.auras_buffs import (
                                   PhialOfTepidVersatility, PhialOfElementalChaos, DraconicAugmentRune, GrandBanquetOfTheKaluakFood, 
                                   TimelyDemiseFood, FiletOfFangsFood, SeamothSurpriseFood, SaltBakedFishcakeFood, FeistyFishSticksFood, 
                                   AromaticSeafoodPlatterFood, SizzlingSeafoodMedleyFood, RevengeServedColdFood, ThousandboneTongueslicerFood, 
                                   GreatCeruleanSeaFood, BuzzingRune, ChirpingRune, HowlingRune, HissingRune, ArcaneIntellect, MarkOfTheWild, 
                                   CloseToHeart, RetributionAura, SourceOfMagic, PowerInfusion, Innervate, PotionAbsorptionInhibitor,
                                   AlliedChestplateOfGenerosity, AlliedWristguardOfCompanionship, VerdantConduit, VerdantTether, ElementalLariat,
                                   DreamtendersCharm
                                  )

buff_class_map = {
    # flasks
    "Phial of Tepid Versatility": PhialOfTepidVersatility,
    "Phial of Elemental Chaos": PhialOfElementalChaos,
    
    # augment runes
    "Draconic Augment Rune": DraconicAugmentRune,
    
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
    
    # raid buffs
    "Arcane Intellect": ArcaneIntellect,
    "Mark of the Wild": MarkOfTheWild,
    "Close to Heart": CloseToHeart,
    "Retribution Aura": RetributionAura,
    
    # external buffs
    "Source of Magic": SourceOfMagic,
    "Innervate": Innervate,
    "Power Infusion": PowerInfusion,
    
    # embellishments
    "Potion Absorption Inhibitor": PotionAbsorptionInhibitor,
    "Verdant Tether": VerdantTether,
    "Verdant Conduit": VerdantConduit,
    "Dreamtender's Charm": DreamtendersCharm,
    
    "Elemental Lariat": ElementalLariat,
    "Allied Chestplate of Generosity": AlliedChestplateOfGenerosity,
    "Allied Wristgaurds of Companionship": AlliedWristguardOfCompanionship,
}