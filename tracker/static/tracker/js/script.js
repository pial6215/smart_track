function startLiveTimer(checkInTimeStr) {
    const display = document.getElementById('live-timer');
    if (!display) return;

    const checkInTime = new Date(checkInTimeStr).getTime();

    function updateTimer() {
        const now = new Date().getTime();
        
        let diff = now - checkInTime;

        const activeDiff = diff < 0 ? 0 : diff;

        const hours = Math.floor(activeDiff / (1000 * 60 * 60));
        const minutes = Math.floor((activeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((activeDiff % (1000 * 60)) / 1000);

        display.innerText = 
            `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    updateTimer(); 
    setInterval(updateTimer, 1000);
}

function toggleManualForm() {
    const form = document.getElementById('m-form');
    if (form) {
        form.classList.toggle('show-form');
        if (form.classList.contains('show-form')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    }
}