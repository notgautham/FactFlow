# /ml_model/final/api_server.py

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add PYTHONPATH from .env to sys.path (for module resolution)
python_path = os.getenv("PYTHONPATH")
if python_path and python_path not in sys.path:
    sys.path.append(os.path.abspath(python_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml_model.final.main_verifier import run_all_verifications

app = FastAPI()

# Enable CORS (for use with frontend browser extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with extension origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class VerificationInput(BaseModel):
    title: str
    content: str
    url: str

# Main endpoint
@app.post("/api/analyze")
def analyze(data: VerificationInput):
    """
    Accepts title, content, and URL from the frontend,
    returns combined analysis from all 3 verification layers.
    """
    try:
        result = run_all_verifications(data.title, data.content, data.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
