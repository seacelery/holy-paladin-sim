import { createElement, formatNumbers, formatTime } from "./index.js";
import { spellToIconsMap } from '../utils/spell-to-icons-map.js';
import { buffsToIconsMap } from "../utils/buffs-to-icons-map.js";
import { cooldownFilterState } from './index.js';
import { playerAurasFilterState } from './index.js';

const createPriorityBreakdown = (simulationData, containerCount) => {
    const formatPriorityTime = (seconds) => {
        let minutes = Math.floor(seconds / 60);
        let remainingSeconds = (seconds % 60).toFixed(2);
    
        if (remainingSeconds === 60) {
            minutes += 1;
            remainingSeconds = 0;
        };

        if (remainingSeconds < 10) {
            return `${minutes}:0${String(remainingSeconds).padStart(2, '0')}`;
        } else if (remainingSeconds >= 10) {
            return `${minutes}:${String(remainingSeconds).padStart(2, '0')}`;
        };
    };

    // aura overlay starts from nothing and fills clockwise
    const setupAuraOverlay = (overlayElement, currentDuration, totalDuration) => {
        const percentage = 100 - (currentDuration / totalDuration) * 100;
        overlayElement.style.background = `conic-gradient(rgba(0, 0, 0, 0.5) ${percentage}%, transparent ${percentage}%)`;
    };

    // cooldown overlay should start with the full overlay present but needs to be mirrored to unfill clockwise
    const setupCooldownOverlay = (overlayElement, remainingCooldown, baseCooldown) => {
        const percentage = (remainingCooldown / baseCooldown) * 100;
        overlayElement.style.background = `conic-gradient(rgba(0, 0, 0, 0.5) ${percentage}%, transparent ${percentage}%)`;
        overlayElement.style.transform = "scaleX(-1)";
    };

    const priorityData = simulationData.results.priority_breakdown;
    const priorityBreakdownContainer = document.getElementById(`priority-breakdown-table-container-${containerCount}`);

    // create filter options

    // player auras filter
    const playerAurasFilter = createElement("div", "priority-grid-player-auras-filter", null);
    const playerAurasFilterModal = createElement("div", "priority-grid-player-auras-filter-modal", null);

    const playerAurasFilterButton = createElement("div", "priority-grid-player-auras-filter-button", "priority-grid-player-auras-filter-button", null);
    const playerAurasFilterIcon = createElement("i", "priority-grid-player-auras-filter-icon fa-solid fa-wand-sparkles", "priority-grid-player-auras-filter-icon", null);
    playerAurasFilterButton.appendChild(playerAurasFilterIcon);
    playerAurasFilterButton.addEventListener("click", (e) => {
        playerAurasFilterModal.style.opacity = playerAurasFilterModal.style.opacity === "0" ? "1" : "0";
        playerAurasFilterModal.classList.toggle("modal-active");
    });

    playerAurasFilter.appendChild(playerAurasFilterModal);
    playerAurasFilter.appendChild(playerAurasFilterButton);

    // hardcode the order & excluded auras and track the auras present in the current simulation
    const excludedAuras = [
        "Arcane Intellect", "Mark of the Wild", "Buzzing Rune", "Howling Rune", "Chirping Rune", "Hissing Rune",
        "Phial of Tepid Versatility", "Phial of Elemental Chaos", "Iced Phial of Corrupting Rage", "Draconic Augment Rune",
        "Grand Banquet of the Kalu'ak", "Timely Demise", "Filet of Fangs", "Seamoth Surprise", "Salt-Baked Fishcake",
        "Feisty Fish Sticks", "Aromatic Seafood Platter", "Sizzling Seafood Medley", "Revenge, Served Cold",
        "Thousandbone Tongueslicer", "Great Cerulean Sea", "Pip's Emerald Friendship Badge", "Elemental Lariat",
        "Close to Heart", "Allied Wristguards of Companionship", "Potion Absorption Inhibitor", "Saved by the Light",
        "Retribution Aura ", "Source of Magic", "Symbol of Hope", "Mana Spring Totem", "Ominous Chromatic Essence",
        "Magazine of Healing Darts", "Bronzed Grip Wrappings", "Incarnate's Mark of Fire", "Mana Tide Totem",
        "Flask of Saving Graces", "Flask of Tempered Aggression", "Flask of Tempered Swiftness",
        "Flask of Tempered Mastery", "Flask of Tempered Versatility", "Flask of Alchemical Chaos",
        "Algari Mana Oil", "Oil of Beledar's Grace", "Crystallized Augment Rune"
    ];
    const playerAurasModalIconOrder = [
        "Avenging Wrath", "Blessing of Dawn", "Blessing of Dusk", "Infusion of Light", "Divine Purpose", 
        "Tyr's Deliverance (self)", "Blessing of Summer", "Blessing of Autumn", "Blessing of Winter", "Blessing of Spring",
        "Rising Sunlight", "First Light", "Divine Favor", "Awakening", "Awakening Ready"
    ];
    const currentSimulationPlayerAuras = [];

    for (const timestamp in priorityData) {
        const playerAurasData = priorityData[timestamp].player_active_auras;

        // overlapping buff case, generalise if needed
        let solarGraceCount = 0;
        let solarGraceHighestDuration = 0;
        for (let aura in playerAurasData) {
            if (aura.includes("Solar Grace ")) { 
                solarGraceCount += 1;
                if (playerAurasData[aura].duration > solarGraceHighestDuration) {
                    solarGraceHighestDuration = playerAurasData[aura].duration;
                };
                delete playerAurasData[aura];
            };
        };
        playerAurasData["Solar Grace"] = {"applied_duration": 12, "duration": solarGraceHighestDuration, "stacks": solarGraceCount};
        
        let surekiZealotsInsigniaCount = 0;
        let surekiZealotsInsigniaHighestDuration = 0;
        for (let aura in playerAurasData) {
            if (aura.includes("Sureki Zealot's Insignia ")) { 
                surekiZealotsInsigniaCount += 1;
                if (playerAurasData[aura].duration > surekiZealotsInsigniaHighestDuration) {
                    surekiZealotsInsigniaHighestDuration = playerAurasData[aura].duration;
                };
                delete playerAurasData[aura];
            };
        };
        playerAurasData["Sureki Zealot's Insignia"] = {"applied_duration": 12, "duration": surekiZealotsInsigniaHighestDuration, "stacks": surekiZealotsInsigniaCount};

        let araKaraSacbroodCount = 0;
        let araKaraSacbroodHighestDuration = 0;
        for (let aura in playerAurasData) {
            if (aura.includes("Ara-Kara Sacbrood ")) { 
                araKaraSacbroodCount += 1;
                if (playerAurasData[aura].duration > araKaraSacbroodHighestDuration) {
                    araKaraSacbroodHighestDuration = playerAurasData[aura].duration;
                };
                delete playerAurasData[aura];
            };
        };
        playerAurasData["Ara-Kara Sacbrood"] = {"applied_duration": 60, "duration": araKaraSacbroodHighestDuration, "stacks": araKaraSacbroodCount};

        for (const auraName in playerAurasData) {
            if (excludedAuras.includes(auraName)) {
                continue;
            };

            if (!playerAurasModalIconOrder.includes(auraName)) {
                playerAurasModalIconOrder.push(auraName);      
            };

            if (!currentSimulationPlayerAuras.includes(auraName)) {
                currentSimulationPlayerAuras.push(auraName);
            };  
        };
    };

    // create the player auras modal
    const playerAurasModalContainer = createElement("div", `priority-grid-player-auras-modal-container`, null);
    playerAurasModalIconOrder.forEach(auraName => {
        if (currentSimulationPlayerAuras.includes(auraName)) {
            const formattedAuraName = auraName.toLowerCase().replaceAll(" (self)", "").replaceAll(" ", "-").replaceAll("'", "");
            const playerAurasModalIconContainer = createElement("div", `priority-grid-player-auras-modal-icon-container-${formattedAuraName}`, null);
            const playerAurasModalIcon = createElement("img", "priority-grid-player-auras-modal-icon", null);
            playerAurasModalIcon.src = buffsToIconsMap[auraName];
            playerAurasModalIconContainer.appendChild(playerAurasModalIcon);
            playerAurasModalIconContainer.addEventListener("click", () => {
                const isVisible = playerAurasModalIconContainer.style.filter !== "grayscale(1)";
                playerAurasModalIconContainer.style.filter = isVisible ? "grayscale(1)" : "grayscale(0)";

                playerAurasFilterState[formattedAuraName] = !isVisible;
            
                const playerAurasIconsToHide = document.querySelectorAll(`.priority-grid-player-auras-icon-container-${formattedAuraName}`);
                playerAurasIconsToHide.forEach(icon => {
                    icon.style.display = isVisible ? "none" : "block";
                });      
                
                const playerAurasModalIconsToDim = document.querySelectorAll(`.priority-grid-player-auras-modal-icon-container-${formattedAuraName}`);
                playerAurasModalIconsToDim.forEach(icon => {
                    icon.style.filter = isVisible ? "grayscale(1)" : "grayscale(0)";
                });
            });
            playerAurasModalContainer.appendChild(playerAurasModalIconContainer);
        };
    });      
    playerAurasFilterModal.appendChild(playerAurasModalContainer);

    // cooldown filter
    const cooldownFilter = createElement("div", "priority-grid-cooldown-filter", null);
    const cooldownFilterModal = createElement("div", "priority-grid-cooldown-filter-modal", null);
    
    const cooldownFilterButton = createElement("div", "priority-grid-cooldown-filter-button", "priority-grid-cooldown-filter-button", null);
    const cooldownFilterIcon = createElement("i", "priority-grid-cooldown-filter-icon fa-regular fa-hourglass", "priority-grid-cooldown-filter-icon", null);
    cooldownFilterButton.appendChild(cooldownFilterIcon);
    cooldownFilterButton.addEventListener("click", (e) => {
        cooldownFilterModal.style.opacity = cooldownFilterModal.style.opacity === "0" ? "1" : "0";
        cooldownFilterModal.classList.toggle("modal-active");
    });

    cooldownFilter.appendChild(cooldownFilterModal);
    cooldownFilter.appendChild(cooldownFilterButton);

    // hardcode the order and exclude certain spells
    const cooldownModalIconOrder = ["Holy Shock", "Judgment", "Crusader Strike", "Avenging Wrath", "Daybreak", 
                                    "Divine Toll", "Tyr's Deliverance", "Blessing of the Seasons", "Divine Favor"];
    const excludedCooldowns = ["Flash of Light", "Holy Light", "Word of Glory", "Light of Dawn", "Wait", "Potion"]

    for (const timestamp in priorityData) {
        const cooldownsData = priorityData[timestamp].remaining_cooldowns;
        for (const cooldownName in cooldownsData) {
            if (!cooldownModalIconOrder.includes(cooldownName) && !excludedCooldowns.includes(cooldownName)) {
                cooldownModalIconOrder.push(cooldownName);      
            };
        };
    };

    // create the cooldowns modal
    cooldownModalIconOrder.forEach(cooldownName => {
        const formattedCooldownName = cooldownName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
        const cooldownModalIconContainer = createElement("div", `priority-grid-cooldown-modal-icon-container-${formattedCooldownName}`, null);
        const cooldownModalIcon = createElement("img", "priority-grid-cooldown-modal-icon", null);
        cooldownModalIcon.src = spellToIconsMap[cooldownName];
        cooldownModalIconContainer.appendChild(cooldownModalIcon);
        cooldownModalIconContainer.addEventListener("click", () => {
            const isVisible = cooldownModalIconContainer.style.filter !== "grayscale(1)";
            cooldownModalIconContainer.style.filter = isVisible ? "grayscale(1)" : "grayscale(0)";

            cooldownFilterState[formattedCooldownName] = !isVisible;
        
            const cooldownIconsToHide = document.querySelectorAll(`.priority-grid-cooldown-icon-container-${formattedCooldownName}`);
            cooldownIconsToHide.forEach(icon => {
                icon.style.display = isVisible ? "none" : "block";
            });      
            
            const cooldownModalIconsToDim = document.querySelectorAll(`.priority-grid-cooldown-modal-icon-container-${formattedCooldownName}`);
            cooldownModalIconsToDim.forEach(icon => {
                icon.style.filter = isVisible ? "grayscale(1)" : "grayscale(0)";
            });
        });
        cooldownFilterModal.appendChild(cooldownModalIconContainer);
    });          
    
    // create the grid
    const createPriorityGrid = (data, container, headers) => {
        const rowHeight = 113;
        // extra rows to generate below viewport
        const buffer = 9;
        const timestamps = Object.keys(priorityData);

        const headerGridContainer = createElement("div", "priority-header-grid-container", null);
        const gridContainer = createElement("div", "priority-grid-container", `priority-grid-container`);
        gridContainer.style.height = "100vh";
        gridContainer.style.overflowY = "scroll";

        // generate header row
        const gridHeaderRow = createElement("div", "priority-grid-header-row", null);
        headers.forEach(header => {
            const headerCell = createElement("div", "priority-grid-header-cell priority-grid-cell", null);
            headerCell.textContent = header;
            gridHeaderRow.appendChild(headerCell);

            if (headerCell.textContent === "Player Auras") {
                headerCell.appendChild(playerAurasFilter);
            };

            if (headerCell.textContent === "Cooldowns") {
                headerCell.appendChild(cooldownFilter);
            };
        });
        headerGridContainer.appendChild(gridHeaderRow);

        // create each row to be added while scrolling
        const createRow = (timestamp) => {
            if (!timestamp) return null;

            const timestampData = priorityData[timestamp];

            const gridRow = createElement("div", "priority-grid-row", null);

            const timeCell = createElement("div", "priority-grid-time-cell priority-grid-cell", null);
            timeCell.textContent = formatPriorityTime(timestamp);
            gridRow.appendChild(timeCell);

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
            manaText.textContent = `${formatNumbers(timestampData.resources.mana)}`;
            // percent option
            // manaText.textContent = `${Math.round(timestampData.resources.mana / simulationData.simulation_details.max_mana * 100)}%`;
            manaBarContainer.appendChild(manaText);
            
            resourcesCell.appendChild(manaBarContainer);
            gridRow.appendChild(resourcesCell);

            const playerAurasCell = createElement("div", "priority-grid-player-auras-cell priority-grid-cell", null);
            const playerAurasContainer = createElement("div", "priority-grid-player-auras-container", null);
            const playerAuras = timestampData.player_active_auras;

            for (let aura in playerAuras) {  
                if (!currentSimulationPlayerAuras.includes(aura)) {
                    continue;
                };  

                if (playerAuras[aura].stacks === 0) {
                    continue;
                };
   
                const formattedAuraName = aura.toLowerCase().replaceAll(" (self)", "").replaceAll(" ", "-").replaceAll("'", "");
                // create an icon for each aura and show duration & stacks
                const auraIconContainer = createElement("div", `priority-grid-player-auras-icon-container-${formattedAuraName}`, null);

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

            const targetAurasCell = createElement("div", "priority-grid-target-auras-cell priority-grid-cell", null);
            const targetAurasContainer = createElement("div", "priority-grid-player-auras-container", null);
            const targets = timestampData.target_active_auras;           
            for (const target in targets) {
                const targetAuras = targets[target];
                for (const aura in targetAuras) {                
                    const formattedAuraName = aura.toLowerCase().replaceAll(" (self)", "").replaceAll(" ", "-").replaceAll("'", "");
                    // create an icon for each aura and show duration & stacks
                    const auraIconContainer = createElement("div", `priority-grid-player-auras-icon-container-${formattedAuraName}`, null);
    
                    // create an overlay for each icon, going clockwise
                    const iconOverlayContainer = createElement("div", "aura-icon-overlay-container", null);
                    const auraOverlay = createElement("div", "aura-duration-overlay", null);
                    setupAuraOverlay(auraOverlay, targetAuras[aura].duration, targetAuras[aura].applied_duration);
    
                    const auraIcon = createElement("img", "priority-grid-aura-icon", null);
                    auraIcon.src = buffsToIconsMap[aura];
    
                    const auraDurationText = createElement("div", "priority-grid-aura-duration-text", null);
                    if (targetAuras[aura].duration < 1000) {
                        auraDurationText.textContent = targetAuras[aura].duration.toFixed(1);
                    };
                    
                    const auraStacksText = createElement("div", "priority-grid-aura-stacks-text", null);
                    if (targetAuras[aura].stacks > 1) {
                        auraStacksText.textContent = targetAuras[aura].stacks;
                    };
    
                    iconOverlayContainer.appendChild(auraIcon);
                    iconOverlayContainer.appendChild(auraOverlay);
    
                    auraIconContainer.appendChild(iconOverlayContainer);
                    auraIconContainer.appendChild(auraStacksText);
                    auraIconContainer.appendChild(auraDurationText);
                    targetAurasContainer.appendChild(auraIconContainer);
                }; 
            };         
            targetAurasCell.appendChild(targetAurasContainer);        
            gridRow.appendChild(targetAurasCell);

            const cooldownsCell = createElement("div", "priority-grid-cooldowns-cell priority-grid-cell", null);
            const cooldownsContainer = createElement("div", "priority-grid-cooldowns-container", null);
            const cooldowns = timestampData.remaining_cooldowns;

            const generatorRow = createElement("div", "priority-grid-cooldown-row", null);
            const majorCooldownRow = createElement("div", "priority-grid-cooldown-row", null);

            // select the order for each row
            const generatorRowOrder = ["Holy Shock", "Judgment", "Crusader Strike", "Hammer of Wrath", "Consecration", "Beacon of Virtue"];
            const majorCooldownRowOrder = ["Avenging Wrath", "Daybreak", "Divine Toll", "Tyr's Deliverance",
                                           "Light's Hammer", "Holy Prism", "Barrier of Faith", "Blessing of the Seasons", 
                                           "Divine Favor", "Lay on Hands", "Arcane Torrent", "Fireblood", "Gift of the Naaru", 
                                           "Aerated Mana Potion", "Elemental Potion of Ultimate Power"];

            // only append if the cooldown is actually present in the current simulation
            generatorRowOrder.forEach(cooldownName => {
                if (cooldowns[cooldownName]) {
                    const cooldown = cooldowns[cooldownName];
                    const formattedCooldownName = cooldownName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                    const cooldownIconContainer = createElement("div", `priority-grid-cooldown-icon-container-${formattedCooldownName}`, `priority-grid-cooldown-icon-container-${formattedCooldownName}`);

                    const iconOverlayContainer = createElement("div", "cooldown-icon-overlay-container", null);
                    const cooldownOverlay = createElement("div", "cooldown-remaining-overlay", null);
                    setupCooldownOverlay(cooldownOverlay, cooldown.remaining_cooldown, cooldown.base_cooldown);
    
                    const cooldownIcon = createElement("img", "priority-grid-cooldown-icon", null);
                    cooldownIcon.src = spellToIconsMap[cooldownName];
                    // set to greyscale if the spell is on cooldown
                    if (cooldown.remaining_cooldown > 0 && cooldown.current_charges < 1) {
                        cooldownIcon.style.filter = "grayscale(1)";
                    };
    
                    const cooldownRemainingText = createElement("div", "priority-grid-cooldown-remaining-text", null);
                    cooldownRemainingText.textContent = cooldown.remaining_cooldown > 0 ? cooldown.remaining_cooldown.toFixed(1) : '';

                    const cooldownChargesText = createElement("div", "priority-grid-cooldown-charges-text", null);
                    if (cooldown.max_charges > 1) {
                        cooldownChargesText.textContent = cooldown.current_charges;
                    };
    
                    iconOverlayContainer.appendChild(cooldownIcon);
                    iconOverlayContainer.appendChild(cooldownOverlay);
                    cooldownIconContainer.appendChild(iconOverlayContainer);
                    cooldownIconContainer.appendChild(cooldownRemainingText);
                    cooldownIconContainer.appendChild(cooldownChargesText);
                    generatorRow.appendChild(cooldownIconContainer);
                };
            });
    
            majorCooldownRowOrder.forEach(cooldownName => {
                if (cooldowns[cooldownName]) {
                    const temporaryCooldowns = ["Aerated Mana Potion", "Elemental Potion of Ultimate Power"];
                    if (cooldowns[cooldownName].remaining_cooldown === 0 && (temporaryCooldowns.includes(cooldownName))) {
                        return;
                    };

                    const cooldown = cooldowns[cooldownName];
                    if ("Divine Favor" in timestampData.player_active_auras && cooldownName === "Divine Favor") {
                        cooldown.remaining_cooldown = 0;
                    };
                    
                    const formattedCooldownName = cooldownName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "");
                    const cooldownIconContainer = createElement("div", `priority-grid-cooldown-icon-container-${formattedCooldownName}`, `priority-grid-cooldown-icon-container-${formattedCooldownName}`);
                    const iconOverlayContainer = createElement("div", "cooldown-icon-overlay-container", null);
                    const cooldownOverlay = createElement("div", "cooldown-remaining-overlay", null);
                    setupCooldownOverlay(cooldownOverlay, cooldown.remaining_cooldown, cooldown.base_cooldown);
    
                    const cooldownIcon = createElement("img", "priority-grid-cooldown-icon", null);
                    cooldownIcon.src = spellToIconsMap[cooldownName];

                    if (cooldowns[cooldownName].remaining_cooldown > 0) {
                        cooldownIcon.style.filter = "grayscale(1)";
                    };

                    const cooldownRemainingText = createElement("div", "priority-grid-cooldown-remaining-text", null);
                    cooldownRemainingText.textContent = cooldown.remaining_cooldown > 0 ? formatTime(cooldown.remaining_cooldown) : '';

                    const cooldownChargesText = createElement("div", "priority-grid-cooldown-charges-text", null);
                    if (cooldown.max_charges > 1) {
                        cooldownChargesText.textContent = cooldown.current_charges;
                    };
    
                    iconOverlayContainer.appendChild(cooldownIcon);
                    iconOverlayContainer.appendChild(cooldownOverlay);
                    cooldownIconContainer.appendChild(iconOverlayContainer);
                    cooldownIconContainer.appendChild(cooldownRemainingText);
                    cooldownIconContainer.appendChild(cooldownChargesText);
                    majorCooldownRow.appendChild(cooldownIconContainer);
                };
            });

            cooldownsContainer.appendChild(generatorRow);
            cooldownsContainer.appendChild(majorCooldownRow);
            cooldownsCell.appendChild(cooldownsContainer);
            gridRow.appendChild(cooldownsCell);

            const auraCountsCell = createElement("div", "priority-grid-player-auras-cell priority-grid-cell", null);
            const auraCountsContainer = createElement("div", "priority-grid-player-auras-container", null);
            const auraCounts = timestampData.total_target_aura_counts;
            for (const aura in auraCounts) {                
                const formattedAuraName = aura.toLowerCase().replaceAll(" (self)", "").replaceAll(" ", "-").replaceAll("'", "");
                // create an icon for each aura and show duration & stacks
                const auraIconContainer = createElement("div", `priority-grid-player-auras-icon-container-${formattedAuraName}`, null);

                // create an overlay for each icon, going clockwise
                const iconOverlayContainer = createElement("div", "aura-icon-overlay-container", null);
                const auraOverlay = createElement("div", "aura-duration-overlay", null);

                const auraIcon = createElement("img", "priority-grid-aura-icon", null);
                auraIcon.src = buffsToIconsMap[aura];

                const auraCountsText = createElement("div", "priority-grid-aura-counts-text", null);
                auraCountsText.textContent = auraCounts[aura];

                iconOverlayContainer.appendChild(auraIcon);
                iconOverlayContainer.appendChild(auraOverlay);

                auraIconContainer.appendChild(iconOverlayContainer);
                auraIconContainer.appendChild(auraCountsText)
                auraCountsContainer.appendChild(auraIconContainer);
            };

            auraCountsCell.appendChild(auraCountsContainer);
            gridRow.appendChild(auraCountsCell);

            const statsCell = createElement("div", "priority-grid-stats-cell priority-grid-cell", null);
            const statsData = simulationData.results.priority_breakdown[timestamp].current_stats;
            const statsOrder = ["intellect", "haste", "crit", "mastery", "versatility"];
            const sortedStatsData = Object.fromEntries(
                Object.entries(statsData).sort(([a], [b]) => statsOrder.indexOf(a) - statsOrder.indexOf(b))
            );

            for (const stat in sortedStatsData) {
                let statRating, statPercent;
                const statData = sortedStatsData[stat];
                if (stat === "intellect") {
                    statRating = Math.round(statData[stat]);
                } else {
                    statPercent = Number(statData[stat]).toFixed(2);
                    statRating = Math.round(statData[`${stat}_rating`]);
                };

                const statContainer = createElement("div", "priority-grid-stat-container", null);
                const statNameContainer = createElement("span", "priority-grid-stat-container-name", null);
                statNameContainer.textContent = stat.charAt(0).toUpperCase() + stat.slice(1);
                statNameContainer.style.color = `var(--stat-${stat})`;
                const statRatingContainer = createElement("span", "priority-grid-stat-container-rating", null);
                statRatingContainer.textContent = statRating;
                statRatingContainer.style.color = `var(--stat-${stat})`;
                const statDivider = createElement("span", "priority-grid-stat-container-divider", null);
                statDivider.textContent = stat !== "intellect" ? "/" : "";
                statDivider.style.color = `var(--stat-${stat})`;
                const statPercentContainer = createElement("span", "priority-grid-stat-container-percent", null);
                statPercentContainer.textContent = stat !== "intellect" ? statPercent + "%" : "";
                statPercentContainer.style.color = `var(--stat-${stat})`;
                statContainer.append(statNameContainer, statRatingContainer, statDivider, statPercentContainer);
        
                statsCell.appendChild(statContainer);
            };
              
            gridRow.appendChild(statsCell);

            return gridRow
        };

        // create rows from scrolling instead of loading all at once
        const handleScroll = () => {
            const scrollTop = gridContainer.scrollTop;
            const visibleRowCount = Math.ceil(gridContainer.clientHeight / rowHeight);
            const totalRows = timestamps.length;
        
            let startIndex = Math.max(0, Math.floor(scrollTop / rowHeight) - buffer);
            const endIndex = Math.min(totalRows - 1, startIndex + visibleRowCount + buffer);

            if (scrollTop === 0) {
                gridContainer.innerHTML = "";
                currentEndIndex = Math.ceil(gridContainer.clientHeight / rowHeight) + buffer - 1;
                const fragment = document.createDocumentFragment();
                for (let i = 0; i <= currentEndIndex; i++) {
                    const row = createRow(timestamps[i]);
                    if (row) fragment.appendChild(row);
                };
                gridContainer.appendChild(fragment);
                currentStartIndex = 0;
                return;
            };
        
            if (endIndex > currentEndIndex) {
                const fragment = document.createDocumentFragment();
                for (let i = currentEndIndex + 1; i <= endIndex; i++) {
                    const row = createRow(timestamps[i]);
                    if (row) fragment.appendChild(row);
                }
                gridContainer.appendChild(fragment);
                currentEndIndex = endIndex;
            };
        };
        
        let currentStartIndex = 0;
        let currentEndIndex = Math.ceil(gridContainer.clientHeight / rowHeight) + buffer - 1;
        
        // initial rows
        const initialFragment = document.createDocumentFragment();
        for (let i = currentStartIndex; i <= currentEndIndex; i++) {
            const row = createRow(timestamps[i]);
            if (row) initialFragment.appendChild(row);
        }
        gridContainer.appendChild(initialFragment);
        
        gridContainer.addEventListener("scroll", handleScroll);
        headerGridContainer.appendChild(gridContainer);
        return headerGridContainer;
    };

    // close modals when clicked away
    document.addEventListener("click", (e) => {
        const playerAurasTargetClasses = ["priority-grid-player-auras-filter-modal", "priority-grid-player-auras-filter-icon", "priority-grid-player-auras-filter-button",
                                          "priority-grid-player-auras-modal-icon", "priority-grid-player-auras-modal-icon-container"];
        const cooldownsTargetClasses = ["priority-grid-cooldown-filter-modal", "priority-grid-cooldown-filter-icon", "priority-grid-cooldown-filter-button",
                                        "priority-grid-cooldown-modal-icon", "priority-grid-cooldown-modal-icon-container"];
        
        if (!playerAurasTargetClasses.some(className => e.target.classList.contains(className))) {
            playerAurasFilterModal.style.opacity = "0";
            playerAurasFilterModal.classList.remove("modal-active");
        };

        if (!cooldownsTargetClasses.some(className => e.target.classList.contains(className))) {
            cooldownFilterModal.style.opacity = "0";
            cooldownFilterModal.classList.remove("modal-active");
        };
    });

    // choose headers and create the grid
    const gridHeaders = ["Time", "Spell", "Resources", "Player Auras", "Target Auras", "Cooldowns", "Counts", "Stats"];
    const priorityGrid = createPriorityGrid(priorityData, priorityBreakdownContainer, gridHeaders);
    priorityBreakdownContainer.appendChild(priorityGrid);

    // disable icons that are in the global filter lists
    Object.keys(playerAurasFilterState).forEach(auraName => {
        const isVisible = playerAurasFilterState[auraName];
        const icons = document.querySelectorAll(`.priority-grid-player-auras-icon-container-${auraName}`);
        icons.forEach(icon => {
            icon.style.display = isVisible ? "block" : "none";
        });
        const modalIcons = document.querySelectorAll(`.priority-grid-player-auras-modal-icon-container-${auraName}`);
        modalIcons.forEach(icon => {
            icon.style.filter = isVisible ? "grayscale(0)" : "grayscale(1)";
        });
    });

    Object.keys(cooldownFilterState).forEach(cooldownName => {
        const isVisible = cooldownFilterState[cooldownName];
        const icons = document.querySelectorAll(`.priority-grid-cooldown-icon-container-${cooldownName}`);
        icons.forEach(icon => {
            icon.style.display = isVisible ? "block" : "none";
        });
        const modalIcons = document.querySelectorAll(`.priority-grid-cooldown-modal-icon-container-${cooldownName}`);
        modalIcons.forEach(icon => {
            icon.style.filter = isVisible ? "grayscale(0)" : "grayscale(1)";
        });
    });

    // align header with grid rows as size changes
    const syncColumnWidths = () => {
        const headerCells = document.querySelectorAll(".priority-grid-header-row .priority-grid-header-cell");
        const firstRowCells = document.querySelector(".priority-grid-row").children;

        if (firstRowCells.length === headerCells.length) {
            for (let i = 0; i < headerCells.length; i++) {
                headerCells[i].style.width = `${firstRowCells[i].offsetWidth - 0.5}px`;
            };
        };
    };
    // window.addEventListener("resize", syncColumnWidths);
};

export { createPriorityBreakdown };