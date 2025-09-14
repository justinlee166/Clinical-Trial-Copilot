import React from 'react';
import { FileText, Users, Target, TrendingUp, Shield, BarChart3 } from 'lucide-react';

const ResultsCard = ({ clinicalData }) => {
  if (!clinicalData) return null;

  const formatValue = (value) => {
    if (!value || value === 'Unable to extract') return 'Not available';
    
    // Try to parse string that looks like an object
    let parsedValue = value;
    if (typeof value === 'string' && value.startsWith('{') && value.includes('}')) {
      try {
        // Extract just the dictionary part (from { to the matching })
        let dictString = '';
        let braceCount = 0;
        let inString = false;
        let stringChar = '';
        
        for (let i = 0; i < value.length; i++) {
          const char = value[i];
          
          if (!inString && (char === '{' || char === '}')) {
            braceCount += char === '{' ? 1 : -1;
            dictString += char;
            if (braceCount === 0) break; // Found the end of the dictionary
          } else if (!inString && (char === "'" || char === '"')) {
            inString = true;
            stringChar = char;
            dictString += char;
          } else if (inString && char === stringChar) {
            inString = false;
            dictString += char;
          } else {
            dictString += char;
          }
        }
        
        // Convert Python dictionary format to JSON format
        const jsonString = dictString.replace(/'/g, '"');
        parsedValue = JSON.parse(jsonString);
      } catch (e) {
        // If parsing fails, use original value
        parsedValue = value;
      }
    }
    
    // If it's an object, format it nicely
    if (typeof parsedValue === 'object' && parsedValue !== null) {
      if (parsedValue.number && parsedValue.demographics) {
        return `${parsedValue.number} ${parsedValue.demographics}`;
      }
      if (parsedValue.primary && parsedValue.secondary) {
        return `Primary: ${parsedValue.primary}\nSecondary: ${parsedValue.secondary}`;
      }
      if (parsedValue.methods && parsedValue.significance) {
        return `Methods: ${parsedValue.methods}\nSignificance: ${parsedValue.significance}`;
      }
      if (parsedValue.key_findings && parsedValue.results) {
        return `Key Findings: ${parsedValue.key_findings}\nResults: ${parsedValue.results}`;
      }
      // Fallback to JSON string for other objects
      return JSON.stringify(parsedValue, null, 2);
    }
    
    return parsedValue;
  };

  const dataItems = [
    {
      icon: FileText,
      label: 'Study Title',
      value: clinicalData.title,
      color: 'text-blue-600'
    },
    {
      icon: Users,
      label: 'Participants',
      value: clinicalData.participants,
      color: 'text-green-600'
    },
    {
      icon: Target,
      label: 'Study Type',
      value: clinicalData.study_type,
      color: 'text-purple-600'
    },
    {
      icon: TrendingUp,
      label: 'Primary Endpoints',
      value: clinicalData.endpoints,
      color: 'text-orange-600'
    },
    {
      icon: Shield,
      label: 'Adverse Events',
      value: clinicalData.adverse_events,
      color: 'text-red-600'
    },
    {
      icon: BarChart3,
      label: 'Statistical Analysis',
      value: clinicalData.statistical_analysis,
      color: 'text-indigo-600'
    }
  ];

  return (
    <div className="card">
      <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <FileText className="h-6 w-6 mr-2 text-primary-600" />
        Clinical Trial Summary
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {dataItems.map((item, index) => {
          const IconComponent = item.icon;
          return (
            <div key={index} className="space-y-2">
              <div className="flex items-center space-x-2">
                <IconComponent className={`h-5 w-5 ${item.color}`} />
                <h3 className="font-medium text-gray-900">{item.label}</h3>
              </div>
              <p className="text-gray-700 text-sm leading-relaxed pl-7">
                {formatValue(item.value)}
              </p>
            </div>
          );
        })}
      </div>
      
      {clinicalData.results_summary && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="font-medium text-gray-900 mb-3 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
            Key Results
          </h3>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-gray-800 text-sm leading-relaxed">
              {formatValue(clinicalData.results_summary)}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsCard;
