document.querySelector('#login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Get the email and password input values
    const email = document.querySelector('.input[placeholder="Enter your Email"]').value.trim();
    const password = document.querySelector('.input[placeholder="Enter your Password"]').value.trim();

    // Ensure both fields are filled
    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    // Prepare the data to be sent to the server
    const data = {
        email: email,
        password: password
    };

    try {
        // Send a POST request to the token endpoint
        const response = await fetch('/user/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // Check if the response is successful
        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || 'Unable to log in.'}`);
            return;
        }

        // Parse the response JSON
        const tokens = await response.json();

        // Save the access and refresh tokens to localStorage or sessionStorage
        document.cookie = `access_token=${tokens.access}; path=/;`;
        document.cookie = `refresh_token=${tokens.refresh}; path=/;`;

        // Notify the user and redirect or update the UI as needed
        alert('Login successful!');
        window.location.href = '/'; // Redirect to a dashboard or another page

    } catch (error) {
        console.error('Error during login:', error);
        alert('An unexpected error occurred. Please try again.');
    }
});



