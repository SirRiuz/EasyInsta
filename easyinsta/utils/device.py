"""
Device and network generation utilities for Instagram API requests.

This module provides functionality to generate device identifiers,
network parameters, and locale headers that mimic real Android devices.
"""

import base64
import random
import struct
import time
import uuid

from easyinsta.constants import App, RequestHeaders


def generate_locale(region: str = "US", language: str = "en") -> str:
    """
    Generate locale string in language_REGION format.

    Args:
        region: The region code (e.g., "US", "CO").
        language: The language code (e.g., "en", "es").

    Returns:
        Locale string in format "language_REGION".
    """
    return f"{language}_{region.upper()}"


def generate_mapped_locale(region: str = "US", language: str = "en") -> str:
    """
    Generate normalized locale for Facebook format.

    Args:
        region: The region code (e.g., "US", "CO").
        language: The language code (e.g., "en", "es").

    Returns:
        Normalized locale string in format "language_REGION".
    """
    return f"{language}_{region.upper()}"


def generate_pigeon_session_id() -> str:
    """Generate a random pigeon session ID (UUID v4)."""
    return str(uuid.uuid4())


def generate_pigeon_rawclienttime() -> str:
    """Generate current timestamp with milliseconds."""
    return f"{time.time():.3f}"


def get_locale_for_country(country: str = "usa") -> dict:
    """
    Get locale headers for a specific country.

    Args:
        country: Country name (e.g., "usa", "colombia", "spain").

    Returns:
        Dictionary with locale headers.
    """
    lang, region = App.LOCALES.get(country.lower(), ("en", "US"))
    locale = generate_locale(region, lang)
    mapped = generate_mapped_locale(region, lang)
    return {
        RequestHeaders.X_IG_APP_LOCALE: locale,
        RequestHeaders.X_IG_DEVICE_LOCALE: locale,
        RequestHeaders.X_IG_MAPPED_LOCALE: mapped,
        RequestHeaders.ACCEPT_LANGUAGE: f"{lang}-{region},{lang};q=0.9",
    }


def generate_capabilities() -> str:
    """Generate Instagram capabilities header (base64 encoded)."""
    packed = struct.pack("<I", App.CAPABILITIES_INT)
    return base64.b64encode(packed).decode("ascii")


def generate_device_id() -> str:
    """Generate Android device ID."""
    return f"android-{uuid.uuid4().hex[:16]}"


def generate_ig_did() -> str:
    """Generate Instagram device ID (uppercase UUID)."""
    return str(uuid.uuid4()).upper()


def generate_mid() -> str:
    """Generate machine ID (24 character hex string)."""
    return uuid.uuid4().hex[:24]


def generate_guid() -> str:
    """Generate a random GUID (UUID v4)."""
    return str(uuid.uuid4())


def generate_connection_type(wifi: bool = True) -> str:
    """
    Generate connection type header.

    Args:
        wifi: True for WiFi, False for mobile connection.

    Returns:
        Connection type string.
    """
    if wifi:
        return "WIFI"
    return f"MOBILE({random.choice(['LTE', 'HSPA', 'HSDPA'])})"


def generate_timezone_offset() -> str:
    """Generate UTC timezone offset in seconds."""
    offset = -time.timezone
    if time.daylight:
        offset = -time.altzone
    return str(offset)


def generate_bandwidth_speed(wifi: bool = True) -> str:
    """
    Generate bandwidth speed in KBPS.

    Simulates natural network variation with gaussian noise.
    WiFi: 2000-8000 KBPS, Mobile: 500-3000 KBPS.

    Args:
        wifi: True for WiFi, False for mobile connection.

    Returns:
        Bandwidth speed string with 3 decimal places.
    """
    if wifi:
        base = random.uniform(2000, 8000)
        noise = random.gauss(0, 150)
    else:
        base = random.uniform(500, 3000)
        noise = random.gauss(0, 80)
    speed = max(100.0, base + noise)
    return f"{speed:.3f}"


def generate_bandwidth_bytes(session_start: bool = True) -> str:
    """
    Generate total bytes transferred.

    Args:
        session_start: True if session just started (returns "0").

    Returns:
        Total bytes as string.
    """
    if session_start:
        return "0"
    return str(random.randint(1_000_000, 50_000_000))


def generate_bandwidth_time(session_start: bool = True) -> str:
    """
    Generate total transfer time in milliseconds.

    Args:
        session_start: True if session just started (returns "0").

    Returns:
        Total time in ms as string.
    """
    if session_start:
        return "0"
    return str(random.randint(5_000, 120_000))


def generate_connection_speed(wifi: bool = True) -> str:
    """
    Generate instantaneous connection speed in kbps.

    Args:
        wifi: True for WiFi (1500-9000 kbps), False for mobile (300-5000 kbps).

    Returns:
        Connection speed string in format "XXXXkbps".
    """
    if wifi:
        base = random.randint(1500, 9000)
        noise = random.randint(-200, 200)
    else:
        base = random.randint(300, 5000)
        noise = random.randint(-100, 100)
    speed = max(100, base + noise)
    return f"{speed}kbps"
