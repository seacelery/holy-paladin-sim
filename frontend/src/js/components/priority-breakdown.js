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
            spellIcon.src = "holy-power/single/4-full.png";
            
            spellIconContainer.appendChild(spellIcon);
            console.log(spellIconContainer)
            spellCell.appendChild(spellIconContainer);
            gridRow.appendChild(spellCell);

            const playerAurasCell = createElement("div", "priority-grid-player-auras-cell priority-grid-cell", null);
            playerAurasCell.textContent = "a";
            gridRow.appendChild(playerAurasCell);

            const resourcesCell = createElement("div", "priority-grid-resources-cell priority-grid-cell", null);
            resourcesCell.textContent = `${timestampData.resources.holy_power} ${timestampData.resources.mana}`
            gridRow.appendChild(resourcesCell);

            const targetCell = createElement("div", "priority-grid-target-cell priority-grid-cell", null);
            const targetAurasCell = createElement("div", "priority-grid-target-auras-cell priority-grid-cell", null);

            for (const target in timestampData.target_active_auras) {
                // console.log(target)
                // console.log(timestampData.target_active_auras[target])
            };

            gridRow.appendChild(targetCell);
            gridRow.appendChild(targetAurasCell);

            gridContainer.appendChild(gridRow);
            
        };
        return gridContainer;
    };

    const gridHeaders = ["Time", "Priority", "Spell", "Player Auras", "Resources", "Target", "Target Auras"];
    const priorityGrid = createPriorityGrid(priorityData, priorityBreakdownContainer, gridHeaders);
    priorityBreakdownContainer.appendChild(priorityGrid);
};

export { createPriorityBreakdown };