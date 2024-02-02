// TO DOS
// colour spell names by spell type
// change awakening triggers on the graph using the cooldown data instead

import { createAbilityBreakdown } from "./ability-breakdown.js";
import { createBuffsBreakdown } from "./buffs-breakdown.js";
import { createResourcesBreakdown } from "./resources-breakdown.js";
import { createPriorityBreakdown } from "./priority-breakdown.js";
import { createCooldownsBreakdown } from "./cooldowns-breakdown.js";
import { handleTabs } from "./simulation-options-tabs.js";
import { setSimulationOptionsFromImportedData } from "./simulation-options.js";
import { createTalentGrid, updateTalentsFromImportedData } from "./talent-grid.js";
import { formatNumbers, formatNumbersNoRounding, formatTime, formatThousands, makeFieldEditable } from "../utils/misc-functions.js";

// window.addEventListener("mouseover", (e) => {
//     console.log(e.target)
// })

// window.addEventListener("click", (e) => {
//     console.log(e.target)
// })

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
const socket = io("http://localhost:5000");

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
let lastSliderChange = null;
let isSimulationRunning = false;

// save states for use in separate priority breakdowns
export let cooldownFilterState = {};
export let playerAurasFilterState = {};

const importButton = document.getElementById("import-button");
const raceOption = document.getElementById("race-filter");

const simulationName = document.getElementById("simulation-name-text-input");
simulationName.value = "Simulation 1";

const simulateButton = document.getElementById("simulate-button");
const simulationProgressBarContainer = document.getElementById("simulation-progress-bar-container");
const simulationProgressBar = document.getElementById("simulation-progress-bar");
const simulationProgressBarText = document.getElementById("simulation-progress-bar-text");

const fullResultsContainer = document.getElementById("results-container");

document.addEventListener("DOMContentLoaded", () => {
    createTalentGrid();
});

// increment the percentage on the progress bar when the server sends an iteration update
socket.on("iteration_update", function(data) {
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
        updateUIAfterImport(data);
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

const runSimulation = async () => {
    encounterLength = document.getElementById("encounter-length-option").value;

    if (lastSliderChange === "Slider") {
        iterations = roundIterations(document.getElementById("iterations-option").value);
    } else {
        iterations = document.getElementById("iterations-option").value;
    };
    
    console.log("iterations", iterations)
    const timeWarpTime = document.getElementById("time-warp-time").value;

    simulationProgressBarContainer.style.opacity = "100";

    isSimulationRunning = true;

    return fetch(`http://127.0.0.1:5000/run_simulation?encounter_length=${encounterLength}&iterations=${iterations}&
                  time_warp_time=${timeWarpTime}`, {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        let simulationData = data;     
        console.log(simulationData)
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
    resultArrowIconContainer.addEventListener("click", (e) => {
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
    });
    leftSideContainer.appendChild(resultArrowIconContainer);

    // auto-generate new title if no input given
    const resultText = createElement("div", `result-text-${containerCount}`, null);
    resultText.textContent = simulationName.value;
    if (simulationName.value.includes (`Simulation ${containerCount}`)) {
        simulationName.value = `Simulation ${containerCount + 1}`;
    };

    // allow editing of title
    makeFieldEditable(resultText);
    leftSideContainer.appendChild(resultText);

    // add a display for hps, encounter length, and iterations
    const resultDetailsContainer = createElement("div", `result-details-container-${containerCount}`, null);
    const resultHPS = createElement("div", `result-details-hps-${containerCount}`, null);
    resultHPS.innerHTML = `<span>HPS: </span><span style="color: var(--healing-font)">${formatThousands(simulationData.simulation_details.average_hps)}</span>`;
    resultDetailsContainer.appendChild(resultHPS);

    const resultEncounterLength = createElement("div", `result-details-encounter-length-${containerCount}`, null);
    resultEncounterLength.innerHTML = `<span>Length: </span><span style="color: var(--holy-font)">${formatTime(simulationData.simulation_details.encounter_length)}</span>`;
    resultDetailsContainer.appendChild(resultEncounterLength);

    const resultIterations = createElement("div", `result-details-iterations-${containerCount}`, null);
    resultIterations.innerHTML = `<span>Iterations: </span><span style="color: var(--paladin-font)">${simulationData.simulation_details.iterations}</span>`
    
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

    resultsNavbar.appendChild(healingTab);
    resultsNavbar.appendChild(buffsWindowTab);
    resultsNavbar.appendChild(resourcesTab);
    resultsNavbar.appendChild(priorityTab);
    resultsNavbar.appendChild(cooldownsTab);
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

    // initialise tabs within the results
    handleTabs(`results-navbar-${containerCount}`, `results-tab-content-${containerCount}`, containerCount);
    handleTabs(`buffs-line-graph-navbar-${containerCount}`, `buffs-line-graph-tab-content-${containerCount}`, containerCount);
};

// update the paladin class when attributes are changed
const handleRaceChange = (race) => {
    updateCharacter({
        race: race.race
    });
};

let currentConsumables = {
    flask: [],
    food: [],
    weapon_imbue: [],
    augment_rune: [],
    raid_buff: [],
    external_buff: []
};

const handleConsumableChange = (consumable) => {
    const attributeKey = Object.keys(consumable)[0];
    let attributeValue = consumable[attributeKey];

    if (consumable.remove) {
        currentConsumables[attributeKey] = currentConsumables[attributeKey].filter(item => item !== attributeValue);
    } else {
        if (!currentConsumables[attributeKey].includes(attributeValue)) {
            currentConsumables[attributeKey].push(attributeValue);
        };
    };

    updateCharacter({
        consumables: currentConsumables
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
simulationProgressBarContainer.addEventListener("click", runSimulation);

// allows options images to be clicked to change/toggle options
const handleOptionImages = (images, attribute, optionType, toggle = false, multipleAllowed = false) => {
    const formattedAttribute = attribute.replaceAll("-", "_");

    const handlerFunctions = {
        consumable: handleConsumableChange,
        race: handleRaceChange,
    };

    const handlerFunction = handlerFunctions[optionType];

    images.forEach(image => {
        image.classList.add(`${attribute}-unselected`);
        image.classList.remove(`${attribute}-selected`);
        image.addEventListener("click", (e) => {
            const attributeName = e.target.getAttribute(`data-${attribute}`);
            const isSelected = e.target.classList.contains(`${attribute}-selected`);

            if (multipleAllowed) {
                e.target.classList.toggle(`${attribute}-selected`);
                e.target.classList.toggle(`${attribute}-unselected`);
                handlerFunction({[formattedAttribute]: attributeName, remove: isSelected});
            } else {
                if (isSelected && toggle) {
                    e.target.classList.add(`${attribute}-unselected`);
                    e.target.classList.remove(`${attribute}-selected`);
                    handlerFunction({[formattedAttribute]: attributeName, remove: true});
                } else {
                    images.forEach(img => {
                        if (img.classList.contains(`${attribute}-selected`)) {
                            const prevAttributeName = img.getAttribute(`data-${attribute}`);
                            handlerFunction({[formattedAttribute]: prevAttributeName, remove: true});
                            img.classList.add(`${attribute}-unselected`);
                            img.classList.remove(`${attribute}-selected`);
                        };
                    });
                    e.target.classList.remove(`${attribute}-unselected`);
                    e.target.classList.add(`${attribute}-selected`);
                    handlerFunction({[formattedAttribute]: attributeName});
                };
            };
        });
    });
};

const raceImages = document.querySelectorAll(".race-image");
handleOptionImages(raceImages, "race", "race");

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

// option sliders
const updateSliderStep = (value, slider, sliderText) => {
    if (value < 100) {
        slider.step = 1;
        sliderText.textContent = value;
    } else {
        slider.step = 50;
        sliderText.textContent = roundIterations(value);
    };
};

const roundIterations = (number) => {
    if (number < 100) {
        return number
    } else {
        return Math.round(number / 10) * 10;
    };
};

// iterations slider
const iterationsSlider = document.getElementById("iterations-option");
const iterationsValue = document.getElementById("iterations-value");
const baseMaxIterations = 1001;

iterationsSlider.addEventListener("input", () => {
    iterationsSlider.max = baseMaxIterations;

    const value = iterationsSlider.value
    updateSliderStep(value, iterationsSlider, iterationsValue);
    lastSliderChange = "Slider";
});
iterationsValue.textContent = iterationsSlider.value;
makeFieldEditable(iterationsValue, 1, iterationsSlider);

iterationsValue.addEventListener("input", (e) => {
    iterationsSlider.max = baseMaxIterations;

    // reset step to 1 to allow setting any number
    iterationsSlider.step = 1;
    let newValue = Number(iterationsValue.textContent);

    if (newValue > baseMaxIterations) {
        iterationsSlider.max = newValue;
    };

    iterationsSlider.value = newValue;
    lastSliderChange = "Value";
});

// encounter length slider
const encounterLengthSlider = document.getElementById("encounter-length-option");
const encounterLengthMinutes = document.getElementById("encounter-length-minutes");
const encounterLengthSeconds = document.getElementById("encounter-length-seconds");
const baseMaxEncounterLength = 600;

const updateEncounterLengthDisplay = (secondsValue) => {
    const minutes = Math.floor(secondsValue / 60);
    const seconds = secondsValue % 60;
    encounterLengthMinutes.textContent = minutes;
    encounterLengthSeconds.textContent = seconds.toString().padStart(2, '0');
};

// initial display
updateEncounterLengthDisplay(parseInt(encounterLengthSlider.value, 10));

encounterLengthSlider.addEventListener("input", () => {
    encounterLengthSlider.max = baseMaxEncounterLength;
    updateEncounterLengthDisplay(parseInt(encounterLengthSlider.value, 10));
});

makeFieldEditable(encounterLengthMinutes, { charLimit: 2 });
makeFieldEditable(encounterLengthSeconds, { charLimit: 2 });

[encounterLengthMinutes, encounterLengthSeconds].forEach(field => {
    field.addEventListener("input", (e) => {
        const minutes = parseInt(encounterLengthMinutes.textContent, 10) || 0;
        const seconds = parseInt(encounterLengthSeconds.textContent, 10) || 0;
        let totalSeconds = (minutes * 60) + seconds;

        if (totalSeconds > baseMaxEncounterLength) {
            encounterLengthSlider.max = totalSeconds;
        } else {
            encounterLengthSlider.max = baseMaxEncounterLength;
        };

        encounterLengthSlider.value = totalSeconds;
    });
});

// initialise tabs for primary navbar
handleTabs(`options-navbar-1`, "options-tab-content");

export { updateCharacter, formatNumbers, formatNumbersNoRounding, formatThousands, formatTime, createElement };