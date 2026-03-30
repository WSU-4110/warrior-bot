"""Tests for the 'go' command."""

import pytest
from click.testing import CliRunner
from warrior_bot.commands.go import go as go_command

# Fixture for a mock browser
@pytest.fixture
def mockBrowser(monkeypatch):
    opened = []

    def fakeOpen(url, new, autoraise):
        opened.append((url, new, autoraise))

    monkeypatch.setattr("warrior_bot.commands.go.webbrowser.open", fakeOpen)
    return opened

#1. Academica Unit Test
def test_Academica(mockBrowser):
    runner = CliRunner()

    result = runner.invoke(go_command, ["academica"])

    assert result.exit_code == 0
    assert "Academica" in result.output
    url, new, autoraise = mockBrowser[0]
    assert url == "http://academica.aws.wayne.edu/"
    assert new == 1
    assert autoraise is True

#2. Library Unit Test
def test_Library(mockBrowser):
    runner = CliRunner()

    result = runner.invoke(go_command, ["library"])

    assert result.exit_code == 0
    assert "Library" in result.output
    url, new, autoraise = mockBrowser[0]
    assert url == "https://library.wayne.edu/"
    assert new == 1
    assert autoraise is True

#3. Bookstore Unit Test
def test_Bookstore(mockBrowser):
    runner = CliRunner()

    result = runner.invoke(go_command, ["bookstore"])

    assert result.exit_code == 0
    assert "Bookstore" in result.output
    url, new, autoraise = mockBrowser[0]
    assert url == "https://waynestatebookstore.com/"
    assert new == 1
    assert autoraise is True

#4. DegreeWorks Unit Test
def test_Degreeworks(mockBrowser):
    runner = CliRunner()

    result = runner.invoke(go_command, ["degreeworks"])

    assert result.exit_code == 0
    assert "Degree Works" in result.output
    url, new, autoraise = mockBrowser[0]
    assert url == "https://degreeworks.wayne.edu/"
    assert new == 1
    assert autoraise is True
