document.querySelector('#login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const email = document.querySelector('.input[placeholder="Enter your Email"]').value.trim();
    const password = document.querySelector('.input[placeholder="Enter your Password"]').value.trim();

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    const data = {
        email: email,
        password: password
    };

    try {
        const response = await fetch('/user/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || 'Unable to log in.'}`);
            return;
        }

        const tokens = await response.json();

        document.cookie = `access_token=${tokens.access}; path=/;`;
        document.cookie = `refresh_token=${tokens.refresh}; path=/;`;

        alert('Login successful!');
        window.location.href = '/'; // Redirect to a dashboard or another page

    } catch (error) {
        console.error('Error during login:', error);
        alert('An unexpected error occurred. Please try again.');
    }
});



