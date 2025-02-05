// Set the active state of the navbar
function setActiveNav() {
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '');

    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href').includes(currentPage)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Call the function to set the active state
setActiveNav();

// Task Form Submission Logic
document.getElementById('taskForm')?.addEventListener('submit', function (e) {
    e.preventDefault();

    const taskName = document.getElementById('taskName').value;
    const taskPriority = document.getElementById('taskPriority').value;
    const taskDeadline = document.getElementById('taskDeadline').value;

    // Create a new task card
    const taskCard = document.createElement('div');
    taskCard.className = 'task-card col-md-6';

    taskCard.innerHTML = `
        <div class="task-name">${taskName}</div>
        <div class="task-priority ${taskPriority}">${taskPriority}</div>
        <div class="task-deadline">Deadline: ${taskDeadline}</div>
        <div class="task-status">Status: <span class="status-text">Pending</span></div>
        <div class="task-actions">
            <button class="btn btn-success" onclick="markAsCompleted(this)">
                <i class="fas fa-check"></i>
            </button>
            <button class="btn btn-warning" onclick="editTask(this)">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-danger" onclick="deleteTask(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;

    // Add the task card to the task list
    document.getElementById('taskList').appendChild(taskCard);

    // Clear the form
    document.getElementById('taskForm').reset();
});

function deleteTask(button) {
    const taskCard = button.closest('.task-card');
    taskCard.remove();
}

function editTask(button) {
    const taskCard = button.closest('.task-card');
    const taskName = taskCard.querySelector('.task-name').textContent;
    const taskPriority = taskCard.querySelector('.task-priority').textContent.toLowerCase();
    const taskDeadline = taskCard.querySelector('.task-deadline').textContent.replace('Deadline: ', '');

    // Populate the form with the task details
    document.getElementById('taskName').value = taskName;
    document.getElementById('taskPriority').value = taskPriority;
    document.getElementById('taskDeadline').value = taskDeadline;

    // Remove the task card
    taskCard.remove();
}

function markAsCompleted(button) {
    const taskCard = button.closest('.task-card');
    const statusText = taskCard.querySelector('.status-text');
    statusText.textContent = 'Completed';
    statusText.style.color = 'green';

    const completedDate = new Date().toLocaleDateString();
    const completedDateElement = document.createElement('div');
    completedDateElement.className = 'task-completed-date';
    completedDateElement.textContent = `Completed on: ${completedDate}`;
    taskCard.appendChild(completedDateElement);

    // Disable the mark as completed button
    button.disabled = true;
}