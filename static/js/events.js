const container =           document.getElementById('events-container');
const paginationContainer = document.getElementById('pagination-container');

let nextPage = null;
let prevPage = null;


function fetchEvents(pageUrl = '/api/event/') {
    var parser = document.createElement('a')
    parser.href = pageUrl
    
    var path = ''
    if (parser.pathname) {
        path = path + parser.pathname;
    }

    if (parser.search) {
        path = path + parser.search;
    }

    fetch(path, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.status == 401) {
            displayMessage("You have to be authorized to view this content");
            return
        }
        return response.json();
    })
    .then(data => {
        renderEvents(data.results);
        renderFilters(data.filters);
        nextPage = data.next;

        prevPage = data.previous;
        renderPagination();
    })
    .catch(error => console.error('error fetching events:', error));
}

function renderFilters(filters) {
    const cityFilters = document.getElementById('city-choices') 
    cities = filters.cities
    cityFilters.innerHTML = ''
    const cityOpt = document.createElement('option');
    cityOpt.textContent = 'All';
    cityOpt.setAttribute("value", ' ');
    cityFilters.appendChild(cityOpt);
    cities.forEach(city => {
        const cityOpt = document.createElement('option');
        cityOpt.setAttribute("value", city);
        cityOpt.textContent = city
        cityFilters.appendChild(cityOpt)
    })

    const genresFilters = document.getElementById('genres-options');
    genresFilters.innerHTML = ''
    genres = filters.genres
    genres.forEach(genre => {
        const input = document.createElement('input');
        input.setAttribute('type', 'checkbox');
        input.setAttribute('id', `genre-${genre.id}`);
        input.setAttribute('name', 'genres');
        input.setAttribute('value', genre.title); 

        const label = document.createElement('label');
        label.setAttribute('for', `genre-${genre.id}`)
        label.textContent = genre.title

        genresFilters.appendChild(input);
        genresFilters.appendChild(label);
    })

    const categoriesFilters = document.getElementById('categories-options');
    categoriesFilters.innerHTML = ''
    categories = filters.categories
    categories.forEach(category => {
        const input = document.createElement('input');
        input.setAttribute('type', 'checkbox');
        input.setAttribute('id', `category-${category.id}`);
        input.setAttribute('name', 'category');
        input.setAttribute('value', category.title); 

        const label = document.createElement('label');
        label.setAttribute('for', `category-${category.id}`)
        label.textContent = category.title

        categoriesFilters.appendChild(input);
        categoriesFilters.appendChild(label);
    })
}

function renderEvents(events) {
    container.innerHTML = '';
    events.forEach(event => {
        const eventDiv = renderEvent(event);
        container.appendChild(eventDiv);
    });
}

function renderEvent(event) {
    const eventDiv = document.createElement('div');
    eventDiv.classList.add('event')

    const eventImage = document.createElement('img');
    eventImage.src = event.img;
    eventImage.alt = event.title;
    eventImage.classList.add('event-image')

    const eventTitle = document.createElement('h3');
    eventTitle.textContent = event.title;

    // date
    const eventDate = document.createElement('p');
    const formattedDate = new Date(event.date).toLocaleDateString();
    eventDate.textContent = `${formattedDate}`;
    eventDate.setAttribute("style", "display: inline; float: right;");


    // location
    const icon = document.createElement('i');
    icon.classList.add('fa');
    icon.classList.add('fa-map-marker');
    const eventCity = document.createElement('p');
    eventCity.textContent = ` ${event.city}`;
    eventCity.setAttribute("style", "display: inline;");

    const locationInfo = document.createElement('div')
    locationInfo.appendChild(icon)
    locationInfo.appendChild(eventCity)
    
    // Event payment
    const eventPayment = document.createElement('p');
    eventPayment.textContent = `Payment: $${event.payment}`;
    eventPayment.setAttribute("style", "display: inline; float: left;");

    // type tag
    const eventType = document.createElement('div');
    eventType.classList.add('event-type')
    eventType.textContent = `${event.event_type}`
    if (event.event_type === 'gig') {
        eventType.setAttribute("style", "background-color: #871f29;");
    }else if(event.event_type === 'collaboration') {
        eventType.setAttribute("style", "background-color: #040075;");
    }


    // Append all elements to eventDiv
    const eventContent = document.createElement('div');
    eventContent.classList.add('event-content');
    
    eventContent.appendChild(eventTitle);
    eventContent.appendChild(locationInfo);
    if (event.date != null) {
        eventContent.appendChild(eventPayment);
        eventContent.appendChild(eventDate);
    }
  const wrapperLink = document.createElement('a');
    wrapperLink.href=`/event/${event.id}/`;


    wrapperLink.appendChild(eventType);
    wrapperLink.appendChild(eventImage);
    wrapperLink.appendChild(eventContent);

      eventDiv.appendChild(wrapperLink);
    

    return eventDiv
}

function renderPagination(){
    paginationContainer.innerHTML = '';
    if (prevPage) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.addEventListener('click', () => fetchEvents(prevPage));
        paginationContainer.appendChild(prevButton);
    }

    if (nextPage) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => fetchEvents(nextPage));
        paginationContainer.appendChild(nextButton);
    }
}

function displayMessage(message) {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        messageContainer.textContent = message;
        messageContainer.style.display = 'block'; // Make the container visible if hidden
    } else {
        console.error('Message container not found');
    }
}


window.onload = function(){
    fetchEvents('/api/event/');
}
