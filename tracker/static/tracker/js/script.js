/**
 * Smart Tracker Live Timer Logic
 * With Server-Client Time Synchronization Fix
 */

function startLiveTimer(checkInTimeStr) {
    const display = document.getElementById('live-timer');
    if (!display) return;

    // ১. সার্ভারের পাঠানো চেক-ইন টাইমকে মিলিসেকেন্ডে রূপান্তর
    const checkInTime = new Date(checkInTimeStr).getTime();

    function updateTimer() {
        // ২. বর্তমান সময় (Browser Time)
        const now = new Date().getTime();
        
        // ৩. সময়ের পার্থক্য বের করা
        const diff = now - checkInTime;

        // ৪. যদি পার্থক্য নেগেটিভ হয় (সার্ভার টাইম ব্রাউজার থেকে এগিয়ে থাকলে)
        // তবে আমরা সেটাকে ০ ধরে নেব যাতে ১ মিনিট পর্যন্ত অপেক্ষা করতে না হয়
        const activeDiff = diff < 0 ? 0 : diff;

        const hours = Math.floor(activeDiff / (1000 * 60 * 60));
        const minutes = Math.floor((activeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((activeDiff % (1000 * 60)) / 1000);

        // ৫. ফরম্যাট করা (00:00:00)
        const hDisplay = String(hours).padStart(2, '0');
        const mDisplay = String(minutes).padStart(2, '0');
        const sDisplay = String(seconds).padStart(2, '0');

        display.innerText = `${hDisplay}:${mDisplay}:${sDisplay}`;
    }

    // সাথে সাথে একবার কল করা এবং প্রতি সেকেন্ডে চালানো
    updateTimer(); 
    setInterval(updateTimer, 1000);
}

/**
 * Manual form toggle function
 */
function toggleManualForm() {
    const form = document.getElementById('m-form');
    if (form) {
        form.classList.toggle('show-form');
        if (form.classList.contains('show-form')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    }
}