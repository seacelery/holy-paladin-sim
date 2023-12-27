const handleTabs = (navbarId, contentClass) => {
    const navbar = document.getElementById(navbarId);
    navbar.addEventListener("click", (e) => {
        if (e.target && e.target.classList.contains("options-tab")) {
            switchTab(e.target.id, contentClass);
        };
    });
};

const switchTab = (tabId, contentClass) => {
    document.querySelectorAll(`.${contentClass}`).forEach(element => {
        element.style.display = "none";
    });

    document.querySelectorAll(".options-tab").forEach(element => {
        element.style.backgroundColor = "var(--panel-colour-2)"
        element.style.textShadow = "none";
    });

    const contentId = tabId.replace("tab", "content");
    document.getElementById(contentId).style.display = "block";
    document.getElementById(tabId).style.backgroundColor = "var(--panel-colour-4)";
    document.getElementById(tabId).style.textShadow = "0.5px 0 0 var(--light-font-colour)";
};

export { handleTabs };