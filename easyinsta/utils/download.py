"""
Download utilities for Instagram API.

This module provides functionality to download media from URLs.
"""

from io import BytesIO

import aiohttp


async def download_image(url: str) -> BytesIO:
    """
    Download an image from a URL and return it as BytesIO.

    Args:
        url: The URL of the image to download.

    Returns:
        A BytesIO object containing the image bytes.

    Raises:
        aiohttp.ClientError: If the download fails.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            image_bytes = await response.read()
            return BytesIO(image_bytes)
