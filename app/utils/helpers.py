"""
Utility functions for the AI Poster Maker Backend
"""
import uuid
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def generate_unique_id() -> str:
    """Generate a unique ID for posters"""
    return str(uuid.uuid4())

def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def ensure_directory_exists(path: str) -> None:
    """Ensure directory exists, create if it doesn't"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def validate_image_format(filename: str) -> bool:
    """Validate if filename has a valid image extension"""
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    return Path(filename).suffix.lower() in valid_extensions

def create_response_metadata(
    poster_id: str,
    generation_time: float,
    file_size: int,
    additional_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create metadata for API responses"""
    metadata = {
        "poster_id": poster_id,
        "generation_time_seconds": round(generation_time, 2),
        "file_size_bytes": file_size,
        "generated_at": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    
    if additional_info:
        metadata.update(additional_info)
    
    return metadata

def log_api_call(endpoint: str, request_data: Dict[str, Any], success: bool = True) -> None:
    """Log API call for monitoring"""
    log_data = {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "request_summary": {
            "theme": request_data.get("theme", "unknown"),
            "has_custom_text": bool(request_data.get("custom_text")),
            "size": request_data.get("size", "unknown")
        }
    }
    
    if success:
        logger.info(f"API Call Success: {log_data}")
    else:
        logger.error(f"API Call Failed: {log_data}")

def get_color_palette(theme: str) -> Dict[str, str]:
    """Get color palette for a given theme"""
    palettes = {
        "professional": {
            "primary": "#2E3B4E",
            "secondary": "#4A90A4",
            "accent": "#7FC7D9",
            "background": "#F8F9FA",
            "text": "#2E3B4E"
        },
        "creative": {
            "primary": "#FF6B6B",
            "secondary": "#4ECDC4",
            "accent": "#45B7D1",
            "background": "#F7F9FC",
            "text": "#2D3748"
        },
        "minimal": {
            "primary": "#2D3748",
            "secondary": "#4A5568",
            "accent": "#718096",
            "background": "#FFFFFF",
            "text": "#2D3748"
        },
        "vibrant": {
            "primary": "#E53E3E",
            "secondary": "#DD6B20",
            "accent": "#D69E2E",
            "background": "#FFF5F5",
            "text": "#2D3748"
        },
        "dark": {
            "primary": "#1A202C",
            "secondary": "#2D3748",
            "accent": "#4A5568",
            "background": "#171923",
            "text": "#F7FAFC"
        },
        "retro": {
            "primary": "#C53030",
            "secondary": "#ED8936",
            "accent": "#ECC94B",
            "background": "#FDF2E9",
            "text": "#2D3748"
        },
        "modern": {
            "primary": "#667EEA",
            "secondary": "#764BA2",
            "accent": "#F093FB",
            "background": "#F8FAFC",
            "text": "#2D3748"
        },
        "elegant": {
            "primary": "#553C9A",
            "secondary": "#805AD5",
            "accent": "#B794F6",
            "background": "#FAF5FF",
            "text": "#2D3748"
        }
    }
    
    return palettes.get(theme, palettes["minimal"])

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
