// Component for displaying the list of tracked flights
const FlightList = ({ flights, selectedFlight, onSelectFlight, onRemoveFlight, isLoading }) => {
  if (flights.length === 0) {
    return (
      <div className="empty-state">
        <p>No flights added yet</p>
        <small>Add a flight using the form above</small>
      </div>
    );
  }
  
  return (
    <div className="flight-list">
      <ul className="list-group">
        {flights.map((flight) => (
          <li
            key={flight.flight_number}
            className={`list-group-item flight-card d-flex justify-content-between align-items-center ${selectedFlight === flight.flight_number ? 'active' : ''}`}
            onClick={() => onSelectFlight(flight.flight_number)}
          >
            <div>
              <strong>{flight.flight_number}</strong>
            </div>
            <button
              className="btn btn-sm btn-outline-danger"
              onClick={(e) => {
                e.stopPropagation();
                onRemoveFlight(flight.flight_number);
              }}
              disabled={isLoading}
            >
              <i className="fas fa-times"></i>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};
