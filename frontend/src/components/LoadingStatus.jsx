function LoadingStatus({theme}) {
    return <div className="loading-container">
        <h2>Generating your {theme} story</h2>
        <div className="loading-animation">
            <div className="spinner"></div>
        </div>
        <p className="loading-info">
            Please wait while we generate your story
        </p>
    </div>
}

// you need to export the Component...
export default LoadingStatus; 