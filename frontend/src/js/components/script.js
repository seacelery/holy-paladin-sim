// TO DOS
// colour spell names by spell type

import { createAbilityBreakdown } from "./AbilityBreakdown.js";
import { createBuffsBreakdown } from "./BuffsBreakdown.js";
import { handleTabs } from "./SimulationOptionsTabs.js";
import { setSimulationOptionsFromImportedData } from "./SimulationOptions.js";
import { createTalentGrid, updateTalentsFromImportedData } from "./TalentGrid.js";

let savedDataTimeout;
let containerCount = 0;

const importButton = document.getElementById("import-button");
const raceOption = document.getElementById("race-filter");

const simulateButton = document.getElementById("simulate-button");
// const resultsNavbar = document.getElementById("results-navbar");

const fullResultsContainer = document.getElementById("results-container");

document.addEventListener("DOMContentLoaded", () => {
    createTalentGrid();
});

// request functions
const importCharacter = async () => {
    let characterName = document.getElementById("character-name-input").value.toLowerCase();
    let characterRealm = document.getElementById("character-realm-input").value.toLowerCase().replaceAll(" ", "-");

    characterName = "daisu";
    characterRealm = "aszune";

    return fetch(`http://127.0.0.1:5000/import_character?character_name=${characterName}&realm=${characterRealm}`, {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        updateUIAfterImport(data)
    })
    .catch(error => { console.error("Error:", error);
                    if (!characterName) {
                        window.alert(`Character name missing`)
                    } else if (!characterRealm) {
                        window.alert(`Character realm missing`)
                    } else {
                        window.alert(`Character not found`)
                    };          
    });
};

const updateCharacter = async (data) => {
    // const savingData = document.getElementById("saving-data-status");
    const savedData = document.getElementById("saved-data-status");
    
    const handleSavedDataStatus = () => {
        savedData.style.opacity = 1

        clearTimeout(savedDataTimeout);
        savedDataTimeout = setTimeout(() => {
            savedData.style.opacity = 0;
        }, 5000);
    };

    handleSavedDataStatus();

    return fetch("http://127.0.0.1:5000/update_character", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        handleSavedDataStatus();
    })
    .catch(error => console.error("Error:", error));
};

const convertToJSON = (data) => {
    return JSON.stringify(data, null, 2)
};

const runSimulation = async () => {
    const encounterLength = document.getElementById("encounter-length-option").value;
    const iterations = document.getElementById("iterations-option").value;

    return fetch(`http://127.0.0.1:5000/run_simulation?encounter_length=${encounterLength}&iterations=${iterations}`, {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        let simulationData = data;     
        createSimulationResults(simulationData);
    })
    .catch(error => console.error("Error:", error));
};

const createElement = (elementName, className = null, id = null) => {
    const element = document.createElement(elementName);

    if (className && className.includes(" ")) {
        element.classList = className;
    } else if (className) {
        element.classList.add(className);
    };

    if (id) {
        element.id = id + `-${containerCount}`;
    };
    return element;
};

const createSimulationResults = (simulationData) => {
    containerCount++;

    const resultContainer = createElement("div", "single-result-container", "single-result-container");

    // create simulation header
    const resultHeader = createElement("div", "result-header", "result-header");
    resultHeader.textContent = `Simulation ${containerCount}`;
    resultContainer.appendChild(resultHeader);

    // create the navbar and tabs
    const resultsNavbar = createElement("nav", null, "results-navbar");

    const healingTab = createElement("div", `results-tab-${containerCount} active`, "healing-tab");
    healingTab.textContent = "Healing";
    const buffsWindowTab = createElement("div", `results-tab-${containerCount} inactive`, "buffs-window-tab");
    buffsWindowTab.textContent = "Buffs";

    resultsNavbar.appendChild(healingTab);
    resultsNavbar.appendChild(buffsWindowTab);
    resultContainer.appendChild(resultsNavbar);

    // create content windows

    // ability breakdown
    const healingContent = createElement("div", `results-tab-content-${containerCount}`, "healing-content");
    const abilityBreakdown = createElement("div", null, "ability-breakdown-table-container");
    
    healingContent.appendChild(abilityBreakdown);
    resultContainer.appendChild(healingContent);

    // buffs breakdown
    const buffsContent = createElement("div", `results-tab-content-${containerCount}`, "buffs-window-content");
    const buffsBreakdown = createElement("div", null, "buffs-breakdown-table-container");

    buffsContent.appendChild(buffsBreakdown);
    resultContainer.appendChild(buffsContent);
    
    const firstChild = fullResultsContainer.firstChild;
    if (firstChild) {
        fullResultsContainer.insertBefore(resultContainer, firstChild);
    } else {
        fullResultsContainer.appendChild(resultContainer);
    };

    createAbilityBreakdown(simulationData, containerCount);
    createBuffsBreakdown(simulationData, containerCount);

    // initialise tabs within the results
    handleTabs(`results-navbar-${containerCount}`, `results-tab-content-${containerCount}`, containerCount);
    handleTabs(`buffs-line-graph-navbar-${containerCount}`, `buffs-line-graph-tab-content-${containerCount}`, containerCount);
};

// update the paladin class when attributes are changed
const handleRaceChange = () => {
    updateCharacter({
        race: raceOption.value
    });
};

// update displayed information based on imported character
const updateUIAfterImport = (data) => {
    console.log(data);
    setSimulationOptionsFromImportedData(data);

    updateTalentsFromImportedData(data);
};

// event listeners
importButton.addEventListener("click", importCharacter);
simulateButton.addEventListener("click", runSimulation);

raceOption.addEventListener("change", handleRaceChange);

// initialise tabs for primary navbar
handleTabs(`options-navbar-1`, "options-tab-content");

export { updateCharacter, createElement };