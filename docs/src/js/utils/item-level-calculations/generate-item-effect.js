import { ratingMultiplierByItemLevel, ratingMultiplierByItemLevelRingsNeck, ratingMultiplierStamina } from "./rating-multipliers.js";
import { itemSlotAllocations } from "./item-slot-allocations.js";

// scaling classes
// -1 = no_multiplier
// -7 = rating_multiplier
// -8 = flat_damage
// -9 = flat_healing

const calculateNewEffect = (effectsData, itemSlot, itemLevel, effectDescription) => {
    let newEffectsData = effectsData;
    let newValues = [];

    for (const effect in effectsData) {
        const effectData = effectsData[effect];
        const effectType = effectData["effect_type"];
        const effectValue = effectData["base_value"];

        if (effectType === "scalar") {
            // get slot allocation
            const allocationType = effectData["allocation_type"];
            let slotAllocation;
            for (const allocation in itemSlotAllocations) {
                if (allocation == itemLevel) {
                    switch (true) {
                        case allocationType === "no_multiplier":
                            slotAllocation = itemSlotAllocations[allocation]["1"];
                            break;
                        case allocationType === "rating_multiplier":
                            slotAllocation = itemSlotAllocations[allocation]["1"] * ratingMultiplierByItemLevel[itemLevel];
                            break
                        case allocationType === "rating_multiplier_jewellery":
                            slotAllocation = itemSlotAllocations[allocation]["1"] * ratingMultiplierByItemLevelRingsNeck[itemLevel];
                            break
                        case allocationType === "flat_healing":
                            slotAllocation = itemSlotAllocations[allocation]["6"];
                            break
                        case allocationType === "flat_damage":
                            slotAllocation = itemSlotAllocations[allocation]["5"];
                            break
                        default:
                            slotAllocation = itemSlotAllocations[allocation]["1"];
                    };
                };
            };

            const newValue = Math.round(slotAllocation * effectData["effect_coefficient"]);
            newValues.push(newValue);

        } else if (effectType === "linear") {
            const scaleFactor = effectData["scale_factor"];
            const baseItemLevel = effectData["base_item_level"];
            const newValue = Math.round(effectValue + scaleFactor * (itemLevel - baseItemLevel));
            newValues.push(newValue);
        };
    };

    for (let i = 0; i < newValues.length; i++) {
        newEffectsData[i]["base_value"] = newValues[i];
        newEffectsData[i]["base_item_level"] = itemLevel;
    };

    const replacementIterator = newValues[Symbol.iterator]();
    const newDescription = effectDescription.replace(/\*(\d+(,\d+)?(\.\d+)?)/g, (match) => {
        const nextValue = replacementIterator.next().value;
        return nextValue !== undefined ? `*${nextValue}` : match;
    });

    return { newEffectsData, newDescription };
};

const generateItemEffects = (effects, itemSlot, itemLevel) => {
    effects.forEach((effectData, index) => {
        if (effectData["effect_values"]) {
            const { newEffectsData, newDescription } = calculateNewEffect(effectData["effect_values"], itemSlot, itemLevel, effectData["description"]);
            effects[index]["effect_values"] = newEffectsData;
            effects[index]["description"] = newDescription;
        };
    });

    return effects;
};

export { generateItemEffects };