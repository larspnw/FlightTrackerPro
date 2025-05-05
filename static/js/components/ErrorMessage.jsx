// Error message component
const ErrorMessage = ({ message, onDismiss }) => {
  if (!message) return null;
  
  return (
    <div className="alert alert-danger alert-dismissible fade show mb-4" role="alert">
      <div className="d-flex align-items-center">
        <i className="fas fa-exclamation-circle me-2"></i>
        <div>{message}</div>
      </div>
      <button 
        type="button" 
        className="btn-close" 
        aria-label="Close" 
        onClick={onDismiss}
      ></button>
    </div>
  );
};
