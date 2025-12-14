# Website Redesign Agent - Implementation Plan

## Overview

A backend-focused application that takes a screenshot of a user-provided website, analyzes the landing page design, and generates a "10x better" redesigned version in TSX using AI.

**Tech Stack:**
- **Cua (C/UA)** - Computer-Using Agent framework for sandboxed browser automation and screenshots
- **Google Gemini** - Vision + code generation for redesign
- **Node.js/Python** - Backend API

---

## Progress Tracking

### Current Status

| Phase | Status | Started | Completed | Notes |
|-------|--------|---------|-----------|-------|
| Phase 1: Project Setup | ✅ Complete | 2024-12-13 | 2024-12-13 | Dependencies and env configured |
| Phase 2: Screenshot Service | 🔄 In Progress | - | - | Cua integration pending |
| Phase 3: Design Analysis | ⏳ Not Started | - | - | - |
| Phase 4: TSX Generator | ⏳ Not Started | - | - | - |
| Phase 5: API Layer | 🔄 In Progress | 2024-12-13 | - | Routes defined, testing needed |
| Phase 6: Testing & Deployment | ⏳ Not Started | - | - | - |

### Status Legend
- ✅ Complete
- 🔄 In Progress
- ⏳ Not Started
- ❌ Blocked

---

## Error Log

Track errors encountered during development for debugging and future reference.

| Date | Error | Location | Cause | Resolution | Status |
|------|-------|----------|-------|------------|--------|
| - | - | - | - | - | - |

### Error Template
When adding new errors, use the following format:
```
| YYYY-MM-DD | Brief error description | File/function | Root cause | How it was fixed | ✅/🔄/❌ |
```

---

## Implementation Notes

### Key Decisions
- Using Cua ComputerAgent instead of Playwright for browser automation (sandboxed, AI-driven)
- Using Gemini 2.0 Flash for both vision analysis and code generation
- Viewport-only screenshots (full-page requires different approach)
- Single-file TSX component output for simplicity

### Known Limitations
- Screenshots are viewport-only (no true full-page capture without browser automation libraries)
- Cua requires cloud sandbox container
- Generated TSX assumes React + Tailwind CSS setup

### Testing Checklist
- [ ] Environment variables configured (.env file)
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] Screenshot service connects to Cua
- [ ] Gemini API key validated
- [ ] Full redesign pipeline works end-to-end

---

## Development Checkpoints

Before proceeding to the next phase, each checkpoint must be verified and working.

### Checkpoint 1: Screenshot Transfer (Cua → Backend)
**Goal:** Successfully capture and transfer screenshots from Cua sandbox to the backend.

| Task | Description | Verification |
|------|-------------|--------------|
| 1.1 | Set up Cua Cloud connection | Can connect to sandbox without errors |
| 1.2 | Initialize ComputerAgent | Agent created with browser model |
| 1.3 | Navigate to test URL | Agent opens browser and loads page |
| 1.4 | Capture viewport screenshot | Returns valid base64 PNG data |
| 1.5 | Capture scrolled screenshot | Returns valid base64 PNG data |
| 1.6 | Transfer to backend | Screenshots saved/accessible in backend memory |

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Should return: { "viewport": "base64...", "full_page": "base64..." }
```

**Success Criteria:**
- [ ] Screenshots are captured without timeout
- [ ] Base64 data can be decoded back to valid PNG
- [ ] Both viewport and full-page screenshots are distinct

---

### Checkpoint 2: Redesign Generation (Gemini)
**Goal:** Generate a complete, valid TSX component from the screenshot.

| Task | Description | Verification |
|------|-------------|--------------|
| 2.1 | Connect to Gemini API | API key validated, model accessible |
| 2.2 | Send screenshot to Gemini Vision | No errors, receives response |
| 2.3 | Parse design analysis | Valid JSON with all required fields |
| 2.4 | Generate TSX code | Returns syntactically valid TSX |
| 2.5 | Extract code from response | Code block properly parsed |

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/redesign \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Should return: { "tsx_code": "import React...", "analysis": {...} }
```

**Success Criteria:**
- [ ] Gemini returns structured analysis JSON
- [ ] TSX code includes all required imports
- [ ] TSX code uses Tailwind CSS classes
- [ ] TSX code compiles without TypeScript errors
- [ ] Component is self-contained and exportable

---

### Checkpoint 3: User Display
**Goal:** Present the redesigned component to the user in a viewable format.

| Task | Description | Verification |
|------|-------------|--------------|
| 3.1 | Return TSX via API | Response includes formatted code |
| 3.2 | Side-by-side comparison | Original screenshot + new code visible |
| 3.3 | Code syntax highlighting | TSX is readable with proper formatting |
| 3.4 | Copy-to-clipboard | User can copy the generated code |
| 3.5 | Live preview (optional) | Render TSX in sandboxed iframe |

**API Response Format:**
```json
{
  "original_url": "https://example.com",
  "original_screenshot": "data:image/png;base64,...",
  "analysis": {
    "color_palette": {...},
    "typography": {...},
    "improvements": [...]
  },
  "tsx_code": "import React from 'react';\n\nexport default function LandingPage() {...}",
  "preview_url": "/preview/abc123"  // optional: live preview link
}
```

**Success Criteria:**
- [ ] API returns complete response with all fields
- [ ] Screenshot is viewable as image
- [ ] TSX code is properly escaped/formatted
- [ ] User can copy and paste code into their project
- [ ] (Optional) Live preview renders correctly

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Backend API (Python/FastAPI)         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌───────────────┐  │
│  │   Input     │ → │  Screenshot │ → │   Redesign    │  │
│  │   Handler   │   │   Service   │   │   Generator   │  │
│  └─────────────┘   └─────────────┘   └───────────────┘  │
│         │                │                   │          │
│         ▼                ▼                   ▼          │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Cua ComputerAgent                      ││
│  │  • AI-driven browser control (no Playwright)        ││
│  │  • Desktop screenshot capture                               ││
│  └─────────────────────────────────────────────────────┘│
│                          │                              │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Google Gemini API                      ││
│  │  • Vision analysis of screenshots                   ││
│  │  • TSX code generation                              ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

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
├── requirements.txt
├── .env.example
├── .env
└── README.md
```

---

## Phase 1: Project Setup

### 1.1 Dependencies (requirements.txt)

```txt
fastapi>=0.104.0
uvicorn>=0.24.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
pydantic>=2.5.0
httpx>=0.25.0
pillow>=10.0.0
tenacity>=8.2.0

# Cua Framework
cua-computer[all]
cua-agent[all]
```

### 1.2 Environment Variables (.env.example)

```env
# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Cua Cloud
CUA_API_KEY=your-cua-api-key
CUA_CONTAINER_NAME=your-container-name

# Browser Control Model (for ComputerAgent)
# This model controls the browser to navigate and capture screenshots
CUA_BROWSER_MODEL=anthropic/claude-3-5-sonnet-20241022

# Server
PORT=8000
HOST=0.0.0.0
```

---

## Phase 2: Screenshot Service

### 2.1 Using Cua ComputerAgent

Uses an AI model (Claude/GPT) to control the browser through desktop automation - no Playwright required.

```python
# src/services/screenshot.py

import os
import base64
import logging
from computer import Computer, VMProviderType
from agent import ComputerAgent

class ScreenshotService:
    """Service for capturing website screenshots using Cua ComputerAgent."""

    def __init__(self):
        self.api_key = os.getenv("CUA_API_KEY")
        self.container_name = os.getenv("CUA_CONTAINER_NAME")
        # Model for browser control (Claude or GPT)
        self.browser_model = os.getenv(
            "CUA_BROWSER_MODEL", "anthropic/claude-3-5-sonnet-20241022"
        )
        self.logger = logging.getLogger(__name__)

    async def capture_website(self, url: str) -> dict:
        """
        Capture screenshots using ComputerAgent to control browser.
        No Playwright - uses AI to navigate the desktop browser.

        Args:
            url: The website URL to capture

        Returns:
            dict: Contains 'viewport' and 'full_page' base64 encoded screenshots
        """
        self.logger.info(f"Starting screenshot capture for: {url}")

        async with Computer(
            os_type="linux",
            provider_type=VMProviderType.CLOUD,
            name=self.container_name,
            api_key=self.api_key,
        ) as computer:
            # Create agent to control the browser
            agent = ComputerAgent(
                model=self.browser_model,
                tools=[computer],
                max_trajectory_budget=2.0,  # Limit spend per screenshot
                verbosity=logging.INFO,
            )

            # Step 1: Open browser and navigate to URL
            navigate_task = f"""
            Open Firefox browser and navigate to {url}.
            Wait for the page to fully load (wait 3 seconds after page appears loaded).
            Do NOT interact with any popups or consent banners - just let them be visible.
            Once the page is loaded, stop and report success.
            """

            self.logger.info("Navigating to URL with ComputerAgent...")
            async for result in agent.run(
                [{"role": "user", "content": navigate_task}]
            ):
                # Agent is navigating...
                pass

            # Step 2: Capture viewport screenshot via computer interface
            self.logger.info("Capturing viewport screenshot...")
            viewport_bytes = await computer.interface.screenshot()
            viewport_b64 = base64.b64encode(viewport_bytes).decode("utf-8")

            # Step 3: Scroll down and capture more (simulated full page)
            scroll_task = """
            Scroll down to the bottom of the page slowly, then scroll back to the top.
            """
            self.logger.info("Scrolling page...")
            async for _ in agent.run([{"role": "user", "content": scroll_task}]):
                pass

            # Capture again at top (viewport-only, true full-page not available without Playwright)
            self.logger.info("Capturing full page screenshot...")
            full_page_bytes = await computer.interface.screenshot()
            full_page_b64 = base64.b64encode(full_page_bytes).decode("utf-8")

            self.logger.info("Screenshot capture complete")
            return {
                "viewport": viewport_b64,
                "full_page": full_page_b64,
                "url": url,
            }
```

**Note:** The ComputerAgent approach captures viewport screenshots only. True full-page screenshots require browser automation libraries.

---

## Phase 3: Design Analysis with Gemini

```python
# src/services/analyzer.py

import os
import google.generativeai as genai
from PIL import Image
import base64
import io

class DesignAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    async def analyze_design(self, screenshot_b64: str) -> dict:
        """
        Analyze the design of a website screenshot using Gemini Vision.

        Args:
            screenshot_b64: Base64 encoded PNG screenshot

        Returns:
            dict: Structured design analysis
        """
        # Convert base64 to PIL Image
        image_bytes = base64.b64decode(screenshot_b64)
        image = Image.open(io.BytesIO(image_bytes))

        analysis_prompt = """
        Analyze this website screenshot in detail. Provide a structured analysis:

        ## 1. Color Palette
        - Primary color (hex)
        - Secondary colors (hex)
        - Accent colors (hex)
        - Background colors
        - Text colors

        ## 2. Typography
        - Heading style (size, weight, font-family guess)
        - Body text style
        - Font hierarchy observations

        ## 3. Layout Structure
        - Grid system (columns, gutters)
        - Section breakdown (header, hero, features, footer, etc.)
        - Spacing patterns (margins, padding)
        - Responsive considerations visible

        ## 4. UI Components
        - Navigation style
        - Buttons (style, colors, shapes)
        - Cards or containers
        - Forms or inputs
        - Icons and imagery

        ## 5. Visual Hierarchy
        - Primary focal point
        - Secondary elements
        - Call-to-action placement

        ## 6. Design Style
        - Overall aesthetic (minimal, corporate, playful, luxury, etc.)
        - Design era/trend

        ## 7. Areas for Improvement
        - List 5-7 specific improvements that would make this design better
        - Focus on: accessibility, modern trends, visual appeal, UX

        Respond in JSON format with these sections as keys.
        """

        response = await self.model.generate_content_async(
            [analysis_prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        return response.text
```

---

## Phase 4: TSX Redesign Generator with Gemini

```python
# src/services/generator.py

import os
import google.generativeai as genai
from PIL import Image
import base64
import io
import re

class RedesignGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Use Gemini Pro for complex code generation
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    async def generate_redesign(
        self,
        analysis: dict,
        screenshot_b64: str,
        style_preferences: dict = None
    ) -> str:
        """
        Generate a redesigned TSX component based on analysis and screenshot.

        Args:
            analysis: Design analysis from DesignAnalyzer
            screenshot_b64: Original screenshot for reference
            style_preferences: Optional user preferences

        Returns:
            str: Complete TSX component code
        """
        image_bytes = base64.b64decode(screenshot_b64)
        image = Image.open(io.BytesIO(image_bytes))

        prompt = f"""
        You are an expert UI/UX designer and React developer. Based on the original
        website screenshot and design analysis, create a DRAMATICALLY improved
        redesign as a TSX component.

        ## Original Design Analysis:
        {analysis}

        ## Your Task:
        Create a modern, beautiful, production-ready TSX landing page component that:

        1. **Keeps the same general purpose/content** as the original
        2. **Dramatically improves** the visual design with:
           - Modern, clean aesthetic
           - Better visual hierarchy
           - Improved spacing and breathing room
           - Contemporary color palette (can deviate from original)
           - Smooth micro-interactions and hover effects

        3. **Technical Requirements:**
           - Use React functional component with TypeScript
           - Use Tailwind CSS for all styling (no external CSS)
           - Make it fully responsive (mobile-first)
           - Include dark mode support with `dark:` variants
           - Use semantic HTML elements
           - Add ARIA labels for accessibility
           - Include subtle animations with Tailwind's animation classes

        4. **Component Structure:**
           - Self-contained single file component
           - Mock any dynamic data as constants at the top
           - Include all necessary imports
           - Export as default

        5. **Design Principles to Apply:**
           - Generous whitespace
           - Clear typography hierarchy (use Tailwind's prose or custom)
           - Subtle shadows and depth
           - Rounded corners where appropriate
           - Gradient accents (subtle, not overwhelming)
           - Modern button and card styles
           - Smooth transitions on interactive elements

        ## Output Format:
        Return ONLY the TSX code wrapped in a code block. No explanations before or after.
        The component should be named `LandingPage`.

        ```tsx
        // Your complete component here
        ```
        """

        response = await self.model.generate_content_async(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8192
            )
        )

        # Extract TSX code from response
        tsx_code = self._extract_code(response.text)
        return tsx_code

    def _extract_code(self, response_text: str) -> str:
        """Extract TSX code from markdown code blocks."""
        # Match ```tsx or ```typescript or ``` code blocks
        pattern = r"```(?:tsx|typescript|jsx|javascript)?\n([\s\S]*?)```"
        matches = re.findall(pattern, response_text)

        if matches:
            return matches[0].strip()

        # If no code block found, return the whole response
        return response_text.strip()
```

---

## Phase 5: API Layer

```python
# src/api/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import logging

from src.services.screenshot import ScreenshotService
# Or use: from src.services.screenshot_local import LocalScreenshotService
from src.services.analyzer import DesignAnalyzer
from src.services.generator import RedesignGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
screenshot_service = ScreenshotService()
analyzer = DesignAnalyzer()
generator = RedesignGenerator()


class RedesignRequest(BaseModel):
    url: HttpUrl
    style_preferences: Optional[dict] = None


class RedesignResponse(BaseModel):
    original_url: str
    original_screenshot: str  # base64
    analysis: dict
    tsx_code: str


@router.post("/redesign", response_model=RedesignResponse)
async def redesign_website(request: RedesignRequest):
    """
    Main endpoint: Takes a URL and returns a redesigned TSX component.
    """
    try:
        logger.info(f"Starting redesign for: {request.url}")

        # Step 1: Capture screenshots
        logger.info("Capturing screenshots...")
        screenshots = await screenshot_service.capture_website(str(request.url))

        # Step 2: Analyze design
        logger.info("Analyzing design...")
        analysis = await analyzer.analyze_design(screenshots["viewport"])

        # Step 3: Generate redesign
        logger.info("Generating TSX redesign...")
        tsx_code = await generator.generate_redesign(
            analysis=analysis,
            screenshot_b64=screenshots["full_page"],
            style_preferences=request.style_preferences
        )

        logger.info("Redesign complete!")

        return RedesignResponse(
            original_url=str(request.url),
            original_screenshot=screenshots["viewport"],
            analysis=analysis,
            tsx_code=tsx_code
        )

    except Exception as e:
        logger.error(f"Redesign failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

```python
# src/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.api.routes import router

load_dotenv()

app = FastAPI(
    title="Website Redesign Agent",
    description="AI-powered website redesign generator using Gemini",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
```

---

## Phase 6: Running the Application

### 6.1 Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### 6.2 Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 6.3 Run the Server

```bash
python -m src.main
# Or
uvicorn src.main:app --reload
```

### 6.4 Test the API

```bash
curl -X POST http://localhost:8000/api/redesign \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## API Reference

### POST /api/redesign

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
  "original_screenshot": "base64-encoded-png...",
  "analysis": {
    "color_palette": {...},
    "typography": {...},
    "layout": {...},
    "improvements": [...]
  },
  "tsx_code": "import React from 'react';\n\nexport default function LandingPage() {...}"
}
```

---

## Key Gemini Models Used

| Model | Purpose |
|-------|---------|
| `gemini-2.0-flash-exp` | Vision analysis + code generation (fast, capable) |
| `gemini-1.5-pro` | Alternative for complex analysis (more capable, slower) |

---

## Future Enhancements

1. **Multiple viewport captures** - Mobile, tablet, desktop screenshots
2. **Component library integration** - Generate with shadcn/ui, Radix, etc.
3. **Style presets** - "Make it more minimal", "Make it more playful"
4. **Iterative refinement** - Allow users to request changes
5. **A/B comparison view** - Side-by-side original vs redesign
6. **Export options** - Next.js page, standalone HTML, Figma design tokens
