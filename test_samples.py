"""
Sample API requests for testing the AI Poster Maker Backend
"""

# Sample poster generation request
sample_poster_request = {
    "title": "Summer Music Festival 2024",
    "description": "Join us for an unforgettable night of music and fun!",
    "additional_text": "July 15-16, 2024 | Central Park | Tickets: $45",
    "theme": "vibrant",
    "size": "A4",
    "template": "event_flyer",
    "background_prompt": "vibrant summer festival atmosphere with colorful stage lights",
    "include_logo": True,
    "custom_text": "Don't miss out on the biggest music event of the year!"
}

# Sample text generation request
sample_text_request = {
    "prompt": "Create an engaging description for a summer music festival poster",
    "context": "music festival, summer, outdoor event, family-friendly",
    "tone": "exciting and inviting",
    "max_length": 200
}

# Sample image generation request
sample_image_request = {
    "prompt": "A vibrant summer music festival scene with colorful stage lights and crowd",
    "style": "modern digital art",
    "size": "landscape"
}

# Test endpoints
test_endpoints = {
    "health_check": "GET /health",
    "generate_poster": "POST /api/generate-poster",
    "generate_text": "POST /api/generate-text",
    "generate_image": "POST /api/generate-image",
    "get_templates": "GET /api/templates",
    "get_themes": "GET /api/themes"
}

# cURL examples for testing
curl_examples = {
    "health_check": "curl -X GET http://localhost:8000/health",
    "generate_poster": """curl -X POST http://localhost:8000/api/generate-poster \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Summer Music Festival 2024",
    "description": "Join us for an unforgettable night!",
    "theme": "vibrant",
    "size": "A4",
    "template": "event_flyer"
  }'""",
    "generate_text": """curl -X POST http://localhost:8000/api/generate-text \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "Create a catchy slogan for a summer music festival"
  }'""",
    "get_templates": "curl -X GET http://localhost:8000/api/templates",
    "get_themes": "curl -X GET http://localhost:8000/api/themes"
}
