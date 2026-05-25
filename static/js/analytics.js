document.addEventListener("DOMContentLoaded", () => {
    if (!window.Chart) {
        return;
    }

    const configs = {
        focus: { type: "bar", label: "Hours", color: "#5de4c7" },
        distractions: { type: "line", label: "Distractions", color: "#ff6b7a" },
        productivity: { type: "line", label: "Score", color: "#6ea8fe" },
    };

    document.querySelectorAll(".chart-canvas").forEach((canvas) => {
        const mode = canvas.dataset.chart;
        const config = configs[mode];
        new Chart(canvas, {
            type: config.type,
            data: {
                labels: JSON.parse(canvas.dataset.labels),
                datasets: [{
                    label: config.label,
                    data: JSON.parse(canvas.dataset.values),
                    borderColor: config.color,
                    backgroundColor: `${config.color}66`,
                    fill: config.type === "line",
                    tension: 0.35,
                }],
            },
            options: {
                plugins: { legend: { labels: { color: "#9fb2c9" } } },
                scales: {
                    y: { beginAtZero: true, ticks: { color: "#9fb2c9" }, grid: { color: "rgba(255,255,255,0.08)" } },
                    x: { ticks: { color: "#9fb2c9" }, grid: { display: false } },
                },
            },
        });
    });
});
