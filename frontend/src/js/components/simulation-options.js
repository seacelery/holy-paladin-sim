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

export { setSimulationOptionsFromImportedData };