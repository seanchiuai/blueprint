# src/services/screenshot.py

import os
import base64
import logging
from playwright.async_api import async_playwright


class ScreenshotService:
    """Service for capturing website screenshots using local Playwright."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def capture_website(self, url: str) -> dict:
        """
        Capture screenshots using Playwright browser automation.

        Args:
            url: The website URL to capture

        Returns:
            dict: Contains 'viewport' and 'full_page' base64 encoded screenshots
        """
        self.logger.info(f"Starting screenshot capture for: {url}")

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)

            # Create page with viewport settings
            page = await browser.new_page(
                viewport={"width": 1440, "height": 900},
                device_scale_factor=2  # Retina quality
            )

            self.logger.info("Opening browser and navigating to URL...")

            # Navigate to URL and wait for page to load
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for any lazy-loaded content
            await page.wait_for_timeout(2000)

            # Capture viewport screenshot (above-the-fold)
            self.logger.info("Capturing viewport screenshot...")
            viewport_screenshot = await page.screenshot(type="png")
            viewport_b64 = base64.b64encode(viewport_screenshot).decode("utf-8")

            # Capture full page screenshot
            self.logger.info("Capturing full page screenshot...")
            full_page_screenshot = await page.screenshot(full_page=True, type="png")
            full_page_b64 = base64.b64encode(full_page_screenshot).decode("utf-8")

            await page.close()
            await browser.close()

            self.logger.info("Screenshot capture complete")
            return {
                "viewport": viewport_b64,
                "full_page": full_page_b64,
                "url": url,
            }

