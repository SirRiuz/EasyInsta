"""Tests for user agent generation utilities."""

import re

from easyinsta.utils.agents import (
    ANDROID_VERSIONS,
    APP_VERSIONS,
    DEVICES,
    DPIS,
    RESOLUTIONS,
    get_random_user_agent,
)


class TestGetRandomUserAgent:
    """Tests for get_random_user_agent function."""

    def test_returns_string(self):
        """Should return a string."""
        ua = get_random_user_agent()
        assert isinstance(ua, str)

    def test_starts_with_instagram(self):
        """Should start with 'Instagram'."""
        ua = get_random_user_agent()
        assert ua.startswith("Instagram ")

    def test_contains_android(self):
        """Should contain 'Android'."""
        ua = get_random_user_agent()
        assert "Android" in ua

    def test_contains_valid_app_version(self):
        """Should contain a valid app version."""
        ua = get_random_user_agent()
        assert any(version in ua for version in APP_VERSIONS)

    def test_contains_valid_device_brand(self):
        """Should contain a valid device brand."""
        ua = get_random_user_agent()
        brands = [device["brand"] for device in DEVICES]
        assert any(brand in ua for brand in brands)

    def test_contains_valid_dpi(self):
        """Should contain a valid DPI value."""
        ua = get_random_user_agent()
        assert any(f"{dpi}dpi" in ua for dpi in DPIS)

    def test_contains_valid_resolution(self):
        """Should contain a valid resolution."""
        ua = get_random_user_agent()
        assert any(resolution in ua for resolution in RESOLUTIONS)

    def test_contains_valid_android_version(self):
        """Should contain a valid Android version."""
        ua = get_random_user_agent()
        assert any(f"({api}/" in ua for api, _ in ANDROID_VERSIONS)

    def test_contains_locale(self):
        """Should contain en_US locale."""
        ua = get_random_user_agent()
        assert "en_US" in ua

    def test_contains_build_id(self):
        """Should contain a numeric build ID."""
        ua = get_random_user_agent()
        match = re.search(r"en_US; (\d+)\)", ua)
        assert match is not None
        build_id = int(match.group(1))
        assert 450000000 <= build_id <= 460000000

    def test_format_structure(self):
        """Should match expected format structure."""
        ua = get_random_user_agent()
        pattern = r"Instagram \d+\.\d+\.\d+\.\d+\.\d+ Android \(\d+/[\d.]+; \d+dpi; \d+x\d+; .+; .+; .+; .+; en_US; \d+\)"
        assert re.match(pattern, ua) is not None

    def test_randomness(self):
        """Should generate different user agents on multiple calls."""
        user_agents = {get_random_user_agent() for _ in range(50)}
        assert len(user_agents) > 1


class TestDevicesConstant:
    """Tests for DEVICES constant."""

    def test_devices_not_empty(self):
        """DEVICES should not be empty."""
        assert len(DEVICES) > 0

    def test_devices_have_required_keys(self):
        """Each device should have required keys."""
        required_keys = {"brand", "model", "device", "cpu"}
        for device in DEVICES:
            assert required_keys.issubset(device.keys())


class TestAndroidVersionsConstant:
    """Tests for ANDROID_VERSIONS constant."""

    def test_android_versions_not_empty(self):
        """ANDROID_VERSIONS should not be empty."""
        assert len(ANDROID_VERSIONS) > 0

    def test_android_versions_format(self):
        """Each version should be a tuple of (int, str)."""
        for api_level, version_str in ANDROID_VERSIONS:
            assert isinstance(api_level, int)
            assert isinstance(version_str, str)


class TestAppVersionsConstant:
    """Tests for APP_VERSIONS constant."""

    def test_app_versions_not_empty(self):
        """APP_VERSIONS should not be empty."""
        assert len(APP_VERSIONS) > 0

    def test_app_versions_format(self):
        """Each version should match Instagram version format."""
        pattern = r"\d+\.\d+\.\d+\.\d+\.\d+"
        for version in APP_VERSIONS:
            assert re.match(pattern, version) is not None
