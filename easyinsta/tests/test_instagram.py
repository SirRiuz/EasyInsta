"""Tests for Instagram main class."""

import pytest

from easyinsta import Instagram
from easyinsta.modules import Profiles, Validators


class TestInstagram:
    """Tests for Instagram class."""

    def test_creates_validators_module(self):
        """Should create validators module."""
        ig = Instagram()
        assert isinstance(ig.validators, Validators)

    def test_creates_profiles_module(self):
        """Should create profiles module."""
        ig = Instagram()
        assert isinstance(ig.profiles, Profiles)
