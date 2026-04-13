"""
Upload utilities for Instagram API.

This module provides functionality to upload media (photos) to Instagram.
"""

import time
import uuid
from io import BytesIO

import requests


# Hardcoded config (same as foo.py)
BEARER = "IGT:2:eyJkc191c2VyX2lkIjoiMzY2NzY3MTI2NTYiLCJzZXNzaW9uaWQiOiIzNjY3NjcxMjY1NiUzQUJvZGgzem5FQ0FoNTVwJTNBNyUzQUFZaHZtSGlSZVk5ckljdWIzZlpKaTV2b3o0WkpwRTdZM3JmMGw5Q1pGQSJ9"
WWW_CLAIM = "hmac.AR15DbrFJ725WBbDqzRf-QBsEkOsGLrMmREH-JEqRwW9yico"

DEVICE = {
    "user_agent": "Instagram 278.0.0.19.103 Android (31/12; 480dpi; 1440x3200; samsung; SM-S908B; b0s; exynos2200; en_US; 457547470)",
    "device_id": "4EA5230C-6A2B-44E5-9542-E7A4149AC5BA",
    "android_id": "android-c2d5d1c487d24b4d",
    "pigeon_sid": "fa41a265-eca6-462d-b0fd-8da5bdc8f415",
}


def _base_headers() -> dict:
    return {
        "User-Agent": DEVICE["user_agent"],
        "Authorization": f"Bearer {BEARER}",
        "X-Ig-App-Id": "936619743392459",
        "X-Ig-Capabilities": "3brTPw==",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Device-Id": DEVICE["device_id"],
        "X-Ig-Android-Id": DEVICE["android_id"],
        "X-Ig-Timezone-Offset": "-18000",
        "X-Ig-Www-Claim": WWW_CLAIM,
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": DEVICE["pigeon_sid"],
        "X-Pigeon-Rawclienttime": f"{time.time():.3f}",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
    }


def upload_photo(
    image: BytesIO,
    headers: dict,  # Ignored for now, using hardcoded headers
) -> str | None:
    """
    Upload a photo to Instagram's rupload endpoint.

    Args:
        image: A BytesIO object containing the image bytes (JPEG).
        headers: Authentication headers (ignored, using hardcoded for testing).

    Returns:
        The upload_id if successful, None otherwise.
    """
    image_data = image.getvalue()
    upload_id = str(int(time.time() * 1000))
    entity_name = f"{upload_id}_0_{uuid.uuid4().int & 0xFFFFFFFF}"
    content_len = len(image_data)

    print(f"\n📤 Subiendo imagen...")
    print(f"   upload_id   : {upload_id}")
    print(f"   entity_name : {entity_name}")

    upload_headers = _base_headers()
    upload_headers.update({
        "X-Instagram-Rupload-Params": f'{{"upload_id":"{upload_id}","media_type":"1"}}',
        "X-Entity-Type": "image/jpeg",
        "X-Entity-Name": entity_name,
        "X-Entity-Length": str(content_len),
        "Offset": "0",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(content_len),
    })

    resp = requests.post(
        f"https://i.instagram.com/rupload_igphoto/{entity_name}/",
        headers=upload_headers,
        data=image_data,
    )

    print(f"   Status  : {resp.status_code}")
    print(f"   Response: {resp.text}")

    if resp.status_code == 200 and resp.json().get("status") == "ok":
        print(f"   ✅ Upload exitoso")
        return upload_id

    print(f"   ❌ Upload falló")
    return None
