"""Tests for data models."""

import pytest

from easyinsta.models import Profile, ProfileLight


class TestProfileLight:
    """Tests for ProfileLight model."""

    def test_extracts_id(self):
        """Should extract id from pk field."""
        data = {"pk": "123456", "username": "test", "profile_pic_url": "http://example.com/pic.jpg"}
        profile = ProfileLight(data)
        assert profile.id == "123456"

    def test_extracts_username(self):
        """Should extract username."""
        data = {"pk": "123456", "username": "testuser", "profile_pic_url": "http://example.com/pic.jpg"}
        profile = ProfileLight(data)
        assert profile.username == "testuser"

    def test_extracts_profile_pic_url(self):
        """Should extract profile pic URL."""
        data = {"pk": "123456", "username": "test", "profile_pic_url": "http://example.com/pic.jpg"}
        profile = ProfileLight(data)
        assert profile.profile_pic_url == "http://example.com/pic.jpg"

    def test_raw_property(self):
        """Should return raw data."""
        data = {"pk": "123456", "username": "test", "profile_pic_url": "http://example.com/pic.jpg"}
        profile = ProfileLight(data)
        assert profile.raw == data

    def test_defaults_for_missing_fields(self):
        """Should use defaults for missing fields."""
        profile = ProfileLight({})
        assert profile.id == ""
        assert profile.username == ""
        assert profile.profile_pic_url == ""

    def test_repr(self):
        """Should have correct repr."""
        data = {"pk": "123456", "username": "testuser"}
        profile = ProfileLight(data)
        assert "123456" in repr(profile)
        assert "testuser" in repr(profile)


class TestProfile:
    """Tests for Profile model."""

    def test_extracts_basic_info(self):
        """Should extract basic profile info."""
        data = {
            "pk": "123456",
            "fbid_v2": "fb123",
            "username": "testuser",
            "full_name": "Test User",
            "biography": "Test bio",
        }
        profile = Profile(data)
        assert profile.id == "123456"
        assert profile.fbid == "fb123"
        assert profile.username == "testuser"
        assert profile.full_name == "Test User"
        assert profile.biography == "Test bio"

    def test_extracts_profile_pic_urls(self):
        """Should extract profile picture URLs."""
        data = {
            "profile_pic_url": "http://example.com/pic.jpg",
            "hd_profile_pic_url_info": {"url": "http://example.com/pic_hd.jpg"},
        }
        profile = Profile(data)
        assert profile.profile_pic_url == "http://example.com/pic.jpg"
        assert profile.profile_pic_url_hd == "http://example.com/pic_hd.jpg"

    def test_extracts_account_status(self):
        """Should extract account status flags."""
        data = {
            "is_private": True,
            "is_verified": True,
            "is_business": True,
            "is_memorialized": False,
        }
        profile = Profile(data)
        assert profile.is_private is True
        assert profile.is_verified is True
        assert profile.is_business is True
        assert profile.is_memorialized is False

    def test_extracts_counts(self):
        """Should extract follower/following counts."""
        data = {
            "follower_count": 1000,
            "following_count": 500,
            "media_count": 50,
            "total_clips_count": 10,
        }
        profile = Profile(data)
        assert profile.follower_count == 1000
        assert profile.following_count == 500
        assert profile.media_count == 50
        assert profile.total_clips_count == 10

    def test_extracts_additional_info(self):
        """Should extract additional profile info."""
        data = {
            "external_url": "http://example.com",
            "category": "Artist",
            "has_highlight_reels": True,
            "has_guides": False,
            "is_active_on_text_post_app": True,
            "is_whatsapp_linked": False,
        }
        profile = Profile(data)
        assert profile.external_url == "http://example.com"
        assert profile.category == "Artist"
        assert profile.has_highlight_reels is True
        assert profile.has_guides is False
        assert profile.is_active_on_text_post_app is True
        assert profile.is_whatsapp_linked is False

    def test_extracts_privacy_settings(self):
        """Should extract privacy settings."""
        data = {
            "allow_mention_setting": "following",
            "allow_tag_setting": "no_one",
        }
        profile = Profile(data)
        assert profile.allow_mention_setting == "following"
        assert profile.allow_tag_setting == "no_one"

    def test_extracts_timezone(self):
        """Should extract timezone."""
        data = {"last_seen_timezone": "America/New_York"}
        profile = Profile(data)
        assert profile.last_seen_timezone == "America/New_York"

    def test_raw_property(self):
        """Should return raw data."""
        data = {"pk": "123456", "username": "test"}
        profile = Profile(data)
        assert profile.raw == data

    def test_defaults_for_missing_fields(self):
        """Should use defaults for missing fields."""
        profile = Profile({})
        assert profile.id == ""
        assert profile.username == ""
        assert profile.follower_count == 0
        assert profile.is_private is False
        assert profile.category is None

    def test_repr(self):
        """Should have correct repr."""
        data = {"pk": "123456", "username": "testuser", "full_name": "Test User"}
        profile = Profile(data)
        assert "123456" in repr(profile)
        assert "testuser" in repr(profile)
        assert "Test User" in repr(profile)
