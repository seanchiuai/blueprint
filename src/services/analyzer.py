# src/services/analyzer.py

import os
import json
import base64
import io
import logging
from PIL import Image
import google.generativeai as genai


class DesignAnalyzer:
    """Service for analyzing website designs using Google Gemini Vision."""

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
            return "Analyze this website screenshot in detail."

    async def analyze_design(self, screenshot_b64: str) -> dict:
        """
        Analyze the design of a website screenshot using Gemini Vision.

        Args:
            screenshot_b64: Base64 encoded PNG screenshot

        Returns:
            dict: Structured design analysis
        """
        self._ensure_configured()
        self.logger.info("Starting design analysis with Gemini...")

        # Convert base64 to PIL Image
        image_bytes = base64.b64decode(screenshot_b64)
        image = Image.open(io.BytesIO(image_bytes))

        # Load prompt from markdown file
        analysis_prompt = self._load_prompt("analysis_prompt.md")

        response = await self._model.generate_content_async(
            [analysis_prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )

        self.logger.info("Design analysis complete")

        # Parse JSON string to dict
        return json.loads(response.text)

