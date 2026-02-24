"""
FastAPI application for Government Compliance Tool
Simple web UI for testing the scoring and rewriting engine
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from compliance_scorer import ComplianceScorer
from rewrite_engine import RewriteEngine

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Government Compliance Tool")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class AnalysisRequest(BaseModel):
    text: str
    target_grade: float = 7.0


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/analyze")
async def analyze_text(request: AnalysisRequest):
    """
    Analyze and rewrite text
    Returns original scores, rewritten text, and new scores
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "No text provided"}
            )
        
        # Validate target grade
        if request.target_grade < 5 or request.target_grade > 10:
            return JSONResponse(
                status_code=400,
                content={"error": "Target grade must be between 5 and 10"}
            )
        
        # Initialize engines with context-aware scoring
        scorer = ComplianceScorer(target_grade=request.target_grade)
        
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            # Score only (no rewriting)
            original_scores = scorer.score_text_with_context(request.text)
            return JSONResponse(content={
                "success": True,
                "original_scores": original_scores,
                "rewritten_text": None,
                "new_scores": None,
                "confidence": None,
                "iterations": 0,
                "message": "API key not configured. Scoring only.",
                "warning": "Set OPENAI_API_KEY environment variable to enable rewriting"
            })
        
        # Full analysis with rewriting
        rewrite_engine = RewriteEngine(api_key=api_key, target_grade=request.target_grade)
        result = rewrite_engine.rewrite_with_validation(request.text)
        
        return JSONResponse(content={
            "success": True,
            "original_text": result['original_text'],
            "original_scores": result['original_scores'],
            "rewritten_text": result['rewritten_text'],
            "new_scores": result['new_scores'],
            "confidence": result['confidence'],
            "iterations": result['iterations'],
            "message": result['message']
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Analysis failed: {str(e)}"}
        )


@app.post("/api/score-only")
async def score_only(request: AnalysisRequest):
    """
    Score text without rewriting
    Useful for quick validation
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "No text provided"}
            )
        
        scorer = ComplianceScorer(target_grade=request.target_grade)
        scores = scorer.score_text_with_context(request.text)
        
        return JSONResponse(content={
            "success": True,
            "scores": scores
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Scoring failed: {str(e)}"}
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    api_key_configured = bool(os.getenv('OPENAI_API_KEY'))
    
    spacy_model = False
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            spacy_model = True
        except:
            pass
    except ImportError:
        pass
    
    return JSONResponse(content={
        "status": "healthy",
        "api_key_configured": api_key_configured,
        "spacy_model_loaded": spacy_model,
        "features": {
            "scoring": True,
            "rewriting": api_key_configured,
            "passive_voice_detection": "regex" if not spacy_model else "spacy"
        }
    })


# Run the app
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Government Compliance Tool")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:8000")
    print("\nPress CTRL+C to stop")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
