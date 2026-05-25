document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const savedMode = localStorage.getItem("focussprint-visual-mode") || "dark";
    html.dataset.theme = savedMode;

    const toggle = document.querySelector("[data-theme-toggle]");
    if (toggle) {
        toggle.checked = savedMode === "midnight";
        toggle.addEventListener("change", () => {
            const nextMode = toggle.checked ? "midnight" : "dark";
            html.dataset.theme = nextMode;
            localStorage.setItem("focussprint-visual-mode", nextMode);
        });
    }
});
