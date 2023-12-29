const createAbilityBreakdown = (simulationData) => {
    const formatNumbers = (number) => {
        return Math.round(number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };

    // convert to array and back to sort the data by healing
    const abilityBreakdownData = simulationData[0];
    let abilityBreakdownArray = Object.entries(abilityBreakdownData);
    abilityBreakdownArray.sort((a, b) => b[1].total_healing - a[1].total_healing);
    let sortedAbilityBreakdownData = Object.fromEntries(abilityBreakdownArray);

    console.log(sortedAbilityBreakdownData)
    const encounterLength = simulationData[1];

    const table = document.createElement("table");

    // headers
    const header = table.createTHead();
    header.id = "table-headers";
    const headerRow = header.insertRow(0);
    const headers = ["Spell Name", "%", "Healing", "HPS", "Casts", "Avg Cast", "Hits", "Crit %", "Mana Spent", "Holy Power"];
    headers.forEach((text, index) => {
        const cell = headerRow.insertCell(index);
        cell.textContent = text;

        // format the headers
        if (text.includes("%")) {
            cell.id = `${text.toLowerCase()}-header`;
            cell.id = cell.id.replaceAll("%", "percent");
        } else {
            cell.id = `${text.toLowerCase()}-header`;
        };

        if (cell.id.includes(" ")) {
            cell.id = cell.id.replaceAll(" ", "-");
        };
        
        // header arrow
        cell.className = `table-header`;

        if (cell.id === "spell-name-header") {
            const iconContainer = document.createElement("div");
            iconContainer.className = "table-header-icon-container";
            const icon = document.createElement("i");
            icon.className = "fa-solid fa-sort-down table-header-arrows";

            // expand or collapse all rows on click
            iconContainer.addEventListener("click", () => {
                const subRows = document.querySelectorAll(".sub-row");
                const subSubRows = document.querySelectorAll(".sub-sub-row");
                
                const isHidden = subRows.length > 0 && subRows[0].style.display !== "none";

                subRows.forEach(subRow => {
                    subRow.style.display = subRow.style.display === "table-row" ? "none" : "table-row";
                });

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
            });

            iconContainer.appendChild(icon);
            cell.appendChild(iconContainer);
        };
    });

    // content rows
    const tableBody = table.createTBody();
    let overallHealing = 0;
    let overallHPS = 0;
    let overallCasts = 0;
    let overallManaSpent = 0;
    let overallHolyPower = 0;

    // overall required for some cells in the main table
    for (const spellName in sortedAbilityBreakdownData) {
        const spellData = sortedAbilityBreakdownData[spellName];
        overallHealing += spellData.total_healing;
        overallHPS += spellData.total_healing / encounterLength;
        overallCasts += spellData.casts;
        overallManaSpent += spellData.mana_spent;
    };

    for (const spellName in sortedAbilityBreakdownData) {
        const spellData = sortedAbilityBreakdownData[spellName];
        const row = tableBody.insertRow();

        const nameCell = row.insertCell();
        nameCell.className = "table-cell-left spell-name-cell";
        if (Object.keys(spellData["sub_spells"]).length > 0) {    
              
            const iconContainer = document.createElement("div");
            iconContainer.className = "table-icon-container";

            const icon = document.createElement("i");
            icon.className = "fa-solid fa-sort-down table-arrows";

            // expand sub-row or collapse all nested rows on click
            iconContainer.addEventListener("click", () => {
                const spellClass = spellName.toLowerCase().replaceAll(" ", "-") + "-subrow";

                let subRows = document.querySelectorAll(`.${spellClass}`);
                let subSubRows = document.querySelectorAll(`.${spellClass}.sub-sub-row`);

                const isHidden = subRows.length > 0 && subRows[0].style.display !== "none";

                subRows.forEach(subRow => {
                    subRow.style.display = isHidden ? "none" : "table-row";
                });

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
            });
            nameCell.textContent = spellName;
            iconContainer.appendChild(icon);
            nameCell.appendChild(iconContainer);
        } else {
            nameCell.textContent = spellName;
        };
        
        const percentHealingCell = row.insertCell();
        percentHealingCell.className = "table-cell-right healing-percent-cell";
        percentHealingCell.textContent = Number(formatNumbers(((spellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%";

        const healingCell = row.insertCell();
        healingCell.className = "table-cell-right healing-cell";
        healingCell.textContent = formatNumbers(spellData.total_healing);

        const HPSCell = row.insertCell();
        HPSCell.className = "table-cell-right HPS-cell";
        HPSCell.textContent = formatNumbers(spellData.total_healing / encounterLength);

        const castsCell = row.insertCell();
        castsCell.className = "table-cell-right";
        castsCell.textContent = spellData.casts;

        const avgCastsCell = row.insertCell();
        avgCastsCell.className = "table-cell-right";
        avgCastsCell.textContent = formatNumbers(spellData.total_healing / spellData.casts);

        const hitsCell = row.insertCell();
        hitsCell.className = "table-cell-right";
        hitsCell.textContent = spellData.hits > 0 ? spellData.hits : "";

        const critPercentCell = row.insertCell();
        critPercentCell.className = "table-cell-right";
        critPercentCell.textContent = spellData.crits > 0 ? (spellData.crit_percent).toFixed(1) + "%" : "";

        const manaSpentCell = row.insertCell();
        manaSpentCell.className = "table-cell-right mana-spent-cell";
        manaSpentCell.textContent = formatNumbers(spellData.mana_spent);
        if (spellData.mana_spent === 0) {
            manaSpentCell.textContent = "";
        };

        // show positive if gained, negative if spent
        const holyPowerCell = row.insertCell();
        holyPowerCell.className = "table-cell-right holy-power-cell";
        let holyPowerText = spellData.holy_power_gained > 0 ? spellData.holy_power_gained : spellData.holy_power_spent;
        
        if (spellData.holy_power_gained > 0) {
            holyPowerText = "+" + holyPowerText;
            holyPowerCell.style.color = "var(--holy-power-gain)";
            overallHolyPower += spellData.holy_power_gained;
        } else if (spellData.holy_power_spent > 0) {
            holyPowerText = "-" + holyPowerText;
            holyPowerCell.style.color = "var(--holy-power-loss)";
            overallHolyPower -= spellData.holy_power_spent;
        } else if (spellData.holy_power_gained === 0 && spellData.holy_power_spent === 0) {
            holyPowerText = "";
        };
        holyPowerCell.textContent = holyPowerText;

        // SUB SPELLS
        for (const subSpellName in spellData["sub_spells"]) {
            const subSpellData = spellData["sub_spells"][subSpellName];
            const subRow = tableBody.insertRow();
            subRow.style.display = "none";
            subRow.className = `${spellName.toLowerCase()}-subrow`;
            subRow.className = subRow.className.replaceAll(/\s|\(|\)/g, "-");
            subRow.className = subRow.className.replaceAll("--", "-");
            subRow.classList.add("sub-row");
            
            const nameCell = subRow.insertCell();
            nameCell.className = "table-sub-cell-left spell-name-cell sub-cell";
            if (Object.keys(subSpellData["sub_spells"]).length > 0) {
        
                const iconContainer = document.createElement("div");
                iconContainer.className = "table-icon-container";

                const icon = document.createElement("i");
                icon.className = "fa-solid fa-sort-down table-arrows";

                // expand or collapse sub-row on click
                iconContainer.addEventListener("click", () => {
                    let spellClass = subSpellName.toLowerCase().replaceAll(/\s|\(|\)/g, "-") + "-subrow";
                    spellClass = spellClass.replaceAll("--", "-");
    
                    let subRows = document.querySelectorAll(`.${spellClass}`);
                    subRows.forEach(subRow => {
                        subRow.style.display = subRow.style.display === "none" ? "table-row" : "none";
                        if (subRow.style.display === "none") {
                            subRow.setAttribute("visibility", "hidden")
                        } else {
                            subRow.setAttribute("visibility", "shown")
                        };
                    });

                });
                if (subSpellName.includes("Glimmer")) {
                    nameCell.textContent = "Glimmer of Light";
                } else {
                    nameCell.textContent = subSpellName;
                };
                iconContainer.appendChild(icon);
                nameCell.appendChild(iconContainer);
            } else {
                if (subSpellName.includes("Glimmer")) {
                    nameCell.textContent = "Glimmer of Light";
                } else {
                    nameCell.textContent = subSpellName;
                };
            };

            const percentHealingCell = subRow.insertCell();
            percentHealingCell.className = "table-sub-cell-right healing-percent-cell";
            percentHealingCell.textContent = "(" + Number(formatNumbers(((subSpellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%)";

            const healingCell = subRow.insertCell();
            healingCell.className = "table-sub-cell-right healing-cell";
            healingCell.textContent = "(" + formatNumbers(subSpellData.total_healing) + ")";

            const HPSCell = subRow.insertCell();
            HPSCell.className = "table-sub-cell-right HPS-cell";
            HPSCell.textContent = "(" + formatNumbers(subSpellData.total_healing / encounterLength) + ")";

            const castsCell = subRow.insertCell();
            castsCell.className = "table-sub-cell-right";
            castsCell.textContent = "(" + subSpellData.casts + ")";
            if (subSpellName.includes("Glimmer")) {
                castsCell.textContent = "";
            };

            const avgCastsCell = subRow.insertCell();
            avgCastsCell.className = "table-sub-cell-right";
            avgCastsCell.textContent = formatNumbers(subSpellData.total_healing / subSpellData.casts);

            const hitsCell = subRow.insertCell();
            hitsCell.className = "table-sub-cell-right";
            hitsCell.textContent = subSpellData.hits > 0 ? subSpellData.hits : "";

            const critPercentCell = subRow.insertCell();
            critPercentCell.className = "table-sub-cell-right";
            critPercentCell.textContent = (subSpellData.crit_percent).toFixed(1) + "%";

            const manaSpentCell = subRow.insertCell();
            manaSpentCell.className = "table-sub-cell-right mana-spent-cell";
            manaSpentCell.textContent = formatNumbers(subSpellData.mana_spent);
            if (subSpellData.mana_spent === 0) {
                manaSpentCell.textContent = "";
            };

            // show positive if gained, negative if spent
            const holyPowerCell = subRow.insertCell();
            holyPowerCell.className = "table-sub-cell-right holy-power-cell";
            let holyPowerText = subSpellData.holy_power_gained > 0 ? subSpellData.holy_power_gained : subSpellData.holy_power_spent;
            
            if (subSpellData.holy_power_gained > 0) {
                holyPowerText = "(+" + holyPowerText + ")";
                holyPowerCell.style.color = "var(--holy-power-gain)";
                overallHolyPower += subSpellData.holy_power_gained;
            } else if (subSpellData.holy_power_spent > 0) {
                holyPowerText = "(-" + holyPowerText + ")";
                holyPowerCell.style.color = "var(--holy-power-loss)";
                overallHolyPower -= subSpellData.holy_power_spent;
            } else if (subSpellData.holy_power_gained === 0 && subSpellData.holy_power_spent === 0) {
                holyPowerText = "";
            };
            holyPowerCell.textContent = holyPowerText;  

            // SUB SUB SPELLS
            for (const subSubSpellName in spellData["sub_spells"][subSpellName]["sub_spells"]) {
                const subSubSpellData = spellData["sub_spells"][subSpellName]["sub_spells"][subSubSpellName];
                const subRow = tableBody.insertRow();
                subRow.style.display = "none";
                subRow.setAttribute("visibility", "hidden");
                subRow.className = `${subSpellName.toLowerCase()}-subrow`;
                subRow.className = subRow.className.replaceAll(/\s|\(|\)/g, "-");
                subRow.className = subRow.className.replaceAll("--", "-");
                subRow.classList.add(spellName.toLowerCase().replaceAll(/\s|\(|\)/g, "-").replaceAll("--", "-") + "-subrow");
                subRow.classList.add("sub-sub-row");
                
                const nameCell = subRow.insertCell();
                nameCell.className = "table-sub-sub-cell-left spell-name-cell sub-sub-cell";
                nameCell.textContent = subSubSpellName;
                if (subSubSpellName.includes("Glimmer")) {
                    nameCell.textContent = "Glimmer of Light";
                };
    
                const percentHealingCell = subRow.insertCell();
                percentHealingCell.className = "table-sub-sub-cell-right healing-percent-cell";
                percentHealingCell.textContent = "((" + Number(formatNumbers(((subSubSpellData.total_healing / overallHealing) * 100 * 10) / 10)).toFixed(1) + "%))";
    
                const healingCell = subRow.insertCell();
                healingCell.className = "table-sub-sub-cell-right healing-cell";
                healingCell.textContent = "((" + formatNumbers(subSubSpellData.total_healing) + "))";
    
                const HPSCell = subRow.insertCell();
                HPSCell.className = "table-sub-sub-cell-right HPS-cell";
                HPSCell.textContent = "((" + formatNumbers(subSubSpellData.total_healing / encounterLength) + "))";
    
                const castsCell = subRow.insertCell();
                castsCell.className = "table-sub-sub-cell-right";
                castsCell.textContent = "((" + subSubSpellData.casts + "))";
                if (subSubSpellName.includes("Glimmer")) {
                    castsCell.textContent = "";
                };
    
                const avgCastsCell = subRow.insertCell();
                avgCastsCell.className = "table-sub-sub-cell-right";
                avgCastsCell.textContent = formatNumbers(subSubSpellData.total_healing / subSubSpellData.casts);
    
                const hitsCell = subRow.insertCell();
                hitsCell.className = "table-sub-sub-cell-right";
                hitsCell.textContent = subSubSpellData.hits;
    
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
                let holyPowerText = subSubSpellData.holy_power_gained > 0 ? subSubSpellData.holy_power_gained : subSubSpellData.holy_power_spent;
                
                if (subSubSpellData.holy_power_gained > 0) {
                    holyPowerText = "((+" + holyPowerText + "))";
                    holyPowerCell.style.color = "var(--holy-power-gain)";
                    overallHolyPower += subSubSpellData.holy_power_gained;
                } else if (subSubSpellData.holy_power_spent > 0) {
                    holyPowerText = "((-" + holyPowerText + "))";
                    holyPowerCell.style.color = "var(--holy-power-loss)";
                    overallHolyPower -= subSubSpellData.holy_power_spent;
                } else if (subSubSpellData.holy_power_gained === 0 && subSubSpellData.holy_power_spent === 0) {
                    holyPowerText = "";
                };
                holyPowerCell.textContent = holyPowerText;  
            };
        };
    };

    // bottom row
    const row = tableBody.insertRow();
    const overallHealingTextCell = row.insertCell(0);
    overallHealingTextCell.className = "table-cell-bottom-left";
    overallHealingTextCell.textContent = "Total";
    overallHealingTextCell.style.fontWeight = 500;

    const overallHealingPercentCell = row.insertCell(1);
    overallHealingPercentCell.id = "overall-healing-percent-cell";
    overallHealingPercentCell.className = "table-cell-bottom-right";
    overallHealingPercentCell.textContent = "100%";
    overallHealingPercentCell.style.fontWeight = 500;
    
    const overallHealingCell = row.insertCell(2);
    overallHealingCell.id = "overall-healing-cell"
    overallHealingCell.className = "table-cell-bottom-right";
    overallHealingCell.textContent = formatNumbers(overallHealing);
    overallHealingCell.style.fontWeight = 500;

    const overallHPSCell = row.insertCell(3);
    overallHPSCell.id = "overall-HPS-cell";
    overallHPSCell.className = "table-cell-bottom-right";
    overallHPSCell.textContent = formatNumbers(overallHPS);
    overallHPSCell.style.fontWeight = 500;

    const overallCastsCell = row.insertCell(4);
    overallCastsCell.id = "overall-casts-cell";
    overallCastsCell.className = "table-cell-bottom-right";
    overallCastsCell.textContent = overallCasts;
    overallCastsCell.style.fontWeight = 500;

    const cell5 = row.insertCell(5);
    const cell6 = row.insertCell(6);
    const cell7 = row.insertCell(7);
    cell5.className = "table-cell-bottom-right";
    cell6.className = "table-cell-bottom-right";
    cell7.className = "table-cell-bottom-right";

    const overallManaSpentCell = row.insertCell(8);
    overallManaSpentCell.id = "overall-mana-spent-cell";
    overallManaSpentCell.className = "table-cell-bottom-right";
    overallManaSpentCell.textContent = formatNumbers(overallManaSpent);
    overallManaSpentCell.style.fontWeight = 500;

    const overallHolyPowerCell = row.insertCell(9);
    overallHolyPowerCell.id = "overall-holy-power-cell";
    overallHolyPowerCell.className = "table-cell-bottom-right";

    // append
    const tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = '';
    tableContainer.appendChild(table);
};

export { createAbilityBreakdown };