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
        
        # For debugging
        logger.debug(f"API response data: {data}")
        
        try:
            # Extract flight information from the first result
            flight_info = data["data"][0]
            
            # For debugging
            logger.debug(f"Flight info: {flight_info}")
            
            # Safely get nested values
            def safe_get(obj, *keys):
                try:
                    for key in keys:
                        if obj is None:
                            return None
                        obj = obj.get(key)
                    return obj
                except (AttributeError, KeyError, TypeError):
                    return None
            
            # Format the return data
            formatted_data = {
                "flight_number": safe_get(flight_info, "flight", "iata") or flight_number,
                "airline": safe_get(flight_info, "airline", "name"),
                "departure_airport": safe_get(flight_info, "departure", "iata"),
                "arrival_airport": safe_get(flight_info, "arrival", "iata"),
                "scheduled_departure": format_date(safe_get(flight_info, "departure", "scheduled")),
                "scheduled_arrival": format_date(safe_get(flight_info, "arrival", "scheduled")),
                "actual_departure": format_date(safe_get(flight_info, "departure", "actual")),
                "actual_arrival": format_date(safe_get(flight_info, "arrival", "actual")),
                "status": flight_info.get("flight_status"),
                "departure_lat": safe_get(flight_info, "departure", "latitude"),
                "departure_lon": safe_get(flight_info, "departure", "longitude"),
                "arrival_lat": safe_get(flight_info, "arrival", "latitude"),
                "arrival_lon": safe_get(flight_info, "arrival", "longitude"),
                "current_lat": safe_get(flight_info, "live", "latitude"),
                "current_lon": safe_get(flight_info, "live", "longitude"),
                "altitude": safe_get(flight_info, "live", "altitude"),
                "speed": safe_get(flight_info, "live", "speed_horizontal")
            }
            
            # Check if we got any meaningful data
            has_data = any([
                formatted_data["airline"],
                formatted_data["departure_airport"],
                formatted_data["arrival_airport"],
                formatted_data["scheduled_departure"],
                formatted_data["scheduled_arrival"],
                formatted_data["status"]
            ])
            
            if not has_data:
                return {"error": "No flight data available for this flight number"}
        except Exception as e:
            logger.error(f"Error processing flight data: {str(e)}")
            return {"error": f"Error processing flight data: {str(e)}"}
        
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
