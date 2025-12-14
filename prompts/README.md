# Prompts Directory

This directory contains the Gemini AI prompts used by the Website Redesign Agent.

## Files

### `analysis_prompt.md`
The prompt used to analyze website screenshots and extract design information.

**Used by:** `src/services/analyzer.py`

**Output:** JSON structure with color palette, typography, layout, UI components, visual hierarchy, design style, and improvement suggestions.

### `generation_prompt.md`
The prompt used to generate the redesigned TSX component based on the analysis.

**Used by:** `src/services/generator.py`

**Output:** Complete TSX/React component with Tailwind CSS styling.

**Placeholders:**
- `{ANALYSIS_JSON}` - Replaced with the JSON output from the analysis step
- `{STYLE_PREFERENCES}` - Replaced with user-provided style preferences (if any)

## How to Edit

1. Edit the markdown files directly to modify the prompts
2. The Python services will automatically load the updated prompts
3. Restart the server to apply changes

## Tips for Editing

- Be specific about what you want the AI to analyze or generate
- Use clear section headers and bullet points
- Include examples when helpful
- Specify output format requirements clearly
- Test changes with a sample website to verify results
