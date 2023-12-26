const simulateText = document.getElementById("simulate-text")
const simulateButton = document.getElementById("simulate-button")
const importButton = document.getElementById("import-button")

const raceFilter = document.getElementById("race-filter")

const lightsConvictionTalent = document.getElementById("talent1")
const reclamationTalent = document.getElementById("talent2")
const lightOfDawnTalent = document.getElementById("talent3")

raceFilter.addEventListener("change", () => {
    const raceValue = raceFilter.value

    fetch('http://127.0.0.1:5000/update_character', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            race: raceValue 
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
})

importButton.addEventListener("click", () => {
    fetch('http://127.0.0.1:5000/import_character?character_name=daisu&realm=aszune', {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        raceFilter.value = data[1]
        simulateText.textContent = JSON.stringify(data, null, 2);

        if (data[2].row3["Light's Conviction"].ranks["current rank"] === 1) {
            lightsConvictionTalent.checked = true
        }
        if (data[2].row2["Light of Dawn"].ranks["current rank"] === 1) {
            lightOfDawnTalent.checked = true
        }
        if (data[2].row8["Reclamation"].ranks["current rank"] === 1) {
            reclamationTalent.checked = true
        }
    })
    .catch(error => console.error('Error:', error));
})

reclamationTalent.addEventListener("change", () => {
    const talentUpdate = {
        "talents": {
            "Reclamation": reclamationTalent.checked ? 1 : 0 // Assuming checked means talent is active (1), and unchecked means inactive (0)
        }
    };

    fetch('http://127.0.0.1:5000/update_character', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            talentUpdate
        )
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
})

lightOfDawnTalent.addEventListener("change", () => {
    const talentUpdate = {
        "talents": {
            "Light of Dawn": lightOfDawnTalent.checked ? 1 : 0 // Assuming checked means talent is active (1), and unchecked means inactive (0)
        }
    };

    fetch('http://127.0.0.1:5000/update_character', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            talentUpdate
        )
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
})

lightsConvictionTalent.addEventListener("change", () => {
    const talentUpdate = {
        "talents": {
            "Light's Conviction": lightsConvictionTalent.checked ? 1 : 0 // Assuming checked means talent is active (1), and unchecked means inactive (0)
        }
    };

    fetch('http://127.0.0.1:5000/update_character', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            talentUpdate
        )
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
})

simulateButton.addEventListener("click", () => {
    fetch('http://127.0.0.1:5000/run_simulation', {
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            simulateText.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error('Error:', error));
})

