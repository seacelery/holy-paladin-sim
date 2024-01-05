import { buffsToIconsMap } from "../utils/buffsToIconsMap.js";

const createBuffsBreakdown = (simulationData) => {
    
    const formatNumbersNoRounding = (number) => {
        const parts = number.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    };

    const createArrowIcon = (buffName = null) => {
        const iconContainer = document.createElement("div");
        iconContainer.className = "table-header-icon-container";
        const icon = document.createElement("i");
        icon.className = "fa-solid fa-caret-right table-arrows";
        icon.id = `table-arrow-icon-${buffName}`;

        iconContainer.appendChild(icon);
        return iconContainer;
    };

    const buffTablesContainer = document.getElementById("buffs-breakdown-table-container");
    buffTablesContainer.style.display = "flex";

    const selfBuffsTableContainer = document.getElementById("self-buffs-breakdown-table-container");
    const targetBuffsTableContainer = document.getElementById("target-buffs-breakdown-table-container");

    

    const createBuffsTable = (tableContainer, buffsData, isTargetBuffs = false, individualTargetBuffsData = null) => {
        const table = document.createElement("table");

        // headers
        const header = table.createTHead();
        header.id = "table-headers";
        const headerRow = header.insertRow(0);

        const headers = isTargetBuffs ? ["Buff Name", "Count", "Uptime", "Average Duration"] : ["Buff Name", "Count", "Uptime"];
        
        headers.forEach((text, index) => {
            const cell = headerRow.insertCell(index);
            cell.textContent = text;
            cell.className = `table-header`;
            cell.classList.add(`${text.toLowerCase().replaceAll(" ", "-")}-header`);
            cell.id = `${text.toLowerCase().replaceAll(" ", "-")}-header`;
        });

        const tableBody = table.createTBody();

        for (const buffName in buffsData) {
            const buffData = buffsData[buffName];
            const row = tableBody.insertRow();

            const formattedBuffName = buffName
                .toLowerCase()
                .replace(/['()]/g, "")
                .replace(/\s+/g, "-")
                .replace(/-self/g, "")

            const nameCell = row.insertCell();
            nameCell.className = "buff-table-cell-left spell-name-cell";

            // buff icon
            const buffIconContainer = document.createElement("div");
            buffIconContainer.className = "table-spell-icon-container";

            const buffIcon = document.createElement("img");
            buffIcon.src = buffsToIconsMap[buffName];
            buffIcon.className = "table-spell-icon";

            nameCell.appendChild(buffIcon);
            
            const buffNameText = document.createElement("div");
            if (buffName.includes("Tyr's Deliverance")) {
                buffNameText.textContent = "Tyr's Deliverance";
            } else {
                buffNameText.textContent = buffName;
            };
            buffNameText.className = "table-spell-name-text";
            nameCell.appendChild(buffNameText);

            if (!isTargetBuffs) {
                const arrowContainer = createArrowIcon(formattedBuffName);
                nameCell.appendChild(arrowContainer);

                arrowContainer.addEventListener("click", () => {
                    const targetRows = document.querySelectorAll(`.${formattedBuffName}-target-row`);
                    const arrow = document.getElementById(`table-arrow-icon-${formattedBuffName}`)
                    
                    targetRows.forEach(targetRow => {
                        if (targetRow.getAttribute("visibility") === "hidden") {
                            arrow.classList.remove("fa-caret-right");
                            arrow.classList.add("fa-sort-down");
                            targetRow.style.display = "table-row";
                            targetRow.setAttribute("visibility", "shown");
                        } else {
                            arrow.classList.add("fa-caret-right");
                            arrow.classList.remove("fa-sort-down");
                            targetRow.style.display = "none";
                            targetRow.setAttribute("visibility", "hidden");
                        };
                    });
                });
            };
        
            const countCell = row.insertCell();
            countCell.className = "buff-table-cell-right count-cell";
            countCell.textContent = formatNumbersNoRounding(buffData.count.toFixed(1));

            const uptimeCell = row.insertCell();
            uptimeCell.className = "buff-table-cell-right uptime-cell";
            uptimeCell.textContent = formatNumbersNoRounding((buffData.uptime * 100).toFixed(2)) + "%";

            if (isTargetBuffs) {
                const averageDurationCell = row.insertCell();
                averageDurationCell.className = "buff-table-cell-right average-duration-cell";
                averageDurationCell.textContent = formatNumbersNoRounding((Math.ceil(buffData.average_duration * 10) / 10).toFixed(1));
            }; 
            
            // create rows for target data
            if (individualTargetBuffsData) {

                let targetArray = Object.entries(individualTargetBuffsData[buffName]);
                targetArray.sort((a, b) => b[1].uptime - a[1].uptime);
                let sortedTargetData = Object.fromEntries(targetArray);

                for (const target in sortedTargetData) {
                    const targetData = sortedTargetData[target];
                    const row = tableBody.insertRow();
                    
                    const nameCell = row.insertCell();
                    nameCell.className = "buff-table-sub-cell-left spell-name-cell";
                    nameCell.textContent = target;

                    const countCell = row.insertCell();
                    countCell.className = "buff-table-sub-cell-right count-cell";
                    countCell.textContent = formatNumbersNoRounding(targetData.count.toFixed(1));

                    const uptimeCell = row.insertCell();
                    uptimeCell.className = "buff-table-sub-cell-right uptime-cell";
                    uptimeCell.textContent = formatNumbersNoRounding((targetData.uptime * 100).toFixed(2)) + "%";

                    row.style.display = "none";
                    row.classList.add(`${formattedBuffName}-target-row`);
                    row.classList.add("target-sub-row");
                    row.setAttribute("visibility", "hidden");
                };
            };        
        };

        // append
        const container = tableContainer;
        container.innerHTML = "";
        container.appendChild(table);
        container.style.display = "block";
    };

    const selfBuffsData = simulationData[3];
    const individualTargetBuffsData = simulationData[4];
    const combinedTargetBuffsData = simulationData[5];

    const paladinBuffsTab = document.getElementById("paladin-buffs-tab");
    paladinBuffsTab.textContent = simulationData[6];

    createBuffsTable(selfBuffsTableContainer, selfBuffsData, true);
    createBuffsTable(targetBuffsTableContainer, combinedTargetBuffsData, false, individualTargetBuffsData);
};

export { createBuffsBreakdown };