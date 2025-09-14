import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import ProgressBar from '../components/ProgressBar';
import { Play, AlertCircle } from 'lucide-react';
import { analyzePDF } from '../services/api';

const UploadPage = ({ onAnalysisComplete, onStartAnalysis, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('idle');

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first');
      return;
    }

    try {
      onStartAnalysis();
      setStatus('processing');
      setProgress(0);
      setError(null);

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.random() * 15;
        });
      }, 1000);

      const apiResponse = await analyzePDF(selectedFile);
      
      // Debug: Log the API response
      console.log('API Response:', apiResponse);
      console.log('API Response Keys:', Object.keys(apiResponse));
      
      clearInterval(progressInterval);
      setProgress(100);
      setStatus('completed');
      
      // Extract the actual results from the API response
      const result = apiResponse.results || apiResponse;
      
      // Debug: Log the extracted result
      console.log('Extracted Result:', result);
      console.log('Result Keys:', Object.keys(result));
      
      setTimeout(() => {
        onAnalysisComplete(result);
      }, 1000);

    } catch (err) {
      setStatus('error');
      setError(err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Analyze Clinical Trial PDF
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload a clinical trial PDF to get AI-powered analysis, insights, and visualizations
          using Cerebras and Claude AI.
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-medium text-red-800">Analysis Failed</h3>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Upload Section */}
      {status === 'idle' && (
        <div className="space-y-6">
          <FileUpload
            onFileSelect={handleFileSelect}
            disabled={isLoading}
          />
          
          {selectedFile && (
            <div className="text-center">
              <button
                onClick={handleAnalyze}
                disabled={isLoading}
                className="btn-primary flex items-center space-x-2 mx-auto text-lg px-8 py-3"
              >
                <Play className="h-5 w-5" />
                <span>Start Analysis</span>
              </button>
            </div>
          )}
        </div>
      )}

      {/* Progress Section */}
      {status === 'processing' && (
        <ProgressBar
          status="processing"
          progress={progress}
          message="Processing your clinical trial PDF..."
        />
      )}

      {/* Features Section */}
      {status === 'idle' && (
        <div className="mt-16">
          <h2 className="text-2xl font-semibold text-gray-900 text-center mb-8">
            What You'll Get
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🧠</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600 text-sm">
                Comprehensive clinical insights powered by Claude AI
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Visualizations</h3>
              <p className="text-gray-600 text-sm">
                Charts, graphs, and dashboards for data insights
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📁</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Export Options</h3>
              <p className="text-gray-600 text-sm">
                Download results in JSON, CSV, and report formats
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
