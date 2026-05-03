// ১. মেইন কাজের টাইমার (Check-in Timer)
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

// ২. ব্রেক টাইমার (Break Countdown Timer)
function startBreakTimer(breakStartTimeStr) {
    const display = document.getElementById('break-live-timer');
    if (!display) return;

    function updateBreak() {
        const breakStart = new Date(breakStartTimeStr).getTime();
        const now = new Date().getTime();
        let diff = now - breakStart;

        if (isNaN(diff) || diff < 0) diff = 0;

        const h = Math.floor(diff / 3600000);
        const m = Math.floor((diff % 3600000) / 60000);
        const s = Math.floor((diff % 60000) / 1000);

        display.innerText = 
            `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }
    
    updateBreak(); 
    setInterval(updateBreak, 1000);
}

// ৩. ম্যানুয়াল ফরম টগল করার ফাংশন
function toggleManualForm() {
    const form = document.getElementById('m-form');
    if (form) {
        form.classList.toggle('show-form');
        if (form.classList.contains('show-form')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    }
}