import { createElement } from "./index.js";
import { itemsToIconsMap } from "../utils/items-to-icons-map.js";

const updateEquipmentFromImportedData = (data) => {
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
    };

    const equippedItemsInfo = document.getElementById("equipped-items-info");
    if (tier16Counter) {
        const tier16Container = createElement("div", "item-slot-tier", null);
        tier16Container.innerHTML = `<span style="color: var(--paladin-font)">Tier 16</span> <span style="color: var(--sorting-arrow-colour)">${tier16Counter}/5</span>`;
        equippedItemsInfo.appendChild(tier16Container);
    };
    const embellishmentsContainer = createElement("div", "item-slot-embellishments", null);
    embellishmentsContainer.innerHTML = `<span style="color: var(--subrow-arrow-colour)">Embellishments</span> <span style="color: var(--red-font-hover)">${embellishmentCounter}/2</span>`;
    equippedItemsInfo.appendChild(embellishmentsContainer);
};

export { updateEquipmentFromImportedData };