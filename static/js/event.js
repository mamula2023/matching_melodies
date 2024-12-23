async function fetchEventDetails(eventId) {
    const token = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*=\s*([^;]*).*$)|^.*$/, "$1");

    var parser = document.createElement('a')
    parser.href = window.location.href 
    
    eventId = parser.pathname.split('/')[2]

    const event_fetch = await fetch(`/api/event/${eventId}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })

    const data = await event_fetch.json()

    // Populate the event details dynamically
    document.getElementById('event-title').textContent = data.title;
    document.getElementById('event-date').textContent = (new Date(data.date).toLocaleDateString()) || '';
    document.getElementById('event-city').textContent = `City: ${data.city}`;
    document.getElementById('event-location').textContent = `Location: ${data.location}`;
    document.getElementById('event-description').textContent = data.description

    // Set the event image
    const eventImage = document.getElementById('event-image');
    eventImage.src = data.img || '/static/event_images/default-image.png';
    eventImage.alt = data.title

    // Show payment info if event type is "gig"
    const paymentSection = document.getElementById('event-payment');
    if (data.event_type === 'gig' && data.payment) {
        paymentSection.style.display = 'block';
        document.getElementById('payment-amount').textContent = `$${data.payment}`;
    } else {
        paymentSection.style.display = 'none';
    }
    
    // Set additional info
    document.getElementById('event-additional-info').textContent = data.additional_info || 'No additional information provided'

    // Populate categories
    const categoriesList = document.getElementById('event-categories');
    categoriesList.innerHTML = '';
    data.categories.forEach(category => {
        const li = document.createElement('li');
        li.textContent = category.title; // Adjust according to your API response
        categoriesList.appendChild(li);
    })

    // Populate genres
    const genresList = document.getElementById('event-genres');
    genresList.innerHTML = '';
    data.genres.forEach(genre => {
        const li = document.createElement('li');
        li.textContent = genre.title; // Adjust according to your API response
        genresList.appendChild(li);
    })

    // Set organizer (author)
    author_id = data.author

    const author_fetch = await fetch(`/api/user/${author_id}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })

    const author_data = await author_fetch.json()


    document.getElementById('event-author').textContent = author_data.username
}

// Call the function with the event ID
fetchEventDetails(1); // Replace with the actual event ID

window.onload = function (){
    fetchEventDetails();    
}
