"""
FastAPI endpoints for Clinical Trial Copilot
Optional API interface for the clinical trial analysis pipeline.
"""

import os
import sys
import json
import tempfile
from typing import Dict, Any, List
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our pipeline
from main import ClinicalTrialPipeline


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Clinical Trial Copilot API",
    description="AI-powered clinical trial analysis API using Cerebras and Claude",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


# Global pipeline instance
pipeline = None

# Pydantic models for API responses
class AnalysisStatus(BaseModel):
    """Model for analysis status responses."""
    status: str
    message: str
    timestamp: str
    progress: float = 0.0


class AnalysisResult(BaseModel):
    """Model for complete analysis results."""
    input_file: str
    timestamp: str
    clinical_data: Dict[str, Any]
    claude_analysis: str
    visualization_recommendations: Dict[str, Any]
    generated_files: List[str]
    status: str = "completed"


class HealthCheck(BaseModel):
    """Model for health check responses."""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]


# Global storage for analysis results (in production, use a database)
analysis_results: Dict[str, Dict[str, Any]] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize the pipeline on startup."""
    global pipeline
    try:
        pipeline = ClinicalTrialPipeline()
        print("✅ FastAPI: Clinical Trial Copilot pipeline initialized")
    except Exception as e:
        print(f"❌ FastAPI: Failed to initialize pipeline: {str(e)}")
        pipeline = None


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with API information."""
    return HealthCheck(
        status="healthy" if pipeline else "unhealthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services={
            "cerebras": "available" if pipeline and pipeline.cerebras_client else "unavailable",
            "claude": "available" if pipeline and pipeline.claude_client else "unavailable",
            "analyzer": "available" if pipeline and pipeline.analyzer else "unavailable"
        }
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return await root()


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_clinical_trial(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Analyze a clinical trial PDF file.
    
    This endpoint accepts a PDF file and returns analysis results.
    The analysis runs in the background for large files.
    """
    if not pipeline:
        raise HTTPException(
            status_code=503, 
            detail="Clinical Trial Copilot pipeline not available. Check service health."
        )
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="File must be a PDF document"
        )
    
    # Generate unique analysis ID
    analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(file.filename) % 10000}"
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Initialize analysis status
        analysis_results[analysis_id] = {
            "status": "processing",
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "progress": 0.0,
            "message": "Analysis started"
        }
        
        # For small files, process synchronously
        if len(content) < 10 * 1024 * 1024:  # Less than 10MB
            try:
                results = pipeline.process_clinical_trial(temp_file_path)
                
                # Clean up temp file
                os.unlink(temp_file_path)
                
                # Store results
                analysis_results[analysis_id] = {
                    "status": "completed",
                    "timestamp": datetime.now().isoformat(),
                    "filename": file.filename,
                    "progress": 100.0,
                    "message": "Analysis completed successfully",
                    "results": results
                }
                
                return {
                    "analysis_id": analysis_id,
                    "status": "completed",
                    "message": "Analysis completed successfully",
                    "results": results
                }
                
            except Exception as e:
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
                analysis_results[analysis_id] = {
                    "status": "failed",
                    "timestamp": datetime.now().isoformat(),
                    "filename": file.filename,
                    "progress": 0.0,
                    "message": f"Analysis failed: {str(e)}"
                }
                
                raise HTTPException(
                    status_code=500,
                    detail=f"Analysis failed: {str(e)}"
                )
        
        else:
            # For large files, process in background
            background_tasks.add_task(
                process_large_file,
                analysis_id,
                temp_file_path,
                file.filename
            )
            
            return {
                "analysis_id": analysis_id,
                "status": "processing",
                "message": "Large file detected. Analysis started in background. Use /status/{analysis_id} to check progress."
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


async def process_large_file(analysis_id: str, temp_file_path: str, filename: str):
    """Background task for processing large files."""
    try:
        # Update progress
        analysis_results[analysis_id]["progress"] = 25.0
        analysis_results[analysis_id]["message"] = "Processing PDF with Cerebras..."
        
        results = pipeline.process_clinical_trial(temp_file_path)
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Store final results
        analysis_results[analysis_id] = {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "progress": 100.0,
            "message": "Analysis completed successfully",
            "results": results
        }
        
    except Exception as e:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        analysis_results[analysis_id] = {
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "progress": 0.0,
            "message": f"Analysis failed: {str(e)}"
        }


@app.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get the status of an analysis by ID."""
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis ID {analysis_id} not found"
        )
    
    return analysis_results[analysis_id]


@app.get("/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """Get the complete results of an analysis by ID."""
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis ID {analysis_id} not found"
        )
    
    analysis = analysis_results[analysis_id]
    
    if analysis["status"] != "completed":
        raise HTTPException(
            status_code=202,
            detail=f"Analysis not completed. Status: {analysis['status']}"
        )
    
    return analysis.get("results", {})


@app.get("/download/{analysis_id}/{file_type}")
async def download_analysis_file(analysis_id: str, file_type: str):
    """
    Download specific analysis files.
    
    file_type can be: json, csv, dashboard, report, summary
    """
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis ID {analysis_id} not found"
        )
    
    analysis = analysis_results[analysis_id]
    
    if analysis["status"] != "completed":
        raise HTTPException(
            status_code=202,
            detail=f"Analysis not completed. Status: {analysis['status']}"
        )
    
    results = analysis.get("results", {})
    generated_files = results.get("generated_files", [])
    
    # Find the requested file type
    target_file = None
    for file_path in generated_files:
        filename = os.path.basename(file_path).lower()
        
        if file_type == "json" and "clinical_data" in filename and filename.endswith('.json'):
            target_file = file_path
            break
        elif file_type == "csv" and filename.endswith('.csv'):
            target_file = file_path
            break
        elif file_type == "dashboard" and "dashboard" in filename and filename.endswith('.png'):
            target_file = file_path
            break
        elif file_type == "report" and "analysis_report" in filename and filename.endswith('.txt'):
            target_file = file_path
            break
        elif file_type == "summary" and "executive_summary" in filename and filename.endswith('.txt'):
            target_file = file_path
            break
    
    if not target_file or not os.path.exists(target_file):
        raise HTTPException(
            status_code=404,
            detail=f"File type '{file_type}' not found for analysis {analysis_id}"
        )
    
    return FileResponse(
        target_file,
        filename=os.path.basename(target_file)
    )


@app.get("/analyses")
async def list_analyses():
    """List all analyses with their status."""
    return {
        "total_analyses": len(analysis_results),
        "analyses": [
            {
                "analysis_id": analysis_id,
                "filename": data.get("filename", "unknown"),
                "status": data.get("status", "unknown"),
                "timestamp": data.get("timestamp", "unknown")
            }
            for analysis_id, data in analysis_results.items()
        ]
    }


@app.delete("/analyses/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis and its associated files."""
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis ID {analysis_id} not found"
        )
    
    analysis = analysis_results[analysis_id]
    
    # Clean up generated files if analysis completed
    if analysis["status"] == "completed" and "results" in analysis:
        results = analysis["results"]
        generated_files = results.get("generated_files", [])
        
        for file_path in generated_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Warning: Could not delete file {file_path}: {str(e)}")
    
    # Remove from memory
    del analysis_results[analysis_id]
    
    return {
        "message": f"Analysis {analysis_id} deleted successfully"
    }


# Development server runner
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Clinical Trial Copilot API server...")
    print("📖 API documentation available at: http://localhost:8000/docs")
    print("🔍 Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
