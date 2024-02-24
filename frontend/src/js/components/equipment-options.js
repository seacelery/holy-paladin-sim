import { createElement } from "./index.js";
import { itemsToIconsMap } from "../utils/items-to-icons-map.js";
import { generateItem } from "../utils/item-level-calculations/generate-item.js";
import { itemSlotsMap } from "../utils/item-slots-map.js";
import itemData from "../utils/data/item_data.js";

const updateEquipmentFromImportedData = (data) => {
    // left half
    const equipmentData = data["equipment"];

    let tier16Counter = 0;
    let embellishmentCounter = 0;

    for (const itemSlot in equipmentData) {
        const itemSlotData = equipmentData[itemSlot];

        const itemIcon = itemSlotData["item_icon"];
        const itemLevel = itemSlotData["item_level"];
        const itemName = itemSlotData["name"];
        const itemEnchants = itemSlotData["enchantments"];
        const itemGems = itemSlotData["gems"];
        const itemStats = itemSlotData["stats"];

        const itemSlotContainer = document.getElementById(`item-slot-${itemSlot}`);

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

        if (itemName) {
            const itemNameDisplay = createElement("div", "item-slot-name", null);
            itemNameDisplay.textContent = itemName;
            itemSlotInfo.appendChild(itemNameDisplay);
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

                if (formattedEnchantText.includes("Flexweave Underlay")) {
                    continue
                };
                
                const itemEnchantDisplay = createElement("div", "item-slot-enchants", null);
                itemEnchantDisplay.textContent = formattedEnchantText;
                itemSlotInfo.appendChild(itemEnchantDisplay);
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
        itemSlotInfo.appendChild(gemsContainer);

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

        const bonusesDisplay = createElement("div", "item-slot-bonuses");
        if (itemName.includes("Virtuous Silver")) {
            bonusesDisplay.textContent = "Tier 16";
            tier16Counter += 1;
        };
        itemSlotInfo.appendChild(bonusesDisplay);

        // const itemSlotHover = itemSlotContainer.querySelector(`.item-slot-hover`);
        // itemSlotHover.style.height = "calc(100% + 15px)";
    };

    const equippedItemsInfo = document.getElementById("equipped-items-info");
    if (tier16Counter) {
        const tier16Container = createElement("div", "item-slot-tier", null);
        let tier16Colour = tier16Counter >= 4 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
        tier16Container.innerHTML = `<span style="color: var(--paladin-font)">Tier 16</span> <span style="color: ${tier16Colour}">${tier16Counter}/5</span>`;
        equippedItemsInfo.appendChild(tier16Container);
    };
    const embellishmentsContainer = createElement("div", "item-slot-embellishments", null);
    let embellishmentColour = embellishmentCounter >= 2 ? "var(--sorting-arrow-colour)" : "var(--red-font-hover)";
    embellishmentsContainer.innerHTML = `<span style="color: var(--paladin-font)">Embellishments</span> <span style="color: ${embellishmentColour}">${embellishmentCounter}/2</span>`;
    equippedItemsInfo.appendChild(embellishmentsContainer);

    // right half
    const statsData = data["stats"];
    console.log(statsData)
    for (const stat in statsData) {
        if (["haste", "crit", "versatility", "mastery"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            console.log(statContainer)
            const statValue = statContainer.querySelector(".equipped-items-stat-value");

            const statPercent = `${stat}_percent`;
            statValue.textContent = `${statsData[stat]} / ${statsData[statPercent].toFixed(2)}%`;
        } else if (["intellect", "leech", "health", "mana"].includes(stat)) {
            const statContainer = document.getElementById(`equipped-items-stats-${stat}`);
            console.log(statContainer)
            const statValue = statContainer.querySelector(".equipped-items-stat-value");
            statValue.textContent = statsData[stat];
        };
    };
};

const initialiseEquipment = () => {
    const updateEquippedItemDisplay = (itemSlot, itemSlots) => {
        const currentEquippedIcon = document.getElementById("current-equipped-item-icon");

        itemSlots.forEach(itemSlot => {
            itemSlot.querySelector(".item-slot-hover").classList.remove("item-slot-selected");
            itemSlot.querySelector(".item-slot-hover").style.backgroundColor = "var(--tooltip-colour)";
        })
        itemSlot.querySelector(".item-slot-hover").classList.add("item-slot-selected");
        itemSlot.querySelector(".item-slot-hover").style.backgroundColor = "var(--panel-colour-5)";

        const selectedItemIcon = itemSlot.querySelector(".item-slot-icon");
        currentEquippedIcon.src = selectedItemIcon.src;
        currentEquippedIcon.style.filter = "grayscale(0)";
        currentEquippedIcon.style.opacity = "1";
    };

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

export { updateEquipmentFromImportedData, initialiseEquipment };