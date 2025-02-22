document.addEventListener("DOMContentLoaded", function () {
    // Auto-close alerts after 5 seconds
    document.querySelectorAll(".alert").forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease-out";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500); 
        }, 5000);
    });

    // Task reminder for deadlines today
    let today = new Date().toISOString().split('T')[0]; 
    let taskRows = document.querySelectorAll("tbody tr");

    taskRows.forEach((row) => {
        let deadlineCell = row.querySelector(".task-deadline"); 
        if (deadlineCell && deadlineCell.innerText.trim() === today) {
            setTimeout(() => {
                alert("⏰ Reminder: You have tasks due today!");
            }, 2000);
        }
    });
});
