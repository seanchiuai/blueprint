# src/services/generator.py

import os
import json
import base64
import io
import re
import logging
from PIL import Image
import google.generativeai as genai


class RedesignGenerator:
    """Service for generating HTML redesigns using Google Gemini."""

    def __init__(self):
        # Lazy initialization - don't configure until first use
        self._model = None
        self.logger = logging.getLogger(__name__)

    def _ensure_configured(self):
        """Lazy initialization after env vars are loaded."""
        if self._model is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set")
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def _load_prompt(self, prompt_file: str) -> str:
        """Load prompt from markdown file."""
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "prompts",
            prompt_file,
        )
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Remove the title if it exists (first line starting with #)
                lines = content.split("\n")
                if lines and lines[0].startswith("#"):
                    return "\n".join(lines[1:]).strip()
                return content.strip()
        except FileNotFoundError:
            self.logger.warning(
                f"Prompt file {prompt_file} not found, using fallback prompt"
            )
            # Fallback to a basic prompt if file not found
            return "Generate a modern TSX component."

    async def generate_redesign(
        self,
        analysis: dict,
        screenshot_b64: str,
        style_preferences: dict | None = None,
    ) -> str:
        """
        Generate a redesigned HTML page based on analysis and screenshot.

        Args:
            analysis: Design analysis from DesignAnalyzer
            screenshot_b64: Original screenshot for reference
            style_preferences: Optional user preferences for the redesign

        Returns:
            str: Complete standalone HTML code
        """
        self._ensure_configured()
        self.logger.info("Starting HTML redesign generation...")

        image_bytes = base64.b64decode(screenshot_b64)
        image = Image.open(io.BytesIO(image_bytes))

        # Load prompt template from markdown file
        prompt_template = self._load_prompt("generation_prompt.md")

        # Build style section from preferences if provided
        style_section = ""
        if style_preferences:
            style_section = f"""
## User Style Preferences:
{json.dumps(style_preferences, indent=2)}

Please incorporate these preferences into the redesign. Priority should be given to:
- Color scheme: {style_preferences.get('color_scheme', 'not specified')}
- Style: {style_preferences.get('style', 'not specified')}
- Any additional notes: {style_preferences.get('notes', 'none')}
"""

        # Replace placeholders in the prompt template
        prompt = prompt_template.replace(
            "{ANALYSIS_JSON}", json.dumps(analysis, indent=2)
        ).replace("{STYLE_PREFERENCES}", style_section)

        response = await self._model.generate_content_async(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                temperature=0.7, max_output_tokens=8192
            ),
        )

        # Extract HTML code from response
        html_code = self._extract_code(response.text)
        self.logger.info("HTML redesign generation complete")
        return html_code

    def _extract_code(self, response_text: str) -> str:
        """Extract HTML code from markdown code blocks."""
        # Match ```tsx or ```typescript or ``` code blocks
        pattern = r"```(?:html)?\n([\s\S]*?)```"
        matches = re.findall(pattern, response_text)

        if matches:
            return matches[0].strip()

        # If no code block found, return the whole response
        return response_text.strip()

