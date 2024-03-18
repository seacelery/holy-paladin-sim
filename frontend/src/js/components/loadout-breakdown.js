import { itemsToIconsMap } from "../utils/items-to-icons-map.js";
import { spellToIconsMap } from "../utils/spell-to-icons-map.js";
import { talentsToIcons } from "../utils/talents-to-icons-map.js";
import { createElement } from "./index.js";

const createLoadoutBreakdown = (simulationData, containerCount) => {
    const classTalentsData = simulationData.simulation_details.talents.class_talents;
    const specTalentsData = simulationData.simulation_details.talents.spec_talents;
    const equipmentData = simulationData.simulation_details.equipment;
    const statsData = simulationData.simulation_details.stats;
    const priorityListData = simulationData.simulation_details.priority_list;

    const loadoutBreakdownContainer = document.getElementById(`loadout-breakdown-table-container-${containerCount}`);

    const loadoutContainer = createElement("div", "loadout-container", null);
    loadoutBreakdownContainer.appendChild(loadoutContainer);

    const talentsContainer = createElement("div", "loadout-container-content", "loadout-talents-container");
    const equipmentContainer = createElement("div", "loadout-container-content", "loadout-equipment-container");
    const priorityListContainer = createElement("div", "loadout-container-content", "loadout-priority-list-container");
    loadoutContainer.append(talentsContainer, equipmentContainer, priorityListContainer);

    // talents
    const talentsHeader = createElement("div", "loadout-header", null);
    talentsHeader.textContent = "Talents";
    talentsContainer.appendChild(talentsHeader);

    const combinedTalentsContainer = createElement("div", "loadout-combined-talents-container", null);
    const classTalentsContainer = createElement("div", "loadout-talents-container", "loadout-class-talents-container");
    const specTalentsContainer = createElement("div", "loadout-talents-container", "loadout-spec-talents-container");
    combinedTalentsContainer.append(classTalentsContainer, specTalentsContainer);
    talentsContainer.append(combinedTalentsContainer);

    const classTalentsIconContainer = createElement("img", null, "loadout-class-talent-icon");
    classTalentsIconContainer.src = "https://wow.zamimg.com/images/wow/icons/large/classicon_paladin.jpg";
    classTalentsContainer.appendChild(classTalentsIconContainer);
    const specTalentsIconContainer = createElement("img", null, "loadout-spec-talent-icon");
    specTalentsIconContainer.src = "https://wow.zamimg.com/images/wow/icons/large/spell_holy_holybolt.jpg";
    specTalentsContainer.appendChild(specTalentsIconContainer);

    const talentTooltip = createElement("div", "loadout-talent-tooltip", "loadout-talent-tooltip");
    talentTooltip.style.display = "none";
    talentTooltip.style.position = "absolute";
    document.body.appendChild(talentTooltip);

    const classTalentRows = Object.keys(classTalentsData);
    classTalentRows.sort((a, b) => {
            const numA = parseInt(a.replace("row", ""), 10);
            const numB = parseInt(b.replace("row", ""), 10);
            return numA - numB;
        });
    classTalentRows.forEach(row => {
        const classTalentRow = createElement("div", "loadout-class-talent-row", null);

        for (const talent in classTalentsData[row]) {
            const currentTalentRank = classTalentsData[row][talent]["ranks"]["current rank"];
            const maxTalentRank = classTalentsData[row][talent]["ranks"]["max rank"];

            if (currentTalentRank > 0) {
                const talentIcon = createElement("Img", "loadout-talent-icon", null);
                talentIcon.src = talentsToIcons[talent];
                classTalentRow.appendChild(talentIcon);

                talentIcon.addEventListener("mousemove", (e) => {
                    const xOffset = 15;
                    const yOffset = 15;

                    talentTooltip.style.left = e.pageX + xOffset + "px";
                    talentTooltip.style.top = e.pageY + yOffset + "px";

                    talentTooltip.style.display = "flex";

                    talentTooltip.innerHTML = "";
                    talentTooltip.textContent = `${talent}: ${currentTalentRank} / ${maxTalentRank}`;
                });

                talentIcon.addEventListener("mouseleave", () => {
                    talentTooltip.style.display = "none";
                });
            };
        };
        classTalentsContainer.appendChild(classTalentRow);
    });

    const specTalentRows = Object.keys(specTalentsData);
    specTalentRows.sort((a, b) => {
            const numA = parseInt(a.replace("row", ""), 10);
            const numB = parseInt(b.replace("row", ""), 10);
            return numA - numB;
        });

    specTalentRows.forEach(row => {
        const specTalentRow = createElement("div", "loadout-spec-talent-row", null);

        for (const talent in specTalentsData[row]) {
            const currentTalentRank = specTalentsData[row][talent]["ranks"]["current rank"];
            const maxTalentRank = specTalentsData[row][talent]["ranks"]["max rank"];

            if (currentTalentRank > 0) {
                const talentIcon = createElement("Img", "loadout-talent-icon", null);
                talentIcon.src = talentsToIcons[talent];
                specTalentRow.appendChild(talentIcon);

                talentIcon.addEventListener("mousemove", (e) => {
                    const xOffset = 15;
                    const yOffset = 15;

                    talentTooltip.style.left = e.pageX + xOffset + "px";
                    talentTooltip.style.top = e.pageY + yOffset + "px";

                    talentTooltip.style.display = "flex";

                    talentTooltip.innerHTML = "";
                    talentTooltip.textContent = `${talent}: ${currentTalentRank} / ${maxTalentRank}`;
                });

                talentIcon.addEventListener("mouseleave", () => {
                    talentTooltip.style.display = "none";
                });
            };

            
        };
        specTalentsContainer.appendChild(specTalentRow);
    });

    // stats
    // const statsHeader = createElement("div", "loadout-header", null);
    // statsHeader.textContent = "Stats";
    // equipmentContainer.appendChild(statsHeader);

    const equipmentTooltip = createElement("div", "loadout-equipment-tooltip", "loadout-equipment-tooltip");
    equipmentTooltip.style.display = "none";
    equipmentTooltip.style.position = "absolute";
    document.body.appendChild(equipmentTooltip);

    const equipmentHeader = createElement("div", "loadout-header", "loadout-header-equipment");
    equipmentHeader.textContent = "Equipment";
    equipmentContainer.appendChild(equipmentHeader);

    const equipmentList = createElement("div", "loadout-equipment-list", null);
    const equipmentOrder = ["head", "neck", "shoulder", "back", "chest", "wrist", "hands", "waist", "legs", "feet", "finger_1", "finger_2", "trinket_1", "trinket_2", "main_hand", "off_hand"];
    const equipmentArray = Object.entries(equipmentData);

    let sortedEquipment = equipmentArray.sort((a, b) => {
        const A = equipmentOrder.indexOf(a[0]);
        const B = equipmentOrder.indexOf(b[0]);
        return A - B;
    });

    sortedEquipment = sortedEquipment.reduce((acc, [key, value]) => {
        acc[key] = value;
        return acc;
    }, {});

    for (const item in sortedEquipment) {
        const itemData = equipmentData[item];
        const rarityColour = `var(--rarity-${itemData["quality"].toLowerCase()})`;
        const itemContainer = createElement("div", "loadout-equipment-item-container", null);
        const itemItemLevel = createElement("div", "loadout-equipment-item-item-level", null);
        itemItemLevel.textContent = itemData["item_level"];
        itemItemLevel.style.color = rarityColour;
        const itemIcon = createElement("img", "loadout-equipment-item-icon", null);
        itemIcon.src = itemData["item_icon"];
        itemIcon.style.border = `1px solid ${rarityColour}`;
        const itemName = createElement("div", "loadout-equipment-item-name", null);
        itemName.textContent = itemData["name"];
        itemName.style.color = rarityColour;
        itemContainer.append(itemIcon, itemName, itemItemLevel);
        equipmentList.appendChild(itemContainer);

        itemContainer.addEventListener("mousemove", (e) => {
            const xOffset = 15;
            const yOffset = 15;

            equipmentTooltip.style.left = e.pageX + xOffset + "px";
            equipmentTooltip.style.top = e.pageY + yOffset + "px";

            equipmentTooltip.style.display = "flex";

            equipmentTooltip.innerHTML = "";
            const equipmentTooltipNameContainer = createElement("div", "loadout-equipment-tooltip-name-container", null);
            const equipmentTooltipName = createElement("div", "loadout-equipment-tooltip-name", null);
            equipmentTooltipName.textContent = `${itemData["name"]}`;
            equipmentTooltipName.style.color = rarityColour;
            equipmentTooltipNameContainer.appendChild(equipmentTooltipName);

            const equipmentTooltipItemLevel = createElement("div", "loadout-equipment-tooltip-item-level", null);
            equipmentTooltipItemLevel.textContent = `${itemData["item_level"]}`;
            equipmentTooltipItemLevel.style.color = rarityColour;
            equipmentTooltipNameContainer.appendChild(equipmentTooltipItemLevel);

            equipmentTooltip.appendChild(equipmentTooltipNameContainer);

            if (itemData["stats"]) {
                const statsOrder = ["intellect", "haste", "crit", "mastery", "versatility", "leech"];
                const statsArray = Object.entries(itemData["stats"]);

                let sortedStats = statsArray.sort((a, b) => {
                    const A = statsOrder.indexOf(a[0]);
                    const B = statsOrder.indexOf(b[0]);
                    return A - B;
                });

                sortedStats = sortedStats.reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {});

                for (const stat in sortedStats) {
                    const equipmentTooltipStat = createElement("div", "loadout-equipment=tooltip-stats", null);
                    equipmentTooltipStat.textContent = `+${itemData["stats"][stat]} ${stat.charAt(0).toUpperCase() + stat.slice(1)}`;
                    if (stat.toLowerCase() === "leech") {
                        equipmentTooltipStat.style.color = "var(--leech-font)";
                    } else if (stat.toLowerCase() === "stamina" || stat.toLowerCase() === "combat_rating_sturdiness") {
                        continue
                    } else {
                        equipmentTooltipStat.style.color = `var(--stat-${stat})`;
                    };
                    equipmentTooltip.appendChild(equipmentTooltipStat);
                };
            };

            if (itemData["enchantments"] && itemData["enchantments"].length > 0) {
                const equipmentTooltipEnchant = createElement("div", "loadout-equipment-tooltip-enchant", null);
                equipmentTooltipEnchant.textContent = itemData["enchantments"][0].split(" |")[0];
                equipmentTooltipEnchant.style.color = "var(--rarity-uncommon)";
                equipmentTooltip.appendChild(equipmentTooltipEnchant);
            };

            if (itemData["gems"]) {
                const equipmentTooltipGems = createElement("div", "loadout-equipment-tooltip-gems", null);
                for (const gem in itemData["gems"]) {
                    const equipmentTooltipGem = createElement("img", "loadout-equipment-tooltip-gem", null);
                    equipmentTooltipGem.src = itemsToIconsMap[itemData["gems"][gem]];
                    equipmentTooltipGems.appendChild(equipmentTooltipGem);
                };
                equipmentTooltip.appendChild(equipmentTooltipGems);
            };

            if (itemData["effects"][0]) {
                const equipmentTooltipEffect = createElement("div", "loadout-equipment-tooltip-effect", null);
                equipmentTooltipEffect.textContent = itemData["effects"][0]["description"];
                equipmentTooltipEffect.style.color = "var(--mana)";
                equipmentTooltip.appendChild(equipmentTooltipEffect);
            };
        });

        itemContainer.addEventListener("mouseleave", () => {
            equipmentTooltip.style.display = "none";
        });
    };
    equipmentContainer.appendChild(equipmentList);

    // priority list
    const priorityListHeader = createElement("div", "loadout-header", null);
    priorityListHeader.textContent = "Priority List";
    priorityListContainer.appendChild(priorityListHeader);

    const priorityList = createElement("div", "loadout-priority-list", null);
    for (const priority in priorityListData) {
        const priorityData = priorityListData[priority];
        const abilityName = priorityData.split(" | ")[0];
        let conditionText = "";
        for (let i = 1; i < priorityData.split(" | ").length; i++) {
            conditionText += ` ${priorityData.split(" | ")[i]}`;
        };
        conditionText.replace("or", "OR").replace("and", "AND");
        const priorityContainer = createElement("div", "loadout-priority-container", null);
        const priorityIcon = createElement("img", "loadout-priority-icon", null);
        priorityIcon.src = spellToIconsMap[abilityName];
        const priorityAbility = createElement("div", "loadout-priority-ability", null);
        const priorityCondition = createElement("div", "loadout-priority-condition", null);
        priorityAbility.textContent = abilityName;
        if (abilityName.length >= 20) {
            priorityAbility.style.marginTop = "-1px";
        };
        priorityCondition.textContent = conditionText;
        priorityContainer.append(priorityIcon, priorityAbility, priorityCondition);
        priorityList.appendChild(priorityContainer);
    }
    priorityListContainer.appendChild(priorityList);
};

export { createLoadoutBreakdown };