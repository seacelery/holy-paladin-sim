import { createElement } from "./index.js";
import { createBellCurveBarChart, createLowestToHighestBarChart } from "./create-distribution-bar-chart.js";

const createDistributionBreakdown = (simulationData, containerCount) => {
    const distributionData = simulationData.results.healing_distribution;
    const distributionBreakdownContainer = document.getElementById(`distribution-breakdown-table-container-${containerCount}`);

    const bellCurveGraphContainer = createElement("div", `distribution-graph-container-${containerCount}`, `distribution-graph-content`);
    const bellCurveGraph = createElement("div", null, `bell-curve-graph`);

    bellCurveGraphContainer.appendChild(bellCurveGraph);
    distributionBreakdownContainer.appendChild(bellCurveGraphContainer);
    createBellCurveBarChart(distributionData, `#bell-curve-graph-${containerCount}`, "HPS", "var(--rarity-epic)");

    const lowestToHighestGraphContainer = createElement("div", `distribution-graph-container-${containerCount}`, `distribution-graph-content`);
    const lowestToHighestGraph = createElement("div", null, `lowest-to-highest-graph`);

    lowestToHighestGraphContainer.appendChild(lowestToHighestGraph);
    distributionBreakdownContainer.appendChild(lowestToHighestGraphContainer);
    createLowestToHighestBarChart(distributionData, `#lowest-to-highest-graph-${containerCount}`, "HPS", "var(--rarity-epic)");
    document.getElementById(`lowest-to-highest-graph-${containerCount}`).style.display = "none";
};

export { createDistributionBreakdown };