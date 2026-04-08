"""Tests for Instagram main class."""

import pytest

from easyinsta import Instagram
from easyinsta.modules import Auth, Profiles, Validators


class TestInstagram:
    """Tests for Instagram class."""

    def test_creates_auth_module(self):
        """Should create auth module."""
        ig = Instagram()
        assert isinstance(ig.auth, Auth)

    def test_creates_validators_module(self):
        """Should create validators module."""
        ig = Instagram()
        assert isinstance(ig.validators, Validators)

    def test_creates_profiles_module(self):
        """Should create profiles module."""
        ig = Instagram()
        assert isinstance(ig.profiles, Profiles)

    def test_profiles_has_auth_reference(self):
        """Should pass auth to profiles module."""
        ig = Instagram()
        assert ig.profiles._auth is ig.auth
