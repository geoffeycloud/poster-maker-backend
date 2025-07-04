from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class PosterSize(str, Enum):
    A4 = "A4"
    LETTER = "LETTER"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    BANNER = "BANNER"
    CUSTOM = "CUSTOM"

class PosterTheme(str, Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    MINIMAL = "minimal"
    VIBRANT = "vibrant"
    CORPORATE = "corporate"
    EVENT = "event"
    SALE = "sale"

class PosterRequest(BaseModel):
    title: str = Field(..., description="Main title for the poster")
    description: Optional[str] = Field(None, description="Additional description or subtitle")
    theme: PosterTheme = Field(PosterTheme.MODERN, description="Visual theme of the poster")
    size: PosterSize = Field(PosterSize.A4, description="Size of the poster")
    custom_width: Optional[int] = Field(None, description="Custom width in pixels")
    custom_height: Optional[int] = Field(None, description="Custom height in pixels")
    background_prompt: Optional[str] = Field(None, description="Prompt for background image generation")
    include_logo: bool = Field(False, description="Whether to include a logo placeholder")
    color_scheme: Optional[List[str]] = Field(None, description="Preferred color scheme")
    additional_text: Optional[str] = Field(None, description="Any additional text content")

class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for text generation")
    context: Optional[str] = Field(None, description="Additional context for text generation")
    tone: Optional[str] = Field("professional", description="Tone of the generated text")
    max_length: Optional[int] = Field(200, description="Maximum length of generated text")

class TextGenerationResponse(BaseModel):
    text: str
    prompt: str
    message: str = "Text generated successfully"

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for image generation")
    style: Optional[str] = Field("realistic", description="Style of the image")
    aspect_ratio: Optional[str] = Field("16:9", description="Aspect ratio of the image")
    quality: Optional[str] = Field("standard", description="Quality of the image")

class ImageGenerationResponse(BaseModel):
    image_url: Optional[str] = None
    image_data: Optional[str] = None
    prompt: str
    message: str = "Image generated successfully"

class PosterResponse(BaseModel):
    poster_id: str
    image_url: str
    filename: str
    theme: str
    message: str = "Poster generated successfully"

class TemplateInfo(BaseModel):
    id: str
    name: str
    description: str
    theme: PosterTheme
    preview_image: str
    supported_sizes: List[PosterSize]
