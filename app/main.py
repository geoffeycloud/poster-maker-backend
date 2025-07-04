from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import Optional
import json

# Import our models and services
from app.models.poster_models import (
    PosterRequest, 
    PosterResponse, 
    TextGenerationRequest, 
    TextGenerationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse
)
from app.services.ai_service import GoogleCloudAIService
from app.services.poster_service import PosterGenerationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Poster Maker Backend",
    description="Generate beautiful posters with AI-powered text and images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create output directory if it doesn't exist
output_dir = Path("generated_posters")
output_dir.mkdir(exist_ok=True)

# Mount static files for serving generated posters
app.mount("/static", StaticFiles(directory="generated_posters"), name="static")

# Initialize services
ai_service = GoogleCloudAIService()
poster_service = PosterGenerationService(ai_service)  

@app.get("/")
async def read_root():
    return {
        "message": "AI Poster Maker Backend is Running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "generate_poster": "/api/generate-poster",
            "generate_text": "/api/generate-text",
            "generate_image": "/api/generate-image",
            "preview_poster": "/api/preview-poster/{poster_id}",
            "download_poster": "/api/download-poster/{poster_id}",
            "docs": "/docs"
        }
    }  

@app.get("/health", response_class=HTMLResponse)
async def health_check():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Poster Maker Backend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
                margin: 20px 0;
            }
            .endpoints {
                margin-top: 30px;
            }
            .endpoint {
                background: #e9ecef;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                font-family: monospace;
            }
            .method {
                color: #007bff;
                font-weight: bold;
            }
            .post { color: #28a745; }
            .get { color: #17a2b8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 AI Poster Maker Backend</h1>
            <div class="status">
                ✅ Server is running successfully!
            </div>
            <div class="endpoints">
                <h3>Available Endpoints:</h3>
                <div class="endpoint"><span class="method get">GET</span> / - API status (JSON)</div>
                <div class="endpoint"><span class="method get">GET</span> /health - This page (HTML)</div>
                <div class="endpoint"><span class="method post">POST</span> /api/generate-poster - Generate complete poster</div>
                <div class="endpoint"><span class="method post">POST</span> /api/generate-text - Generate AI text content</div>
                <div class="endpoint"><span class="method post">POST</span> /api/generate-image - Generate AI images</div>
                <div class="endpoint"><span class="method get">GET</span> /api/preview-poster/{poster_id} - Preview poster</div>
                <div class="endpoint"><span class="method get">GET</span> /api/download-poster/{poster_id} - Download poster</div>
                <div class="endpoint"><span class="method get">GET</span> /api/templates - Get available templates</div>
                <div class="endpoint"><span class="method get">GET</span> /api/themes - Get available themes</div>
                <div class="endpoint"><span class="method get">GET</span> /docs - FastAPI documentation</div>
            </div>
            <div style="margin-top: 30px; text-align: center;">
                <a href="/docs" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    📚 View API Documentation
                </a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/api/generate-poster", response_model=PosterResponse)
async def generate_poster(request: PosterRequest):
    """Generate a complete poster with AI-generated content"""
    try:
        logger.info(f"Generating poster with theme: {request.theme}")
        
        # Generate the poster
        poster_data = await poster_service.generate_poster(request)
        
        return PosterResponse(
            poster_id=poster_data["poster_id"],
            image_url=f"/static/{poster_data['filename']}",
            filename=poster_data["filename"],
            theme=request.theme,
            message="Poster generated successfully!"
        )
    
    except Exception as e:
        logger.error(f"Error generating poster: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate poster: {str(e)}")

@app.post("/api/generate-text", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """Generate AI text content for posters"""
    try:
        logger.info(f"Generating text for: {request.prompt}")
        
        # Generate text using AI service
        generated_text = await ai_service.generate_text(request.prompt)
        
        return TextGenerationResponse(
            text=generated_text,
            prompt=request.prompt,
            message="Text generated successfully!"
        )
    
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate text: {str(e)}")

@app.post("/api/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Generate AI images for posters"""
    try:
        logger.info(f"Generating image for: {request.prompt}")
        
        # Generate image using AI service
        image_data = await ai_service.generate_image(request.prompt)
        
        return ImageGenerationResponse(
            image_url=image_data.get("image_url", ""),
            image_data=image_data.get("image_data", ""),
            prompt=request.prompt,
            message="Image generated successfully!"
        )
    
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")

@app.get("/api/preview-poster/{poster_id}")
async def preview_poster(poster_id: str):
    """Preview a generated poster"""
    try:
        poster_path = output_dir / f"{poster_id}.png"
        if not poster_path.exists():
            raise HTTPException(status_code=404, detail="Poster not found")
        
        return FileResponse(
            poster_path,
            media_type="image/png",
            filename=f"{poster_id}.png"
        )
    
    except Exception as e:
        logger.error(f"Error previewing poster: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to preview poster: {str(e)}")

@app.get("/api/download-poster/{poster_id}")
async def download_poster(poster_id: str):
    """Download a generated poster"""
    try:
        poster_path = output_dir / f"{poster_id}.png"
        if not poster_path.exists():
            raise HTTPException(status_code=404, detail="Poster not found")
        
        return FileResponse(
            poster_path,
            media_type="application/octet-stream",
            filename=f"poster_{poster_id}.png"
        )
    
    except Exception as e:
        logger.error(f"Error downloading poster: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download poster: {str(e)}")

@app.get("/api/templates")
async def get_templates():
    """Get available poster templates"""
    try:
        templates = poster_service.get_available_templates()
        return {"templates": templates}
    
    except Exception as e:
        logger.error(f"Error fetching templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch templates: {str(e)}")

@app.get("/api/themes")
async def get_themes():
    """Get available poster themes"""
    return {
        "themes": [
            "professional",
            "creative",
            "minimal",
            "vibrant",
            "dark",
            "retro",
            "modern",
            "elegant"
        ]
    }