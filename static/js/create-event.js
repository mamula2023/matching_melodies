const form = document.querySelector("#event-create-form");

async function createEvent() {
        event.preventDefault(); // Prevent default form submission
        // Get token from cookies
        const token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*=\s*([^;]*).*$)|^.*$/, "$1");

        // Gather form data

        const formData = new FormData(form);

        fetch('/api/event/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        })
        .then(response => {
            if (response.status === 201) {
                return response.json(); // Successful creation, parse the response
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Failed to create event');
                });
            }
        })
        .then(data => {
            window.location.href = `/`;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while creating the event.');
        });
}

async function populateSelects() {
    try {
        // Fetch categories and genres from their respective APIs
        const [categoriesResponse, genresResponse] = await Promise.all([
            fetch('/api/event/category/'),
            fetch('/api/event/genre/')
        ]);

        if (!categoriesResponse.ok || !genresResponse.ok) {
            throw new Error('Failed to fetch data from one or more endpoints');
        }

        const categoriesData = await categoriesResponse.json();
        const genresData = await genresResponse.json();

        // Populate categories select element
        const categoriesSelect = document.getElementById('categories');
        categoriesData.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.title;
            categoriesSelect.appendChild(option);
        });

        // Populate genres select element
        const genresSelect = document.getElementById('genres');
        genresData.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre.id;
            option.textContent = genre.title;
            genresSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error populating selects:', error);
    }
}

// Call the function to populate the selects when the page loads
window.addEventListener('DOMContentLoaded', populateSelects);
form.addEventListener("submit", (event) => {
  event.preventDefault();
  createEvent();
});
