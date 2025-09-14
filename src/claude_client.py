"""
Claude client for analyzing clinical trial data and generating insights and visualization recommendations.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple
from anthropic import Anthropic


class ClaudeClient:
    """Client for interacting with Claude API for clinical trial analysis."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude client with API key."""
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
    
    def analyze_clinical_data(self, clinical_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Analyze clinical trial data and provide insights plus visualization recommendations.
        
        Args:
            clinical_data: Structured clinical trial data from Cerebras
            
        Returns:
            Tuple of (analysis_text, visualization_recommendations)
        """
        prompt = f"""
        You are a clinical research expert analyzing clinical trial data. Please provide:

        1. **CLINICAL ANALYSIS**: A comprehensive analysis of this clinical trial including:
           - Study design assessment
           - Statistical significance of results
           - Clinical relevance and implications
           - Safety profile evaluation
           - Limitations and potential biases
           - Comparison to standard of care or existing treatments
           - Recommendations for clinical practice

        2. **VISUALIZATION RECOMMENDATIONS**: Suggest specific charts and graphs that would best represent this data. For each visualization, provide:
           - Chart type (bar, line, scatter, box plot, etc.)
           - Data to plot (x-axis, y-axis, categories)
           - Title and labels
           - Purpose/insight the chart reveals

        Clinical Trial Data:
        {json.dumps(clinical_data, indent=2)}

        Please structure your response as follows:
        ## Clinical Analysis
        [Your detailed analysis here]

        ## Visualization Recommendations
        [List of specific chart recommendations with details]

        At the end, provide a JSON block with visualization specifications:
        ```json
        {{
            "visualizations": [
                {{
                    "type": "bar_chart",
                    "title": "Chart Title",
                    "data_source": "field_name_from_data",
                    "x_label": "X-axis label",
                    "y_label": "Y-axis label",
                    "description": "What this chart shows"
                }}
            ]
        }}
        ```
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text
            
            # Extract visualization recommendations JSON
            viz_recommendations = self._extract_visualization_json(content)
            
            return content, viz_recommendations
            
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def _extract_visualization_json(self, content: str) -> Dict[str, Any]:
        """Extract JSON visualization recommendations from Claude's response."""
        try:
            # Look for JSON block in the response
            start_marker = "```json"
            end_marker = "```"
            
            start_idx = content.find(start_marker)
            if start_idx == -1:
                return {"visualizations": []}
            
            start_idx += len(start_marker)
            end_idx = content.find(end_marker, start_idx)
            
            if end_idx == -1:
                return {"visualizations": []}
            
            json_str = content[start_idx:end_idx].strip()
            return json.loads(json_str)
            
        except (json.JSONDecodeError, Exception):
            # Fallback: create default visualizations based on common clinical trial data
            return self._create_default_visualizations()
    
    def _create_default_visualizations(self) -> Dict[str, Any]:
        """Create default visualization recommendations for clinical trials."""
        return {
            "visualizations": [
                {
                    "type": "bar_chart",
                    "title": "Primary Endpoint Results",
                    "data_source": "results_summary",
                    "x_label": "Treatment Groups",
                    "y_label": "Outcome Measure",
                    "description": "Comparison of primary endpoint across treatment groups"
                },
                {
                    "type": "pie_chart",
                    "title": "Adverse Events Distribution",
                    "data_source": "adverse_events",
                    "x_label": "Event Type",
                    "y_label": "Frequency",
                    "description": "Distribution of reported adverse events"
                },
                {
                    "type": "line_chart",
                    "title": "Treatment Response Over Time",
                    "data_source": "results_summary",
                    "x_label": "Time Point",
                    "y_label": "Response Rate",
                    "description": "Treatment response progression throughout the study"
                }
            ]
        }
    
    def generate_executive_summary(self, clinical_data: Dict[str, Any], analysis: str) -> str:
        """Generate a concise executive summary of the clinical trial."""
        prompt = f"""
        Create a concise executive summary (2-3 paragraphs) of this clinical trial for healthcare professionals. 
        Focus on the most important findings, clinical implications, and actionable insights.

        Clinical Data:
        {json.dumps(clinical_data, indent=2)}

        Detailed Analysis:
        {analysis}

        Executive Summary:
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating executive summary: {str(e)}"
    
    def suggest_follow_up_studies(self, clinical_data: Dict[str, Any]) -> str:
        """Suggest potential follow-up studies based on the current trial results."""
        prompt = f"""
        Based on this clinical trial data, suggest 3-5 potential follow-up studies that would be valuable 
        for advancing this research. Consider:
        - Limitations of the current study
        - Unanswered questions
        - Different patient populations
        - Longer-term outcomes
        - Combination therapies

        Clinical Trial Data:
        {json.dumps(clinical_data, indent=2)}

        Follow-up Study Recommendations:
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.4,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating follow-up study suggestions: {str(e)}"


# Example usage and testing function
def test_claude_client():
    """Test function for the Claude client."""
    try:
        # Debug: Check what's in the environment
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        raw_key = os.getenv("CLAUDE_API_KEY")
        print(f"🔍 Raw API key from env: {raw_key[:20] if raw_key else 'None'}...")
        print(f"🔍 API key length: {len(raw_key) if raw_key else 0}")
        print(f"🔍 API key starts with sk-ant: {raw_key.startswith('sk-ant') if raw_key else False}")
        
        client = ClaudeClient()
        print("✅ Claude client initialized successfully")
        
        # Test API key format (don't make actual API call)
        if client.api_key and client.api_key.startswith('sk-ant-api03-'):
            print("✅ Claude API key format looks correct")
            return True
        else:
            print(f"⚠️  Claude API key format may be incorrect")
            print(f"   Expected: sk-ant-api03-...")
            print(f"   Got: {client.api_key[:20] if client.api_key else 'None'}...")
            return False
        
    except Exception as e:
        print(f"❌ Error testing Claude client: {str(e)}")
        return False


if __name__ == "__main__":
    test_claude_client()
