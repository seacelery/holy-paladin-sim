import { createElement } from "./index.js";
import { spellToIconsMap } from '../utils/spell-to-icons-map.js';
import { buffsToIconsMap } from "../utils/buffs-to-icons-map.js";

const createPriorityBreakdown = (simulationData, containerCount) => {
    const priorityData = simulationData.results.priority_breakdown;
    console.log(priorityData)
    const priorityBreakdownContainer = document.getElementById(`priority-breakdown-table-container-${containerCount}`);

    const createPriorityGrid = (data, container, headers) => {
        const gridContainer = createElement("div", "priority-grid-container", `priority-grid-container`);

        // generate header row
        const gridHeaderRow = createElement("div", "priority-grid-header-row", null);
        headers.forEach(header => {
            const headerCell = createElement("div", "priority-grid-header-cell priority-grid-cell", null);
            headerCell.textContent = header;
            gridHeaderRow.appendChild(headerCell);
        });
        gridContainer.appendChild(gridHeaderRow);

        // generate content rows
        for (const timestamp in priorityData) {
            const timestampData = priorityData[timestamp];

            const gridRow = createElement("div", "priority-grid-row", null);

            const timeCell = createElement("div", "priority-grid-time-cell priority-grid-cell", null);
            timeCell.textContent = Number(timestamp).toFixed(2);
            gridRow.appendChild(timeCell);

            const numberCell = createElement("div", "priority-grid-number-cell priority-grid-cell", null);
            numberCell.textContent = timestampData.priority_list_number;
            gridRow.appendChild(numberCell);

            const spellCell = createElement("div", "priority-grid-name-cell priority-grid-cell", null);
            const spellIconContainer = createElement("div", "priority-grid-spell-icon-container", null);
            const spellIcon = createElement("img", "priority-grid-spell-icon", null);
            spellIcon.src = spellToIconsMap[timestampData.spell_name];
            
            spellIconContainer.appendChild(spellIcon);
            spellCell.appendChild(spellIconContainer);
            gridRow.appendChild(spellCell);

            const resourcesCell = createElement("div", "priority-grid-resources-cell priority-grid-cell", null);
            // resourcesCell.textContent = `${timestampData.resources.holy_power} ${timestampData.resources.mana}`
            const holyPowerDisplay = createElement("img", "priority-grid-holy-power-display");
            holyPowerDisplay.src = `holy-power/holy-power-${timestampData.resources.holy_power}.png`;
            
            resourcesCell.appendChild(holyPowerDisplay);
            gridRow.appendChild(resourcesCell);

            const playerAurasCell = createElement("div", "priority-grid-player-auras-cell priority-grid-cell", null);
            gridRow.appendChild(playerAurasCell);

            const targetCell = createElement("div", "priority-grid-target-cell priority-grid-cell", null);
            const targetAurasCell = createElement("div", "priority-grid-target-auras-cell priority-grid-cell", null);

            for (const target in timestampData.target_active_auras) {
                // console.log(target)
                // console.log(timestampData.target_active_auras[target])
            };

            // gridRow.appendChild(targetCell);
            gridRow.appendChild(targetAurasCell);

            const cooldownsCell = createElement("div", "priority-grid-cooldowns-cell priority-grid-cell", null);
            gridRow.appendChild(cooldownsCell);

            gridContainer.appendChild(gridRow);
            
        };
        return gridContainer;
    };

    const gridHeaders = ["Time", "Priority", "Spell", "Resources", "Player Auras", "Target Auras", "Cooldowns"];
    const priorityGrid = createPriorityGrid(priorityData, priorityBreakdownContainer, gridHeaders);
    priorityBreakdownContainer.appendChild(priorityGrid);
};

export { createPriorityBreakdown };