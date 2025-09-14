import React from 'react';
import { Brain, Lightbulb, ArrowRight } from 'lucide-react';

const InsightsCard = ({ analysis, recommendations }) => {
  if (!analysis) return null;

  // Extract sections from the analysis text
  const extractSections = (text) => {
    const sections = {
      clinicalAnalysis: '',
      visualizationRecommendations: ''
    };

    // Look for section headers
    const clinicalMatch = text.match(/## Clinical Analysis\s*([\s\S]*?)(?=##|$)/i);
    const vizMatch = text.match(/## Visualization Recommendations\s*([\s\S]*?)(?=##|$)/i);

    if (clinicalMatch) {
      sections.clinicalAnalysis = clinicalMatch[1].trim();
    } else {
      // If no clear sections, use the whole text as clinical analysis
      sections.clinicalAnalysis = text;
    }

    if (vizMatch) {
      let vizText = vizMatch[1].trim();
      // Remove JSON object if it exists at the end
      const jsonMatch = vizText.match(/^([\s\S]*?)(?=\n*```json|$)/);
      if (jsonMatch) {
        sections.visualizationRecommendations = jsonMatch[1].trim();
      } else {
        sections.visualizationRecommendations = vizText;
      }
    }

    return sections;
  };

  const sections = extractSections(analysis);

  return (
    <div className="space-y-6">
      {/* Clinical Analysis */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Brain className="h-6 w-6 mr-2 text-primary-600" />
          AI Clinical Analysis
        </h2>
        <div className="prose prose-sm max-w-none">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {sections.clinicalAnalysis}
            </p>
          </div>
        </div>
      </div>

      {/* Visualization Recommendations */}
      {sections.visualizationRecommendations && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Lightbulb className="h-6 w-6 mr-2 text-yellow-600" />
            Visualization Recommendations
          </h2>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {sections.visualizationRecommendations}
            </p>
          </div>
        </div>
      )}

    </div>
  );
};

export default InsightsCard;
