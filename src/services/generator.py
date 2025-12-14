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
            self._model = genai.GenerativeModel("gemini-3-pro-preview")

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
        original_html: str,
        style_preferences: dict | None = None,
    ) -> str:
        """
        Generate a redesigned HTML page based on analysis, screenshot, and original HTML.

        Args:
            analysis: Design analysis from DesignAnalyzer
            screenshot_b64: Original screenshot for reference
            original_html: Original HTML source from the webpage
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
        # Note: We no longer pass original HTML to avoid confusion - rely on screenshot
        prompt = prompt_template.replace(
            "{ANALYSIS_JSON}", json.dumps(analysis, indent=2)
        ).replace("{STYLE_PREFERENCES}", style_section)

        response = await self._model.generate_content_async(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                temperature=0.7, max_output_tokens=32768
            ),
        )

        # Log response metadata for debugging
        self.logger.info("Gemini response received")
        if response.candidates:
            self.logger.info(
                f"Response finish_reason: {response.candidates[0].finish_reason}"
            )
            if response.candidates[0].finish_reason == "MAX_TOKENS":
                self.logger.error("Response was TRUNCATED due to max_tokens limit!")

        # Log response preview for debugging
        response_text = response.text
        self.logger.info(
            f"Response preview (first 300 chars): {response_text[:300]}"
        )
        self.logger.info(f"Response preview (last 200 chars): {response_text[-200:]}")
        self.logger.info(f"Total response length: {len(response_text)} characters")

        # Extract HTML code from response
        html_code = self._extract_code(response_text)

        # Final validation
        if not html_code or len(html_code) < 100:
            self.logger.error(
                f"Extracted HTML is suspiciously short: {len(html_code)} chars"
            )
            raise ValueError(
                f"Generated HTML is invalid or too short ({len(html_code)} chars)"
            )

        self.logger.info("HTML redesign generation complete")
        return html_code

    def _extract_code(self, response_text: str) -> str:
        """
        Extract HTML code from markdown code blocks with robust fallback strategies.
        """
        self.logger.info(f"Extracting HTML from response ({len(response_text)} chars)")

        # STRATEGY 0: Direct cleanup - most reliable approach
        # Simply strip markdown code block markers from start and end
        cleaned = response_text.strip()

        # Remove opening code fence: ```html, ```HTML, or just ```
        # Handle: ```html\n, ```html , ```html<!DOCTYPE, etc.
        cleaned = re.sub(r"^```(?:html|HTML)?\s*", "", cleaned, flags=re.IGNORECASE)

        # Remove closing code fence: ``` at the end (with optional whitespace)
        cleaned = re.sub(r"\s*```\s*$", "", cleaned)

        # Also handle case where there might be text after closing ```
        # Find last occurrence of ``` and remove everything from there if it looks like end marker
        last_fence_match = re.search(r"\n```\s*(?:\n.*)?$", cleaned)
        if last_fence_match:
            cleaned = cleaned[: last_fence_match.start()]

        cleaned = cleaned.strip()

        if cleaned and self._validate_html(cleaned):
            self.logger.info(
                f"Strategy 0 (direct cleanup) succeeded: {len(cleaned)} chars"
            )
            return cleaned

        # STRATEGY 1: Regex pattern matching for well-formed code blocks
        patterns = [
            r"```html\s*\n([\s\S]*?)```",  # ```html\n with newline
            r"```html\s+([\s\S]*?)```",  # ```html with space(s)
            r"```html([\s\S]*?)```",  # ```html with no separator
            r"```\s*\n([\s\S]*?)```",  # ``` with newline (no lang tag)
            r"```([\s\S]*?)```",  # ``` with anything
        ]

        for i, pattern in enumerate(patterns, 1):
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            if matches:
                extracted = matches[0].strip()
                self.logger.info(f"Pattern {i} matched: {len(extracted)} chars")

                if self._validate_html(extracted):
                    self.logger.info(f"Strategy 1 pattern {i} succeeded")
                    return extracted

        # STRATEGY 2: Handle truncated responses (no closing ```)
        if "```" in response_text:
            self.logger.warning("Trying truncated response extraction")
            # Find opening fence and take everything after it
            opening_match = re.search(r"```(?:html|HTML)?\s*", response_text)
            if opening_match:
                partial = response_text[opening_match.end() :].strip()
                # Remove any trailing ``` if present
                partial = re.sub(r"\s*```\s*$", "", partial).strip()
                if self._validate_html(partial):
                    self.logger.info(
                        f"Strategy 2 (truncated) succeeded: {len(partial)} chars"
                    )
                    return partial

        # STRATEGY 3: Response is raw HTML without code fences
        if response_text.strip().lower().startswith(
            "<!doctype"
        ) or response_text.strip().lower().startswith("<html"):
            self.logger.info("Strategy 3: Response is raw HTML")
            return response_text.strip()

        # FINAL FALLBACK: Return cleaned version even if validation failed
        # This ensures we at least try to show something
        self.logger.error(f"All strategies failed! Response preview: {response_text[:300]}")

        # Last attempt: just return whatever we cleaned, validation be damned
        if cleaned and "<!doctype" in cleaned.lower():
            self.logger.warning("Returning cleaned response despite validation failure")
            return cleaned

        return response_text.strip()

    def _validate_html(self, code: str) -> bool:
        """
        Validate that extracted code looks like valid HTML.
        Simple validation: must look like HTML and not have markdown fences.
        """
        if not code or len(code) < 50:
            return False

        code_stripped = code.strip()
        code_lower = code_stripped.lower()

        # Must NOT start with markdown code fence
        if code_stripped.startswith("```"):
            self.logger.warning("Validation failed: starts with code fence")
            return False

        # Should contain HTML markers
        has_doctype = "<!doctype" in code_lower
        has_html_tag = "<html" in code_lower

        # At minimum, should have doctype or html tag
        if not (has_doctype or has_html_tag):
            self.logger.warning("Validation failed: no DOCTYPE or html tag found")
            return False

        # Should not have code fences anywhere prominent
        if code_lower.startswith("html\n") or code_lower.startswith("html "):
            self.logger.warning("Validation failed: starts with 'html' language tag")
            return False

        return True

