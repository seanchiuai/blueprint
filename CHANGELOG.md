# Changelog

All notable changes to the Website Redesign Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Multiple viewport captures (mobile, tablet, desktop)
- Component library integration (shadcn/ui, Radix)
- Style presets ("minimal", "playful", "corporate")
- Iterative refinement based on user feedback
- Export options (Next.js page, standalone HTML, Figma tokens)
- Download generated HTML as file
- Copy to clipboard for code

---

## [0.3.2] - 2025-12-13

### Added
- **"Open in New Tab" Button** (`index.html`)
  - Button appears in results section after successful generation
  - Opens generated HTML in new browser tab instantly
  - Uses Blob URL creation for instant preview
  - Styled with same accent color (#FF6600) as main UI
  - Located next to "GENERATED SOURCE" section header

### Changed
- **Results Display** (`index.html`)
  - Section header now includes action button
  - Generated HTML stored in `window.generatedHtmlCode` global variable
  - Button visibility controlled by generation success

### Technical Details
- Uses `Blob` API to create temporary URL from HTML string
- `window.open()` with `_blank` target for new tab
- Automatic URL cleanup with `URL.revokeObjectURL()` after 1 second
- No file download required - opens directly in browser
- Works with all generated HTML including dark mode toggle

---

## [0.3.1] - 2025-12-13

### Added
- **HTML Source Capture** (`src/services/screenshot.py`)
  - Now captures full HTML source alongside screenshots using Playwright's `page.content()`
  - Enables content-accurate redesigns by providing original text, links, and structure

- **HTML-Aware Generation** (`src/services/generator.py`)
  - Generator now receives original HTML as context
  - HTML is truncated to 50k characters to avoid token limits
  - Prompt updated to instruct Gemini to preserve real content from original

- **API Response** (`src/api/routes.py`)
  - New `original_html` field in RedesignResponse
  - Returns captured HTML source alongside screenshot

### Changed
- **Generation Prompt** (`prompts/generation_prompt.md`)
  - Added "Original HTML Source" section with `{ORIGINAL_HTML}` placeholder
  - Instructs AI to extract actual text content, links, navigation items, and semantic structure

### Technical Details
- HTML capture adds ~1-2 seconds to pipeline (negligible)
- HTML truncated at 50k characters to stay within model context limits
- Full pipeline now: Screenshot + HTML capture → Vision analysis → HTML-aware generation

---

## [0.3.0] - 2025-12-13

### Added
- **Frontend Interface** (`index.html`)
  - Complete web UI with brutalist/technical design aesthetic
  - Real-time pipeline visualization with 4 stages
  - Live system metrics (nodes processed, tokens, GPU, accuracy)
  - Terminal-style log output for debugging
  - Data visualization with animated bars
  - Fully responsive design with mobile support

- **API Integration**
  - Frontend connects to backend via `http://localhost:8000/api/redesign`
  - Real API calls replace simulated execution
  - Displays actual screenshot from backend (base64 PNG)
  - Shows live preview of generated HTML in iframe
  - Parses and displays design analysis data

- **Results Display**
  - Side-by-side comparison: original screenshot vs generated HTML
  - Syntax-highlighted code block for generated HTML
  - Live preview renders HTML in isolated iframe
  - Session statistics tracking (processed count, avg time)

- **User Experience**
  - Pre-filled with example URL (https://wikipedia.org)
  - Visual progress indicators for each pipeline stage
  - Error handling with user-friendly messages
  - Processing state with animated button
  - Automatic scroll-to-results on completion

### Technical Details
- Frontend: Vanilla JavaScript, custom CSS with grid layout
- Typography: Bebas Neue (headers), Archivo (body), Space Mono (code)
- Color scheme: Black (#0A0A0A), White (#FAFAFA), Accent (#FF6600)
- Grid overlay with 20px spacing for visual alignment
- Metrics update every 600ms during processing
- Backend runs on localhost:8000 with CORS enabled

### Fixed
- Backend startup: Changed from `python src/main.py` to `python -m uvicorn src.main:app`
- Module import errors resolved by using uvicorn module mode

---

## [0.2.0] - 2025-12-13

### Changed
- **Redesign Generator** (`src/services/generator.py`)
  - **BREAKING**: Changed output format from TSX to standalone HTML
  - Now generates complete HTML5 documents instead of React components
  - Includes Tailwind CSS via CDN (no build step required)
  - HTML files can be opened directly in a browser

- **API Response** (`src/api/routes.py`)
  - Response field renamed: `tsx_code` → `html_code`
  - HTML output is ~95 lines of complete, standalone code

- **Generation Prompt** (`prompts/generation_prompt.md`)
  - Complete rewrite focused on HTML generation
  - Simplified from design analysis prompt to code generation prompt
  - More explicit output format requirements

### Added
- Dark mode toggle button with JavaScript implementation
- Self-contained HTML with inline styles and scripts
- Tailwind CSS CDN integration
- Responsive meta viewport tags

### Technical Details
- HTML output: ~95 lines, complete DOCTYPE to </html>
- Features: Tailwind CSS, dark mode toggle, responsive design, ARIA labels
- No build tools required - HTML runs directly in browser
- Response size: ~66 KB (similar to previous TSX version)
- Generation time: ~19 seconds

---

## [0.1.1] - 2025-12-13

### Changed
- **Screenshot Service** (`src/services/screenshot.py`)
  - Replaced Cua ComputerAgent with local Playwright for browser automation
  - Removed dependency on Anthropic API (now only requires Gemini API)
  - Simplified architecture: local Chromium headless browser instead of cloud sandbox
  - Improved performance with local execution

### Added
- Playwright integration (v1.57.0)
- Chromium browser installation (playwright build v1200)
- SSL certificate configuration for Python 3.14
- Virtual environment setup documentation

### Fixed
- SSL certificate verification errors when connecting to external APIs
- Python 3.14 compatibility issues with certificate bundles

### Removed
- Cua ComputerAgent dependency for screenshot capture
- Anthropic API key requirement (Claude 3.5 Sonnet no longer needed for screenshots)
- Cua Cloud sandbox dependency

### Technical Details
- **Checkpoint 1 Completed**: Screenshot capture fully functional
  - Screenshot resolution: 2880x1800 (1440x900 @ 2x scale factor)
  - Response format: Base64-encoded PNG images
  - Test endpoint: `POST /api/screenshot` returns valid screenshots for https://example.com

- **Checkpoint 2 Completed**: Redesign generation with Gemini fully functional
  - Design analysis: 7 structured sections (color, typography, layout, components, hierarchy, style, improvements)
  - TSX generation: 49-line React component with TypeScript
  - Features: Tailwind CSS, dark mode, responsive design, accessibility (ARIA labels), animations
  - Response time: ~16 seconds for full redesign pipeline
  - Test endpoint: `POST /api/redesign` successfully processes https://example.com
  - Model: gemini-2.0-flash-exp for both vision analysis and code generation

- **Checkpoint 3 Completed**: User display format validated
  - API returns complete JSON response (62 KB)
  - Screenshot base64 decodes to valid PNG (2880x1800)
  - TSX code properly formatted and escaped
  - All response fields present: original_url, original_screenshot, analysis, tsx_code
  - Code is copy-paste ready for React projects

---

## [0.1.0] - 2024-12-13

### Added
- Initial project setup with FastAPI backend
- **Screenshot Service** (`src/services/screenshot.py`)
  - Cua ComputerAgent integration for AI-driven browser automation
  - Viewport screenshot capture
  - Scrolling and full-page capture (viewport-based)
- **Design Analyzer** (`src/services/analyzer.py`)
  - Gemini Vision integration for design analysis
  - Extracts: color palette, typography, layout, UI components
  - Generates improvement suggestions
- **Redesign Generator** (`src/services/generator.py`)
  - TSX component generation with Gemini
  - Tailwind CSS styling
  - Responsive design support
  - Dark mode support
  - Accessibility features (ARIA labels)
- **API Layer** (`src/api/routes.py`)
  - `POST /api/redesign` - Main redesign endpoint
  - `GET /api/health` - Health check endpoint
- **Configuration**
  - Environment variable support via `.env`
  - Configurable API keys and server settings
- **Documentation**
  - `README.md` - User documentation
  - `IMPLEMENTATION_PLAN.md` - Development checkpoints and progress tracking
  - `GEMINI.md` - AI assistant guidelines
  - `CHANGELOG.md` - This file

### Technical Details
- Python 3.10+ required
- FastAPI for async web framework
- Google Gemini 2.0 Flash for vision + code generation
- Cua Framework for sandboxed browser automation
- Claude 3.5 Sonnet for browser control via Cua

---

## Version History Template

When adding new versions, use the following format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
```

---

## Links

- [README](./README.md)
- [Implementation Plan](./IMPLEMENTATION_PLAN.md)
- [AI Guidelines](./GEMINI.md)
