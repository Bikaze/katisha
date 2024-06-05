// Define the API URL
const apiUrl = 'http://127.0.0.1:8000/api/tickets/';

// Function to build query parameters
function buildQueryParams() {
    const searchValue = $('#search-input').val();
    const originValue = $('#origin').val();
    const dateValue = $('#date').val();
    const departTimeStartValue = $('#depart-time-start').val();
    const departTimeEndValue = $('#depart-time-end').val();

    let queryParams = `search=${searchValue}`;

    if (originValue) queryParams += `&route__origin=${originValue}`;
    if (dateValue) queryParams += `&departure_date=${dateValue}`;
    if (departTimeStartValue) queryParams += `&departure_time__gt=${departTimeStartValue}`;
    if (departTimeEndValue) queryParams += `&departure_time__lt=${departTimeEndValue}`;

    return queryParams;
}

// Debounce function to delay the execution
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Define the function to fetch data
function fetchData(page = 1) {
    const queryParams = buildQueryParams();
    const searchUrl = `${apiUrl}?${queryParams}&page=${page}`;

    // Hide the results count initially
    $('#results-count').hide();

    // Use jQuery to make a GET request to the API
    $.get(searchUrl, function(data) {
        // Clear the results container
        $('#results-container').empty();
        $('#pagination').empty();

        // Show filters only if there are results
        if (data.count > 0) {
            $('#filter-box').show();
            $('#no-results').hide();
        } else {
            $('#filter-box').hide();
            $('#no-results').show();
        }

        // Show the results count and update its text
        $('#results-count').show().text(`Results: ${data.count}`);

        // Append each ticket to the results container
        data.results.forEach(ticket => {
            const resultItem = `
                <div class="result-item">
                    <h3><a href="#" class="route-link" data-id="${ticket.id}">${ticket.route}</a></h3>
                    <div>
                        <p><strong>Date:</strong> ${ticket.departure_date}</p>
                        <p><strong>Depart. time:</strong> ${ticket.departure_time}</p>
                    </div>
                    <div><strong>${ticket.vehicle.company}</strong></div>
                </div>
            `;
            $('#results-container').append(resultItem);
        });

        // Add click event listener to each route link
        $('.route-link').on('click', function(e) {
            e.preventDefault();
            const ticketId = $(this).data('id');
            fetchTicketDetails(ticketId);
        });

        // Create pagination buttons
        const totalPages = Math.ceil(data.count / 10); // Assuming 10 items per page
        let currentPage = page;

        // Determine the range of pages to display
        let startPage = Math.max(1, currentPage - 1);
        let endPage = Math.min(totalPages, currentPage + 1);

        // Add previous button if applicable
        if (currentPage > 1) {
            const previousButton = $('<button>Previous</button>');
            previousButton.on('click', function() {
                fetchData(currentPage - 1);
            });
            $('#pagination').append(previousButton);
        }

        // Add page buttons
        for (let i = startPage; i <= endPage; i++) {
            const pageButton = $(`<button>${i}</button>`);
            if (i === currentPage) {
                pageButton.addClass('active');
            }
            pageButton.on('click', function() {
                fetchData(i);
            });
            $('#pagination').append(pageButton);
        }

        // Add next button if applicable
        if (currentPage < totalPages) {
            const nextButton = $('<button>Next</button>');
            nextButton.on('click', function() {
                fetchData(currentPage + 1);
            });
            $('#pagination').append(nextButton);
        }
    });
}

// Function to fetch and display ticket details
function fetchTicketDetails(ticketId) {
    const detailUrl = `${apiUrl}${ticketId}/`;

    $.get(detailUrl, function(ticket) {
        // Clear the results container
        $('#results-container').empty();
        $('#pagination').empty();
        $('#results-count').hide();

        const detailItem = `
            <div class="detail-item">
                <h3>${ticket.route}</h3>
                <div>
                    <p><strong>Date:</strong> ${ticket.departure_date}</p>
                    <p><strong>Depart. time:</strong> ${ticket.departure_time}</p>
                    <p><strong>Vehicle Company:</strong> ${ticket.vehicle.company}</p>
                    <p><strong>Price:</strong> ${ticket.price}</p>
                    <p><strong>Available Seats:</strong> ${ticket.inventory}</p>
                </div>
                <button class="btn btn-primary" id="buy-ticket">Buy Ticket</button>
            </div>
        `;

        $('#results-container').append(detailItem);

        // Add event listener to the "Buy Ticket" button
        $('#buy-ticket').on('click', function() {
            alert('Ticket purchase functionality is not implemented yet.');
        });
    });
}

// Add an event listener to the button
$('#search-button').on('click', function() {
    fetchData();
});

// Add event listeners for filter inputs with debounce
$('#origin, #date, #depart-time-start, #depart-time-end').on('input', debounce(function() {
    fetchData();
}, 1500));
