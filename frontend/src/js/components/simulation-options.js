import { flasks, foodItems, weaponImbues, augmentRunes, raidBuffs, externalBuffs, potions } from "../utils/data/buffs-consumables-data.js";
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

const generateBuffsConsumablesImages = () => {
    const flaskFilterContainer = document.getElementById("flask-filter-container");
    for (const flask in flasks) {
        const flaskImage = createElement("img", "flask-image", null);
        flaskImage.src = flasks[flask].image;
        flaskImage.setAttribute("data-flask", flask);
        flaskFilterContainer.appendChild(flaskImage);
    };

    const foodFilterContainer = document.getElementById("food-filter-container");
    for (const food in foodItems) {
        const foodImage = createElement("img", "food-image", null);
        foodImage.src = foodItems[food].image;
        foodImage.setAttribute("data-food", food);
        foodFilterContainer.appendChild(foodImage);
    };

    const weaponImbueFilterContainer = document.getElementById("weapon-imbue-filter-container");
    for (const weaponImbue in weaponImbues) {
        const weaponImbueImage = createElement("img", "weapon-imbue-image", null);
        weaponImbueImage.src = weaponImbues[weaponImbue].image;
        weaponImbueImage.setAttribute("data-weapon-imbue", weaponImbue);
        weaponImbueFilterContainer.appendChild(weaponImbueImage);
    };

    const augmentRuneFilterContainer = document.getElementById("augment-rune-filter-container");
    for (const augmentRune in augmentRunes) {
        const augmentRuneImage = createElement("img", "augment-rune-image", null);
        augmentRuneImage.src = augmentRunes[augmentRune].image;
        augmentRuneImage.setAttribute("data-augment-rune", augmentRune);
        augmentRuneFilterContainer.appendChild(augmentRuneImage);
    };

    const manaPotionContainer = document.getElementById("aerated-mana-potion-container");
    const manaPotionImage = manaPotionContainer.querySelector(".potion-image");

    const intellectPotionContainer = document.getElementById("elemental-potion-of-ultimate-power-container");
    const intellectPotionImage = intellectPotionContainer.querySelector(".potion-image");

    const raidBuffsFilterContainer = document.getElementById("raid-buffs-filter-container");

    const powerInfusionContainer = document.getElementById("power-infusion-container");
    const powerInfusionImage = manaPotionContainer.querySelector(".external-buff-image");

    const innervateContainer = document.getElementById("innervate-container");
    const innervateImage = manaPotionContainer.querySelector(".external-buff-image");

    const sourceOfMagicContainer = document.getElementById("source-of-magic-container");
    const sourceOfMagicImage = manaPotionContainer.querySelector(".external-buff-image");
};

export { setSimulationOptionsFromImportedData, generateBuffsConsumablesImages };