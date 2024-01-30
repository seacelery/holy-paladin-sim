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

const makeFieldEditable = (field, defaultValue = null, fieldSlider = null) => {
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
        e.target.removeAttribute("contenteditable");
    });

    field.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            if (!e.target.textContent.trim() && defaultValue !== null) {
                e.target.textContent = defaultValue;

                if (field.id === "iterations-value") {
                    fieldSlider.step = 1;
                    fieldSlider.value = defaultValue;
                }
            }
            e.target.removeAttribute("contenteditable");
            e.preventDefault();
        };
    });
};

export { formatNumbers, formatNumbersNoRounding, formatTime, formatThousands, makeFieldEditable };