import os
import uuid
import logging
from typing import Dict, Any, Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import json
from datetime import datetime

from app.models.poster_models import PosterRequest, PosterResponse, PosterSize, PosterTheme
from app.services.ai_service import GoogleCloudAIService
from app.templates.template_config import get_template, get_available_templates, get_template_config
from app.utils.helpers import generate_unique_id, get_color_palette, get_timestamp

logger = logging.getLogger(__name__)

class PosterGenerationService:
    def __init__(self, ai_service: GoogleCloudAIService):
        self.ai_service = ai_service
        self.output_folder = os.getenv("OUTPUT_FOLDER", "generated_posters")
        self.templates_folder = "app/templates"
        
        # Ensure output directory exists
        os.makedirs(self.output_folder, exist_ok=True)
    
    async def generate_poster(self, request: PosterRequest) -> Dict[str, Any]:
        """Generate a complete poster based on the request"""
        try:
            # Generate unique ID for this poster
            poster_id = generate_unique_id()
            
            # Get poster dimensions
            width, height = self._get_poster_dimensions(request.size, request.custom_width, request.custom_height)
            
            # Create base canvas
            poster = Image.new('RGB', (width, height), color='white')
            
            # Generate background if requested
            if request.background_prompt:
                background = await self._generate_background(request.background_prompt, width, height)
                if background:
                    poster.paste(background, (0, 0))
            else:
                # Apply theme-based background
                poster = self._apply_theme_background(poster, request.theme)
            
            # Add main content using template
            poster = await self._add_content_to_poster(poster, request)
            
            # Save the poster
            filename = f"{poster_id}.png"
            file_path = os.path.join(self.output_folder, filename)
            poster.save(file_path, 'PNG', quality=95)
            
            return {
                "poster_id": poster_id,
                "filename": filename,
                "file_path": file_path,
                "width": width,
                "height": height,
                "theme": request.theme,
                "generated_at": get_timestamp()
            }
            
            # Create metadata
            metadata = {
                "poster_id": poster_id,
                "created_at": datetime.now().isoformat(),
                "request": request.dict(),
                "dimensions": {"width": width, "height": height},
                "file_size": os.path.getsize(file_path)
            }
            
            # Save metadata
            metadata_path = os.path.join(self.output_folder, f"{poster_id}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return PosterResponse(
                poster_id=poster_id,
                file_path=file_path,
                preview_url=f"/api/poster/{poster_id}/preview",
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Poster generation error: {e}")
            raise
    
    async def _generate_background(self, prompt: str, width: int, height: int) -> Optional[Image.Image]:
        """Generate AI background image"""
        try:
            # Enhance the prompt for background generation
            enhanced_prompt = f"Background for poster: {prompt}, clean design, suitable for text overlay, professional"
            
            # Determine aspect ratio
            aspect_ratio = f"{width}:{height}" if width >= height else f"{height}:{width}"
            
            # Generate image
            result = await self.ai_service.generate_image(
                prompt=enhanced_prompt,
                style="clean and modern",
                aspect_ratio=aspect_ratio
            )
            
            if result and "image_data" in result:
                # Convert to PIL Image
                img = Image.open(io.BytesIO(result["image_data"]))
                
                # Resize to exact dimensions
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Apply slight blur for text readability
                img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
                
                # Reduce opacity
                overlay = Image.new('RGBA', (width, height), (255, 255, 255, 100))
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
                
                return img
            
        except Exception as e:
            logger.error(f"Background generation error: {e}")
        
        return None
    
    def _apply_theme_background(self, poster: Image.Image, theme: PosterTheme) -> Image.Image:
        """Apply theme-based background"""
        width, height = poster.size
        draw = ImageDraw.Draw(poster)
        
        theme_colors = {
            PosterTheme.MODERN: ['#f8f9fa', '#e9ecef', '#6c757d'],
            PosterTheme.CLASSIC: ['#f5f5dc', '#deb887', '#8b4513'],
            PosterTheme.MINIMAL: ['#ffffff', '#f8f9fa', '#e9ecef'],
            PosterTheme.VIBRANT: ['#ff6b6b', '#4ecdc4', '#45b7d1'],
            PosterTheme.CORPORATE: ['#2c3e50', '#34495e', '#3498db'],
            PosterTheme.EVENT: ['#e74c3c', '#f39c12', '#9b59b6'],
            PosterTheme.SALE: ['#e74c3c', '#f1c40f', '#27ae60']
        }
        
        colors = theme_colors.get(theme, theme_colors[PosterTheme.MODERN])
        
        # Create gradient background
        for i in range(height):
            color_intensity = int(255 * (1 - i / height))
            color = tuple(int(c * color_intensity / 255) for c in self._hex_to_rgb(colors[0]))
            draw.line([(0, i), (width, i)], fill=color)
        
        return poster
    
    async def _add_content_to_poster(self, poster: Image.Image, request: PosterRequest) -> Image.Image:
        """Add text and content to the poster"""
        draw = ImageDraw.Draw(poster)
        width, height = poster.size
        
        try:
            # Try to load a good font, fallback to default
            title_font_size = max(24, width // 20)
            subtitle_font_size = max(16, width // 30)
            
            try:
                title_font = ImageFont.truetype("arial.ttf", title_font_size)
                subtitle_font = ImageFont.truetype("arial.ttf", subtitle_font_size)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Add main title
            title_y = height // 4
            self._draw_text_with_outline(
                draw, request.title, width // 2, title_y, title_font, 
                fill='white', outline='black', anchor='mm'
            )
            
            # Add description if provided
            if request.description:
                desc_y = title_y + title_font_size + 20
                self._draw_text_with_outline(
                    draw, request.description, width // 2, desc_y, subtitle_font,
                    fill='white', outline='black', anchor='mm'
                )
            
            # Add additional text if provided
            if request.additional_text:
                additional_y = height * 3 // 4
                self._draw_text_with_outline(
                    draw, request.additional_text, width // 2, additional_y, subtitle_font,
                    fill='white', outline='black', anchor='mm'
                )
            
            # Add logo placeholder if requested
            if request.include_logo:
                self._add_logo_placeholder(draw, width, height)
            
        except Exception as e:
            logger.error(f"Content addition error: {e}")
        
        return poster
    
    def _draw_text_with_outline(self, draw, text, x, y, font, fill, outline, anchor='mm', outline_width=2):
        """Draw text with outline for better visibility"""
        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline, anchor=anchor)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=fill, anchor=anchor)
    
    def _add_logo_placeholder(self, draw, width, height):
        """Add a logo placeholder"""
        logo_size = min(width, height) // 8
        logo_x = width - logo_size - 20
        logo_y = 20
        
        # Draw placeholder rectangle
        draw.rectangle(
            [logo_x, logo_y, logo_x + logo_size, logo_y + logo_size],
            outline='gray', width=2
        )
        
        # Add "LOGO" text
        try:
            font = ImageFont.truetype("arial.ttf", logo_size // 4)
        except:
            font = ImageFont.load_default()
        
        draw.text(
            (logo_x + logo_size // 2, logo_y + logo_size // 2),
            "LOGO", font=font, fill='gray', anchor='mm'
        )
    
    def _get_poster_dimensions(self, size: PosterSize, custom_width: Optional[int], custom_height: Optional[int]) -> tuple:
        """Get poster dimensions based on size"""
        size_map = {
            PosterSize.A4: (2480, 3508),  # 300 DPI A4
            PosterSize.LETTER: (2550, 3300),  # 300 DPI Letter
            PosterSize.SOCIAL_MEDIA: (1080, 1080),  # Square format
            PosterSize.BANNER: (1200, 400),  # Banner format
            PosterSize.CUSTOM: (custom_width or 800, custom_height or 600)
        }
        
        return size_map.get(size, (800, 600))
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_poster_file(self, poster_id: str) -> Optional[str]:
        """Get the file path for a generated poster"""
        file_path = os.path.join(self.output_folder, f"{poster_id}.png")
        return file_path if os.path.exists(file_path) else None
    
    def get_poster_metadata(self, poster_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a generated poster"""
        metadata_path = os.path.join(self.output_folder, f"{poster_id}_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get available poster templates"""
        return get_available_templates()
    
    def _apply_template_layout(self, poster: Image.Image, template_name: str, content: Dict[str, Any]) -> Image.Image:
        """Apply template layout to poster"""
        try:
            template_config = get_template_config(template_name)
            layout = template_config.get("layout", {})
            styles = template_config.get("styles", {})
            fonts = template_config.get("fonts", {})
            
            draw = ImageDraw.Draw(poster)
            
            # Apply template-specific content based on layout
            for area_name, area_config in layout.items():
                if area_name in content and content[area_name]:
                    self._render_template_area(
                        draw, area_config, content[area_name], 
                        fonts.get(area_name.replace("_area", ""), {}),
                        styles
                    )
            
            return poster
        except Exception as e:
            logger.error(f"Template application error: {e}")
            return poster
    
    def _render_template_area(self, draw, area_config, content_text, font_config, styles):
        """Render content in a specific template area"""
        try:
            x, y = area_config["x"], area_config["y"]
            width, height = area_config["width"], area_config["height"]
            
            # Get font
            font_size = font_config.get("size", 16)
            font_family = font_config.get("family", "arial.ttf")
            font_weight = font_config.get("weight", "normal")
            
            try:
                font = ImageFont.truetype(font_family, font_size)
            except:
                font = ImageFont.load_default()
            
            # Wrap text to fit area
            wrapped_text = self._wrap_text(content_text, font, width)
            
            # Draw text
            draw.text((x, y), wrapped_text, font=font, fill='black')
            
        except Exception as e:
            logger.error(f"Template area rendering error: {e}")
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
