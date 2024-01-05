const setSimulationOptionsFromImportedData = (importedData) => {
    const raceOption = document.getElementById("race-filter");

    raceOption.value = importedData.race
};

export { setSimulationOptionsFromImportedData };