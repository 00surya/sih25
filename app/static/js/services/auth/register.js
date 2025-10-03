const form = document.getElementById('registerForm');
const messageArea = document.getElementById('messageArea');
const submitButton = document.getElementById('submitButton');

console.log(messageArea)

// Add an event listener to the form for the 'submit' event
form.addEventListener('submit', async function (event) {
    // Prevent the default browser action of reloading the page on form submission
    event.preventDefault();

    // Clear any previous messages
    messageArea.textContent = '';
    messageArea.className = 'text-sm text-center';
    submitButton.disabled = true;
    submitButton.textContent = 'Creating account...';

    // Create a FormData object from the form to easily access its fields
    const formData = new FormData(form);
    // Convert the FormData into a simple JavaScript object
    const data = Object.fromEntries(formData.entries());

    try {
        // Use the fetch API to send the data to your backend
        const response = await fetch('/auth/register/api/register', {
            method: 'POST', // The HTTP method
            headers: {
                'Content-Type': 'application/json' // Tell the server we're sending JSON
            },
            body: JSON.stringify(data) // Convert the JS object to a JSON string
        });

        // Get the JSON response from the server
        const result = await response.json();

        console.log(result)

        // Check if the request was successful
        if (response.ok) { // Status codes 200-299
            // Display a success message
            if (result.status){
                showNotification('Success! Redirecting you to the dashboard...', result.message, 'success');
                
                // After a short delay, redirect the user to their dashboard or home page
                setTimeout(() => {
                    window.location.href = '/dashboard'; // Change '/dashboard' to your desired page
                }, 1500); // 1.5-second delay
            }
            else{
                showNotification(result.message, 'Your account has been created.', 'success');
            }

        } else {
            // If the server returned an error, display it
            showNotification('Error', result.message, 'error');
            submitButton.disabled = false;
            submitButton.textContent = 'Create Account';
        }

    } catch (error) {
        // This block catches network errors (e.g., server is down)
        showNotification('Info', 'Could not connect to the server. Please try again later.', 'info');
        submitButton.disabled = false;
        submitButton.textContent = 'Create Account';
    }
});