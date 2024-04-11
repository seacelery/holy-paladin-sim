import { buffsToIconsMap } from "../utils/buffs-to-icons-map.js";
import { formatThousands, formatTime, createElement } from './index.js';

const createCooldownsBreakdown = (simulationData, containerCount) => {
    const cooldownsData = simulationData.results.cooldowns_breakdown;

    const displayContainer = document.getElementById(`cooldowns-breakdown-table-container-${containerCount}`);
    displayContainer.innerHTML = "";
    displayContainer.style.display = "flex";

    const cooldownsContainer = createElement("div", "cooldowns-breakdown-container", null);
    displayContainer.appendChild(cooldownsContainer);

    const createCooldownsDisplay = (cooldownsData) => {
        const checkboxes =  document.querySelectorAll(".cooldown-tracking-checkbox");
        let isChecked = false;
        checkboxes.forEach(checkbox => {
            if (checkbox.checked && checkbox.parentElement.style.display !== "none") {
                isChecked = true;
            };
        });

        if (!isChecked) {
            const container = createElement("div", "no-cooldowns-tracked-container", null);
            container.textContent = "No cooldowns are being tracked.";
            cooldownsContainer.appendChild(container);
            return;
        } else if (Object.keys(cooldownsData).length === 0) {
            const container = createElement("div", "no-cooldowns-tracked-container", null);
            container.textContent = "No cooldowns are available to be tracked.";
            cooldownsContainer.appendChild(container);
            return;
        };
        
        // display each cooldown
        for (const cooldownName in cooldownsData) {
            const formattedCooldownName = cooldownName.toLowerCase().replace(/\s+/g, "-").replace(/\(|\)/g, "");
            const checkboxId = `cooldown-tracking-${formattedCooldownName}-checkbox`;

            const checkbox = document.getElementById(checkboxId);

            if (!checkbox.checked) {
                continue;
            };

            const cooldownData = cooldownsData[cooldownName];

            const cooldownContainer = createElement("div", "cooldowns-breakdown-cooldown-container", null);

            // add the cooldown icon
            const cooldownIconContainer = createElement("div", "cooldowns-breakdown-cooldown-icon-container", null);
            const cooldownIcon = createElement("img", "cooldowns-breakdown-cooldown-icon", null);
            cooldownIcon.src = buffsToIconsMap[cooldownName];
            cooldownIconContainer.appendChild(cooldownIcon);
            cooldownContainer.appendChild(cooldownIconContainer);

            const cooldownNameAndInstancesContainer = createElement("div", "cooldowns-breakdown-cooldown-name-and-instances-container", null);
            cooldownContainer.appendChild(cooldownNameAndInstancesContainer)
            // add the cooldown name
            const cooldownNameText = createElement("div", "cooldowns-breakdown-cooldown-name-text", null);
            cooldownNameText.textContent = cooldownName;
            cooldownNameAndInstancesContainer.appendChild(cooldownNameText);

            // display the data for each instance of the cooldown
            for (const cooldownInstance in cooldownData) {
                const cooldownInstanceData = cooldownData[cooldownInstance];

                const cooldownInstanceContainer = createElement("div", "cooldowns-breakdown-cooldown-instance-container", null);

                const cooldownInstanceText = createElement("div", "cooldowns-breakdown-cooldown-instance-text", null);
                cooldownInstanceText.textContent = cooldownInstance;
                cooldownInstanceContainer.appendChild(cooldownInstanceText);

                const timestamps = `Time<br>${formatTime((Math.floor(cooldownInstanceData.start_time * 10) / 10).toFixed(1))}-${formatTime((Math.round(cooldownInstanceData.end_time * 10) / 10).toFixed(1))}`;
                const timestampsText = createElement("div", "cooldowns-breakdown-cooldown-average-duration-text", null);
                timestampsText.innerHTML = timestamps;
                cooldownInstanceContainer.appendChild(timestampsText);

                const HPS = `HPS<br><span style="color: var(--healing-font)">${formatThousands(Math.round(cooldownInstanceData.hps))}</span>`;
                const HPSText = createElement("div", "cooldowns-breakdown-cooldown-hps-text", null);
                HPSText.innerHTML = HPS;
                cooldownInstanceContainer.appendChild(HPSText);

                const averageDuration = `Duration<br>${(Math.ceil(cooldownInstanceData.total_duration * 10) / 10).toFixed(1)}s`;
                const averageDurationText = createElement("div", "cooldowns-breakdown-cooldown-average-duration-text", null);
                averageDurationText.innerHTML = averageDuration;
                cooldownInstanceContainer.appendChild(averageDurationText);

                cooldownNameAndInstancesContainer.appendChild(cooldownInstanceContainer);
            };

            cooldownsContainer.appendChild(cooldownContainer);
        };
    };

    createCooldownsDisplay(cooldownsData);
};

export { createCooldownsBreakdown };
