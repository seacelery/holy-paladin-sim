import { createElement, updateStats } from "./index.js";
import { itemsToIconsMap, groupedGems } from "../utils/items-to-icons-map.js";
import { generateItem } from "../utils/item-level-calculations/generate-item.js";
import { itemSlotsMap } from "../utils/item-slots-map.js";
import { itemSlotBonuses } from "../utils/item-level-calculations/item-slot-bonuses.js";
import itemData from "../utils/data/item_data.js";

const updateEquipmentFromImportedData = (data) => {
    console.log(data)
    // left half
    const equipmentData = data["equipment"];
    console.log(equipmentData)
    let updatedEquipmentData = JSON.parse(JSON.stringify(equipmentData));
    console.log(updatedEquipmentData)

    let tierS1Counter = 0;
    let tierS2Counter = 0;
    let tierS3Counter = 0;
    let embellishmentCounter = 0;

    for (const itemSlot in equipmentData) {
        const itemSlotData = equipmentData[itemSlot];

        const itemIcon = itemSlotData["item_icon"];
        const itemLevel = itemSlotData["item_level"];
        const itemName = itemSlotData["name"];
        const itemEnchants = itemSlotData["enchantments"];
        const itemGems = itemSlotData["gems"];
        const itemStats = itemSlotData["stats"];
        const itemEffects = itemSlotData["effects"];
        const itemCategory = itemSlotData["limit"];

        const itemSlotContainer = document.getElementById(`item-slot-${itemSlot}`);
        itemSlotContainer.setAttribute("data-item-data", JSON.stringify(itemSlotData));

        const iconDisplay = itemSlotContainer.querySelector(`.item-slot-icon`);
        iconDisplay.src = itemIcon;
        iconDisplay.style.border = "1px solid var(--rarity-epic)";

        const itemLevelDisplay = itemSlotContainer.querySelector(`.item-slot-item-level`);
        itemLevelDisplay.textContent = itemLevel;
        itemLevelDisplay.style.display = "flex";
        itemLevelDisplay.style.border = "1px solid var(--rarity-epic)";
        itemLevelDisplay.style.borderTop = "none";

        const itemSlotInfo = itemSlotContainer.querySelector(`.item-slot-info`);
        itemSlotInfo.innerHTML = "";

        const itemSlotInfoContainer = createElement("div", "item-slot-info-container", null);
        itemSlotInfo.appendChild(itemSlotInfoContainer);

        if (itemName) {
            const itemNameDisplay = createElement("div", "item-slot-name", null);
            itemNameDisplay.textContent = itemName;
            itemSlotInfoContainer.appendChild(itemNameDisplay);
        };

        // if (itemStats) {
        //     const mainStatContainer = createElement("div", "item-slot-main-stat-container", null);
        //     for (let stat in itemStats) {
        //         if (stat === "intellect") {
        //             console.log(stat)
        //             const statNumber = itemStats[stat];
        //             stat = stat.charAt(0).toUpperCase() + stat.slice(1);
        //             const statContainer = createElement("div", "item-slot-stat-container", null);
        //             const statName = createElement("div", "item-slot-stat-name", null);
        //             statName.textContent = stat;
        //             const statValue = createElement("div", "item-slot-stat-value", null);
        //             statValue.textContent = statNumber;

        //             statContainer.appendChild(statValue);
        //             statContainer.appendChild(statName);

        //             mainStatContainer.appendChild(statContainer);
        //         };        
        //     };

        //     const secondaryStatsContainer = createElement("div", "item-slot-secondary-stats-container", null);
        //     for (let stat in itemStats) {
        //         if (stat !== "intellect" && stat !== "stamina" && stat !== "leech" && stat !== "avoidance") {
        //             const statNumber = itemStats[stat];
        //             stat = stat.charAt(0).toUpperCase() + stat.slice(1);
        //             const statContainer = createElement("div", "item-slot-stat-container", null);
        //             const statName = createElement("div", "item-slot-stat-name", null);
        //             statName.textContent = stat;
        //             const statValue = createElement("div", "item-slot-stat-value", null);
        //             statValue.textContent = statNumber;

        //             statContainer.appendChild(statValue);
        //             statContainer.appendChild(statName);                  

        //             secondaryStatsContainer.appendChild(statContainer);
        //         };        
        //     };
        //     itemSlotInfo.appendChild(mainStatContainer);
        //     itemSlotInfo.appendChild(secondaryStatsContainer);
        // };

        if (itemEnchants) {
            for (const enchant in itemEnchants) {
                let enchantText = itemEnchants[enchant];
                let formattedEnchantText = enchantText.split(":");
                if (formattedEnchantText.length > 1) {
                    formattedEnchantText = formattedEnchantText[1].split("|")[0];
                };

                if (formattedEnchantText.includes("Flexweave Underlay") || formattedEnchantText.includes("Personal Space Amplifier")) {
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
                if (stat === "leech") {
                    const leechValue = itemStats[stat];
                    const leechContainer = createElement("div", "item-slot-leech-container", null);
                    leechContainer.textContent = "+" + leechValue + " Leech";
                    gemsContainer.appendChild(leechContainer);
                };
            };
        };

        if (itemCategory) {
            const itemCategoryDisplay = createElement("div", "item-slot-category", null);
            const itemCategoryText = itemCategory.replace("Unique-Equipped: ", "")
                                                 .replace("Embellished", "Embellishment")
                                                 .replace(/\s\(\d+\)/g, "");
            if (itemEffects && itemCategory.includes("Embellished")) {
                itemCategoryDisplay.textContent = `${itemCategoryText}: ${itemEffects[0]["name"]}`;
            } else {
                itemCategoryDisplay.textContent = itemCategoryText;
            };          
            
            itemSlotInfoContainer.appendChild(itemCategoryDisplay);            
        };

        const tierSetNames = ["Virtuous Silver", "Heartfire Sentinel", "Zealous Pyreknight"];
        const bonusesDisplay = createElement("div", "item-slot-bonuses");
        if (itemName.includes(tierSetNames[0])) {
            bonusesDisplay.textContent = "Tier Season 1";
            tierS1Counter += 1;
        } else if (itemName.includes(tierSetNames[1])) {
            bonusesDisplay.textContent = "Tier Season 2";
            tierS2Counter += 1;
        } else if (itemName.includes(tierSetNames[2])) {
            bonusesDisplay.textContent = "Tier Season 3";
            tierS3Counter += 1;
        };
        itemSlotInfoContainer.appendChild(bonusesDisplay);

        if (window.getComputedStyle(itemSlotInfoContainer).height.replace("px", "") > 90) {
            itemSlotInfoContainer.style.borderRight = "1px solid var(--border-colour-3)";
        };
    };

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

    const embellishmentsContainer = createElement("div", "item-slot-embellishments", null);
    let embellishmentColour = embellishmentCounter >= 2 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
    embellishmentsContainer.innerHTML = `<span style="color: var(--paladin-font)">Embellishments</span> <span style="color: ${embellishmentColour}">${embellishmentCounter}/2</span>`;
    equippedItemsInfo.appendChild(embellishmentsContainer);

    // right half
    const statsData = data["stats"];
    console.log(statsData)
    for (const stat in statsData) {
        console.log(statsData)
        if (["haste", "crit", "versatility", "mastery", "leech"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            console.log(statContainer)
            const statValue = statContainer.querySelector(".equipped-items-stat-value");

            const statPercent = `${stat}_percent`;
            statValue.textContent = `${statsData[stat]} / ${statsData[statPercent].toFixed(2)}%`;
        } else if (["intellect", "health", "mana"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            console.log(statContainer)
            const statValue = statContainer.querySelector(".equipped-items-stat-value");
            statValue.textContent = statsData[stat];
        };
    };
};

const generateFullItemData = () => {
    let fullItemData = {"equipment": {}};
    const itemSlots = document.querySelectorAll(".item-slot");
    itemSlots.forEach(itemSlot => {
        const slotData = JSON.parse(itemSlot.getAttribute("data-item-data"));
        const slotType = itemSlot.getAttribute("data-item-slot");
        fullItemData["equipment"][itemSlotsMap[slotType.toLowerCase()]] = slotData;
    });
    console.log("updated item data")
    console.log(fullItemData)
    updateEquipmentFromImportedData(fullItemData);
    return fullItemData;
};

const initialiseEquipment = () => {
    const updateEquippedItemDisplay = (itemSlot, itemSlots) => {
        const currentEquippedIcon = document.getElementById("current-equipped-item-icon");
        const currentItemLevel = document.getElementById("equipped-item-item-level");
        const currentItemTitle = document.getElementById("current-equipped-item-title");
        const currentItemInfoContainer = document.getElementById("current-equipped-item-info-container");
        const currentItemInfo = document.getElementById("current-equipped-item-info");

        console.log(itemSlot)
        console.log(itemSlot.getAttribute("data-item-data"))    
        const itemSlotData = JSON.parse(itemSlot.getAttribute("data-item-data"));

        const updateItemData = (property, new_value) => {
            itemSlotData[property] = new_value;
            itemSlot.setAttribute("data-item-data", JSON.stringify(itemSlotData))
            generateFullItemData();
            updateStats();
        };

        itemSlots.forEach(itemSlot => {
            itemSlot.querySelector(".item-slot-hover").classList.remove("item-slot-selected");
            itemSlot.querySelector(".item-slot-hover").style.backgroundColor = "var(--tooltip-colour)";
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

        currentItemLevel.textContent = itemLevel;
        currentItemLevel.style.color = rarityColour;
        currentItemLevel.style.borderTop = `1px solid ${rarityColour}`;

        currentItemTitle.style.border = `1px solid ${rarityColour}`;
        currentItemTitle.style.borderBottom = "none";
        currentItemTitle.innerHTML = `<span>Currently equipped: </span><span style="color: ${rarityColour}">${itemName}</span>`;

        currentItemInfoContainer.style.border = `1px solid ${rarityColour}`;
        
        currentItemInfo.style.borderLeft = `1px solid ${rarityColour}`;

        const jewelleryItemSlots = ["Necklace", "Ring 1", "Ring 2"];
        const miscItemSlots = ["Trinket 1", "Trinket 2"];
        const selectedItemSlot = itemSlot.getAttribute("data-item-slot");

        if (jewelleryItemSlots.includes(selectedItemSlot)) {
            return
        } else if (miscItemSlots.includes(selectedItemSlot)) {
            return
        } else {
            currentItemInfo.innerHTML = "";
            const currentItemLeftContainer = createElement("div", "current-equipped-item-info-left", null);      
            currentItemInfo.appendChild(currentItemLeftContainer);
            const currentItemRightContainer = createElement("div", "current-equipped-item-info-right", null);
            currentItemInfo.appendChild(currentItemRightContainer);
            // left
            const currentItemStats = itemSlotData.stats;
            const secondaryStats = ["haste", "versatility", "mastery", "crit"].filter(stat => currentItemStats.hasOwnProperty(stat))
                                                                              .sort((a, b) => currentItemStats[b] - currentItemStats[a])
                                                                              .map(stat => {
                                                                                return {name: stat, value: currentItemStats[stat]}
                                                                              })                                                                 

            const currentItemDetails = [
                {id: "current-equipped-item-intellect", text: `+${itemSlotData.stats["intellect"]} Intellect`, colour: "var(--stat-intellect)"},
                {id: "current-equipped-item-stat-one", text: `+${secondaryStats[0]["value"]} ${secondaryStats[0]["name"].charAt(0).toUpperCase()}${secondaryStats[0]["name"].slice(1)}`, colour: `var(--stat-${secondaryStats[0]["name"]})`},
                {id: "current-equipped-item-stat-two", text: `+${secondaryStats[1]["value"]} ${secondaryStats[1]["name"].charAt(0).toUpperCase()}${secondaryStats[1]["name"].slice(1)}`, colour: `var(--stat-${secondaryStats[1]["name"]})`},
                {id: "current-equipped-item-leech", text: itemSlotData.stats["leech"] ? `+${itemSlotData.stats["leech"]} Leech` : "", colour: "var(--leech-font)"},
            ];
            currentItemDetails.forEach(item => {
                const field = createElement("div", "current-equipped-item-field-left", item.id);
                field.textContent = item.text;
                field.style.color = item.colour;
                currentItemLeftContainer.appendChild(field);
            });

            // right
            // enchants
            const currentItemEnchantSelect = createElement("div", "current-equipped-item-field-right", "current-equipped-item-enchants");
            const defaultEnchantOption = createElement("div", "current-equipped-item-default-enchant-option", null);
            if (itemSlotData["enchantments"]) {
                defaultEnchantOption.textContent = itemSlotData["enchantments"][0].split("|")[0];
                defaultEnchantOption.style.color = "var(--rarity-uncommon)";
            } else {
                defaultEnchantOption.textContent = "No enchants available";
                defaultEnchantOption.style.color = "var(--light-font-colour)";
            };
            
            currentItemEnchantSelect.appendChild(defaultEnchantOption);

            const enchantOptions = createElement("div", "current-equipped-item-enchant-options", null);
            currentItemEnchantSelect.appendChild(enchantOptions);
            currentItemEnchantSelect.addEventListener("click", () => {
                enchantOptions.style.display = enchantOptions.style.display === "flex" ? "none" : "flex";
            });

            itemSlotBonuses[selectedItemSlot]["enchants"].forEach(enchant => {
                const enchantOption = createElement("div", "current-equipped-item-enchant-option", null);
                enchantOption.textContent = enchant;
                enchantOptions.appendChild(enchantOption);

                enchantOption.addEventListener("click", () => {
                    let updatedEnchantData = null;
                    if (enchantOption.textContent === "No enchant") {
                        defaultEnchantOption.textContent = `${enchantOption.textContent}`;
                        defaultEnchantOption.style.color = "var(--light-font-colour)";
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

            Object.values(groupedGems).forEach(group => {
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

                    currentItemGemContainer.addEventListener("click", () => {
                        currentItemGemContainer.remove()
                    });

                    currentItemGemsContainer.insertBefore(currentItemGemContainer, addGemContainer);
                });
            };
        };
    };

    // item slot select
    const itemSlotDropdown = document.getElementById("equipped-items-edit-choose-slot-dropdown");

    const itemSlots = document.querySelectorAll(".item-slot");
    itemSlots.forEach(itemSlot => {
        itemSlot.addEventListener("click", () => {
            updateEquippedItemDisplay(itemSlot, itemSlots);
            const dataItemSlot = itemSlot.getAttribute("data-item-slot");
            itemSlotDropdown.value = dataItemSlot;
        });
    });

    itemSlotDropdown.addEventListener("change", (e) => {
        const slotName = e.target.value.toLowerCase();
        const itemSlot = document.getElementById(`item-slot-${itemSlotsMap[slotName]}`);
        updateEquippedItemDisplay(itemSlot, itemSlots);
    });

    // item search
    const generateSearchResults = () => {
        const searchInput = itemSearch.value.toLowerCase();
        const filteredData = itemData.filter(item => item.name.toLowerCase().includes(searchInput));
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
            itemSuggestion.addEventListener("click", () => {
                itemSearch.value = item.name;
                itemSuggestions.innerHTML = "";
            });

            if (filteredData.length <= 6) {
                itemSuggestion.style.borderRight = "none";
            } else {
                itemSuggestion.style.borderRight = "1px solid var(--border-colour-3)";
            }

            const itemIcon = createElement("img", "item-search-icon", null);
            itemIcon.src = item.icon;

            itemContainer.appendChild(itemIcon);
            itemContainer.appendChild(itemSuggestion);
            itemSuggestions.appendChild(itemContainer);
        });
    };

    const itemSearch = document.getElementById("new-equipped-item-search");
    const itemSuggestions = document.getElementById("item-search-suggestions");

    itemSearch.addEventListener("input", () => {
        generateSearchResults();
    });

    itemSearch.addEventListener("click", () => {
        generateSearchResults();
    });

    document.addEventListener("click", (e) => {
        if (e.target !== itemSearch) {
            itemSuggestions.innerHTML = "";
            itemSuggestions.style.display = "none";
        };
    });

    const replaceItemButton = document.getElementById("replace-item-button");
    replaceItemButton.addEventListener("click", () => {
        console.log(itemSearch.value)
    });
};

export { updateEquipmentFromImportedData, initialiseEquipment, generateFullItemData };