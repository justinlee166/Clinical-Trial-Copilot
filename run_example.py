"""
Example runner for Clinical Trial Copilot
Demonstrates how to use the system programmatically.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append('src')

from main import ClinicalTrialPipeline


def run_example():
    """Run an example analysis if a PDF file is available."""
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are set
    if not os.getenv("CLAUDE_API_KEY") or not os.getenv("CEREBRAS_API_KEY"):
        print("❌ Please set up your API keys in the .env file first!")
        print("   Copy env_template.txt to .env and add your keys.")
        return False
    
    # Look for example PDF files
    data_dir = "data"
    example_files = []
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.lower().endswith('.pdf'):
                example_files.append(os.path.join(data_dir, file))
    
    if not example_files:
        print("📄 No PDF files found in the data/ directory.")
        print("   Please add a clinical trial PDF file to data/ and try again.")
        print("\n💡 You can also run the analysis directly:")
        print("   python main.py path/to/your/clinical_trial.pdf")
        return False
    
    # Use the first PDF file found
    pdf_file = example_files[0]
    print(f"📄 Found example file: {pdf_file}")
    
    try:
        # Initialize the pipeline
        print("🔧 Initializing Clinical Trial Copilot...")
        pipeline = ClinicalTrialPipeline(output_dir="example_outputs")
        
        # Run the analysis
        print(f"🚀 Starting analysis of: {pdf_file}")
        results = pipeline.process_clinical_trial(pdf_file)
        
        # Print summary
        pipeline.print_results_summary(results)
        
        print("\n✨ Example analysis completed successfully!")
        print("📁 Check the 'example_outputs' directory for all generated files.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running example: {str(e)}")
        return False


def test_individual_components():
    """Test individual components without requiring a PDF."""
    print("🧪 Testing individual components...")
    
    # Load environment variables first
    load_dotenv()
    
    # Test Cerebras client
    try:
        from cerebras_client import test_cerebras_client
        cerebras_ok = test_cerebras_client()
    except Exception as e:
        print(f"❌ Cerebras client test failed: {str(e)}")
        cerebras_ok = False
    
    # Test Claude client
    try:
        from claude_client import test_claude_client
        claude_ok = test_claude_client()
    except Exception as e:
        print(f"❌ Claude client test failed: {str(e)}")
        claude_ok = False
    
    # Test analyzer
    try:
        from analysis import test_analyzer
        analyzer_ok = test_analyzer()
    except Exception as e:
        print(f"❌ Analyzer test failed: {str(e)}")
        analyzer_ok = False
    
    # Summary
    total_tests = 3
    passed_tests = sum([cerebras_ok, claude_ok, analyzer_ok])
    
    print(f"\n📊 Component Tests: {passed_tests}/{total_tests} passed")
    
    if passed_tests == total_tests:
        print("✅ All components are working correctly!")
        return True
    else:
        print("⚠️ Some components have issues. Check your API keys and dependencies.")
        return False


if __name__ == "__main__":
    print("🏥 Clinical Trial Copilot - Example Runner")
    print("=" * 50)
    
    # First test components
    components_ok = test_individual_components()
    
    if components_ok:
        print("\n" + "=" * 50)
        # Then try to run a full example
        run_example()
    else:
        print("\n💡 Fix the component issues above before running a full analysis.")
        print("   Make sure your .env file is set up correctly with valid API keys.")
