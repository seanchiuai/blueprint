# src/api/routes.py

import ipaddress
import logging
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, field_validator

router = APIRouter()
logger = logging.getLogger(__name__)

# Lazy service initialization - services will be created on first request
_services: tuple | None = None


def get_services():
    """
    Lazy initialization of services to ensure environment variables
    are loaded before service instantiation.
    """
    global _services
    if _services is None:
        from src.services.screenshot import ScreenshotService
        from src.services.analyzer import DesignAnalyzer
        from src.services.generator import RedesignGenerator

        _services = (ScreenshotService(), DesignAnalyzer(), RedesignGenerator())
    return _services


class RedesignRequest(BaseModel):
    """Request model for website redesign endpoint."""

    url: HttpUrl
    style_preferences: dict | None = None

    @field_validator("url")
    @classmethod
    def validate_safe_url(cls, v):
        """
        Validate URL to prevent SSRF attacks.
        Blocks internal/private URLs and requires HTTPS.
        """
        parsed = urlparse(str(v))
        hostname = parsed.hostname

        # Block common internal hostnames
        blocked_hosts = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "169.254.169.254",  # AWS metadata
            "metadata.google.internal",  # GCP metadata
            "169.254.169.253",  # Azure metadata
        ]
        if hostname in blocked_hosts:
            raise ValueError("Internal URLs are not allowed")

        # Block private IP ranges
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise ValueError("Private/internal IP addresses are not allowed")
        except ValueError:
            # Not an IP address, that's fine (it's a domain name)
            pass

        # Require HTTPS for external URLs
        if parsed.scheme != "https":
            raise ValueError("Only HTTPS URLs are allowed for security")

        return v


class RedesignResponse(BaseModel):
    """Response model for website redesign endpoint."""

    original_url: str
    original_screenshot: str  # base64
    original_html: str  # source HTML from the webpage
    analysis: dict
    html_code: str


@router.post("/redesign", response_model=RedesignResponse)
async def redesign_website(request: RedesignRequest):
    """
    Main endpoint: Takes a URL and returns a redesigned HTML page.

    This endpoint:
    1. Captures screenshots of the provided URL using Cua ComputerAgent
    2. Analyzes the design using Google Gemini Vision
    3. Generates a modern HTML page redesign

    Args:
        request: RedesignRequest containing the URL and optional style preferences

    Returns:
        RedesignResponse with original screenshot, analysis, and HTML code
    """
    screenshot_service, analyzer, generator = get_services()

    try:
        logger.info(f"Starting redesign for: {request.url}")

        # Step 1: Capture screenshots
        logger.info("Capturing screenshots...")
        screenshots = await screenshot_service.capture_website(str(request.url))

        # Step 2: Analyze design
        logger.info("Analyzing design...")
        analysis = await analyzer.analyze_design(screenshots["viewport"])

        # Step 3: Generate redesign
        logger.info("Generating HTML redesign...")
        html_code = await generator.generate_redesign(
            analysis=analysis,
            screenshot_b64=screenshots["full_page"],
            original_html=screenshots["html"],
            style_preferences=request.style_preferences,
        )

        logger.info("Redesign complete!")

        return RedesignResponse(
            original_url=str(request.url),
            original_screenshot=screenshots["viewport"],
            original_html=screenshots["html"],
            analysis=analysis,
            html_code=html_code,
        )

    except Exception as e:
        logger.error(f"Redesign failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/screenshot")
async def capture_screenshot(request: RedesignRequest):
    """
    Capture screenshots of a website without redesigning.
    Useful for testing the screenshot service.

    Args:
        request: RedesignRequest containing the URL

    Returns:
        dict with viewport and full_page base64 screenshots
    """
    screenshot_service, _, _ = get_services()

    try:
        logger.info(f"Capturing screenshot for: {request.url}")
        screenshots = await screenshot_service.capture_website(str(request.url))
        return screenshots
    except Exception as e:
        logger.error(f"Screenshot capture failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

