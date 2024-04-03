import { makeFieldEditable } from "../utils/misc-functions.js";

const roundIterations = (number) => {
    if (number < 100) {
        return number
    } else {
        return Math.round(number / 10) * 10;
    };
};

const createOptionsSliders = () => {
    window.lastSliderChange = "";

    const updateSliderStep = (value, slider, sliderText) => {
        if (value < 100) {
            slider.step = 1;
            sliderText.textContent = value;
        } else {
            slider.step = 50;
            sliderText.textContent = roundIterations(value);
        };
    };
    
    const updateSliderDisplay = (secondsValue, minutesElement, secondsElement) => {
        const minutes = Math.floor(secondsValue / 60);
        const seconds = secondsValue % 60;
        minutesElement.textContent = minutes;
        secondsElement.textContent = seconds.toString().padStart(2, "0");
    };
    
    // iterations slider
    const iterationsSlider = document.getElementById("iterations-option");
    const iterationsValue = document.getElementById("iterations-value");
    const baseMaxIterations = 1001;
    
    iterationsSlider.addEventListener("input", () => {
        iterationsSlider.max = baseMaxIterations;
    
        const value = iterationsSlider.value
        updateSliderStep(value, iterationsSlider, iterationsValue);
        window.lastSliderChange = "Slider";
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
        window.lastSliderChange = "Value";
    });
    
    // encounter length slider
    const encounterLengthSlider = document.getElementById("encounter-length-option");
    const encounterLengthMinutes = document.getElementById("encounter-length-minutes");
    const encounterLengthSeconds = document.getElementById("encounter-length-seconds");
    const baseMaxEncounterLength = 600;
    
    // initial encounter length display
    updateSliderDisplay(parseInt(encounterLengthSlider.value, 10), encounterLengthMinutes, encounterLengthSeconds);
    
    encounterLengthSlider.addEventListener("input", () => {
        encounterLengthSlider.max = baseMaxEncounterLength;
        updateSliderDisplay(parseInt(encounterLengthSlider.value, 10), encounterLengthMinutes, encounterLengthSeconds);
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
    
    // time warp timer slider
    const timeWarpSlider = document.getElementById("time-warp-option");
    const timeWarpMinutes = document.getElementById("time-warp-minutes");
    const timeWarpSeconds = document.getElementById("time-warp-seconds");
    const baseMaxTimeWarp = 600;
    
    // initial time warp display
    updateSliderDisplay(parseInt(timeWarpSlider.value, 10), timeWarpMinutes, timeWarpSeconds);
    
    timeWarpSlider.addEventListener("input", () => {
        timeWarpSlider.max = baseMaxTimeWarp;
        updateSliderDisplay(parseInt(timeWarpSlider.value, 10), timeWarpMinutes, timeWarpSeconds);
    });
    
    makeFieldEditable(timeWarpMinutes, { charLimit: 2 });
    makeFieldEditable(timeWarpSeconds, { charLimit: 2 });
    
    [timeWarpMinutes, timeWarpSeconds].forEach(field => {
        field.addEventListener("input", (e) => {
            const minutes = parseInt(timeWarpMinutes.textContent, 10) || 0;
            const seconds = parseInt(timeWarpSeconds.textContent, 10) || 0;
            let totalSeconds = (minutes * 60) + seconds;
    
            if (totalSeconds > baseMaxTimeWarp) {
                timeWarpSlider.max = totalSeconds;
            } else {
                timeWarpSlider.max = baseMaxTimeWarp;
            };
    
            timeWarpSlider.value = totalSeconds;
        });
    });
    
    // tick rate slider
    const tickRateSlider = document.getElementById("tick-rate-option");
    const tickRateValue = document.getElementById("tick-rate-value");
    
    tickRateSlider.addEventListener("input", () => {
        tickRateValue.textContent = tickRateSlider.value;
    });
    tickRateValue.textContent = tickRateSlider.value;
    makeFieldEditable(tickRateValue, 1, tickRateSlider);
    
    // raid health slider
    const raidHealthSlider = document.getElementById("raid-health-option");
    const raidHealthValue = document.getElementById("raid-health-value");
    
    raidHealthSlider.addEventListener("input", () => {
        raidHealthValue.textContent = raidHealthSlider.value + "%";
    });
    raidHealthValue.textContent = raidHealthSlider.value + "%";
    makeFieldEditable(raidHealthValue, 1, raidHealthSlider);
    
    // mastery effectiveness slider
    const masteryEffectivenessSlider = document.getElementById("mastery-effectiveness-option");
    const masteryEffectivenessValue = document.getElementById("mastery-effectiveness-value");
    
    masteryEffectivenessSlider.addEventListener("input", () => {
        masteryEffectivenessValue.textContent = masteryEffectivenessSlider.value + "%";
    });
    masteryEffectivenessValue.textContent = masteryEffectivenessSlider.value + "%";
    makeFieldEditable(masteryEffectivenessValue, 1, masteryEffectivenessSlider);
    
    // light of dawn targets slider
    const lightOfDawnSlider = document.getElementById("light-of-dawn-option");
    const lightOfDawnValue = document.getElementById("light-of-dawn-value");
    
    lightOfDawnSlider.addEventListener("input", () => {
        lightOfDawnValue.textContent = lightOfDawnSlider.value;
    });
    lightOfDawnValue.textContent = lightOfDawnSlider.value;
    makeFieldEditable(lightOfDawnValue, 1, lightOfDawnSlider);
    
    // light's hammer targets slider
    const lightsHammerSlider = document.getElementById("lights-hammer-option");
    const lightsHammerValue = document.getElementById("lights-hammer-value");
    
    lightsHammerSlider.addEventListener("input", () => {
        lightsHammerValue.textContent = lightsHammerSlider.value;
    });
    lightsHammerValue.textContent = lightsHammerSlider.value;
    makeFieldEditable(lightsHammerValue, 1, lightsHammerSlider);
    
    // resplendent light targets slider
    const resplendentLightSlider = document.getElementById("resplendent-light-option");
    const resplendentLightValue = document.getElementById("resplendent-light-value");
    
    resplendentLightSlider.addEventListener("input", () => {
        resplendentLightValue.textContent = resplendentLightSlider.value;
    });
    resplendentLightValue.textContent = resplendentLightSlider.value;
    makeFieldEditable(resplendentLightValue, 1, resplendentLightSlider);
};

export { createOptionsSliders, roundIterations };