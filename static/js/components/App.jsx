// Main App component
const App = () => {
  const [flights, setFlights] = React.useState([]);
  const [selectedFlight, setSelectedFlight] = React.useState(null);
  const [flightDetails, setFlightDetails] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [autoRefresh, setAutoRefresh] = React.useState(false);
  const [refreshInterval, setRefreshIntervalState] = React.useState(null);
  
  // Reference to store the interval ID
  const refreshIntervalRef = React.useRef(null);
  
  // Set refresh interval state and update the ref
  const setRefreshInterval = (interval) => {
    setRefreshIntervalState(interval);
    refreshIntervalRef.current = interval;
  };
  
  // Fetch saved flights on component mount
  React.useEffect(() => {
    fetchFlights();
    
    // Cleanup function to clear any intervals on unmount
    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, []);
  
  // Handle auto-refresh toggle
  React.useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        refreshAllFlights();
      }, 60000); // Refresh every minute
      
      setRefreshInterval(interval);
    } else if (refreshInterval) {
      clearInterval(refreshInterval);
      setRefreshInterval(null);
    }
    
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [autoRefresh]);
  
  // Fetch all saved flights from the backend
  const fetchFlights = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/flights');
      const data = await response.json();
      
      if (data.success) {
        setFlights(data.flights);
        if (data.flights.length > 0 && !selectedFlight) {
          // Select the first flight by default
          selectFlight(data.flights[0].flight_number);
        } else if (selectedFlight) {
          // Refresh the selected flight details
          selectFlight(selectedFlight);
        }
      } else {
        setError(data.error || 'Failed to fetch flights');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error fetching flights:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Add a new flight to track
  const addFlight = async (flightNumber) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/flights/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ flight_number: flightNumber }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        await fetchFlights();
        selectFlight(flightNumber);
      } else {
        setError(data.error || 'Failed to add flight');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error adding flight:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Remove a flight from tracking
  const removeFlight = async (flightNumber) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/flights/remove/${flightNumber}`, {
        method: 'DELETE',
      });
      
      const data = await response.json();
      
      if (data.success) {
        if (selectedFlight === flightNumber) {
          setSelectedFlight(null);
          setFlightDetails(null);
        }
        await fetchFlights();
      } else {
        setError(data.error || 'Failed to remove flight');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error removing flight:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Select a flight to view details
  const selectFlight = async (flightNumber) => {
    try {
      setSelectedFlight(flightNumber);
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/flights/details/${flightNumber}`);
      const data = await response.json();
      
      if (data.success) {
        setFlightDetails(data.flight);
      } else {
        setError(data.error || 'Failed to fetch flight details');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error fetching flight details:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Refresh data for the selected flight
  const refreshFlight = async () => {
    if (!selectedFlight) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/flights/update/${selectedFlight}`);
      const data = await response.json();
      
      if (data.success) {
        setFlightDetails(data.flight);
      } else {
        setError(data.error || 'Failed to update flight data');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error refreshing flight:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Refresh all tracked flights
  const refreshAllFlights = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/flights/update-all');
      const data = await response.json();
      
      if (data.success) {
        await fetchFlights();
      } else {
        setError(data.error || 'Failed to update flights');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
      console.error('Error refreshing all flights:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Toggle auto-refresh
  const toggleAutoRefresh = () => {
    setAutoRefresh(!autoRefresh);
  };
  
  return (
    <div className="container py-4">
      <header className="mb-4">
        <div className="d-flex justify-content-between align-items-center">
          <h1 className="mb-0">
            <i className="fas fa-plane me-2"></i>
            Flight Tracker
          </h1>
          <div className="d-flex align-items-center">
            <div className="form-check form-switch me-3">
              <input 
                className="form-check-input" 
                type="checkbox" 
                id="autoRefreshToggle" 
                checked={autoRefresh}
                onChange={toggleAutoRefresh}
              />
              <label className="form-check-label" htmlFor="autoRefreshToggle">
                Auto-refresh
              </label>
            </div>
            <button 
              className={`btn btn-sm btn-outline-info refresh-btn ${loading ? 'refreshing' : ''}`}
              onClick={refreshAllFlights}
              disabled={loading}
            >
              <i className="fas fa-sync-alt"></i> Refresh All
            </button>
          </div>
        </div>
      </header>
      
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}
      
      <div className="row g-4">
        <div className="col-md-4">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Tracked Flights</h5>
            </div>
            <div className="card-body">
              <FlightForm onAddFlight={addFlight} isLoading={loading} />
              <hr />
              <FlightList 
                flights={flights} 
                selectedFlight={selectedFlight}
                onSelectFlight={selectFlight}
                onRemoveFlight={removeFlight}
                isLoading={loading}
              />
            </div>
          </div>
        </div>
        
        <div className="col-md-8">
          {selectedFlight && flightDetails ? (
            <>
              <div className="card mb-4">
                <div className="card-header d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">Flight Details</h5>
                  <button 
                    className="btn btn-sm btn-outline-secondary" 
                    onClick={refreshFlight}
                    disabled={loading}
                  >
                    <i className={`fas fa-sync-alt ${loading ? 'fa-spin' : ''}`}></i> Refresh
                  </button>
                </div>
                <div className="card-body">
                  <FlightMap flightDetails={flightDetails} />
                  <FlightDetails flightDetails={flightDetails} isLoading={loading} />
                </div>
              </div>
            </>
          ) : (
            <div className="card">
              <div className="card-body empty-state">
                <i className="fas fa-plane"></i>
                <h3>No Flight Selected</h3>
                <p>Add a flight or select one from the list to view its details.</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <footer className="mt-5 text-center text-muted">
        <small>© {new Date().getFullYear()} Flight Tracker | Data refreshed {loading ? 'now' : autoRefresh ? 'automatically' : 'manually'}</small>
      </footer>
    </div>
  );
};
