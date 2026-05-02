/**
 * Smart Tracker Live Timer Logic
 */

function startLiveTimer(checkInTimeStr) {
    const display = document.getElementById('live-timer');
    if (!display) return;

    // CheckIn time ke Date object e convert kora
    const checkInTime = new Date(checkInTimeStr).getTime();

    function updateTimer() {
        const now = new Date().getTime();
        const diff = now - checkInTime;

        if (diff < 0) {
            display.innerText = "00:00:00";
            return;
        }

        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Format: 00:00:00
        const hDisplay = hours < 10 ? "0" + hours : hours;
        const mDisplay = minutes < 10 ? "0" + minutes : minutes;
        const sDisplay = seconds < 10 ? "0" + seconds : seconds;

        display.innerText = `${hDisplay}:${mDisplay}:${sDisplay}`;
    }

    // Protite second e update hobe
    updateTimer(); 
    setInterval(updateTimer, 1000);
}

// Manual form toggle function
function toggleManualForm() {
    const form = document.getElementById('m-form');
    if (form) {
        form.classList.toggle('show-form');
        if (form.classList.contains('show-form')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    }
}