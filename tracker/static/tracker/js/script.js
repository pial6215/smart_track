// ১. মেইন কাজের টাইমার (Check-in Timer) - আপডেট করা হয়েছে
function startLiveTimer(checkInTimeStr, savedBreaksSec = 0) {
    const display = document.getElementById('live-timer');
    if (!display) return;

    const checkInTime = new Date(checkInTimeStr).getTime();
    // savedBreaksSec কে মিলিসেকেন্ডে রূপান্তর করছি
    const totalBreakMs = savedBreaksSec * 1000;

    function updateTimer() {
        const now = new Date().getTime();
        // সূত্র: (বর্তমান সময় - চেকইন সময়) - মোট ব্রেক সময়
        let diff = (now - checkInTime) - totalBreakMs;
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

// ২. ব্রেক টাইমার (Break Countdown Timer) - আগের মতোই আছে
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

// ৩. ম্যানুয়াল ফরম টগল করার ফাংশন - অপরিবর্তিত
function toggleManualForm() {
    const form = document.getElementById('m-form');
    if (form) {
        form.classList.toggle('show-form');
        if (form.classList.contains('show-form')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    }
}