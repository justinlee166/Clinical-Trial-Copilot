# Clinical Trial Copilot - Setup Instructions

## 🚀 Quick Setup Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy the template
cp env_template.txt .env

# Edit .env file with your actual API keys:
# CLAUDE_API_KEY=your_anthropic_api_key_here
# CEREBRAS_API_KEY=your_cerebras_api_key_here
```

### 3. Test the Installation
```bash
# Test all components
python run_example.py

# Or test individual components
python src/cerebras_client.py
python src/claude_client.py
python src/analysis.py
```

### 4. Run Your First Analysis
```bash
# Place a clinical trial PDF in the data/ directory
# Then run:
python main.py data/your_clinical_trial.pdf
```

## 📋 Required API Keys

### Claude API Key (Anthropic)
1. Visit: https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your .env file

### Cerebras API Key
1. Visit: https://cloud.cerebras.ai/
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your .env file

## 🎯 Usage Examples

### CLI Usage
```bash
# Basic analysis
python main.py data/trial.pdf

# Custom output directory
python main.py data/trial.pdf --output my_results/

# Verbose logging
python main.py data/trial.pdf --verbose
```

### API Usage
```bash
# Start the API server
python src/api.py

# Upload and analyze (in another terminal)
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@data/trial.pdf"

# Check status
curl "http://localhost:8000/status/{analysis_id}"

# Download results
curl "http://localhost:8000/download/{analysis_id}/dashboard"
```

## 📁 Expected Outputs

After running an analysis, you'll find these files in the `outputs/` directory:

### Data Files
- `clinical_data_*.json` - Structured clinical trial data
- `clinical_trial_data_*.csv` - Data in spreadsheet format
- `analysis_summary_*.json` - Complete analysis metadata

### Reports
- `clinical_analysis_report_*.txt` - Detailed AI analysis
- `executive_summary_*.txt` - Executive summary
- `follow_up_studies_*.txt` - Research recommendations

### Visualizations
- `efficacy_chart_*.png` - Treatment results chart
- `safety_profile_*.png` - Adverse events distribution
- `study_timeline_*.png` - Study methodology timeline
- `clinical_dashboard_*.png` - Comprehensive overview
- Custom charts based on AI recommendations

## 🔧 Troubleshooting

### Common Issues

**"API key not found" error:**
- Ensure your .env file exists in the project root
- Check that API keys are correctly formatted (no extra spaces)
- Verify the .env file is not named .env.txt

**"PDF file not found" error:**
- Check the file path is correct
- Ensure the file has a .pdf extension
- Verify the file is not corrupted

**Import errors:**
- Run `pip install -r requirements.txt` to install dependencies
- Ensure you're in the correct directory
- Check Python version (requires Python 3.7+)

**API connection errors:**
- Verify your internet connection
- Check that API keys are valid and active
- Ensure you have API credits/quota available

### Getting Help

1. Check the console output for specific error messages
2. Use the `--verbose` flag for detailed logging
3. Test individual components with `python run_example.py`
4. Verify your API keys are working with simple test calls

## 🏗️ Architecture Overview

```
Clinical Trial Copilot Pipeline:

PDF Input → Cerebras (Data Extraction) → Claude (Analysis) → Visualizations
    ↓              ↓                        ↓                ↓
Text Extract   JSON Structure         Insights +         Charts + Reports
               + Metadata           Recommendations      + CSV Exports
```

### Key Components:
- **Cerebras Client**: PDF parsing and structured data extraction
- **Claude Client**: Clinical analysis and visualization recommendations
- **Analysis Engine**: Chart generation and data export
- **Pipeline Orchestrator**: Workflow coordination and error handling
- **FastAPI Server**: Optional REST API interface

## 📊 Data Processing Flow

1. **PDF Ingestion**: Extract text from clinical trial PDF
2. **Text Chunking**: Split large documents for optimal API processing
3. **Structured Extraction**: Use Cerebras to extract clinical trial data
4. **Data Validation**: Ensure extracted data completeness
5. **Clinical Analysis**: Generate insights with Claude AI
6. **Visualization Planning**: Get chart recommendations from Claude
7. **Chart Generation**: Create multiple visualization types
8. **Report Generation**: Produce executive summaries and recommendations
9. **File Export**: Save all outputs in multiple formats

This robust pipeline ensures comprehensive analysis of clinical trial data with minimal user intervention.
