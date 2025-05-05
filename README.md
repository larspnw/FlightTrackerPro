# Flight Tracker

A real-time flight tracking web application that allows users to monitor multiple flights with real-time status updates and enhanced tracking features.

## Features

- Track up to 3 flights simultaneously
- Real-time flight status information
- Interactive map visualization of flight routes
- Flight history with departure and arrival details
- Toggle between map and list views
- Links to FlightAware for detailed flight tracking
- Mobile-friendly responsive design

## Technologies Used

- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL
- Mapping: Leaflet.js
- Styling: Bootstrap CSS
- Flight Data: Aviation Stack API

## Setup Instructions

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Set up environment variables:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `AVIATION_API_KEY`: Your Aviation Stack API key
4. Run the application: `gunicorn --bind 0.0.0.0:5000 main:app`

## API Reference

This application uses the Aviation Stack API to fetch real-time flight data. You need to register for an API key at [aviationstack.com](https://aviationstack.com/).

## License

MIT