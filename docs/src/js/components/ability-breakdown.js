import { spellToIconsMap } from '../utils/spell-to-icons-map.js';
import { createHealingLineGraph } from './create-healing-line-graph.js';
import { formatNumbers, formatNumbersNoRounding, createElement } from './index.js';

const createAbilityBreakdown = (simulationData, containerCount) => {    
    const sortTableByColumn = (table, column, asc = true) => {
        if (column !== lastSortedColumn) {
            asc = defaultSortOrders[column] !== undefined ? defaultSortOrders[column] : false;
            lastSortedColumn = column;
        };

        // reset sorting icons display
        table.querySelectorAll(`.sorting-icon-${containerCount}`).forEach(icon => {
            icon.style.display = "none";
        });

        const currentArrowIcon = table.querySelector(`tr:first-child td:nth-child(${column + 1}) i`);
        currentArrowIcon.style.display = "inline-block";
        if (!asc) {
            currentArrowIcon.className = `fa fa-sort-down sorting-icon-${containerCount}`;
        } else {
            currentArrowIcon.className = `fa fa-sort-up sorting-icon-${containerCount}`;
        };

        const dirModifier = asc ? 1 : -1;
        const tBody = table.tBodies[0];
        const totalRow = tBody.querySelector(".total-values-row");
        const totalRowParent = totalRow.parentNode;
    
        // remove total row
        totalRowParent.removeChild(totalRow);
    
        const rows = Array.from(tBody.querySelectorAll(`tr:not(.sub-row-${containerCount}):not(.sub-sub-row-${containerCount})`));
        const allSubRows = Array.from(tBody.querySelectorAll(`.sub-row-${containerCount}`));
        const allSubSubRows = Array.from(tBody.querySelectorAll(`.sub-sub-row-${containerCount}`));
    
        // select the rows
        const sortedRows = rows.sort((a, b) => {
            let aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            let bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
    
            // remove number formatting
            aColText = aColText.replace(/,/g, '');
            bColText = bColText.replace(/,/g, '');
    
            // i'm not really sure but it stops different types from messing it up
            if (!isNaN(parseFloat(aColText)) && !isNaN(parseFloat(bColText))) {
                return dirModifier * (parseFloat(aColText) - parseFloat(bColText));
            } else {
                return dirModifier * aColText.localeCompare(bColText);
            };
        });
    
        // clear the table
        while (tBody.firstChild) {
            tBody.removeChild(tBody.firstChild);
        };
    
        // re-add each row
        sortedRows.forEach(mainRow => {
            tBody.appendChild(mainRow);
    
            // find and append subrows belonging to the parent row
            allSubRows.forEach(subRow => {
                if (subRow.getAttribute("data-parent-row") === mainRow.id) {
                    tBody.appendChild(subRow);
    
                    // find and append sub-subrows belonging to the parent row
                    allSubSubRows.forEach(subSubRow => {
                        if (subSubRow.getAttribute("data-parent-row") === subRow.id) {
                            tBody.appendChild(subSubRow);
                        };
                    });
                };
            });
        });
    
        // add total values back
        tBody.appendChild(totalRow);
    
        // update sorting indicators
        table.querySelectorAll("tr:first-child td").forEach(td => td.classList.remove("td-sort-asc", "td-sort-desc"));
        table.querySelector(`tr:first-child td:nth-child(${column + 1})`).classList.toggle("td-sort-asc", asc);
        table.querySelector(`tr:first-child td:nth-child(${column + 1})`).classList.toggle("td-sort-desc", !asc);
    };
    
    let sortOrder = {};
    let lastSortedColumn = null;
    const defaultSortOrders = {
        0: true
    };

    const changeArrowDirection = (element) => {
        if (element.classList.contains("fa-sort-down")) {
            element.classList.remove("fa-sort-down");
            element.classList.add("fa-caret-right");
        } else if (element.classList.contains("fa-caret-right")) {
            element.classList.remove("fa-caret-right");
            element.classList.add("fa-sort-down");
        };       
    };

    // leave cells blank for certain spells
    // "Blessing of Summer", "Blessing of Autumn", "Blessing of Winter", "Blessing of Spring", 
    const excludedSpells = [
        "Reclamation (Holy Shock)", "Reclamation (Crusader Strike)", "Divine Revelations (Holy Light)", "Divine Revelations (Judgment)", 
        "Aerated Mana Potion", "Tirion's Devotion", "Source of Magic", "Mana Spring Totem", "Symbol of Hope", "Mana Tide Totem"
    ];
    // displays only casts and resource gains
    const excludedSpellsOnlyResourcesAndCasts = [
        "Beacon of Virtue", "Beacon of Faith", "Blessing of the Seasons", "Blessing of Summer", "Blessing of Autumn", "Blessing of Winter", "Blessing of Spring", 
        "Divine Favor", "Avenging Wrath", "Arcane Torrent", "Aerated Mana Potion"
    ];
    // displays casts with average as healing divided by casts
    const excludedSpellsCasts = [
        "Beacon of Light", "Overflowing Light", "Resplendent Light", "Crusader's Reprieve", "Judgment of Light", "Greater Judgment", 
        "Touch of Light", "Afterimage", "Glimmer of Light", "Glimmer of Light (Glistening Radiance (Light of Dawn))",
        "Glimmer of Light (Glistening Radiance (Word of Glory))", "Glimmer of Light (Daybreak)", "Embrace of Akunda", "Holy Reverberation", 
        "Restorative Sands", "Echoing Tyrstone", "Smoldering Seedling", "Blossom of Amirdrassil Large HoT", "Blossom of Amirdrassil Small HoT", 
        "Blossom of Amirdrassil Absorb", "Blossom of Amirdrassil", "Barrier of Faith (Holy Shock)", "Barrier of Faith (Flash of Light)", 
        "Barrier of Faith (Holy Light)", "Leech", "Dreaming Devotion", "Veneration", "Merciful Auras", "Light of the Martyr ", "Saved by the Light",
        "Chirping Rune", "Larodar's Fiery Reverie", "Rashok's Molten Heart", "Magazine of Healing Darts", "Bronzed Grip Wrappings",
        "Dawnlight", "Dawnlight (HoT)", "Dawnlight (AoE)", "Afterimage (Word of Glory)", "Afterimage (Eternal Flame)", "Eternal Flame (HoT)",
        "Broodkeeper's Promise", "Sun Sear", "Sacred Weapon 1", "Sacred Weapon 2", "Authority of Fiery Resolve", "Rite of Adjuration",
        "Avenging Crusader (Judgment)", "Avenging Crusader (Crusader Strike)", "Sun's Avatar", "Divine Guidance", "Hammer and Anvil", "Scrapsinger's Symphony",
        "Siphoning Phylactery Shard", "Creeping Coagulum ", "Gruesome Syringe"
    ];
    // displays casts with average as healing divided by hits
    const excludedSpellsCastsAverageHits = [
        "Gift of the Naaru"
    ];
    const excludedSpellsCrit = [
        "Beacon of Light", "Overflowing Light", "Resplendent Light", "Crusader's Reprieve", "Crusader Strike", "Judgment", "Daybreak", 
        "Divine Toll", "Smoldering Seedling", "Blossom of Amirdrassil Absorb", "Blossom of Amirdrassil", "Lay on Hands", "Leech", "Veneration",
        "Light of the Martyr ", "Saved by the Light", "Dawnlight", "Broodkeeper's Promise", "Sacred Weapon", "Holy Bulwark",
        "Avenging Crusader", "Siphoning Phylactery Shard"
    ];
    const excludedSpellsAverage = [
        "Dawnlight"
    ];

    const tableContainer = document.getElementById(`ability-breakdown-table-container-${containerCount}`);
    tableContainer.innerHTML = "";

    const healingGraphCheckbox = document.getElementById("hide-healing-graph-option");
    if (healingGraphCheckbox.checked) {
        const healingTimelineData = simulationData.results.healing_timeline;
        const manaTimelineData = simulationData.results.mana_timeline;
        const healingGraphContainer = createElement("div", `healing-graph-container-${containerCount}`, `healing-graph-content`);
        const healingGraph = createElement("div", null, `healing-graph`);

        tableContainer.appendChild(healingGraphContainer);
        healingGraphContainer.appendChild(healingGraph);

        createHealingLineGraph(healingTimelineData, manaTimelineData, `#healing-graph-${containerCount}`, "Healing", "var(--healing-font)");
    };
    
    // convert to array and back to sort the data by healing
    const abilityBreakdownData = simulationData.results.ability_breakdown;
    let abilityBreakdownArray = Object.entries(abilityBreakdownData);
    abilityBreakdownArray.sort((a, b) => b[1].total_healing - a[1].total_healing);
    let sortedAbilityBreakdownData = Object.fromEntries(abilityBreakdownArray);

    const encounterLength = simulationData.simulation_details.encounter_length;

    const table = document.createElement("table");

    // headers
    const header = table.createTHead();
    header.id = `table-headers-${containerCount}`;
    const headerRow = header.insertRow(0);
    const headers = ["Spell Name", "%", "Healing", "HPS", "Casts", "Average", "Hits", "Crit %", "Mana Spent", "Holy Power", "CPM", "OH %"];
    headers.forEach((text, index) => {
        const cell = headerRow.insertCell(index);
        cell.textContent = text;

        // format the headers
        if (text.includes("%")) {
            cell.id = `${text.toLowerCase()}-header-${containerCount}`;
            cell.id = cell.id.replaceAll("%", "percent");
        } else {
            cell.id = `${text.toLowerCase()}-header-${containerCount}`;
        };

        if (cell.id.includes(" ")) {
            cell.id = cell.id.replaceAll(" ", "-");
        };

        if (sortOrder[index] === undefined) {
            sortOrder[index] = "asc";
        };
    
        cell.addEventListener("click", (e) => {
            if (e.target.classList.contains("table-header") || e.target.classList.contains(`sorting-icon-${containerCount}`)) {
                const isAscending = sortOrder[index] === "asc";
                sortTableByColumn(table, index, !isAscending);
                sortOrder[index] = isAscending ? "desc" : "asc";
            };        
        });
        
        // header arrow
        cell.className = `table-header`;

        const sortArrowIcon = document.createElement("i");
        sortArrowIcon.classList.add("fa", "fa-sort-down", `sorting-icon-${containerCount}`);
        cell.appendChild(sortArrowIcon);
        sortArrowIcon.style.display = "none";

        if (cell.id === `healing-header-${containerCount}`) {
            sortArrowIcon.style.display = "inline-block";
        };

        if (cell.id === `spell-name-header-${containerCount}`) {
            cell.classList.add("ability-spell-name-header");

            const headerIconContainer = document.createElement("div");
            headerIconContainer.className = "table-header-icon-container";
            const headerIcon = document.createElement("i");
            headerIcon.className = "fa-solid fa-caret-right table-header-arrows";
            headerIcon.id = `table-header-icon-${containerCount}`;

            // expand or collapse all rows on click
            headerIconContainer.addEventListener("click", () => {
                const subRows = document.querySelectorAll(`.sub-row-${containerCount}`);
                const subRowArrows = document.querySelectorAll(`.sub-row-arrows-${containerCount}`);

                const subSubRows = document.querySelectorAll(`.sub-sub-row-${containerCount}`);
                const subSubRowArrows = document.querySelectorAll(`.sub-sub-row-arrows-${containerCount}`);
                
                const isHidden = subRows.length > 0 && !Array.from(subRows).every(subRow => subRow.style.display === "none");

                // handle sub-rows display
                subRows.forEach(subRow => {
                    subRow.style.display = isHidden ? "none" : "table-row";
                });

                // handle sub-row arrows display
                subRowArrows.forEach(arrow => {
                    if (!isHidden) {
                        if (arrow.classList.contains("fa-caret-right")) {
                            changeArrowDirection(arrow);
                        } else if (arrow.classList.contains("fa-sort-down")) {
                            return
                        };
                    } else {
                        if (arrow.classList.contains("fa-caret-right")) {
                            return
                        } else if (arrow.classList.contains("fa-sort-down")) {
                            changeArrowDirection(arrow);
                        };
                    };
                });

                const allArrowsRight = Array.from(subRowArrows).every(arrow => arrow.classList.contains("fa-caret-right"));
                const allArrowsDown = Array.from(subRowArrows).every(arrow => arrow.classList.contains("fa-sort-down"));

                if (!allArrowsRight) {
                    headerIcon.classList.remove("fa-caret-right");
                    headerIcon.classList.add("fa-sort-down");
                };

                if (allArrowsRight) {
                    headerIcon.classList.add("fa-caret-right");
                    headerIcon.classList.remove("fa-sort-down");
                };

                if (!allArrowsDown) {
                    headerIcon.classList.add("fa-caret-right");
                    headerIcon.classList.remove("fa-sort-down");
                };

                // handle sub-sub-rows display
                subSubRows.forEach(subSubRow => {
                    if (isHidden) {
                        if (subSubRow.getAttribute("visibility") === "hidden") {
                            subSubRow.style.display = "none";
                        } else if (subSubRow.getAttribute("visibility") === "shown") {
                            subSubRow.style.display = "none";
                        };
                    } else {
                        if (subSubRow.getAttribute("visibility") === "hidden") {
                            subSubRow.style.display = "table-row";
                            subSubRow.setAttribute("visibility", "shown")
                        } else {
                            subSubRow.style.display = "table-row";
                        };
                    };
                });

                // handle sub-sub-row arrows display
                subSubRowArrows.forEach(arrow => {
                    if (!isHidden) {
                        if (arrow.classList.contains("fa-caret-right")) {
                            changeArrowDirection(arrow);
                        } else if (arrow.classList.contains("fa-sort-down")) {
                           return
                        };
                    } else {
                        if (arrow.classList.contains("fa-caret-right")) {
                            return
                        } else if (arrow.classList.contains("fa-sort-down")) {
                            return
                        };
                    };
                });
            });

            headerIconContainer.appendChild(headerIcon);
            cell.appendChild(headerIconContainer);
        };
    });

    // content rows
    const tableBody = table.createTBody();
    let overallHealing = 0;
    let overallHPS = 0;
    let overallCasts = 0;
    let overallManaSpent = 0;
    let overallHolyPower = 0;
    let overallCPM = 0;

    console.log(sortedAbilityBreakdownData)

    // overall required for some cells in the main table
    for (const spellName in sortedAbilityBreakdownData) {
        const spellData = sortedAbilityBreakdownData[spellName];
        if (spellData.total_healing > 0) {
            overallHealing += spellData.total_healing;
        } else {
            overallHealing -= spellData.total_healing;
        };
        
        overallHPS += spellData.total_healing / encounterLength;
        overallCasts += spellData.casts;
        overallManaSpent += spellData.mana_spent;
        overallCPM += spellData.casts / (encounterLength / 60);
    };

    for (const spellName in sortedAbilityBreakdownData) {
        if (excludedSpells.includes(spellName)) {
            continue
        };

        const spellData = sortedAbilityBreakdownData[spellName];
        const row = tableBody.insertRow();
        row.id = `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`;

        const nameCell = row.insertCell();
        nameCell.className = "table-cell-left spell-name-cell";

        // spell icon
        const spellIconContainer = document.createElement("div");
        spellIconContainer.className = "table-spell-icon-container";

        const spellIcon = document.createElement("img");
        spellIcon.src = spellToIconsMap[spellName];
        spellIcon.className = "table-spell-icon";

        // spellIconContainer.appendChild(spellIcon);
        nameCell.appendChild(spellIcon);
        
        const spellNameText = document.createElement("div");
        spellNameText.textContent = spellName;
        spellNameText.className = "table-spell-name-text";
        nameCell.appendChild(spellNameText);

        // make collapsible if it has sub-spells
        if (Object.keys(spellData["sub_spells"]).length > 0 || spellName === "Beacon of Light") {    
        
            const arrowIconContainer = document.createElement("div");
            arrowIconContainer.className = "table-icon-container";

            const arrowIcon = document.createElement("i");
            arrowIcon.className = `fa-solid fa-caret-right table-arrows sub-row-arrows-${containerCount}`;
            arrowIcon.setAttribute("visibility", "hidden");

            // expand sub-row or collapse all nested rows on click
            arrowIconContainer.addEventListener("click", () => {
                changeArrowDirection(arrowIcon);

                const spellClass = spellName.toLowerCase().replaceAll(" ", "-") + "-subrow";

                let subRows = document.querySelectorAll(`.${spellClass}-${containerCount}`);
                let subSubRows = document.querySelectorAll(`.${spellClass}.sub-sub-row-${containerCount}`);

                const isHidden = subRows.length > 0 && !Array.from(subRows).every(subRow => subRow.style.display === "none");

                // handle sub-rows display
                subRows.forEach(subRow => {
                    subRow.style.display = isHidden ? "none" : "table-row";
                });

                // handle sub-sub-rows display
                subSubRows.forEach(subSubRow => {
                    if (isHidden) {
                        if (subSubRow.getAttribute("visibility") === "hidden") {
                            subSubRow.style.display = "none";
                        } else if (subSubRow.getAttribute("visibility") === "shown") {
                            subSubRow.style.display = "none";
                        }
                    } else {
                        if (subSubRow.getAttribute("visibility") === "hidden") {
                            subSubRow.style.display = "none";
                        } else {
                            subSubRow.style.display = "table-row";
                        };
                    };
                });

                // change header arrow
                const headerArrow = document.getElementById(`table-header-icon-${containerCount}`);
                if (!arrowIcon.classList.contains("fa-caret-right")) {
                    headerArrow.classList.add("fa-sort-down");
                    headerArrow.classList.remove("fa-caret-right");
                };

                const subRowArrows = document.querySelectorAll(`.sub-row-arrows-${containerCount}`);
                const allArrowsRight = Array.from(subRowArrows).every(arrow => arrow.classList.contains("fa-caret-right"));

                if (allArrowsRight) {
                    changeArrowDirection(headerArrow);
                };
            });
            arrowIconContainer.appendChild(arrowIcon);
            nameCell.appendChild(arrowIconContainer);
        };
        
        const percentHealingCell = row.insertCell();
        percentHealingCell.className = "table-cell-right healing-percent-cell";
        if (excludedSpellsOnlyResourcesAndCasts.includes(spellName)) {
            percentHealingCell.textContent = "";
        } else {
            if (spellData.total_healing > 0) {
                percentHealingCell.textContent = Number(formatNumbersNoRounding(((spellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";
            } else{
                percentHealingCell.textContent = Number(formatNumbersNoRounding(((spellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";
            };
        };
        
        const healingCell = row.insertCell();
        healingCell.className = "table-cell-right healing-cell";
        if (excludedSpellsOnlyResourcesAndCasts.includes(spellName) ) {
            healingCell.textContent = "";
        } else {
            healingCell.textContent = formatNumbers(spellData.total_healing);
            if (spellData.total_healing < 0) {
                healingCell.style.color = "var(--red-font-hover)";
            };
        };
        
        const HPSCell = row.insertCell();
        HPSCell.className = "table-cell-right HPS-cell";
        if (excludedSpellsOnlyResourcesAndCasts.includes(spellName)) {
            HPSCell.textContent = "";
        } else {
            HPSCell.textContent = formatNumbers(spellData.total_healing / encounterLength);
            if (spellData.total_healing < 0) {
                HPSCell.style.color = "var(--red-font-hover)";
            };
        };
        
        const castsCell = row.insertCell();
        castsCell.className = "table-cell-right";

        // adjust functionality for certain spells
        if (excludedSpellsCasts.includes(spellName)) {
            castsCell.textContent = "";
        } else {
            castsCell.textContent = spellData.casts.toFixed(1);
        };
        
        const avgCastsCell = row.insertCell();
        avgCastsCell.className = "table-cell-right average-healing-cell";

        if (excludedSpellsAverage.includes(spellName)) {
            avgCastsCell.textContent = "";
        } else if (excludedSpellsCasts.includes(spellName) || excludedSpellsCastsAverageHits.includes(spellName)) {
            avgCastsCell.textContent = formatNumbers(spellData.total_healing / spellData.hits);
            if (spellData.total_healing < 0) {
                avgCastsCell.style.color = "var(--red-font-hover)";
            };
        } else if (excludedSpellsOnlyResourcesAndCasts.includes(spellName)) {
            avgCastsCell.textContent = "";
        } else {
            avgCastsCell.textContent = formatNumbers(spellData.total_healing / spellData.casts);
            if (spellData.total_healing < 0) {
                avgCastsCell.style.color = "var(--red-font-hover)";
            };
        };
        if (avgCastsCell.textContent === "Infinity") {
            avgCastsCell.textContent = "0";
        };

        const hitsCell = row.insertCell();
        hitsCell.className = "table-cell-right";
        hitsCell.textContent = spellData.hits > 0 ? spellData.hits.toFixed(1) : "";

        const critPercentCell = row.insertCell();
        critPercentCell.className = "table-cell-right";
        if (excludedSpellsCrit.includes(spellName) || excludedSpellsOnlyResourcesAndCasts.includes(spellName)) {
            critPercentCell.textContent = "";
        } else {
            critPercentCell.textContent = (spellData.crit_percent).toFixed(1) + "%";
        };
        
        const manaSpentCell = row.insertCell();
        manaSpentCell.className = "table-cell-right mana-spent-cell";
        manaSpentCell.textContent = formatNumbers(spellData.mana_spent);
        if (spellData.mana_spent === 0) {
            manaSpentCell.textContent = "";
        };

        // show positive if gained, negative if spent
        const holyPowerCell = row.insertCell();
        holyPowerCell.className = "table-cell-right holy-power-cell";
        let holyPowerText = spellData.holy_power_gained > 0 ? spellData.holy_power_gained.toFixed(1) : spellData.holy_power_spent.toFixed(1);
        
        if (spellData.holy_power_gained > 0) {
            holyPowerText = "+" + holyPowerText;
            holyPowerCell.style.color = "var(--holy-power-gain)";
            overallHolyPower += spellData.holy_power_gained.toFixed(1);
        } else if (spellData.holy_power_spent > 0) {
            holyPowerText = "-" + holyPowerText;
            holyPowerCell.style.color = "var(--holy-power-loss)";
            overallHolyPower -= spellData.holy_power_spent.toFixed(1);
        } else if (spellData.holy_power_gained === 0 && spellData.holy_power_spent === 0) {
            holyPowerText = "";
        };
        holyPowerCell.textContent = holyPowerText

        const CPMCell = row.insertCell();
        CPMCell.className = "table-cell-right CPM-cell";
        if (spellData.casts > 0) {
            CPMCell.textContent = (spellData.casts / (encounterLength / 60)).toFixed(1);
        };

        const overhealingPercentCell = row.insertCell();
        overhealingPercentCell.className = "table-cell-right";
        if (spellData.overhealing) {
            overhealingPercentCell.textContent = (spellData.overhealing * 100).toFixed(1) + "%";
        };
        
        // BEACON SOURCES
        if (spellName === "Beacon of Light") {
            for (const sourceSpellName in spellData["source_spells"]) {
                const sourceSpellData = spellData["source_spells"][sourceSpellName];
                const sourceSpellRow = tableBody.insertRow();
                sourceSpellRow.style.display = "none";
                sourceSpellRow.className = `${spellName.toLowerCase()}-subrow`;
                sourceSpellRow.className = sourceSpellRow.className.replaceAll(/\s|\(|\)/g, "-");
                sourceSpellRow.className = sourceSpellRow.className.replaceAll("--", "-");
                sourceSpellRow.className = sourceSpellRow.className + `-${containerCount}`;
                sourceSpellRow.classList.add(`sub-row-${containerCount}`);
                sourceSpellRow.id = `${sourceSpellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`;
                sourceSpellRow.setAttribute('data-parent-row', `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`);
                sourceSpellRow.setAttribute("visibility", "hidden");
                // subRow.style.display = "none";

                const nameCell = sourceSpellRow.insertCell();
                nameCell.className = "table-sub-cell-left spell-name-cell sub-cell";

                // spell icon
            const spellIconContainer = document.createElement("div");
            spellIconContainer.className = "table-spell-icon-container";

            const spellIcon = document.createElement("img");

            // format spell names to make them less ugly
            let formattedSubSpellName = sourceSpellName;
            if (formattedSubSpellName.includes("Glimmer of Light")) {
                formattedSubSpellName = "Glimmer of Light";
            };

            spellIcon.src = spellToIconsMap[formattedSubSpellName];
            spellIcon.className = "table-spell-icon";

            // spellIconContainer.appendChild(spellIcon);
            nameCell.appendChild(spellIcon);
            
            const spellNameText = document.createElement("div");
            spellNameText.textContent = formattedSubSpellName;
            
            spellNameText.className = "table-spell-name-text";
            nameCell.appendChild(spellNameText);

            const percentHealingCell = sourceSpellRow.insertCell();
            percentHealingCell.className = "table-sub-cell-right healing-percent-cell";
            percentHealingCell.textContent = Number(formatNumbersNoRounding(((sourceSpellData.healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";

            const healingCell = sourceSpellRow.insertCell();
            healingCell.className = "table-sub-cell-right healing-cell";
            healingCell.textContent = formatNumbers(sourceSpellData.healing);

            const HPSCell = sourceSpellRow.insertCell();
            HPSCell.className = "table-sub-cell-right HPS-cell";
            HPSCell.textContent = formatNumbers(sourceSpellData.healing / encounterLength);

            const castsCell = sourceSpellRow.insertCell();
            castsCell.className = "table-sub-cell-right";
            
            const avgCastsCell = sourceSpellRow.insertCell();
            avgCastsCell.className = "table-sub-cell-right average-healing-cell";
            avgCastsCell.textContent = formatNumbers(sourceSpellData.healing / sourceSpellData.hits);

            const hitsCell = sourceSpellRow.insertCell();
            hitsCell.className = "table-sub-cell-right";
            hitsCell.textContent = sourceSpellData.hits > 0 ? sourceSpellData.hits.toFixed(1): "";

            const critPercentCell = sourceSpellRow.insertCell();
            critPercentCell.className = "table-sub-cell-right";
  
            const manaSpentCell = sourceSpellRow.insertCell();
            manaSpentCell.className = "table-sub-cell-right mana-spent-cell";

            // show positive if gained, negative if spent
            const holyPowerCell = sourceSpellRow.insertCell();
            holyPowerCell.className = "table-sub-cell-right holy-power-cell";

            const CPMCell = sourceSpellRow.insertCell();
            CPMCell.className = "table-sub-cell-right CPM-cell";

            const overhealingPercentCell = sourceSpellRow.insertCell();
            overhealingPercentCell.className = "table-cell-right";
            };
        };
        
        // SUB SPELLS
        for (const subSpellName in spellData["sub_spells"]) {
            if (excludedSpells.includes(subSpellName)) {
                continue
            };

            const subSpellData = spellData["sub_spells"][subSpellName];
            const subRow = tableBody.insertRow();
            subRow.style.display = "none";
            subRow.className = `${spellName.toLowerCase()}-subrow`;
            subRow.className = subRow.className.replaceAll(/\s|\(|\)/g, "-");
            subRow.className = subRow.className.replaceAll("--", "-");
            subRow.className = subRow.className + `-${containerCount}`
            subRow.classList.add(`sub-row-${containerCount}`);
            subRow.id = `${subSpellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`;
            subRow.setAttribute('data-parent-row', `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`);
            subRow.setAttribute("visibility", "hidden");
            
            const nameCell = subRow.insertCell();
            nameCell.className = "table-sub-cell-left spell-name-cell sub-cell";

            // spell icon
            const spellIconContainer = document.createElement("div");
            spellIconContainer.className = "table-spell-icon-container";

            const spellIcon = document.createElement("img");

            // format spell names to make them less ugly
            let formattedSubSpellName = subSpellName;
            if (formattedSubSpellName.includes("Glimmer of Light")) {
                formattedSubSpellName = "Glimmer of Light";
            };

            spellIcon.src = spellToIconsMap[formattedSubSpellName];
            spellIcon.className = "table-spell-icon";

            // spellIconContainer.appendChild(spellIcon);
            nameCell.appendChild(spellIcon);
            
            const spellNameText = document.createElement("div");
            spellNameText.textContent = formattedSubSpellName;
            
            spellNameText.className = "table-spell-name-text";
            nameCell.appendChild(spellNameText);
            
            if (Object.keys(subSpellData["sub_spells"]).length > 0) {
        
                const arrowIconContainer = document.createElement("div");
                arrowIconContainer.className = "table-icon-container";

                const arrowIcon = document.createElement("i");
                arrowIcon.className = `fa-solid fa-caret-right table-arrows sub-sub-row-arrows-${containerCount}`;
                arrowIcon.setAttribute("visibility", "hidden");

                // expand or collapse sub-row on click
                arrowIconContainer.addEventListener("click", () => {
                    changeArrowDirection(arrowIcon);

                    let spellClass = subSpellName.toLowerCase().replaceAll(/\s|\(|\)/g, "-") + "-subrow";
                    spellClass = spellClass.replaceAll("--", "-");
    
                    let subRows = document.querySelectorAll(`.${spellClass}-${containerCount}`);
                    subRows.forEach(subRow => {
                        subRow.style.display = subRow.style.display === "none" ? "table-row" : "none";
                        if (subRow.style.display === "none") {
                            subRow.setAttribute("visibility", "hidden")
                        } else {
                            subRow.setAttribute("visibility", "shown")
                        };
                    });

                });
                arrowIconContainer.appendChild(arrowIcon);
                nameCell.appendChild(arrowIconContainer);
            };

            const percentHealingCell = subRow.insertCell();
            percentHealingCell.className = "table-sub-cell-right healing-percent-cell";
            if (excludedSpellsOnlyResourcesAndCasts.includes(subSpellName)) {
                percentHealingCell.textContent = "";
            } else {
                percentHealingCell.textContent = Number(formatNumbersNoRounding(((subSpellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";
            };
            
            const healingCell = subRow.insertCell();
            healingCell.className = "table-sub-cell-right healing-cell";
            if (excludedSpellsOnlyResourcesAndCasts.includes(subSpellName)) {
                healingCell.textContent = "";
            } else {
                healingCell.textContent = formatNumbers(subSpellData.total_healing);
            };

            const HPSCell = subRow.insertCell();
            HPSCell.className = "table-sub-cell-right HPS-cell";
            if (excludedSpellsOnlyResourcesAndCasts.includes(subSpellName)) {
                HPSCell.textContent = "";
            } else {
                HPSCell.textContent = formatNumbers(subSpellData.total_healing / encounterLength);

            };

            const castsCell = subRow.insertCell();
            castsCell.className = "table-sub-cell-right";

            // adjust functionality for certain spells
            if (excludedSpellsCasts.includes(subSpellName)) {
                castsCell.textContent = "";
            } else {
                castsCell.textContent = subSpellData.casts.toFixed(1);
            };
            
            const avgCastsCell = subRow.insertCell();
            avgCastsCell.className = "table-sub-cell-right average-healing-cell";

            if (excludedSpellsCasts.includes(subSpellName) || excludedSpellsCastsAverageHits.includes(spellName)) {
                avgCastsCell.textContent = formatNumbers(subSpellData.total_healing / subSpellData.hits);
            } else if (excludedSpellsOnlyResourcesAndCasts.includes(subSpellName)) {
                avgCastsCell.textContent = "";
            } else {
                avgCastsCell.textContent = formatNumbers(subSpellData.total_healing / subSpellData.casts);
            };

            const hitsCell = subRow.insertCell();
            hitsCell.className = "table-sub-cell-right";
            hitsCell.textContent = subSpellData.hits > 0 ? subSpellData.hits.toFixed(1) : "";

            const critPercentCell = subRow.insertCell();
            critPercentCell.className = "table-sub-cell-right";

            if (excludedSpellsCrit.includes(subSpellName) || (excludedSpellsOnlyResourcesAndCasts.includes(subSpellName))) {
                critPercentCell.textContent = "";
            } else {
                critPercentCell.textContent = (subSpellData.crit_percent).toFixed(1) + "%";
            };
            
            const manaSpentCell = subRow.insertCell();
            manaSpentCell.className = "table-sub-cell-right mana-spent-cell";
            manaSpentCell.textContent = formatNumbers(subSpellData.mana_spent);
            if (subSpellData.mana_spent === 0) {
                manaSpentCell.textContent = "";
            };

            // show positive if gained, negative if spent
            const holyPowerCell = subRow.insertCell();
            holyPowerCell.className = "table-sub-cell-right holy-power-cell";
            let holyPowerText = subSpellData.holy_power_gained > 0 ? subSpellData.holy_power_gained.toFixed(1) : subSpellData.holy_power_spent.toFixed(1);
            
            if (subSpellData.holy_power_gained > 0) {
                holyPowerText = "+" + holyPowerText;
                holyPowerCell.style.color = "var(--holy-power-gain)";
                overallHolyPower += subSpellData.holy_power_gained.toFixed(1);
            } else if (subSpellData.holy_power_spent > 0) {
                holyPowerText = "-" + holyPowerText;
                holyPowerCell.style.color = "var(--holy-power-loss)";
                overallHolyPower -= subSpellData.holy_power_spent.toFixed(1);
            } else if (subSpellData.holy_power_gained === 0 && subSpellData.holy_power_spent === 0) {
                holyPowerText = "";
            };
            holyPowerCell.textContent = holyPowerText

            const CPMCell = subRow.insertCell();
            CPMCell.className = "table-sub-cell-right CPM-cell";
            if (subSpellData.casts > 0) {
                CPMCell.textContent = (subSpellData.casts / (encounterLength / 60)).toFixed(1);
            };

            const overhealingPercentCell = subRow.insertCell();
            overhealingPercentCell.className = "table-sub-cell-right overhealing-cell";
            if (subSpellData.overhealing) {
                overhealingPercentCell.textContent = (subSpellData.overhealing * 100).toFixed(1)  + "%";
            };

            // SUB SUB SPELLS
            for (const subSubSpellName in spellData["sub_spells"][subSpellName]["sub_spells"]) {
                const subSubSpellData = spellData["sub_spells"][subSpellName]["sub_spells"][subSubSpellName];
                const subRow = tableBody.insertRow();
                subRow.style.display = "none";
                subRow.setAttribute("visibility", "hidden");
                subRow.className = `${subSpellName.toLowerCase()}-subrow`;
                subRow.className = subRow.className.replaceAll(/\s|\(|\)/g, "-");
                subRow.className = subRow.className.replaceAll("--", "-");
                subRow.className = subRow.className + `-${containerCount}`
                subRow.classList.add(spellName.toLowerCase().replaceAll(/\s|\(|\)/g, "-").replaceAll("--", "-") + "-subrow");
                subRow.classList.add(`sub-sub-row-${containerCount}`);
                subRow.setAttribute('data-parent-row', `${subSpellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`);
                
                const nameCell = subRow.insertCell();
                nameCell.className = "table-sub-sub-cell-left spell-name-cell sub-sub-cell";

                // spell icon
                const spellIconContainer = document.createElement("div");
                spellIconContainer.className = "table-spell-icon-container";

                const spellIcon = document.createElement("img");

                // format spell names to make them less ugly
                let formattedSubSubSpellName = subSubSpellName;
                if (formattedSubSubSpellName.includes("Glimmer of Light")) {
                    formattedSubSubSpellName = "Glimmer of Light";
                };

                spellIcon.src = spellToIconsMap[formattedSubSubSpellName];
                spellIcon.className = "table-spell-icon";

                // spellIconContainer.appendChild(spellIcon);
                nameCell.appendChild(spellIcon);
                
                const spellNameText = document.createElement("div");
                spellNameText.textContent = formattedSubSubSpellName;
                
                spellNameText.className = "table-spell-name-text";
                nameCell.appendChild(spellNameText);

    
                const percentHealingCell = subRow.insertCell();
                percentHealingCell.className = "table-sub-sub-cell-right healing-percent-cell";
                percentHealingCell.textContent = Number(formatNumbersNoRounding(((subSubSpellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";
    
                const healingCell = subRow.insertCell();
                healingCell.className = "table-sub-sub-cell-right healing-cell";
                healingCell.textContent = formatNumbers(subSubSpellData.total_healing);
    
                const HPSCell = subRow.insertCell();
                HPSCell.className = "table-sub-sub-cell-right HPS-cell";
                HPSCell.textContent = formatNumbers(subSubSpellData.total_healing / encounterLength);
    
                const castsCell = subRow.insertCell();
                castsCell.className = "table-sub-sub-cell-right";
                castsCell.textContent = subSubSpellData.casts.toFixed(1);
                if (subSubSpellName.includes("Glimmer")) {
                    castsCell.textContent = "";
                };
    
                const avgCastsCell = subRow.insertCell();
                avgCastsCell.className = "table-sub-sub-cell-right average-healing-cell";
                avgCastsCell.textContent = formatNumbers(subSubSpellData.total_healing / subSubSpellData.casts);
    
                const hitsCell = subRow.insertCell();
                hitsCell.className = "table-sub-sub-cell-right";
                hitsCell.textContent = subSubSpellData.hits.toFixed(1);
    
                const critPercentCell = subRow.insertCell();
                critPercentCell.className = "table-sub-sub-cell-right";
                critPercentCell.textContent = (subSubSpellData.crit_percent).toFixed(1) + "%";
    
                const manaSpentCell = subRow.insertCell();
                manaSpentCell.className = "table-sub-sub-cell-right mana-spent-cell";
                manaSpentCell.textContent = formatNumbers(subSubSpellData.mana_spent);
                if (subSpellData.mana_spent === 0) {
                    manaSpentCell.textContent = "";
                };
    
                // show positive if gained, negative if spent
                const holyPowerCell = subRow.insertCell();
                holyPowerCell.className = "table-sub-sub-cell-right holy-power-cell";
                let holyPowerText = subSubSpellData.holy_power_gained > 0 ? subSubSpellData.holy_power_gained.toFixed(1) : subSubSpellData.holy_power_spent.toFixed(1);
                
                if (subSubSpellData.holy_power_gained > 0) {
                    holyPowerText = "+" + holyPowerText;
                    holyPowerCell.style.color = "var(--holy-power-gain)";
                    overallHolyPower += subSubSpellData.holy_power_gained.toFixed(1);
                } else if (subSubSpellData.holy_power_spent > 0) {
                    holyPowerText = "-" + holyPowerText;
                    holyPowerCell.style.color = "var(--holy-power-loss)";
                    overallHolyPower -= subSubSpellData.holy_power_spent.toFixed(1);
                } else if (subSubSpellData.holy_power_gained === 0 && subSubSpellData.holy_power_spent === 0) {
                    holyPowerText = "";
                };
                holyPowerCell.textContent = holyPowerText

                const CPMCell = subRow.insertCell();
                CPMCell.className = "table-sub-sub-cell-right CPM-cell";
                if (subSubSpellData.casts > 0) {
                    CPMCell.textContent = (subSubSpellData.casts / (encounterLength / 60)).toFixed(1);
                };

                const overhealingPercentCell = subRow.insertCell();
                overhealingPercentCell.className = "table-sub-sub-cell-right overhealing-cell";
                if (subSubSpellData.overhealing) {
                    overhealingPercentCell.textContent = (subSubSpellData.overhealing * 100).toFixed(1)  + "%";
                };
            };
        };
    };

    // bottom row
    const row = tableBody.insertRow();
    row.classList.add("total-values-row");
    const overallHealingTextCell = row.insertCell(0);
    overallHealingTextCell.className = "table-cell-bottom-left";
    overallHealingTextCell.textContent = "Total";
    overallHealingTextCell.style.fontWeight = 500;

    const overallHealingPercentCell = row.insertCell(1);
    overallHealingPercentCell.id = `overall-healing-percent-cell-${containerCount}`;
    overallHealingPercentCell.className = "table-cell-bottom-right";
    overallHealingPercentCell.textContent = "100%";
    overallHealingPercentCell.style.fontWeight = 500;
    
    const overallHealingCell = row.insertCell(2);
    overallHealingCell.id = `overall-healing-cell-${containerCount}`
    overallHealingCell.className = "table-cell-bottom-right";
    overallHealingCell.textContent = formatNumbers(overallHealing);
    overallHealingCell.style.fontWeight = 500;

    const overallHPSCell = row.insertCell(3);
    overallHPSCell.id = `overall-HPS-cell-${containerCount}`;
    overallHPSCell.className = "table-cell-bottom-right";
    overallHPSCell.textContent = formatNumbers(overallHPS);
    overallHPSCell.style.fontWeight = 500;

    const overallCastsCell = row.insertCell(4);
    overallCastsCell.id = `overall-casts-cell-${containerCount}`;
    overallCastsCell.className = "table-cell-bottom-right";
    overallCastsCell.textContent = overallCasts.toFixed(1);
    overallCastsCell.style.fontWeight = 500;

    const cell5 = row.insertCell(5);
    const cell6 = row.insertCell(6);
    const cell7 = row.insertCell(7);
    cell5.className = "table-cell-bottom-right";
    cell6.className = "table-cell-bottom-right";
    cell7.className = "table-cell-bottom-right";

    const overallManaSpentCell = row.insertCell(8);
    overallManaSpentCell.id = `overall-mana-spent-cell-${containerCount}`;
    overallManaSpentCell.className = "table-cell-bottom-right";
    overallManaSpentCell.textContent = formatNumbers(overallManaSpent);
    overallManaSpentCell.style.fontWeight = 500;

    const overallHolyPowerCell = row.insertCell(9);
    overallHolyPowerCell.id = `overall-holy-power-cell-${containerCount}`;
    overallHolyPowerCell.className = "table-cell-bottom-right";

    const overallCPMCell = row.insertCell(10);
    overallCPMCell.id = `overall-CPM-cell-${containerCount}`;
    overallCPMCell.className = "table-cell-bottom-right";
    overallCPMCell.textContent = overallCPM.toFixed(1);
    overallCPMCell.style.fontWeight = 500;

    const overallOverhealingCell = row.insertCell(11);
    overallOverhealingCell.id = `overall-overhealing-cell-${containerCount}`;
    overallOverhealingCell.className = "table-cell-bottom-right";

    // append
    const tableWrapper = createElement("div", "table-wrapper", `ability-table-wrapper-${containerCount}`);
    tableWrapper.appendChild(table);
    tableContainer.appendChild(tableWrapper);
    tableContainer.style.display = "block";
};

export { createAbilityBreakdown };