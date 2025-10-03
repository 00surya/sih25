/**
 * Displays a modern, auto-dismissing notification.
 *
 * @param {string} heading - The bolded title of the notification.
 * @param {string} content - The main message content.
 * @param {string} [type='info'] - The type ('success', 'error', 'info').
 * @param {number} [duration=4000] - Duration in ms before auto-dismissing.
 */
function showNotification(heading, content, type = 'info', duration = 4000) {
    const container = document.getElementById('notification-container');
    if (!container) {
        console.error('Notification container not found!');
        return;
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;

    // SVG Icons Map
    const icons = {
        success: `<svg class="notification-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`,
        error: `<svg class="notification-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`,
        info: `<svg class="notification-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
    };

    notification.innerHTML = `
        ${icons[type] || icons.info}
        <div class="notification-content">
            <p class="heading">${heading}</p>
            <p class="message">${content}</p>
        </div>
    `;

    container.appendChild(notification);

    // Animate in
    // We use a short timeout to allow the element to be added to the DOM
    // before the transition class is applied.
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Set timer to auto-dismiss
    setTimeout(() => {
        notification.classList.remove('show');
        // Remove the element from the DOM after the fade-out transition ends
        notification.addEventListener('transitionend', () => notification.remove(), { once: true });
    }, duration);
}


// --- HOW TO USE IT ---
// You can test it by calling these functions from your browser's console
// or by hooking them up to button clicks.

// showNotification('Success!', 'Your profile was updated successfully.', 'success');
// showNotification('Update Failed', 'The server could not be reached.', 'error');
// showNotification('Just a heads up', 'Your trial period expires in 3 days.', 'info');