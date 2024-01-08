// TO DOS
// colour spell names by spell type

import { createAbilityBreakdown } from "./AbilityBreakdown.js";
import { createBuffsBreakdown } from "./BuffsBreakdown.js";
import { handleTabs } from "./SimulationOptionsTabs.js";
import { setSimulationOptionsFromImportedData } from "./SimulationOptions.js";
import { createTalentGrid, updateTalentsFromImportedData } from "./TalentGrid.js";

// window.addEventListener("mouseover", (e) => {
//     console.log(e.target)
// })

const socket = io('http://localhost:5000');

socket.on('connect', function() {
    console.log('Connected to the server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from the server');
});

socket.on('connect_error', (error) => {
    console.log('Connection failed:', error);
});

let savedDataTimeout;
let containerCount = 0;
let iterations = 0;
let isSimulationRunning = false;

const importButton = document.getElementById("import-button");
const raceOption = document.getElementById("race-filter");

const simulatioName = document.getElementById("simulation-name-text-input");
simulatioName.value = "Simulation 1";
const simulateButton = document.getElementById("simulate-button");
const simulateButtonContainer = document.getElementById("simulate-button-container");
const simulationProgressBarContainer = document.getElementById("simulation-progress-bar-container");
const simulationProgressBar = document.getElementById("simulation-progress-bar");
const simulationProgressBarText = document.getElementById("simulation-progress-bar-text");

const fullResultsContainer = document.getElementById("results-container");

document.addEventListener("DOMContentLoaded", () => {
    createTalentGrid();
});

socket.on('iteration_update', function(data) {
    if (isSimulationRunning) {
        const progressPercentage = Math.round((data.iteration / iterations) * 100);
        simulationProgressBar.style.width = progressPercentage + "%";
        simulationProgressBarText.textContent = progressPercentage + "%";
    };
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

const playCheckmarkAnimation = () => {
    document.querySelector('.simulation-progress-bar-checkmark-circle').classList.add('animate-circle');
    document.querySelector('.simulation-progress-bar-checkmark-check').classList.add('animate-check');
    document.querySelector('.simulation-progress-bar-checkmark').classList.add('animate-checkmark');
    
    setTimeout(() => {         
        simulateButton.style.opacity = "100";
        simulationProgressBarContainer.style.opacity = "0";
        simulationProgressBar.style.width = "0%";
        document.querySelector('.simulation-progress-bar-checkmark-circle').classList.remove('animate-circle');
        document.querySelector('.simulation-progress-bar-checkmark-check').classList.remove('animate-check');
        document.querySelector('.simulation-progress-bar-checkmark').classList.remove('animate-checkmark');
    }, 3000);    
}

const runSimulation = async () => {
    const encounterLength = document.getElementById("encounter-length-option").value;
    iterations = document.getElementById("iterations-option").value;

    simulationProgressBarContainer.style.opacity = "100";

    isSimulationRunning = true;

    return fetch(`http://127.0.0.1:5000/run_simulation?encounter_length=${encounterLength}&iterations=${iterations}`, {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        let simulationData = data;     
        createSimulationResults(simulationData);

        simulationProgressBarText.textContent = "";
        playCheckmarkAnimation();
           
        isSimulationRunning = false;
    })
    .catch(error => {
        console.error("Error:", error);
        isSimulationRunning = false;
    });
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
    resultHeader.textContent = simulatioName.value;
    console.log(containerCount)
    if (simulatioName.value.includes (`Simulation ${containerCount}`)) {
        simulatioName.value = `Simulation ${containerCount + 1}`;
    };
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
simulateButtonContainer.addEventListener("click", runSimulation);

raceOption.addEventListener("change", handleRaceChange);

// initialise tabs for primary navbar
handleTabs(`options-navbar-1`, "options-tab-content");

export { updateCharacter, createElement };