import os
import logging
import requests
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# AviationStack API base URL and API key
BASE_URL = "http://api.aviationstack.com/v1"
API_KEY = os.environ.get("AVIATION_API_KEY", "default_api_key")

def get_flight_data(flight_number):
    """
    Fetch flight data from AviationStack API
    
    Args:
        flight_number (str): The flight number to look up
        
    Returns:
        dict: Flight information or error message
    """
    try:
        # Make API request
        response = requests.get(
            f"{BASE_URL}/flights",
            params={
                "access_key": API_KEY,
                "flight_iata": flight_number
            }
        )
        
        # Check if request was successful
        if response.status_code != 200:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            return {"error": f"API request failed with status code {response.status_code}"}
        
        # Parse response
        data = response.json()
        
        # Check for API errors
        if "error" in data:
            error_info = data["error"]
            logger.error(f"API returned an error: {error_info}")
            return {"error": f"API error: {error_info.get('message', 'Unknown error')}"}
        
        # Check if data was returned
        if not data.get("data") or len(data["data"]) == 0:
            return {"error": "Flight not found"}
        
        # Extract flight information from the first result
        flight_info = data["data"][0]
        
        # Format the return data
        formatted_data = {
            "flight_number": flight_info.get("flight", {}).get("iata"),
            "airline": flight_info.get("airline", {}).get("name"),
            "departure_airport": flight_info.get("departure", {}).get("iata"),
            "arrival_airport": flight_info.get("arrival", {}).get("iata"),
            "scheduled_departure": format_date(flight_info.get("departure", {}).get("scheduled")),
            "scheduled_arrival": format_date(flight_info.get("arrival", {}).get("scheduled")),
            "actual_departure": format_date(flight_info.get("departure", {}).get("actual")),
            "actual_arrival": format_date(flight_info.get("arrival", {}).get("actual")),
            "status": flight_info.get("flight_status"),
            "departure_lat": flight_info.get("departure", {}).get("latitude"),
            "departure_lon": flight_info.get("departure", {}).get("longitude"),
            "arrival_lat": flight_info.get("arrival", {}).get("latitude"),
            "arrival_lon": flight_info.get("arrival", {}).get("longitude"),
            "current_lat": flight_info.get("live", {}).get("latitude"),
            "current_lon": flight_info.get("live", {}).get("longitude"),
            "altitude": flight_info.get("live", {}).get("altitude"),
            "speed": flight_info.get("live", {}).get("speed_horizontal")
        }
        
        return formatted_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}

def format_date(date_str):
    """Format date string to ISO format"""
    if not date_str:
        return None
    
    try:
        # Parse the date string
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        # Format as ISO 8601
        return dt.isoformat()
    except Exception as e:
        logger.error(f"Error formatting date {date_str}: {str(e)}")
        return None
