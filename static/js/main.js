const token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*=\s*([^;]*).*$)|^.*$/, "$1");


function displayMessage(message) {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        messageContainer.textContent = message;
        messageContainer.style.display = 'block'; // Make the container visible if hidden
    } else {
        console.error('Message container not found');
    }
}


// Function to handle the "Apply Filters" button click
document.getElementById('apply-filters-button').addEventListener('click', () => {
    const city = document.getElementById('city-choices').value.trim();
    const type = document.getElementById('event-type').value.trim();

    // Get selected genres from checkboxes
    const selectedGenres = Array.from(document.querySelectorAll('#genres-options input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.id.split('-')[1]);
    const selectedCategories = Array.from(document.querySelectorAll('#categories-options input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.id.split('-')[1]);

    const filters = {};

    if (city && city !== " ") filters.city = city;
    if (type && type !== " ") filters.event_type = type; 

    // Add genres to filters
    if (selectedGenres.length > 0) {
        filters.genres = selectedGenres;
    }
    if (selectedCategories.length > 0) {
        filters.categories = selectedCategories;
    }

    // Build query string
    const filterParams = new URLSearchParams();

    Object.keys(filters).forEach(key => {
        if (Array.isArray(filters[key])) {
            // Add multiple values for the same key
            filters[key].forEach(value => filterParams.append(key, value));
        } else {
            filterParams.append(key, filters[key]);
        }
    });

    const filteredUrl = `/api/event/?${filterParams.toString()}`;
    console.log(filteredUrl)
    fetchEvents(filteredUrl); // Call your existing fetchEvents function with the filtered URL
});


function onRemoved(cookie) {
  console.log(`Removed: ${cookie}`);
}

function onError(error) {
  console.log(`Error removing cookie: ${error}`);
}


function logout(){
    event.preventDefault(); // Prevent default link behavior

    const access_token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*=\s*([^;]*).*$)|^.*$/, "$1");

    const refresh_token = document.cookie.replace(/(?:(?:^|.*;\s*)refresh_token\s*=\s*([^;]*).*$)|^.*$/, "$1");

    fetch('/user/token/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
        body: JSON.stringify({refresh: refresh_token})
    }).then(response => {
        if(response.ok) {
            // Remove tokens from localStorage and sessionStorage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('refresh_token');
         
            document.cookie = "access_token=; expires=Thy, 01 Jan 1970 00:00:00 UTC;";
            document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";

            window.location.href = '/';
        }
    });

};


document.addEventListener('DOMContentLoaded', () => {
    const link = document.querySelector("#logout-link")
    if (link) {
        link.addEventListener('click', logout)
    }
});
