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
let isFirstImport = true;

// save states for use in separate priority breakdowns
export let cooldownFilterState = {};
export let playerAurasFilterState = {};

const importButtonMain = document.getElementById("import-button-main");
const importButton = document.getElementById("import-button");

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

const generateRealmOptions = () => {
    const characterRegionFieldMain = document.getElementById("character-region-input-main");
    const characterRealmFieldMain = document.getElementById("character-realm-input-main");
    const characterNameFieldMain = document.getElementById("character-name-input-main");
    characterNameFieldMain.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            characterNameFieldMain.value = characterNameFieldMain.value.charAt(0).toUpperCase() + characterNameFieldMain.value.slice(1).toLowerCase();
        };
    });

    realmList[characterRegionFieldMain.value].forEach(realm => {
        const realmOption = createElement("option", "realm-option", null);
        realmOption.textContent = realm;
        realmOption.name = realm;
        characterRealmFieldMain.appendChild(realmOption);
    });

    characterRegionFieldMain.addEventListener("input", (e) => {
        characterRealmFieldMain.innerHTML = "";
    
        realmList[e.target.value].forEach(realm => {
            const realmOption = createElement("option", "realm-option", null);
            realmOption.textContent = realm;
            realmOption.name = realm;
            characterRealmFieldMain.appendChild(realmOption);
        });
    });

    const characterRegionField = document.getElementById("character-region-input");
    const characterRealmField = document.getElementById("character-realm-input");
    const characterNameField = document.getElementById("character-name-input");
    characterNameField.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            characterNameField.value = characterNameField.value.charAt(0).toUpperCase() + characterNameField.value.slice(1).toLowerCase();
        };
    });
    
    characterRegionField.addEventListener("input", (e) => {
        characterRealmField.innerHTML = "";
    
        realmList[e.target.value].forEach(realm => {
            const realmOption = createElement("option", "realm-option", null);
            realmOption.textContent = realm;
            realmOption.name = realm;
            characterRealmField.appendChild(realmOption);
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
        characterRealm = document.getElementById("character-realm-input-main").value.toLowerCase().replaceAll(" ", "-");
    };
    if (!characterRegion) {
        characterRegion = document.getElementById("character-region-input-main").value.toLowerCase();
    };

    // characterName = "daisu";
    // characterRealm = "aszune";
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

    return fetch(`http://127.0.0.1:5000/import_character?character_name=${characterName}&realm=${characterRealm}&region=${characterRegion}`, {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
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
                    
                    if (!characterName) {
                        window.alert(`Character name missing`)
                    } else if (!characterRealm) {
                        window.alert(`Character realm missing`)
                    } else {
                        window.alert(`Character not found`)
                    };          
    });
};

const updateStats = async () => {
    let characterName = document.getElementById("character-name-input").value.toLowerCase();
    let characterRealm = document.getElementById("character-realm-input").value.toLowerCase().replaceAll(" ", "-");
    let characterRegion = document.getElementById("character-region-input").value.toLowerCase();

    // characterName = "daisu";
    // characterRealm = "aszune";
    const customEquipment = encodeURIComponent(JSON.stringify(generateFullItemData()["equipment"]));

    return fetch(`http://127.0.0.1:5000/fetch_updated_data?character_name=${characterName}&realm=${characterRealm}&custom_equipment=${customEquipment}&region=${characterRegion}`, {
        credentials: "include"
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

const runSimulation = async () => {
    encounterLength = document.getElementById("encounter-length-option").value;

    if (lastSliderChange === "Slider") {
        iterations = roundIterations(document.getElementById("iterations-option").value);
    } else {
        iterations = document.getElementById("iterations-option").value;
    };
    
    console.log("iterations", iterations)
    const timeWarpTime = document.getElementById("time-warp-time").value;
    console.log(timeWarpTime)

    simulationProgressBarContainer.style.opacity = "100";

    isSimulationRunning = true;

    const priorityListJson = encodeURIComponent(JSON.stringify(priorityList));

    const customEquipment = encodeURIComponent(JSON.stringify(generateFullItemData()["equipment"]));

    return fetch(`http://127.0.0.1:5000/run_simulation?encounter_length=${encounterLength}&iterations=${iterations}&time_warp_time=${timeWarpTime}&priority_list=${priorityListJson}&custom_equipment=${customEquipment}`, {
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

    resultHeader.scrollIntoView({ behavior: "smooth" });
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
    console.log(data);
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

generateRealmOptions();

// event listeners
importButtonMain.addEventListener("click", importCharacter);
importButton.addEventListener("click", importCharacter);
simulationProgressBarContainer.addEventListener("click", runSimulation);

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
                        repeatButton.style.display = "none";
                        addTimerButton.style.display = "none";
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
    encounterLengthSeconds.textContent = seconds.toString().padStart(2, "0");
};

// initial encounter length display
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