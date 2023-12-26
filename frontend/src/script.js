const simulateText = document.getElementById("simulate-text")
const simulateButton = document.getElementById("simulate-button")

simulateButton.addEventListener("click", () => {
    fetch('http://127.0.0.1:5000/simulate?character_name=daisu&realm=aszune')
        .then(response => response.json())
        .then(data => {
            simulateText.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error('Error:', error));
})

