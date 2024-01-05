// TO DOS
// colour spell names by spell type

import { createAbilityBreakdown } from "./AbilityBreakdown.js";
import { createBuffsBreakdown } from "./BuffsBreakdown.js";
import { handleTabs } from "./SimulationOptionsTabs.js";
import { setSimulationOptionsFromImportedData } from "./SimulationOptions.js";
import { createTalentGrid, updateTalentsFromImportedData } from "./TalentGrid.js";

let savedDataTimeout;

const importButton = document.getElementById("import-button");
const raceOption = document.getElementById("race-filter");

const simulateButton = document.getElementById("simulate-button");

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
        // simulateText.textContent = simulationData;
        createAbilityBreakdown(simulationData);
        createBuffsBreakdown(simulationData);
    })
    .catch(error => console.error("Error:", error));
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

// initialise options tabs
handleTabs("options-navbar", "options-tab-content");

export { updateCharacter };