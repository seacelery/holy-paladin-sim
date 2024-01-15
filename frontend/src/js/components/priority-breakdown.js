import { createElement } from "./index.js";
import { spellToIconsMap } from '../utils/spell-to-icons-map.js';
import { buffsToIconsMap } from "../utils/buffs-to-icons-map.js";

const createPriorityBreakdown = (simulationData, containerCount) => {
    const formatTime = (seconds) => {
        let minutes = Math.floor(seconds / 60);
        let remainingSeconds = Math.round(seconds % 60);

        if (remainingSeconds === 60) {
            minutes += 1;
            remainingSeconds = 0;
        };
    
        return `${minutes}:${String(remainingSeconds).padStart(2, '0')}`;
    };

    const setupAuraOverlay = (overlayElement, currentDuration, totalDuration) => {
        const percentage = 100 - (currentDuration / totalDuration) * 100;
        overlayElement.style.background = `conic-gradient(rgba(0, 0, 0, 0.5) ${percentage}%, transparent ${percentage}%)`;
    };

    const setupCooldownOverlay = (overlayElement, remainingCooldown, baseCooldown) => {
        const percentage = 100 - (remainingCooldown / baseCooldown) * 100;
        overlayElement.style.background = `conic-gradient(rgba(0, 0, 0, 0.5) ${percentage}%, transparent ${percentage}%)`;
    };

    const priorityData = simulationData.results.priority_breakdown;
    console.log(priorityData)
    const priorityBreakdownContainer = document.getElementById(`priority-breakdown-table-container-${containerCount}`);

    // create filter options
    const cooldownFilter = createElement("div", "priority-grid-cooldown-filter");

    const cooldownFilterButton = createElement("div", "priority-grid-cooldown-filter-button", "priority-grid-cooldown-filter-button");
    const cooldownFilterIcon = createElement("i", "priority-grid-cooldown-filter-icon fa-regular fa-hourglass", "priority-grid-cooldown-filter-icon");
    cooldownFilterButton.appendChild(cooldownFilterIcon);

    cooldownFilter.appendChild(cooldownFilterButton);

    // create the grid
    const createPriorityGrid = (data, container, headers) => {
        const gridContainer = createElement("div", "priority-grid-container", `priority-grid-container`);

        // generate header row
        const gridHeaderRow = createElement("div", "priority-grid-header-row", null);
        headers.forEach(header => {
            const headerCell = createElement("div", "priority-grid-header-cell priority-grid-cell", null);
            headerCell.textContent = header;
            gridHeaderRow.appendChild(headerCell);

            if (headerCell.textContent === "Cooldowns") {
                // convert to jquery object for popover
                headerCell.appendChild(cooldownFilter);
            };
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

            const holyPowerDisplay = createElement("img", "priority-grid-holy-power-display");
            holyPowerDisplay.src = `holy-power/holy-power-${timestampData.resources.holy_power}.png`;
            resourcesCell.appendChild(holyPowerDisplay);

            const manaBarContainer = createElement("div", "priority-grid-mana-bar-container", null);
            const manaBar = createElement("progress", "priority-grid-mana-bar", null);
            manaBar.max = 1;
            manaBar.value = timestampData.resources.mana / simulationData.simulation_details.max_mana;
            manaBarContainer.appendChild(manaBar);

            const manaText = createElement("div", "priority-grid-mana-text", null);
            manaText.textContent = `${timestampData.resources.mana}`;
            // percent option
            // manaText.textContent = `${Math.round(timestampData.resources.mana / simulationData.simulation_details.max_mana * 100)}%`;
            manaBarContainer.appendChild(manaText);
            
            resourcesCell.appendChild(manaBarContainer);
            gridRow.appendChild(resourcesCell);

            const playerAurasCell = createElement("div", "priority-grid-player-auras-cell priority-grid-cell", null);
            const playerAurasContainer = createElement("div", "priority-grid-player-auras-container", null);
            const playerAuras = timestampData.player_active_auras;
            for (const aura in playerAuras) {                
                // create an icon for each aura and show duration & stacks
                const auraIconContainer = createElement("div", "priority-grid-aura-icon-container", null);

                // create an overlay for each icon, going clockwise
                const iconOverlayContainer = createElement("div", "aura-icon-overlay-container", null);
                const auraOverlay = createElement("div", "aura-duration-overlay", null);
                setupAuraOverlay(auraOverlay, playerAuras[aura].duration, playerAuras[aura].applied_duration);

                const auraIcon = createElement("img", "priority-grid-aura-icon", null);
                auraIcon.src = buffsToIconsMap[aura];

                const auraDurationText = createElement("div", "priority-grid-aura-duration-text", null);
                if (playerAuras[aura].duration < 1000) {
                    auraDurationText.textContent = playerAuras[aura].duration.toFixed(1);
                };
                
                const auraStacksText = createElement("div", "priority-grid-aura-stacks-text", null);
                if (playerAuras[aura].stacks > 1) {
                    auraStacksText.textContent = playerAuras[aura].stacks;
                };

                iconOverlayContainer.appendChild(auraIcon);
                iconOverlayContainer.appendChild(auraOverlay);

                auraIconContainer.appendChild(iconOverlayContainer);
                auraIconContainer.appendChild(auraStacksText);
                auraIconContainer.appendChild(auraDurationText);
                playerAurasContainer.appendChild(auraIconContainer);
            };

            playerAurasCell.appendChild(playerAurasContainer);
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
            const cooldownsContainer = createElement("div", "priority-grid-cooldowns-container", null);
            const cooldowns = timestampData.remaining_cooldowns;

            const generatorRow = createElement("div", "priority-grid-cooldown-row", null);
            const majorCooldownRow = createElement("div", "priority-grid-cooldown-row", null);

            const generatorRowOrder = ["Holy Shock", "Judgment", "Crusader Strike", "Hammer of Wrath"];
            const majorCooldownRowOrder = ["Avenging Wrath", "Daybreak", "Divine Toll", "Tyr's Deliverance", "Blessing of the Seasons", "Divine Favor",];

            let cooldownsPopoverHTML = "";

            generatorRowOrder.forEach(cooldownName => {
                if (cooldowns[cooldownName]) {
                    const cooldown = cooldowns[cooldownName];
                    const formattedCooldownName = cooldownName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                    const cooldownIconContainer = createElement("div", `priority-grid-cooldown-icon-container-${formattedCooldownName}-${containerCount}`, `priority-grid-cooldown-icon-container-${formattedCooldownName}`);

                    const iconOverlayContainer = createElement("div", "cooldown-icon-overlay-container", null);
                    const cooldownOverlay = createElement("div", "cooldown-remaining-overlay", null);
                    setupCooldownOverlay(cooldownOverlay, cooldown.remaining_cooldown, cooldown.base_cooldown);
    
                    const cooldownIcon = createElement("img", "priority-grid-cooldown-icon", null);
                    cooldownIcon.src = spellToIconsMap[cooldownName];
                    cooldownsPopoverHTML += `<div class="priority-grid-cooldown-popover-icon-container" data-cooldown="${formattedCooldownName}">
                                                <img class="priority-grid-cooldown-icon" src="${spellToIconsMap[cooldownName]}"></img>
                                             </div>`;
    
                    const cooldownRemainingText = createElement("div", "priority-grid-cooldown-remaining-text", null);
                    cooldownRemainingText.textContent = cooldown.remaining_cooldown > 0 ? cooldown.remaining_cooldown.toFixed(1) : '';
    
                    iconOverlayContainer.appendChild(cooldownIcon);
                    iconOverlayContainer.appendChild(cooldownOverlay);
                    cooldownIconContainer.appendChild(iconOverlayContainer);
                    cooldownIconContainer.appendChild(cooldownRemainingText);
                    generatorRow.appendChild(cooldownIconContainer);
                };
            });
    
            majorCooldownRowOrder.forEach(cooldownName => {
                if (cooldowns[cooldownName]) {
                    const cooldown = cooldowns[cooldownName];
                    const formattedCooldownName = cooldownName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                    const cooldownIconContainer = createElement("div", `priority-grid-cooldown-icon-container-${formattedCooldownName}-${containerCount}`, `priority-grid-cooldown-icon-container-${formattedCooldownName}`);
                    const iconOverlayContainer = createElement("div", "cooldown-icon-overlay-container", null);
                    const cooldownOverlay = createElement("div", "cooldown-remaining-overlay", null);
                    setupCooldownOverlay(cooldownOverlay, cooldown.remaining_cooldown, cooldown.base_cooldown);
    
                    const cooldownIcon = createElement("img", "priority-grid-cooldown-icon", null);
                    cooldownIcon.src = spellToIconsMap[cooldownName];
                    cooldownsPopoverHTML += `<div class="priority-grid-cooldown-popover-icon-container" data-cooldown="${formattedCooldownName}">
                                                <img class="priority-grid-cooldown-icon" src="${spellToIconsMap[cooldownName]}"></img>
                                             </div>`;
    
                    const cooldownRemainingText = createElement("div", "priority-grid-cooldown-remaining-text", null);
                    cooldownRemainingText.textContent = cooldown.remaining_cooldown > 0 ? formatTime(cooldown.remaining_cooldown) : '';
    
                    iconOverlayContainer.appendChild(cooldownIcon);
                    iconOverlayContainer.appendChild(cooldownOverlay);
                    cooldownIconContainer.appendChild(iconOverlayContainer);
                    cooldownIconContainer.appendChild(cooldownRemainingText);
                    majorCooldownRow.appendChild(cooldownIconContainer);
                };
            });

            // add popover with the accumulated html
            $(cooldownFilterButton).popover({
                html: true,
                content: cooldownsPopoverHTML,
                placement: "right",
                sanitize: false,
            });

            cooldownsContainer.appendChild(generatorRow);
            cooldownsContainer.appendChild(majorCooldownRow);
            cooldownsCell.appendChild(cooldownsContainer);
            gridRow.appendChild(cooldownsCell);
    
            gridContainer.appendChild(gridRow);
        };
        return gridContainer;
    };

    $(document).on("click", ".priority-grid-cooldown-popover-icon-container", function(e) {
        const cooldownName = $(this).attr('data-cooldown');
        console.log(cooldownName)

        console.log(`priority-grid-cooldown-icon-container-${cooldownName}-${containerCount}`)
        const iconsToHide = document.querySelectorAll(`.priority-grid-cooldown-icon-container-${cooldownName}-${containerCount}`);
        console.log(iconsToHide)
        iconsToHide.forEach(icon => {
            icon.style.display = icon.style.display === "none" ? "block" : "none";
        });
    });

    const gridHeaders = ["Time", "Priority", "Spell", "Resources", "Player Auras", "Target Auras", "Cooldowns"];
    const priorityGrid = createPriorityGrid(priorityData, priorityBreakdownContainer, gridHeaders);
    priorityBreakdownContainer.appendChild(priorityGrid);
};

export { createPriorityBreakdown };