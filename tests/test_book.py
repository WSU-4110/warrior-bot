"""Tests for the 'book' command."""

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from warrior_bot.commands.book.prompts import (
    MAX_DAYS_AHEAD,
    _fuzzy_score,
    fuzzy_match_templates,
    prompt_date,
)


class TestFuzzyScore:
    """Tests for _fuzzy_score helper function."""

    def test_exact_match_returns_one(self):
        """Exact match (case-insensitive) should return 1.0."""
        assert _fuzzy_score("State Hall", "state hall") == 1.0
        assert _fuzzy_score("STEM", "stem") == 1.0

    def test_substring_match_scores_high(self):
        """Substring matches should score above 0.9."""
        score = _fuzzy_score("lounge", "Student Lounge Space")
        assert score > 0.9

    def test_no_match_scores_low(self):
        """Completely unrelated strings should score below threshold."""
        score = _fuzzy_score("xyz123", "Student Lounge Space")
        assert score < 0.55


class TestFuzzyMatchTemplates:
    """Tests for fuzzy_match_templates function."""

    @pytest.fixture
    def sample_templates(self):
        """Sample template list for testing."""
        return [
            {"name": "STEM Innovation Learning Center", "index": "0"},
            {"name": "Student Lounge Space", "index": "1"},
            {"name": "State Hall Conference Room", "index": "2"},
        ]

    def test_exact_name_match_first(self, sample_templates):
        """Exact name match should be returned first."""
        matches = fuzzy_match_templates("State Hall Conference Room", sample_templates)
        assert len(matches) >= 1
        assert matches[0]["name"] == "State Hall Conference Room"

    def test_partial_match_returns_results(self, sample_templates):
        """Partial/substring match should return relevant templates."""
        matches = fuzzy_match_templates("lounge", sample_templates)
        assert len(matches) >= 1
        assert any("Lounge" in m["name"] for m in matches)

    def test_no_match_returns_empty(self, sample_templates):
        """Query with no fuzzy matches should return empty list."""
        matches = fuzzy_match_templates("xyzabc999", sample_templates)
        assert matches == []


class TestPromptDate:
    """Tests for prompt_date validation logic."""

    def test_rejects_past_date(self):
        """Past dates should be rejected with appropriate message."""
        yesterday = (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")
        today_str = date.today().strftime("%m/%d/%Y")

        with patch("click.prompt", side_effect=[yesterday, today_str]):
            with patch("click.echo") as mock_echo:
                result = prompt_date()
                assert result == today_str
                calls = [str(c) for c in mock_echo.call_args_list]
                assert any("past" in c.lower() for c in calls)

    def test_rejects_date_beyond_max_days_ahead(self):
        """Dates more than MAX_DAYS_AHEAD should be rejected."""
        too_far = (date.today() + timedelta(days=MAX_DAYS_AHEAD + 1)).strftime(
            "%m/%d/%Y"
        )
        valid_date = date.today().strftime("%m/%d/%Y")

        with patch("click.prompt", side_effect=[too_far, valid_date]):
            with patch("click.echo") as mock_echo:
                result = prompt_date()
                assert result == valid_date
                calls = [str(c) for c in mock_echo.call_args_list]
                assert any(str(MAX_DAYS_AHEAD) in c for c in calls)

    def test_accepts_valid_date_within_range(self):
        """Valid date within the allowed range should be accepted."""
        valid_date = (date.today() + timedelta(days=5)).strftime("%m/%d/%Y")

        with patch("click.prompt", return_value=valid_date):
            result = prompt_date()
            assert result == valid_date
