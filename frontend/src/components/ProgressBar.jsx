import React from 'react';
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react';

const ProgressBar = ({ status, progress = 0, message = '' }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'processing':
        return <Loader2 className="h-5 w-5 animate-spin text-primary-600" />;
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-600" />;
      default:
        return <Loader2 className="h-5 w-5 animate-spin text-primary-600" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'processing':
        return 'bg-primary-600';
      case 'completed':
        return 'bg-green-600';
      case 'error':
        return 'bg-red-600';
      default:
        return 'bg-primary-600';
    }
  };

  return (
    <div className="card">
      <div className="flex items-center space-x-3 mb-4">
        {getStatusIcon()}
        <div className="flex-1">
          <h3 className="font-medium text-gray-900">
            {status === 'processing' && 'Processing Clinical Trial'}
            {status === 'completed' && 'Analysis Complete'}
            {status === 'error' && 'Analysis Failed'}
          </h3>
          {message && (
            <p className="text-sm text-gray-600 mt-1">{message}</p>
          )}
        </div>
      </div>
      
      {status === 'processing' && (
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${getStatusColor()}`}
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}
      
      {status === 'processing' && (
        <div className="mt-3 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Step 1: Extracting data with Cerebras</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressBar;
