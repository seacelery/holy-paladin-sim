import { createElement } from "./script.js";
import { createResourceGraph } from "./createResourceGraph.js";
import { spellToIconsMap } from "../utils/spellToIconsMap.js";

const createResourcesBreakdown = (simulationData, containerCount) => {
    const sortTableByColumn = (table, column, asc = true, headerNames) => {
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

        if (headerNames.includes("Holy Power Gained")) {
            console.log("hi")
            currentArrowIcon.classList.add("holy-power-arrow");
        };

        const dirModifier = asc ? 1 : -1;
        const tBody = table.tBodies[0];
        const totalRow = tBody.querySelector(".total-values-row");
        const totalRowParent = totalRow.parentNode;
    
        // remove total row
        totalRowParent.removeChild(totalRow);
    
        // select the rows
        const rows = Array.from(tBody.querySelectorAll("tr:not(.sub-row)"));
        const allSubRows = Array.from(tBody.querySelectorAll(".sub-row"));
    
        // sort the rows
        const sortedRows = rows.sort((a, b) => {
            let aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            let bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
    
            // remove number formatting
            aColText = aColText.replace(/[-,]/g, '');
            bColText = bColText.replace(/[-,]/g, '');

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

    const formatNumbers = (number) => {
        return Math.round(number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };
    
    let sortOrder = {};
    let lastSortedColumn = null;
    const defaultSortOrders = {
        0: true,
    };
    
    const tableContainer = document.getElementById(`resources-breakdown-table-container-${containerCount}`);
    tableContainer.innerHTML = "";
    tableContainer.style.display = "flex";

    const manaContainer = createElement("div", "resources-container", null);
    const holyPowerContainer = createElement("div", "resources-container", null);

    tableContainer.appendChild(manaContainer);
    tableContainer.appendChild(holyPowerContainer);

    const manaBreakdown = createElement("div", null, `mana-breakdown-container`);
    const holyPowerBreakdown = createElement("div", null, `holy-power-breakdown-container`);

    manaContainer.appendChild(manaBreakdown);
    holyPowerContainer.appendChild(holyPowerBreakdown);

    const manaGraphContainer = createElement("div", `mana-graph-container-${containerCount}`, `mana-graph-content`);
    const manaGraph = createElement("div", null, `mana-graph`);

    const holyPowerGraphContainer = createElement("div", `holy-power-graph-container-${containerCount}`, `holy-power-graph-content`);
    const holyPowerGraph = createElement("div", null, `holy-power-graph`);

    manaGraphContainer.appendChild(manaGraph);
    manaBreakdown.appendChild(manaGraphContainer);

    const manaTimelineData = simulationData[11];
    createResourceGraph(manaTimelineData, `#mana-graph-${containerCount}`, "Mana", "var(--mana)");

    holyPowerGraphContainer.appendChild(holyPowerGraph);
    holyPowerBreakdown.appendChild(holyPowerGraphContainer);

    const holyPowerTimelineData = simulationData[13];
    createResourceGraph(holyPowerTimelineData, `#holy-power-graph-${containerCount}`, "Holy Power", "var(--holy-font");

    const createArrowIcon = (spellName = null) => {
        const iconContainer = document.createElement("div");
        iconContainer.className = "table-icon-container";
        const icon = document.createElement("i");
        icon.className = "fa-solid fa-caret-right table-arrows";
        icon.id = `table-arrow-icon-${spellName}-${containerCount}`;

        iconContainer.appendChild(icon);
        return iconContainer;
    };

    const createResourceTable = (data, headerNames) => {
        const table = document.createElement("table");
        table.className = "resources-table";
        if (headerNames.includes("Mana Gained")) {
            table.id = `resources-table-mana-${containerCount}`;
        } else if (headerNames.includes("Holy Power Gained")) {
            table.id = `resources-table-holy-power-${containerCount}`
        };

        // headers
        const header = table.createTHead();
        header.id = `table-headers-${containerCount}`;
        const headerRow = header.insertRow(0);
        const headers = headerNames;
        headers.forEach((text, index) => {
            const cell = headerRow.insertCell(index);
            cell.textContent = text;
            cell.className = `table-header`;
            cell.classList.add(`${text.toLowerCase().replaceAll(" ", "-")}-header`);
            cell.id = `${text.toLowerCase().replaceAll(" ", "-")}-header-${containerCount}`;

            if (sortOrder[index] === undefined) {
                sortOrder[index] = "asc";
            };
        
            cell.addEventListener("click", (e) => {
                if (e.target.classList.contains("table-header") || e.target.classList.contains(`sorting-icon-${containerCount}`)) {
                    const isAscending = sortOrder[index] === "asc";
                    sortTableByColumn(table, index, !isAscending, headerNames);
                    sortOrder[index] = isAscending ? "desc" : "asc";
                };
            });

            const sortArrowIcon = document.createElement("i");
            sortArrowIcon.classList.add("fa", "fa-sort-down", `sorting-icon-${containerCount}`);
            cell.appendChild(sortArrowIcon);
            sortArrowIcon.style.display = "none";

            if (cell.id === `spell-name-header-${containerCount}`) {
                sortArrowIcon.style.display = "inline-block";
                if (headers.includes("Holy Power Gained")) {
                    cell.classList.add("resources-spell-name-header");
                    sortArrowIcon.classList.add("holy-power-arrow");
                };
            };
        });

        const tableBody = table.createTBody();
        let overallManaSpent = 0;
        let overallManaGained = 0;
        let overallHolyPowerGained = 0;
        let overallHolyPowerSpent = 0;
        let overallHolyPowerWasted = 0;

        for (const spellName in data) {
            const spellData = data[spellName];
            overallManaGained += spellData.mana_gained;
            overallManaSpent += spellData.mana_spent;
            overallHolyPowerGained += spellData.holy_power_gained;
            overallHolyPowerSpent += spellData.holy_power_spent;
            overallHolyPowerWasted += spellData.holy_power_wasted;
        };

        // rows
        for (const spellName in data) {
            const spellData = data[spellName];

            const formattedSpellName = spellName
                .toLowerCase()
                .replace(/['()]/g, "")
                .replace(/\s+/g, "-")
                .replace(/-self/g, "");

            if (headerNames.includes("Mana Spent") && (spellData.mana_spent > 0 || spellData.mana_gained > 0)) {
                const row = tableBody.insertRow();
                row.id = `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`;

                const nameCell = row.insertCell();
                nameCell.className = "table-cell-left spell-name-cell";

                // spell icon
                const spellIcon = document.createElement("img");
                spellIcon.src = spellToIconsMap[spellName];
                spellIcon.className = "table-spell-icon";
                nameCell.appendChild(spellIcon);

                const spellNameText = document.createElement("div");
                spellNameText.textContent = spellName;
                spellNameText.className = "table-spell-name-text";
                nameCell.appendChild(spellNameText);

                let totalManaGained = 0;
                for (const spell in spellData["sub_spells"]) {
                    totalManaGained += spellData["sub_spells"][spell].mana_gained 
                };

                if (Object.keys(spellData["sub_spells"]).length > 0 && totalManaGained > 0) {
                    const arrowContainer = createArrowIcon(formattedSpellName);
                    nameCell.appendChild(arrowContainer);
    
                    arrowContainer.addEventListener("click", () => {
                        const subRows = document.querySelectorAll(`.${formattedSpellName}-sub-row-${containerCount}`);
                        console.log(subRows)
                        const arrow = document.getElementById(`table-arrow-icon-${formattedSpellName}-${containerCount}`)
                        
                        subRows.forEach(subRow => {
                            if (subRow.getAttribute("visibility") === "hidden") {
                                arrow.classList.remove("fa-caret-right");
                                arrow.classList.add("fa-sort-down");
                                subRow.style.display = "table-row";
                                subRow.setAttribute("visibility", "shown");
                            } else {
                                arrow.classList.add("fa-caret-right");
                                arrow.classList.remove("fa-sort-down");
                                subRow.style.display = "none";
                                subRow.setAttribute("visibility", "hidden");
                            };
                        });
                    });
                };

                const manaGainedCell = row.insertCell();
                manaGainedCell.className = "table-cell-right mana-gained-cell";
                if (spellData.mana_gained > 0) {
                    manaGainedCell.textContent = "+" + formatNumbers(spellData.mana_gained);
                };
                
                const manaSpentCell = row.insertCell();
                manaSpentCell.className = "table-cell-right mana-spent-cell";
                if (spellData.mana_spent > 0) {
                    manaSpentCell.textContent = "-" + formatNumbers(spellData.mana_spent);
                };
            };

            if (headerNames.includes("Holy Power Gained") && (spellData.holy_power_gained > 0 || spellData.holy_power_spent > 0 || spellData.holy_power_wasted > 0)) {
                const row = tableBody.insertRow();
                row.id = `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`;

                const nameCell = row.insertCell();
                nameCell.className = "resources-table-cell-left spell-name-cell";

                // spell icon
                const spellIcon = document.createElement("img");
                spellIcon.src = spellToIconsMap[spellName];
                spellIcon.className = "table-spell-icon";
                nameCell.appendChild(spellIcon);

                const spellNameText = document.createElement("div");
                spellNameText.textContent = spellName;
                spellNameText.className = "table-spell-name-text";
                nameCell.appendChild(spellNameText);

                let totalHolyPowerGained = 0;
                let totalHolyPowerWasted = 0;
                for (const spell in spellData["sub_spells"]) {
                    totalHolyPowerGained += spellData["sub_spells"][spell].holy_power_gained;
                    totalHolyPowerWasted += spellData["sub_spells"][spell].holy_power_wasted;
                };

                const excludedHolyPowerSubSpells = ["Light of Dawn", "Word of Glory", "Holy Shock", "Holy Light", "Flash of Light"];
                if (Object.keys(spellData["sub_spells"]).length > 0 && (totalHolyPowerGained > 0 || totalHolyPowerWasted > 0) && !excludedHolyPowerSubSpells.includes(spellName)) {
                    const arrowContainer = createArrowIcon(formattedSpellName);
                    nameCell.appendChild(arrowContainer);
    
                    arrowContainer.addEventListener("click", () => {
                        const subRows = document.querySelectorAll(`.${formattedSpellName}-sub-row-${containerCount}`);
                        const arrow = document.getElementById(`table-arrow-icon-${formattedSpellName}-${containerCount}`)
                        
                        subRows.forEach(subRow => {
                            if (subRow.getAttribute("visibility") === "hidden") {
                                arrow.classList.remove("fa-caret-right");
                                arrow.classList.add("fa-sort-down");
                                subRow.style.display = "table-row";
                                subRow.setAttribute("visibility", "shown");
                            } else {
                                arrow.classList.add("fa-caret-right");
                                arrow.classList.remove("fa-sort-down");
                                subRow.style.display = "none";
                                subRow.setAttribute("visibility", "hidden");
                            };
                        });
                    });
                };

                const holyPowerGainedCell = row.insertCell();
                holyPowerGainedCell.className = "table-cell-right holy-power-gained-cell";
                if (spellData.holy_power_gained > 0) {
                    holyPowerGainedCell.textContent = "+" + Math.round(spellData.holy_power_gained * 10) / 10;
                };
                
                const holyPowerWastedCell = row.insertCell();
                holyPowerWastedCell.className = "table-cell-right holy-power-wasted-cell";
                if (spellData.holy_power_wasted > 0) {
                    holyPowerWastedCell.textContent = "-" + Math.round(spellData.holy_power_wasted * 10) / 10;
                };
                
                const holyPowerSpentCell = row.insertCell();
                holyPowerSpentCell.className = "table-cell-right holy-power-spent-cell";
                if (spellData.holy_power_spent > 0) {
                    holyPowerSpentCell.textContent = "-" + Math.round(spellData.holy_power_spent * 10) / 10;
                };
            };

            // subrows
            for (const subSpellName in spellData["sub_spells"]) {
                const subSpellData = spellData["sub_spells"][subSpellName];

                if (headerNames.includes("Mana Spent") && (subSpellData.mana_spent > 0 || subSpellData.mana_gained > 0) && subSpellName !== spellName) {
                    const subRow = tableBody.insertRow();
                    subRow.setAttribute('data-parent-row', `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`);
                    subRow.style.display = "none";
                    subRow.classList.add(`${formattedSpellName}-sub-row-${containerCount}`);
                    subRow.classList.add("sub-row");
                    subRow.setAttribute("visibility", "hidden");

                    const nameCell = subRow.insertCell();
                    nameCell.className = "table-sub-cell-left spell-name-cell sub-cell";

                    // spell icon
                    const spellIcon = document.createElement("img");
                    spellIcon.src = spellToIconsMap[subSpellName];
                    spellIcon.className = "table-spell-icon";
                    nameCell.appendChild(spellIcon);

                    const spellNameText = document.createElement("div");
                    spellNameText.className = "table-spell-name-text";

                    // adjust names for spells with multiple sources
                    switch(true) {
                        case subSpellName.includes("Divine Revelations"):
                            spellNameText.textContent = "Divine Revelations";
                            break;
                        case subSpellName.includes("Reclamation"):
                            spellNameText.textContent = "Reclamation";
                            break;
                        default:
                            spellNameText.textContent = subSpellName;
                    };

                    nameCell.appendChild(spellNameText);
                
                    const manaGainedCell = subRow.insertCell();
                    manaGainedCell.className = "table-sub-cell-right mana-gained-cell";
                    if (subSpellData.mana_gained > 0) {
                        manaGainedCell.textContent = "+" + Math.round(subSpellData.mana_gained);
                    };
                    
                    const manaSpentCell = subRow.insertCell();
                    manaSpentCell.className = "table-sub-cell-right mana-spent-cell";
                    if (subSpellData.mana_spent > 0) {
                        manaSpentCell.textContent = "-" + Math.round(subSpellData.mana_spent);
                    };
                };

                if (headerNames.includes("Holy Power Gained") && (subSpellData.holy_power_gained > 0 || subSpellData.holy_power_spent > 0 || subSpellData.holy_power_wasted > 0) && subSpellName !== spellName) {
                    const subRow = tableBody.insertRow();
                    subRow.setAttribute('data-parent-row', `${spellName.toLowerCase().replaceAll(" ", "-").replaceAll("'", "")}-row-${containerCount}`);
                    subRow.style.display = "none";
                    subRow.classList.add(`${formattedSpellName}-sub-row-${containerCount}`);
                    subRow.classList.add("sub-row");
                    subRow.setAttribute("visibility", "hidden");

                    const nameCell = subRow.insertCell();
                    nameCell.className = "resources-table-sub-cell-left spell-name-cell sub-cell";

                    // spell icon
                    const spellIcon = document.createElement("img");
                    spellIcon.src = spellToIconsMap[subSpellName];
                    spellIcon.className = "table-spell-icon";
                    nameCell.appendChild(spellIcon);
                    
                    const spellNameText = document.createElement("div");
                    spellNameText.textContent = subSpellName;
                    spellNameText.className = "table-spell-name-text";
                    nameCell.appendChild(spellNameText);

                    const holyPowerGainedCell = subRow.insertCell();
                    holyPowerGainedCell.className = "table-sub-cell-right holy-power-gained-cell";
                    if (subSpellData.holy_power_gained > 0) {
                        holyPowerGainedCell.textContent = "+" + Math.round(subSpellData.holy_power_gained * 10) / 10;
                    };
                    
                    const holyPowerWastedCell = subRow.insertCell();
                    holyPowerWastedCell.className = "table-sub-cell-right holy-power-wasted-cell";
                    if (subSpellData.holy_power_wasted > 0) {
                        holyPowerWastedCell.textContent = "-" + Math.round(subSpellData.holy_power_wasted * 10) / 10;
                    };
                    
                    const holyPowerSpentCell = subRow.insertCell();
                    holyPowerSpentCell.className = "table-sub-cell-right holy-power-spent-cell";
                    if (subSpellData.holy_power_spent > 0) {
                        holyPowerSpentCell.textContent = "-" + Math.round(subSpellData.holy_power_spent * 10) / 10;
                    };
                };
            };
        };

        // bottom row
        const row = tableBody.insertRow();
        row.classList.add("total-values-row");
        const overallTextCell = row.insertCell(0);
        overallTextCell.className = "resources-table-cell-bottom-left";
        overallTextCell.textContent = "Total";
        overallTextCell.style.fontWeight = 500;

        if (headerNames.includes("Mana Gained")) {
            const overallManaGainedCell = row.insertCell(1);
            overallManaGainedCell.id = `overall-mana-gained-cell-${containerCount}`;
            overallManaGainedCell.className = "table-cell-bottom-right";
            overallManaGainedCell.textContent = "+" + Math.round(overallManaGained);
            overallManaGainedCell.style.fontWeight = 500;
            
            const overallManaSpentCell = row.insertCell(2);
            overallManaSpentCell.id = `overall-mana-spent-cell-${containerCount}`
            overallManaSpentCell.className = "table-cell-bottom-right";
            overallManaSpentCell.textContent = "-" + Math.round(overallManaSpent);
            overallManaSpentCell.style.fontWeight = 500;
        };

        if (headerNames.includes("Holy Power Gained")) {
            const overallHolyPowerGainedCell = row.insertCell(1);
            overallHolyPowerGainedCell.id = `overall-holy-power-gained-cell-${containerCount}`;
            overallHolyPowerGainedCell.className = "table-cell-bottom-right";
            overallHolyPowerGainedCell.textContent = "+" + Math.round(overallHolyPowerGained * 10) / 10;
            overallHolyPowerGainedCell.style.fontWeight = 500;
            
            const overallHolyPowerWastedCell = row.insertCell(2);
            overallHolyPowerWastedCell.id = `overall-holy-power-wasted-cell-${containerCount}`;
            overallHolyPowerWastedCell.className = "table-cell-bottom-right";
            overallHolyPowerWastedCell.textContent = "-" + Math.round(overallHolyPowerWasted * 10) / 10;
            overallHolyPowerWastedCell.style.fontWeight = 500;

            const overallHolyPowerSpentCell = row.insertCell(3);
            overallHolyPowerSpentCell.id = `overall-holy-power-spent-cell-${containerCount}`;
            overallHolyPowerSpentCell.className = "table-cell-bottom-right";
            overallHolyPowerSpentCell.textContent = "-" + Math.round(overallHolyPowerSpent * 10) / 10;
            overallHolyPowerSpentCell.style.fontWeight = 500;
        };

        return table;
    };

    let manaTable = createResourceTable(simulationData[0], ["Spell Name", "Mana Gained", "Mana Spent"]);
    let holyPowerTable = createResourceTable(simulationData[0], ["Spell Name", "Holy Power Gained", "Holy Power Wasted", "Holy Power Spent"]);

    manaBreakdown.appendChild(manaTable);
    holyPowerBreakdown.appendChild(holyPowerTable);
};

export { createResourcesBreakdown };