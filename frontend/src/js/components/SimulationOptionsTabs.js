const handleTabs = (navbarId, contentClass, containerCount = null) => {
    const navbar = document.getElementById(navbarId);
    navbar.addEventListener("click", (e) => {
        if (e.target && e.target.classList.contains("options-tab")) {
            switchTab(e.target.id, contentClass, containerCount);
        };

        if (e.target && e.target.classList.contains(`results-tab-${containerCount}`)) {
            switchTab(e.target.id, contentClass, containerCount);
        };

        if (e.target && e.target.classList.contains(`buffs-line-graph-tab-${containerCount}`)) {
            switchTab(e.target.id, contentClass, containerCount);
        };
    });
};

const switchTab = (tabId, contentClass, containerCount = null) => {
    document.querySelectorAll(`.${contentClass}`).forEach(element => {
        element.style.display = "none";
    });
     
    if (contentClass.includes("options")) {
        document.querySelectorAll(".options-tab").forEach(element => {
            element.classList.remove("active");
            element.classList.add("inactive");
        });
    } else if (contentClass.includes("results")) {
        document.querySelectorAll(`.results-tab-${containerCount}`).forEach(element => {
            element.classList.remove("active");
            element.classList.add("inactive");
        });
    } else if (contentClass.includes(`buffs-line-graph`)) {
        document.querySelectorAll(`.buffs-line-graph-tab-${containerCount}`).forEach(element => {
            element.classList.remove("active");
            element.classList.add("inactive");
        });
    };
    
    const contentId = tabId.replace("tab", "content");
    document.getElementById(contentId).style.display = "block";
    const activeTab = document.getElementById(tabId);
    activeTab.classList.add("active");
    activeTab.classList.remove("inactive");
};

export { handleTabs };