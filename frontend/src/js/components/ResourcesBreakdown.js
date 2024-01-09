import { createElement } from "./script.js";
import { createResourceGraph } from "./createResourceGraph.js";

const createResourcesBreakdown = (simulationData, containerCount) => {
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

    const createResourceTable = (data, headerNames) => {
        const table = document.createElement("table");
        table.className = "resources-table";

        const header = table.createTHead();
        header.id = `table-headers-${containerCount}`;
        const headerRow = header.insertRow(0);
        const headers = headerNames;
        headers.forEach((text, index) => {
            const cell = headerRow.insertCell(index);
            cell.textContent = text;

            cell.className = `table-header`;
        });

        return table;
    };

    const manaTable = createResourceTable(simulationData, ["Spell Name", "Mana Spent"]);
    const holyPowerTable = createResourceTable(simulationData, ["Spell Name", "Gained", "Spent", "Wasted"]);

    manaBreakdown.appendChild(manaTable);
    holyPowerBreakdown.appendChild(holyPowerTable);
};

export { createResourcesBreakdown };