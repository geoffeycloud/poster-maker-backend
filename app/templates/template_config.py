"""
Template configuration for poster generation
"""
from typing import Dict, Any, List

class PosterTemplate:
    """Base template class for poster generation"""
    
    def __init__(self, name: str, description: str, config: Dict[str, Any]):
        self.name = name
        self.description = description
        self.config = config
    
    def get_layout(self) -> Dict[str, Any]:
        """Get layout configuration"""
        return self.config.get("layout", {})
    
    def get_styles(self) -> Dict[str, Any]:
        """Get style configuration"""
        return self.config.get("styles", {})
    
    def get_fonts(self) -> Dict[str, Any]:
        """Get font configuration"""
        return self.config.get("fonts", {})

# Template definitions
TEMPLATES = {
    "event_flyer": PosterTemplate(
        name="Event Flyer",
        description="Perfect for events, concerts, and gatherings",
        config={
            "layout": {
                "title_area": {"x": 50, "y": 100, "width": 700, "height": 150},
                "subtitle_area": {"x": 50, "y": 270, "width": 700, "height": 80},
                "content_area": {"x": 50, "y": 370, "width": 700, "height": 200},
                "image_area": {"x": 50, "y": 590, "width": 700, "height": 300},
                "footer_area": {"x": 50, "y": 910, "width": 700, "height": 80}
            },
            "styles": {
                "background_style": "gradient",
                "border_style": "rounded",
                "shadow": True,
                "padding": 20
            },
            "fonts": {
                "title": {"size": 48, "weight": "bold", "family": "Arial"},
                "subtitle": {"size": 24, "weight": "normal", "family": "Arial"},
                "content": {"size": 18, "weight": "normal", "family": "Arial"},
                "footer": {"size": 14, "weight": "normal", "family": "Arial"}
            }
        }
    ),
    
    "business_poster": PosterTemplate(
        name="Business Poster",
        description="Professional design for business promotions",
        config={
            "layout": {
                "logo_area": {"x": 50, "y": 50, "width": 200, "height": 100},
                "title_area": {"x": 270, "y": 50, "width": 480, "height": 100},
                "hero_image": {"x": 50, "y": 170, "width": 700, "height": 300},
                "content_area": {"x": 50, "y": 490, "width": 700, "height": 300},
                "cta_area": {"x": 50, "y": 810, "width": 700, "height": 100},
                "contact_area": {"x": 50, "y": 930, "width": 700, "height": 60}
            },
            "styles": {
                "background_style": "solid",
                "border_style": "clean",
                "shadow": False,
                "padding": 30
            },
            "fonts": {
                "title": {"size": 36, "weight": "bold", "family": "Arial"},
                "content": {"size": 16, "weight": "normal", "family": "Arial"},
                "cta": {"size": 20, "weight": "bold", "family": "Arial"},
                "contact": {"size": 12, "weight": "normal", "family": "Arial"}
            }
        }
    ),
    
    "social_media": PosterTemplate(
        name="Social Media Post",
        description="Optimized for social media platforms",
        config={
            "layout": {
                "background_image": {"x": 0, "y": 0, "width": 800, "height": 800},
                "overlay": {"x": 0, "y": 0, "width": 800, "height": 800},
                "title_area": {"x": 100, "y": 200, "width": 600, "height": 150},
                "content_area": {"x": 100, "y": 400, "width": 600, "height": 200},
                "hashtag_area": {"x": 100, "y": 650, "width": 600, "height": 50}
            },
            "styles": {
                "background_style": "image_overlay",
                "border_style": "none",
                "shadow": False,
                "padding": 40,
                "overlay_opacity": 0.6
            },
            "fonts": {
                "title": {"size": 42, "weight": "bold", "family": "Arial"},
                "content": {"size": 18, "weight": "normal", "family": "Arial"},
                "hashtags": {"size": 14, "weight": "normal", "family": "Arial"}
            }
        }
    ),
    
    "announcement": PosterTemplate(
        name="Announcement",
        description="Clean design for announcements and notices",
        config={
            "layout": {
                "header_area": {"x": 50, "y": 50, "width": 700, "height": 100},
                "title_area": {"x": 50, "y": 170, "width": 700, "height": 120},
                "content_area": {"x": 50, "y": 310, "width": 700, "height": 400},
                "image_area": {"x": 50, "y": 730, "width": 700, "height": 200},
                "footer_area": {"x": 50, "y": 950, "width": 700, "height": 40}
            },
            "styles": {
                "background_style": "clean",
                "border_style": "minimal",
                "shadow": True,
                "padding": 25
            },
            "fonts": {
                "header": {"size": 20, "weight": "bold", "family": "Arial"},
                "title": {"size": 36, "weight": "bold", "family": "Arial"},
                "content": {"size": 16, "weight": "normal", "family": "Arial"},
                "footer": {"size": 12, "weight": "normal", "family": "Arial"}
            }
        }
    ),
    
    "creative_poster": PosterTemplate(
        name="Creative Poster",
        description="Artistic and creative design with flexible layout",
        config={
            "layout": {
                "creative_area": {"x": 0, "y": 0, "width": 800, "height": 1000},
                "title_area": {"x": 100, "y": 150, "width": 600, "height": 200},
                "visual_area": {"x": 50, "y": 400, "width": 700, "height": 400},
                "text_area": {"x": 100, "y": 850, "width": 600, "height": 100}
            },
            "styles": {
                "background_style": "artistic",
                "border_style": "creative",
                "shadow": True,
                "padding": 20,
                "artistic_elements": True
            },
            "fonts": {
                "title": {"size": 52, "weight": "bold", "family": "Arial"},
                "content": {"size": 18, "weight": "normal", "family": "Arial"}
            }
        }
    )
}

def get_template(template_name: str) -> PosterTemplate:
    """Get template by name"""
    return TEMPLATES.get(template_name, TEMPLATES["event_flyer"])

def get_available_templates() -> List[Dict[str, str]]:
    """Get list of available templates"""
    return [
        {
            "name": template.name,
            "key": key,
            "description": template.description
        }
        for key, template in TEMPLATES.items()
    ]

def get_template_config(template_name: str) -> Dict[str, Any]:
    """Get template configuration"""
    template = get_template(template_name)
    return template.config
