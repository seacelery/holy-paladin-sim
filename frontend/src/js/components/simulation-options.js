import { flasks, foodItems, weaponImbues, augmentRunes, raidBuffs, externalBuffs, potions } from "../utils/data/buffs-consumables-data.js";
import { createTooltip, addTooltipFunctionality } from "../utils/misc-functions.js";
import { createElement } from "./index.js";

const setSimulationOptionsFromImportedData = (importedData) => {
    const importedRace = importedData.race;

    const raceImages = document.querySelectorAll(".race-image");
    raceImages.forEach(image => {
        if (image.getAttribute("data-race") === importedRace) {
            image.classList.remove("race-unselected");
            image.classList.add("race-selected");
        } else {
            image.classList.add("race-unselected");
            image.classList.remove("race-selected");
        };
    });
};

const colourStatWords = (text) => {
    let words = ["intellect", "haste", "crit", "mastery", "versatility", "critical strike", "leech", "healing", "damage", "mana"];
    let styledText = text;

    words.forEach(word => {
        let colourVariable = `var(--stat-${word.toLowerCase()})`;
        if (word === "critical strike") {
            colourVariable = "var(--stat-crit)";
        } else if (word === "healing") {
            colourVariable = "var(--healing-font)";
        } else if (word === "damage") {
            colourVariable = "var(--red-font-hover)";
        } else if (word === "mana") {
            colourVariable = "var(--mana)";
        };

        const regex = new RegExp(`\\b${word}\\b`, "gi");
        styledText = styledText.replace(regex, (match) => `<span style="color: ${colourVariable}">${match}</span>`);
});

    return styledText;
};

const generateBuffsConsumablesImages = () => {
    const flaskFilterContainer = document.getElementById("flask-filter-container");
    const flaskTooltip = createTooltip("flask-tooltip", "option-image-tooltip");

    for (const flask in flasks) {
        const flaskImage = createElement("img", "flask-image", null);
        flaskImage.src = flasks[flask].image;
        flaskImage.draggable = false;
        flaskImage.setAttribute("data-flask", flask);
        flaskFilterContainer.appendChild(flaskImage);

        const flaskInnerHTML = `${flask}<br><br>` + colourStatWords(flasks[flask].effect);
        addTooltipFunctionality(flaskImage, flaskTooltip, null, flaskInnerHTML);
    };

    const foodFilterContainer = document.getElementById("food-filter-container");
    const foodTooltip = createTooltip("food-tooltip", "option-image-tooltip");
    for (const food in foodItems) {
        const foodImage = createElement("img", "food-image", null);
        foodImage.src = foodItems[food].image;
        foodImage.draggable = false;
        foodImage.setAttribute("data-food", food);
        foodFilterContainer.appendChild(foodImage);

        const foodInnerHTML = `${food}<br><br>` + colourStatWords(foodItems[food].effect);
        addTooltipFunctionality(foodImage, foodTooltip, null, foodInnerHTML);
    };

    const weaponImbueFilterContainer = document.getElementById("weapon-imbue-filter-container");
    const weaponImbueTooltip = createTooltip("weapon-imbue-tooltip", "option-image-tooltip");
    for (const weaponImbue in weaponImbues) {
        const weaponImbueImage = createElement("img", "weapon-imbue-image", null);
        weaponImbueImage.src = weaponImbues[weaponImbue].image;
        weaponImbueImage.draggable = false;
        weaponImbueImage.setAttribute("data-weapon-imbue", weaponImbue);
        weaponImbueFilterContainer.appendChild(weaponImbueImage);

        const weaponImbueInnerHTML = `${weaponImbue}<br><br>` + colourStatWords(weaponImbues[weaponImbue].effect);
        addTooltipFunctionality(weaponImbueImage, weaponImbueTooltip, null, weaponImbueInnerHTML);
    };

    const augmentRuneFilterContainer = document.getElementById("augment-rune-filter-container");
    const augmentRuneTooltip = createTooltip("augment-rune-tooltip", "option-image-tooltip");
    for (const augmentRune in augmentRunes) {
        const augmentRuneImage = createElement("img", "augment-rune-image", null);
        augmentRuneImage.src = augmentRunes[augmentRune].image;
        augmentRuneImage.draggable = false;
        augmentRuneImage.setAttribute("data-augment-rune", augmentRune);
        augmentRuneFilterContainer.appendChild(augmentRuneImage);

        const augmentRuneInnerHTML = `${augmentRune}<br><br>` + colourStatWords(augmentRunes[augmentRune].effect);
        addTooltipFunctionality(augmentRuneImage, augmentRuneTooltip, null, augmentRuneInnerHTML);
    };

    const manaPotionContainer = document.getElementById("aerated-mana-potion-container");
    const manaPotionTooltip = createTooltip("mana-potion-tooltip", "option-image-tooltip");
    const manaPotionImage = manaPotionContainer.querySelector(".potion-image");
    manaPotionImage.src = potions["Aerated Mana Potion"].image;
    manaPotionImage.draggable = false;
    manaPotionImage.setAttribute("data-potion", "Aerated Mana Potion");

    const manaPotionInnerHTML = `Aerated Mana Potion<br><br>` + colourStatWords(potions["Aerated Mana Potion"].effect);
    addTooltipFunctionality(manaPotionImage, manaPotionTooltip, null, manaPotionInnerHTML);

    const intellectPotionContainer = document.getElementById("elemental-potion-of-ultimate-power-container");
    const intellectPotionTooltip = createTooltip("intellect-potion-tooltip", "option-image-tooltip");
    const intellectPotionImage = intellectPotionContainer.querySelector(".potion-image");
    intellectPotionImage.src = potions["Elemental Potion of Ultimate Power"].image;
    intellectPotionImage.draggable = false;
    intellectPotionImage.setAttribute("data-potion", "Elemental Potion of Ultimate Power");

    const intellectPotionInnerHTML = `Elemental Potion of Ultimate Power<br><br>` + colourStatWords(potions["Elemental Potion of Ultimate Power"].effect);
    addTooltipFunctionality(intellectPotionImage, intellectPotionTooltip, null, intellectPotionInnerHTML);

    const raidBuffsFilterContainer = document.getElementById("raid-buffs-filter-container");
    const raidBuffTooltip = createTooltip("raid-buff-tooltip", "option-image-tooltip");
    for (const raidBuff in raidBuffs) {
        const raidBuffImage = createElement("img", "raid-buff-image", null);
        raidBuffImage.src = raidBuffs[raidBuff].image;
        raidBuffImage.draggable = false;
        raidBuffImage.setAttribute("data-raid-buff", raidBuff);
        raidBuffsFilterContainer.appendChild(raidBuffImage);

        const raidBuffsInnerHTML = `${raidBuff}<br><br>` + colourStatWords(raidBuffs[raidBuff].effect);
        addTooltipFunctionality(raidBuffImage, raidBuffTooltip, null, raidBuffsInnerHTML);
    };

    const powerInfusionContainer = document.getElementById("power-infusion-container");
    const powerInfusionTooltip = createTooltip("power-infusion-tooltip", "option-image-tooltip");
    const powerInfusionImage = powerInfusionContainer.querySelector(".external-buff-image");
    powerInfusionImage.src = externalBuffs["Power Infusion"].image;
    powerInfusionImage.draggable = false;
    powerInfusionImage.setAttribute("data-external-buff", "Power Infusion");

    const powerInfusionInnerHTML = `Power Infusion<br><br>` + colourStatWords(externalBuffs["Power Infusion"].effect);
    addTooltipFunctionality(powerInfusionImage, powerInfusionTooltip, null, powerInfusionInnerHTML);

    const innervateContainer = document.getElementById("innervate-container");
    const innervateTooltip = createTooltip("innervate-tooltip", "option-image-tooltip");
    const innervateImage = innervateContainer.querySelector(".external-buff-image");
    innervateImage.src = externalBuffs["Innervate"].image;
    innervateImage.draggable = false;
    innervateImage.setAttribute("data-external-buff", "Innervate");

    const innervateInnerHTML = `Innervate<br><br>` + colourStatWords(externalBuffs["Innervate"].effect);
    addTooltipFunctionality(innervateImage, innervateTooltip, null, innervateInnerHTML);

    const sourceOfMagicContainer = document.getElementById("source-of-magic-container");
    const sourceOfMagicTooltip = createTooltip("source-of-magic-tooltip", "option-image-tooltip");
    const sourceOfMagicImage = sourceOfMagicContainer.querySelector(".external-buff-image");
    sourceOfMagicImage.src = externalBuffs["Source of Magic"].image;
    sourceOfMagicImage.draggable = false;
    sourceOfMagicImage.setAttribute("data-external-buff", "Source of Magic");

    const sourceOfMagicInnerHTML = `Source of Magic<br><br>` + colourStatWords(externalBuffs["Source of Magic"].effect);
    addTooltipFunctionality(sourceOfMagicImage, sourceOfMagicTooltip, null, sourceOfMagicInnerHTML);
};

export { setSimulationOptionsFromImportedData, generateBuffsConsumablesImages };