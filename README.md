# Website Redesign Agent

An AI-powered backend application that analyzes website screenshots and generates dramatically improved redesigns as production-ready TSX components.

## Overview

This tool takes a screenshot of any website's landing page and uses AI to generate a "10x better" redesigned version in TSX with modern design principles, responsive layouts, and Tailwind CSS styling.

## Features

- **Automated Screenshot Capture**: Uses Cua ComputerAgent for AI-driven browser automation
- **AI Design Analysis**: Leverages Google Gemini Vision to analyze design elements, color palettes, typography, and layout
- **Intelligent Redesign**: Generates production-ready TSX components with:
  - Modern, clean aesthetics
  - Tailwind CSS styling
  - Responsive design (mobile-first)
  - Dark mode support
  - Accessibility features (ARIA labels, semantic HTML)
  - Smooth animations and transitions

## Tech Stack

- **Backend**: Python, FastAPI
- **AI Models**:
  - Google Gemini 2.0 Flash (vision analysis + code generation)
  - Claude 3.5 Sonnet (browser automation via Cua)
- **Browser Automation**: Cua Framework (ComputerAgent)
- **Styling**: Tailwind CSS (in generated components)

## Prerequisites

- Python 3.10+
- Google Gemini API key
- Cua Cloud API key and container

## Installation

### 1. Clone the repository
```bash
cd redesign
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Cua Cloud
CUA_API_KEY=your-cua-api-key
CUA_CONTAINER_NAME=your-container-name

# Browser Control Model (for ComputerAgent)
CUA_BROWSER_MODEL=anthropic/claude-3-5-sonnet-20241022

# Server
PORT=8000
HOST=0.0.0.0
```

## Usage

### Start the server
```bash
# Option 1: Using Python module
python -m src.main

# Option 2: Using Uvicorn directly
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

### Make a redesign request
```bash
curl -X POST http://localhost:8000/api/redesign \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## API Reference

### POST /api/redesign

Generate a redesigned TSX component from a website URL.

**Request Body:**
```json
{
  "url": "https://example.com",
  "style_preferences": {
    "color_scheme": "dark",
    "style": "minimal"
  }
}
```

**Response:**
```json
{
  "original_url": "https://example.com",
  "original_screenshot": "data:image/png;base64,...",
  "analysis": {
    "color_palette": {
      "primary": "#FF5733",
      "secondary": ["#C70039", "#900C3F"],
      "background": "#FFFFFF"
    },
    "typography": {
      "heading": "Large, bold sans-serif",
      "body": "Medium weight, readable"
    },
    "layout": {
      "grid": "12-column",
      "sections": ["header", "hero", "features", "footer"]
    },
    "improvements": [
      "Increase whitespace for better readability",
      "Modernize color palette",
      "Add subtle animations"
    ]
  },
  "tsx_code": "import React from 'react';\n\nexport default function LandingPage() {\n  return (\n    <div className=\"min-h-screen bg-white\">\n      ...\n    </div>\n  );\n}"
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Project Structure

```
redesign/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # FastAPI routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── screenshot.py       # Cua screenshot service
│   │   ├── analyzer.py         # Design analysis with Gemini
│   │   └── generator.py        # TSX generation with Gemini
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Environment config
│   └── main.py                 # Application entry point
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (not in git)
├── IMPLEMENTATION_PLAN.md    # Detailed implementation plan
└── README.md                  # This file
```

## How It Works

1. **Screenshot Capture**: ComputerAgent uses AI to control a browser in a sandboxed environment, navigates to the provided URL, and captures screenshots
2. **Design Analysis**: Gemini Vision analyzes the screenshot to extract:
   - Color palette
   - Typography
   - Layout structure
   - UI components
   - Visual hierarchy
   - Areas for improvement
3. **Redesign Generation**: Gemini generates a modern TSX component that:
   - Maintains the original content and purpose
   - Dramatically improves visual design
   - Implements modern UX best practices
   - Uses Tailwind CSS for all styling
   - Includes responsive and dark mode support

## Development Checkpoints

The project is structured around three main checkpoints:

1. **Screenshot Transfer**: Capture and transfer screenshots from Cua sandbox to backend
2. **Redesign Generation**: Generate valid TSX components from screenshots using Gemini
3. **User Display**: Present the redesigned component in a viewable format

See `IMPLEMENTATION_PLAN.md` for detailed checkpoint criteria.

## Future Enhancements

- Multiple viewport captures (mobile, tablet, desktop)
- Component library integration (shadcn/ui, Radix)
- Style presets ("minimal", "playful", "corporate")
- Iterative refinement based on user feedback
- A/B comparison view
- Export options (Next.js page, standalone HTML, Figma tokens)

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues or questions, please open an issue on the repository.
