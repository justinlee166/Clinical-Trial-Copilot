import React, { useState } from 'react';

function SimpleApp() {
  const [currentPage, setCurrentPage] = useState('upload');

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🏥 Clinical Trial Copilot</h1>
      <p>Current page: {currentPage}</p>
      
      {currentPage === 'upload' && (
        <div>
          <h2>Upload Page</h2>
          <p>This is the upload page content.</p>
          <button 
            onClick={() => setCurrentPage('results')}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#3b82f6', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Go to Results
          </button>
        </div>
      )}
      
      {currentPage === 'results' && (
        <div>
          <h2>Results Page</h2>
          <p>This is the results page content.</p>
          <button 
            onClick={() => setCurrentPage('upload')}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#6b7280', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Back to Upload
          </button>
        </div>
      )}
    </div>
  );
}

export default SimpleApp;
