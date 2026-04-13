"""Tests for device utilities."""

import re
from unittest.mock import patch

import pytest

from easyinsta.constants import RequestHeaders
from easyinsta.utils.device import (
    generate_bandwidth_bytes,
    generate_bandwidth_speed,
    generate_bandwidth_time,
    generate_capabilities,
    generate_connection_speed,
    generate_connection_type,
    generate_device_id,
    generate_guid,
    generate_ig_did,
    generate_locale,
    generate_mapped_locale,
    generate_mid,
    generate_pigeon_rawclienttime,
    generate_pigeon_session_id,
    generate_timezone_offset,
    get_locale_for_country,
)


class TestGenerateLocale:
    """Tests for generate_locale function."""

    def test_default_values(self):
        """Should return en_US with default values."""
        result = generate_locale()
        assert result == "en_US"

    def test_custom_values(self):
        """Should return correct locale with custom values."""
        result = generate_locale("CO", "es")
        assert result == "es_CO"

    def test_lowercase_region_converted_to_uppercase(self):
        """Should convert lowercase region to uppercase."""
        result = generate_locale("mx", "es")
        assert result == "es_MX"


class TestGenerateMappedLocale:
    """Tests for generate_mapped_locale function."""

    def test_default_values(self):
        """Should return en_US with default values."""
        result = generate_mapped_locale()
        assert result == "en_US"

    def test_custom_values(self):
        """Should return correct mapped locale with custom values."""
        result = generate_mapped_locale("BR", "pt")
        assert result == "pt_BR"

    def test_lowercase_region_converted_to_uppercase(self):
        """Should convert lowercase region to uppercase."""
        result = generate_mapped_locale("fr", "fr")
        assert result == "fr_FR"


class TestGeneratePigeonSessionId:
    """Tests for generate_pigeon_session_id function."""

    def test_returns_valid_uuid(self):
        """Should return a valid UUID v4 string."""
        result = generate_pigeon_session_id()
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
        assert re.match(uuid_pattern, result)

    def test_returns_unique_values(self):
        """Should return unique values on each call."""
        results = [generate_pigeon_session_id() for _ in range(10)]
        assert len(set(results)) == 10


class TestGeneratePigeonRawclienttime:
    """Tests for generate_pigeon_rawclienttime function."""

    def test_returns_timestamp_format(self):
        """Should return timestamp with 3 decimal places."""
        result = generate_pigeon_rawclienttime()
        assert re.match(r"^\d+\.\d{3}$", result)

    def test_returns_current_time(self):
        """Should return approximately current time."""
        with patch("easyinsta.utils.device.time.time", return_value=1234567890.123):
            result = generate_pigeon_rawclienttime()
        assert result == "1234567890.123"


class TestGetLocaleForCountry:
    """Tests for get_locale_for_country function."""

    def test_default_country(self):
        """Should return US locale by default."""
        result = get_locale_for_country()
        assert result[RequestHeaders.X_IG_APP_LOCALE] == "en_US"
        assert result[RequestHeaders.X_IG_DEVICE_LOCALE] == "en_US"
        assert result[RequestHeaders.X_IG_MAPPED_LOCALE] == "en_US"
        assert result[RequestHeaders.ACCEPT_LANGUAGE] == "en-US,en;q=0.9"

    def test_colombia_locale(self):
        """Should return Colombia locale."""
        result = get_locale_for_country("colombia")
        assert result[RequestHeaders.X_IG_APP_LOCALE] == "es_CO"
        assert result[RequestHeaders.X_IG_DEVICE_LOCALE] == "es_CO"
        assert result[RequestHeaders.X_IG_MAPPED_LOCALE] == "es_CO"
        assert result[RequestHeaders.ACCEPT_LANGUAGE] == "es-CO,es;q=0.9"

    def test_unknown_country_defaults_to_us(self):
        """Should return US locale for unknown country."""
        result = get_locale_for_country("unknown_country")
        assert result[RequestHeaders.X_IG_APP_LOCALE] == "en_US"

    def test_case_insensitive(self):
        """Should handle uppercase country names."""
        result = get_locale_for_country("SPAIN")
        assert result[RequestHeaders.X_IG_APP_LOCALE] == "es_ES"


class TestGenerateCapabilities:
    """Tests for generate_capabilities function."""

    def test_returns_base64_string(self):
        """Should return a valid base64 string."""
        result = generate_capabilities()
        assert result == "3brTPw=="


class TestGenerateDeviceId:
    """Tests for generate_device_id function."""

    def test_returns_android_prefix(self):
        """Should return string with android- prefix."""
        result = generate_device_id()
        assert result.startswith("android-")

    def test_returns_correct_length(self):
        """Should return 24 character string (android- + 16 hex chars)."""
        result = generate_device_id()
        assert len(result) == 24

    def test_hex_part_is_valid(self):
        """Should have valid hex characters after prefix."""
        result = generate_device_id()
        hex_part = result.replace("android-", "")
        assert re.match(r"^[0-9a-f]{16}$", hex_part)


class TestGenerateIgDid:
    """Tests for generate_ig_did function."""

    def test_returns_uppercase_uuid(self):
        """Should return uppercase UUID."""
        result = generate_ig_did()
        assert result == result.upper()

    def test_returns_valid_uuid_format(self):
        """Should return valid UUID format."""
        result = generate_ig_did()
        uuid_pattern = r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$"
        assert re.match(uuid_pattern, result)


class TestGenerateMid:
    """Tests for generate_mid function."""

    def test_returns_24_char_hex(self):
        """Should return 24 character hex string."""
        result = generate_mid()
        assert len(result) == 24
        assert re.match(r"^[0-9a-f]{24}$", result)


class TestGenerateGuid:
    """Tests for generate_guid function."""

    def test_returns_valid_uuid(self):
        """Should return valid UUID format."""
        result = generate_guid()
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        assert re.match(uuid_pattern, result)


class TestGenerateConnectionType:
    """Tests for generate_connection_type function."""

    def test_wifi_returns_wifi(self):
        """Should return WIFI when wifi=True."""
        result = generate_connection_type(wifi=True)
        assert result == "WIFI"

    def test_mobile_returns_mobile_type(self):
        """Should return MOBILE with type when wifi=False."""
        result = generate_connection_type(wifi=False)
        assert result.startswith("MOBILE(")
        assert result.endswith(")")
        mobile_type = result.replace("MOBILE(", "").replace(")", "")
        assert mobile_type in ["LTE", "HSPA", "HSDPA"]


class TestGenerateTimezoneOffset:
    """Tests for generate_timezone_offset function."""

    def test_returns_string(self):
        """Should return string representation of offset."""
        result = generate_timezone_offset()
        assert isinstance(result, str)

    def test_returns_integer_string(self):
        """Should return string that can be converted to int."""
        result = generate_timezone_offset()
        int(result)  # Should not raise

    def test_with_daylight_savings(self):
        """Should use altzone when daylight is True."""
        with patch("easyinsta.utils.device.time.daylight", True):
            with patch("easyinsta.utils.device.time.altzone", 14400):
                result = generate_timezone_offset()
        assert result == "-14400"

    def test_without_daylight_savings(self):
        """Should use timezone when daylight is False."""
        with patch("easyinsta.utils.device.time.daylight", False):
            with patch("easyinsta.utils.device.time.timezone", 18000):
                result = generate_timezone_offset()
        assert result == "-18000"


class TestGenerateBandwidthSpeed:
    """Tests for generate_bandwidth_speed function."""

    def test_wifi_returns_decimal_string(self):
        """Should return string with 3 decimal places for WiFi."""
        result = generate_bandwidth_speed(wifi=True)
        assert re.match(r"^\d+\.\d{3}$", result)

    def test_mobile_returns_decimal_string(self):
        """Should return string with 3 decimal places for mobile."""
        result = generate_bandwidth_speed(wifi=False)
        assert re.match(r"^\d+\.\d{3}$", result)

    def test_wifi_speed_in_range(self):
        """WiFi speed should be approximately in expected range."""
        speeds = [float(generate_bandwidth_speed(wifi=True)) for _ in range(100)]
        assert all(s >= 100 for s in speeds)  # min after max()

    def test_mobile_speed_in_range(self):
        """Mobile speed should be approximately in expected range."""
        speeds = [float(generate_bandwidth_speed(wifi=False)) for _ in range(100)]
        assert all(s >= 100 for s in speeds)  # min after max()


class TestGenerateBandwidthBytes:
    """Tests for generate_bandwidth_bytes function."""

    def test_session_start_returns_zero(self):
        """Should return '0' when session_start=True."""
        result = generate_bandwidth_bytes(session_start=True)
        assert result == "0"

    def test_active_session_returns_bytes(self):
        """Should return bytes in range when session_start=False."""
        result = generate_bandwidth_bytes(session_start=False)
        value = int(result)
        assert 1_000_000 <= value <= 50_000_000


class TestGenerateBandwidthTime:
    """Tests for generate_bandwidth_time function."""

    def test_session_start_returns_zero(self):
        """Should return '0' when session_start=True."""
        result = generate_bandwidth_time(session_start=True)
        assert result == "0"

    def test_active_session_returns_time(self):
        """Should return time in range when session_start=False."""
        result = generate_bandwidth_time(session_start=False)
        value = int(result)
        assert 5_000 <= value <= 120_000


class TestGenerateConnectionSpeed:
    """Tests for generate_connection_speed function."""

    def test_wifi_returns_kbps_format(self):
        """Should return string ending with 'kbps' for WiFi."""
        result = generate_connection_speed(wifi=True)
        assert result.endswith("kbps")

    def test_mobile_returns_kbps_format(self):
        """Should return string ending with 'kbps' for mobile."""
        result = generate_connection_speed(wifi=False)
        assert result.endswith("kbps")

    def test_wifi_speed_is_integer(self):
        """WiFi speed should be an integer value."""
        result = generate_connection_speed(wifi=True)
        speed = int(result.replace("kbps", ""))
        assert speed >= 100  # min after max()

    def test_mobile_speed_is_integer(self):
        """Mobile speed should be an integer value."""
        result = generate_connection_speed(wifi=False)
        speed = int(result.replace("kbps", ""))
        assert speed >= 100  # min after max()
