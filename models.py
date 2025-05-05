from datetime import datetime
from app import db


class Flight(db.Model):
    """Model for storing flight tracking information"""
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    airline = db.Column(db.String(100))
    departure_airport = db.Column(db.String(5))
    arrival_airport = db.Column(db.String(5))
    scheduled_departure = db.Column(db.DateTime)
    scheduled_arrival = db.Column(db.DateTime)
    actual_departure = db.Column(db.DateTime)
    actual_arrival = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    departure_lat = db.Column(db.Float)
    departure_lon = db.Column(db.Float)
    arrival_lat = db.Column(db.Float)
    arrival_lon = db.Column(db.Float)
    current_lat = db.Column(db.Float)
    current_lon = db.Column(db.Float)
    altitude = db.Column(db.Float)
    speed = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Flight {self.flight_number}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "airline": self.airline,
            "departure_airport": self.departure_airport,
            "arrival_airport": self.arrival_airport,
            "scheduled_departure": self.scheduled_departure.isoformat() if self.scheduled_departure else None,
            "scheduled_arrival": self.scheduled_arrival.isoformat() if self.scheduled_arrival else None,
            "actual_departure": self.actual_departure.isoformat() if self.actual_departure else None,
            "actual_arrival": self.actual_arrival.isoformat() if self.actual_arrival else None,
            "status": self.status,
            "departure_lat": self.departure_lat,
            "departure_lon": self.departure_lon,
            "arrival_lat": self.arrival_lat,
            "arrival_lon": self.arrival_lon,
            "current_lat": self.current_lat,
            "current_lon": self.current_lon,
            "altitude": self.altitude,
            "speed": self.speed,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }


class SavedFlight(db.Model):
    """Model for storing user's saved flights"""
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SavedFlight {self.flight_number}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "date_added": self.date_added.isoformat() if self.date_added else None
        }
