from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files from the 'assets' directory
BASE_DIR = Path(__file__).resolve().parent
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/list", response_class=HTMLResponse)
async def list_content(request: Request):
    # URL to the raw README.md file
    url = "https://raw.githubusercontent.com/sukhdeepg/reading-list/main/README.md"
    
    # Fetch the content
    response = requests.get(url)
    md_content = response.text  # Get the text content of the response
    
    # Properly escape the content for JavaScript
    escaped_content = json.dumps(md_content)[1:-1]  # Remove the outer quotes
    
    return templates.TemplateResponse(
        "list.html",
        {
            "request": request, 
            "content": escaped_content
        }
    )
