import { ratingMultiplierByItemLevel, ratingMultiplierByItemLevelRingsNeck, ratingMultiplierStamina } from "./rating-multipliers.js";
import { itemSlotAllocations } from "./item-slot-allocations.js";
import { futurePatchSelected } from "../../components/config/version-config.js";

const calculateStatAllocations = (stats, itemSlot) => {
    console.log(itemSlot)
    // console.log(stats)

    let intellectAllocated = 0;
    let staminaAllocated = 0;
    let totalSecondariesAllocated = 0;
    let leechAllocated = 0;

    // if (futurePatchSelected) {
    //     intellectAllocated = 5259;
    //     staminaAllocated = 7889;
    //     totalSecondariesAllocated = 6640;
    //     leechAllocated = 3000;

    //     switch(true) {
    //         case ["trinket_1", "trinket_2"].includes(itemSlot):
    //             intellectAllocated = 6666;
    //             totalSecondariesAllocated = 6920;
    //             break;
    //         case ["finger_1", "finger_2", "neck"].includes(itemSlot):
    //             intellectAllocated = 0;
    //             totalSecondariesAllocated = 22600;
    //             break;
    //         case ["main_hand"].includes(itemSlot):
    //             intellectAllocated = 30629;
    //             totalSecondariesAllocated = 6400;
    //             break;
    //         case ["off_hand"].includes(itemSlot):
    //             intellectAllocated = 16132;
    //             totalSecondariesAllocated = 7250;
    //             break;
    //         case ["waist", "wrist", "feet"].includes(itemSlot):
    //             totalSecondariesAllocated = 6400;
    //             break;
    //         case ["back"].includes(itemSlot):
    //             totalSecondariesAllocated = 7250;
    //             break;
    //         default:
    //             break;
    //     };
    // } else {
        intellectAllocated = 5259;
        staminaAllocated = 7889;
        totalSecondariesAllocated = 7000;
        leechAllocated = 3000;

        switch(true) {
            case ["trinket_1", "trinket_2"].includes(itemSlot):
                intellectAllocated = 6666;
                totalSecondariesAllocated = 6666;
                break;
            case ["finger_1", "finger_2", "neck"].includes(itemSlot):
                intellectAllocated = 0;
                totalSecondariesAllocated = 17500;
                break;
            case ["main_hand"].includes(itemSlot):
                intellectAllocated = 30629;
                break;
            case ["off_hand"].includes(itemSlot):
                intellectAllocated = 16132;
                break;
            default:
                break;
        };
    // };

    const statAllocations = {};

    if ("stamina" in stats || "Stamina" in stats) {
        statAllocations["stamina"] = staminaAllocated;
    };

    if ("intellect" in stats || "Intellect" in stats) {
        statAllocations["intellect"] = intellectAllocated;
    };

    if (("leech" in stats && stats["leech"] > 0) || ("Leech" in stats && stats["Leech"] > 0)) {
        statAllocations["leech"] = leechAllocated;
    };

    const secondaryStats = Object.entries(stats).filter(([key]) => !["intellect", "leech", "stamina", "Intellect", "Leech", "Stamina", "combat_rating_sturdiness"].includes(key));
    secondaryStats.sort((a, b) => b[1] - a[1]);

    const numSecondaryStats = secondaryStats.length;

    if (numSecondaryStats === 1) {
        const [onlySecondaryName] = secondaryStats[0];
        statAllocations[onlySecondaryName] = totalSecondariesAllocated;
    } else if (numSecondaryStats > 1) {
        const [highestSecondaryName, highestSecondaryValue] = secondaryStats[0];
        const [lowestSecondaryName, lowestSecondaryValue] = secondaryStats[1];

        const ratio = highestSecondaryValue / lowestSecondaryValue;

        statAllocations[highestSecondaryName] = totalSecondariesAllocated / (ratio + 1) * ratio;
        statAllocations[lowestSecondaryName] = totalSecondariesAllocated / (ratio + 1);
    };

    return statAllocations;
};

const generateItemStats = (stats, itemSlot, itemLevel) => {
    let ratingMultiplier;
    let staminaMultiplier = ratingMultiplierStamina[itemLevel] ? ratingMultiplierStamina[itemLevel] : 1;

    if (["finger_1", "finger_2", "neck"].includes(itemSlot)) {
        ratingMultiplier = ratingMultiplierByItemLevelRingsNeck[itemLevel];
        staminaMultiplier /= 1.778;
    } else {
        ratingMultiplier = ratingMultiplierByItemLevel[itemLevel];
    };

    let slotAllocation;
    for (const allocation in itemSlotAllocations) {
        if (allocation == itemLevel) {
            switch (true) {
                case ["head", "chest", "legs"].includes(itemSlot):
                    slotAllocation = itemSlotAllocations[allocation]["1"];
                    break;
                case ["shoulder", "hands", "waist", "feet", "trinket_1", "trinket_2"].includes(itemSlot):
                    slotAllocation = itemSlotAllocations[allocation]["2"];
                    break;
                case ["back", "wrist", "neck", "finger_1", "finger_2"].includes(itemSlot):
                    slotAllocation = itemSlotAllocations[allocation]["3"];
                    break;
                case ["main_hand", "off_hand"].includes(itemSlot):
                    slotAllocation = itemSlotAllocations[allocation]["4"];
                    break;
                default:
                    slotAllocation = itemSlotAllocations[allocation]["1"];
            };
        };
    };

    const statAllocations = calculateStatAllocations(stats, itemSlot);

    const finalStats = {};
    
    for (const stat in statAllocations) {
        switch(true) {
            case ["intellect", "Intellect"].includes(stat):
                finalStats[stat] = Math.round(slotAllocation * statAllocations[stat] * 0.0001);
                break;
            case ["haste", "crit", "mastery", "versatility", "Haste", "Crit", "Mastery", "Versatility", "Critical Strike"].includes(stat):
                finalStats[stat] = Math.round(slotAllocation * statAllocations[stat] * 0.0001 * ratingMultiplier);
                break;
            case ["leech", "Leech"].includes(stat):
                finalStats[stat] = Math.round(slotAllocation * statAllocations[stat] * 0.0001 * ratingMultiplier);
                break;
            case ["stamina", "Stamina"].includes(stat):
                finalStats[stat] = Math.round(1612 * staminaMultiplier);
        };
    };

    return finalStats;
};

export { generateItemStats };