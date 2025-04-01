# /ml_model/final/api_server.py

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add PYTHONPATH from .env to sys.path
python_path = os.getenv("PYTHONPATH")
if python_path and python_path not in sys.path:
    sys.path.append(os.path.abspath(python_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml_model.final.main_verifier import run_all_verifications

app = FastAPI()

# Enable CORS (for use with frontend browser extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with exact extension origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request format
class VerificationInput(BaseModel):
    title: str
    content: str
    url: str

# API route
@app.post("/api/analyze")
def analyze(data: VerificationInput):
    """
    Accepts title, content, and URL from the frontend,
    returns combined analysis from all 3 verification layers.
    """
    result = run_all_verifications(data.title, data.content, data.url)
    return result
