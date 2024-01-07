import { baseClassTalents, baseSpecTalents } from "../utils/BaseTalents.js";
import { updateCharacter } from "./script.js";
import { talentsToIcons } from "../utils/talentsToIconsMap.js";

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
    console.log("Imported talents:")
    console.log(importedTalents)

    let importedClassTalents = importedTalents.class_talents;
    let importedSpecTalents = importedTalents.spec_talents;

    const updateTalents = (imported, baseTalents) => {
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
                };
            };
        };
    };

    updateTalents(importedClassTalents, baseClassTalents);
    updateTalents(importedSpecTalents, baseSpecTalents);    
};

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

const incrementTalent = (talentData, talentIcon) => {
    if (talentData.ranks["current rank"] < talentData.ranks["max rank"]) {
        talentData.ranks["current rank"] += 1;
    };
    talentIcon.style.filter = talentData.ranks["current rank"] > 0 ? "saturate(1)" : "saturate(0)";
};

const decrementTalent = (talentData, talentIcon) => {
    if (talentData.ranks["current rank"] > 0) {
        talentData.ranks["current rank"] -= 1;
    };
    talentIcon.style.filter = talentData.ranks["current rank"] === 0 ? "saturate(0)" : "saturate(1)";
};

const createTalentGrid = () => {
    const classTalentsGridContainer = document.getElementById("class-talents");
    const specTalentsGridContainer = document.getElementById("spec-talents");

    const createTalentCells = (talentSet, baseTalentSet, container) => {
        talentSet.forEach((talentName, index) => {
            let cell = document.createElement("div");
            cell.classList.add("talent-option");
    
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
                    console.log(e.target.id)
                    if (e.button === 0 && e.target.id === formattedTalentNameLeft + "-icon") {
                        incrementTalent(talentDataLeft, talentIconLeft);
                    };
    
                    handleTalentChange(talentNameLeft, talentDataLeft);
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();
                    if (e.target.id === formattedTalentNameLeft + "-icon") {                 
                        decrementTalent(talentDataLeft, talentIconLeft);
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
                    if (e.button === 0 && e.target.id === formattedTalentNameRight + "-icon") {
                        incrementTalent(talentDataRight, talentIconRight);
                    };
                    handleTalentChange(talentNameRight, talentDataRight);
                });
    
                cell.addEventListener("contextmenu", (e) => {
                    e.preventDefault();   
                    if (e.target.id === formattedTalentNameRight + "-icon") {                 
                        decrementTalent(talentDataRight, talentIconRight);
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
    
                    cell.addEventListener("click", (e) => {   
                        if (e.button === 0) {
                            incrementTalent(talentData, talentIcon);
                        };
                        handleTalentChange(talentName, talentData);
                    });
    
                    cell.addEventListener("contextmenu", (e) => {
                        e.preventDefault();
                        decrementTalent(talentData, talentIcon);
                        handleTalentChange(talentName, talentData);
                    });
                };
            };
    
            container.appendChild(cell);
        });
    };

    createTalentCells(classTalents, baseClassTalents, classTalentsGridContainer);
    createTalentCells(specTalents, baseSpecTalents, specTalentsGridContainer);

    // new LeaderLine(
    //     document.getElementById('lay-on-hands-icon'),
    //     document.getElementById('improved-cleanse-icon'),
    //     {
    //         color: 'aqua',
    //         size: 2,
    //         path: 'straight',
    //         endPlug: 'arrow1',
    //         endPlugSize: 1,
    //         startSocket: 'bottom left',
    //         endSocket: 'top right', 
    //     }
    // );

};

export { createTalentGrid, updateTalentsFromImportedData };