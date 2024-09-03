import { createElement, updateStats } from "./index.js";
import { itemsToIconsMap, groupedGems, ptrGroupedGems } from "../utils/items-to-icons-map.js";
import { generateItemStats } from "../utils/item-level-calculations/generate-item-stats.js";
import { generateItemEffects } from "../utils/item-level-calculations/generate-item-effect.js";
import { itemSlotsMap, blizzardItemSlotsMap, itemSlotToDefaultIcon } from "../utils/item-slots-map.js";
import { itemSlotBonuses, ptrItemSlotBonuses, embellishmentsData, ptrEmbellishmentsData, embellishmentItems, ptrEmbellishmentItems, craftedItems, ptrCraftedItems } from "../utils/item-level-calculations/item-slot-bonuses.js";
import { futurePatchSelected } from "./config/version-config.js";
import itemData from "../utils/data/item-data.js";

const updateBlurListener = (element, listener) => {
    const blurHandler = () => {
        listener();
    };

    if (element.hasBlurListener) {
        element.removeEventListener("blur", element._blurHandler);
    };

    element._blurHandler = blurHandler;
    element.addEventListener("blur", element._blurHandler);
    element.addEventListener("keydown", (e) => {
        if (e.key !== "Enter") return;
        
        element.blur();                             
    });
    element.hasBlurListener = true;
};

const updateEquipmentFromImportedData = (data) => {
    // left half
    let equipmentData = data["equipment"];

    let tierS1Counter = 0;
    let tierS2Counter = 0;
    let tierS3Counter = 0;
    let tierDragonflightS2Counter = 0;
    let embellishmentCounter = 0;
    let idolCounter = 0;
    let combinedItemLevel = 0;

    for (const itemSlot in equipmentData) {
        const itemSlotData = equipmentData[itemSlot];

        const itemIcon = itemSlotData["item_icon"];
        const itemLevel = itemSlotData["item_level"];
        combinedItemLevel += Number(itemLevel);
        const itemName = itemSlotData["name"];
        const itemEnchants = itemSlotData["enchantments"];
        const itemGems = itemSlotData["gems"];
        const itemStats = itemSlotData["stats"];
        const itemEffects = itemSlotData["effects"];
        const itemCategory = itemSlotData["limit"];
        const itemQuality = itemSlotData["quality"];
        const rarityColour = `var(--rarity-${itemQuality.toLowerCase()})`;

        const itemSlotContainer = document.getElementById(`item-slot-${itemSlot}`);
        itemSlotContainer.setAttribute("data-item-data", JSON.stringify(itemSlotData));

        const iconDisplay = itemSlotContainer.querySelector(`.item-slot-icon`);
        iconDisplay.src = itemIcon;
        iconDisplay.style.border = `1px solid ${rarityColour}`;

        const itemLevelDisplay = itemSlotContainer.querySelector(`.item-slot-item-level`);
        itemLevelDisplay.textContent = itemLevel;
        itemLevelDisplay.style.display = "flex";
        itemLevelDisplay.style.border = `1px solid ${rarityColour}`;
        itemLevelDisplay.style.borderTop = "none";
        itemLevelDisplay.style.color = rarityColour;

        const itemSlotInfo = itemSlotContainer.querySelector(`.item-slot-info`);
        itemSlotInfo.innerHTML = "";

        const itemSlotInfoContainer = createElement("div", "item-slot-info-container", null);
        itemSlotInfo.appendChild(itemSlotInfoContainer);

        if (itemName) {
            const itemNameDisplay = createElement("div", "item-slot-name", null);
            itemNameDisplay.textContent = itemName;
            itemNameDisplay.style.color = rarityColour;
            itemSlotInfoContainer.appendChild(itemNameDisplay);
        };

        if (itemEnchants) {
            for (const enchant in itemEnchants) {
                let enchantText = itemEnchants[enchant];
                let formattedEnchantText = enchantText.split(":");

                if (formattedEnchantText.length > 1) {
                    if (formattedEnchantText[2] && formattedEnchantText[2].includes("Incandescent Essence")) {
                        formattedEnchantText = "Incandescent Essence";
                    } else {
                        const parts = formattedEnchantText[1].split("|");
                        formattedEnchantText = parts[0];
                    };
                };

                const excludedEnchants = [
                    "Flexweave Underlay",
                    "Personal Space Amplifier",
                    "Hissing Rune",
                    "Howling Rune",
                    "Chirping Rune",
                    "Buzzing Rune"
                ];

                if (excludedEnchants.includes(formattedEnchantText[0])) {
                    continue
                };
                
                const itemEnchantDisplay = createElement("div", "item-slot-enchants", null);
                itemEnchantDisplay.textContent = formattedEnchantText;
                itemSlotInfoContainer.appendChild(itemEnchantDisplay);
            };
        };

        const gemsContainer = createElement("div", "item-slot-gems-container", null);
        if (itemGems) {
            for (const gem in itemGems) {
                const gemName = itemGems[gem];
                const gemContainer = createElement("div", "item-slot-gem-container", null);
                const gemIcon = createElement("img", "item-slot-gem-icon", null);
                gemIcon.src = itemsToIconsMap[gemName];
                gemContainer.appendChild(gemIcon);

                gemsContainer.appendChild(gemContainer);
            };    
        };
        itemSlotInfoContainer.appendChild(gemsContainer);

        if (itemStats) {
            for (let stat in itemStats) {
                if (stat === "leech" && itemStats[stat] > 0) {
                    const leechValue = itemStats[stat];
                    const leechContainer = createElement("div", "item-slot-leech-container", null);
                    leechContainer.textContent = "+" + leechValue + " Leech";
                    gemsContainer.appendChild(leechContainer);
                };
            };
        };

        if (itemCategory && itemEffects.length > 0) {
            const itemCategoryDisplay = createElement("div", "item-slot-category", null);
            const itemCategoryText = itemCategory.replace("Unique-Equipped: ", "")
                                                 .replace("Embellished", "Embellishment")
                                                 .replace(/\s\(\d+\)/g, "");

            if (itemEffects && itemCategory.includes("Embellished")) {
                embellishmentCounter += 1;
                itemCategoryDisplay.textContent = `${itemCategoryText}: ${itemEffects[0]["name"]}`;
            } else {
                itemCategoryDisplay.textContent = itemCategoryText;
            };    
            
            itemSlotInfoContainer.appendChild(itemCategoryDisplay);            
        };

        const tierSetNames = ["Entombed Seraph", "Heartfire Sentinel"];
        const bonusesDisplay = createElement("div", "item-slot-bonuses");
        if (itemName.includes(tierSetNames[0])) {
            bonusesDisplay.textContent = "Tier Season 1";
            tierS1Counter += 1;
        // } else if (itemName.includes(tierSetNames[1])) {
        //     bonusesDisplay.textContent = "Tier Season 2";
        //     tierS2Counter += 1;
        // } else if (itemName.includes(tierSetNames[2])) {
        //     bonusesDisplay.textContent = "Tier Season 3";
        //     tierS3Counter += 1;
        } else if (itemName.includes(tierSetNames[1])) {
            bonusesDisplay.textContent = "Dragonflight Tier Season 2";
            tierDragonflightS2Counter += 1;
        };
        itemSlotInfoContainer.appendChild(bonusesDisplay);

        if (window.getComputedStyle(itemSlotInfoContainer).height.replace("px", "") > 90) {
            itemSlotInfoContainer.style.borderRight = "1px solid var(--border-colour-3)";
        };
    };

    combinedItemLevel = (combinedItemLevel / 16).toFixed(1);
    const combinedItemLevelValue = document.getElementById("equipped-items-item-level-value");
    combinedItemLevelValue.textContent = combinedItemLevel;
    const combinedItemLevelText = document.getElementById("equipped-items-item-level-text");
    combinedItemLevelText.style.color = "var(--paladin-font)";
    let combinedItemLevelColour;

    switch(true) {
        case combinedItemLevel >= 350:
            combinedItemLevelColour = "var(--rarity-epic)";
            break;
        case combinedItemLevel >= 250:
            combinedItemLevelColour = "var(--rarity-rare)";
            break;
        case combinedItemLevel >= 150:
            combinedItemLevelColour = "var(--rarity-uncommon)";
            break;
        case combinedItemLevel >= 50:
            combinedItemLevelColour = "var(--rarity-common)";
            break;
        default:
            combinedItemLevelColour = "var(--rarity-poor)";
    };
    combinedItemLevelValue.style.color = combinedItemLevelColour;


    const equippedItemsInfo = document.getElementById("equipped-items-info");
    equippedItemsInfo.innerHTML = "";
    const tierSetCounts = [tierS1Counter, tierS2Counter, tierS3Counter];
    for (let i = 0; i <= tierSetCounts.length; i++) {
        if (tierSetCounts[i]) {
            const tierContainer = createElement("div", "item-slot-tier", null);
            let tierColour = tierSetCounts[i] >= 4 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
            tierContainer.innerHTML = `<span style="color: var(--paladin-font)">Tier Season ${i + 1}</span> <span style="color: ${tierColour}">${tierSetCounts[i]}/5</span>`;
            equippedItemsInfo.appendChild(tierContainer);
        };
    };
    if (tierDragonflightS2Counter) {
        const tierContainer = createElement("div", "item-slot-tier", null);
        let tierColour = tierDragonflightS2Counter >= 2 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
        tierContainer.innerHTML = `<span style="color: var(--paladin-font)">DF Tier Season 2</span> <span style="color: ${tierColour}">${tierDragonflightS2Counter}/2</span>`;
        equippedItemsInfo.appendChild(tierContainer);
    };

    const embellishmentsContainer = createElement("div", "item-slot-embellishments", null);
    let embellishmentColour = embellishmentCounter === 2 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
    embellishmentsContainer.innerHTML = `<span style="color: var(--paladin-font)">Embellishments</span> <span style="color: ${embellishmentColour}">${embellishmentCounter}/2</span>`;
    equippedItemsInfo.appendChild(embellishmentsContainer);

    // right half
    const statsData = data["stats"];
    for (const stat in statsData) {
        if (["haste", "crit", "versatility", "mastery", "leech"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            const statValue = statContainer.querySelector(".equipped-items-stat-value");

            const statPercent = `${stat}_percent`;
            statValue.textContent = `${statsData[stat]} / ${statsData[statPercent].toFixed(2)}%`;
        } else if (["intellect", "health", "mana"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            const statValue = statContainer.querySelector(".equipped-items-stat-value");
            statValue.textContent = statsData[stat];
        };
    };

    const itemLevelContainer = document.getElementById("equipped-items-item-level");
    const itemLevelInfo = document.getElementById("equipped-items-info");
    itemLevelContainer.style.display = "block";
    itemLevelInfo.style.display = "block";

    const unsupportedTrinketTooltip = createElement("div", "trinket-unsupported-tooltip", "trinket-unsupported-tooltip");
    unsupportedTrinketTooltip.style.display = "none";
    unsupportedTrinketTooltip.style.position = "absolute";
    document.body.appendChild(unsupportedTrinketTooltip);
};

const generateFullItemData = () => {
    let fullItemData = {"equipment": {}};
    const itemSlots = document.querySelectorAll(".item-slot");
    itemSlots.forEach(itemSlot => {
        const slotData = JSON.parse(itemSlot.getAttribute("data-item-data"));
        const slotType = itemSlot.getAttribute("data-item-slot");
        fullItemData["equipment"][itemSlotsMap[slotType.toLowerCase()]] = slotData;
    });

    updateEquipmentFromImportedData(fullItemData);
    return fullItemData;
};

const clearNewItem = () => {
    const newItemIcon = document.getElementById("new-equipped-item-icon");
    const newItemLevel = document.getElementById("new-item-item-level");
    const itemSearch = document.getElementById("new-equipped-item-search");
    const newItemInfoContainer = document.getElementById("new-equipped-item-info-container");
    const newItemInfo = document.getElementById("new-equipped-item-info");
    const replaceItemButton = document.getElementById("replace-item-button");

    newItemInfo.innerHTML = "";

    newItemIcon.style.opacity = 0.2;
    newItemIcon.style.filter = "grayscale(1)";

    newItemLevel.textContent = "";
    newItemLevel.style.color = "var(--light-font-colour)";
    newItemLevel.style.borderTop = `1px solid var(--border-colour-3)`;

    itemSearch.style.color = "var(--light-font-colour)";
    itemSearch.style.border = `1px solid var(--border-colour-3)`;
    itemSearch.style.borderBottom = "none";
    itemSearch.value = "";

    newItemInfoContainer.style.border = `1px solid var(--border-colour-3)`;

    newItemInfo.style.borderLeft = `1px solid var(--border-colour-3)`;
    // replaceItemButton.style.borderTop = `1px solid var(--border-colour-3)`;
    // replaceItemButton.style.borderRight = `1px solid var(--border-colour-3)`;

    document.getElementById("new-equipped-item-container").style.backgroundColor = `var(--panel-colour-table-3)`;
    document.getElementById("new-equipped-item-search").style.backgroundColor = "var(--panel-colour-2)";
};

const initialiseEquipment = () => {
    const gemsToUse = futurePatchSelected ? ptrGroupedGems : groupedGems;
    const itemSlotBonusesToUse = futurePatchSelected ? ptrItemSlotBonuses : itemSlotBonuses;
    const craftedItemsToUse = futurePatchSelected ? ptrCraftedItems : craftedItems;
    const embellishmentsToUse = futurePatchSelected ? ptrEmbellishmentsData : embellishmentsData;
    const embellishmentItemsToUse = futurePatchSelected ? ptrEmbellishmentItems : embellishmentItems;

    const updateEquippedItemDisplay = (itemSlot, itemSlots) => {
        const currentEquippedIcon = document.getElementById("current-equipped-item-icon");
        const currentItemLevel = document.getElementById("equipped-item-item-level");
        currentItemLevel.contentEditable = true;
        currentItemLevel.style.outline = "none";
        const currentItemTitle = document.getElementById("current-equipped-item-title");
        const currentItemSlot = itemSlotsMap[itemSlot.getAttribute("data-item-slot").toLowerCase()];
        
        const currentItemInfoContainer = document.getElementById("current-equipped-item-info-container");
        const currentItemInfo = document.getElementById("current-equipped-item-info");

        const itemSlotData = JSON.parse(itemSlot.getAttribute("data-item-data"));

        const updateItemData = (property, newValue, subProperty = null) => {
            if (property === "effects" && newValue.length === 0) {
                itemSlotData["limit"] = "";
            };

            if (newValue[0]?.type === "embellishment") {
                itemSlotData["limit"] = "Unique-Equipped: Embellished (2)";
            };

            if (subProperty) {
                if (newValue === 0) {
                    delete itemSlotData[property][subProperty];
                } else {
                    itemSlotData[property][subProperty] = newValue;
                };
            } else {
                itemSlotData[property] = newValue;
            };

            itemSlot.setAttribute("data-item-data", JSON.stringify(itemSlotData))
            generateFullItemData();
            updateStats();
        };

        const currentItemLevelBlur = () => {
            let fullItemData = generateFullItemData();
            let newItemLevel = currentItemLevel.textContent;
            
            const currentItemSlot = itemSlotsMap[itemSlot.getAttribute("data-item-slot").toLowerCase()];

            if (newItemLevel.length === 0 || newItemLevel.length > 3) {
                newItemLevel = fullItemData.equipment[currentItemSlot].item_level;
            };

            const newStats = generateItemStats(itemSlotData.stats, currentItemSlot, newItemLevel);
            fullItemData.equipment[currentItemSlot].stats = newStats;
            fullItemData.equipment[currentItemSlot].item_level = newItemLevel;

            const newEffects = generateItemEffects(itemSlotData.effects, currentItemSlot, newItemLevel);
            fullItemData.equipment[currentItemSlot].effects = newEffects;

            updateEquipmentFromImportedData(fullItemData);
            updateEquippedItemDisplay(itemSlot, itemSlots);
            updateStats();
        };

        updateBlurListener(currentItemLevel, currentItemLevelBlur);

        const createStatsDisplay = () => {
            const currentItemStats = itemSlotData.stats;
            const secondaryStats = ["haste", "versatility", "mastery", "crit"].filter(stat => currentItemStats.hasOwnProperty(stat))
                                                                              .sort((a, b) => currentItemStats[b] - currentItemStats[a])
                                                                              .map(stat => {
                                                                                return {name: stat, value: currentItemStats[stat]}
                                                                              });                                                             

            const currentItemDetails = [];  
            if (itemSlotData.stats["intellect"]) {
                currentItemDetails.push({
                    id: `current-equipped-item-intellect`,
                    text: `+${itemSlotData.stats["intellect"]} Intellect`,
                    colour: "var(--stat-intellect)"
                });
            };                                                      
            secondaryStats.forEach((stat, index) => {
                currentItemDetails.push({
                    id: `current-equipped-item-stat-${index + 1}`,
                    text: `+${stat.value} ${stat.name.charAt(0).toUpperCase()}${stat.name.slice(1)}`,
                    colour: `var(--stat-${stat.name})`
                });
            });
            
            if (itemSlotData.stats["leech"]) {
                currentItemDetails.push({
                    id: `current-equipped-item-leech`,
                    text: `+${itemSlotData.stats["leech"]} Leech`,
                    colour: "var(--leech-font)"
                });
            };

            const itemDetailsLength = currentItemDetails.length;
            if (itemDetailsLength < 4) {
                for (let i = 0; i < 4 - itemDetailsLength; i++) {
                    currentItemDetails.push({ id: i, text: "", colour: "" });
                };
            };

            currentItemDetails.forEach((item, index) => {
                const field = createElement("div", "current-equipped-item-field-left", null);
                field.id = `current-equipped-item-field-left-${index};`
                field.textContent = item.text;
                field.style.color = item.colour;
                currentItemLeftContainer.appendChild(field);

                // edit secondary stats
                if (["current-equipped-item-stat-1", "current-equipped-item-stat-2"].includes(item.id) && itemSlotData.name in craftedItemsToUse) {
                    const stat = item.text.split(" ")[1].toLowerCase();

                    field.contentEditable = true;
                    field.addEventListener("input", (e) => {
                        if (e.target.innerText === "") {
                            e.target.innerHTML = "&#8203";
                        };
                    });

                    field.addEventListener("blur", () => {
                        const valueMatch = field.textContent.match(/\d+/);
                        let newStatValue = valueMatch ? parseInt(valueMatch[0]) : 0;

                        const statMatch = field.textContent.match(/[a-zA-Z]+/);
                        let statName = statMatch ? statMatch[0].toLowerCase() : null;
                        if (statName !== stat) {
                            updateItemData("stats", 0, stat);
                            updateItemData("stats", newStatValue, statName);
                        } else {
                            updateItemData("stats", newStatValue, stat);
                        };
                        
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });

                    field.addEventListener("keydown", (e) => {
                        if (e.key !== "Enter") return;

                        field.blur();                             
                    });
                };

                // edit leech
                if (itemSlotData.stats["leech"] && item.id === "current-equipped-item-leech") {
                    field.contentEditable = true;
                    field.addEventListener("input", (e) => {
                        if (e.target.innerText === "") {
                            e.target.innerHTML = "&#8203";
                        };
                    });

                    field.addEventListener("blur", () => {
                        const matches = field.textContent.match(/\d+/);
                        let newLeechValue = matches ? parseInt(matches[0]) : 0;

                        updateItemData("stats", newLeechValue, "leech");
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });

                    field.addEventListener("keydown", (e) => {
                        if (e.key !== "Enter") return;

                        field.blur();                             
                    });
                } else if (item.id == 0) {
                    field.contentEditable = true;

                    field.addEventListener("focus", (e) => {
                        if (e.target.innerText === "") {
                            e.target.innerHTML = "&#8203";
                        };
                    });

                    field.addEventListener("blur", () => {
                        const matches = field.textContent.match(/\d+/);
                        let newLeechValue = matches ? parseInt(matches[0]) : 0;

                        if (newLeechValue > 0) {
                            updateItemData("stats", newLeechValue, "leech");
                        };
                        
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });

                    field.addEventListener("keydown", (e) => {
                        if (e.key !== "Enter") return;

                        field.blur();                             
                    });
                };
            });
        };

        const createItemBonusesDisplay = () => {
            const currentItemEnchantSelect = createElement("div", "current-equipped-item-field-right", "current-equipped-item-enchants");
            const defaultEnchantOption = createElement("div", "current-equipped-item-default-enchant-option", null);

            const selectedItemSlot = document.getElementById("equipped-items-edit-choose-slot-dropdown").value;
            const availableEnchants = itemSlotBonusesToUse[selectedItemSlot]["enchants"];

            if (itemSlotData["enchantments"] && itemSlotData["enchantments"].length > 0) {
                if (itemSlotData["enchantments"][0].split("|")[1] && itemSlotData["enchantments"][0].split("|")[1].includes("Incandescent Essence")) {
                    defaultEnchantOption.textContent = "Enchanted: Incandescent Essence";
                } else {
                    defaultEnchantOption.textContent = itemSlotData["enchantments"][0].split("|")[0];
                };

                defaultEnchantOption.style.color = "var(--rarity-uncommon)";
            } else if (availableEnchants.length > 0) {
                defaultEnchantOption.textContent = "No enchant";
                defaultEnchantOption.style.color = "var(--rarity-common)";
            } else {
                defaultEnchantOption.textContent = "No enchants available";
                defaultEnchantOption.style.color = "var(--rarity-poor)";
            };
            currentItemEnchantSelect.appendChild(defaultEnchantOption);

            const enchantOptions = createElement("div", "current-equipped-item-enchant-options", null);
            currentItemEnchantSelect.appendChild(enchantOptions);
            currentItemEnchantSelect.addEventListener("click", () => {
                if (itemSlotData["enchantments"]) {
                    enchantOptions.style.display = enchantOptions.style.display === "flex" ? "none" : "flex";
                };         
            });

            itemSlotBonusesToUse[selectedItemSlot]["enchants"].forEach(enchant => {
                const enchantOption = createElement("div", "current-equipped-item-enchant-option", null);
                enchantOption.textContent = enchant;
                enchantOptions.appendChild(enchantOption);

                enchantOption.addEventListener("click", () => {
                    let updatedEnchantData = null;
                    if (enchantOption.textContent === "No enchant") {
                        defaultEnchantOption.textContent = `${enchantOption.textContent}`;
                        defaultEnchantOption.style.color = "var(--light-font-colour)";
                        updatedEnchantData = [];
                    } else {
                        defaultEnchantOption.textContent = `Enchanted: ${enchantOption.textContent}`;
                        defaultEnchantOption.style.color = "var(--rarity-uncommon)";
                        updatedEnchantData = [`Enchanted: ${enchantOption.textContent}`];
                    };
                    updateItemData("enchantments", updatedEnchantData);
                    updateEquippedItemDisplay(itemSlot, itemSlots);
                });
            });
            currentItemRightContainer.appendChild(currentItemEnchantSelect);

            // gems
            const currentItemGemsField = createElement("div", "current-equipped-item-field-right current-equipped-item-gems-field", null);
            currentItemRightContainer.appendChild(currentItemGemsField);

            const currentItemGemsContainer = createElement("div", "current-equipped-item-gems-container", null);
            currentItemGemsField.appendChild(currentItemGemsContainer);

            const addGemContainer = createElement("div", "current-equipped-item-add-gem-container", null);
            const addGemButton = createElement("div", "current-equipped-item-add-gem-button", null);
            const addGemIcon = createElement("div", "current-equipped-item-add-gem-icon fa-solid fa-plus", null);
            addGemButton.appendChild(addGemIcon);
            addGemContainer.appendChild(addGemButton);

            // gem modal
            const addGemModal = createElement("div", "add-gem-modal", null);
            addGemContainer.appendChild(addGemModal);
            addGemContainer.addEventListener("click", () => {
                addGemModal.style.display = addGemModal.style.display === "block" ? "none" : "block";
            });

            const secondaryStatRow = createElement("div", "gem-modal-row stat-label-row", null);
            const statLabelsContainer = createElement("div", "stat-labels-container", null);
            secondaryStatRow.appendChild(statLabelsContainer);
            const statLabels = ["+Haste", "+Crit", "+Mast", "+Vers", "+Int"];
            statLabels.forEach(label => {
                const container = createElement("div", "row-stat-label", null);
                container.textContent = label;
                statLabelsContainer.appendChild(container);
            })
            addGemModal.appendChild(secondaryStatRow);

            Object.values(gemsToUse).forEach(group => {
                const row = createElement("div", "gem-modal-row", null);

                const rowLabel = createElement("div", "gem-modal-row-label", null);
                rowLabel.textContent = group["label"];
                rowLabel.style.color = `var(--stat-${group["label"].toLowerCase()})`;
                row.appendChild(rowLabel);

                group["gems"].forEach(([gemName, gemIcon, gemStatOne, gemStatTwo]) => {
                    const modalGemContainer = createElement("div", "gem-modal-gem-container", null);
                    const modalGemIcon = createElement("img", "gem-modal-gem-icon", null);
                    modalGemIcon.src = gemIcon;
                    modalGemIcon.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;
                    modalGemContainer.appendChild(modalGemIcon);
                    modalGemContainer.addEventListener("click", () => {
                        let newGemData = [];
                        if (itemSlotData["gems"]) {
                            newGemData = [...itemSlotData["gems"]];
                            newGemData.push(gemName);
                            updateItemData("gems", newGemData);
                        } else {
                            newGemData.push(gemName);
                            updateItemData("gems", newGemData);
                        };
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });

                    const modalGemTooltip = createElement("div", "gem-modal-tooltip", null);
                    modalGemTooltip.style.display = "none";
                    modalGemTooltip.style.position = "absolute";
                    document.body.appendChild(modalGemTooltip);
                    modalGemContainer.addEventListener("mousemove", (e) => {
                        const xOffset = 15;
                        const yOffset = 15;

                        modalGemTooltip.style.left = e.pageX + xOffset + "px";
                        modalGemTooltip.style.top = e.pageY + yOffset + "px";

                        modalGemTooltip.style.display = "block";
                        modalGemTooltip.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;

                        modalGemTooltip.innerHTML = "";
                        const tooltipGemName = createElement("div", "gem-modal-tooltip-gem-name", null);
                        tooltipGemName.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemName}</span>`;
                        
                        const tooltipStats = createElement("div", "gem-modal-tooltip-gem-stats", null);
                        if (gemStatTwo) {
                            tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span> & <span style="color: var(--stat-${gemStatTwo.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatTwo}</span>`;
                        } else {
                            tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span>`;
                        };
                        
                        modalGemTooltip.appendChild(tooltipGemName);
                        modalGemTooltip.appendChild(tooltipStats);
                    });
                    modalGemContainer.addEventListener("mouseleave", () => {
                        modalGemTooltip.style.display = "none";
                    });
                    modalGemContainer.addEventListener("click", () => {
                        modalGemTooltip.style.display = "none";
                    });

                    row.appendChild(modalGemContainer);
                });

                addGemModal.appendChild(row);
            });
            currentItemGemsContainer.appendChild(addGemContainer);

            const gemsData = itemSlotData["gems"];
            if (gemsData) {
                gemsData.forEach(gem => {
                    const currentItemGemContainer = createElement("div", "current-equipped-item-gem-container", null);
                    const currentItemGemIcon = createElement("img", "current-equipped-item-gem-icon", null);
                    currentItemGemIcon.src = itemsToIconsMap[gem];
                    currentItemGemContainer.appendChild(currentItemGemIcon);

                    const gemTooltip = createElement("div", "gem-modal-tooltip", null);
                    gemTooltip.style.display = "none";
                    gemTooltip.style.position = "absolute";
                    document.body.appendChild(gemTooltip);

                    let gemStatOne, gemStatTwo;

                    for (const gemGroupKey in gemsToUse) {
                        const gemGroup = gemsToUse[gemGroupKey];
                        for (const gemName of gemGroup.gems) {
                            const [currentGemName, , ...stats] = gemName;
                            if (currentGemName === gem) {
                                [gemStatOne, gemStatTwo] = stats;
                            };
                        };
                    };

                    currentItemGemContainer.addEventListener("mousemove", (e) => {
                        const xOffset = 15;
                        const yOffset = 15;

                        gemTooltip.style.left = e.pageX + xOffset + "px";
                        gemTooltip.style.top = e.pageY + yOffset + "px";

                        gemTooltip.style.display = "block";
                        gemTooltip.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;

                        gemTooltip.innerHTML = "";
                        const tooltipGemName = createElement("div", "gem-modal-tooltip-gem-name", null);
                        tooltipGemName.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gem}</span>`;
                        
                        const tooltipStats = createElement("div", "gem-modal-tooltip-gem-stats", null);
                        if (gemStatTwo) {
                            tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span> & <span style="color: var(--stat-${gemStatTwo.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatTwo}</span>`;
                        } else {
                            tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span>`;
                        };
                        
                        gemTooltip.appendChild(tooltipGemName);
                        gemTooltip.appendChild(tooltipStats);
                    });
                    currentItemGemContainer.addEventListener("mouseleave", () => {
                        gemTooltip.style.display = "none";
                    });
                    currentItemGemContainer.addEventListener("click", () => {
                        gemTooltip.style.display = "none";
                    });

                    currentItemGemContainer.addEventListener("click", () => {
                        currentItemGemContainer.remove();
                        if (itemSlotData["gems"]) {
                            const indexToRemove = itemSlotData["gems"].findIndex(gemToRemove => gemToRemove === gem);
                            
                            if (indexToRemove !== -1) {
                                itemSlotData["gems"].splice(indexToRemove, 1);
                                updateItemData("gems", itemSlotData["gems"]);
                            };
                        };
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });

                    // currentItemGemIcon.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;

                    currentItemGemsContainer.insertBefore(currentItemGemContainer, addGemContainer);
                });
            };

            // embellishments
            const currentItemEmbellishmentSelect = createElement("div", "current-equipped-item-field-right-double", "current-equipped-item-embellishments");
            const defaultEmbellishmentOption = createElement("div", "current-equipped-item-default-embellishment-option", null);
            if (itemSlotData["effects"].length > 0 && (craftedItemsToUse[itemSlotData.name] || embellishmentItemsToUse[itemSlotData.name])) {
                defaultEmbellishmentOption.textContent = `Embellishment: ${itemSlotData["effects"][0].name}`;
                defaultEmbellishmentOption.style.color = "var(--mana)";
            } else if (craftedItemsToUse[itemSlotData.name] || embellishmentItemsToUse[itemSlotData.name]) {
                defaultEmbellishmentOption.textContent = `No embellishment`;
                defaultEmbellishmentOption.style.color = "var(--light-font-colour)";
            } else {
                defaultEmbellishmentOption.textContent = `No embellishments available`;
                defaultEmbellishmentOption.style.color = "var(--rarity-poor)";
            };
            currentItemEmbellishmentSelect.appendChild(defaultEmbellishmentOption);

            const embellishmentOptions = createElement("div", "current-equipped-item-embellishment-options", null);
            currentItemEmbellishmentSelect.appendChild(embellishmentOptions);
            currentItemEmbellishmentSelect.addEventListener("click", () => {
                if (craftedItemsToUse[itemSlotData.name] || embellishmentItemsToUse[itemSlotData.name]) {
                    embellishmentOptions.style.display = embellishmentOptions.style.display === "flex" ? "none" : "flex";
                };
            });

            if (craftedItemsToUse[itemSlotData.name]) {
                for (const embellishment in itemSlotBonusesToUse[selectedItemSlot]["embellishments"]) {
                    const embellishmentOption = createElement("div", "current-equipped-item-embellishment-option", null);
                    embellishmentOption.textContent = embellishment;
                    embellishmentOptions.appendChild(embellishmentOption);
    
                    embellishmentOption.addEventListener("click", () => {
                        let updatedEmbellishmentData = null;
                        if (embellishmentOption.textContent === "No embellishment") {
                            defaultEmbellishmentOption.textContent = `${embellishmentOption.textContent}`;
                            defaultEmbellishmentOption.style.color = "var(--light-font-colour)";
                            updatedEmbellishmentData = [];
                        } else {
                            defaultEmbellishmentOption.textContent = `Embellishment: ${embellishmentOption.textContent}`;
                            defaultEmbellishmentOption.style.color = "var(--rarity-uncommon)";
                            updatedEmbellishmentData = [{"name": embellishmentsToUse[embellishment].name, "description": embellishmentsToUse[embellishment].description, "id": embellishmentsToUse[embellishment].id, "type": embellishmentsToUse[embellishment].type, "effect_values": embellishmentsToUse[embellishment].effect_values}];
                            
                        };
                        updatedEmbellishmentData = generateItemEffects(updatedEmbellishmentData, itemSlot.getAttribute("data-item-slot"), currentItemLevel.textContent);
                        updateItemData("effects", updatedEmbellishmentData);
                        updateEquippedItemDisplay(itemSlot, itemSlots);
                    });
                };
            };   
            currentItemRightContainer.appendChild(currentItemEmbellishmentSelect);
        };

        const createTrinketBonusesDisplay = () => {
            const currentTrinketEffectField = createElement("div", "current-equipped-item-field-right-trinket", "current-equipped-item-trinket-effects-0");
            const currentTrinketEffect = createElement("div", "current-equipped-item-trinket-effect", null);
            if (itemSlotData["effects"].length > 0) {
                const descriptionText = itemSlotData["effects"][0].description.replaceAll("*", "").replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
                currentTrinketEffect.innerHTML = descriptionText;
                currentTrinketEffect.style.color = "var(--mana)";
            } else {
                currentTrinketEffect.textContent = `No effect`;
                currentTrinketEffect.style.color = "var(--rarity-poor)";
            };
            currentTrinketEffectField.appendChild(currentTrinketEffect);
            currentItemRightContainer.appendChild(currentTrinketEffectField);
        };

        itemSlots.forEach(itemSlot => {
            itemSlot.querySelector(".item-slot-hover").classList.remove("item-slot-selected");
            itemSlot.querySelector(".item-slot-hover").style.backgroundColor = "var(--panel-colour-table-2)";
        })
        itemSlot.querySelector(".item-slot-hover").classList.add("item-slot-selected");
        itemSlot.querySelector(".item-slot-hover").style.backgroundColor = "var(--panel-colour-5)";

        const itemName = itemSlotData.name;
        const itemLevel = itemSlotData.item_level;
        const itemIcon = itemSlotData.item_icon;
        const rarityColour = `var(--rarity-${itemSlotData.quality.toLowerCase()})`;
    
        currentEquippedIcon.src = itemIcon;
        currentEquippedIcon.style.filter = "grayscale(0)";
        currentEquippedIcon.style.opacity = "1";

        if (!itemSlotData.item_id) return;

        currentItemLevel.textContent = itemLevel;
        currentItemLevel.style.color = rarityColour;
        // currentItemLevel.style.borderTop = `1px solid ${rarityColour}`;

        currentItemTitle.style.border = `1px solid ${rarityColour}`;
        currentItemTitle.style.borderBottom = "none";
        currentItemTitle.innerHTML = `<span>Currently equipped: </span><span style="color: ${rarityColour}">${itemName}</span><div id="trinket-unsupported-icon-container">
        <i class="fa-solid fa-triangle-exclamation" id="trinket-unsupported-icon"></i></div><select id="trinket-option-dropdown"></select>`;

        const trinketUnsupported = document.getElementById("trinket-unsupported-icon-container");
        const supportedTrinkets = [
            "Ominous Chromatic Essence", "Rashok's Molten Heart", "Broodkeeper's Promise", "Whispering Incarnate Icon",
            "Screaming Black Dragonscale", "Smoldering Seedling", "Pip's Emerald Friendship Badge", "Neltharion's Call to Chaos",
            "Spoils of Neltharus", "Blossom of Amirdrassil", "Miniature Singing Stone", "Conjured Chillglobe",
            "Idol of the Spell-Weaver", "Idol of the Life-Binder", "Idol of the Earth-Warder", "Idol of the Dreamer",
            "Time-Breaching Talon", "Nymue's Unraveling Spindle", "Mirror of Fractured Tomorrows", "Echoing Tyrstone",
            "Sea Star", "Coagulated Genesaur Blood", "Sustaining Alchemist Stone", "Alactritous Alchemist Stone",
            "Eye of the Broodmother", "Emerald Coach's Whistle", "Unbound Changeling", "Gruesome Syringe",
            "Harvester's Edict", "Scrapsinger's Symphony", "High Speaker's Accretion", "Ovinax's Mercurial Egg",
            "Empowering Crystal of Anub'ikkaj", "Siphoning Phylactery Shard", "Creeping Coagulum", "Treacherous Transmitter",
            "Mereldar's Toll", "Ara-Kara Sacbrood", "Gale of Shadows", "Corrupted Egg Shell", "Spymaster's Web",
            "Algari Alchemist Stone", "Darkmoon Deck: Symbiosis"
        ];
        if ((currentItemSlot === "trinket_1" || currentItemSlot === "trinket_2") && !supportedTrinkets.includes(itemName)) {
            trinketUnsupported.style.display = "block";
        } else {
            trinketUnsupported.style.display = "none";
        };
        const trinketUnsupportedTooltip = document.querySelector(".trinket-unsupported-tooltip");
        trinketUnsupported.addEventListener("mousemove", (e) => {
            const xOffset = 15;
            const yOffset = 15;
        
            trinketUnsupportedTooltip.style.left = e.pageX + xOffset + "px";
            trinketUnsupportedTooltip.style.top = e.pageY + yOffset + "px";
        
            trinketUnsupportedTooltip.style.display = "block";
        
            trinketUnsupportedTooltip.innerHTML = "";
            trinketUnsupportedTooltip.textContent = "This trinket's effect is not supported!";
        });

        trinketUnsupported.addEventListener("mouseleave", () => {
            trinketUnsupportedTooltip.style.display = "none";
        });

        const trinketsWithOptions = {
            "Ominous Chromatic Essence": ["Mastery", "Haste", "Crit", "Versatility"],
            "Unbound Changeling": ["Mastery", "Haste", "Crit", "Combined"],
            "High Speaker's Accretion": [1, 2, 3, 4, 5],
            "Ovinax's Mercurial Egg": ["Low Movement", "Some Movement", "High Movement"]
        };
        const trinketOptionDropdown = document.getElementById("trinket-option-dropdown");
        if (itemName in trinketsWithOptions) {
            trinketOptionDropdown.style.display = "block";
            trinketOptionDropdown.innerHTML = "";
            trinketsWithOptions[itemName].forEach(optionName => {
                const option = createElement("option", "trinket-option-option", null);
                option.textContent = optionName;
                option.classList.add("trinket-option-option");
                option.style.border = `1px solid ${rarityColour}`;
                trinketOptionDropdown.appendChild(option);
            });

            let trinketItemData = JSON.parse(itemSlot.getAttribute("data-item-data"));
            trinketOptionDropdown.value = trinketItemData["effects"][0].trinket_options ?? trinketsWithOptions[itemName][0];
            trinketItemData["effects"][0].trinket_options = trinketOptionDropdown.value;
            itemSlot.setAttribute("data-item-data", JSON.stringify(trinketItemData));

            trinketOptionDropdown.addEventListener("input", () => {
                let trinketItemData = JSON.parse(itemSlot.getAttribute("data-item-data"));
                trinketItemData["effects"][0].trinket_options = trinketOptionDropdown.value;
                itemSlot.setAttribute("data-item-data", JSON.stringify(trinketItemData));
            });
        };
    
        currentItemInfoContainer.style.border = `1px solid ${rarityColour}`;
        
        // currentItemInfo.style.borderLeft = `1px solid ${rarityColour}`;

        const jewelleryItemSlots = ["Necklace", "Ring 1", "Ring 2"];
        const miscItemSlots = ["Trinket 1", "Trinket 2"];
        const selectedItemSlot = itemSlot.getAttribute("data-item-slot");

        currentItemInfo.innerHTML = "";
        
        const currentItemLeftContainer = createElement("div", "current-equipped-item-info-left", null);      
        currentItemInfo.appendChild(currentItemLeftContainer);
        const currentItemRightContainer = createElement("div", "current-equipped-item-info-right", null);
        currentItemInfo.appendChild(currentItemRightContainer);

        if (jewelleryItemSlots.includes(selectedItemSlot)) {
            // left
            createStatsDisplay();

            // right
            createItemBonusesDisplay();

        } else if (miscItemSlots.includes(selectedItemSlot)) {
            // left
            createStatsDisplay();

            // right
            createTrinketBonusesDisplay();
        } else {
            // left
            createStatsDisplay();

            // right
            createItemBonusesDisplay();
        };

        document.getElementById("current-equipped-item-container").style.backgroundColor = `var(--rarity-${itemSlotData.quality.toLowerCase()}-dark)`;
        document.getElementById("current-equipped-item-title").style.backgroundColor = `var(--rarity-${itemSlotData.quality.toLowerCase()}-dark)`;
        const enchantOptions = document.querySelector(".current-equipped-item-enchant-options");
        const embellishmentOptions = document.querySelector(".current-equipped-item-embellishment-options");
        if (enchantOptions) {
            enchantOptions.style.backgroundColor = `var(--rarity-${itemSlotData.quality.toLowerCase()}-dark)`;
        };
        if (embellishmentOptions) {
            embellishmentOptions.style.backgroundColor = `var(--rarity-${itemSlotData.quality.toLowerCase()}-dark)`;
        };

        // currentItemInfo.querySelectorAll(".current-equipped-item-field-left").forEach(item => {
        //     item.style.borderBottom = `1px solid ${rarityColour}`;
        // });
        // currentItemInfo.querySelectorAll(".current-equipped-item-field-right").forEach(item => {
        //     item.style.borderBottom = `1px solid ${rarityColour}`;
        // });
        // currentItemInfo.querySelectorAll(".current-equipped-item-enchant-options").forEach(item => {
        //     item.style.border = `1px solid ${rarityColour}`;
        // });
        // currentItemInfo.querySelectorAll(".current-equipped-item-embellishment-options").forEach(item => {
        //     item.style.border = `1px solid ${rarityColour}`;
        // });     
        // currentItemInfo.querySelector(".current-equipped-item-info-left").style.borderRight = `1px solid ${rarityColour}`;
        // if (currentItemInfo.querySelector(".current-equipped-item-default-enchant-option")) {
        //     currentItemInfo.querySelector(".current-equipped-item-default-enchant-option").style.borderBottom = `1px solid ${rarityColour}`;
        // };
        if (currentItemInfo.querySelector(".current-equipped-item-default-embellishment-option")) {
            // currentItemInfo.querySelector(".current-equipped-item-default-embellishment-option").style.borderBottom = `1px solid ${rarityColour}`;
            currentItemInfo.querySelector(".current-equipped-item-default-embellishment-option").style.borderBottom = `none`;
        };
        if (currentItemInfo.querySelector(".current-equipped-item-field-right-double")) {
            // currentItemInfo.querySelector(".current-equipped-item-default-embellishment-option").style.borderBottom = `1px solid ${rarityColour}`;
            currentItemInfo.querySelector(".current-equipped-item-field-right-double").style.borderBottom = `none`;
        };
        if (document.querySelector(".current-equipped-item-enchant-options")) {
            document.querySelector(".current-equipped-item-enchant-options").style.borderRight = `1px solid ${rarityColour}`;
        };
        if (document.querySelector(".current-equipped-item-enchant-options")) {
            document.querySelector(".current-equipped-item-enchant-options").style.borderBottom = `1px solid ${rarityColour}`;
        };
    };

    // item slot select
    const itemSlotDropdown = document.getElementById("equipped-items-edit-choose-slot-dropdown");

    const itemSlots = document.querySelectorAll(".item-slot");
    itemSlots.forEach(itemSlot => {
        if (itemSlotDropdown.value === itemSlot.getAttribute("data-item-slot")) {
            updateEquippedItemDisplay(itemSlot, itemSlots)
        };

        itemSlot.addEventListener("click", () => {
            const dataItemSlot = itemSlot.getAttribute("data-item-slot");
            itemSlotDropdown.value = dataItemSlot;
            updateEquippedItemDisplay(itemSlot, itemSlots);

            clearNewItem();

            const newItemIcon = document.getElementById("new-equipped-item-icon");
            newItemIcon.src = itemSlotToDefaultIcon[itemSlot.getAttribute("data-item-slot")];
            newItemIcon.style.opacity = "1";
        });
    });

    itemSlotDropdown.addEventListener("change", (e) => {
        const slotName = e.target.value.toLowerCase();
        const itemSlot = document.getElementById(`item-slot-${itemSlotsMap[slotName]}`);
        updateEquippedItemDisplay(itemSlot, itemSlots);
        clearNewItem();
    });

    // item search
    let currentItemSuggestion = "";
    let finalNewItemData = {};

    const generateSearchResults = () => {
        const updateNewItemDisplay = (item) => {
            finalNewItemData = item;

            const newItemIcon = document.getElementById("new-equipped-item-icon");
            const newItemLevel = document.getElementById("new-item-item-level");
            const itemSearch = document.getElementById("new-equipped-item-search");
            const newItemInfoContainer = document.getElementById("new-equipped-item-info-container");
            const newItemInfo = document.getElementById("new-equipped-item-info");

            const rarityColour = `var(--rarity-${item.quality.toLowerCase()})`;
            newItemInfoContainer.style.border = `1px solid ${rarityColour}`;
            newItemIcon.src = item.icon;
            newItemIcon.style.opacity = 1;
            newItemIcon.style.filter = "grayscale(0)";

            document.getElementById("new-equipped-item-container").style.backgroundColor = `var(--rarity-${item.quality.toLowerCase()}-dark)`;
            document.getElementById("new-equipped-item-search").style.backgroundColor = `var(--rarity-${item.quality.toLowerCase()}-dark)`;

            newItemLevel.textContent = item.base_item_level;
            newItemLevel.style.color = rarityColour;
            // newItemLevel.style.borderTop = `1px solid ${rarityColour}`;
            newItemLevel.contentEditable = true;
            newItemLevel.style.outline = "none";

            const newItemLevelBlur = () => {
                let newItemLevelText = newItemLevel.textContent;
                const selectedItemSlot = document.getElementById("equipped-items-edit-choose-slot-dropdown").value;

                if (newItemLevelText.length === 0 || newItemLevelText.length > 3) {
                    newItemLevelText = item.base_item_level;
                };

                const newStats = generateItemStats(item.stats, itemSlotsMap[selectedItemSlot.toLowerCase()], newItemLevelText);
                item.stats = newStats;
                item.base_item_level = newItemLevelText;

                const newEffects = generateItemEffects(item.effects, itemSlotsMap[selectedItemSlot.toLowerCase()], newItemLevelText);
                item.effects = newEffects;

                updateNewItemDisplay(item);
            };
    
            updateBlurListener(newItemLevel, newItemLevelBlur);

            itemSearch.style.color = rarityColour;
            itemSearch.style.border = `1px solid ${rarityColour}`;
            itemSearch.style.borderBottom = "none";

            newItemInfoContainer.style.border = `1px solid ${rarityColour}`;
        
            // newItemInfo.style.borderLeft = `1px solid ${rarityColour}`;
            // replaceItemButton.style.borderTop = `1px solid `;
            // replaceItemButton.style.borderRight = `1px solid ${rarityColour}`;

            newItemInfo.innerHTML = "";
            const newItemLeftContainer = createElement("div", "new-equipped-item-info-left", null);      
            newItemInfo.appendChild(newItemLeftContainer);
            const newItemRightContainer = createElement("div", "new-equipped-item-info-right", null);
            newItemInfo.appendChild(newItemRightContainer);

            // stats
            const createNewItemStatsDisplay = () => {
                const newItemStats = item.stats;
                
                const secondaryStats = ["Haste", "Versatility", "Mastery", "Critical Strike"].filter(stat => newItemStats.hasOwnProperty(stat))
                                                                                .sort((a, b) => newItemStats[b] - newItemStats[a])
                                                                                .map(stat => {
                                                                                    return {name: stat, value: newItemStats[stat]}
                                                                                });                                                             

                const newItemDetails = [];  
                if (item.stats["Intellect"] || item.stats["intellect"]) {
                    newItemDetails.push({
                        id: `new-equipped-item-intellect`,
                        text: `+${item.stats["Intellect"] ? item.stats["Intellect"] : item.stats["intellect"]} Intellect`,
                        colour: "var(--stat-intellect)"
                    });
                };                                                      
                secondaryStats.forEach((stat, index) => {
                    if (stat.name === "Critical Strike") {
                        stat.name = "Crit";
                    };
                    newItemDetails.push({
                        id: `new-equipped-item-stat-${index + 1}`,
                        text: `+${stat.value} ${stat.name.charAt(0).toUpperCase()}${stat.name.slice(1)}`,
                        colour: `var(--stat-${stat.name.toLowerCase()})`
                    });
                });
                
                if (item.stats["leech"]) {
                    newItemDetails.push({
                        id: `newt-equipped-item-leech`,
                        text: `+${item.stats["leech"]} Leech`,
                        colour: "var(--leech-font)"
                    });
                };

                const itemDetailsLength = newItemDetails.length;
                if (itemDetailsLength < 4) {
                    for (let i = 0; i < 4 - itemDetailsLength; i++) {
                        newItemDetails.push({ id: "", text: "", colour: "" });
                    };
                };

                newItemDetails.forEach(itemStat => {
                    const field = createElement("div", "new-equipped-item-field-left", itemStat.id);
                    field.textContent = itemStat.text;
                    field.style.color = itemStat.colour;
                    newItemLeftContainer.appendChild(field);

                    if (["new-equipped-item-stat-1", "new-equipped-item-stat-2"].includes(itemStat.id) && item.name in craftedItemsToUse) {
                        let stat = itemStat.text.split(" ")[1];
                        if (stat === "Crit") stat = "Critical Strike";

                        field.contentEditable = true;
                        field.addEventListener("input", (e) => {
                            if (e.target.innerText === "") {
                                e.target.innerHTML = "&#8203";
                            };
                        });

                        field.addEventListener("blur", () => {
                            const valueMatch = field.textContent.match(/\d+/);
                            let newStatValue = valueMatch ? parseInt(valueMatch[0]) : 0;

                            const statMatch = field.textContent.match(/[a-zA-Z]+/);
                            let statName = statMatch ? statMatch[0].toLowerCase() : null;

                            if (statName !== stat) {
                                delete item.stats[stat];
                                item.stats[statName] = newStatValue;
                                if (statName === "Critical Strike") statName = "Crit";
                                field.textContent = `+${item.stats[statName]} ${statName.charAt(0).toUpperCase()}${statName.slice(1)}`;
                                field.style.color = `var(--stat-${statName})`;
                            } else {
                                item.stats[stat] = newStatValue;
                                if (stat === "Critical Strike") stat = "crit";
                                field.textContent = `+${item.stats[stat]} ${stat.charAt(0).toUpperCase()}${stat.slice(1)}`;
                                field.style.color = `var(--stat-${stat})`;
                            };
                        });

                        field.addEventListener("keydown", (e) => {
                            if (e.key !== "Enter") return;

                            field.blur();                             
                        });
                    };

                    if (itemStat.id == 0) {
                        field.contentEditable = true;

                        field.addEventListener("input", (e) => {
                            if (e.target.innerText === "") {
                                e.target.innerHTML = "&#8203";
                            };
                        });

                        field.addEventListener("blur", () => {
                            const matches = field.textContent.match(/\d+/);
                            let newLeechValue = matches ? parseInt(matches[0]) : 0;
                            
                            if (newLeechValue > 0) {
                                item.stats["leech"] = newLeechValue;
                                field.textContent = `+${item.stats["leech"]} Leech`;
                                field.style.color = "var(--leech-font)";
                            } else {
                                delete item.stats["leech"];
                            };                  
                        });

                        field.addEventListener("keydown", (e) => {
                            if (e.key !== "Enter") return;

                            field.blur();                         
                        });

                        field.addEventListener("focus", (e) => {
                            if (e.target.innerText === "") {
                                e.target.innerHTML = "&#8203";
                            };
                        });
                    };
                });
            };

            const selectedItemSlot = document.getElementById("equipped-items-edit-choose-slot-dropdown").value;

            const createNewItemBonusesDisplay = () => {
                const availableEnchants = itemSlotBonusesToUse[selectedItemSlot]["enchants"];
        
                const newItemEnchantSelect = createElement("div", "new-equipped-item-field-right", "new-equipped-item-enchants");
                const defaultEnchantOption = createElement("div", "new-equipped-item-default-enchant-option", null);
                if (item["enchantments"] && item["enchantments"].length > 0) {
                    defaultEnchantOption.textContent = item["enchantments"][0];
                    defaultEnchantOption.style.color = "var(--rarity-uncommon)";
                } else if (availableEnchants.length > 0) {
                    defaultEnchantOption.textContent = "No enchant";
                    defaultEnchantOption.style.color = "var(--rarity-common)";
                } else {
                    defaultEnchantOption.textContent = "No enchants available";
                    defaultEnchantOption.style.color = "var(--rarity-poor)";
                };
                newItemEnchantSelect.appendChild(defaultEnchantOption);

                const enchantOptions = createElement("div", "new-equipped-item-enchant-options", null);
                newItemEnchantSelect.appendChild(enchantOptions);
                newItemEnchantSelect.addEventListener("click", () => {
                    if (defaultEnchantOption.textContent !== "No enchants available") {
                        enchantOptions.style.display = enchantOptions.style.display === "flex" ? "none" : "flex";      
                    };
                });

                availableEnchants.forEach(enchant => {
                    const enchantOption = createElement("div", "new-equipped-item-enchant-option", null);
                    enchantOption.textContent = enchant;
                    enchantOptions.appendChild(enchantOption);

                    enchantOption.addEventListener("click", () => {
                        let updatedEnchantData = null;
                        if (enchantOption.textContent === "No enchant") {
                            defaultEnchantOption.textContent = `${enchantOption.textContent}`;
                            defaultEnchantOption.style.color = "var(--light-font-colour)";
                            updatedEnchantData = [];
                        } else {
                            defaultEnchantOption.textContent = `Enchanted: ${enchantOption.textContent}`;
                            defaultEnchantOption.style.color = "var(--rarity-uncommon)";
                            updatedEnchantData = [`Enchanted: ${enchantOption.textContent}`];
                        };
                        item["enchantments"] = updatedEnchantData;
                    });
                });
                newItemRightContainer.appendChild(newItemEnchantSelect);

                // gems
                const newItemGemsField = createElement("div", "new-equipped-item-field-right new-equipped-item-gems-field", null);
                newItemRightContainer.appendChild(newItemGemsField);

                const newItemGemsContainer = createElement("div", "new-equipped-item-gems-container", null);
                newItemGemsField.appendChild(newItemGemsContainer);

                const addGemContainer = createElement("div", "new-equipped-item-add-gem-container", null);
                const addGemButton = createElement("div", "new-equipped-item-add-gem-button", null);
                const addGemIcon = createElement("div", "new-equipped-item-add-gem-icon fa-solid fa-plus", null);
                addGemButton.appendChild(addGemIcon);
                addGemContainer.appendChild(addGemButton);

                // gem modal
                const addGemModal = createElement("div", "add-gem-modal", null);
                addGemContainer.appendChild(addGemModal);
                addGemContainer.addEventListener("click", () => {
                    addGemModal.style.display = addGemModal.style.display === "block" ? "none" : "block";
                });

                const secondaryStatRow = createElement("div", "gem-modal-row stat-label-row", null);
                const statLabelsContainer = createElement("div", "stat-labels-container", null);
                secondaryStatRow.appendChild(statLabelsContainer);
                const statLabels = ["+Haste", "+Crit", "+Mast", "+Vers", "+Int"];
                statLabels.forEach(label => {
                    const container = createElement("div", "row-stat-label", null);
                    container.textContent = label;
                    statLabelsContainer.appendChild(container);
                })
                addGemModal.appendChild(secondaryStatRow);

                let newGemData = [];
                Object.values(gemsToUse).forEach(group => {
                    const row = createElement("div", "gem-modal-row", null);

                    const rowLabel = createElement("div", "gem-modal-row-label", null);
                    rowLabel.textContent = group["label"];
                    rowLabel.style.color = `var(--stat-${group["label"].toLowerCase()})`;
                    row.appendChild(rowLabel);

                    group["gems"].forEach(([gemName, gemIcon, gemStatOne, gemStatTwo]) => {
                        const modalGemContainer = createElement("div", "gem-modal-gem-container", null);
                        const modalGemIcon = createElement("img", "gem-modal-gem-icon", null);
                        modalGemIcon.src = gemIcon;
                        modalGemIcon.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;
                        modalGemContainer.appendChild(modalGemIcon);
                        modalGemContainer.addEventListener("click", () => {
                            newGemData.push(gemName);
                            item["gems"] = newGemData;

                            const newItemGemContainer = createElement("div", "new-equipped-item-gem-container", null);
                            const newItemGemIcon = createElement("img", "new-equipped-item-gem-icon", null);
                            newItemGemIcon.src = gemIcon;
                            newItemGemContainer.appendChild(newItemGemIcon);

                            newItemGemContainer.addEventListener("click", () => {
                                newItemGemContainer.remove();
                                if (item["gems"]) {
                                    const indexToRemove = item["gems"].findIndex(gemToRemove => gemToRemove === gemName);
                                    
                                    if (indexToRemove !== -1) {
                                        item["gems"].splice(indexToRemove, 1);
                                    };
                                };
                            });
                            newItemGemsContainer.insertBefore(newItemGemContainer, addGemContainer);           
                        });

                        const modalGemTooltip = createElement("div", "gem-modal-tooltip", null);
                        modalGemTooltip.style.display = "none";
                        modalGemTooltip.style.position = "absolute";
                        document.body.appendChild(modalGemTooltip);
                        modalGemContainer.addEventListener("mousemove", (e) => {
                            const xOffset = 15;
                            const yOffset = 15;

                            modalGemTooltip.style.left = e.pageX + xOffset + "px";
                            modalGemTooltip.style.top = e.pageY + yOffset + "px";

                            modalGemTooltip.style.display = "block";
                            modalGemTooltip.style.border = `1px solid var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})`;

                            modalGemTooltip.innerHTML = "";
                            const tooltipGemName = createElement("div", "gem-modal-tooltip-gem-name", null);
                            tooltipGemName.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemName}</span>`;
                            
                            const tooltipStats = createElement("div", "gem-modal-tooltip-gem-stats", null);
                            if (gemStatTwo) {
                                tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span> & <span style="color: var(--stat-${gemStatTwo.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatTwo}</span>`;
                            } else {
                                tooltipStats.innerHTML = `<span style="color: var(--stat-${gemStatOne.replace(/\+\d+\s+/, "").toLowerCase()})">${gemStatOne}</span>`;
                            };
                            
                            modalGemTooltip.appendChild(tooltipGemName);
                            modalGemTooltip.appendChild(tooltipStats);
                        });
                        modalGemContainer.addEventListener("mouseleave", () => {
                            modalGemTooltip.style.display = "none";
                        });
                        modalGemContainer.addEventListener("click", () => {
                            modalGemTooltip.style.display = "none";
                        });

                        row.appendChild(modalGemContainer);
                    });

                    addGemModal.appendChild(row);
                });
                newItemGemsContainer.appendChild(addGemContainer);

                const gemsData = item["gems"];
                if (gemsData) {
                    gemsData.forEach(gem => {
                        const newItemGemContainer = createElement("div", "new-equipped-item-gem-container", null);
                        const newItemGemIcon = createElement("img", "new-equipped-item-gem-icon", null);
                        newItemGemIcon.src = itemsToIconsMap[gem];
                        newItemGemContainer.appendChild(newItemGemIcon);

                        newItemGemContainer.addEventListener("click", () => {
                            newItemGemContainer.remove();
                            if (item["gems"]) {
                                const indexToRemove = item["gems"].findIndex(gemToRemove => gemToRemove === gem);
                                
                                if (indexToRemove !== -1) {
                                    item["gems"].splice(indexToRemove, 1);
                                };
                            };
                        });

                        newItemGemsContainer.insertBefore(newItemGemContainer, addGemContainer);
                    });
                };

                // embellishments
                const newItemEmbellishmentSelect = createElement("div", "new-equipped-item-field-right-double", "new-equipped-item-embellishments");
                const defaultEmbellishmentOption = createElement("div", "new-equipped-item-default-embellishment-option", null);
                if (item["effects"].length > 0 && (craftedItemsToUse[item.name] || embellishmentItemsToUse[item.name])) {
                    defaultEmbellishmentOption.textContent = `Embellishment: ${item["effects"][0].name}`;
                    defaultEmbellishmentOption.style.color = "var(--mana)";
                } else if (craftedItemsToUse[item.name] || embellishmentItemsToUse[item.name]) {
                    defaultEmbellishmentOption.textContent = `No embellishment`;
                    defaultEmbellishmentOption.style.color = "var(--light-font-colour)";
                } else {
                    defaultEmbellishmentOption.textContent = `No embellishments available`;
                    defaultEmbellishmentOption.style.color = "var(--rarity-poor)";
                };
                newItemEmbellishmentSelect.appendChild(defaultEmbellishmentOption);

                const embellishmentOptions = createElement("div", "new-equipped-item-embellishment-options", null);
                newItemEmbellishmentSelect.appendChild(embellishmentOptions);
                newItemEmbellishmentSelect.addEventListener("click", () => {
                    if (craftedItemsToUse[item.name]) {
                        embellishmentOptions.style.display = embellishmentOptions.style.display === "flex" ? "none" : "flex";
                    };
                });

                if (craftedItemsToUse[item.name]) {
                    for (const embellishment in itemSlotBonusesToUse[selectedItemSlot]["embellishments"]) {
                        const embellishmentOption = createElement("div", "new-equipped-item-embellishment-option", null);
                        embellishmentOption.textContent = embellishment;
                        embellishmentOptions.appendChild(embellishmentOption);
        
                        embellishmentOption.addEventListener("click", () => {
                            let updatedEmbellishmentData = null;
                            if (embellishmentOption.textContent === "No embellishment") {
                                defaultEmbellishmentOption.textContent = `${embellishmentOption.textContent}`;
                                defaultEmbellishmentOption.style.color = "var(--light-font-colour)";
                                updatedEmbellishmentData = "";
                            } else {
                                defaultEmbellishmentOption.textContent = `Embellishment: ${embellishmentOption.textContent}`;
                                defaultEmbellishmentOption.style.color = "var(--mana)";
                                updatedEmbellishmentData = [{"name": embellishmentsToUse[embellishment].name, "description": embellishmentsToUse[embellishment].description, "id": embellishmentsToUse[embellishment].id, "type": embellishmentsToUse[embellishment].type, "effect_values": embellishmentsToUse[embellishment].effect_values}];
                            };
                            updatedEmbellishmentData = generateItemEffects(updatedEmbellishmentData, document.getElementById("equipped-items-edit-choose-slot-dropdown").value, newItemLevel.textContent);
                            item["effects"] = updatedEmbellishmentData;
                            item["limit"] = "Unique-Equipped: Embellished (2)";
                        });
                    };
                };   
                newItemRightContainer.appendChild(newItemEmbellishmentSelect);

                const newItemInfo = document.getElementById("new-equipped-item-info");

                // newItemInfo.querySelectorAll(".new-equipped-item-field-left").forEach(item => {
                //     item.style.borderBottom = `1px solid ${rarityColour}`;
                // });
                // newItemInfo.querySelectorAll(".new-equipped-item-field-right").forEach(item => {
                //     item.style.borderBottom = `1px solid ${rarityColour}`;
                // });
                // newItemInfo.querySelectorAll(".new-equipped-item-enchant-options").forEach(item => {
                //     item.style.border = `1px solid ${rarityColour}`;
                // });
                // newItemInfo.querySelectorAll(".new-equipped-item-embellishment-options").forEach(item => {
                //     item.style.border = `1px solid ${rarityColour}`;
                // });   

                // newItemInfo.querySelector(".new-equipped-item-info-left").style.borderRight = `1px solid ${rarityColour}`;
                // if (newItemInfo.querySelector(".new-equipped-item-default-enchant-option")) {
                //     newItemInfo.querySelector(".new-equipped-item-default-enchant-option").style.borderBottom = `1px solid ${rarityColour}`;
                // };
                // if (newItemInfo.querySelector(".new-equipped-item-default-embellishment-option")) {
                //     newItemInfo.querySelector(".new-equipped-item-default-embellishment-option").style.borderBottom = `1px solid ${rarityColour}`;
                // };
                if (newItemInfo.querySelector(".new-equipped-item-field-right-double")) {
                    // currentItemInfo.querySelector(".current-equipped-item-default-embellishment-option").style.borderBottom = `1px solid ${rarityColour}`;
                    newItemInfo.querySelector(".new-equipped-item-field-right-double").style.borderBottom = `none`;
                };

                if (enchantOptions) {
                    enchantOptions.style.backgroundColor = `var(--rarity-${item.quality.toLowerCase()}-dark)`;
                };
                if (embellishmentOptions) {
                    embellishmentOptions.style.backgroundColor = `var(--rarity-${item.quality.toLowerCase()}-dark)`;
                };
                enchantOptions.style.borderRight = `1px solid ${rarityColour}`;
                enchantOptions.style.borderBottom = `1px solid ${rarityColour}`;
                
            };
    
            const createNewItemTrinketBonusesDisplay = () => {
                const newTrinketEffectField = createElement("div", "new-equipped-item-field-right-trinket", "new-equipped-item-trinket-effects-0");
                const newTrinketEffect = createElement("div", "new-equipped-item-trinket-effect", null);
                if (item["effects"].length > 0) {
                    const descriptionText = item["effects"][0].description.replaceAll("*", "").replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
                    newTrinketEffect.innerHTML = `${descriptionText}`;
                    newTrinketEffect.style.color = "var(--mana)";
                } else {
                    newTrinketEffect.textContent = `No effect`;
                    newTrinketEffect.style.color = "var(--rarity-poor)";
                };
                newTrinketEffectField.appendChild(newTrinketEffect);
                newItemRightContainer.appendChild(newTrinketEffectField);

                const newItemInfo = document.getElementById("new-equipped-item-info");

                // newItemInfo.querySelectorAll(".new-equipped-item-field-left").forEach(item => {
                //     item.style.borderBottom = `1px solid ${rarityColour}`;
                // });

                newItemInfo.querySelector(".new-equipped-item-info-left").style.borderRight = `1px solid ${rarityColour}`;
            };

            const jewelleryItemSlots = ["Necklace", "Ring 1", "Ring 2"];
            const miscItemSlots = ["Trinket 1", "Trinket 2"];

            if (jewelleryItemSlots.includes(selectedItemSlot)) {
                // left
                createNewItemStatsDisplay();

                // right
                createNewItemBonusesDisplay();

            } else if (miscItemSlots.includes(selectedItemSlot)) {
                // left
                createNewItemStatsDisplay();

                // right
                createNewItemTrinketBonusesDisplay();
            } else {
                // left
                createNewItemStatsDisplay();

                // right
                createNewItemBonusesDisplay();
            };
        };

        const searchInput = itemSearch.value.toLowerCase();
        const currentSlot = document.getElementById("equipped-items-edit-choose-slot-dropdown").value.toLowerCase();
        
        const filteredData = itemData.filter(item => {
            const slot = item.item_slot.toLowerCase();
            const searchMatch = item.name.toLowerCase().includes(searchInput);
            const slotMap = blizzardItemSlotsMap[slot];

            if (slot === "finger") {
                return searchMatch && (itemSlotsMap[currentSlot] === "finger_1" || itemSlotsMap[currentSlot] === "finger_2");
            } else if (slot === "trinket") {
                return searchMatch && (itemSlotsMap[currentSlot] === "trinket_1" || itemSlotsMap[currentSlot] === "trinket_2");
            } else {
                return searchMatch && slotMap === itemSlotsMap[currentSlot];
            };
        });

        itemSuggestions.innerHTML = "";
        itemSuggestions.style.display = "block";

        if (searchInput === "") {
            itemSuggestions.style.display = "none";
            return;
        };
        
        filteredData.forEach(item => {
            const itemContainer = createElement("div", "item-search-suggestion-container", null);

            const itemSuggestion = createElement("div", "item-search-suggestion", null);
            itemSuggestion.textContent = item.name;
            itemSuggestion.style.color = `var(--rarity-${item.quality.toLowerCase()})`;
            itemSuggestion.addEventListener("click", () => {
                itemSearch.value = item.name;
                itemSuggestions.innerHTML = "";
                updateNewItemDisplay(item);
                currentItemSuggestion = item;
                finalNewItemData = item;
            });

            if (filteredData.length <= 6) {
                itemSuggestion.style.borderRight = "none";
            } else {
                itemSuggestion.style.borderRight = "1px solid var(--border-colour-3)";
            };

            const itemIcon = createElement("img", "item-search-icon", null);
            itemIcon.src = item.icon;
            itemIcon.style.border = `1px solid var(--rarity-${item.quality.toLowerCase()})`;

            itemContainer.appendChild(itemIcon);
            itemContainer.appendChild(itemSuggestion);
            itemSuggestions.appendChild(itemContainer);
        });
    };

    const itemSearch = document.getElementById("new-equipped-item-search");
    const itemSuggestions = document.getElementById("item-search-suggestions");

    itemSearch.addEventListener("input", () => {
        generateSearchResults();
        itemSearch.style.color = "var(--light-font-colour)";
    });

    itemSearch.addEventListener("click", () => {
        generateSearchResults();
    });

    document.addEventListener("click", (e) => {
        if (e.target !== itemSearch) {
            itemSuggestions.innerHTML = "";
            itemSuggestions.style.display = "none";
            if (itemSearch.value !== "" && currentItemSuggestion) {
                itemSearch.value = currentItemSuggestion.name;
                itemSearch.style.color = `var(--rarity-${currentItemSuggestion.quality.toLowerCase()}`;
            };
        };
    });

    const replaceItemButton = document.getElementById("replace-item-button");
    replaceItemButton.addEventListener("click", () => {
        const renameKeys = (data, keyMap) => {
            const newData = {};
            Object.keys(data).forEach(key => {
                const newKey = keyMap[key] || key;
                newData[newKey] = data[key];
            });
            return newData;
        };
        
        const propertyKeyMap = {
            "id": "item_id",
            "icon": "item_icon",
            "base_item_level": "item_level"
        };

        const statsKeyMap = {
            "Intellect": "intellect",
            "Haste": "haste",
            "Critical Strike": "crit",
            "Mastery": "mastery",
            "Versatility": "versatility",
            "Leech": "leech"
        };

        if (Object.keys(finalNewItemData).length === 0) return;

        const currentSlot = document.getElementById("equipped-items-edit-choose-slot-dropdown").value.toLowerCase();
        let convertedItemSlot = "";

        const convertedCurrentSlot = itemSlotsMap[currentSlot];
        if (finalNewItemData["item_slot"]) {
            convertedItemSlot = blizzardItemSlotsMap[finalNewItemData["item_slot"].toLowerCase()];
        } else {
            convertedItemSlot = currentSlot.replaceAll(" ", "_");
        };

        if (convertedItemSlot.startsWith("trinket") && convertedCurrentSlot.startsWith("trinket")) {
        } else if (convertedItemSlot.startsWith("finger") && convertedCurrentSlot.startsWith("finger")) {
        } else if (convertedItemSlot !== convertedCurrentSlot) {
            return;
        };

        finalNewItemData["item_slot"] = convertedCurrentSlot;
        clearNewItem();
        let fullItemData = generateFullItemData();
        const slotToReplace = finalNewItemData["item_slot"];

        if (fullItemData.equipment && fullItemData.equipment[slotToReplace]) {
            fullItemData.equipment[slotToReplace] = finalNewItemData;
        };

        finalNewItemData = renameKeys(fullItemData.equipment[finalNewItemData["item_slot"]], propertyKeyMap);
        finalNewItemData["stats"] = renameKeys(fullItemData.equipment[finalNewItemData["item_slot"]]["stats"], statsKeyMap);
        if (!finalNewItemData["enchantments"]) finalNewItemData["enchantments"] = [];
        
        fullItemData.equipment[slotToReplace] = finalNewItemData;

        updateEquipmentFromImportedData(fullItemData);
        const itemSlots = document.querySelectorAll(".item-slot");
        const itemSlot = document.getElementById(`item-slot-${itemSlotsMap[currentSlot]}`);
        itemSlot.setAttribute("data-item-data", JSON.stringify(finalNewItemData));
        updateEquippedItemDisplay(itemSlot, itemSlots);
        updateStats();
    });
};

export { updateEquipmentFromImportedData, initialiseEquipment, generateFullItemData };