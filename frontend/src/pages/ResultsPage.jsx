import React from 'react';
import ResultsCard from '../components/ResultsCard';
import InsightsCard from '../components/InsightsCard';
import ChartViewer from '../components/ChartViewer';
import ExportButtons from '../components/ExportButtons';
import { ArrowLeft, CheckCircle } from 'lucide-react';

const ResultsPage = ({ result, onBackToUpload }) => {
  if (!result) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No results available</p>
      </div>
    );
  }

  const { 
    clinical_data, 
    claude_analysis, 
    visualization_recommendations,
    generated_files = [],
    analysis_id 
  } = result;

  // Extract chart files from generated files
  const chartFiles = generated_files.filter(file => 
    file.includes('.png') && (
      file.includes('efficacy') || 
      file.includes('safety') || 
      file.includes('timeline') || 
      file.includes('dashboard')
    )
  );

  // Helper function to extract participant count from text
  const extractParticipantCount = (participantsText) => {
    if (!participantsText || participantsText === 'Unable to extract participants') {
      return 'N/A';
    }
    
    // Try to parse string that looks like an object
    let parsedValue = participantsText;
    if (typeof participantsText === 'string' && participantsText.startsWith('{') && participantsText.includes('}')) {
      try {
        // Convert Python dictionary format to JSON format
        const jsonString = participantsText.replace(/'/g, '"');
        parsedValue = JSON.parse(jsonString);
      } catch (e) {
        parsedValue = participantsText;
      }
    }
    
    // If it's an object with number property
    if (typeof parsedValue === 'object' && parsedValue.number) {
      return parsedValue.number;
    }
    
    // Look for numbers in the text (e.g., "1,234 participants", "500 patients", etc.)
    const numberMatch = participantsText.match(/(\d{1,3}(?:,\d{3})*|\d+)/);
    return numberMatch ? numberMatch[1] : 'N/A';
  };

  // Helper function to extract study phase from text
  const extractStudyPhase = (studyTypeText) => {
    if (!studyTypeText || studyTypeText === 'Unable to extract study type') {
      return 'N/A';
    }
    
    // Look for phase indicators (Phase I, Phase II, Phase III, Phase IV)
    const phaseMatch = studyTypeText.match(/Phase\s+[IVX]+/i);
    if (phaseMatch) {
      return phaseMatch[0];
    }
    
    // Look for other study type indicators
    const typeMatch = studyTypeText.match(/(Randomized|Double-blind|Placebo-controlled|Open-label|Pilot|Feasibility)/i);
    if (typeMatch) {
      return typeMatch[1];
    }
    
    // Return first word if it looks like a study type
    const firstWord = studyTypeText.split(' ')[0];
    return firstWord.length > 2 ? firstWord : 'N/A';
  };

  const participantCount = extractParticipantCount(clinical_data?.participants);
  const studyPhase = extractStudyPhase(clinical_data?.study_type);

  // Debug: Log the clinical data to console (remove this in production)
  console.log('Clinical Data:', clinical_data);
  console.log('Extracted Participant Count:', participantCount);
  console.log('Extracted Study Phase:', studyPhase);

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-3">
          <CheckCircle className="h-8 w-8 text-green-600" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Analysis Complete
            </h1>
            <p className="text-gray-600">
              Clinical trial analysis results and insights
            </p>
          </div>
        </div>
        <button
          onClick={onBackToUpload}
          className="btn-secondary flex items-center space-x-2"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Analyze Another PDF</span>
        </button>
      </div>

      {/* Results Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Clinical Data */}
        <div className="lg:col-span-2 space-y-8">
          <ResultsCard clinicalData={clinical_data} />
          <InsightsCard 
            analysis={claude_analysis}
            recommendations={visualization_recommendations}
          />
        </div>

        {/* Right Column - Charts and Export */}
        <div className="space-y-8">
          <ChartViewer charts={chartFiles} />
          <ExportButtons 
            analysisId={analysis_id}
            generatedFiles={generated_files}
          />
        </div>
      </div>


      {/* Summary Stats */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600 mb-1">
            {participantCount}
          </div>
          <div className="text-sm text-gray-600">Participants</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600 mb-1">
            {chartFiles.length}
          </div>
          <div className="text-sm text-gray-600">Charts Generated</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-purple-600 mb-1">
            {generated_files.length}
          </div>
          <div className="text-sm text-gray-600">Files Created</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-orange-600 mb-1">
            {studyPhase}
          </div>
          <div className="text-sm text-gray-600">Study Phase</div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
