import os
import logging
import requests
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# AviationStack API base URL and API key
BASE_URL = "http://api.aviationstack.com/v1"
API_KEY = os.environ.get("AVIATION_API_KEY", "default_api_key")

# Airport coordinates lookup table (IATA code -> [lat, lon])
AIRPORT_COORDINATES = {
    # Major US airports
    "ATL": [33.6407, -84.4277],   # Atlanta
    "LAX": [33.9416, -118.4085],  # Los Angeles
    "ORD": [41.9742, -87.9073],   # Chicago O'Hare
    "DFW": [32.8998, -97.0403],   # Dallas/Fort Worth
    "DEN": [39.8561, -104.6737],  # Denver
    "JFK": [40.6413, -73.7781],   # New York JFK
    "SFO": [37.7749, -122.4194],  # San Francisco
    "SEA": [47.4502, -122.3088],  # Seattle
    "LAS": [36.0840, -115.1537],  # Las Vegas
    "MCO": [28.4312, -81.3081],   # Orlando
    "EWR": [40.6895, -74.1745],   # Newark
    "CLT": [35.2144, -80.9473],   # Charlotte
    "PHX": [33.4352, -112.0101],  # Phoenix
    "IAH": [29.9844, -95.3414],   # Houston
    "MIA": [25.7932, -80.2906],   # Miami
    "BOS": [42.3656, -71.0096],   # Boston
    "MSP": [44.8848, -93.2223],   # Minneapolis
    "DTW": [42.2162, -83.3554],   # Detroit
    "FLL": [26.0742, -80.1506],   # Fort Lauderdale
    "PHL": [39.8729, -75.2437],   # Philadelphia
    "LGA": [40.7769, -73.8740],   # New York LaGuardia
    "BWI": [39.1774, -76.6694],   # Baltimore
    "SLC": [40.7899, -111.9791],  # Salt Lake City
    "DCA": [38.8512, -77.0402],   # Washington Reagan
    "IAD": [38.9531, -77.4565],   # Washington Dulles
    "SAN": [32.7338, -117.1933],  # San Diego
    "MDW": [41.7868, -87.7522],   # Chicago Midway
    "TPA": [27.9772, -82.5311],   # Tampa
    "PDX": [45.5898, -122.5951],  # Portland
    "HNL": [21.3245, -157.9251],  # Honolulu
    "CVG": [39.0489, -84.6678],   # Cincinnati
    
    # Major international airports
    "LHR": [51.4700, -0.4543],    # London Heathrow
    "CDG": [49.0097, 2.5479],     # Paris Charles de Gaulle
    "FRA": [50.0379, 8.5622],     # Frankfurt
    "AMS": [52.3105, 4.7683],     # Amsterdam
    "MAD": [40.4983, -3.5676],    # Madrid
    "BCN": [41.2974, 2.0833],     # Barcelona
    "FCO": [41.8003, 12.2389],    # Rome
    "LGW": [51.1481, -0.1903],    # London Gatwick
    "MUC": [48.3537, 11.7750],    # Munich
    "ZRH": [47.4582, 8.5555],     # Zurich
    "DUB": [53.4264, -6.2499],    # Dublin
    "MAN": [53.3537, -2.2750],    # Manchester
    "CPH": [55.6180, 12.6508],    # Copenhagen
    "VIE": [48.1200, 16.5672],    # Vienna
    "ARN": [59.6497, 17.9237],    # Stockholm
    "OSL": [60.1975, 11.1004],    # Oslo
    "HEL": [60.3183, 24.9497],    # Helsinki
    "WAW": [52.1672, 20.9679],    # Warsaw
    "BRU": [50.9014, 4.4844],     # Brussels
    "ATH": [37.9356, 23.9484],    # Athens
    "LIS": [38.7756, -9.1354],    # Lisbon
    
    # Major Asian airports
    "HND": [35.5494, 139.7798],   # Tokyo Haneda
    "NRT": [35.7719, 140.3929],   # Tokyo Narita
    "PEK": [40.0799, 116.6031],   # Beijing
    "HKG": [22.3080, 113.9185],   # Hong Kong
    "ICN": [37.4602, 126.4407],   # Seoul Incheon
    "SIN": [1.3644, 103.9915],    # Singapore
    "BKK": [13.6900, 100.7501],   # Bangkok
    "KUL": [2.7456, 101.7099],    # Kuala Lumpur
    "DEL": [28.5562, 77.1000],    # Delhi
    "BOM": [19.0896, 72.8656],    # Mumbai
    "SYD": [33.9399, 151.1753],   # Sydney
    "MEL": [37.6690, 144.8410],   # Melbourne
    "AKL": [36.0086, 174.7853],   # Auckland
    "CGK": [6.1275, 106.6537],    # Jakarta
    "MNL": [14.5086, 121.0197],   # Manila
    
    # Middle East airports
    "DXB": [25.2528, 55.3644],    # Dubai
    "DOH": [25.2609, 51.6138],    # Doha
    "AUH": [24.4331, 54.6511],    # Abu Dhabi
    "IST": [41.2606, 28.7425],    # Istanbul
    "CAI": [30.1219, 31.4056],    # Cairo
    
    # Major African airports
    "JNB": [26.1367, 28.2412],    # Johannesburg
    "CPT": [33.9649, 18.6027],    # Cape Town
    "ADD": [8.9778, 38.7989],     # Addis Ababa
    "NBO": [1.3192, 36.9280],     # Nairobi
    "CMN": [33.3698, -7.5900],    # Casablanca
    
    # Major South American airports
    "GRU": [-23.4356, -46.4731],  # São Paulo
    "EZE": [-34.8222, -58.5358],  # Buenos Aires
    "BOG": [4.7016, -74.1469],    # Bogotá
    "SCL": [-33.3898, -70.7945],  # Santiago
    "LIM": [-12.0219, -77.1143],  # Lima
}

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
            
            # Get airport codes
            departure_airport = safe_get(flight_info, "departure", "iata")
            arrival_airport = safe_get(flight_info, "arrival", "iata")
            
            # Get coordinates from our lookup table if API doesn't provide them
            departure_lat = safe_get(flight_info, "departure", "latitude")
            departure_lon = safe_get(flight_info, "departure", "longitude")
            arrival_lat = safe_get(flight_info, "arrival", "latitude")
            arrival_lon = safe_get(flight_info, "arrival", "longitude")
            
            # If coordinates are missing, try to get them from our lookup table
            if not departure_lat and not departure_lon and departure_airport in AIRPORT_COORDINATES:
                departure_lat, departure_lon = AIRPORT_COORDINATES[departure_airport]
                logger.info(f"Using lookup table coordinates for {departure_airport}: {departure_lat}, {departure_lon}")
                
            if not arrival_lat and not arrival_lon and arrival_airport in AIRPORT_COORDINATES:
                arrival_lat, arrival_lon = AIRPORT_COORDINATES[arrival_airport]
                logger.info(f"Using lookup table coordinates for {arrival_airport}: {arrival_lat}, {arrival_lon}")
            
            # Get current position (if available)
            current_lat = safe_get(flight_info, "live", "latitude")
            current_lon = safe_get(flight_info, "live", "longitude")
            
            # If we don't have current position but we have both airports,
            # we can estimate a position along the route based on flight status
            if not current_lat and not current_lon and departure_lat and departure_lon and arrival_lat and arrival_lon:
                status = flight_info.get("flight_status", "").lower()
                
                if status == "scheduled":
                    # Not departed yet, use departure airport
                    current_lat, current_lon = departure_lat, departure_lon
                elif status == "landed" or status == "arrived":
                    # Already arrived, use arrival airport
                    current_lat, current_lon = arrival_lat, arrival_lon
                elif status == "active" or status == "en-route":
                    # In flight, estimate position halfway between airports
                    current_lat = (departure_lat + arrival_lat) / 2
                    current_lon = (departure_lon + arrival_lon) / 2
            
            # Format the return data
            formatted_data = {
                "flight_number": safe_get(flight_info, "flight", "iata") or flight_number,
                "airline": safe_get(flight_info, "airline", "name"),
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "scheduled_departure": format_date(safe_get(flight_info, "departure", "scheduled")),
                "scheduled_arrival": format_date(safe_get(flight_info, "arrival", "scheduled")),
                "actual_departure": format_date(safe_get(flight_info, "departure", "actual")),
                "actual_arrival": format_date(safe_get(flight_info, "arrival", "actual")),
                "status": flight_info.get("flight_status"),
                "departure_lat": departure_lat,
                "departure_lon": departure_lon,
                "arrival_lat": arrival_lat,
                "arrival_lon": arrival_lon,
                "current_lat": current_lat,
                "current_lon": current_lon, 
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
