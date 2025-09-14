# Clinical Trial Copilot 🏥🤖

A robust AI-powered backend for analyzing clinical trial PDFs using Cerebras for data extraction and Claude for insights generation.

## Features

- **PDF Processing**: Extract structured data from clinical trial PDFs using Cerebras AI
- **Intelligent Analysis**: Generate insights and recommendations using Claude AI  
- **Rich Visualizations**: Create charts, graphs, and dashboards using matplotlib
- **Multiple Export Formats**: JSON, CSV, PNG charts, and text reports
- **CLI Interface**: Simple command-line interface for batch processing
- **REST API**: Optional FastAPI endpoints for web integration
- **Local Processing**: Runs entirely locally with no external database required

## Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to project
cd Clinical_Data_Copilot

# Install dependencies
pip install -r requirements.txt

# Setup API keys
cp env_template.txt .env
# Edit .env with your actual API keys
```

### 2. Get API Keys

- **Claude API Key**: Get from [Anthropic Console](https://console.anthropic.com/)
- **Cerebras API Key**: Get from [Cerebras Cloud](https://cloud.cerebras.ai/)

### 3. Run Analysis

```bash
# Analyze a clinical trial PDF
python main.py data/your_trial.pdf

# Use custom output directory
python main.py data/your_trial.pdf --output my_results/

# Enable verbose logging
python main.py data/your_trial.pdf --verbose
```

### 4. Start API Server (Optional)

```bash
# Start FastAPI server
python src/api.py

# API docs available at: http://localhost:8000/docs
```

## Project Structure

```
Clinical_Data_Copilot/
├── main.py                 # Main CLI pipeline orchestrator
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── env_template.txt       # Environment variables template
├── README.md              # This file
├── data/                  # Input PDF files (create this directory)
├── outputs/               # Generated analysis files
└── src/                   # Core modules
    ├── cerebras_client.py # PDF parsing with Cerebras
    ├── claude_client.py   # Analysis with Claude
    ├── analysis.py        # Visualization generation
    └── api.py            # FastAPI endpoints (optional)
```

## Output Files

The system generates comprehensive analysis outputs:

### Data Files
- `clinical_data_YYYYMMDD_HHMMSS.json` - Structured trial data
- `clinical_trial_data_YYYYMMDD_HHMMSS.csv` - Data in CSV format
- `analysis_summary_YYYYMMDD_HHMMSS.json` - Complete analysis summary

### Reports
- `clinical_analysis_report_YYYYMMDD_HHMMSS.txt` - Detailed Claude analysis
- `executive_summary_YYYYMMDD_HHMMSS.txt` - Executive summary
- `follow_up_studies_YYYYMMDD_HHMMSS.txt` - Research recommendations

### Visualizations
- `efficacy_chart_YYYYMMDD_HHMMSS.png` - Treatment efficacy results
- `safety_profile_YYYYMMDD_HHMMSS.png` - Adverse events analysis
- `study_timeline_YYYYMMDD_HHMMSS.png` - Study methodology timeline
- `clinical_dashboard_YYYYMMDD_HHMMSS.png` - Comprehensive dashboard
- Custom charts based on Claude's recommendations

## API Usage

### Start the Server
```bash
python src/api.py
```

### Analyze a PDF
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@data/trial.pdf"
```

### Check Analysis Status
```bash
curl "http://localhost:8000/status/{analysis_id}"
```

### Download Results
```bash
curl "http://localhost:8000/download/{analysis_id}/json"
curl "http://localhost:8000/download/{analysis_id}/dashboard"
```

## Key Components

### 🧠 Cerebras Client (`cerebras_client.py`)
- Extracts text from PDF files using pypdf
- Chunks text for optimal API processing
- Sends data to Cerebras for structured extraction
- Returns JSON with: title, participants, study type, endpoints, results, methodology, adverse events, statistical analysis

### 🤖 Claude Client (`claude_client.py`)
- Analyzes clinical data for insights and significance
- Generates visualization recommendations
- Creates executive summaries
- Suggests follow-up research studies

### 📊 Analysis Engine (`analysis.py`)
- Creates multiple chart types (bar, pie, line, timeline)
- Generates comprehensive dashboards
- Exports data to CSV format
- Saves all visualizations as high-quality PNG files

### 🚀 Pipeline Orchestrator (`main.py`)
- Coordinates the complete analysis workflow
- Handles CLI arguments and file validation
- Manages error handling and progress reporting
- Generates final summary reports

## Environment Variables

Required in your `.env` file:

```env
CLAUDE_API_KEY=your_anthropic_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

## Dependencies

- `pypdf==4.0.1` - PDF text extraction
- `requests==2.31.0` - HTTP requests for Cerebras API
- `anthropic==0.25.0` - Claude AI integration
- `pandas==2.1.4` - Data manipulation and CSV export
- `matplotlib==3.8.2` - Visualization generation
- `python-dotenv==1.0.0` - Environment variable management
- `fastapi==0.104.1` - REST API framework (optional)
- `uvicorn==0.24.0` - ASGI server (optional)

## Error Handling

The system includes comprehensive error handling:

- **API Key Validation**: Checks for required environment variables on startup
- **File Validation**: Ensures input files exist and are valid PDFs
- **Graceful Degradation**: Continues processing even if some steps fail
- **Detailed Logging**: Provides clear progress updates and error messages
- **Cleanup**: Automatically removes temporary files

## Security

- API keys stored in `.env` file (git-ignored)
- No hardcoded credentials in source code
- Local processing - no data sent to external databases
- Temporary files automatically cleaned up

## Limitations

- Requires valid Cerebras and Claude API keys
- PDF text extraction quality depends on PDF format
- Large files may take several minutes to process
- Visualization quality depends on data structure in PDFs

## Contributing

This is a backend-focused implementation. Future enhancements could include:

- Enhanced PDF parsing for complex layouts
- Additional visualization types
- Database integration for result storage
- Web frontend interface
- Batch processing capabilities
- Integration with clinical trial databases

## License

This project is designed for educational and research purposes. Please ensure compliance with API terms of service for Cerebras and Anthropic.
