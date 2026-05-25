document.addEventListener("DOMContentLoaded", () => {
    const greetingHeading = document.getElementById("greetingHeading");
    if (greetingHeading) {
        const hour = new Date().getHours();
        let greeting = "Good evening";
        if (hour < 12) greeting = "Good morning";
        else if (hour < 18) greeting = "Good afternoon";
        greetingHeading.textContent = greetingHeading.textContent.replace("Good evening", greeting);
    }

    const chartCanvas = document.getElementById("weeklyChart");
    let chartInstance = null;

    if (chartCanvas && window.Chart) {
        const labels = JSON.parse(chartCanvas.dataset.labels);
        const values = JSON.parse(chartCanvas.dataset.values);
        const buildDataset = (multiplier = 1) => values.map((value, index) => {
            if (multiplier === 1) return value;
            const scale = 1 + ((index % 3) * 0.08);
            return Number((value * scale * multiplier).toFixed(2));
        });

        const buildChart = (range) => {
            const ctx = chartCanvas.getContext("2d");
            const gradient = ctx.createLinearGradient(0, 0, 0, 320);
            gradient.addColorStop(0, "rgba(97, 243, 255, 0.95)");
            gradient.addColorStop(0.5, "rgba(142, 125, 255, 0.78)");
            gradient.addColorStop(1, "rgba(255, 120, 218, 0.18)");

            const borderGradient = ctx.createLinearGradient(0, 0, 500, 0);
            borderGradient.addColorStop(0, "#61f3ff");
            borderGradient.addColorStop(0.55, "#8e7dff");
            borderGradient.addColorStop(1, "#ff78da");

            const rangeMap = {
                "7": { labels, values: buildDataset(1) },
                "14": {
                    labels: [...labels, ...labels].map((label, index) => `${label}${index > 6 ? " +" : ""}`),
                    values: [...buildDataset(0.92), ...buildDataset(1.08)],
                },
                "30": {
                    labels: Array.from({ length: 10 }, (_, index) => `W${index + 1}`),
                    values: Array.from({ length: 10 }, (_, index) => Number((values[index % values.length] * (1 + index * 0.04)).toFixed(2))),
                },
            };

            const active = rangeMap[range] || rangeMap["7"];
            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(chartCanvas, {
                type: "line",
                data: {
                    labels: active.labels,
                    datasets: [{
                        label: "Focus hours",
                        data: active.values,
                        borderColor: borderGradient,
                        backgroundColor: gradient,
                        fill: true,
                        tension: 0.42,
                        pointRadius: 4,
                        pointBackgroundColor: "#040814",
                        pointBorderColor: "#61f3ff",
                        pointBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: "#61f3ff",
                        pointHoverBorderColor: "#8e7dff",
                        pointHoverBorderWidth: 2,
                        borderWidth: 3,
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: "rgba(8, 14, 28, 0.96)",
                            borderColor: "rgba(97, 243, 255, 0.18)",
                            borderWidth: 1,
                            titleColor: "#f7fbff",
                            bodyColor: "#c9d7f1",
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: "#90a1c0",
                                stepSize: 1.0,
                                callback: function(value) {
                                    return value + "h";
                                }
                            },
                            grid: { color: "rgba(255,255,255,0.06)" },
                        },
                        x: {
                            ticks: { color: "#90a1c0" },
                            grid: { display: false },
                        },
                    },
                },
            });
        };

        buildChart("7");
        const chartRange = document.getElementById("chartRange");
        if (chartRange) {
            chartRange.addEventListener("change", () => buildChart(chartRange.value));
        }
    }

    const quoteButton = document.getElementById("quoteButton");
    const quoteCard = document.getElementById("quoteCard");
    const loadQuote = async () => {
        if (!quoteButton || !quoteCard) {
            return;
        }
        quoteButton.disabled = true;
        quoteButton.textContent = "Loading...";
        try {
            const response = await fetch("/api/quote");
            const data = await response.json();
            quoteCard.textContent = `"${data.text}" — ${data.author}`;
        } catch (error) {
            quoteCard.textContent = "Unable to load a quote right now.";
        } finally {
            quoteButton.disabled = false;
            quoteButton.textContent = "Refresh quote";
        }
    };

    if (quoteButton && quoteCard) {
        quoteButton.addEventListener("click", loadQuote);
        loadQuote();
    }
});
