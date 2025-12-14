# GEMINI.md - AI Assistant Guidelines

## Project Overview

**Website Redesign Agent** is a backend-focused Python/FastAPI application that:
1. Captures screenshots of user-provided website URLs using Cua ComputerAgent
2. Analyzes the design using Google Gemini Vision
3. Generates a "10x better" redesigned version as a production-ready TSX component

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Backend language |
| **FastAPI** | Web framework |
| **Google Gemini 2.0 Flash** | Vision analysis + TSX code generation |
| **Cua Framework** | AI-driven browser automation (no Playwright) |
| **Claude 3.5 Sonnet** | Browser control model via Cua |
| **Tailwind CSS** | Styling in generated TSX components |

## Project Structure

```
redesign/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # FastAPI routes (/api/redesign, /api/health)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── screenshot.py       # Cua screenshot service
│   │   ├── analyzer.py         # Design analysis with Gemini Vision
│   │   └── generator.py        # TSX generation with Gemini
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Environment configuration
│   └── main.py                 # Application entry point
├── venv/                       # Virtual environment (not in git)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Local environment variables (not in git)
├── IMPLEMENTATION_PLAN.md     # Detailed implementation plan + progress
├── CHANGELOG.md               # Version history and changes
├── README.md                  # User documentation
└── GEMINI.md                  # This file - AI assistant guidelines
```

## Key Files to Understand

### Entry Points
- `src/main.py` - FastAPI application initialization
- `src/api/routes.py` - API endpoint definitions

### Core Services
- `src/services/screenshot.py` - Captures website screenshots via Cua ComputerAgent
- `src/services/analyzer.py` - Analyzes design elements using Gemini Vision
- `src/services/generator.py` - Generates redesigned TSX components

### Configuration
- `.env` / `.env.example` - Environment variables (API keys, server config)
- `src/config/settings.py` - Application settings

## Required Environment Variables

```env
GEMINI_API_KEY=         # Google Gemini API key
CUA_API_KEY=            # Cua Cloud API key
CUA_CONTAINER_NAME=     # Cua container name
CUA_BROWSER_MODEL=      # Browser control model (default: anthropic/claude-3-5-sonnet-20241022)
PORT=8000               # Server port
HOST=0.0.0.0           # Server host
```

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m src.main
# or
uvicorn src.main:app --reload

# Test the API
curl -X POST http://localhost:8000/api/redesign \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/redesign` | POST | Main endpoint - takes URL, returns redesigned TSX |
| `/api/health` | GET | Health check endpoint |
| `/docs` | GET | Interactive Swagger UI documentation |

## Architecture Flow

```
1. User Request (URL) 
        ↓
2. Screenshot Service (Cua ComputerAgent)
   - Opens browser in sandboxed environment
   - Navigates to URL
   - Captures viewport screenshot
        ↓
3. Design Analyzer (Gemini Vision)
   - Extracts color palette, typography, layout
   - Identifies UI components
   - Suggests improvements
        ↓
4. Redesign Generator (Gemini)
   - Takes analysis + screenshot
   - Generates modern TSX component
   - Includes Tailwind CSS, responsive design, dark mode
        ↓
5. API Response
   - Original screenshot (base64)
   - Design analysis (JSON)
   - TSX code (string)
```

## Development Checkpoints

Track progress in `IMPLEMENTATION_PLAN.md`:

1. **Checkpoint 1: Screenshot Transfer** - Cua → Backend
2. **Checkpoint 2: Redesign Generation** - Gemini analysis + TSX
3. **Checkpoint 3: User Display** - API response formatting

## Code Style Guidelines

- Use type hints in Python functions
- Follow PEP 8 for Python code
- Use async/await for I/O operations
- Log important operations with `logging` module
- Handle errors with try/except and return appropriate HTTP status codes

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Cua connection timeout | Check `CUA_API_KEY` and `CUA_CONTAINER_NAME` |
| Gemini API errors | Verify `GEMINI_API_KEY`, check rate limits |
| Screenshot capture fails | Ensure Cua sandbox is running, check browser model |
| TSX extraction fails | Check Gemini response format, update regex patterns |

## Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Full redesign test
curl -X POST http://localhost:8000/api/redesign \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Important Notes

- The application uses **Cua ComputerAgent** for browser automation, NOT Playwright
- Screenshots are **viewport-only** (full-page requires browser automation libraries)
- Generated TSX is designed for **React + Tailwind CSS** projects
- All generated components are **self-contained single-file components**
