import React, { useState } from 'react';
import { BarChart3, Download, Eye, EyeOff } from 'lucide-react';

const ChartViewer = ({ charts = [] }) => {
  const [selectedChart, setSelectedChart] = useState(null);
  const [showAll, setShowAll] = useState(false);

  // Debug: Log the charts data
  console.log('ChartViewer received charts:', charts);
  
  // Debug: Log the generated URLs
  if (charts && charts.length > 0) {
    charts.forEach((chart, index) => {
      const filename = chart.replace(/\\/g, '/').split('/').pop();
      const url = `http://localhost:8000/image/${filename}`;
      console.log(`Chart ${index}: ${chart} -> ${url}`);
    });
  }

  if (!charts || charts.length === 0) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No charts available</p>
        </div>
      </div>
    );
  }

  const displayCharts = showAll ? charts : charts.slice(0, 3);

  const getChartType = (filename) => {
    if (filename.includes('efficacy')) return 'Efficacy Results';
    if (filename.includes('safety')) return 'Safety Profile';
    if (filename.includes('timeline')) return 'Study Timeline';
    if (filename.includes('dashboard')) return 'Clinical Dashboard';
    return 'Clinical Chart';
  };

  const downloadChart = (chartPath) => {
    const link = document.createElement('a');
    link.href = chartPath;
    link.download = chartPath.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center">
          <BarChart3 className="h-6 w-6 mr-2 text-primary-600" />
          Generated Visualizations
        </h2>
        {charts.length > 3 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="btn-secondary flex items-center space-x-2"
          >
            {showAll ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            <span>{showAll ? 'Show Less' : `Show All (${charts.length})`}</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {displayCharts.map((chart, index) => (
          <div key={index} className="space-y-3">
            <div className="relative group">
              <img
                src={`http://localhost:8000/outputs/${chart.replace(/\\/g, '/').split('/').pop()}`}
                alt={getChartType(chart)}
                className="w-full h-48 object-cover rounded-lg border border-gray-200 cursor-pointer hover:shadow-lg transition-shadow duration-200"
                onClick={() => setSelectedChart(chart)}
                onError={(e) => {
                  console.log('Image failed to load:', e.target.src);
                  console.log('Original chart path:', chart);
                }}
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 rounded-lg flex items-center justify-center">
                <button
                  onClick={() => setSelectedChart(chart)}
                  className="opacity-0 group-hover:opacity-100 bg-white bg-opacity-90 hover:bg-opacity-100 rounded-full p-2 transition-all duration-200"
                >
                  <Eye className="h-5 w-5 text-gray-700" />
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <h3 className="font-medium text-gray-900 text-sm">
                {getChartType(chart)}
              </h3>
              <button
                onClick={() => downloadChart(chart)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                title="Download chart"
              >
                <Download className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal for full-size chart view */}
      {selectedChart && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl max-h-full overflow-auto">
            <div className="p-4 border-b border-gray-200 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                {getChartType(selectedChart)}
              </h3>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => downloadChart(selectedChart)}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <Download className="h-4 w-4" />
                  <span>Download</span>
                </button>
                <button
                  onClick={() => setSelectedChart(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>
            </div>
            <div className="p-4">
              <img
                src={`http://localhost:8000/outputs/${selectedChart.replace(/\\/g, '/').split('/').pop()}`}
                alt={getChartType(selectedChart)}
                className="w-full h-auto rounded-lg"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChartViewer;
