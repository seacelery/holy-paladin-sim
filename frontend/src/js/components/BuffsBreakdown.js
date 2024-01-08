import { buffsToIconsMap } from "../utils/buffsToIconsMap.js";
import { createBuffsLineGraph } from "./createBuffsLineGraph.js";
import { createElement } from "./script.js";

const createBuffsBreakdown = (simulationData, containerCount) => {
    const handleTalentGraph = (talentData, prefix, talentName, colour, awakening = false) => {
        const isTalentActive = Object.values(talentData).reduce((a, b) => a + b, 0) > 0 ? true : false;

        const talentTab = document.getElementById(`${prefix}-tab-${containerCount}`);
        const talentContent = document.getElementById(`${prefix}-content-${containerCount}`);
        const talentGraph = document.getElementById(`${prefix}-graph-${containerCount}`);

        if (isTalentActive) {
            talentTab.style.display = "block";
            talentGraph.innerHTML = "";

            createBuffsLineGraph(talentData, `#${prefix}-graph-${containerCount}`, talentName, colour, awakening, simulationData[12], simulationData);
        } else if (!isTalentActive) {
            talentTab.style.display = "none";
            talentTab.classList.remove("active");
            talentTab.classList.add("inactive");
            talentContent.style.display = "none";
            talentGraph.innerHTML = ""; 

            document.getElementById(`glimmer-content-${containerCount}`).style.display = "block";
            document.getElementById(`glimmer-tab-${containerCount}`).classList.remove("inactive");
            document.getElementById(`glimmer-tab-${containerCount}`).classList.add("active");
        };
    };

    const formatNumbersNoRounding = (number) => {
        const parts = number.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    };

    const createArrowIcon = (buffName = null) => {
        const iconContainer = document.createElement("div");
        iconContainer.className = "table-icon-container";
        const icon = document.createElement("i");
        icon.className = "fa-solid fa-caret-right table-arrows";
        icon.id = `table-arrow-icon-${buffName}-${containerCount}`;

        iconContainer.appendChild(icon);
        return iconContainer;
    };

    const createBuffsTable = (tableContainer, buffsData, isTargetBuffs = false, individualTargetBuffsData = null) => {
        const table = document.createElement("table");

        // headers
        const header = table.createTHead();
        header.id = `table-headers-${containerCount}`;
        const headerRow = header.insertRow(0);

        const headers = isTargetBuffs ? ["Buff Name", "Count", "Uptime", "Average Duration"] : ["Buff Name", "Count", "Uptime"];
        
        headers.forEach((text, index) => {
            const cell = headerRow.insertCell(index);
            cell.textContent = text;
            cell.className = `table-header`;
            cell.classList.add(`${text.toLowerCase().replaceAll(" ", "-")}-header`);
            cell.id = `${text.toLowerCase().replaceAll(" ", "-")}-header-${containerCount}`;
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
                    const targetRows = document.querySelectorAll(`.${formattedBuffName}-target-row-${containerCount}`);
                    const arrow = document.getElementById(`table-arrow-icon-${formattedBuffName}-${containerCount}`)
                    
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
                    row.classList.add(`${formattedBuffName}-target-row-${containerCount}`);
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

    const buffTablesContainer = document.getElementById(`buffs-breakdown-table-container-${containerCount}`);
    buffTablesContainer.style.display = "flex";

    const buffsTabContainer = createElement("div", "buffs-tab-container", null);
    const paladinBuffsTab = createElement("div", "buffs-tab", `paladin-buffs-tab`);
    paladinBuffsTab.textContent = simulationData[6];
    const selfBuffsTableContainer = createElement("div", null, `self-buffs-breakdown-table-container`);
    buffsTabContainer.appendChild(paladinBuffsTab);
    buffsTabContainer.appendChild(selfBuffsTableContainer);
    buffTablesContainer.appendChild(buffsTabContainer);

    const targetBuffsTabContainer = createElement("div", "buffs-tab-container", `target-buffs-container`);
    const targetBuffsTab = createElement("div", "buffs-tab", null);
    targetBuffsTab.textContent = "Targets";
    const targetBuffsTableContainer = createElement("div", null, `target-buffs-breakdown-table-container`);
    targetBuffsTabContainer.appendChild(targetBuffsTab);
    targetBuffsTabContainer.appendChild(targetBuffsTableContainer);

    const buffsLineGraphNavbar = createElement("nav", null, `buffs-line-graph-navbar`);
    const glimmerTab = createElement("div", `buffs-line-graph-tab-${containerCount} active`, `glimmer-tab`);
    glimmerTab.textContent = "Glimmer of Light";
    const tyrsTab = createElement("div", `buffs-line-graph-tab-${containerCount} inactive`, `tyrs-tab`);
    tyrsTab.textContent = "Tyr's Deliverance";
    const awakeningTab = createElement("div", `buffs-line-graph-tab-${containerCount} inactive`, `awakening-tab`);
    awakeningTab.textContent = "Awakening";
    buffsLineGraphNavbar.appendChild(glimmerTab);
    buffsLineGraphNavbar.appendChild(tyrsTab);
    buffsLineGraphNavbar.appendChild(awakeningTab);
    targetBuffsTabContainer.appendChild(buffsLineGraphNavbar);

    const glimmerContent = createElement("div", `buffs-line-graph-tab-content-${containerCount}`, `glimmer-content`);
    const glimmerGraph = createElement("div", null, `glimmer-graph`);
    glimmerGraph.innerHTML = "";
    const glimmerCountData = simulationData[7];
    
    glimmerContent.appendChild(glimmerGraph);
    targetBuffsTabContainer.appendChild(glimmerContent);

    const tyrsContent = createElement("div", `buffs-line-graph-tab-content-${containerCount}`, `tyrs-content`);
    const tyrsGraph = createElement("div", null, `tyrs-graph`);
    tyrsContent.appendChild(tyrsGraph);
    targetBuffsTabContainer.appendChild(tyrsContent);

    const awakeningContent = createElement("div", `buffs-line-graph-tab-content-${containerCount}`, `awakening-content`);
    const awakeningGraph = createElement("div", null, `awakening-graph`);
    awakeningContent.appendChild(awakeningGraph);
    targetBuffsTabContainer.appendChild(awakeningContent);

    buffTablesContainer.appendChild(targetBuffsTabContainer);

    const selfBuffsData = simulationData[3];
    const individualTargetBuffsData = simulationData[4];
    const combinedTargetBuffsData = simulationData[5];
    
    createBuffsTable(selfBuffsTableContainer, selfBuffsData, true);
    createBuffsTable(targetBuffsTableContainer, combinedTargetBuffsData, false, individualTargetBuffsData);

    const tyrsCountData = simulationData[8];
    const awakeningCountData = simulationData[9];

    // add tracking for other talents only if the talent is active
    createBuffsLineGraph(glimmerCountData, `#glimmer-graph-${containerCount}`, "Glimmer of Light", "rgb(206, 163, 106)");
    handleTalentGraph(tyrsCountData, "tyrs", "Tyr's Deliverance", "#ececc3");
    handleTalentGraph(awakeningCountData, "awakening", "Awakening", "rgb(206, 163, 106)", true);
};

export { createBuffsBreakdown };