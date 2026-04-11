"""Tests for the 'help' command."""

from click.testing import CliRunner

from warrior_bot.cli import cli


def test_help_command_shows_banner():
    """The help command should display the warrior-bot ASCII banner."""
    runner = CliRunner()

    result = runner.invoke(cli, ["help"])

    assert result.exit_code == 0
    assert "██" in result.output


def test_help_command_shows_usage():
    """The help command should display usage information."""
    runner = CliRunner()

    result = runner.invoke(cli, ["help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_help_command_lists_commands():
    """The help command should list the available warrior-bot commands."""
    runner = CliRunner()

    result = runner.invoke(cli, ["help"])

    assert result.exit_code == 0
    assert "go" in result.output
    assert "where" in result.output
    assert "book" in result.output
    assert "help" in result.output


def test_cli_help_flag():
    """wb --help should show the same output as wb help."""
    runner = CliRunner()

    help_result = runner.invoke(cli, ["help"])
    flag_result = runner.invoke(cli, ["--help"])

    assert help_result.exit_code == 0
    assert flag_result.exit_code == 0
    assert help_result.output == flag_result.output


def test_subcommand_help():
    """Each subcommand should have working --help."""
    runner = CliRunner()

    for cmd in ["go", "where", "book"]:
        result = runner.invoke(cli, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
