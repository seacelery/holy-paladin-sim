import { ratingMultiplierByItemLevel, ratingMultiplierByItemLevelRingsNeck, ratingMultiplierStamina } from "./rating-multipliers.js";
import { itemSlotAllocations } from "./item-slot-allocations.js";

const calculateNewEffect = (effectsData, itemSlot, itemLevel, effectDescription) => {
    // let intellectAllocated = 5259;
    // let staminaAllocated = 7889;
    // let totalSecondariesAllocated = 7000;
    // let leechAllocated = 3000;

    // switch(true) {
    //     case ["trinket_1", "trinket_2"].includes(itemSlot):
    //         intellectAllocated = 6666;
    //         totalSecondariesAllocated = 6666;
    //         break;
    //     case ["finger_1", "finger_2", "neck"].includes(itemSlot):
    //         intellectAllocated = 0;
    //         totalSecondariesAllocated = 17500;
    //         break;
    //     case ["main_hand"].includes(itemSlot):
    //         intellectAllocated = 30629;
    //         break;
    //     case ["off_hand"].includes(itemSlot):
    //         intellectAllocated = 16132;
    //         break;
    //     default:
    //         break;
    // };

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
                        case allocationType === 1:
                            slotAllocation = itemSlotAllocations[allocation][allocationType]
                            break;
                        case allocationType === "rating_multiplier":
                            slotAllocation = itemSlotAllocations[allocation][1] * ratingMultiplierByItemLevel[itemLevel];
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
            console.log(`effectValue ${effectValue}, scale factor ${scaleFactor}, base ilvl ${baseItemLevel}, new ilvl ${itemLevel}`)
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