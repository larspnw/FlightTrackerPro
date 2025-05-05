// Loading indicator component
const LoadingIndicator = () => {
  return (
    <div className="loading-overlay d-flex justify-content-center align-items-center p-3">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};
