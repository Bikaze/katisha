# Katisha Online

Katisha Online is a web application that allows users to search for tickets based on various filters such as origin, departure date, and departure time. The application fetches data from an API and displays the results in a user-friendly manner, allowing for easy navigation and detailed views of individual tickets.

## Features
- **Search Functionality**: Users can search for tickets using a search bar.
- **Filter Options**: Users can filter results by origin, departure date, and departure time.
- **Responsive Design**: The application is designed to be responsive and works well on various screen sizes.
- **Pagination**: Results are paginated, allowing users to navigate through multiple pages of results.
- **Detailed View**: Each ticket in the search results can be clicked to view more detailed information and purchase options.

## Technologies Used
- **HTML5**
- **CSS3**
- **JavaScript (jQuery)**
- **Bootstrap 4**
- **FontAwesome for icons**
- **Google Fonts for typography**
- **[API URL] for ticket data**

## Getting Started
### Prerequisites
To run this project locally, you need to have the following installed:
- A web browser (e.g., Chrome, Firefox)
- A text editor (e.g., VSCode, Sublime Text)
- A local server setup (optional for static files)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Bikaze/katisha.git
    ```

2. Navigate to the project directory:
    ```bash
    cd katisha
    ```

3. Open index.html in your web browser to view the application.

## Usage
### Search for Tickets
Enter your search query in the search bar and click the search button. The search results will be displayed along with filters.

### Apply Filters
Use the filters to narrow down your search results by origin, departure date, and departure time. The results will be updated automatically as you input filter values.

### View Detailed Information
Click on a ticket route in the search results to view detailed information about the ticket. The detailed view will include additional details and a button to purchase the ticket.

## Project Structure
```
katisha/
│
├── index.html           # Main HTML file
├── style.css            # CSS styles
└── script.js            # JavaScript for functionality
```

- `index.html`: Contains the structure of the web application, including the search bar, filters, and results container. Uses Bootstrap for responsive design and layout.
- `style.css`: Contains custom styles for the application. Ensures that the application is visually appealing and user-friendly.
- `script.js`: Contains the logic for fetching data from the API, displaying search results, and handling filter inputs. Uses jQuery for AJAX requests and DOM manipulation.

## API Integration
The application integrates with an API to fetch ticket data. The base URL for the API is: `http://127.0.0.1:8000/api/tickets/`

### Example API Call
To fetch tickets based on search and filters:
```
http://127.0.0.1:8000/api/tickets/?search=skyndu&departure_date=&departure_time__gt=01%3A00%3A00&departure_time__lt=23%3A00%3A00&route__origin=
```

### API Parameters
- `search`: Search query for the tickets.
- `departure_date`: Filter by departure date.
- `departure_time__gt`: Filter by departure time (greater than).
- `departure_time__lt`: Filter by departure time (less than).
- `route__origin`: Filter by route origin.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Contact
For questions or feedback, please contact:
- Names:    Clement MUGISHA,            Poli NDIRAMIYE
- GitHub: https://github.com/Bikaze, https://github.com/Mr-ndi
