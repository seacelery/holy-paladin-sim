const initialiseTheme = () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeToggleCircle = document.getElementById("theme-circle");
    const themePaladinIcon = document.getElementById("theme-paladin-icon");
    const themeMoonIcon = document.getElementById("theme-moon-icon");
    themeToggle.addEventListener("click", () => {
        themeToggleCircle.classList.toggle("theme-checked");
        themePaladinIcon.classList.toggle("theme-icon-hidden");
        themeMoonIcon.classList.toggle("theme-icon-hidden");

        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "plain" ? "paladin" : "plain";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    });

    const currentTheme = document.documentElement.getAttribute("data-theme");
    if (currentTheme === "plain") {
        themeToggleCircle.classList.toggle("theme-checked");
        themePaladinIcon.classList.toggle("theme-icon-hidden");
        themeMoonIcon.classList.toggle("theme-icon-hidden");
    };
};

export { initialiseTheme };