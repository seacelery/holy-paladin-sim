import { baseClassTalents, baseSpecTalents, classTalentsDown, classTalentsDownLong, classTalentsLeft, classTalentsRight, specTalentsDown, specTalentsDownLong, specTalentsLeft, specTalentsRight } from "../utils/base-talents.js";
import { createElement, updateCharacter, updateStats } from "./index.js";
import { talentsToIcons } from "../utils/talents-to-icons-map.js";

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

const updateTalentsFromImportedData = (importedTalents) => {
    let importedClassTalents = importedTalents.class_talents;
    let importedSpecTalents = importedTalents.spec_talents;

    const updateTalents = (imported, baseTalents, category) => {
        let classTalentsCount = 0;
        let specTalentsCount = 0;

        for (const row in imported) {
            for (const talentName in imported[row]) {
                const talentData = imported[row][talentName];
                const formattedTalentName = talentName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
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

                    if (category === "class") {
                        classTalentsCount += talentData.ranks["current rank"];
                    } else if (category === "spec") {
                        specTalentsCount += talentData.ranks["current rank"];
                    };

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
                };
            };
        };
        
        if (category === "class") {
            const freeTalentsCount = 3;
            const classTalents = document.getElementById("class-talents");
            classTalents.setAttribute("data-class-talents-count", classTalentsCount - freeTalentsCount);
        } else if (category === "spec") {
            const freeTalentsCount = 1;
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
    };
}

const handleTalentChange = (talentName, talentData) => {
    const talentValue = talentData.ranks["current rank"];

    let talentUpdate = {};

    const isClassTalent = classTalents.some(t => t.includes(talentName));
    const isSpecTalent = specTalents.some(t => t.includes(talentName));

    if (isClassTalent) {
        console.log("Updating class talent");
        talentUpdate = {
            "class_talents": {
                [talentName]: talentValue
            }
        };
    } else if (isSpecTalent) {
        console.log("Updating spec talent");
        talentUpdate = {
            "spec_talents": {
                [talentName]: talentValue
            }
        };
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

const incrementTalent = (talentData, talentIcon, category) => {
    if (talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
        talentData.ranks["current rank"] += 1;
    };
    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

    if (talentData.ranks["max rank"] > 1) {
        const rankDisplay = talentIcon.parentElement.querySelector(".talent-rank-display");
        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
    };

    updateTalentCounts(category, 1);

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
};

const decrementTalent = (talentData, talentIcon, category) => {
    if (talentData.ranks["current rank"] > 0) {
        talentData.ranks["current rank"] -= 1;
    };
    talentIcon.style.filter = talentData.ranks["current rank"] === 0 ? "saturate(0)" : "saturate(1)";

    if (talentData.ranks["max rank"] > 1) {
        const rankDisplay = talentIcon.parentElement.querySelector(".talent-rank-display");
        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
    };

    updateTalentCounts(category, -1);

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
    
            let formattedTalentName = talentName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
            cell.id = formattedTalentName;
            
            if (talentName === "") {
                cell.style.backgroundColor = "transparent";
            };
    
            // if it's a multiple choice talent then create a split icon
            let splitTalent = talentName.split("/");
            if (splitTalent.length > 1) {
                cell.classList.add("split-talent-option");
    
                let talentNameLeft = splitTalent[0];
                let talentNameRight = splitTalent[1];
    
                let talentDataLeft = findTalentInTalentsData(baseTalentSet, splitTalent[0]);
                let talentDataRight = findTalentInTalentsData(baseTalentSet, splitTalent[1]);
    
                let talentIconLeft = document.createElement("img");
                let formattedTalentNameLeft = talentNameLeft.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                talentIconLeft.id = formattedTalentNameLeft + "-icon";
    
                talentIconLeft.classList.add("talent-icon");
                talentIconLeft.classList.add("split-talent-icon-left");
                talentIconLeft.src = talentsToIcons[talentNameLeft];
                talentIconLeft.style.filter = talentDataLeft.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                talentIconLeft.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] < talentDataLeft.ranks["max rank"]) {
                        incrementTalent(talentDataLeft, talentIconLeft, category);
                        handleTalentChange(talentNameLeft, talentDataLeft);
                    };
                    
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();
                    if (e.target.id === formattedTalentNameLeft + "-icon" && talentDataLeft.ranks["current rank"] > 0) {                 
                        decrementTalent(talentDataLeft, talentIconLeft, category);
                        handleTalentChange(talentNameLeft, talentDataLeft);
                    };
                });
    
                let talentIconRight = document.createElement("img");
                let formattedTalentNameRight = talentNameRight.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                talentIconRight.id = formattedTalentNameRight + "-icon";
                talentIconRight.classList.add("talent-icon");
                talentIconRight.classList.add("split-talent-icon-right");
                talentIconRight.src = talentsToIcons[talentNameRight];
                talentIconRight.style.filter = talentDataRight.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";

                talentIconRight.addEventListener("click", (e) => {
                    if (e.button === 0 && e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] < talentDataRight.ranks["max rank"]) {
                        incrementTalent(talentDataRight, talentIconRight, category);
                        handleTalentChange(talentNameRight, talentDataRight);
                    };                 
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();   
                    if (e.target.id === formattedTalentNameRight + "-icon" && talentDataRight.ranks["current rank"] > 0) {                 
                        decrementTalent(talentDataRight, talentIconRight, category);
                        handleTalentChange(talentNameRight, talentDataRight);
                    };
                });
    
                cell.appendChild(talentIconLeft);
                cell.appendChild(talentIconRight);
    
            } else if (talentName !== "") {
                let talentIcon = document.createElement("img");
                talentIcon.id = formattedTalentName + "-icon";
                talentIcon.classList.add("talent-icon");
    
                let talentData = findTalentInTalentsData(baseTalentSet, talentName);
    
                if (talentData) {
                    talentIcon.src = talentsToIcons[talentName];
                    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";
                    
                    cell.appendChild(talentIcon);

                    if (talentData.ranks["max rank"] > 1) {
                        const rankDisplay = createElement("div", "talent-rank-display", null);
                        rankDisplay.textContent = `${talentData.ranks["current rank"]} / ${talentData.ranks["max rank"]}`;
                        cell.appendChild(rankDisplay);
                    };
    
                    cell.addEventListener("click", (e) => {   
                        if (e.button === 0 && talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
                            incrementTalent(talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
    
                    cell.addEventListener("contextmenu", (e) => {
                        e.preventDefault();
                        if (talentData.ranks["current rank"] > 0) {
                            decrementTalent(talentData, talentIcon, category);
                            handleTalentChange(talentName, talentData);
                        };
                    });
                };
            };
    
            container.appendChild(cell);
        });
    };

    createTalentCells(classTalents, baseClassTalents, classTalentsGridContainer, "class");
    createTalentCells(specTalents, baseSpecTalents, specTalentsGridContainer, "spec");

};

export { createTalentGrid, updateTalentsFromImportedData };