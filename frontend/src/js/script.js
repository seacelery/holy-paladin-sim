// TO DOS
// colour spell names by spell type

import { createAbilityBreakdown } from "./AbilityBreakdown.js";
import { handleTabs } from "./SimulationOptions.js";

let savedDataTimeout;

const simulateText = document.getElementById("simulate-text");

const importButton = document.getElementById("import-button");
const raceOptions = document.getElementById("race-filter");

const simulateButton = document.getElementById("simulate-button");

// request functions
const importCharacter = async () => {
    let characterName = document.getElementById("character-name-input").value.toLowerCase()
    let characterRealm = document.getElementById("character-realm-input").value.toLowerCase()

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
    return fetch("http://127.0.0.1:5000/run_simulation", {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        let simulationData = data;
        simulateText.textContent = simulationData;
        createAbilityBreakdown(simulationData);
    })
    .catch(error => console.error("Error:", error));
};

// update the paladin class when attributes are changed
const handleRaceChange = () => {
    updateCharacter({
        race: raceOptions.value
    });
};

const handleTalentChange = (event) => {
    const talentName = event.target.getAttribute("data-talent")
    const talentValue = event.target.checked ? 1 : 0

    const talentUpdate = {
        "talents": {
            [talentName]: talentValue
        }
    };

    updateCharacter(talentUpdate);
};

// update displayed information based on imported character
const updateUIAfterImport = (data) => {
    console.log(data);
    raceOptions.value = data.race
    simulateText.textContent = JSON.stringify(data, null, 2);

    // create a checkbox for each talent that exists in html, and check it if the talent is active on the character
    Object.keys(data.talents).forEach(row => {
        Object.keys(data.talents[row]).forEach(talentName => {
            const talentCheckbox = document.querySelector(`input[data-talent="${talentName}"]`);
            if (talentCheckbox) {
                talentCheckbox.checked = data.talents[row][talentName].ranks["current rank"] === 1;
            };
        });
    });
};

// event listeners
importButton.addEventListener("click", importCharacter);
simulateButton.addEventListener("click", runSimulation);

document.querySelectorAll("input[data-talent]").forEach(element => {
    element.addEventListener("change", handleTalentChange);
});

raceOptions.addEventListener("change", handleRaceChange);

// initialise options tabs
handleTabs("options-navbar", "options-tab-content");
