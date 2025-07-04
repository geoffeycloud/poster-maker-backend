import os
import logging
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
import google.generativeai as genai
from google.api_core import exceptions
import base64
import requests
from PIL import Image
import io

logger = logging.getLogger(__name__)

class GoogleCloudAIService:
    def __init__(self):
        """Initialize Google Cloud AI services"""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "postermaker-464715")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        # Initialize Vertex AI
        try:
            aiplatform.init(project=self.project_id, location=self.location)
            logger.info(f"Initialized Vertex AI for project: {self.project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI: {e}")
            raise
    
    async def generate_text(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        tone: str = "professional",
        max_length: int = 200
    ) -> str:
        """Generate text using Gemini Pro"""
        try:
            # Configure Gemini
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-pro')
            
            # Build the full prompt
            full_prompt = self._build_text_prompt(prompt, context, tone, max_length)
            
            # Generate text
            response = model.generate_content(full_prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "Generated text not available"
                
        except Exception as e:
            logger.error(f"Text generation error: {e}")
            # Fallback to a simple response
            return self._generate_fallback_text(prompt, tone)
    
    async def generate_image(
        self, 
        prompt: str, 
        style: str = "realistic",
        aspect_ratio: str = "16:9",
        quality: str = "standard"
    ) -> Dict[str, Any]:
        """Generate image using Vertex AI Imagen"""
        try:
            # Use Vertex AI Imagen model
            model = aiplatform.Model("publishers/google/models/imagegeneration@006")
            
            # Prepare the request
            instances = [
                {
                    "prompt": f"{prompt}, {style} style, high quality",
                    "sampleCount": 1,
                    "aspectRatio": aspect_ratio,
                    "safetyFilterLevel": "block_some",
                    "personGeneration": "allow_adult"
                }
            ]
            
            parameters = {
                "sampleCount": 1,
            }
            
            # Generate image
            response = model.predict(instances=instances, parameters=parameters)
            
            if response.predictions:
                prediction = response.predictions[0]
                if "bytesBase64Encoded" in prediction:
                    image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                    return {
                        "image_data": image_data,
                        "format": "PNG",
                        "size": len(image_data)
                    }
            
            raise Exception("No image generated")
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            # Return a placeholder or fallback
            return await self._generate_fallback_image(prompt, aspect_ratio)
    
    async def enhance_poster_prompt(self, user_prompt: str, theme: str) -> str:
        """Enhance user prompt for better poster generation"""
        enhancement_prompt = f"""
        As an expert graphic designer, enhance this poster description to create a detailed, visually appealing prompt:
        
        Original: {user_prompt}
        Theme: {theme}
        
        Create a detailed description that includes:
        - Visual composition and layout
        - Color schemes and mood
        - Typography suggestions
        - Design elements and style
        - Professional presentation
        
        Make it specific for poster/flyer design:
        """
        
        return await self.generate_text(enhancement_prompt, max_length=300)
    
    def _build_text_prompt(self, prompt: str, context: Optional[str], tone: str, max_length: int) -> str:
        """Build a comprehensive prompt for text generation"""
        system_prompt = f"""
        You are a professional copywriter specializing in poster and flyer content.
        Generate {tone} text that is engaging, clear, and suitable for visual marketing materials.
        Keep the response under {max_length} characters.
        """
        
        if context:
            system_prompt += f"\n\nContext: {context}"
        
        return f"{system_prompt}\n\nRequest: {prompt}\n\nResponse:"
    
    def _generate_fallback_text(self, prompt: str, tone: str) -> str:
        """Generate fallback text when AI service is unavailable"""
        fallback_responses = {
            "professional": f"Professional content for: {prompt}",
            "casual": f"Exciting announcement about: {prompt}",
            "urgent": f"Don't miss out on: {prompt}",
            "friendly": f"Join us for: {prompt}"
        }
        
        return fallback_responses.get(tone, f"Learn more about: {prompt}")
    
    async def _generate_fallback_image(self, prompt: str, aspect_ratio: str) -> Dict[str, Any]:
        """Generate a placeholder image when AI service is unavailable"""
        try:
            # Create a simple placeholder image
            width, height = self._get_dimensions_from_aspect_ratio(aspect_ratio)
            
            # Create a gradient placeholder
            img = Image.new('RGB', (width, height), color='#4A90E2')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return {
                "image_data": img_byte_arr,
                "format": "PNG",
                "size": len(img_byte_arr),
                "is_placeholder": True
            }
            
        except Exception as e:
            logger.error(f"Fallback image generation error: {e}")
            raise
    
    def _get_dimensions_from_aspect_ratio(self, aspect_ratio: str) -> tuple:
        """Convert aspect ratio to dimensions"""
        ratio_map = {
            "16:9": (800, 450),
            "4:3": (800, 600),
            "1:1": (600, 600),
            "9:16": (450, 800)
        }
        
        return ratio_map.get(aspect_ratio, (800, 600))
