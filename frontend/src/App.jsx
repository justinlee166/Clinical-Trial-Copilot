import React, { useState } from 'react';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';
import { Brain } from 'lucide-react';

function App() {
  const [currentPage, setCurrentPage] = useState('upload');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    setCurrentPage('results');
    setIsLoading(false);
  };

  const handleStartAnalysis = () => {
    setIsLoading(true);
  };

  const handleBackToUpload = () => {
    setCurrentPage('upload');
    setAnalysisResult(null);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Brain className="h-8 w-8 text-primary-600" />
              <h1 className="text-xl font-semibold text-gray-900">
                Clinical Trial Copilot
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              AI-Powered Clinical Trial Analysis
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentPage === 'upload' && (
          <UploadPage
            onAnalysisComplete={handleAnalysisComplete}
            onStartAnalysis={handleStartAnalysis}
            isLoading={isLoading}
          />
        )}
        
        {currentPage === 'results' && analysisResult && (
          <ResultsPage
            result={analysisResult}
            onBackToUpload={handleBackToUpload}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>Clinical Trial Copilot - Powered by Cerebras & Claude AI</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
