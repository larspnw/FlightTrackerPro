// Component for displaying the flight on a map
const FlightMap = ({ flightDetails }) => {
  const mapRef = React.useRef(null);
  const mapInstanceRef = React.useRef(null);
  const markersRef = React.useRef([]);
  const pathRef = React.useRef(null);
  const planeMarkerRef = React.useRef(null);
  
  React.useEffect(() => {
    // Initialize map if not already created
    if (!mapInstanceRef.current && mapRef.current) {
      mapInstanceRef.current = L.map(mapRef.current, {
        attributionControl: false,
        zoomControl: true
      }).setView([20, 0], 2);
      
      // Add the tile layer (dark mode)
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
      }).addTo(mapInstanceRef.current);
    }
    
    // Return a cleanup function to run when the component unmounts
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);
  
  React.useEffect(() => {
    // Update map when flight details change
    if (!mapInstanceRef.current || !flightDetails) return;
    
    // Clear previous markers and path
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];
    
    if (pathRef.current) {
      pathRef.current.remove();
      pathRef.current = null;
    }
    
    if (planeMarkerRef.current) {
      planeMarkerRef.current.remove();
      planeMarkerRef.current = null;
    }
    
    // Create custom airport marker icon
    const airportIcon = L.divIcon({
      html: '<i class="fas fa-map-marker-alt fa-2x text-info"></i>',
      iconSize: [20, 20],
      iconAnchor: [10, 20],
      className: 'airport-marker'
    });
    
    // Create custom plane marker icon
    const planeIcon = L.divIcon({
      html: '<i class="fas fa-plane text-warning"></i>',
      iconSize: [20, 20],
      iconAnchor: [10, 10],
      className: 'plane-marker'
    });
    
    // Add departure airport marker if coordinates available
    if (flightDetails.departure_lat && flightDetails.departure_lon) {
      const departureMarker = L.marker(
        [flightDetails.departure_lat, flightDetails.departure_lon],
        { icon: airportIcon }
      ).addTo(mapInstanceRef.current);
      
      departureMarker.bindPopup(`
        <strong>${flightDetails.departure_airport}</strong><br>
        Departure Airport
      `);
      
      markersRef.current.push(departureMarker);
    }
    
    // Add arrival airport marker if coordinates available
    if (flightDetails.arrival_lat && flightDetails.arrival_lon) {
      const arrivalMarker = L.marker(
        [flightDetails.arrival_lat, flightDetails.arrival_lon],
        { icon: airportIcon }
      ).addTo(mapInstanceRef.current);
      
      arrivalMarker.bindPopup(`
        <strong>${flightDetails.arrival_airport}</strong><br>
        Arrival Airport
      `);
      
      markersRef.current.push(arrivalMarker);
    }
    
    // Draw path between departure and arrival if both coordinates available
    if (flightDetails.departure_lat && flightDetails.departure_lon && 
        flightDetails.arrival_lat && flightDetails.arrival_lon) {
      
      // Calculate a slightly curved path for better visualization
      const latlngs = [
        [flightDetails.departure_lat, flightDetails.departure_lon],
        [flightDetails.arrival_lat, flightDetails.arrival_lon]
      ];
      
      pathRef.current = L.polyline(latlngs, {
        color: '#1e88e5',
        weight: 2,
        opacity: 0.7,
        className: 'flight-path'
      }).addTo(mapInstanceRef.current);
      
      // Add the current position of the plane if available
      if (flightDetails.current_lat && flightDetails.current_lon) {
        planeMarkerRef.current = L.marker(
          [flightDetails.current_lat, flightDetails.current_lon],
          { icon: planeIcon }
        ).addTo(mapInstanceRef.current);
        
        planeMarkerRef.current.bindPopup(`
          <strong>${flightDetails.flight_number}</strong><br>
          Altitude: ${flightDetails.altitude ? flightDetails.altitude.toLocaleString() + ' ft' : 'N/A'}<br>
          Speed: ${flightDetails.speed ? flightDetails.speed.toLocaleString() + ' km/h' : 'N/A'}
        `);
      }
      
      // Fit the map to show the entire route
      const bounds = L.latLngBounds(latlngs);
      mapInstanceRef.current.fitBounds(bounds, {
        padding: [50, 50],
        maxZoom: 10
      });
    }
    // If only one airport has coordinates, center on it
    else if (flightDetails.departure_lat && flightDetails.departure_lon) {
      mapInstanceRef.current.setView(
        [flightDetails.departure_lat, flightDetails.departure_lon],
        6
      );
    }
    else if (flightDetails.arrival_lat && flightDetails.arrival_lon) {
      mapInstanceRef.current.setView(
        [flightDetails.arrival_lat, flightDetails.arrival_lon],
        6
      );
    }
    
  }, [flightDetails]);
  
  return (
    <div className="map-container mb-4" ref={mapRef}></div>
  );
};
