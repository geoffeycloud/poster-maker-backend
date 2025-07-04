#!/usr/bin/env python3
"""
Startup script for the AI Poster Maker Backend
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def setup_environment():
    """Setup environment and validate configuration"""
    logger = logging.getLogger(__name__)
    
    # Check if Google Cloud credentials exist
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path or not os.path.exists(credentials_path):
        logger.error("Google Cloud credentials not found. Please check GOOGLE_APPLICATION_CREDENTIALS.")
        return False
    
    # Ensure output directory exists
    output_dir = os.getenv('OUTPUT_FOLDER', 'generated_posters')
    Path(output_dir).mkdir(exist_ok=True)
    
    # Validate Google Cloud project configuration
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION')
    
    if not project_id or not location:
        logger.error("Google Cloud project ID or location not configured.")
        return False
    
    logger.info(f"Starting AI Poster Maker Backend...")
    logger.info(f"Google Cloud Project: {project_id}")
    logger.info(f"Google Cloud Location: {location}")
    logger.info(f"Output Directory: {output_dir}")
    
    return True

if __name__ == "__main__":
    if setup_environment():
        import uvicorn
        from app.main import app
        
        # Get configuration from environment
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8000))
        debug = os.getenv('DEBUG', 'True').lower() == 'true'
        
        # Start the server
        uvicorn.run(
            app, 
            host=host, 
            port=port, 
            reload=debug,
            log_level=os.getenv('LOG_LEVEL', 'info').lower()
        )
    else:
        print("Failed to start application. Check configuration.")
        sys.exit(1)
