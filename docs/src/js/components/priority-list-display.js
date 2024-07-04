import { createElement } from "./index.js";
import { spellToIconsMap } from "../utils/spell-to-icons-map.js";

let draggedItem = null;
const transparentImage = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";

const abilityNames = [
    "Holy Shock", "Holy Light", "Flash of Light", "Word of Glory", "Light of Dawn", "Divine Toll", 
    "Daybreak", "Holy Prism", "Beacon of Virtue", "Divine Favor", "Hand of Divinity",
    "Lay on Hands", "Blessing of the Seasons", "Tyr's Deliverance", "Aerated Mana Potion",
    "Elemental Potion of Ultimate Power", "Avenging Wrath", "Avenging Crusader", "Judgment",
    "Crusader Strike", "Consecration", "Barrier of Faith", "Aura Mastery", 
    "Hammer of Wrath", "Eternal Flame", "Ovinax's Mercurial Egg", "Treacherous Transmitter", 
    "Creeping Coagulum", "High Speaker's Accretion", "Siphoning Phylactery Shard", "Holy Armament",
    "Tempered Potion", "Algari Mana Potion", "Slumbering Soul Serum"
];

const abilityAutocomplete = (element, abilityNames, icon) => {
    const autocompleteContainer = createElement("ul", "ability-autocomplete-container", null);

    window.addEventListener("click", (e) => {
        if (e.target !== autocompleteContainer) {
            autocompleteContainer.innerHTML = "";
            autocompleteContainer.style.border = "none";
        };
    });

    element.addEventListener("input", () => {
        const input = element.value;
        const matchedAbilities = abilityNames.filter(abilityName => abilityName.toLowerCase().includes(input.toLowerCase()));
    
        autocompleteContainer.innerHTML = "";
        autocompleteContainer.style.border = "1px solid var(--border-colour-3)";
        autocompleteContainer.style.borderTop = "none";
    
        const elementRect = element.getBoundingClientRect();
        const parentRect = element.parentNode.getBoundingClientRect();
        
        autocompleteContainer.style.left = `${elementRect.left - parentRect.left - 1}px`;
        autocompleteContainer.style.top = `${elementRect.bottom - parentRect.top - 1}px`;
    
        matchedAbilities.forEach(abilityName => {
            const autocompleteSuggestion = createElement("li", "ability-autocomplete-suggestion", null);
            
            autocompleteSuggestion.textContent = abilityName;
            if (autocompleteSuggestion.textContent.length > 21 || autocompleteSuggestion.textContent === "Aerated Mana Potion") {
                autocompleteSuggestion.style.paddingTop = "5px";
            };
    
            autocompleteSuggestion.addEventListener("click", () => {
                element.value = abilityName;
                autocompleteContainer.style.border = "none";
    
                if (spellToIconsMap.hasOwnProperty(abilityName)) {
                    icon.src = spellToIconsMap[abilityName];
                    element.value = abilityName;
                } else {
                    icon.src = "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_questionmark.jpg";
                };
                autocompleteContainer.innerHTML = "";
                document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
                    adjustTextareaHeight(itemText, 40);
                });
                updatePriorityList();
            });
            autocompleteContainer.appendChild(autocompleteSuggestion);
        });
    });

    return autocompleteContainer;
};

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
            if (!["of", "the", "on"].includes(word)) {
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

    const abilityAutocompleteSuggestions = abilityAutocomplete(priorityListItemAbilityText, abilityNames, priorityListItemIcon);

    priorityListItemAbility.appendChild(priorityListItemAbilityText);
    priorityListItemContainer.appendChild(priorityListItemAbility);
    priorityListItemAbility.appendChild(abilityAutocompleteSuggestions);

    const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
    const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
    priorityListItemConditionText.addEventListener("input", () => {
        adjustTextareaHeight(priorityListItemConditionText, 40);
    });
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

    let lineHeight = parseInt(window.getComputedStyle(element).lineHeight);
    let numberOfLines = element.scrollHeight / lineHeight;

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
            if (!["of", "the", "on"].includes(word)) {
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

    const abilityText = document.getElementById("priority-list-item-ability-text");
    abilityText.spellcheck = false;
    const abilityAutocompleteSuggestions = abilityAutocomplete(abilityText, abilityNames, firstPriorityListItemIcon);
    document.querySelector(".priority-list-item-ability").appendChild(abilityAutocompleteSuggestions);

    const firstPriorityListItemConditionText = document.getElementById("priority-list-item-condition-text");
    firstPriorityListItemConditionText.spellcheck = false;
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
        if (event.target.classList.contains("priority-list-and-button") || (event.target.parentNode && event.target.parentNode.classList.contains("priority-list-and-button"))) {
            const item = event.target.closest(".priority-list-item-container");

            const currentConditions = item.querySelectorAll(".priority-list-item-condition");
            const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

            const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
            const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
            priorityListItemCondition.appendChild(priorityListItemConditionText);

            const priorityListAndButton = createElement("div", "priority-list-permanent-and-button priority-list-button priority-list-permanent-button", null);
            priorityListAndButton.textContent = "AND";
            priorityListAndButton.addEventListener("click", () => {
                priorityListItemCondition.remove();
                priorityListAndButton.remove();
                updatePriorityList();
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
        if (event.target.classList.contains("priority-list-or-button") || (event.target.parentNode && event.target.parentNode.classList.contains("priority-list-or-button"))) {
            const item = event.target.closest(".priority-list-item-container");

            const currentConditions = item.querySelectorAll(".priority-list-item-condition");
            const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

            const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
            const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
            priorityListItemCondition.appendChild(priorityListItemConditionText);

            const priorityListOrButton = createElement("div", "priority-list-permanent-or-button priority-list-button priority-list-permanent-button", null);
            priorityListOrButton.textContent = "OR";
            priorityListOrButton.addEventListener("click", () => {
                priorityListItemCondition.remove();
                priorityListOrButton.remove();
                updatePriorityList();
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
        if (event.target.classList.contains("priority-list-add-item") || (event.target.parentNode && event.target.parentNode.classList.contains("priority-list-add-item"))) {
            const item = event.target.closest(".priority-list-item-container");
            const index = Array.from(priorityListItemsContainer.children).indexOf(item);
            const newListItem = createPriorityListItem(index + 1);
            priorityListItemsContainer.insertBefore(newListItem, item.nextSibling);
            updateIndices();

            const deleteButtons = document.querySelectorAll(".priority-list-delete-item");
            const disableDeleteButton = priorityListItemsContainer.children.length <= 1;
            deleteButtons.forEach(button => {
                button.classList.toggle("priority-list-button-disabled", disableDeleteButton);
            });

            const newAbilityTextField = newListItem.querySelectorAll(".priority-list-item-ability-text");
            newAbilityTextField.spellcheck = false;
            newAbilityTextField.forEach(field => {
                const originalLineHeight = parseInt(window.getComputedStyle(field).lineHeight);
                field.addEventListener("input", () => {
                    adjustTextareaHeight(field, originalLineHeight);
                    updatePriorityList();
                });
                adjustTextareaHeight(field, originalLineHeight);
            });

            const newConditionTextField = newListItem.querySelectorAll(".priority-list-item-condition-text");
            newConditionTextField.spellcheck = false;
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
        if (event.target.classList.contains("priority-list-delete-item") || (event.target.parentNode && event.target.parentNode.classList.contains("priority-list-delete-item"))) {
            const item = event.target.closest(".priority-list-item-container");
            priorityListItemsContainer.removeChild(item);

            const deleteButtons = document.querySelectorAll(".priority-list-delete-item");
            const disableDeleteButton = priorityListItemsContainer.children.length <= 1;

            deleteButtons.forEach(button => {
                button.classList.toggle("priority-list-button-disabled", disableDeleteButton);
            });

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

const convertPasteToPriorityList = (pastedCode) => {
    if (typeof pastedCode !== 'string' && !(pastedCode instanceof String)) return;
    
    const lines = pastedCode.split("\n");
    const priorityListItemsContainer = document.getElementById("priority-list-items-container");
    priorityListItemsContainer.innerHTML = "";
    for (const line in lines) {
        const lineData = lines[line];
        const pieces = lineData.split("|");
        const newItem = createPriorityListItem();

        for (const piece in pieces) {
            const pieceData = pieces[piece].trim();
            if (pieceData == pieces[0].trim()) {
                const abilityText = newItem.querySelector(".priority-list-item-ability-text");
                abilityText.spellcheck = false;
                const abilityIcon = newItem.querySelector(".priority-list-item-icon");
                abilityText.textContent = pieceData;

                if (spellToIconsMap.hasOwnProperty(abilityText.textContent)) {
                    abilityIcon.src = spellToIconsMap[abilityText.textContent];
                } else {
                    abilityIcon.src = "https://render.worldofwarcraft.com/eu/icons/56/inv_misc_questionmark.jpg";
                };

                abilityText.addEventListener("input", () => {
                    adjustTextareaHeight(abilityText, 40);
                    updatePriorityList();
                });

                if (abilityText.textContent.length > 25) {
                    adjustTextareaHeight(abilityText, 40);
                };

            } else if (pieceData == pieces[1].trim()) {
                const conditionText = newItem.querySelector(".priority-list-item-condition-text");
                conditionText.spellcheck = false;
                
                conditionText.textContent = pieceData;
                conditionText.addEventListener("input", () => {
                    adjustTextareaHeight(conditionText, 40);
                    updatePriorityList();
                });
                if (conditionText.textContent.length > 25) {
                    adjustTextareaHeight(conditionText, 40);
                };

            } else if (pieceData === "and") {
                const currentConditions = newItem.querySelectorAll(".priority-list-item-condition");
                const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

                const priorityListAndButton = createElement("div", "priority-list-permanent-and-button priority-list-button priority-list-permanent-button", null);
                priorityListAndButton.textContent = "AND";
            
                newItem.insertBefore(priorityListAndButton, lastCondition.nextSibling);
            } else if (pieceData === "or") {
                const currentConditions = newItem.querySelectorAll(".priority-list-item-condition");
                const lastCondition = currentConditions.length > 0 ? currentConditions[currentConditions.length - 1] : null;

                const priorityListOrButton = createElement("div", "priority-list-permanent-or-button priority-list-button priority-list-permanent-button", null);
                priorityListOrButton.textContent = "OR";

                newItem.insertBefore(priorityListOrButton, lastCondition.nextSibling);
            } else {
                const priorityListItemCondition = createElement("div", "priority-list-item-condition", null);
                const priorityListItemConditionText = createElement("textarea", "priority-list-item-condition-text", null);
                priorityListItemConditionText.textContent = pieceData;
                priorityListItemCondition.appendChild(priorityListItemConditionText);

                const currentOperators = newItem.querySelectorAll(".priority-list-permanent-button");
                const lastCondition = currentOperators.length > 0 ? currentOperators[currentOperators.length - 1] : null;

                newItem.insertBefore(priorityListItemCondition, lastCondition.nextSibling);

                priorityListItemConditionText.addEventListener("input", () => {
                    adjustTextareaHeight(priorityListItemConditionText, 40);
                    updatePriorityList();
                });
                if (priorityListItemConditionText.textContent.length > 25) {
                    adjustTextareaHeight(priorityListItemConditionText, 40);
                };
            };

            const currentConditions = newItem.querySelectorAll(".priority-list-item-condition");
            if (currentConditions.length > 1) {
                const andButtons = newItem.querySelectorAll(".priority-list-permanent-and-button");
                andButtons.forEach(andButton => {
                    andButton.addEventListener("click", () => {
                        andButton.nextSibling.remove();
                        andButton.remove();
                        updatePriorityList();
                    });
                });

                const orButtons = newItem.querySelectorAll(".priority-list-permanent-or-button");
                orButtons.forEach(orButton => {
                    orButton.addEventListener("click", () => {
                        orButton.nextSibling.remove();
                        orButton.remove();
                        updatePriorityList();
                    });
                });
            };
        };

        priorityListItemsContainer.appendChild(newItem);
        updateIndices();
        updatePriorityList();
    };
};

let priorityList = [];
let priorityListPastedCode = "";

const updatePriorityList = () => {
    const priorityListItemContainers = document.querySelectorAll(".priority-list-item-container");
    priorityList = [];

    priorityListItemContainers.forEach(container => {
        let priorityString = "";

        const abilityInput = container.querySelector(".priority-list-item-ability-text");
        if (abilityInput) {
            priorityString += abilityInput.value;
        }

        const conditionElements = container.querySelectorAll(".priority-list-item-condition, .priority-list-permanent-and-button, .priority-list-permanent-or-button");
        conditionElements.forEach((element, index) => {
            if (element.classList.contains("priority-list-item-condition")) {
                const conditionText = element.querySelector(".priority-list-item-condition-text").value;
                if (conditionText) {
                    priorityString += ` | ${conditionText}`;
                };
            } else if (element.classList.contains("priority-list-permanent-and-button")) {
                priorityString += " | and";
            } else if (element.classList.contains("priority-list-permanent-or-button")) {
                priorityString += " | or";
            };
        });

        priorityList.push(priorityString);
    });
    priorityListPastedCode = priorityList
};

const priorityListPresetsButton = document.getElementById("priority-list-presets-icon");
const priorityListCopyButton = document.getElementById("priority-list-copy-icon");
const priorityListPasteButton = document.getElementById("priority-list-paste-icon");
const priorityListInfoButton = document.getElementById("priority-list-info-icon");

const priorityListCopyNotification = document.getElementById("priority-list-copy-notification");
priorityListCopyButton.addEventListener("click", () => {
    const priorityListString = priorityList.join("\n"); 
    priorityListPasteButton.classList.remove("priority-list-icon-active");

    navigator.clipboard.writeText(priorityListString).then(() => {
        console.log("Priority list copied to clipboard");
        priorityListCopyNotification.style.opacity = "1";
        setTimeout(() => {
            priorityListCopyNotification.style.opacity = "0";
        }, 2000);
    }).catch(err => {
        console.error("Failed to copy priority list to clipboard: ", err);
    });
});

const priorityListPresetsModal = document.getElementById("priority-list-presets-modal");
priorityListPresetsModal.style.display = "none";
priorityListPresetsButton.addEventListener("mousedown", () => {
    priorityListPresetsModal.style.display = priorityListPresetsModal.style.display === "none" ? "flex" : "none";
    priorityListPresetsButton.classList.toggle("priority-list-icon-active");
    priorityListPasteButton.classList.remove("priority-list-icon-active");
    priorityListInfoButton.classList.remove("priority-list-icon-active");
    if (priorityListPasteModal.style.display !== "none") {
        priorityListPasteModal.style.display = "none";
    };
    if (priorityListInfoModal.style.display !== "none") {
        priorityListInfoModal.style.display = "none";
    };
});

const beaconOfFaithPreset = document.getElementById("standard-beacon-of-faith-preset");
beaconOfFaithPreset.addEventListener("click", () => {
    priorityListPastedCode = `Algari Mana Potion | Timers = [30]
Blessing of the Seasons | Avenging Wrath (Awakening) not active | or | Avenging Wrath not active
Tyr's Deliverance | Avenging Wrath (Awakening) not active
Avenging Wrath | Divine Toll cooldown = 0 | and | Holy Power >= 3
Judgment | Awakening Ready active | and | Holy Power < 5
Holy Shock | Holy Shock charges = 2 | and | Rising Sunlight not active
Holy Shock | Holy Power <= 2 | and | Holy Shock charges = 2 | and | Rising Sunlight active
Holy Prism
Eternal Flame | Dawnlight active
Eternal Flame | Holy Power = 5 | and | Unending Light stacks = 9
Light of Dawn | Holy Power = 5
Eternal Flame | Holy Power >= 3 | and | Avenging Wrath active | and | Divine Toll cooldown = 0 | and | Unending Light stacks = 9
Eternal Flame | Holy Power >= 3 | and | Avenging Wrath (Awakening) active | and | Divine Toll cooldown = 0 | and | Unending Light stacks = 9
Light of Dawn | Holy Power >= 3 | and | Avenging Wrath active | and | Divine Toll cooldown = 0
Light of Dawn | Holy Power >= 3 | and | Avenging Wrath (Awakening) active | and | Divine Toll cooldown = 0
Divine Toll | Avenging Wrath active | or | Avenging Wrath (Awakening) active
Holy Shock | Holy Power <= 2 | and | Rising Sunlight active
Holy Shock | Holy Power < 5 | and | Rising Sunlight not active
Crusader Strike | Holy Power <= 3
Holy Light | Divine Favor active | and | Infusion of Light active
Holy Light | Infusion of Light active | and | Liberation active
Flash of Light | Infusion of Light active
Eternal Flame | Unending Light stacks = 9 | and
Judgment | Awakening Ready not active | and | Awakening stacks < 8
Light of Dawn
Hammer of Wrath
Arcane Torrent
Crusader Strike
Consecration`,
    convertPasteToPriorityList(priorityListPastedCode);
    document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    document.querySelectorAll(".priority-list-item-condition-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    updatePriorityList();
});

const beaconOfVirtuePreset = document.getElementById("standard-beacon-of-virtue-preset");
beaconOfVirtuePreset.addEventListener("click", () => {
    priorityListPastedCode = `Aerated Mana Potion | Timers = [30]
    Tyr's Deliverance
    Nymue's Unraveling Spindle | Timers = [12, 132, 268]
    Avenging Wrath | Timers = [15, 135, 271] | and | previous ability = Nymue's Unraveling Spindle
    Holy Prism
    Light's Hammer
    Beacon of Virtue | Timers = [15, 77, 135, 196, 271] | or | Avenging Wrath active | or | Daybreak cooldown >= 15
    Daybreak | Beacon of Virtue active
    Divine Toll | Beacon of Virtue active | and | previous ability = Word of Glory
    Word of Glory | Beacon of Virtue active | and | Divine Toll cooldown <= 0 | and | Unending Light stacks = 9
    Divine Toll | Beacon of Virtue active | or | previous ability = Daybreak
    Holy Shock | Beacon of Virtue active | and | Holy Shock charges = 2
    Divine Favor | Beacon of Virtue active
    Holy Light | Beacon of Virtue active | and | Infusion of Light active | and | Divine Favor active
    Word of Glory | Beacon of Virtue active | and | Unending Light stacks = 9
    Flash of Light | Beacon of Virtue active | and | Infusion of Light active
    Word of Glory | Beacon of Virtue active | and | Blessing of Dawn stacks = 2
    Holy Shock | Beacon of Virtue active
    Holy Shock | Holy Shock charges = 2
    Blessing of the Seasons
    Word of Glory | Unending Light stacks = 9 | and | Beacon of Virtue cooldown <= 13
    Light of Dawn | Blessing of Dawn stacks = 2
    Light of Dawn | Holy Power >= 5
    Flash of Light | Infusion of Light active
    Holy Shock
    Light of Dawn | Holy Power >= 3
    Judgment | Mana >= 60%
    Hammer of Wrath | Avenging Wrath active
    Crusader Strike
    Consecration`,
    convertPasteToPriorityList(priorityListPastedCode);
    document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    document.querySelectorAll(".priority-list-item-condition-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    updatePriorityList();
});

const clearPreset = document.getElementById("clear-preset");
clearPreset.addEventListener("click", () => {
    priorityListPastedCode = ` `,
    convertPasteToPriorityList(priorityListPastedCode);
    document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    document.querySelectorAll(".priority-list-item-condition-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    updatePriorityList();
});

const priorityListPasteModal = document.getElementById("priority-list-paste-modal");
const priorityListPasteModalTextarea = document.getElementById("priority-list-paste-modal-textarea");
priorityListPasteModal.style.display = "none";
priorityListPasteButton.addEventListener("mousedown", () => {
    priorityListPasteModal.style.display = priorityListPasteModal.style.display === "none" ? "flex" : "none";
    priorityListPasteButton.classList.toggle("priority-list-icon-active");
    priorityListPresetsButton.classList.remove("priority-list-icon-active");
    priorityListInfoButton.classList.remove("priority-list-icon-active");

    const priorityListString = priorityList.join("\n"); 
    priorityListPasteModalTextarea.value = priorityListString;
    if (priorityListPresetsModal.style.display !== "none") {
        priorityListPresetsModal.style.display = "none";
    };
    if (priorityListInfoModal.style.display !== "none") {
        priorityListInfoModal.style.display = "none";
    };
});

priorityListPasteModalTextarea.addEventListener("input", (e) => {
    priorityListPastedCode = e.target.value;
});

document.addEventListener("mousedown", (e) => {
    if (!priorityListPasteModal.contains(e.target) && e.target !== priorityListPasteButton && priorityListPasteModal.style.display !== "none") {
        priorityListPasteModal.style.display = "none";
        priorityListPasteButton.classList.remove("priority-list-icon-active");
        
        convertPasteToPriorityList(priorityListPastedCode);
        document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
            adjustTextareaHeight(itemText, 40);
        });
        document.querySelectorAll(".priority-list-item-condition-text").forEach(itemText => {
            adjustTextareaHeight(itemText, 40);
        });
        updatePriorityList();
    };
});

document.getElementById("save-paste-modal-button").addEventListener("click", (e) => {
    priorityListPasteModal.style.display = "none";
    priorityListPasteButton.classList.remove("priority-list-icon-active");
    convertPasteToPriorityList(priorityListPastedCode);
    document.querySelectorAll(".priority-list-item-ability-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    document.querySelectorAll(".priority-list-item-condition-text").forEach(itemText => {
        adjustTextareaHeight(itemText, 40);
    });
    updatePriorityList();
});

const makeDraggable = (modal, header) => {
    let startX = 0, startY = 0;
    let initialX = 0, initialY = 0;
    let dragging = false;

    header.addEventListener("mousedown", (e) => {
        dragging = true;
        startX = e.clientX;
        startY = e.clientY; 
        
        const transform = window.getComputedStyle(modal).transform;
        if (transform !== 'none') {
            const translate = transform.match(/matrix.*\((.+)\)/)[1].split(', ');
            initialX = parseInt(translate[4], 10);
            initialY = parseInt(translate[5], 10);
        } else {
            initialX = 0;
            initialY = 0;
        };

        document.onmousemove = onMouseMove;
        document.onmouseup = onStopDrag;
    });

    const onMouseMove = (e) => {
        if (!dragging) return;
        const moveX = initialX + e.clientX - startX;
        const moveY = initialY + e.clientY - startY;
        modal.style.transform = `translate(${moveX}px, ${moveY}px)`;
    };

    const onStopDrag = () => {
        dragging = false;
        document.onmousemove = null;
        document.onmouseup = null;
    };
};

const priorityListPasteModalHeader = document.getElementById("priority-list-paste-modal-header");
makeDraggable(priorityListPasteModal, priorityListPasteModalHeader);
// const priorityListPresetsModalHeader = document.getElementById("priority-list-presets-modal-header");
// makeDraggable(priorityListPresetsModal, priorityListPresetsModalHeader);

const priorityListInfoModal = document.getElementById("priority-list-info-modal");
priorityListInfoModal.style.display = "none";
priorityListInfoButton.addEventListener("mousedown", () => {
    priorityListInfoModal.style.display = priorityListInfoModal.style.display === "none" ? "flex" : "none";
    priorityListInfoButton.classList.toggle("priority-list-icon-active");
    priorityListPresetsButton.classList.remove("priority-list-icon-active");
    priorityListPasteButton.classList.remove("priority-list-icon-active");
    if (priorityListPresetsModal.style.display !== "none") {
        priorityListPresetsModal.style.display = "none";
    };
    if (priorityListPasteModal.style.display !== "none") {
        priorityListPasteModal.style.display = "none";
    };
});

const priorityListInfoModalContainer = document.getElementById("priority-list-info-modal-container");
priorityListInfoModalContainer.innerHTML = `
    Conditions<div id="info-modal-divider"></div>
    Time<br>
    Timers<br>
    Fight length<br>
    Mana<br>
    Holy Power<br>
    Ability name cooldown<br>
    Ability name charges<br>
    Buff name active/not active<br>
    Buff name duration<br>
    Buff name stacks<br>
    Talent name talented/not talented<br>
    Previous Ability<br>
    Overhealing<br>
    <br>
    Operations<div id="info-modal-divider"></div>
    Condition = or <span class="aligned">!=</span> Value<br>
    Condition &gt; or <span class="aligned">&gt;=</span> Value<br>
    Condition &lt; or <span class="aligned">&lt;=</span> Value<br>
    Value &lt; or <span class="aligned">&lt;=</span> Condition &lt; or <span class="aligned">&lt;=</span> Value<br>
    Timers = [Values]<br>
    Timers = [Values]+<br>
    <br>
    Examples<br>
    <div id="info-modal-divider"></div>
    Infusion of Light stacks = 2<br>
    Mana &lt;= 50%<br>
    30 < Time <= 40<br>
    Beacon of Virtue cooldown <= 3 * GCD<br>
    Timers = [0, 150, 300]<br>
    Timers = [30]+<br>
    Previous Ability = Daybreak<br>
    Light of Dawn overhealing > 70%<br>
    Holy Infusion talented
`;

const addPotionToPriorityList = (potionName, potionTimers, repeat = false) => {
    const potionRegex = new RegExp(`${potionName} \\| Timers = \\[(\\d*(?:\\.\\d+)?(?:,\\s*\\d*(?:\\.\\d+)?)*)\\][+]?`, "g");
    
    let priorityListJoined = "";
    if (!priorityListPastedCode) {
        priorityListJoined = "";
    } else {
        priorityListJoined = priorityListPastedCode.join("\n");
    };

    if (!priorityListJoined.includes(potionName) && repeat) {
        priorityListPastedCode = `${potionName} | Timers = [${potionTimers.join(", ")}]+\n` + priorityListJoined;
    } else if (!priorityListJoined.includes(potionName)) {
        priorityListPastedCode = `${potionName} | Timers = [${potionTimers.join(", ")}]\n` + priorityListJoined;
    } else if (repeat) {
        priorityListPastedCode = priorityListJoined.replace(potionRegex, `${potionName} | Timers = [${potionTimers.join(", ")}]+`)
    } else {
        priorityListPastedCode = priorityListJoined.replace(potionRegex, `${potionName} | Timers = [${potionTimers.join(", ")}]`)
    };
    
    convertPasteToPriorityList(priorityListPastedCode);
    updatePriorityList();
};

const removePotionFromPriorityList = (potionName) => {
    const potionRegex = new RegExp(`^.*${potionName} \\| Timers = \\[(\\d+(?:\\.\\d+)?(?:,\\s*\\d+(?:\\.\\d+)?)*)\\].*(\r?\n|\r)?`, "gm");
    const priorityListJoined = priorityListPastedCode.join("\n");
    const updatedPriorityList = priorityListJoined.replace(potionRegex, "");

    convertPasteToPriorityList(updatedPriorityList);
    updatePriorityList();
};

export { createPriorityListItem, updateIndices, adjustTextareaHeight, setDraggedItem, handleDragStart, handleDragEnd, handleDragOver, handleDrop, createPriorityListDisplay, convertPasteToPriorityList, priorityList, addPotionToPriorityList, removePotionFromPriorityList, updatePriorityList };