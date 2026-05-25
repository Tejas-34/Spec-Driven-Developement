document.addEventListener("DOMContentLoaded", () => {
    const durationSelect = document.getElementById("durationSelect");
    const customRow = document.getElementById("customDurationRow");

    if (durationSelect && customRow) {
        durationSelect.addEventListener("change", () => {
            customRow.classList.toggle("hidden", durationSelect.value !== "custom");
        });
    }

    document.addEventListener("keydown", (event) => {
        if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            const form = document.querySelector(".session-form");
            if (form) {
                form.submit();
            }
        }
    });
});
