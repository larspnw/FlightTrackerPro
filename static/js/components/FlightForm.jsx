// Component for adding a new flight
const FlightForm = ({ onAddFlight, isLoading }) => {
  const [flightNumber, setFlightNumber] = React.useState('');
  const [error, setError] = React.useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!flightNumber.trim()) {
      setError('Please enter a flight number');
      return;
    }
    
    // Flight number format validation (simple check)
    const flightRegex = /^[A-Za-z0-9]{2,3}\d{1,4}[A-Za-z]?$/;
    if (!flightRegex.test(flightNumber.trim())) {
      setError('Please enter a valid flight number (e.g., BA123, DL4567)');
      return;
    }
    
    setError('');
    onAddFlight(flightNumber.trim());
    setFlightNumber('');
  };
  
  return (
    <div className="flight-form">
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="flightNumber" className="form-label">Add Flight</label>
          <div className="input-group">
            <input
              type="text"
              className={`form-control ${error ? 'is-invalid' : ''}`}
              id="flightNumber"
              placeholder="e.g., BA123"
              value={flightNumber}
              onChange={(e) => setFlightNumber(e.target.value.toUpperCase())}
              disabled={isLoading}
            />
            <button 
              className="btn btn-primary" 
              type="submit"
              disabled={isLoading || !flightNumber.trim()}
            >
              {isLoading ? (
                <span className="loading-spinner"></span>
              ) : (
                <i className="fas fa-plus"></i>
              )}
            </button>
          </div>
          {error && <div className="invalid-feedback d-block">{error}</div>}
          <small className="form-text text-muted">
            Enter the airline code and flight number (e.g., BA123, DL4567)
          </small>
        </div>
      </form>
    </div>
  );
};
