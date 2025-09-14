import React from 'react';
import { Download, FileText, BarChart3, FileSpreadsheet } from 'lucide-react';

const ExportButtons = ({ analysisId, generatedFiles = [] }) => {
  const downloadFile = (fileType) => {
    const url = `http://localhost:8000/download/${analysisId}/${fileType}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = `${fileType}_${analysisId}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const downloadDirectFile = (filePath) => {
    const link = document.createElement('a');
    link.href = filePath;
    link.download = filePath.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportOptions = [
    {
      type: 'json',
      label: 'JSON Data',
      icon: FileText,
      description: 'Structured clinical trial data',
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      type: 'csv',
      label: 'CSV Export',
      icon: FileSpreadsheet,
      description: 'Spreadsheet format data',
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      type: 'report',
      label: 'Analysis Report',
      icon: FileText,
      description: 'Detailed AI analysis',
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      type: 'summary',
      label: 'Executive Summary',
      icon: FileText,
      description: 'Executive summary report',
      color: 'bg-orange-600 hover:bg-orange-700'
    }
  ];

  return (
    <div className="card">
      <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <Download className="h-6 w-6 mr-2 text-primary-600" />
        Export Results
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {exportOptions.map((option) => {
          const IconComponent = option.icon;
          return (
            <button
              key={option.type}
              onClick={() => downloadFile(option.type)}
              className={`${option.color} text-white p-4 rounded-lg transition-colors duration-200 flex items-start space-x-3 text-left`}
            >
              <IconComponent className="h-6 w-6 mt-0.5 flex-shrink-0" />
              <div>
                <h3 className="font-medium">{option.label}</h3>
                <p className="text-sm opacity-90">{option.description}</p>
              </div>
            </button>
          );
        })}
      </div>

      {/* Direct file downloads */}
      {generatedFiles.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="font-medium text-gray-900 mb-4">Generated Files</h3>
          <div className="space-y-2">
            {generatedFiles.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <BarChart3 className="h-5 w-5 text-gray-500" />
                  <span className="text-sm text-gray-700">
                    {file.split('/').pop()}
                  </span>
                </div>
                <button
                  onClick={() => downloadDirectFile(file)}
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  Download
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ExportButtons;
