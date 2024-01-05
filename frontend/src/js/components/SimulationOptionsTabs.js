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
        element.classList.remove("active");
        element.classList.add("inactive");
    });

    const contentId = tabId.replace("tab", "content");
    document.getElementById(contentId).style.display = "block";
    const activeTab = document.getElementById(tabId);
    activeTab.classList.add("active");
    activeTab.classList.remove("inactive");
};

export { handleTabs };