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
def academicaTest(mockBrowser):
    runner = CliRunner()

    result = runner.invoke(go_command, ["academica"])

    assert result.exit_code == 0
    assert "Academica" in result.output
    url, new, autoraise = mockBrowser[0]
    assert url = "http://academica.aws.wayne.edu/"
    assert new = 1
    assert autoraise is True
