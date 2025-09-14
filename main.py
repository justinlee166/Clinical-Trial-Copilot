"""
Clinical Trial Copilot - Main Pipeline
Orchestrates the complete analysis workflow from PDF input to insights and visualizations.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import our custom modules
from src.cerebras_client import CerebrasClient
from src.claude_client import ClaudeClient
from src.analysis import ClinicalTrialAnalyzer


class ClinicalTrialPipeline:
    """Main pipeline orchestrator for clinical trial analysis."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize the pipeline with required clients."""
        self.output_dir = output_dir
        self._ensure_output_dir()
        
        # Load environment variables
        load_dotenv()
        
        # Validate API keys
        self._validate_environment()
        
        # Initialize clients
        print("🔧 Initializing clients...")
        try:
            self.cerebras_client = CerebrasClient()
            print("✅ Cerebras client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Cerebras client: {str(e)}")
            sys.exit(1)
        
        try:
            self.claude_client = ClaudeClient()
            print("✅ Claude client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Claude client: {str(e)}")
            sys.exit(1)
        
        try:
            self.analyzer = ClinicalTrialAnalyzer(output_dir)
            print("✅ Clinical analyzer initialized")
        except Exception as e:
            print(f"❌ Failed to initialize analyzer: {str(e)}")
            sys.exit(1)
        
        print("🚀 Clinical Trial Copilot ready!")
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created output directory: {self.output_dir}")
    
    def _validate_environment(self):
        """Validate that required environment variables are set."""
        required_keys = ["CLAUDE_API_KEY", "CEREBRAS_API_KEY"]
        missing_keys = []
        
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            print("❌ Missing required environment variables:")
            for key in missing_keys:
                print(f"   - {key}")
            print("\n💡 Please create a .env file with your API keys:")
            print("   CLAUDE_API_KEY=your_anthropic_api_key_here")
            print("   CEREBRAS_API_KEY=your_cerebras_api_key_here")
            sys.exit(1)
        
        print("✅ Environment variables validated")
    
    def process_clinical_trial(self, pdf_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: PDF → Cerebras analysis → Claude insights → Visualizations
        
        Args:
            pdf_path: Path to the clinical trial PDF file
            
        Returns:
            Dict containing all analysis results and file paths
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"\n🎯 Starting analysis of: {pdf_path}")
        print("=" * 60)
        
        results = {
            "input_file": pdf_path,
            "timestamp": datetime.now().isoformat(),
            "clinical_data": {},
            "claude_analysis": "",
            "visualization_recommendations": {},
            "generated_files": []
        }
        
        # Step 1: Extract structured data with Cerebras
        print("\n📋 STEP 1: Extracting clinical data with Cerebras...")
        try:
            clinical_data = self.cerebras_client.parse_clinical_trial_pdf(pdf_path)
            results["clinical_data"] = clinical_data
            print("✅ Clinical data extraction completed")
            
            # Save raw clinical data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"clinical_data_{timestamp}.json"
            json_filepath = os.path.join(self.output_dir, json_filename)
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(clinical_data, f, indent=2, ensure_ascii=False)
            
            results["generated_files"].append(json_filepath)
            print(f"💾 Raw data saved to: {json_filepath}")
            
        except Exception as e:
            print(f"❌ Error in Cerebras analysis: {str(e)}")
            return results
        
        # Step 2: Generate insights with Claude
        print("\n🧠 STEP 2: Generating insights with Claude...")
        try:
            analysis_text, viz_recommendations = self.claude_client.analyze_clinical_data(clinical_data)
            results["claude_analysis"] = analysis_text
            results["visualization_recommendations"] = viz_recommendations
            print("✅ Claude analysis completed")
            
            # Save analysis report
            report_file = self.analyzer.save_analysis_report(analysis_text)
            results["generated_files"].append(report_file)
            
            # Generate executive summary
            print("📝 Generating executive summary...")
            exec_summary = self.claude_client.generate_executive_summary(clinical_data, analysis_text)
            
            summary_filename = f"executive_summary_{timestamp}.txt"
            summary_filepath = os.path.join(self.output_dir, summary_filename)
            
            with open(summary_filepath, 'w', encoding='utf-8') as f:
                f.write("EXECUTIVE SUMMARY\n")
                f.write("=" * 30 + "\n\n")
                f.write(exec_summary)
            
            results["generated_files"].append(summary_filepath)
            print(f"📋 Executive summary saved to: {summary_filepath}")
            
            # Generate follow-up study suggestions
            print("🔬 Generating follow-up study suggestions...")
            follow_up = self.claude_client.suggest_follow_up_studies(clinical_data)
            
            followup_filename = f"follow_up_studies_{timestamp}.txt"
            followup_filepath = os.path.join(self.output_dir, followup_filename)
            
            with open(followup_filepath, 'w', encoding='utf-8') as f:
                f.write("FOLLOW-UP STUDY RECOMMENDATIONS\n")
                f.write("=" * 40 + "\n\n")
                f.write(follow_up)
            
            results["generated_files"].append(followup_filepath)
            print(f"🔬 Follow-up suggestions saved to: {followup_filepath}")
            
        except Exception as e:
            print(f"❌ Error in Claude analysis: {str(e)}")
            # Continue with visualization even if Claude analysis fails
        
        # Step 3: Generate visualizations and exports
        print("\n📊 STEP 3: Generating visualizations and exports...")
        try:
            # Save clinical data as CSV
            csv_file = self.analyzer.save_clinical_data_csv(clinical_data)
            results["generated_files"].append(csv_file)
            
            # Generate all visualizations
            chart_files = self.analyzer.generate_all_visualizations(
                clinical_data, viz_recommendations
            )
            results["generated_files"].extend(chart_files)
            
            # Create summary dashboard
            dashboard_file = self.analyzer.create_summary_dashboard(clinical_data)
            results["generated_files"].append(dashboard_file)
            
            print("✅ Visualization generation completed")
            
        except Exception as e:
            print(f"❌ Error in visualization generation: {str(e)}")
        
        # Step 4: Create final summary
        print("\n📋 STEP 4: Creating final summary...")
        try:
            summary_data = {
                "analysis_summary": {
                    "pdf_file": pdf_path,
                    "processing_timestamp": results["timestamp"],
                    "study_title": clinical_data.get("title", "Unknown Study"),
                    "study_type": clinical_data.get("study_type", "Unknown"),
                    "participants": clinical_data.get("participants", "Unknown"),
                    "total_files_generated": len(results["generated_files"])
                },
                "generated_files": results["generated_files"],
                "clinical_data_summary": {
                    key: str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    for key, value in clinical_data.items()
                }
            }
            
            summary_json_filename = f"analysis_summary_{timestamp}.json"
            summary_json_filepath = os.path.join(self.output_dir, summary_json_filename)
            
            with open(summary_json_filepath, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            results["generated_files"].append(summary_json_filepath)
            print(f"📋 Final summary saved to: {summary_json_filepath}")
            
        except Exception as e:
            print(f"⚠️ Error creating final summary: {str(e)}")
        
        return results
    
    def print_results_summary(self, results: Dict[str, Any]):
        """Print a summary of the analysis results."""
        print("\n" + "="*60)
        print("🎉 ANALYSIS COMPLETE!")
        print("="*60)
        
        clinical_data = results.get("clinical_data", {})
        if clinical_data:
            print(f"\n📊 Study Title: {clinical_data.get('title', 'Unknown')}")
            print(f"👥 Participants: {clinical_data.get('participants', 'Unknown')}")
            print(f"🔬 Study Type: {clinical_data.get('study_type', 'Unknown')}")
        
        files_generated = results.get("generated_files", [])
        print(f"\n📁 Generated {len(files_generated)} output files:")
        for i, filepath in enumerate(files_generated, 1):
            filename = os.path.basename(filepath)
            print(f"   {i:2d}. {filename}")
        
        print(f"\n💾 All files saved to: {os.path.abspath(self.output_dir)}")
        print("\n✨ Clinical Trial Copilot analysis complete!")


def main():
    """Main entry point for the Clinical Trial Copilot."""
    parser = argparse.ArgumentParser(
        description="Clinical Trial Copilot - Analyze clinical trial PDFs with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py data/trial_report.pdf
  python main.py data/trial_report.pdf --output custom_output/
        """
    )
    
    parser.add_argument(
        "pdf_path",
        help="Path to the clinical trial PDF file to analyze"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="outputs",
        help="Output directory for generated files (default: outputs)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.pdf_path):
        print(f"❌ Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    if not args.pdf_path.lower().endswith('.pdf'):
        print(f"❌ Error: File must be a PDF: {args.pdf_path}")
        sys.exit(1)
    
    try:
        # Initialize pipeline
        pipeline = ClinicalTrialPipeline(output_dir=args.output)
        
        # Process the clinical trial
        results = pipeline.process_clinical_trial(args.pdf_path)
        
        # Print summary
        pipeline.print_results_summary(results)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
