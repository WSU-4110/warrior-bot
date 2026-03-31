"""Shared fixtures for warrior-bot tests."""

import pytest
from click.testing import CliRunner

from warrior_bot.cli import cli


@pytest.fixture
def runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def invoke(runner):
    """Shortcut: invoke the top-level CLI group."""

    def _invoke(*args, **kwargs):
        return runner.invoke(cli, args, catch_exceptions=False, **kwargs)

    return _invoke
