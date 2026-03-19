"""
User agent generation utilities for Instagram API requests.

This module provides functionality to generate random Instagram app user agents
that mimic real Android devices.
"""

import random


DEVICES: list[dict[str, str]] = [
    {"brand": "OnePlus", "model": "ONEPLUS A3003", "device": "OnePlus3", "cpu": "qcom"},
    {"brand": "samsung", "model": "SM-G991B", "device": "o1s", "cpu": "exynos2100"},
    {"brand": "samsung", "model": "SM-G975F", "device": "beyond2", "cpu": "exynos9820"},
    {"brand": "samsung", "model": "SM-S908B", "device": "b0s", "cpu": "exynos2200"},
    {"brand": "Google", "model": "Pixel 7", "device": "panther", "cpu": "tensor"},
    {"brand": "Google", "model": "Pixel 6", "device": "oriole", "cpu": "tensor"},
    {"brand": "Xiaomi", "model": "M2101K6G", "device": "alioth", "cpu": "qcom"},
    {"brand": "Xiaomi", "model": "2201116SG", "device": "vili", "cpu": "qcom"},
    {"brand": "OnePlus", "model": "LE2121", "device": "OnePlus9Pro", "cpu": "qcom"},
    {"brand": "HUAWEI", "model": "VOG-L29", "device": "HWVOG", "cpu": "kirin980"},
]

ANDROID_VERSIONS: list[tuple[int, str]] = [
    (26, "8.0.0"),
    (28, "9"),
    (29, "10"),
    (30, "11"),
    (31, "12"),
    (33, "13"),
    (34, "14"),
]

DPIS: list[int] = [420, 440, 480, 560]

RESOLUTIONS: list[str] = [
    "1080x1920",
    "1080x2340",
    "1080x2400",
    "1080x2280",
    "1440x3200",
]

APP_VERSIONS: list[str] = [
    "275.0.0.27.98",
    "276.0.0.26.103",
    "277.0.0.15.111",
    "278.0.0.19.103",
]


def get_random_user_agent() -> str:
    """
    Generate a random Instagram Android app user agent.

    Combines random values from device profiles, Android versions,
    screen densities, resolutions, and app versions to create
    a realistic user agent string.

    Returns:
        A user agent string mimicking the Instagram Android app.

    Example:
        >>> ua = get_random_user_agent()
        >>> print(ua)
        Instagram 275.0.0.27.98 Android (33/13; 480dpi; 1080x2400; Google; Pixel 7; panther; tensor; en_US; 458229237)
    """
    device = random.choice(DEVICES)
    android = random.choice(ANDROID_VERSIONS)
    dpi = random.choice(DPIS)
    resolution = random.choice(RESOLUTIONS)
    app_version = random.choice(APP_VERSIONS)
    build_id = random.randint(450000000, 460000000)

    return (
        f"Instagram {app_version} Android ({android[0]}/{android[1]}; {dpi}dpi; {resolution}; "
        f"{device['brand']}; {device['model']}; {device['device']}; {device['cpu']}; en_US; {build_id})"
    )
