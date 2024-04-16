// TO DOS
// colour spell names by spell type

import { createAbilityBreakdown } from "./ability-breakdown.js";
import { createBuffsBreakdown } from "./buffs-breakdown.js";
import { createResourcesBreakdown } from "./resources-breakdown.js";
import { createPriorityBreakdown } from "./priority-breakdown.js";
import { createCooldownsBreakdown } from "./cooldowns-breakdown.js";
import { createPriorityListDisplay, priorityList, addPotionToPriorityList, updatePriorityList, removePotionFromPriorityList } from "./priority-list-display.js";
import { createLoadoutBreakdown } from "./loadout-breakdown.js";
import { handleTabs } from "./simulation-options-tabs.js";
import { setSimulationOptionsFromImportedData, generateBuffsConsumablesImages } from "./simulation-options.js";
import { createTalentGrid, updateTalentsFromImportedData } from "./talent-grid.js";
import { updateEquipmentFromImportedData, initialiseEquipment, generateFullItemData } from "./equipment-options.js";
import { formatNumbers, formatNumbersNoRounding, formatTime, formatThousands, makeFieldEditable, updateEquipmentWithEffectValues, createTooltip, addTooltipFunctionality } from "../utils/misc-functions.js";
import { realmList } from "../utils/data/realm-list.js";
import { createOptionsSliders, roundIterations } from "../components/create-options-sliders.js";

// helper functions
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

// socket to allow the server to send updates while the simulation is ongoing
const socket = io("https://holy-paladin-sim-6479e85b188f.herokuapp.com", {
    withCredentials: true,
    transports: ["websocket"]
});

socket.on("connect", function() {
    console.log("Connected to the server");
});

socket.on("disconnect", function() {
    console.log("Disconnected from the server");
});

socket.on("connect_error", (error) => {
    console.log("Connection failed:", error);
});

let savedDataTimeout;
let containerCount = 0;
let encounterLength = 30;
let iterations = 1;
let isSimulationRunning = false;
let abortController;
let isFirstImport = true;

// save states for use in separate priority breakdowns
export let cooldownFilterState = {};
export let playerAurasFilterState = {};

const themeToggle = document.getElementById("theme-toggle");
const themeToggleCircle = document.getElementById("theme-circle");
const themePaladinIcon = document.getElementById("theme-paladin-icon");
const themeMoonIcon = document.getElementById("theme-moon-icon");
themeToggle.addEventListener("click", () => {
    themeToggleCircle.classList.toggle("theme-checked");
    themePaladinIcon.classList.toggle("theme-icon-hidden");
    themeMoonIcon.classList.toggle("theme-icon-hidden");

    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "plain" ? "paladin" : "plain";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
});

const importButtonMain = document.getElementById("import-button-main");
const importButton = document.getElementById("import-button");

const simulationName = document.getElementById("simulation-name-text-input");
simulationName.value = "Simulation 1";

const simulateButton = document.getElementById("simulate-button");
const simulationProgressBarCheck = document.querySelector(".simulation-progress-bar-check-container");
const simulationProgressBarContainer = document.getElementById("simulation-progress-bar-container");
const simulationProgressBar = document.getElementById("simulation-progress-bar");
const simulationProgressBarText = document.getElementById("simulation-progress-bar-text");
const simulateButtonErrorModal = document.getElementById("simulate-button-error-modal");

window.addEventListener("click", (e) => {
    if (e.target !== document.getElementById("simulate-button-error-modal-message") && e.target !== simulationProgressBarCheck && e.target !== document.querySelector(".simulation-progress-bar-checkmark")) {
        simulateButtonErrorModal.style.display = "none";
    };
});

window.addEventListener("click", (e) => {
    if (e.target !== document.getElementById("character-name-error-modal-message")) {
        document.getElementById("character-name-error-modal").style.display = "none";
    };
});

const fullResultsContainer = document.getElementById("results-container");

document.addEventListener("DOMContentLoaded", () => {
    createTalentGrid();
});

// increment the percentage on the progress bar when the server sends an iteration update
// socket.on("iteration_update", function(data) {
//     console.log("Received iteration update:", data);
//     if (isSimulationRunning) {
//         console.log("Changing progress bar");
//         const progressPercentage = Math.round((data.iteration / iterations) * 100);
//         simulationProgressBar.style.width = progressPercentage + "%";
//         simulationProgressBarText.textContent = progressPercentage + "%";
//     };
// });

function monitorSimulation(taskId) {
    console.log("awawa")
    let iterationInterval = setInterval(() => {
        fetch(`https://holy-paladin-sim-6479e85b188f.herokuapp.com/iteration/${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.iteration) {
                    console.log(`Current Iteration: ${data.iteration} of ${iterations}`);
                    const progressPercentage = Math.round((data.iteration / iterations) * 100);
                    simulationProgressBar.style.width = progressPercentage + "%";
                    simulationProgressBarText.textContent = progressPercentage + "%";
                }
            })
            .catch(error => {
                console.error('Error fetching iteration data:', error);
            });
    }, 1000);

    let resultInterval = setInterval(() => {
        fetch(`https://holy-paladin-sim-6479e85b188f.herokuapp.com/results/${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.state && data.state !== 'SUCCESS') {
                    console.log(`Task state: ${data.state}`);
                } else if (data) {
                    clearInterval(iterationInterval);
                    clearInterval(resultInterval);
                    console.log('Simulation results:', data);
                    simulationProgressBarText.textContent = "";
                    createSimulationResults(data);
                    playCheckmarkAnimation();
                    isSimulationRunning = false;
                    simulationProgressBarContainer.removeEventListener("click", handleSimulationCancel);
                }
            })
            .catch(error => {
                console.error('Error fetching results:', error);
            });
    }, 2000);
}


const handleCharacterName = () => {
    const characterNameFieldMain = document.getElementById("character-name-input-main");
    characterNameFieldMain.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            characterNameFieldMain.value = characterNameFieldMain.value.charAt(0).toUpperCase() + characterNameFieldMain.value.slice(1).toLowerCase();
        };
    });
};

const generateRealmOptions = () => {
    let searchString = "";
    let suggestedOption = "";

    const scrollToMatchingOption = (searchString) => {
        const options = realmSuggestionsContainer.querySelectorAll(".realm-option");

        options.forEach(option => {
            const normalizedOptionText = option.textContent.replace(/\u00A0/g, " ").toLowerCase();
            const normalizedSearchString = searchString.replace(/\u00A0/g, " ").toLowerCase();

            option.classList.remove("option-highlighted");
        
            if (normalizedOptionText.startsWith(normalizedSearchString)) {
                const matchEnd = searchString.length;

                let beforeMatch = option.textContent.slice(0, matchEnd);
                let afterMatch = option.textContent.slice(matchEnd);

                const highlightedText = `<span class="highlighted-text">${beforeMatch}</span>${afterMatch.replace(/ /g, "&nbsp;")}`;
                option.innerHTML = highlightedText;

                if (searchString.length > 0) {
                    option.classList.add("option-highlighted");   
                    selectedRealmDisplay.innerHTML = highlightedText;  
                };

                suggestedOption = option.textContent;
                if (searchString.length > 0) {
                    option.scrollIntoView({ block: "nearest" });
                };
            };
        });
    };

    const characterRegionFieldMain = document.getElementById("character-region-input-main");
    const characterRealmFieldMain = document.getElementById("character-realm-input-main");

    const realmSuggestionsContainer = document.getElementById("character-realm-input-suggestions-container");
    const selectedRealmDisplay = characterRealmFieldMain.querySelector("#character-realm-selected-realm");

    characterRealmFieldMain.addEventListener("click", () => {
        realmSuggestionsContainer.style.display = realmSuggestionsContainer.style.display === "block" ? "none" : "block";
        searchString = "";
        scrollToMatchingOption(searchString);
    });
    
    window.addEventListener("click", (e) => {
        if (!characterRealmFieldMain.contains(e.target) && !realmSuggestionsContainer.contains(e.target)) {
            if (realmSuggestionsContainer.style.display !== "none") {
                realmSuggestionsContainer.style.display = "none";
                selectedRealmDisplay.innerHTML = selectedRealmDisplay.textContent;
            };
        };
    });

    const selectedRegionDisplay = characterRegionFieldMain.querySelector("#character-region-selected-region");
    selectedRealmDisplay.textContent = realmList[selectedRegionDisplay.textContent][0];

    realmList[selectedRegionDisplay.textContent].forEach(realm => {
        const realmOption = createElement("div", "realm-option", null);
        realmOption.textContent = realm;
        realmOption.dataset.name = realm;
        realmSuggestionsContainer.appendChild(realmOption);

        realmOption.addEventListener("click", (e) => {
            e.stopPropagation();
            suggestedOption = realmOption.dataset.name;
            selectedRealmDisplay.innerHTML = suggestedOption;
            realmSuggestionsContainer.style.display = "none";
        });
    });

    characterRealmFieldMain.addEventListener("keydown", (e) => {
        if (e.key.length === 1) {
            searchString += e.key;
            scrollToMatchingOption(searchString);
        } else if (e.key === "Backspace") {
            searchString = searchString.slice(0, -1);
            scrollToMatchingOption(searchString);

            if (searchString.length === 0) {
                selectedRealmDisplay.textContent = realmList[document.getElementById("character-region-selected-region").textContent][0];
            };
        } else if (e.key === "Enter") {
            realmSuggestionsContainer.style.display = "none";
            selectedRealmDisplay.innerHTML = suggestedOption;
            
            suggestedOption = "";
            searchString = "";
        };
    });
};

const generateRegionOptions = () => {
    let searchString = "";
    let suggestedOption = "";

    const scrollToMatchingOption = (searchString) => {
        const options = regionSuggestionsContainer.querySelectorAll(".region-option");

        options.forEach(option => {
            const normalizedOptionText = option.textContent.replace(/\u00A0/g, " ").toLowerCase();
            const normalizedSearchString = searchString.replace(/\u00A0/g, " ").toLowerCase();

            option.classList.remove("option-highlighted");
        
            if (normalizedOptionText.startsWith(normalizedSearchString)) {
                const matchEnd = searchString.length;

                let beforeMatch = option.textContent.slice(0, matchEnd);
                let afterMatch = option.textContent.slice(matchEnd);

                const highlightedText = `<span class="highlighted-text">${beforeMatch}</span>${afterMatch.replace(/ /g, "&nbsp;")}`;
                option.innerHTML = highlightedText;

                if (searchString.length > 0) {
                    option.classList.add("option-highlighted");   
                    selectedRegionDisplay.innerHTML = highlightedText;  
                };

                suggestedOption = option.textContent;
                if (searchString.length > 0) {
                    option.scrollIntoView({ block: "nearest" });
                };
            };
        });

        const characterRealmFieldMain = document.getElementById("character-realm-input-main");
        const realmSuggestionsContainer = document.getElementById("character-realm-input-suggestions-container");
        const selectedRealmDisplay = characterRealmFieldMain.querySelector("#character-realm-selected-realm");
        const selectedRegionDisplay = characterRegionFieldMain.querySelector("#character-region-selected-region");
        
        const regionOptions = document.querySelectorAll(".region-option");
        regionOptions.forEach(option => {
            option.addEventListener("click", (e) => {
                while (realmSuggestionsContainer.firstChild) {
                    realmSuggestionsContainer.removeChild(realmSuggestionsContainer.firstChild);
                };
        
                selectedRealmDisplay.textContent = realmList[e.target.dataset.name][0];
            
                realmList[e.target.dataset.name].forEach(realm => {
                    const realmOption = createElement("div", "realm-option", null);
                    realmOption.textContent = realm;
                    realmOption.dataset.name = realm;
                    realmSuggestionsContainer.appendChild(realmOption);
            
                    realmOption.addEventListener("click", (e) => {
                        e.stopPropagation();
                        selectedRealmDisplay.textContent = realmOption.dataset.name;
                        realmSuggestionsContainer.style.display = "none";
                    });
                });
            });
    });
    };

    const characterRegionFieldMain = document.getElementById("character-region-input-main");

    const regionSuggestionsContainer = document.getElementById("character-region-input-suggestions-container");
    const selectedRegionDisplay = characterRegionFieldMain.querySelector("#character-region-selected-region");

    characterRegionFieldMain.addEventListener("click", () => {
        regionSuggestionsContainer.style.display = regionSuggestionsContainer.style.display === "block" ? "none" : "block";
        scrollToMatchingOption(searchString);
    });
    
    window.addEventListener("click", (e) => {
        if (!characterRegionFieldMain.contains(e.target) && !regionSuggestionsContainer.contains(e.target)) {
            regionSuggestionsContainer.style.display = "none";
        };
    });

    selectedRegionDisplay.textContent = "EU";

    ["EU", "US"].forEach(region => {
        const regionOption = createElement("div", "region-option", null);
        regionOption.textContent = region;
        regionOption.dataset.name = region;
        regionSuggestionsContainer.appendChild(regionOption);

        regionOption.addEventListener("click", (e) => {
            e.stopPropagation();
            selectedRegionDisplay.textContent = regionOption.dataset.name;
            regionSuggestionsContainer.style.display = "none";
        });
    });
};

// request functions
const importCharacter = async () => {
    let characterName = document.getElementById("character-name-input").value.toLowerCase();
    let characterRealm = document.getElementById("character-realm-input").value.toLowerCase().replaceAll(" ", "-");
    let characterRegion = document.getElementById("character-region-input").value.toLowerCase();

    if (!characterName) {
        characterName = document.getElementById("character-name-input-main").value.toLowerCase();
    };
    if (!characterRealm) {
        characterRealm = document.getElementById("character-realm-selected-realm").textContent.toLowerCase().replace(/\u00A0/g, "-").replace(" ", "-");
    };
    if (!characterRegion) {
        characterRegion = document.getElementById("character-region-selected-region").textContent.toLowerCase();
    };

    if (characterName && characterRealm && characterRegion && isFirstImport) {
        const importButtonText = document.getElementById("import-button-text-main");
        const importButtonLoading = document.getElementById("import-button-main-loading-container");
        importButtonText.style.display = "none";
        importButtonLoading.style.display = "flex";
        importButtonMain.style.pointerEvents = "none";
    };

    if (characterName && characterRealm && characterRegion && !isFirstImport) {
        const loadingScreen = document.getElementById("loading-screen");
        loadingScreen.style.display = "flex";
        const loadingCorner = document.getElementById("loading-corner");
        loadingCorner.style.display = "flex";
        const loadingIcon = document.getElementById("import-button-loading-container");
        loadingIcon.style.display = "flex";
        const importContainerMain = document.getElementById("import-container-main");
        importContainerMain.style.display = "none";
    };

    return fetch(`https://holy-paladin-sim-6479e85b188f.herokuapp.com/import_character?character_name=${characterName}&realm=${characterRealm}&region=${characterRegion}`, {
        method: 'GET', // or POST, PUT, etc.
        mode: 'cors',  // Make sure CORS mode is set
        credentials: 'include', // or 'same-origin' if needed
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('sessionToken', data.session_token);
        console.log(data)
        updateEquipmentWithEffectValues(data);
        updateUIAfterImport(data, isFirstImport);
        initialiseEquipment();
        isFirstImport = false;
    })
    .catch(error => { console.error("Error:", error);
                    if (isFirstImport) {
                        const importButtonText = document.getElementById("import-button-text-main");
                        const importButtonLoading = document.getElementById("import-button-main-loading-container");
                        importButtonText.style.display = "block";
                        importButtonLoading.style.display = "none";
                        importButtonMain.style.pointerEvents = "auto";
                    };

                    if (!isFirstImport) {
                        const loadingScreen = document.getElementById("loading-screen");
                        loadingScreen.style.display = "none";
                        const loadingCorner = document.getElementById("loading-corner");
                        loadingCorner.style.display = "none";
                        const loadingIcon = document.getElementById("import-button-loading-container");
                        loadingIcon.style.display = "none";
                    };
                    
                    document.getElementById("character-name-error-modal").style.display = "flex";
                    if (!characterName) {
                        document.getElementById("character-name-error-modal-message").textContent = "Character name missing";
                    } else if (!characterRealm) {
                        document.getElementById("character-name-error-modal-message").textContent = "Character realm missing";
                    } else {
                        document.getElementById("character-name-error-modal-message").textContent = "Character not found";
                    };          
    });
};

const updateStats = async () => {
    let characterName = document.getElementById("character-name-input").value.toLowerCase();
    let characterRealm = document.getElementById("character-realm-input").value.toLowerCase().replaceAll(" ", "-");
    let characterRegion = document.getElementById("character-region-input").value.toLowerCase();

    // const customEquipment = encodeURIComponent(JSON.stringify(generateFullItemData()["equipment"]));
    const customEquipment = generateFullItemData()["equipment"];

    return fetch(`https://holy-paladin-sim-6479e85b188f.herokuapp.com/fetch_updated_data`, {
        method: 'POST', // Changed from 'GET' to 'POST'
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            character_name: characterName,
            realm: characterRealm,
            region: characterRegion,
            custom_equipment: customEquipment
        }),
        credentials: 'include' // To handle cookies
    })
    .then(response => response.json())
    .then(data => {
        updateEquipmentFromImportedData(data);
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
    const savedData = document.getElementById("saved-data-status");
    console.log(data)
    
    const handleSavedDataStatus = () => {
        savedData.style.opacity = 1

        clearTimeout(savedDataTimeout);
        savedDataTimeout = setTimeout(() => {
            savedData.style.opacity = 0;
        }, 5000);
    };

    handleSavedDataStatus();

    return fetch("https://holy-paladin-sim-6479e85b188f.herokuapp.com/update_character", {
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
        updateStats();
    })
    .catch(error => console.error("Error:", error));
};

// used on progress bar
const playCheckmarkAnimation = () => {
    document.querySelector(".simulation-progress-bar-checkmark-circle").classList.add("animate-circle");
    document.querySelector(".simulation-progress-bar-checkmark-check").classList.add("animate-check");
    document.querySelector(".simulation-progress-bar-checkmark").classList.add("animate-checkmark");
    
    setTimeout(() => {         
        simulateButton.style.opacity = "100";
        simulationProgressBarContainer.style.opacity = "0";
        simulationProgressBar.style.width = "0%";
        document.querySelector(".simulation-progress-bar-checkmark-circle").classList.remove("animate-circle");
        document.querySelector(".simulation-progress-bar-checkmark-check").classList.remove("animate-check");
        document.querySelector(".simulation-progress-bar-checkmark").classList.remove("animate-checkmark");
    }, 3000);    
};

const playCancelledAnimation = () => {
    simulationProgressBar.style.background = "var(--red-font-cancelled)";

    document.querySelector(".simulation-progress-bar-cancel-circle").classList.add("animate-circle");
    document.querySelector(".simulation-progress-bar-cancel-x").classList.add("animate-x");
    
    setTimeout(() => {         
        simulateButton.style.opacity = "100";
        simulationProgressBarContainer.style.opacity = "0";
        simulationProgressBar.style.width = "0%";
        document.querySelector(".simulation-progress-bar-cancel-circle").classList.remove("animate-circle");
        document.querySelector(".simulation-progress-bar-cancel-x").classList.remove("animate-x");
        document.querySelector(".simulation-progress-bar-cancel").style.display = "none";
    }, 3000);

    setTimeout(() => {
        simulationProgressBar.style.background = "linear-gradient(to bottom, #16a137 0%,#15b12c 50%,#12aa2b 51%,#17c52e 100%)";
    }, 4000);
};

const handleSimulationCancel = () => {
    if (abortController) {
        abortController.abort();

        document.querySelector(".simulation-progress-bar-checkmark").style.display = "none";
        const cancelSVG = document.querySelector(".simulation-progress-bar-cancel");
        cancelSVG.style.display = "block";
        playCancelledAnimation();

        fetch("https://holy-paladin-sim-6479e85b188f.herokuapp.com/cancel_simulation", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error(err));
    };
};

// socket.on('simulation_progress', function(data) {
//     console.log('Simulation progress:', data);
    
// });

// socket.on('simulation_complete', function(data) {
//     console.log('Simulation complete:', data);
//     createSimulationResults(data);
//     playCheckmarkAnimation();
//     isSimulationRunning = false;
//     simulationProgressBarContainer.removeEventListener("click", handleSimulationCancel);
// });



const startSimulation = () => {
    if (priorityList.length === 0) {
        simulateButtonErrorModal.style.display = "flex";
        return;
    };

    if (window.lastSliderChange === "Slider") {
        iterations = roundIterations(document.getElementById("iterations-option").value);
    } else {
        iterations = document.getElementById("iterations-option").value;
    };

    simulationProgressBarContainer.style.opacity = "100";
    isSimulationRunning = true;
    simulateButton.style.boxShadow = "";  

    const sessionToken = sessionStorage.getItem('sessionToken')
    console.log(sessionToken)
    if (!sessionToken) {
        console.log("Session token not found");
        return;
    }

    const simulationData = {
        session_token: sessionToken,
        encounter_length: document.getElementById("encounter-length-option").value,
        iterations: document.getElementById("iterations-option").value,
        time_warp_time: document.getElementById("time-warp-option").value,
        tick_rate: document.getElementById("tick-rate-option").value,
        raid_health: document.getElementById("raid-health-option").value,
        mastery_effectiveness: document.getElementById("mastery-effectiveness-option").value,
        light_of_dawn_targets: document.getElementById("light-of-dawn-option").value,
        lights_hammer_targets: document.getElementById("lights-hammer-option").value,
        resplendent_light_targets: document.getElementById("resplendent-light-option").value,
        priority_list: priorityList,
        custom_equipment: generateFullItemData()["equipment"]
    };

    console.log("Sending simulation data:", simulationData);
    socket.emit('start_simulation', simulationData);

    console.log("start simulation clicked")

    // socket.emit('start_simulation', { test: 'Hello World' }, (response) => {
    //     console.log('Server responded with:', response);
    // });
}



// const startSimulation = () => {
//     console.log("start simulation clicked");
//     console.log("Socket connected:", socket.connected);  // Confirm connection status

//     if (socket.connected) {
//         socket.emit('start_simulation', { test: 'Hello World' }, (response) => {
//             console.log('Server responded with:', response);
//         });
//     } else {
//         console.log("Socket not connected");
//     }
// }

socket.on("simple_response", function(data) {
    console.log("response received:", data);
})

socket.on('simulation_started', function(data) {
    console.log("Simulation started:", data);
    monitorSimulation(data.task_id);
});

simulationProgressBarContainer.addEventListener("click", startSimulation);

const runSimulation = async () => {
    if (priorityList.length === 0) {
        simulateButtonErrorModal.style.display = "flex";
        return;
    };

    abortController = new AbortController();
    const { signal } = abortController;

    encounterLength = document.getElementById("encounter-length-option").value;

    if (window.lastSliderChange === "Slider") {
        iterations = roundIterations(document.getElementById("iterations-option").value);
    } else {
        iterations = document.getElementById("iterations-option").value;
    };
    
    const timeWarpTime = document.getElementById("time-warp-option").value;
    const tickRate = document.getElementById("tick-rate-option").value;
    const raidHealth = document.getElementById("raid-health-option").value;
    const masteryEffectiveness = document.getElementById("mastery-effectiveness-option").value;
    const lightOfDawnTargets = document.getElementById("light-of-dawn-option").value;
    const lightsHammerTargets = document.getElementById("lights-hammer-option").value;
    const resplendentLightTargets = document.getElementById("resplendent-light-option").value;

    simulationProgressBarContainer.style.opacity = "100";
    isSimulationRunning = true;

    simulationProgressBarContainer.addEventListener("click", handleSimulationCancel);

    const customEquipment = generateFullItemData()["equipment"];

    simulateButton.style.boxShadow = "";  

    return fetch("https://holy-paladin-sim-6479e85b188f.herokuapp.com/run_simulation", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            encounter_length: encounterLength,
            iterations: iterations,
            time_warp_time: timeWarpTime,
            priority_list: priorityList,
            custom_equipment: customEquipment,
            tick_rate: tickRate,
            raid_health: raidHealth,
            mastery_effectiveness: masteryEffectiveness,
            light_of_dawn_targets: lightOfDawnTargets,
            lights_hammer_targets: lightsHammerTargets,
            resplendent_light_targets: resplendentLightTargets
        }),
        credentials: "include",
        signal: signal
    })
    .then(response => response.json())
    .then(data => {
        let simulationData = data;     
        console.log(simulationData)
        
        simulationProgressBarText.textContent = "";
        if (simulationData) {
            createSimulationResults(simulationData);
            playCheckmarkAnimation();
        };
         
        isSimulationRunning = false;
        simulationProgressBarContainer.removeEventListener("click", handleSimulationCancel);
    })
    .catch(error => {
        if (error.name === "AbortError") {
            console.log("Fetch aborted:", error);
        } else {
            console.error("Error:", error);
        }
        
        isSimulationRunning = false;
        simulationProgressBarContainer.removeEventListener("click", handleSimulationCancel);
    });
};

// main function to bring the components together
const createSimulationResults = (simulationData) => {
    containerCount++;

    const simulationContainer = createElement("div", "simulation-container", "simulation-container");
    const resultContainer = createElement("div", "single-result-container", "single-result-container");

    // create simulation header
    const resultHeader = createElement("div", "result-header", "result-header");

    const leftSideContainer = createElement("div", "result-left-side", null);
    resultHeader.appendChild(leftSideContainer);
    const rightSideContainer = createElement("div", "result-right-side", null);
    resultHeader.appendChild(rightSideContainer);

    // make collapsible with arrows
    const resultArrowIconContainer = createElement("div", `result-arrow-container`, null);
    const resultArrowIcon = createElement("i", `fa-solid fa-sort-down result-arrow-icon`, null);
    resultArrowIconContainer.appendChild(resultArrowIcon);
    resultHeader.addEventListener("click", (e) => {
        if (!e.target.id.startsWith("result-text") || e.target === resultArrowIcon) {
            if (resultArrowIcon.classList.contains("fa-sort-down")) {
                resultArrowIcon.classList.remove("fa-sort-down");
                resultArrowIcon.classList.add("fa-caret-right");
                resultContainer.style.display = "none";
                resultHeader.style.display = "flex";
            } else if (resultArrowIcon.classList.contains("fa-caret-right")) {
                resultArrowIcon.classList.remove("fa-caret-right");
                resultArrowIcon.classList.add("fa-sort-down");
                resultContainer.style.display = "block";
            };
        };
    });
    leftSideContainer.appendChild(resultArrowIconContainer);

    // auto-generate new title if no input given
    const resultText = createElement("div", `result-text-${containerCount}`, "result-text");
    resultText.textContent = simulationName.value;
    if (simulationName.value.includes (`Simulation ${containerCount}`)) {
        simulationName.value = `Simulation ${containerCount + 1}`;
    };

    // allow editing of title
    makeFieldEditable(resultText);
    leftSideContainer.appendChild(resultText);

    // add a display for hps, encounter length, and iterations
    const resultDetailsContainer = createElement("div", `result-details-container-${containerCount}`, null);
    const resultName = createElement("div", `result-details-name-${containerCount}`, null);
    resultName.innerHTML = `<span>Name: </span><span style="color: var(--paladin-font)">${simulationData.simulation_details.paladin_name}</span>`;
    resultDetailsContainer.appendChild(resultName);

    const resultHPS = createElement("div", `result-details-hps-${containerCount}`, null);
    resultHPS.innerHTML = `<span>HPS: </span><span style="color: var(--healing-font)">${formatThousands(simulationData.simulation_details.average_hps)}</span>`;
    resultDetailsContainer.appendChild(resultHPS);

    const resultEncounterLength = createElement("div", `result-details-encounter-length-${containerCount}`, null);
    resultEncounterLength.innerHTML = `<span>Length: </span><span style="color: var(--holy-font)">${formatTime(simulationData.simulation_details.encounter_length)}</span>`;
    resultDetailsContainer.appendChild(resultEncounterLength);

    const resultIterations = createElement("div", `result-details-iterations-${containerCount}`, null);
    resultIterations.innerHTML = `<span>Iterations: </span><span style="color: var(--mana)">${simulationData.simulation_details.iterations}</span>`
    
    resultDetailsContainer.appendChild(resultIterations);

    rightSideContainer.appendChild(resultDetailsContainer);

    // add a delete option
    const resultRemoveContainer = createElement("div", `result-remove-container`, null);
    const resultRemoveIcon = createElement("i", `fa-solid fa-xmark result-remove-icon`, null);
    resultRemoveContainer.appendChild(resultRemoveIcon);
    resultRemoveContainer.addEventListener("click", () => {
        simulationContainer.remove();
    });
    rightSideContainer.appendChild(resultRemoveContainer);

    simulationContainer.appendChild(resultHeader);

    // create the navbar and tabs
    const resultsNavbar = createElement("nav", null, "results-navbar");

    const healingTab = createElement("div", `results-tab-${containerCount} active`, "healing-tab");
    healingTab.textContent = "Healing";
    const buffsWindowTab = createElement("div", `results-tab-${containerCount} inactive`, "buffs-window-tab");
    buffsWindowTab.textContent = "Buffs";
    const resourcesTab = createElement("div", `results-tab-${containerCount} inactive`, "resources-tab");
    resourcesTab.textContent = "Resources";
    const priorityTab = createElement("div", `results-tab-${containerCount} inactive`, "priority-tab");
    priorityTab.textContent = "Priority";
    const cooldownsTab = createElement("div", `results-tab-${containerCount} inactive`, "cooldowns-tab");
    cooldownsTab.textContent = "Cooldowns";
    const loadoutTab = createElement("div", `results-tab-${containerCount} inactive`, "loadout-tab");
    loadoutTab.textContent = "Loadout";

    resultsNavbar.appendChild(healingTab);
    resultsNavbar.appendChild(buffsWindowTab);
    resultsNavbar.appendChild(resourcesTab);
    resultsNavbar.appendChild(priorityTab);
    resultsNavbar.appendChild(cooldownsTab);
    resultsNavbar.appendChild(loadoutTab);
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
    
    // resources breakdown
    const resourcesContent = createElement("div", `results-tab-content-${containerCount}`, "resources-content");
    const resourcesBreakdown = createElement("div", null, "resources-breakdown-table-container");

    resourcesContent.appendChild(resourcesBreakdown);
    resultContainer.appendChild(resourcesContent);

    // priority breakdown
    const priorityContent = createElement("div", `results-tab-content-${containerCount}`, "priority-content");
    const priorityBreakdown = createElement("div", null, "priority-breakdown-table-container");

    priorityContent.appendChild(priorityBreakdown);
    resultContainer.appendChild(priorityContent);

    // cooldowns breakdown
    const cooldownsContent = createElement("div", `results-tab-content-${containerCount}`, "cooldowns-content");
    const cooldownsBreakdown = createElement("div", null, "cooldowns-breakdown-table-container");

    cooldownsContent.appendChild(cooldownsBreakdown);
    resultContainer.appendChild(cooldownsContent);

    // player info breakdown
    const loadoutContent = createElement("div", `results-tab-content-${containerCount}`, "loadout-content");
    const loadoutBreakdown = createElement("div", null, "loadout-breakdown-table-container");

    loadoutContent.appendChild(loadoutBreakdown);
    resultContainer.appendChild(loadoutContent);

    simulationContainer.appendChild(resultContainer);

    const firstChild = fullResultsContainer.firstChild;
    if (firstChild) {
        fullResultsContainer.insertBefore(simulationContainer, firstChild);
    } else {
        fullResultsContainer.appendChild(simulationContainer);
    };

    createAbilityBreakdown(simulationData, containerCount);
    createBuffsBreakdown(simulationData, containerCount);
    createResourcesBreakdown(simulationData, containerCount);
    createPriorityBreakdown(simulationData, containerCount);
    createCooldownsBreakdown(simulationData, containerCount);
    createLoadoutBreakdown(simulationData, containerCount);

    // initialise tabs within the results
    handleTabs(`results-navbar-${containerCount}`, `results-tab-content-${containerCount}`, containerCount);
    handleTabs(`buffs-line-graph-navbar-${containerCount}`, `buffs-line-graph-tab-content-${containerCount}`, containerCount);

    simulateButton.scrollIntoView({ behavior: "smooth" });
};

// update the paladin class when attributes are changed
let currentConsumables = {
    flask: [],
    food: [],
    weapon_imbue: [],
    augment_rune: [],
    raid_buff: [],
    external_buff: {},
    potion: {}
};

const minimiseImportContainer = (data) => {
    const loadingScreen = document.getElementById("loading-screen");
    const loadingCorner = document.getElementById("loading-corner");
    loadingScreen.style.display = "none";
    loadingCorner.style.display = "none";

    const importCharacterContainerSmall = document.getElementById("import-character-container");
    importCharacterContainerSmall.style.display = "flex";

    const characterRegionField = document.getElementById("character-region-input");
    const characterRealmField = document.getElementById("character-realm-input");
    const characterNameField = document.getElementById("character-name-input");

    realmList[data.character_region.toUpperCase()].forEach(realm => {
        const realmOption = createElement("option", "realm-option", null);
        realmOption.textContent = realm;
        realmOption.name = realm;
        document.getElementById("character-realm-input").appendChild(realmOption);
    });

    characterNameField.value = data.character_name.charAt(0).toUpperCase() + data.character_name.slice(1);
    characterRegionField.value = data.character_region.toUpperCase();
    characterRealmField.value = data.character_realm.replaceAll("-", " ")
                                                    .split(" ")
                                                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                                                    .join(" ");
};

// update displayed information based on imported character
const updateUIAfterImport = (data, isFirstImport) => {
    setSimulationOptionsFromImportedData(data);

    if (isFirstImport) {
        minimiseImportContainer(data);
    } else {
        const loadingScreen = document.getElementById("loading-screen");
        loadingScreen.style.display = "none";
        const loadingCorner = document.getElementById("loading-corner");
        loadingCorner.style.display = "none";
        const loadingIcon = document.getElementById("import-button-loading-container");
        loadingIcon.style.display = "none";
    };
    
    updateTalentsFromImportedData(data);
    updateEquipmentFromImportedData(data);
};

handleCharacterName();
generateRealmOptions();
generateRegionOptions();

// event listeners
importButtonMain.addEventListener("click", importCharacter);
importButton.addEventListener("click", importCharacter);
// simulationProgressBarContainer.addEventListener("click", runSimulation);

simulationProgressBarCheck.addEventListener("mouseenter", () => {
    simulateButton.style.boxShadow = "0px 0px 3px 2px var(--info-circle-colour)";
    simulateButton.style.transition = "box-shadow 0.1s ease-in-out";
});
  
simulationProgressBarCheck.addEventListener("mouseleave", () => {
    simulateButton.style.boxShadow = "";
});

const tickRateInfoCircle = document.getElementById("tick-rate-info-circle");
const tickRateTooltip = createTooltip("tick-rate-tooltip", "tick-rate-tooltip");
addTooltipFunctionality(tickRateInfoCircle, tickRateTooltip, null, `<span>Reducing this will increase HoT accuracy but it will be much slower.</span>`);

const raidHealthInfoCircle = document.getElementById("raid-health-info-circle");
const raidHealthTooltip = createTooltip("raid-health-tooltip", "raid-health-tooltip");
addTooltipFunctionality(raidHealthInfoCircle, raidHealthTooltip, null, `<span>This only affects Reclamation.</span>`);

generateBuffsConsumablesImages();

// allows options images to be clicked to change/toggle options
const handleOptionImages = (images, attribute, optionType, toggle = false, multipleAllowed = false) => {
    const formattedAttribute = attribute.replaceAll("-", "_");

    images.forEach(image => {
        image.classList.add(`${attribute}-unselected`);
        image.classList.remove(`${attribute}-selected`);
        image.addEventListener("click", (e) => {
            const attributeName = e.target.getAttribute(`data-${attribute}`);
            const isSelected = e.target.classList.contains(`${attribute}-selected`);
    
            if (optionType === "consumable") {
                if (formattedAttribute === "external_buff" || formattedAttribute === "potion") {
                    const name = attributeName.replaceAll(" ", "-").toLowerCase();
                    const timers = document.querySelectorAll(`.${name}-timer`);
                    const repeatButton = document.getElementById(`${name}-repeat-button`);
                    const addTimerButton = document.getElementById(`${name}-add-timer-button`);
                    if (!isSelected) {
                        currentConsumables[formattedAttribute][attributeName] = [];
                        updateTimerValues(attributeName, formattedAttribute);

                        timers.forEach(timer => {
                            timer.style.display = "flex";
                        });
                        if (repeatButton && addTimerButton) {
                            repeatButton.style.display = "flex";
                            addTimerButton.style.display = "flex";
                        };
                        
                        updatePriorityList();
                    } else {
                        delete currentConsumables[formattedAttribute][attributeName];
                        updateCharacter({
                            consumables: currentConsumables
                        });
                        
                        timers.forEach(timer => {
                            timer.style.display = "none";
                        });
                        if (repeatButton && addTimerButton) {
                            repeatButton.style.display = "none";
                            addTimerButton.style.display = "none";
                        };
                        
                        removePotionFromPriorityList(attributeName);
                    };
                  
                    e.target.classList.toggle(`${attribute}-selected`, !isSelected);
                    e.target.classList.toggle(`${attribute}-unselected`, isSelected);
                } else {
                    if (multipleAllowed) {
                        if (isSelected) {
                            currentConsumables[formattedAttribute] = currentConsumables[formattedAttribute].filter(item => item !== attributeName);
                        } else {
                            currentConsumables[formattedAttribute].push(attributeName);
                        };
                    } else {
                        if (isSelected && toggle) {
                            currentConsumables[formattedAttribute] = currentConsumables[formattedAttribute].filter(item => item !== attributeName);
                        } else {
                            currentConsumables[formattedAttribute] = [attributeName];
                            
                            images.forEach(prevImage => {
                                if (prevImage !== e.target) {
                                    prevImage.classList.remove(`${attribute}-selected`);
                                    prevImage.classList.add(`${attribute}-unselected`);
                                };
                            });
                        };
                    };
            
                    e.target.classList.toggle(`${attribute}-selected`, !isSelected);
                    e.target.classList.toggle(`${attribute}-unselected`, isSelected);
            
                    updateCharacter({
                        consumables: currentConsumables
                    });
                };
            } else if (optionType === "race") {
                updateCharacter({
                    race: attributeName
                });
                        
                images.forEach(prevImage => {
                    if (prevImage !== e.target) {
                        prevImage.classList.remove(`${attribute}-selected`);
                        prevImage.classList.add(`${attribute}-unselected`);
                    };
                });

                e.target.classList.add(`${attribute}-selected`, !isSelected);
                e.target.classList.remove(`${attribute}-unselected`, isSelected);
            };       
        });
    });
};

const raceImages = document.querySelectorAll(".race-image");
const raceTooltip = createTooltip(null, "race-tooltip");
handleOptionImages(raceImages, "race", "race");
raceImages.forEach(image => {
    addTooltipFunctionality(image, raceTooltip, image.getAttribute("data-race"));
});

const flaskImages = document.querySelectorAll(".flask-image");
handleOptionImages(flaskImages, "flask", "consumable", true);

const foodImages = document.querySelectorAll(".food-image");
handleOptionImages(foodImages, "food", "consumable", true);

const weaponImbueImages = document.querySelectorAll(".weapon-imbue-image");
handleOptionImages(weaponImbueImages, "weapon-imbue", "consumable", true);

const augmentRuneImages = document.querySelectorAll(".augment-rune-image");
handleOptionImages(augmentRuneImages, "augment-rune", "consumable", true);

const raidBuffImages = document.querySelectorAll(".raid-buff-image");
handleOptionImages(raidBuffImages, "raid-buff", "consumable", true, true);

const externalBuffImages = document.querySelectorAll(".external-buff-image");
handleOptionImages(externalBuffImages, "external-buff", "consumable", true, true);

const potionImages = document.querySelectorAll(".potion-image");
handleOptionImages(potionImages, "potion", "consumable", true, true);

// handle external buff & potion timers
const updateTimerValues = (name, consumableType) => {
    if (!currentConsumables[consumableType].hasOwnProperty(name)) return;

    console.log(name, consumableType)

    let values = [];
    if (!["Source of Magic"].includes(name)) {
        const formattedName = name.replaceAll(" ", "-").toLowerCase();
        const timerInputs = document.querySelectorAll(`.${formattedName}-timer .${consumableType.replaceAll("_","-")}-timer-input`);
        values = Array.from(timerInputs).map(input => input.value);
    } else {
        values = ["0"];
    };

    currentConsumables[consumableType][name] = values;

    updateCharacter({
        consumables: currentConsumables
    });

    if (consumableType === "potion") {
        for (const potion in currentConsumables["potion"]) {
            addPotionToPriorityList(potion, currentConsumables["potion"][potion]);
        };
    };
};

const createExternalBuffTimers = (buffName, buffCooldown) => {
    const formattedBuffName = buffName.replaceAll(" ", "-").toLowerCase();

    const container = document.getElementById(`${formattedBuffName}-container`);
    const repeatButton = document.getElementById(`${formattedBuffName}-repeat-button`);
    const addTimerButton = document.getElementById(`${formattedBuffName}-add-timer-button`);
    const firstTimerInput = container.querySelectorAll(".external-buff-timer-input")[0];
    firstTimerInput.addEventListener("input", (e) => {
        if (!repeatButton.classList.contains("external-buff-repeating")) {
            updateTimerValues(buffName, "external_buff");
        } else {
            const maxValue = 600;
            const firstTimerInputValue = parseFloat(firstTimerInput.value);
            currentConsumables["external_buff"][buffName] = [firstTimerInputValue];

            let nextTimerValue = parseFloat(firstTimerInputValue) + buffCooldown;
            while (nextTimerValue <= maxValue) {
                currentConsumables["external_buff"][buffName].push(nextTimerValue);
                nextTimerValue += buffCooldown;
            };

            updateCharacter({
                consumables: currentConsumables
            });
        };
    });

    repeatButton.addEventListener("click", () => {
        repeatButton.classList.toggle("external-buff-repeating");
        addTimerButton.style.pointerEvents = repeatButton.classList.contains("external-buff-repeating") ? "none" : "all";
        addTimerButton.style.color = repeatButton.classList.contains("external-buff-repeating") ? "#808080" : "var(--light-font-colour)";
        const timers = container.querySelectorAll(`.${formattedBuffName}-timer`);
        timers.forEach((timer, index) => {
            if (index > 0) {
                timer.style.display = repeatButton.classList.contains("external-buff-repeating") ? "none" : "flex";
            };
        });

        if (repeatButton.classList.contains("external-buff-repeating")) {

            const maxValue = 600;
            const firstTimerInputValue = parseFloat(firstTimerInput.value);
            currentConsumables["external_buff"][buffName] = [firstTimerInputValue];

            let nextTimerValue = parseFloat(firstTimerInputValue) + buffCooldown;
            while (nextTimerValue <= maxValue) {
                currentConsumables["external_buff"][buffName].push(nextTimerValue);
                nextTimerValue += buffCooldown;
            };
            
            updateCharacter({
                consumables: currentConsumables
            });
        } else {
            updateTimerValues(buffName, "external_buff");
        };
    });

    let value = 0;
    addTimerButton.addEventListener("click", () => {
        const timer = createElement("div", `option-image-button ${formattedBuffName}-timer`, null);
        const timerInput = createElement("input", "external-buff-timer-input", null);
        timerInput.value = value += buffCooldown;
        timerInput.addEventListener("input", (e) => {
            updateTimerValues(buffName, "external_buff");
        });
        timer.appendChild(timerInput);
        container.appendChild(timer);
        updateTimerValues(buffName, "external_buff");
    });
};

createExternalBuffTimers("Power Infusion", 120);
createExternalBuffTimers("Innervate", 180);

const createPotionTimers = (potionName, potionCooldown) => {
    const formattedPotionName = potionName.replaceAll(" ", "-").toLowerCase();

    const container = document.getElementById(`${formattedPotionName}-container`);
    const repeatButton = document.getElementById(`${formattedPotionName}-repeat-button`);
    const addTimerButton = document.getElementById(`${formattedPotionName}-add-timer-button`);
    const firstTimerInput = container.querySelectorAll(".potion-timer-input")[0];
    firstTimerInput.addEventListener("input", (e) => {
        if (!repeatButton.classList.contains("potion-repeating")) {
            updateTimerValues(potionName, "potion");
        } else {
            const maxValue = 600;
            const firstTimerInputValue = parseFloat(firstTimerInput.value);
            currentConsumables["potion"][potionName] = [firstTimerInputValue];

            let nextTimerValue = parseFloat(firstTimerInputValue) + potionCooldown;
            while (nextTimerValue <= maxValue) {
                currentConsumables["potion"][potionName].push(nextTimerValue);
                nextTimerValue += potionCooldown;
            };

            updateCharacter({
                consumables: currentConsumables
            });
        };
    });

    repeatButton.addEventListener("click", () => {
        repeatButton.classList.toggle("potion-repeating");
        addTimerButton.style.pointerEvents = repeatButton.classList.contains("potion-repeating") ? "none" : "all";
        addTimerButton.style.color = repeatButton.classList.contains("potion-repeating") ? "#808080" : "var(--light-font-colour)";
        const timers = container.querySelectorAll(`.${formattedPotionName}-timer`);
        timers.forEach((timer, index) => {
            if (index > 0) {
                timer.style.display = repeatButton.classList.contains("potion-repeating") ? "none" : "flex";
            };
        });

        if (repeatButton.classList.contains("potion-repeating")) {
            const maxValue = 600;
            const firstTimerInputValue = parseFloat(firstTimerInput.value);
            currentConsumables["potion"][potionName] = [firstTimerInputValue];

            // let nextTimerValue = parseFloat(firstTimerInputValue) + potionCooldown;
            // while (nextTimerValue <= maxValue) {
            //     currentConsumables["potion"][potionName].push(nextTimerValue);
            //     nextTimerValue += potionCooldown;
            // };

            updateCharacter({
                consumables: currentConsumables
            });

            addPotionToPriorityList(potionName, currentConsumables["potion"][potionName], true);
        } else {
            updateTimerValues(potionName, "potion");
        };
    });

    let value = 0;
    addTimerButton.addEventListener("click", () => {
        const timer = createElement("div", `option-image-button ${formattedPotionName}-timer`, null);
        const timerInput = createElement("input", "potion-timer-input", null);
        timerInput.value = value += potionCooldown;
        timerInput.addEventListener("input", (e) => {
            updateTimerValues(potionName, "potion");
        });
        timer.appendChild(timerInput);
        container.appendChild(timer);
        updateTimerValues(potionName, "potion");
    });
};

createPotionTimers("Aerated Mana Potion", 300);
createPotionTimers("Elemental Potion of Ultimate Power", 300);

// option sliders
createOptionsSliders();

// equipment display
initialiseEquipment();

// priority list display
createPriorityListDisplay();

// prevent forbidden cursor
document.addEventListener("dragenter", (e) => {
    e.preventDefault();
});

// initialise tabs for primary navbar
handleTabs(`options-navbar-1`, "options-tab-content");

export { updateCharacter, formatNumbers, formatNumbersNoRounding, formatThousands, formatTime, createElement, updateStats };