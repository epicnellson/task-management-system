// Task Status Update
function updateTaskStatus(taskId, newStatus) {
    const taskElement = document.querySelector(`#task-${taskId}`);
    const statusBadge = taskElement.querySelector('.status-badge');
    
    // Show loading state
    statusBadge.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    
    fetch(`/tasks/${taskId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Update the status badge
        statusBadge.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
        statusBadge.className = `status-badge badge bg-${getStatusColor(newStatus)}`;
        
        // Add animation class
        taskElement.classList.add('task-status-change');
        setTimeout(() => {
            taskElement.classList.remove('task-status-change');
        }, 300);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update task status. Please try again.');
        // Revert to original status
        statusBadge.textContent = statusBadge.dataset.originalStatus;
    });
}

// Get status color
function getStatusColor(status) {
    switch(status) {
        case 'completed':
            return 'success';
        case 'in_progress':
            return 'warning';
        case 'pending':
            return 'secondary';
        default:
            return 'primary';
    }
}

// Delete Task Confirmation
function confirmDelete(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/tasks/${taskId}/delete`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Due Date Warning
function checkDueDates() {
    const tasks = document.querySelectorAll('.task-card');
    const now = new Date();
    
    tasks.forEach(task => {
        const dueDateElement = task.querySelector('.due-date');
        if (dueDateElement) {
            const dueDate = new Date(dueDateElement.dataset.dueDate);
            const daysUntilDue = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24));
            
            if (daysUntilDue < 0) {
                dueDateElement.classList.add('due-date-warning');
                dueDateElement.textContent = 'Overdue!';
            } else if (daysUntilDue <= 2) {
                dueDateElement.classList.add('due-date-warning');
            }
        }
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Check due dates
    checkDueDates();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.classList.remove('show');
            setTimeout(() => message.remove(), 150);
        }, 5000);
    });
}); 