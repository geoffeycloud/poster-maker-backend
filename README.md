# AI Poster Maker Backend

An AI-powered poster generation backend built with FastAPI and Google Cloud Vertex AI. This application allows users to generate beautiful posters with AI-generated text and images.

## Features

- 🎨 AI-powered poster generation with multiple themes
- 📝 Intelligent text generation using Google Gemini
- 🖼️ AI image generation with Vertex AI Imagen
- 🎯 Multiple poster templates and themes
- 📏 Various poster sizes (A4, Letter, Social Media, Banner, Custom)
- 🔧 RESTful API with FastAPI
- 📊 Comprehensive logging and error handling

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Vertex AI enabled
- Service Account with Vertex AI User and Storage Object Admin roles
- Google Cloud credentials JSON file

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd poster-maker-backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials:**
   - Place your service account JSON file in the project root
   - Update the `.env` file with your Google Cloud configuration

4. **Configure environment variables:**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   ```

## Configuration

Update the `.env` file with your specific configuration:

```env
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=your-service-account-key.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Output Settings
OUTPUT_FOLDER=generated_posters
MAX_FILE_SIZE=10485760

# AI Service Settings
DEFAULT_MODEL=gemini-1.5-flash
IMAGE_MODEL=imagen-3.0-generate-001
MAX_TOKENS=1000
TEMPERATURE=0.7

# Poster Generation Settings
DEFAULT_POSTER_SIZE=A4
DEFAULT_THEME=modern
MAX_POSTER_WIDTH=4000
MAX_POSTER_HEIGHT=4000
```

## Running the Application

### Method 1: Using the startup script (Recommended)
```bash
python run.py
```

### Method 2: Using uvicorn directly
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Method 3: Using Python module
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- **GET /** - API status (JSON)
- **GET /health** - Health check page (HTML)

### Poster Generation
- **POST /api/generate-poster** - Generate complete poster
- **POST /api/generate-text** - Generate AI text content
- **POST /api/generate-image** - Generate AI images

### Utilities
- **GET /api/templates** - Get available templates
- **GET /api/themes** - Get available themes
- **GET /api/preview-poster/{poster_id}** - Preview generated poster
- **GET /api/download-poster/{poster_id}** - Download generated poster

### Documentation
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API documentation

## Usage Examples

### Generate a Poster
```bash
curl -X POST http://localhost:8000/api/generate-poster \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Summer Music Festival 2024",
    "description": "Join us for an unforgettable night!",
    "theme": "vibrant",
    "size": "A4",
    "template": "event_flyer",
    "background_prompt": "vibrant summer festival atmosphere",
    "include_logo": true
  }'
```

### Generate Text
```bash
curl -X POST http://localhost:8000/api/generate-text \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a catchy slogan for a summer music festival",
    "tone": "exciting and inviting"
  }'
```

### Get Available Templates
```bash
curl -X GET http://localhost:8000/api/templates
```

## Project Structure

```
poster-maker-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── poster_models.py    # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # Google Cloud AI service
│   │   └── poster_service.py   # Poster generation service
│   ├── templates/
│   │   ├── __init__.py
│   │   └── template_config.py  # Template configurations
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Utility functions
├── generated_posters/          # Output directory
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── run.py                     # Startup script
├── test_samples.py            # Sample requests
└── README.md                  # This file
```

## Available Themes

- **Professional** - Clean, business-focused design
- **Creative** - Artistic and vibrant design
- **Minimal** - Simple, clean aesthetic
- **Vibrant** - Colorful and energetic
- **Dark** - Dark theme with light text
- **Retro** - Vintage-inspired design
- **Modern** - Contemporary design
- **Elegant** - Sophisticated and refined

## Available Templates

- **Event Flyer** - Perfect for events, concerts, and gatherings
- **Business Poster** - Professional design for business promotions
- **Social Media Post** - Optimized for social media platforms
- **Announcement** - Clean design for announcements and notices
- **Creative Poster** - Artistic and creative design with flexible layout

## Poster Sizes

- **A4** - 2480 x 3508 pixels (300 DPI)
- **Letter** - 2550 x 3300 pixels (300 DPI)
- **Social Media** - 1080 x 1080 pixels (square)
- **Banner** - 1200 x 400 pixels (landscape)
- **Custom** - Specify your own dimensions

## Error Handling

The application includes comprehensive error handling:
- Google Cloud API errors
- Image processing errors
- Template rendering errors
- File system errors
- Validation errors

## Logging

The application uses structured logging with different levels:
- **INFO** - General application information
- **WARNING** - Potential issues
- **ERROR** - Error conditions
- **DEBUG** - Detailed debugging information

## Performance Considerations

- Poster generation typically takes 5-15 seconds depending on complexity
- Generated images are cached locally
- File size limits are enforced to prevent resource exhaustion
- Background processing for large requests

## Security

- CORS middleware configured
- Input validation using Pydantic models
- File size limits
- Secure file handling
- Environment variable configuration

## Troubleshooting

### Common Issues

1. **Google Cloud Authentication Error**
   - Ensure service account JSON file is present
   - Check GOOGLE_APPLICATION_CREDENTIALS path
   - Verify service account has required permissions

2. **Font Loading Issues**
   - System fonts may not be available
   - Application falls back to default fonts
   - Consider installing system fonts if needed

3. **Image Generation Failures**
   - Check Google Cloud quotas
   - Verify Vertex AI API is enabled
   - Check network connectivity

4. **Permission Errors**
   - Ensure write permissions to output directory
   - Check file system permissions

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Ensure all dependencies are installed
4. Verify Google Cloud configuration

## Version History

- **v1.0.0** - Initial release with basic poster generation
- Features: AI text/image generation, multiple themes, templates, REST API
