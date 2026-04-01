"""Tests for the 'book' command."""

from datetime import date, timedelta
from unittest.mock import patch

from warrior_bot.commands.book.prompts import (
    MAX_DAYS_AHEAD,
    _fuzzy_score,
    fuzzy_match_templates,
    prompt_date,
)


# Test 1: _fuzzy_score returns high score for substring match
def test_fuzzy_score_substring_match():
    score = _fuzzy_score("state", "state hall")
    assert score >= 0.55


# Test 2: fuzzy_match_templates returns results sorted best first
def test_fuzzy_match_templates_sorted():
    templates = [
        {"name": "State Hall", "index": "0"},
        {"name": "State Tower", "index": "1"},
    ]
    results = fuzzy_match_templates("state hall", templates)
    assert results[0]["name"] == "State Hall"


# Test 3: prompt_date rejects dates too far in the future
def test_prompt_date_rejects_too_far():
    too_far = (date.today() + timedelta(days=MAX_DAYS_AHEAD + 1)).strftime("%m/%d/%Y")
    valid = date.today().strftime("%m/%d/%Y")
    with patch("click.prompt", side_effect=[too_far, valid]):
        result = prompt_date()
    assert result == valid


# Test 4: _fuzzy_score exact match returns 1.0
def test_fuzzy_score_exact_match():
    score = _fuzzy_score("state hall", "state hall")
    assert score == 1.0


# Test 5: _fuzzy_score unrelated strings score below threshold
def test_fuzzy_score_no_match():
    score = _fuzzy_score("xyz", "state hall")
    assert score < 0.55


# Test 6: fuzzy_match_templates finds correct building
def test_fuzzy_match_templates_finds_match():
    templates = [
        {"name": "State Hall", "index": "0"},
        {"name": "STEM Building", "index": "1"},
        {"name": "Student Center", "index": "2"},
    ]
    results = fuzzy_match_templates("state hall", templates)
    assert len(results) > 0
    assert results[0]["name"] == "State Hall"


# Test 7: fuzzy_match_templates returns empty for no match
def test_fuzzy_match_templates_no_match():
    templates = [
        {"name": "State Hall", "index": "0"},
        {"name": "STEM Building", "index": "1"},
    ]
    results = fuzzy_match_templates("zzzzz", templates)
    assert results == []


# Test 8: prompt_date rejects past dates
def test_prompt_date_rejects_past():
    past_date = (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")
    today = date.today().strftime("%m/%d/%Y")
    with patch("click.prompt", side_effect=[past_date, today]):
        result = prompt_date()
    assert result == today
