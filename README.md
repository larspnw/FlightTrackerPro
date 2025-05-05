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

### Local Development
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Set up environment variables:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `AVIATION_API_KEY`: Your Aviation Stack API key
4. Run the application: `gunicorn --bind 0.0.0.0:5000 main:app`

### Deployment on Replit
1. Fork this repository to your Replit account
2. Add the required secrets in the Replit Secrets tab:
   - `DATABASE_URL`: Automatically provided by Replit if you create a PostgreSQL database
   - `AVIATION_API_KEY`: Your Aviation Stack API key (get one at [aviationstack.com](https://aviationstack.com/))
3. Click the "Run" button to start the application
4. To make your app public with a permanent URL, use the "Deployment" tab to deploy your application

## Usage Guide

1. Enter a flight number in the format "Airline Code + Flight Number" (e.g., BA123, DL1234, AS517)
2. Click the "+" button to add the flight to your tracking list
3. Up to 3 flights can be tracked simultaneously
4. Click on a flight in the list to see its detailed information
5. Toggle the map display using the "Show Map" switch
6. Click the FlightAware link to see more detailed tracking on FlightAware
7. Remove flights by clicking the "X" button next to each flight
8. The application automatically refreshes flight data

## Limitations

- Maximum of 3 flights can be tracked at once
- The free tier of Aviation Stack API has limitations on request volume
- Historical data may be limited depending on the API tier
- Some flight information may not be available for all carriers

## API Reference

This application uses the Aviation Stack API to fetch real-time flight data. You need to register for an API key at [aviationstack.com](https://aviationstack.com/).

## License

MIT