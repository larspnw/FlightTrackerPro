// Main application entry point
document.addEventListener('DOMContentLoaded', () => {
  // For React 18 using the new API
  try {
    const root = ReactDOM.createRoot(document.getElementById('app'));
    root.render(React.createElement(App));
  } catch (error) {
    console.error("Error rendering React application:", error);
    
    // Fallback to older React API if needed
    try {
      ReactDOM.render(
        React.createElement(App),
        document.getElementById('app')
      );
    } catch (fallbackError) {
      console.error("Fallback rendering also failed:", fallbackError);
      
      // Display error to user
      document.getElementById('app').innerHTML = `
        <div class="container py-5 text-center">
          <div class="alert alert-danger">
            <h3>Application Error</h3>
            <p>There was a problem loading the Flight Tracker application.</p>
            <p>Please refresh the page or try again later.</p>
          </div>
        </div>
      `;
    }
  }
});
