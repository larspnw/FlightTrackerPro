// Component for displaying detailed flight information
const FlightDetails = ({ flightDetails, isLoading }) => {
  if (!flightDetails) return null;
  
  // Format date and time
  const formatDateTime = (dateTimeStr) => {
    if (!dateTimeStr) return 'N/A';
    
    const date = new Date(dateTimeStr);
    
    // Format: "Mon, 15 Jul 2023 14:30 (GMT)"
    const options = { 
      weekday: 'short',
      day: 'numeric', 
      month: 'short', 
      year: 'numeric',
      hour: '2-digit', 
      minute: '2-digit',
      timeZoneName: 'short'
    };
    
    return date.toLocaleString('en-US', options);
  };
  
  // Determine flight status class
  const getStatusClass = (status) => {
    if (!status) return 'status-unknown';
    
    const statusLower = status.toLowerCase();
    if (statusLower.includes('scheduled')) return 'status-scheduled';
    if (statusLower.includes('active') || statusLower.includes('en-route')) return 'status-active';
    if (statusLower.includes('landed')) return 'status-landed';
    if (statusLower.includes('cancelled')) return 'status-cancelled';
    if (statusLower.includes('delayed')) return 'status-delayed';
    if (statusLower.includes('diverted')) return 'status-diverted';
    
    return 'status-unknown';
  };
  
  // Calculate delay in minutes
  const calculateDelay = (scheduled, actual) => {
    if (!scheduled || !actual) return null;
    
    const scheduledDate = new Date(scheduled);
    const actualDate = new Date(actual);
    
    // Get difference in minutes
    const delayMinutes = Math.round((actualDate - scheduledDate) / (1000 * 60));
    
    return delayMinutes;
  };
  
  // Format delay display
  const formatDelay = (delayMinutes) => {
    if (delayMinutes === null) return '';
    
    if (delayMinutes <= 0) {
      return <span className="text-success">On time</span>;
    }
    
    // Format hours and minutes
    const hours = Math.floor(delayMinutes / 60);
    const minutes = delayMinutes % 60;
    
    let delayText = '';
    if (hours > 0) {
      delayText += `${hours}h `;
    }
    if (minutes > 0 || hours === 0) {
      delayText += `${minutes}m`;
    }
    
    return <span className="text-warning">Delayed by {delayText}</span>;
  };
  
  // Calculate departure delay
  const departureDelay = calculateDelay(flightDetails.scheduled_departure, flightDetails.actual_departure);
  
  // Calculate arrival delay
  const arrivalDelay = calculateDelay(flightDetails.scheduled_arrival, flightDetails.actual_arrival);
  
  const statusClass = getStatusClass(flightDetails.status);
  
  return (
    <div className="flight-details">
      {isLoading && <LoadingIndicator />}
      
      <div className="row">
        <div className="col-12 mb-3">
          <div className="alert alert-secondary d-flex justify-content-between align-items-center">
            <div>
              <h4 className="alert-heading mb-0">
                {flightDetails.airline ? `${flightDetails.airline} ` : ''}
                {flightDetails.flight_number}
              </h4>
              <div className={statusClass}>
                <i className="fas fa-circle me-1"></i>
                {flightDetails.status || 'Unknown Status'}
              </div>
            </div>
            <div className="text-end">
              <div>
                <strong>From:</strong> {flightDetails.departure_airport || 'N/A'}
              </div>
              <div>
                <strong>To:</strong> {flightDetails.arrival_airport || 'N/A'}
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-6 mb-3">
          <div className="card h-100">
            <div className="card-header">
              <h5 className="mb-0">Departure</h5>
            </div>
            <div className="card-body">
              <p className="mb-1">
                <strong>Airport:</strong> {flightDetails.departure_airport || 'N/A'}
              </p>
              <p className="mb-1">
                <strong>Scheduled:</strong> {formatDateTime(flightDetails.scheduled_departure)}
              </p>
              <p className="mb-1">
                <strong>Actual:</strong> {formatDateTime(flightDetails.actual_departure)}
              </p>
              <p className="mb-0 delay-indicator">
                {formatDelay(departureDelay)}
              </p>
            </div>
          </div>
        </div>
        
        <div className="col-md-6 mb-3">
          <div className="card h-100">
            <div className="card-header">
              <h5 className="mb-0">Arrival</h5>
            </div>
            <div className="card-body">
              <p className="mb-1">
                <strong>Airport:</strong> {flightDetails.arrival_airport || 'N/A'}
              </p>
              <p className="mb-1">
                <strong>Scheduled:</strong> {formatDateTime(flightDetails.scheduled_arrival)}
              </p>
              <p className="mb-1">
                <strong>Actual:</strong> {formatDateTime(flightDetails.actual_arrival)}
              </p>
              <p className="mb-0 delay-indicator">
                {formatDelay(arrivalDelay)}
              </p>
            </div>
          </div>
        </div>
        
        {(flightDetails.altitude || flightDetails.speed) && (
          <div className="col-12 mb-3">
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">Live Data</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  {flightDetails.altitude && (
                    <div className="col-md-6 mb-2">
                      <div className="d-flex align-items-center">
                        <i className="fas fa-arrow-up me-2"></i>
                        <div>
                          <div className="text-muted small">Altitude</div>
                          <div><strong>{flightDetails.altitude.toLocaleString()} ft</strong></div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {flightDetails.speed && (
                    <div className="col-md-6 mb-2">
                      <div className="d-flex align-items-center">
                        <i className="fas fa-tachometer-alt me-2"></i>
                        <div>
                          <div className="text-muted small">Speed</div>
                          <div><strong>{flightDetails.speed.toLocaleString()} km/h</strong></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div className="col-12">
          <small className="text-muted">
            <i className="fas fa-clock me-1"></i>
            Last updated: {formatDateTime(flightDetails.last_updated)}
          </small>
        </div>
      </div>
    </div>
  );
};
