document.addEventListener("DOMContentLoaded", () => {
    const sessionLayout = document.querySelector(".session-layout");
    if (!sessionLayout) {
        return;
    }

    const sessionId = sessionLayout.dataset.sessionId;
    const durationMinutes = Number(sessionLayout.dataset.duration);
    const totalSeconds = durationMinutes * 60;
    let remainingSeconds = totalSeconds;
    let timer = null;

    const timerDisplay = document.getElementById("timerDisplay");
    const progressRing = document.querySelector(".ring-progress");
    const distractionCount = document.getElementById("distractionCount");
    const productivityScore = document.getElementById("productivityScore");
    const completionForm = document.getElementById("completionForm");

    const radius = 96;
    const circumference = 2 * Math.PI * radius;
    progressRing.style.strokeDasharray = `${circumference}`;

    const formatTime = (seconds) => {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    };

    const updateProgress = () => {
        timerDisplay.textContent = formatTime(remainingSeconds);
        const progress = 1 - remainingSeconds / totalSeconds;
        progressRing.style.strokeDashoffset = `${circumference * (1 - progress)}`;
    };

    const stopTimer = () => {
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
    };

    const beep = () => {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.type = "sine";
        oscillator.frequency.value = 880;
        gainNode.gain.value = 0.08;
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.35);
    };

    const startTimer = () => {
        if (timer) {
            return;
        }
        timer = setInterval(() => {
            if (remainingSeconds <= 0) {
                stopTimer();
                beep();
                return;
            }
            remainingSeconds -= 1;
            updateProgress();
        }, 1000);
    };

    document.getElementById("startTimer").addEventListener("click", startTimer);
    document.getElementById("pauseTimer").addEventListener("click", stopTimer);
    document.getElementById("resumeTimer").addEventListener("click", startTimer);
    document.getElementById("resetTimer").addEventListener("click", async () => {
        stopTimer();
        remainingSeconds = totalSeconds;
        updateProgress();
        await fetch(`/session/${sessionId}/reset`, { method: "POST" });
    });

    document.getElementById("distractButton").addEventListener("click", async () => {
        const response = await fetch(`/session/${sessionId}/distract`, { method: "POST" });
        const data = await response.json();
        distractionCount.textContent = data.distractions;
        productivityScore.textContent = data.productivity_score;
    });

    completionForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        stopTimer();
        const formData = new FormData(completionForm);
        const payload = Object.fromEntries(formData.entries());
        const response = await fetch(`/session/${sessionId}/complete`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        window.location.href = data.redirect_url;
    });

    document.addEventListener("keydown", (event) => {
        if (event.target.matches("textarea, input")) {
            return;
        }
        if (event.key.toLowerCase() === "s") startTimer();
        if (event.key.toLowerCase() === "p") stopTimer();
        if (event.key.toLowerCase() === "d") document.getElementById("distractButton").click();
    });

    updateProgress();
});
