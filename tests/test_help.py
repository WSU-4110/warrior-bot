"""Tests for the 'help' command."""

import click
from click.testing import CliRunner

from warrior_bot.commands.help import help as help_command


def test_help_command_shows_banner():
    """The help command should display the warrior-bot ASCII banner."""
    runner = CliRunner()

    result = runner.invoke(help_command)

    assert result.exit_code == 0
    assert "██" in result.output


def test_help_command_shows_usage():
    """The help command should display usage information."""
    runner = CliRunner()

    result = runner.invoke(help_command)

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_help_command_lists_commands():
    """The help command should list the available warrior-bot commands."""
    runner = CliRunner()

    result = runner.invoke(help_command)

    assert result.exit_code == 0
    assert "COMMANDS:" in result.output
    assert "go" in result.output
    assert "where" in result.output
    assert "book" in result.output
    assert "help" in result.output


def test_help_command_shows_help_section():
    """The help command should include the HELP usage examples section."""
    runner = CliRunner()

    result = runner.invoke(help_command)

    assert result.exit_code == 0
    assert "HELP:" in result.output
    assert "wb help" in result.output
    assert "wb --help" in result.output


def test_help_command_works_in_parent_group():
    """The help command should work when registered under a parent CLI group."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """Temporary CLI for testing."""
        pass

    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "COMMANDS:" in result.output


def test_help_command_description_in_parent():
    """Help command should appear in the parent group's --help listing."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """CLI with help command."""
        pass

    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["--help"])

    assert result.exit_code == 0
    assert "help" in result.output
