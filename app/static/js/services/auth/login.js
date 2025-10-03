const loginForm = document.getElementById('loginForm');
const loginButton = document.getElementById('loginButton');

loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();


    loginButton.disabled = true;
    loginButton.textContent = 'Logging in...';

    const formData = new FormData(loginForm);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/auth/login/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status) {
            showNotification('Success!', result.message, 'success');

            // Redirect to home/dashboard
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showNotification('Login Failed', result.message || 'Invalid credentials.', 'error');
            loginButton.disabled = false;
            loginButton.textContent = 'Login';
        }
    } catch (error) {
        showNotification('Error', 'Unable to connect to the server. Try again later.', 'info');
        loginButton.disabled = false;
        loginButton.textContent = 'Login';
    }
});
