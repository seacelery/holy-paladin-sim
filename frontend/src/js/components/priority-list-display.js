import { createElement, updatePriorityList } from "./index.js";
import { spellToIconsMap } from "../utils/spell-to-icons-map.js";

let draggedItem = null;
const transparentImage = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";

const createPriorityListItem = (index) => {
    const priorityListItemContainer = createElement("div", "priority-list-item-container", null);

    const priorityListItemNumber = createElement("div", "priority-list-item-number", null);
    priorityListItemNumber.textContent = index;
    priorityListItemContainer.appendChild(priorityListItemNumber);

    const priorityListItemIconContainer = createElement("div", "priority-list-item-icon-container", null);
    const priorityListItemIcon = createElement("img", "priority-list-item-icon", null);
    priorityListItemIcon.src = "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_questionmark.jpg";
    priorityListItemIconContainer.appendChild(priorityListItemIcon);
    priorityListItemContainer.appendChild(priorityListItemIconContainer);

    const priorityListItemAbility = createElement("div", "priority-list-item-ability", null);
    const priorityListItemAbilityText = createElement("textarea", "priority-list-item-ability-text", null);
    priorityListItemAbilityText.addEventListener("input", (e) => {
        let abilityText = e.target.value.split(" ");
        
        abilityText = abilityText.map(word => {
            if (!["of", "the"].includes(word)) {
                return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
            } else {
                return word;
            };
        });

        abilityText = abilityText.join(" ");

        if (spellToIconsMap.hasOwnProperty(abilityText)) {
            priorityListItemIcon.src = spellToIconsMap[abilityText];
            e.target.value = abilityText;
        } else {
            priorityListItemIcon.src = "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_questionmark.jpg";
        };

        updatePriorityList();
    });

    priorityListItemAbility.appendChild(priorityListItemAbilityText);
    priorityListItemContainer.appendChild(priorityListItemAbility);

    const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
    const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
    priorityListItemCondition.appendChild(priorityListItemConditionText);
    priorityListItemContainer.appendChild(priorityListItemCondition);

    const priorityListConditionButtonsContainer = createElement("div", "priority-list-buttons-container", null);
    const priorityListAndButton = createElement("div", "priority-list-and-button priority-list-button", null);
    priorityListAndButton.textContent = "AND";

    const priorityListOrButton = createElement("div", "priority-list-or-button priority-list-button", null);
    priorityListOrButton.textContent = "OR";

    priorityListConditionButtonsContainer.appendChild(priorityListAndButton);
    priorityListConditionButtonsContainer.appendChild(priorityListOrButton);
    priorityListItemContainer.appendChild(priorityListConditionButtonsContainer);

    const priorityListArrowButtonsContainer = createElement("div", "priority-list-buttons-container", null);
    const priorityListUpButton = createElement("div", "priority-list-up-button priority-list-button", null);
    const arrowUpIcon = createElement("i", "fa-solid fa-arrow-up", null);
    priorityListUpButton.appendChild(arrowUpIcon);

    const priorityListDownButton = createElement("div", "priority-list-down-button priority-list-button", null);
    const arrowDownIcon = createElement("i", "fa-solid fa-arrow-down", null);
    priorityListDownButton.appendChild(arrowDownIcon);

    priorityListArrowButtonsContainer.appendChild(priorityListUpButton);
    priorityListArrowButtonsContainer.appendChild(priorityListDownButton);
    priorityListItemContainer.appendChild(priorityListArrowButtonsContainer);

    const priorityListAddRemoveButtonsContainer = createElement("div", "priority-list-buttons-container", null);
    const priorityListAddItem = createElement("div", "priority-list-add-item priority-list-button", null);
    const plusIcon = createElement("i", "fa-solid fa-plus", null);
    priorityListAddItem.appendChild(plusIcon);

    const priorityListDeleteItem = createElement("div", "priority-list-delete-item priority-list-button", null);
    const deleteIcon = createElement("i", "fa-solid fa-xmark", null);
    priorityListDeleteItem.appendChild(deleteIcon);
    
    priorityListAddRemoveButtonsContainer.appendChild(priorityListAddItem);
    priorityListAddRemoveButtonsContainer.appendChild(priorityListDeleteItem);
    priorityListItemContainer.appendChild(priorityListAddRemoveButtonsContainer);

    const priorityListItemHandle = createElement("div", "priority-list-item-handle", null);
    const handleIcon = createElement("i", "fa-solid fa-grip", null);
    priorityListItemHandle.appendChild(handleIcon);
    priorityListItemContainer.appendChild(priorityListItemHandle);

    priorityListItemHandle.setAttribute("draggable", true);
    priorityListItemHandle.addEventListener("dragstart", (e) => handleDragStart(e, setDraggedItem, transparentImage));
    priorityListItemHandle.addEventListener("dragend", handleDragEnd);

    priorityListItemContainer.addEventListener("mouseover", (e) => {
        const buttons = priorityListItemContainer.querySelectorAll(".priority-list-button");
        buttons.forEach(button => {
            button.classList.add("buttons-visible");
        });
        priorityListItemHandle.classList.add("buttons-visible");
    });

    priorityListItemContainer.addEventListener("mouseout", (e) => {
        const buttons = priorityListItemContainer.querySelectorAll(".priority-list-button");
        buttons.forEach(button => {
            button.classList.remove("buttons-visible");
        });
        priorityListItemHandle.classList.remove("buttons-visible");
    });

    return priorityListItemContainer;
};

const updateIndices = () => {
    const items = document.querySelectorAll(".priority-list-item-container");
    items.forEach((item, index) => {
        const numberDisplay = item.querySelector(".priority-list-item-number");
        if (numberDisplay) {
            numberDisplay.textContent = index;
        };
    });
};

const adjustTextareaHeight = (element, originalLineHeight) => {
    element.style.lineHeight = originalLineHeight + "px";

    var lineHeight = parseInt(window.getComputedStyle(element).lineHeight);
    var numberOfLines = element.scrollHeight / lineHeight;

    if (numberOfLines <= 1) {
        element.style.lineHeight = "40px";
    } else {
        element.style.lineHeight = "20px";
    };
};

const handleDragStart = (e, setDraggedItem, transparentImage) => {
    let item = e.target.closest(".priority-list-item-container");

    item.classList.add("dragging");
    const buttons = item.querySelectorAll(".priority-list-button");
    const priorityListItemHandle = item.querySelectorAll(".priority-list-item-handle");
    buttons.forEach(button => {
        button.classList.add("buttons-dragging");
    });
    priorityListItemHandle.forEach(handle => {
        handle.classList.add("buttons-dragging");
    });

    var img = new Image();
    img.src = transparentImage;
    e.dataTransfer.setDragImage(img, 0, 0);

    setTimeout(() => e.target.classList.add("dragging"), 0);

    setDraggedItem(item);
};

const setDraggedItem = (item) => {
    draggedItem = item;
};

const handleDragOver = (e) => {
    e.preventDefault();

    const targetItem = e.target.closest(".priority-list-item-container");
    if (targetItem && targetItem !== draggedItem) {
        const targetRect = targetItem.getBoundingClientRect();
        const isBelowHalf = e.clientY > targetRect.top + (targetRect.height / 2);

        const priorityListItemsContainer = document.getElementById("priority-list-items-container");

        if (isBelowHalf) {
            priorityListItemsContainer.insertBefore(draggedItem, targetItem.nextSibling);
        } else {
            priorityListItemsContainer.insertBefore(draggedItem, targetItem);
        };
    };
};

const handleDrop = (e) => {
    e.preventDefault();
    draggedItem.classList.remove("dragging");
    updateIndices();
};

const handleDragEnd = (e) => {
    draggedItem.classList.remove("dragging");
    const buttons = draggedItem.querySelectorAll(".priority-list-button");
    const priorityListItemHandle = draggedItem.querySelectorAll(".priority-list-item-handle");
    buttons.forEach(button => {
        button.classList.remove("buttons-dragging");
    });
    priorityListItemHandle.forEach(handle => {
        handle.classList.remove("buttons-dragging");
    });
    updateIndices();
    updatePriorityList();
};

const createPriorityListDisplay = () => {
    const priorityListItemsContainer = document.getElementById("priority-list-items-container");
    priorityListItemsContainer.addEventListener("dragover", handleDragOver);
    priorityListItemsContainer.addEventListener("drop", handleDrop);

    const firstPriorityListItemContainer = document.querySelectorAll(".priority-list-item-container");
    const firstPriorityListItemIcon = document.getElementById("priority-list-item-icon");
    const firstPriorityListItemAbilityText = document.getElementById("priority-list-item-ability-text");
    firstPriorityListItemAbilityText.addEventListener("input", (e) => {
        let abilityText = e.target.value.split(" ");
            
        abilityText = abilityText.map(word => {
            if (!["of", "the"].includes(word)) {
                return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
            } else {
                return word;
            };
        });

        abilityText = abilityText.join(" ");

        if (spellToIconsMap.hasOwnProperty(abilityText)) {
            firstPriorityListItemIcon.src = spellToIconsMap[abilityText];
            firstPriorityListItemAbilityText.value = abilityText;
        } else {
            firstPriorityListItemIcon.src = "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_questionmark.jpg";
        };

        updatePriorityList();
    });

    const firstPriorityListItemConditionText = document.getElementById("priority-list-item-condition-text");
    firstPriorityListItemConditionText.addEventListener("input", (e) => {
        updatePriorityList();
    });
    
    const firstPriorityListItemHandle = document.getElementById("priority-list-item-handle");
    firstPriorityListItemContainer.forEach(item => {
        firstPriorityListItemHandle.setAttribute("draggable", true);
        firstPriorityListItemHandle.addEventListener("dragstart", (e) => handleDragStart(e, setDraggedItem, transparentImage));
        firstPriorityListItemHandle.addEventListener("dragend", handleDragEnd);

        item.addEventListener("mouseover", (e) => {
            const buttons = item.querySelectorAll(".priority-list-button");
            buttons.forEach(button => {
                button.classList.add("buttons-visible");
            });
            firstPriorityListItemHandle.classList.add("buttons-visible");
        });

        item.addEventListener("mouseout", (e) => {
            const buttons = item.querySelectorAll(".priority-list-button");
            buttons.forEach(button => {
                button.classList.remove("buttons-visible");
            });
            firstPriorityListItemHandle.classList.remove("buttons-visible");
        });
    });

    // add and condition
    priorityListItemsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("priority-list-and-button") || event.target.parentNode.classList.contains("priority-list-and-button")) {
            const item = event.target.closest(".priority-list-item-container");

            const currentConditions = item.querySelectorAll(".priority-list-item-condition");
            const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

            const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
            const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
            priorityListItemCondition.appendChild(priorityListItemConditionText);

            const priorityListAndButton = createElement("div", "priority-list-permanent-and-button priority-list-button", null);
            priorityListAndButton.textContent = "AND";
            priorityListAndButton.addEventListener("click", () => {
                priorityListItemCondition.remove();
                priorityListAndButton.remove();
            });

            item.insertBefore(priorityListItemCondition, lastCondition.nextSibling);
            item.insertBefore(priorityListAndButton, lastCondition.nextSibling);

            const originalLineHeight = parseInt(window.getComputedStyle(priorityListItemConditionText).lineHeight);
            priorityListItemConditionText.addEventListener("input", () => {
                adjustTextareaHeight(priorityListItemConditionText, originalLineHeight);
                updatePriorityList();
            });
            adjustTextareaHeight(priorityListItemConditionText, originalLineHeight);
        };
    });

    // add or condition
    priorityListItemsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("priority-list-or-button") || event.target.parentNode.classList.contains("priority-list-or-button")) {
            const item = event.target.closest(".priority-list-item-container");

            const currentConditions = item.querySelectorAll(".priority-list-item-condition");
            const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

            const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
            const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
            priorityListItemCondition.appendChild(priorityListItemConditionText);

            const priorityListOrButton = createElement("div", "priority-list-permanent-or-button priority-list-button", null);
            priorityListOrButton.textContent = "OR";
            priorityListOrButton.addEventListener("click", () => {
                priorityListItemCondition.remove();
                priorityListOrButton.remove();
            });

            item.insertBefore(priorityListItemCondition, lastCondition.nextSibling);
            item.insertBefore(priorityListOrButton, lastCondition.nextSibling);

            const originalLineHeight = parseInt(window.getComputedStyle(priorityListItemConditionText).lineHeight);
            priorityListItemConditionText.addEventListener("input", () => {
                adjustTextareaHeight(priorityListItemConditionText, originalLineHeight);
                updatePriorityList();
            });
            adjustTextareaHeight(priorityListItemConditionText, originalLineHeight);
        };
    });

    // add item
    priorityListItemsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("priority-list-add-item") || event.target.parentNode.classList.contains("priority-list-add-item")) {
            const item = event.target.closest(".priority-list-item-container");
            const index = Array.from(priorityListItemsContainer.children).indexOf(item);
            const newListItem = createPriorityListItem(index + 1);
            priorityListItemsContainer.insertBefore(newListItem, item.nextSibling);
            updateIndices();

            const newAbilityTextField = newListItem.querySelectorAll(".priority-list-item-ability-text");
            newAbilityTextField.forEach(field => {
                const originalLineHeight = parseInt(window.getComputedStyle(field).lineHeight);
                field.addEventListener("input", () => {
                    adjustTextareaHeight(field, originalLineHeight);
                    updatePriorityList();
                });
                adjustTextareaHeight(field, originalLineHeight);
            });

            const newConditionTextField = newListItem.querySelectorAll(".priority-list-item-condition-text");
            newConditionTextField.forEach(field => {
                const originalLineHeight = parseInt(window.getComputedStyle(field).lineHeight);
                field.addEventListener("input", () => {
                    adjustTextareaHeight(field, originalLineHeight);
                    updatePriorityList();
                });
                adjustTextareaHeight(field, originalLineHeight);
            });
        };
    });

    // delete item
    priorityListItemsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("priority-list-delete-item") || event.target.parentNode.classList.contains("priority-list-delete-item")) {
            const item = event.target.closest(".priority-list-item-container");
            priorityListItemsContainer.removeChild(item);
            updateIndices();
        };
    });

    // move item
    priorityListItemsContainer.addEventListener("click", function(event) {
        const item = event.target.closest(".priority-list-item-container");
        if (!item) return;

        if (event.target.classList.contains("priority-list-up-button") || event.target.parentNode.classList.contains("priority-list-up-button")) {
            const previousItem = item.previousElementSibling;
            if (previousItem) {
                priorityListItemsContainer.insertBefore(item, previousItem);
                updateIndices();
            };
        } else if (event.target.classList.contains("priority-list-down-button") || event.target.parentNode.classList.contains("priority-list-down-button")) {
            const nextItem = item.nextElementSibling;
            if (nextItem) {
                priorityListItemsContainer.insertBefore(nextItem, item);
                updateIndices();
            };
        };
        updatePriorityList();
    });

    // adjust text area
    document.querySelectorAll(".priority-list-item-ability-text").forEach((element) => {
        const originalLineHeight = parseInt(window.getComputedStyle(element).lineHeight);
        element.addEventListener("input", () => {
            adjustTextareaHeight(element, originalLineHeight);
        });
        adjustTextareaHeight(element, originalLineHeight);
    });

    document.querySelectorAll(".priority-list-item-condition-text").forEach((element) => {
        const originalLineHeight = parseInt(window.getComputedStyle(element).lineHeight);
        element.addEventListener("input", () => {
            adjustTextareaHeight(element, originalLineHeight);
        });
        adjustTextareaHeight(element, originalLineHeight);
    });
};


export { createPriorityListItem, updateIndices, adjustTextareaHeight, setDraggedItem, handleDragStart, handleDragEnd, handleDragOver, handleDrop, createPriorityListDisplay };