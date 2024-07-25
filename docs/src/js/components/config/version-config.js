const initialiseVersion = () => {
    const versionInput = document.getElementById("version-input");
    const versionSuggestions = document.getElementById("version-suggestions");
    const selectedVersion = document.getElementById("version-selected-version");

    versionInput.addEventListener("click", () => {
        versionSuggestions.style.display = versionSuggestions.style.display === "block" ? "none" : "block";
    });

    versionSuggestions.addEventListener("click", (e) => {
        selectedVersion.textContent = e.target.textContent;
        versionSuggestions.style.display = "none";
        document.documentElement.setAttribute("data-version", e.target.textContent);
        localStorage.setItem("version", e.target.textContent);
        window.location.reload();
    });

    selectedVersion.textContent = document.documentElement.getAttribute("data-version");

    window.addEventListener("click", (e) => {
        if (!versionInput.contains(e.target) && !versionSuggestions.contains(e.target)) {
            if (versionSuggestions.style.display !== "none") {
                versionSuggestions.style.display = "none";
            };
        };
    });
};

const version = document.documentElement.getAttribute("data-version");
const futurePatchSelected = version === "The War Within";

const templateButton = document.getElementById("template-button");
templateButton.style.display = "flex";

export { initialiseVersion, futurePatchSelected };