import logging
from flask import render_template, request, jsonify
from app import app, db
from models import Flight, SavedFlight
from aviation_api import get_flight_data
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/api/flights', methods=['GET'])
def get_flights():
    """Get all tracked flights"""
    try:
        saved_flights = SavedFlight.query.all()
        return jsonify({
            'success': True,
            'flights': [flight.to_dict() for flight in saved_flights]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving flights: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve flight data',
            'details': str(e)
        }), 500

@app.route('/api/flights/add', methods=['POST'])
def add_flight():
    """Add a new flight to track"""
    try:
        data = request.get_json()
        flight_number = data.get('flight_number', '').strip().upper()
        
        if not flight_number:
            return jsonify({
                'success': False,
                'error': 'Flight number is required'
            }), 400
        
        # Check if flight already exists
        existing_flight = SavedFlight.query.filter_by(flight_number=flight_number).first()
        if existing_flight:
            return jsonify({
                'success': False,
                'error': 'Flight is already being tracked'
            }), 400
        
        # Check if we've reached the limit of 3 flights
        flight_count = SavedFlight.query.count()
        if flight_count >= 3:
            return jsonify({
                'success': False,
                'error': 'Maximum limit of 3 flights reached. Remove a flight to add a new one.'
            }), 400
        
        # Get flight data from API
        flight_data = get_flight_data(flight_number)
        if not flight_data or 'error' in flight_data:
            return jsonify({
                'success': False,
                'error': flight_data.get('error', 'Flight not found or invalid flight number')
            }), 404
        
        # Save the flight
        new_saved_flight = SavedFlight(flight_number=flight_number)
        db.session.add(new_saved_flight)
        
        # Store detailed flight data
        new_flight = Flight(
            flight_number=flight_number,
            airline=flight_data.get('airline'),
            departure_airport=flight_data.get('departure_airport'),
            arrival_airport=flight_data.get('arrival_airport'),
            scheduled_departure=datetime.fromisoformat(flight_data.get('scheduled_departure')) if flight_data.get('scheduled_departure') else None,
            scheduled_arrival=datetime.fromisoformat(flight_data.get('scheduled_arrival')) if flight_data.get('scheduled_arrival') else None,
            actual_departure=datetime.fromisoformat(flight_data.get('actual_departure')) if flight_data.get('actual_departure') else None,
            actual_arrival=datetime.fromisoformat(flight_data.get('actual_arrival')) if flight_data.get('actual_arrival') else None,
            status=flight_data.get('status'),
            departure_lat=flight_data.get('departure_lat'),
            departure_lon=flight_data.get('departure_lon'),
            arrival_lat=flight_data.get('arrival_lat'),
            arrival_lon=flight_data.get('arrival_lon'),
            current_lat=flight_data.get('current_lat'),
            current_lon=flight_data.get('current_lon'),
            altitude=flight_data.get('altitude'),
            speed=flight_data.get('speed')
        )
        db.session.add(new_flight)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Flight added successfully',
            'flight': flight_data
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding flight: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Failed to add flight',
            'details': str(e)
        }), 500

@app.route('/api/flights/remove/<flight_number>', methods=['DELETE'])
def remove_flight(flight_number):
    """Remove a flight from tracking"""
    try:
        flight = SavedFlight.query.filter_by(flight_number=flight_number).first()
        if flight:
            db.session.delete(flight)
            # Also remove any detailed flight data
            flight_details = Flight.query.filter_by(flight_number=flight_number).first()
            if flight_details:
                db.session.delete(flight_details)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Flight removed successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Flight not found'
            }), 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error removing flight: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to remove flight',
            'details': str(e)
        }), 500

@app.route('/api/flights/update/<flight_number>', methods=['GET'])
def update_flight(flight_number):
    """Update flight data"""
    try:
        # Check if flight exists
        saved_flight = SavedFlight.query.filter_by(flight_number=flight_number).first()
        if not saved_flight:
            return jsonify({
                'success': False,
                'error': 'Flight not found'
            }), 404
        
        # Get updated flight data from API
        flight_data = get_flight_data(flight_number)
        if not flight_data or 'error' in flight_data:
            return jsonify({
                'success': False,
                'error': flight_data.get('error', 'Failed to retrieve flight data')
            }), 400
        
        # Update flight details in database
        flight = Flight.query.filter_by(flight_number=flight_number).first()
        if flight:
            flight.airline = flight_data.get('airline', flight.airline)
            flight.departure_airport = flight_data.get('departure_airport', flight.departure_airport)
            flight.arrival_airport = flight_data.get('arrival_airport', flight.arrival_airport)
            flight.scheduled_departure = datetime.fromisoformat(flight_data.get('scheduled_departure')) if flight_data.get('scheduled_departure') else flight.scheduled_departure
            flight.scheduled_arrival = datetime.fromisoformat(flight_data.get('scheduled_arrival')) if flight_data.get('scheduled_arrival') else flight.scheduled_arrival
            flight.actual_departure = datetime.fromisoformat(flight_data.get('actual_departure')) if flight_data.get('actual_departure') else flight.actual_departure
            flight.actual_arrival = datetime.fromisoformat(flight_data.get('actual_arrival')) if flight_data.get('actual_arrival') else flight.actual_arrival
            flight.status = flight_data.get('status', flight.status)
            flight.departure_lat = flight_data.get('departure_lat', flight.departure_lat)
            flight.departure_lon = flight_data.get('departure_lon', flight.departure_lon)
            flight.arrival_lat = flight_data.get('arrival_lat', flight.arrival_lat)
            flight.arrival_lon = flight_data.get('arrival_lon', flight.arrival_lon)
            flight.current_lat = flight_data.get('current_lat', flight.current_lat)
            flight.current_lon = flight_data.get('current_lon', flight.current_lon)
            flight.altitude = flight_data.get('altitude', flight.altitude)
            flight.speed = flight_data.get('speed', flight.speed)
            flight.last_updated = datetime.utcnow()
            db.session.commit()
        else:
            # If for some reason the detailed flight data doesn't exist, create it
            new_flight = Flight(
                flight_number=flight_number,
                airline=flight_data.get('airline'),
                departure_airport=flight_data.get('departure_airport'),
                arrival_airport=flight_data.get('arrival_airport'),
                scheduled_departure=datetime.fromisoformat(flight_data.get('scheduled_departure')) if flight_data.get('scheduled_departure') else None,
                scheduled_arrival=datetime.fromisoformat(flight_data.get('scheduled_arrival')) if flight_data.get('scheduled_arrival') else None,
                actual_departure=datetime.fromisoformat(flight_data.get('actual_departure')) if flight_data.get('actual_departure') else None,
                actual_arrival=datetime.fromisoformat(flight_data.get('actual_arrival')) if flight_data.get('actual_arrival') else None,
                status=flight_data.get('status'),
                departure_lat=flight_data.get('departure_lat'),
                departure_lon=flight_data.get('departure_lon'),
                arrival_lat=flight_data.get('arrival_lat'),
                arrival_lon=flight_data.get('arrival_lon'),
                current_lat=flight_data.get('current_lat'),
                current_lon=flight_data.get('current_lon'),
                altitude=flight_data.get('altitude'),
                speed=flight_data.get('speed')
            )
            db.session.add(new_flight)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'flight': flight_data
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating flight: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Failed to update flight data',
            'details': str(e)
        }), 500

@app.route('/api/flights/details/<flight_number>', methods=['GET'])
def get_flight_details(flight_number):
    """Get detailed information about a specific flight"""
    try:
        flight = Flight.query.filter_by(flight_number=flight_number).first()
        if flight:
            return jsonify({
                'success': True,
                'flight': flight.to_dict()
            }), 200
        else:
            # If not in database, try to fetch from API
            flight_data = get_flight_data(flight_number)
            if flight_data and 'error' not in flight_data:
                return jsonify({
                    'success': True,
                    'flight': flight_data
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Flight not found'
                }), 404
    except Exception as e:
        logger.error(f"Error retrieving flight details: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve flight details',
            'details': str(e)
        }), 500

@app.route('/api/flights/update-all', methods=['GET'])
def update_all_flights():
    """Update all tracked flights"""
    try:
        saved_flights = SavedFlight.query.all()
        updated_flights = []
        
        for saved_flight in saved_flights:
            flight_data = get_flight_data(saved_flight.flight_number)
            if flight_data and 'error' not in flight_data:
                # Update flight details in database
                flight = Flight.query.filter_by(flight_number=saved_flight.flight_number).first()
                if flight:
                    flight.airline = flight_data.get('airline', flight.airline)
                    flight.departure_airport = flight_data.get('departure_airport', flight.departure_airport)
                    flight.arrival_airport = flight_data.get('arrival_airport', flight.arrival_airport)
                    flight.scheduled_departure = datetime.fromisoformat(flight_data.get('scheduled_departure')) if flight_data.get('scheduled_departure') else flight.scheduled_departure
                    flight.scheduled_arrival = datetime.fromisoformat(flight_data.get('scheduled_arrival')) if flight_data.get('scheduled_arrival') else flight.scheduled_arrival
                    flight.actual_departure = datetime.fromisoformat(flight_data.get('actual_departure')) if flight_data.get('actual_departure') else flight.actual_departure
                    flight.actual_arrival = datetime.fromisoformat(flight_data.get('actual_arrival')) if flight_data.get('actual_arrival') else flight.actual_arrival
                    flight.status = flight_data.get('status', flight.status)
                    flight.departure_lat = flight_data.get('departure_lat', flight.departure_lat)
                    flight.departure_lon = flight_data.get('departure_lon', flight.departure_lon)
                    flight.arrival_lat = flight_data.get('arrival_lat', flight.arrival_lat)
                    flight.arrival_lon = flight_data.get('arrival_lon', flight.arrival_lon)
                    flight.current_lat = flight_data.get('current_lat', flight.current_lat)
                    flight.current_lon = flight_data.get('current_lon', flight.current_lon)
                    flight.altitude = flight_data.get('altitude', flight.altitude)
                    flight.speed = flight_data.get('speed', flight.speed)
                    flight.last_updated = datetime.utcnow()
                else:
                    # If for some reason the detailed flight data doesn't exist, create it
                    new_flight = Flight(
                        flight_number=saved_flight.flight_number,
                        airline=flight_data.get('airline'),
                        departure_airport=flight_data.get('departure_airport'),
                        arrival_airport=flight_data.get('arrival_airport'),
                        scheduled_departure=datetime.fromisoformat(flight_data.get('scheduled_departure')) if flight_data.get('scheduled_departure') else None,
                        scheduled_arrival=datetime.fromisoformat(flight_data.get('scheduled_arrival')) if flight_data.get('scheduled_arrival') else None,
                        actual_departure=datetime.fromisoformat(flight_data.get('actual_departure')) if flight_data.get('actual_departure') else None,
                        actual_arrival=datetime.fromisoformat(flight_data.get('actual_arrival')) if flight_data.get('actual_arrival') else None,
                        status=flight_data.get('status'),
                        departure_lat=flight_data.get('departure_lat'),
                        departure_lon=flight_data.get('departure_lon'),
                        arrival_lat=flight_data.get('arrival_lat'),
                        arrival_lon=flight_data.get('arrival_lon'),
                        current_lat=flight_data.get('current_lat'),
                        current_lon=flight_data.get('current_lon'),
                        altitude=flight_data.get('altitude'),
                        speed=flight_data.get('speed')
                    )
                    db.session.add(new_flight)
                
                updated_flights.append(flight_data)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'{len(updated_flights)} flights updated successfully',
            'flights': updated_flights
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating all flights: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update flights',
            'details': str(e)
        }), 500
