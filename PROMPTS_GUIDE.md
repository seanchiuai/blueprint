# Prompts Guide

## Overview

The Gemini AI prompts have been externalized into markdown files for easy editing. You can now modify the prompts without touching the Python code!

## Location

All prompts are stored in the `/prompts` directory:

```
prompts/
├── README.md                  # Documentation about the prompts
├── analysis_prompt.md         # Design analysis prompt
└── generation_prompt.md       # TSX generation prompt
```

## How It Works

### 1. Analysis Prompt (`analysis_prompt.md`)
- **Used by:** `src/services/analyzer.py`
- **Purpose:** Analyzes website screenshots to extract design information
- **Output:** JSON with color palette, typography, layout, UI components, etc.

### 2. Generation Prompt (`generation_prompt.md`)
- **Used by:** `src/services/generator.py`
- **Purpose:** Generates redesigned TSX components
- **Output:** Complete React/TSX component with Tailwind CSS
- **Placeholders:**
  - `{ANALYSIS_JSON}` - Replaced with analysis results
  - `{STYLE_PREFERENCES}` - Replaced with user preferences

## How to Edit Prompts

### Step 1: Edit the Markdown File
Open the prompt file you want to modify:

```bash
# For analysis prompt
code prompts/analysis_prompt.md

# For generation prompt
code prompts/generation_prompt.md
```

### Step 2: Make Your Changes
Edit the prompt text directly. You can:
- Add new sections
- Modify existing instructions
- Change the output format requirements
- Add specific design guidelines
- Adjust the tone or style

### Step 3: Save and Restart
1. Save the markdown file
2. Restart the FastAPI server (Ctrl+C then `python -m src.main`)
3. The new prompts will be loaded automatically

## Example: Customizing the Generation Prompt

Let's say you want to add a requirement for animations:

**Before:**
```markdown
5. **Design Principles to Apply:**
   - Generous whitespace
   - Clear typography hierarchy
```

**After:**
```markdown
5. **Design Principles to Apply:**
   - Generous whitespace
   - Clear typography hierarchy
   - Add smooth scroll animations
   - Include loading states for all interactive elements
```

## Tips for Effective Prompts

### Be Specific
❌ "Make it look good"
✅ "Use a modern color palette with high contrast ratios (WCAG AA compliant)"

### Use Structure
- Break down complex requirements into numbered lists
- Use headers to organize sections
- Include examples when helpful

### Specify Output Format
Always be clear about:
- What format you want (JSON, code, etc.)
- What should be included/excluded
- Any specific naming conventions

### Test Your Changes
After editing a prompt:
1. Test with a simple website (like Wikipedia)
2. Check if the output matches your expectations
3. Iterate and refine

## Fallback Behavior

If a prompt file is not found or can't be loaded:
- The system will log a warning
- A basic fallback prompt will be used
- The service will continue to function

## Advanced: Dynamic Placeholders

The generation prompt supports these placeholders:

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{ANALYSIS_JSON}` | Design analysis results | `{"Color Palette": {...}}` |
| `{STYLE_PREFERENCES}` | User style preferences | `{"theme": "modern"}` |

These are automatically replaced at runtime by the Python service.

## Troubleshooting

### Prompt not updating?
- Make sure you saved the file
- Restart the server
- Check the logs for any warnings

### Getting unexpected results?
- Review the prompt for clarity
- Test with multiple websites
- Check if placeholders are being replaced correctly

### Server won't start?
- Check if the prompts directory exists
- Verify file permissions
- Look for syntax errors in the markdown

## Need Help?

- Check `prompts/README.md` for quick reference
- Review the Python services to see how prompts are loaded
- Test changes incrementally
