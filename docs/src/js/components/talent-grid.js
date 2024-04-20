import { baseClassTalents, baseSpecTalents, classTalentsDown, classTalentsDownLong, classTalentsLeft, classTalentsRight, specTalentsDown, specTalentsDownLong, specTalentsLeft, specTalentsRight, baseLightsmithTalents, baseHeraldOfTheSunTalents, lightsmithTalentsDown, lightsmithTalentsLeft, lightsmithTalentsRight, heraldOfTheSunTalentsDown, heraldOfTheSunTalentsLeft, heraldOfTheSunTalentsRight } from "../utils/base-talents.js";
import { createElement, updateCharacter, updateStats } from "./index.js";
import { talentsToIcons } from "../utils/talents-to-icons-map.js";
import { createTooltip, addTooltipFunctionality } from "../utils/misc-functions.js";
import { futurePatchSelected } from "./config/version-config.js";

const classTalents = [
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

const specTalents = [
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

const toggleTalentOptions = (talentName, talentData) => {
    switch(true) {
        case talentName === "Light of Dawn":
            document.getElementById("light-of-dawn-option-container").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";
            break;
        case talentName === "Light's Hammer":
            document.getElementById("lights-hammer-option-container").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";
            break;
        case talentName === "Resplendent Light":
            document.getElementById("resplendent-light-option-container").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";  
            break;
        case talentName === "Reclamation":
            document.getElementById("raid-health-option-container").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";  
            break;
        case talentName === "Avenging Wrath":
            document.getElementById("cooldown-tracking-avenging-wrath-option").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none"; 
            break;
        case talentName === "Awakening":
            document.getElementById("cooldown-tracking-avenging-wrath-awakening-option").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none"; 
            break;
        case talentName === "Rising Sunlight":
            document.getElementById("cooldown-tracking-rising-sunlight-option").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";  
            break;
        case talentName === "Blessing of Summer":
            document.getElementById("cooldown-tracking-blessing-of-spring-option").style.display = talentData.ranks["current rank"] === 1 ? "flex" : "none";
            break;
    };
};

const updateTalentsFromImportedData = (importedTalents) => {
    let importedClassTalents = importedTalents.class_talents;
    let importedSpecTalents = importedTalents.spec_talents;

    const updateTalents = (imported, baseTalents, category) => {
        let classTalentsCount = 0;
        let specTalentsCount = 0;

        for (const row in imported) {
            for (const talentName in imported[row]) {
                const talentData = imported[row][talentName];
                const formattedTalentName = talentName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
                const talentIcon = document.getElementById(formattedTalentName + "-icon");
                
                if (talentData && talentIcon) {
                    if (baseTalents[row] && baseTalents[row][talentName]) {
                        baseTalents[row][talentName].ranks["current rank"] = talentData.ranks["current rank"];
                    };
                    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                    if (talentData.ranks["max rank"] > 1) {
                        const rankDisplay = talentIcon.parentElement.querySelector(".talent-rank-display");
                        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
                    };

                    if (talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.style.boxShadow = "0px 0px 4px var(--gold-font)";
                        talentIcon.style.boxShadow = "0px 0px 1px var(--border-colour-2)";
                    };

                    toggleTalentOptions(talentName, talentData);

                    if (category === "class") {
                        classTalentsCount += talentData.ranks["current rank"];
                    } else if (category === "spec") {
                        specTalentsCount += talentData.ranks["current rank"];
                    };

                    // class talents
                    if (talentIcon.parentElement.querySelector(".class-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".class-talents-option-down").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".class-talents-option-down-long") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".class-talents-option-down-long").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".class-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".class-talents-option-left").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".class-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".class-talents-option-right").classList.add("talent-option-highlighted");
                    };

                    // spec talents
                    if (talentIcon.parentElement.querySelector(".spec-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".spec-talents-option-down").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".spec-talents-option-down-long") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".spec-talents-option-down-long").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".spec-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".spec-talents-option-left").classList.add("talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".spec-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".spec-talents-option-right").classList.add("talent-option-highlighted");
                    };

                    // hero talents
                    if (talentIcon.parentElement.querySelector(".hero-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".hero-talents-option-down").classList.add("hero-talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".hero-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".hero-talents-option-left").classList.add("hero-talent-option-highlighted");
                    };
                    if (talentIcon.parentElement.querySelector(".hero-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
                        talentIcon.parentElement.querySelector(".hero-talents-option-right").classList.add("hero-talent-option-highlighted");
                    };
                };
            };
        };
        
        if (category === "class") {
            const freeTalentsCount = 3;
            const classTalents = document.getElementById("class-talents");
            classTalents.setAttribute("data-class-talents-count", classTalentsCount - freeTalentsCount);
        } else if (category === "spec") {
            const freeTalentsCount = 0;
            const specTalents = document.getElementById("spec-talents");
            specTalents.setAttribute("data-specs-talents-count", specTalentsCount - freeTalentsCount);
        };

        updateTalentCounts("class");
        updateTalentCounts("spec");
    };

    updateTalents(importedClassTalents, baseClassTalents, "class");
    updateTalents(importedSpecTalents, baseSpecTalents, "spec");    
};

const updateTalentCounts = (category, pointsToAdd = 0) => {
    if (category === "class") {
        const classTalents = document.getElementById("class-talents");
        let classTalentsCount = Number(classTalents.getAttribute("data-class-talents-count"));
        classTalentsCount += pointsToAdd;

        const classTalentsCountText = document.getElementById("class-talents-count");
        const classTalentsTotalText = document.getElementById("class-talents-total");
        classTalentsCountText.textContent = classTalentsCount;
        
        classTalents.setAttribute("data-class-talents-count", classTalentsCount);

        if (classTalentsCount == 31) {
            classTalentsCountText.style.color = "var(--healing-font)";
            classTalentsTotalText.style.color = "var(--healing-font)";
        } else if (classTalentsCount > 31) {
            classTalentsCountText.style.color = "var(--red-font-hover)";
            classTalentsTotalText.style.color = "var(--red-font-hover)";
        } else if (classTalentsCount < 31) {
            classTalentsCountText.style.color = "var(--light-font-colour)";
            classTalentsTotalText.style.color = "var(--light-font-colour)";
        };
    } else if (category === "spec") {
        const specTalents = document.getElementById("spec-talents");
        let specTalentsCount = Number(specTalents.getAttribute("data-specs-talents-count"));
        specTalentsCount += pointsToAdd;

        const specTalentsCountText = document.getElementById("spec-talents-count");
        const specTalentsTotalText = document.getElementById("spec-talents-total");
        specTalentsCountText.textContent = specTalentsCount;

        specTalents.setAttribute("data-specs-talents-count", specTalentsCount);

        if (specTalentsCount == 30) {
            specTalentsCountText.style.color = "var(--healing-font)";
            specTalentsTotalText.style.color = "var(--healing-font)";
        } else if (specTalentsCount > 30) {
            specTalentsCountText.style.color = "var(--red-font-hover)";
            specTalentsTotalText.style.color = "var(--red-font-hover)";
        } else if (specTalentsCount < 31) {
            specTalentsCountText.style.color = "var(--light-font-colour)";
            specTalentsTotalText.style.color = "var(--light-font-colour)";
        };
    } else if (category === "lightsmith" || category === "herald-of-the-sun") {
        const heroTalents = document.getElementById("hero-talents-modal");
        let heroTalentsCount = Number(heroTalents.getAttribute("data-hero-talents-count"));
        heroTalentsCount += pointsToAdd;

        const heroTalentsCountText = document.getElementById("hero-talents-count");
        const heroTalentsTotalText = document.getElementById("hero-talents-total");
        heroTalentsCountText.textContent = heroTalentsCount;

        heroTalents.setAttribute("data-hero-talents-count", heroTalentsCount);

        if (heroTalentsCount == 11) {
            heroTalentsCountText.style.color = "var(--healing-font)";
            heroTalentsTotalText.style.color = "var(--healing-font)";
        } else if (heroTalentsCount > 11) {
            heroTalentsCountText.style.color = "var(--red-font-hover)";
            heroTalentsTotalText.style.color = "var(--red-font-hover)";
        } else if (heroTalentsCount < 12) {
            heroTalentsCountText.style.color = "var(--light-font-colour)";
            heroTalentsTotalText.style.color = "var(--light-font-colour)";
        };

        const lightsmithHeader = document.getElementById("lightsmith-header");
        const heraldOfTheSunHeader = document.getElementById("herald-of-the-sun-header");

        const lightsmithTalents = document.getElementById("lightsmith-talent-grid");
        const heraldOfTheSunTalents = document.getElementById("herald-of-the-sun-talent-grid");

        const heraldOfTheSunIcon = document.getElementById("herald-of-the-sun-icon");
        const lightsmithIcon = document.getElementById("lightsmith-icon");

        if (category === "lightsmith") {
            let lightsmithTalentsCount = Number(lightsmithTalents.getAttribute("data-lightsmith-talents-count"));
            lightsmithTalentsCount += pointsToAdd;
            lightsmithTalents.setAttribute("data-lightsmith-talents-count", lightsmithTalentsCount);

            lightsmithHeader.style.backgroundColor = "var(--panel-colour-3)";
            lightsmithTalents.style.backgroundColor = "var(--tooltip-colour)";
            heraldOfTheSunHeader.style.backgroundColor = "var(--panel-colour-2)";
            heraldOfTheSunTalents.style.backgroundColor = "var(--panel-colour)";

            lightsmithIcon.style.filter = "grayscale(0)";
            lightsmithIcon.style.boxShadow = "0px 0px 3px 1px var(--paladin-font)";
            heraldOfTheSunIcon.style.filter = "grayscale(1)";
            heraldOfTheSunIcon.style.boxShadow = "none";
        };

        if (category === "herald-of-the-sun") {
            let heraldOfTheSunTalentsCount = Number(heraldOfTheSunTalents.getAttribute("data-herald-of-the-sun-talents-count"));
            heraldOfTheSunTalentsCount += pointsToAdd;
            heraldOfTheSunTalents.setAttribute("data-herald-of-the-sun-talents-count", heraldOfTheSunTalentsCount);

            heraldOfTheSunHeader.style.backgroundColor = "var(--panel-colour-3)";
            heraldOfTheSunTalents.style.backgroundColor = "var(--tooltip-colour)";
            lightsmithHeader.style.backgroundColor = "var(--panel-colour-2)";
            lightsmithTalents.style.backgroundColor = "var(--panel-colour)";

            heraldOfTheSunIcon.style.filter = "grayscale(0)";
            heraldOfTheSunIcon.style.boxShadow = "0px 0px 3px 1px var(--paladin-font)";
            lightsmithIcon.style.filter = "grayscale(1)";
            lightsmithIcon.style.boxShadow = "none";
        };

        const lightsmithTalentCount = Number(lightsmithTalents.getAttribute("data-lightsmith-talents-count"));
        const heraldOfTheSunTalentCount = Number(heraldOfTheSunTalents.getAttribute("data-herald-of-the-sun-talents-count"));

        if (category === "lightsmith" && heraldOfTheSunTalentCount > 0) {
            heraldOfTheSunTalents.setAttribute("data-herald-of-the-sun-talents-count", 0);
            resetHeroTalents("herald_of_the_sun");

            heroTalentsCount = 1;
            heroTalents.setAttribute("data-hero-talents-count", heroTalentsCount);
            heroTalentsCountText.textContent = heroTalentsCount;

            if (heroTalentsCount == 11) {
                heroTalentsCountText.style.color = "var(--healing-font)";
                heroTalentsTotalText.style.color = "var(--healing-font)";
            } else if (heroTalentsCount > 11) {
                heroTalentsCountText.style.color = "var(--red-font-hover)";
                heroTalentsTotalText.style.color = "var(--red-font-hover)";
            } else if (heroTalentsCount < 12) {
                heroTalentsCountText.style.color = "var(--light-font-colour)";
                heroTalentsTotalText.style.color = "var(--light-font-colour)";
            };
        };

        if (category === "herald-of-the-sun" && lightsmithTalentCount > 0) {
            lightsmithTalents.setAttribute("data-lightsmith-talents-count", 0);
            resetHeroTalents("lightsmith");

            heroTalentsCount = 1;
            heroTalents.setAttribute("data-hero-talents-count", heroTalentsCount);
            heroTalentsCountText.textContent = heroTalentsCount;

            if (heroTalentsCount == 11) {
                heroTalentsCountText.style.color = "var(--healing-font)";
                heroTalentsTotalText.style.color = "var(--healing-font)";
            } else if (heroTalentsCount > 11) {
                heroTalentsCountText.style.color = "var(--red-font-hover)";
                heroTalentsTotalText.style.color = "var(--red-font-hover)";
            } else if (heroTalentsCount < 12) {
                heroTalentsCountText.style.color = "var(--light-font-colour)";
                heroTalentsTotalText.style.color = "var(--light-font-colour)";
            };
        };

        if (lightsmithTalentCount === 0) {
            lightsmithHeader.style.backgroundColor = "var(--panel-colour-2)";
            lightsmithIcon.style.filter = "grayscale(1)";
            lightsmithIcon.style.boxShadow = "none";
        };

        if (heraldOfTheSunTalentCount === 0) {
            heraldOfTheSunHeader.style.backgroundColor = "var(--panel-colour-2)";
            heraldOfTheSunIcon.style.filter = "grayscale(1)";
            heraldOfTheSunIcon.style.boxShadow = "none";
        };
    };
};

const resetHeroTalents = (talentSet) => {
    let talentUpdate = {
        "lightsmith_talents": {},
        "herald_of_the_sun_talents": {}
    };

    if (talentSet == "lightsmith") {
        ["Holy Bulwark", "Rite of Sanctification", "Rite of Adjuration", "Solidarity", "Divine Guidance", "Blessed Assurance",
        "Laying Down Arms", "Divine Inspiration", "Forewarning", "Fear No Evil", "Excoriation", "Shared Resolve", "Valiance",
        "Hammer and Anvil", "Blessing of the Forge"].forEach(talent => {
            talentUpdate[talent] = 0;
            let formattedTalentName = talent.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
            const talentIcon = document.getElementById(`${formattedTalentName}-icon`);
            decrementTalent(talent, findTalentInTalentsData(baseLightsmithTalents, talent), talentIcon, null);
        });
    };

    if (talentSet == "herald_of_the_sun") {
        ["Dawnlight", "Morning Star", "Gleaming Rays", "Eternal Flame", "Luminosity", "Illumine", "Will of the Dawn",
        "Blessing of An'she", "Lingering Radiance", "Sun Sear", "Aurora", "Solar Grace", "Second Sunrise", "Sun's Avatar"].forEach(talent => {
            talentUpdate[talent] = 0;
            let formattedTalentName = talent.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
            const talentIcon = document.getElementById(`${formattedTalentName}-icon`);
            decrementTalent(talent, findTalentInTalentsData(baseHeraldOfTheSunTalents, talent), talentIcon, null);
        });
    };

    updateCharacter(talentUpdate);
};

const handleTalentChange = (talentName, talentData, multipleTalentChanges = false) => {
    let talentUpdate = {
        "class_talents": {},
        "spec_talents": {},
        "lightsmith_talents": {},
        "herald_of_the_sun_talents": {}
    };

    if (multipleTalentChanges) {
        for (let i = 0; i < talentName.length; i++) {
            const currentTalentName = talentName[i];
            const currentTalentData = talentData[i];
            const talentValue = currentTalentData.ranks["current rank"];

            const isClassTalent = classTalents.some(t => t.includes(currentTalentName));
            const isSpecTalent = specTalents.some(t => t.includes(currentTalentName));
            const isLightsmithTalent = heroTalentsLightsmith.some(t => t.includes(currentTalentName));
            const isHeraldOfTheSunTalent = heroTalentsHeraldOfTheSun.some(t => t.includes(currentTalentName));

            if (isClassTalent) {
                console.log("Updating class talent");
                talentUpdate.class_talents[currentTalentName] = talentValue;
            } else if (isSpecTalent) {
                console.log("Updating spec talent");
                talentUpdate.spec_talents[currentTalentName] = talentValue;
            } else if (isLightsmithTalent) {
                console.log("Updating lightsmith talent");
                talentUpdate.lightsmith_talents[currentTalentName] = talentValue;
            } else if (isHeraldOfTheSunTalent) {
                console.log("Updating herald of the sun talent");
                talentUpdate.herald_of_the_sun_talents[currentTalentName] = talentValue;
            };
        }
    } else {
        const talentValue = talentData.ranks["current rank"];

        const isClassTalent = classTalents.some(t => t.includes(talentName));
        const isSpecTalent = specTalents.some(t => t.includes(talentName));
        const isLightsmithTalent = heroTalentsLightsmith.some(t => t.includes(talentName));
        const isHeraldOfTheSunTalent = heroTalentsHeraldOfTheSun.some(t => t.includes(talentName));

        if (isClassTalent) {
            console.log("Updating class talent");
            talentUpdate.class_talents[talentName] = talentValue;
        } else if (isSpecTalent) {
            console.log("Updating spec talent");
            talentUpdate.spec_talents[talentName] = talentValue;
        } else if (isLightsmithTalent) {
            console.log("Updating lightsmith talent");
            talentUpdate.lightsmith_talents[talentName] = talentValue;
        } else if (isHeraldOfTheSunTalent) {
            console.log("Updating herald of the sun talent");
            talentUpdate.herald_of_the_sun_talents[talentName] = talentValue;
        };
    }

    if (Object.keys(talentUpdate.class_talents).length === 0) {
        delete talentUpdate.class_talents;
    };
    if (Object.keys(talentUpdate.spec_talents).length === 0) {
        delete talentUpdate.spec_talents;
    };
    if (Object.keys(talentUpdate.lightsmith_talents).length === 0) {
        delete talentUpdate.lightsmith_talents;
    };
    if (Object.keys(talentUpdate.herald_of_the_sun_talents).length === 0) {
        delete talentUpdate.herald_of_the_sun_talents;
    };

    updateCharacter(talentUpdate);
};

const findTalentInTalentsData = (baseTalents, talentName) => {
    for (let row in baseTalents) {
        if (baseTalents[row][talentName]) {
            return baseTalents[row][talentName];
        };
    };
    return null;
};

const incrementTalent = (talentName, talentData, talentIcon, category) => {
    if (talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
        talentData.ranks["current rank"] += 1;
    };
    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

    if (talentData.ranks["max rank"] > 1) {
        const rankDisplay = talentIcon.parentElement.querySelector(".talent-rank-display");
        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
    };

    if (talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.style.boxShadow = "0px 0px 4px var(--gold-font)";
        talentIcon.style.boxShadow = "none";
    };

    toggleTalentOptions(talentName, talentData);

    updateTalentCounts(category, 1);

    // class talents
    if (talentIcon.parentElement.querySelector(".class-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".class-talents-option-down").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-down-long") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".class-talents-option-down-long").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".class-talents-option-left").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".class-talents-option-right").classList.add("talent-option-highlighted");
    };

    // spec talents
    if (talentIcon.parentElement.querySelector(".spec-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".spec-talents-option-down").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-down-long") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".spec-talents-option-down-long").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".spec-talents-option-left").classList.add("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".spec-talents-option-right").classList.add("talent-option-highlighted");
    };

    // hero talents
    if (talentIcon.parentElement.querySelector(".hero-talents-option-down") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".hero-talents-option-down").classList.add("hero-talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".hero-talents-option-left") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".hero-talents-option-left").classList.add("hero-talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".hero-talents-option-right") && talentData.ranks["current rank"] === talentData.ranks["max rank"]) {
        talentIcon.parentElement.querySelector(".hero-talents-option-right").classList.add("hero-talent-option-highlighted");
    };
};

const decrementTalent = (talentName, talentData, talentIcon, category) => {
    if (talentData.ranks["current rank"] > 0) {
        talentData.ranks["current rank"] -= 1;
    };

    talentIcon.style.filter = talentData.ranks["current rank"] === 0 ? "saturate(0)" : "saturate(1)";

    if (talentData.ranks["max rank"] > 1) {
        const rankDisplay = talentIcon.parentElement.querySelector(".talent-rank-display");
        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
    };

    if (talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
        talentIcon.style.boxShadow = "0px 0px 1px var(--border-colour-2)";
        talentIcon.parentElement.style.boxShadow = "none";
    };

    toggleTalentOptions(talentName, talentData);

    updateTalentCounts(category, -1);  

    // class talents
    if (talentIcon.parentElement.querySelector(".class-talents-option-down")) {
        talentIcon.parentElement.querySelector(".class-talents-option-down").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-down-long")) {
        talentIcon.parentElement.querySelector(".class-talents-option-down-long").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-left")) {
        talentIcon.parentElement.querySelector(".class-talents-option-left").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".class-talents-option-right")) {
        talentIcon.parentElement.querySelector(".class-talents-option-right").classList.remove("talent-option-highlighted");
    };

    // spec talents
    if (talentIcon.parentElement.querySelector(".spec-talents-option-down")) {
        talentIcon.parentElement.querySelector(".spec-talents-option-down").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-down-long")) {
        talentIcon.parentElement.querySelector(".spec-talents-option-down-long").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-left")) {
        talentIcon.parentElement.querySelector(".spec-talents-option-left").classList.remove("talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".spec-talents-option-right")) {
        talentIcon.parentElement.querySelector(".spec-talents-option-right").classList.remove("talent-option-highlighted");
    };

    // hero talents
    if (talentIcon.parentElement.querySelector(".hero-talents-option-down")) {
        talentIcon.parentElement.querySelector(".hero-talents-option-down").classList.remove("hero-talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".hero-talents-option-left")) {
        talentIcon.parentElement.querySelector(".hero-talents-option-left").classList.remove("hero-talent-option-highlighted");
    };
    if (talentIcon.parentElement.querySelector(".hero-talents-option-right")) {
        talentIcon.parentElement.querySelector(".hero-talents-option-right").classList.remove("hero-talent-option-highlighted");
    };
};

const createTalentGrid = () => {
    const classTalentsGridContainer = document.getElementById("class-talents");
    const specTalentsGridContainer = document.getElementById("spec-talents");

    const createTalentCells = (talentSet, baseTalentSet, container, category) => {
        talentSet.forEach((talentName, index) => {
            let cell = document.createElement("div");
            cell.classList.add("talent-option");

            if (classTalentsDown.includes(talentName)) {
                const downPseudoElement = createElement("div", "class-talents-option-down", null);
                cell.appendChild(downPseudoElement);
            };              
            if (classTalentsDownLong.includes(talentName)) {
                const downLongPseudoElement = createElement("div", "class-talents-option-down-long", null);
                cell.appendChild(downLongPseudoElement);
            };             
            if (classTalentsLeft.includes(talentName)) {
                const leftPseudoElement = createElement("div", "class-talents-option-left", null);
                cell.appendChild(leftPseudoElement);
            };          
            if (classTalentsRight.includes(talentName)) {
                const rightPseudoElement = createElement("div", "class-talents-option-right", null);
                cell.appendChild(rightPseudoElement);
            };
            
            if (specTalentsDown.includes(talentName)) {
                const downPseudoElement = createElement("div", "spec-talents-option-down", null);
                cell.appendChild(downPseudoElement);
            };              
            if (specTalentsDownLong.includes(talentName)) {
                const downLongPseudoElement = createElement("div", "spec-talents-option-down-long", null);
                cell.appendChild(downLongPseudoElement);
            };             
            if (specTalentsLeft.includes(talentName)) {
                const leftPseudoElement = createElement("div", "spec-talents-option-left", null);
                cell.appendChild(leftPseudoElement);
            };          
            if (specTalentsRight.includes(talentName)) {
                const rightPseudoElement = createElement("div", "spec-talents-option-right", null);
                cell.appendChild(rightPseudoElement);
            };
    
            let formattedTalentName = talentName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
            cell.id = formattedTalentName;
            
            if (talentName === "") {
                cell.style.backgroundColor = "transparent";
            };

            const talentTooltip = createTooltip(null, "talent-tooltip");
    
            // if it's a multiple choice talent then create a split icon
            let splitTalent = talentName.split("/");
            if (splitTalent.length > 1) {
                cell.classList.add("split-talent-option");
    
                let talentNameLeft = splitTalent[0];
                let talentNameRight = splitTalent[1];
    
                let talentDataLeft = findTalentInTalentsData(baseTalentSet, splitTalent[0]);
                let talentDataRight = findTalentInTalentsData(baseTalentSet, splitTalent[1]);

                let talentIconLeft = document.createElement("img");
                let talentIconRight = document.createElement("img");
    
                talentIconLeft.draggable = false;
                let formattedTalentNameLeft = talentNameLeft.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
                talentIconLeft.id = formattedTalentNameLeft + "-icon";
    
                talentIconLeft.classList.add("talent-icon");
                talentIconLeft.classList.add("split-talent-icon-left");
                talentIconLeft.src = talentsToIcons[talentNameLeft];
                talentIconLeft.style.filter = talentDataLeft.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                const talentInnerHTMLLeft = `<span style="color: var(--holy-font)">${talentNameLeft}</span>`;
                addTooltipFunctionality(talentIconLeft, talentTooltip, null, talentInnerHTMLLeft);

                talentIconLeft.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] < talentDataLeft.ranks["max rank"]) {
                        if (talentDataRight.ranks["current rank"] > 0) {
                            decrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        };
                        incrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);

                        handleTalentChange([talentNameRight, talentNameLeft], [talentDataRight, talentDataLeft], true);
                    };              
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();
                    if (e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] > 0) {                 
                        decrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);
                        handleTalentChange(talentNameLeft, talentDataLeft);
                    };
                });  
                
                talentIconRight.draggable = false;
                let formattedTalentNameRight = talentNameRight.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
                talentIconRight.id = formattedTalentNameRight + "-icon";
                talentIconRight.classList.add("talent-icon");
                talentIconRight.classList.add("split-talent-icon-right");
                talentIconRight.src = talentsToIcons[talentNameRight];
                talentIconRight.style.filter = talentDataRight.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                const talentInnerHTMLRight = `<span style="color: var(--holy-font)">${talentNameRight}</span>`;
                addTooltipFunctionality(talentIconRight, talentTooltip, null, talentInnerHTMLRight);

                talentIconRight.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] < talentDataRight.ranks["max rank"]) {
                        if (talentDataLeft.ranks["current rank"] > 0) {
                            decrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);
                        };
                        incrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        
                        handleTalentChange([talentNameRight, talentNameLeft], [talentDataRight, talentDataLeft], true);
                    };                 
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();   
                    if (e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] > 0) {                 
                        decrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        handleTalentChange(talentNameRight, talentDataRight);
                    };
                });

                const divider = createElement("div", "talent-icon-divider", null);
                divider.id = formattedTalentNameLeft + "divider";
    
                cell.appendChild(talentIconLeft);
                cell.appendChild(divider);
                cell.appendChild(talentIconRight);
                
    
            } else if (talentName !== "") {
                let talentIcon = document.createElement("img");
                talentIcon.draggable = false;
                talentIcon.id = formattedTalentName + "-icon";
                talentIcon.classList.add("talent-icon");
    
                let talentData = findTalentInTalentsData(baseTalentSet, talentName);
    
                if (talentData) {
                    talentIcon.src = talentsToIcons[talentName];
                    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                    const talentInnerHTML = `<span style="color: var(--holy-font)">${talentName}</span>`;
                    addTooltipFunctionality(talentIcon, talentTooltip, null, talentInnerHTML);
                    
                    cell.appendChild(talentIcon);

                    if (talentData.ranks["max rank"] > 1) {
                        const rankDisplay = createElement("div", "talent-rank-display", null);
                        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
                        cell.appendChild(rankDisplay);
                    };
    
                    cell.addEventListener("click", (e) => {   
                        if (e.button === 0 && talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
                            incrementTalent(talentName, talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
    
                    cell.addEventListener("contextmenu", (e) => {
                        e.preventDefault();
                        if (talentData.ranks["current rank"] > 0) {
                            decrementTalent(talentName, talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
                };
            };
    
            if (!cell.id) {
                cell.style.pointerEvents = "none";
            };
            container.appendChild(cell);
        });
    };

    createTalentCells(classTalents, baseClassTalents, classTalentsGridContainer, "class");
    createTalentCells(specTalents, baseSpecTalents, specTalentsGridContainer, "spec");

    const createHeroTalentCells = (talentSet, baseTalentSet, container, category) => {
        talentSet.forEach((talentName, index) => {
            let cell = document.createElement("div");
            cell.classList.add("talent-option");
            cell.classList.add("hero-talent-option");

            let formattedTalentName = talentName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
            cell.id = formattedTalentName;
            
            if (talentName === "") {
                cell.style.backgroundColor = "transparent";
            };

            if (lightsmithTalentsDown.includes(talentName)) {
                const downPseudoElement = createElement("div", "hero-talents-option-down", null);
                cell.appendChild(downPseudoElement);
            };                      
            if (lightsmithTalentsLeft.includes(talentName)) {
                const leftPseudoElement = createElement("div", "hero-talents-option-left", null);
                cell.appendChild(leftPseudoElement);
            };          
            if (lightsmithTalentsRight.includes(talentName)) {
                const rightPseudoElement = createElement("div", "hero-talents-option-right", null);
                cell.appendChild(rightPseudoElement);
            };
            
            if (heraldOfTheSunTalentsDown.includes(talentName)) {
                const downPseudoElement = createElement("div", "hero-talents-option-down", null);
                cell.appendChild(downPseudoElement);
            };                         
            if (heraldOfTheSunTalentsLeft.includes(talentName)) {
                const leftPseudoElement = createElement("div", "hero-talents-option-left", null);
                cell.appendChild(leftPseudoElement);
            };          
            if (heraldOfTheSunTalentsRight.includes(talentName)) {
                const rightPseudoElement = createElement("div", "hero-talents-option-right", null);
                cell.appendChild(rightPseudoElement);
            };

            const talentTooltip = createTooltip(null, "talent-tooltip");

            // if it's a multiple choice talent then create a split icon
            let splitTalent = talentName.split("/");
            if (splitTalent.length > 1) {
                cell.classList.add("split-talent-option");
    
                let talentNameLeft = splitTalent[0];
                let talentNameRight = splitTalent[1];
    
                let talentDataLeft = findTalentInTalentsData(baseTalentSet, splitTalent[0]);
                let talentDataRight = findTalentInTalentsData(baseTalentSet, splitTalent[1]);

                let talentIconLeft = document.createElement("img");
                let talentIconRight = document.createElement("img");
    
                talentIconLeft.draggable = false;
                let formattedTalentNameLeft = talentNameLeft.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
                talentIconLeft.id = formattedTalentNameLeft + "-icon";
    
                talentIconLeft.classList.add("talent-icon");
                talentIconLeft.classList.add("hero-talent-icon");
                talentIconLeft.classList.add("split-talent-icon-left");
                talentIconLeft.src = talentsToIcons[talentNameLeft];
                talentIconLeft.style.filter = talentDataLeft.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                const talentInnerHTMLLeft = `<span style="color: var(--holy-font)">${talentNameLeft}</span>`;
                addTooltipFunctionality(talentIconLeft, talentTooltip, null, talentInnerHTMLLeft);

                talentIconLeft.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] < talentDataLeft.ranks["max rank"]) {
                        if (talentDataRight.ranks["current rank"] > 0) {
                            decrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        };
                        incrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);

                        handleTalentChange([talentNameRight, talentNameLeft], [talentDataRight, talentDataLeft], true);
                    };              
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();
                    if (e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] > 0) {                 
                        decrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);
                        handleTalentChange(talentNameLeft, talentDataLeft);
                    };
                });  
                
                talentIconRight.draggable = false;
                let formattedTalentNameRight = talentNameRight.toLowerCase().replaceAll(" ", "-").replaceAll("'", "").replaceAll(":", "");
                talentIconRight.id = formattedTalentNameRight + "-icon";
                talentIconRight.classList.add("talent-icon");
                talentIconRight.classList.add("hero-talent-icon");
                talentIconRight.classList.add("split-talent-icon-right");
                talentIconRight.src = talentsToIcons[talentNameRight];
                talentIconRight.style.filter = talentDataRight.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                const talentInnerHTMLRight = `<span style="color: var(--holy-font)">${talentNameRight}</span>`;
                addTooltipFunctionality(talentIconRight, talentTooltip, null, talentInnerHTMLRight);

                talentIconRight.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] < talentDataRight.ranks["max rank"]) {
                        if (talentDataLeft.ranks["current rank"] > 0) {
                            decrementTalent(talentNameLeft, talentDataLeft, talentIconLeft, category);
                        };
                        incrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        
                        handleTalentChange([talentNameRight, talentNameLeft], [talentDataRight, talentDataLeft], true);
                    };                 
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();   
                    if (e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] > 0) {                 
                        decrementTalent(talentNameRight, talentDataRight, talentIconRight, category);
                        handleTalentChange(talentNameRight, talentDataRight);
                    };
                });

                const divider = createElement("div", "hero-talent-icon-divider", null);
                divider.id = formattedTalentNameLeft + "divider";
    
                cell.appendChild(talentIconLeft);
                cell.appendChild(divider);
                cell.appendChild(talentIconRight);
            } else if (talentName !== "") {
                let talentIcon = document.createElement("img");
                talentIcon.draggable = false;
                talentIcon.id = formattedTalentName + "-icon";
                talentIcon.classList.add("talent-icon");
                talentIcon.classList.add("hero-talent-icon");
    
                let talentData = findTalentInTalentsData(baseTalentSet, talentName);
    
                if (talentData) {
                    talentIcon.src = talentsToIcons[talentName];
                    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                    const talentInnerHTML = `<span style="color: var(--holy-font)">${talentName}</span>`;
                    addTooltipFunctionality(talentIcon, talentTooltip, null, talentInnerHTML);
                    
                    cell.appendChild(talentIcon);

                    if (talentData.ranks["max rank"] > 1) {
                        const rankDisplay = createElement("div", "talent-rank-display", null);
                        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
                        cell.appendChild(rankDisplay);
                    };
    
                    cell.addEventListener("click", (e) => {  
                        if (e.button === 0 && talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
                            incrementTalent(talentName, talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
    
                    cell.addEventListener("contextmenu", (e) => {
                        e.preventDefault();
                        if (talentData.ranks["current rank"] > 0) {
                            decrementTalent(talentName, talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
                };
            };
    
            if (!cell.id) {
                cell.style.pointerEvents = "none";
            };
            container.appendChild(cell);
        });
    };

    const heroTalentsButtonContainer = document.getElementById("hero-talents-button-container");
    if (futurePatchSelected) {
        const heroTalentsModal = document.getElementById("hero-talents-modal");
        heroTalentsModal.style.display = "none";
        const heroTalentsScreenCover = document.getElementById("hero-talents-screen-cover");
        heroTalentsScreenCover.style.display = "none";

        const lightsmithIcon = document.getElementById("lightsmith-icon");
        const heraldOfTheSunIcon = document.getElementById("herald-of-the-sun-icon");
        lightsmithIcon.style.filter = "grayscale(1)";
        heraldOfTheSunIcon.style.filter = "grayscale(1)";

        const lightsmithTalentsGridContainer = document.getElementById("lightsmith-talent-grid");
        const heraldOfTheSunTalentsGridContainer = document.getElementById("herald-of-the-sun-talent-grid");

        heroTalentsButtonContainer.addEventListener("click", () => {
            heroTalentsModal.style.display = heroTalentsModal.style.display === "none" ? "flex" : "none";
            heroTalentsScreenCover.style.display = heroTalentsScreenCover.style.display === "none" ? "flex" : "none";
        });

        window.addEventListener("click", (e) => {
            if (heroTalentsModal.style.display === "flex" && (!heroTalentsModal.contains(e.target) && !heroTalentsButtonContainer.contains(e.target))) {
                heroTalentsModal.style.display = "none";
                heroTalentsScreenCover.style.display = "none";
            };
        });

        createHeroTalentCells(heroTalentsLightsmith, baseLightsmithTalents, lightsmithTalentsGridContainer, "lightsmith");
        createHeroTalentCells(heroTalentsHeraldOfTheSun, baseHeraldOfTheSunTalents, heraldOfTheSunTalentsGridContainer, "herald-of-the-sun");
    } else {
        heroTalentsButtonContainer.style.display = "none";
    };
    
};

export { createTalentGrid, updateTalentsFromImportedData };