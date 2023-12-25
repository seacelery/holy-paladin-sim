# 💀

import random
# import battlenet_api
# import cache
import pprint
import requests
from collections import OrderedDict
pp = pprint.PrettyPrinter(width=200)

def get_character_data(access_token, realm, character_name):
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm}/{character_name}?namespace=profile-eu&locale=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

# def get_misc_data(access_token, realm, character_name):
#     url = f"https://eu.api.blizzard.com/data/wow/talent-tree/790/playable-specialization/65?namespace=static-10.2.0_51825-eu&locale=en_GB&access_token={access_token}"
#     response = requests.get(url)
#     return response.json()

def get_talent_data(access_token, realm, character_name):
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm}/{character_name}/specializations?namespace=profile-eu&locale=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "y3TJQqhljQ7fp50BWMLlvEoIr7yrfxBg"

# access_token = battlenet_api.get_access_token(client_id, client_secret)
access_token = 3

realm = 'twisting-nether'
character_name = 'skaneschnell'

# character_data = get_character_data(access_token, realm, character_name)
# pp.pprint(character_data)
talent_data = get_talent_data(access_token, realm, character_name)

class_talents = {}
spec_talents = {}

class_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_class_talents"]
for talent in class_talent_data:
    talent_name = talent["tooltip"]["talent"]["name"]
    talent_rank = talent["rank"]
    class_talents[talent_name] = talent_rank
    
spec_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_spec_talents"]
for talent in spec_talent_data:
    talent_name = talent["tooltip"]["talent"]["name"]
    talent_rank = talent["rank"]
    spec_talents[talent_name] = talent_rank    
    
active_class_talents = {
        "row1": {
            "Lay on Hands": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Blessing of Freedom": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Hammer of Wrath": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row2": {
            "Improved Cleanse": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Auras of the Resolute": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Obduracy": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Auras of Swift Vengeance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Turn Evil": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row3": {
            "Fist of Justice": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Divine Steed": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Greater Judgment": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row4": {
            "Repentance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Blinding Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Cavalier": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Seasoned Warhorse": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Rebuke": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
        },
        "row5": {
            "Divine Aegis": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Avenging Wrath": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Justification": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Punishment": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row6": {
            "Golden Path": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Echoing Blessings": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Blessing of Sacrifice": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Sanctified Plates": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Blessing of Protection": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Lightforged Blessing": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row7": {
            "Seal of Mercy": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Afterimage": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Sacrifice of the Just": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Recompense": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Unbreakable Spirit": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Improved Blessing of Protection": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Crusader's Reprieve": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row8": {
            "Strength of Conviction": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Judgment of Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Seal of Might": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Divine Purpose": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Seal of Alacrity": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Incandescence": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Touch of Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Faith's Armor": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row9": {
            "Of Dusk and Dawn": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Divine Toll": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Seal of the Crusader": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            }
        },
        "row10": {
            "Seal of Order": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Fading Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Divine Resonance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Quickened Invocation": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Vanguard's Momentum": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        }
    }

active_spec_talents = {
        "row1": {
            "Holy Shock": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row2": {
            "Glimmer of Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Light of Dawn": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row3": {
            "Light's Conviction": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Aura Mastery": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Beacon of the Lightbringer": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row4": {
            "Moment of Compassion": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Resplendent Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Tirion's Devotion": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Unending Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Awestruck": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Holy Infusion": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row5": {
            "Divine Favor": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Hand of Divinity": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Glistening Radiance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Unwavering Spirit": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Protection of Tyr": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Imbued Infusions": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Light of the Martyr": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row6": {
            "Illumination": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Blessed Focus": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Saved by the Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Light's Hammer": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Holy Prism": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Power of the Silver Hand": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Light's Protection": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Overflowing Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Shining Righteousness": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row7": {
            "Divine Revelations": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Commanding Light": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Righteous Judgment": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Breaking Dawn": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 2
                }
            },
            "Tower of Radiance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Divine Glimpse": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Untempered Dedication": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row8": {
            "Beacon of Faith": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Beacon of Virtue": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Veneration": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Avenging Wrath: Might": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Avenging Crusader": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Reclamation": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Barrier of Faith": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Maraad's Dying Breath": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        },
        "row9": {
            "Daybreak": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Crusader's Might": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Merciful Auras": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Blessing of Summer": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Relentless Inquisitor": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Tyr's Deliverance": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
        },
        "row10": {
            "Rising Sunlight": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Glorious Dawn": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Sanctified Wrath": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Awakening": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Inflorescence of the Sunwell": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Empyrean Legacy": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            },
            "Boundless Salvation": {
                "ranks": {
                    "current rank": 0,
                    "max rank": 1
                }
            }
        }
    }

total_class_points = 0
total_spec_points = 0

for talent_row, talents in active_class_talents.items():
    for talent_name, talent_info in talents.items():
        if talent_name in class_talents:
            active_class_talents[talent_row][talent_name]["ranks"]["current rank"] = class_talents[talent_name]
            total_spec_points += active_class_talents[talent_row][talent_name]["ranks"]["current rank"]
            
for talent_row, talents in active_spec_talents.items():
    for talent_name, talent_info in talents.items():
        if talent_name in spec_talents:
            active_spec_talents[talent_row][talent_name]["ranks"]["current rank"] = spec_talents[talent_name]
            total_spec_points += active_spec_talents[talent_row][talent_name]["ranks"]["current rank"]
    

