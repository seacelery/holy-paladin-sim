const simulateText = document.getElementById("simulate-text")

// update the paladin class when talents are changed
const handleTalentChange = (event) => {
    const talentName = event.target.getAttribute("data-talent")
    const talentValue = event.target.checked ? 1 : 0

    const talentUpdate = {
        "talents": {
            [talentName]: talentValue
        }
    };

    fetch("http://127.0.0.1:5000/update_character", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(talentUpdate)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
};

document.querySelectorAll("input[data-talent]").forEach(element => {
    element.addEventListener("change", handleTalentChange);
});

// update the paladin class when the race is changed
const raceFilter = document.getElementById("race-filter")
raceFilter.addEventListener("change", () => {
    const raceValue = raceFilter.value

    fetch("http://127.0.0.1:5000/update_character", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
            race: raceValue 
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error("Error:", error));
})

// update displayed information based on imported character
const importButton = document.getElementById("import-button")
importButton.addEventListener("click", () => {
    fetch("http://127.0.0.1:5000/import_character?character_name=daisu&realm=aszune", {
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        raceFilter.value = data.race
        simulateText.textContent = JSON.stringify(data, null, 2);

        // create a checkbox for each talent that exists in html, and check it if the talent is active on the character
        Object.keys(data.talents).forEach(row => {
            Object.keys(data.talents[row]).forEach(talentName => {
                const talentCheckbox = document.querySelector(`input[data-talent="${talentName}"]`);
                if (talentCheckbox) {
                    talentCheckbox.checked = data.talents[row][talentName].ranks["current rank"] === 1;
                };
            });
        });
    })
    .catch(error => console.error("Error:", error));
});

const simulateButton = document.getElementById("simulate-button")
simulateButton.addEventListener("click", () => {
    fetch("http://127.0.0.1:5000/run_simulation", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {
            simulateText.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error("Error:", error));
});

