import itemDataEffects from "../utils/data/item-data-effects.js";
import { generateItemEffects } from "./item-level-calculations/generate-item-effect.js";

const formatNumbers = (number) => {
    return Math.round(number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const formatNumbersNoRounding = (number) => {
    const parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
};

const formatThousands = (number) => {
    if (number >= 1000) {
        return (number / 1000).toFixed(1) + "K";
    } else {
        return number.toString();
    };
};

const formatTime = (seconds) => {
    let minutes = Math.floor(seconds / 60);
    let remainingSeconds = Math.round(seconds % 60);

    if (remainingSeconds === 60) {
        minutes += 1;
        remainingSeconds = 0;
    };

    return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
};

const makeFieldEditable = (field, {defaultValue = null, fieldSlider = null, charLimit = null} = {}) => {
    field.addEventListener("click", (e) => {
        e.target.setAttribute("contenteditable", "true");
        e.target.focus();
    });
    
    field.addEventListener("blur", (e) => {
        if (!e.target.textContent.trim() && defaultValue !== null) {
            e.target.textContent = defaultValue;

            if (field.id === "iterations-value") {
                fieldSlider.step = 1;
                fieldSlider.value = defaultValue;
            };
        };

        if (e.target.id === "encounter-length-seconds" && e.target.textContent === "") {
            e.target.textContent = "00";
        };

        if (e.target.id === "encounter-length-minutes" && e.target.textContent === "") {
            e.target.textContent = "0";
        };

        if (e.target.id === "encounter-length-seconds" && Number(e.target.textContent) > 59) {
            const remainder = Number(e.target.textContent) - 60;
            e.target.textContent = "00";
            const encounterLengthMinutes = document.getElementById("encounter-length-minutes");
            encounterLengthMinutes.textContent = Number(encounterLengthMinutes.textContent) + 1;
            const encounterLengthSeconds = document.getElementById("encounter-length-seconds");
            encounterLengthSeconds.textContent = remainder > 9 ? remainder : "0" + remainder;
        };

        e.target.removeAttribute("contenteditable");
    });

    field.addEventListener("keydown", (e) => {
        if (field.id === "encounter-length-minutes" &&  e.key === "Tab") {
            e.preventDefault();
            e.target.removeAttribute("contenteditable");
    
            // set a timeout so the typing indicator shows up at the end
            setTimeout(() => {
                const encounterLengthSeconds = document.getElementById("encounter-length-seconds");
                encounterLengthSeconds.setAttribute("contenteditable", "true");
                encounterLengthSeconds.focus();
    
                if (encounterLengthSeconds.textContent) {
                    const range = document.createRange();
                    const sel = window.getSelection();
                    range.selectNodeContents(encounterLengthSeconds);
                    range.collapse(false);
                    sel.removeAllRanges();
                    sel.addRange(range);
                }
            }, 0);
        };

        if (e.key === "Enter") {
            if (!e.target.textContent.trim() && defaultValue !== null) {
                e.target.textContent = defaultValue;

                if (field.id === "iterations-value") {
                    fieldSlider.step = 1;
                    fieldSlider.value = defaultValue;
                };
            };

            if (e.target.id === "encounter-length-seconds" && e.target.textContent === "") {
                e.target.textContent = "00";
            };

            if (e.target.id === "encounter-length-minutes" && e.target.textContent === "") {
                e.target.textContent = "0";
            };

            if (e.target.id === "encounter-length-seconds" && Number(e.target.textContent) > 59) {
                const remainder = Number(e.target.textContent) - 60;
                e.target.textContent = "00";
                const encounterLengthMinutes = document.getElementById("encounter-length-minutes");
                encounterLengthMinutes.textContent = Number(encounterLengthMinutes.textContent) + 1;
                const encounterLengthSeconds = document.getElementById("encounter-length-seconds");
                encounterLengthSeconds.textContent = remainder > 9 ? remainder : "0" + remainder;
            };

            e.target.removeAttribute("contenteditable");
            e.preventDefault();
        };
    });

    // prevent time fields from having more than two characters
    field.addEventListener("input", (e) => {
        if (charLimit !== null && e.target.textContent.length > charLimit) {
            e.target.textContent = e.target.textContent.slice(0, charLimit);
        };
    });
};

const updateEquipmentWithEffectValues = (data) => {
    const equipmentData = data["equipment"];
    Object.keys(equipmentData).forEach(slot => {
        const equipmentPiece = equipmentData[slot];
        const enhancedItem = itemDataEffects.find(item => item.id === equipmentPiece.item_id);
        
        if (enhancedItem && enhancedItem.effects) {
            equipmentPiece.effects[0]["effect_values"] = enhancedItem.effects.map(effect => effect.effect_values)[0];
            equipmentPiece.effects[0]["description"] = enhancedItem.effects.map(effect => effect.description)[0];
        };
        
        equipmentPiece.effects = generateItemEffects(equipmentPiece.effects, slot, equipmentPiece.item_level);
    });
};

const createTooltip = (tooltipId, tooltipClass) => {
    const tooltip = document.createElement("div");
    tooltip.id = tooltipId;
    tooltip.classList.add(tooltipClass);

    tooltip.style.display = "none";
    tooltip.style.position = "absolute";
    document.body.appendChild(tooltip);

    return tooltip;
};

const addTooltipFunctionality = (container, tooltip, tooltipText=null, tooltipInnerHTML=null) => {
    container.addEventListener("mousemove", (e) => {
        const xOffset = 15;
        const yOffset = 15;
    
        tooltip.style.left = e.pageX + xOffset + "px";
        tooltip.style.top = e.pageY + yOffset + "px";
    
        tooltip.style.display = "block";
    
        tooltip.innerHTML = "";
        if (tooltipText) {
            tooltip.textContent = tooltipText;
        } else if (tooltipInnerHTML) {
            tooltip.innerHTML = tooltipInnerHTML;
        };
    });

    container.addEventListener("mouseleave", () => {
        tooltip.style.display = "none";
    });
};

export { formatNumbers, formatNumbersNoRounding, formatTime, formatThousands, makeFieldEditable, updateEquipmentWithEffectValues, createTooltip, addTooltipFunctionality };