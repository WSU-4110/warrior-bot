"""Tests for the 'help' command."""

import click
from click.testing import CliRunner

from warrior_bot.commands.help import help as help_command


def test_help_command_standalone_shows_its_own_help():
    """If help is invoked by itself, it should show its own help text."""
    runner = CliRunner()

    result = runner.invoke(help_command)

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Show help information." in result.output


def test_help_command_uses_parent_help_when_registered():
    """If help is attached to a parent CLI, it should print the parent's help."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """Temporary CLI for testing."""
        pass

    @click.command()
    def sample():
        """Sample command."""
        pass

    test_cli.add_command(sample)
    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Temporary CLI for testing." in result.output
    assert "Commands:" in result.output
    assert "sample" in result.output
    assert "help" in result.output


def test_help_command_matches_parent_dash_help_output():
    """The custom help command output should match the normal --help output."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """Temporary CLI for testing."""
        pass

    @click.command()
    def sample():
        """Sample command."""
        pass

    test_cli.add_command(sample)
    test_cli.add_command(help_command)

    result_help_cmd = runner.invoke(test_cli, ["help"])
    result_dash_help = runner.invoke(test_cli, ["--help"])

    assert result_help_cmd.exit_code == 0
    assert result_dash_help.exit_code == 0
    assert result_help_cmd.output == result_dash_help.output


def test_help_command_lists_registered_commands():
    """The help command should include all commands registered on the parent CLI."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """Temporary CLI for testing."""
        pass

    @click.command()
    def alpha():
        """Alpha command."""
        pass

    @click.command()
    def beta():
        """Beta command."""
        pass

    test_cli.add_command(alpha)
    test_cli.add_command(beta)
    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["help"])

    assert result.exit_code == 0
    assert "alpha" in result.output
    assert "beta" in result.output
    assert "help" in result.output


def test_help_command_description_in_parent():
    """Help command should display its description in the command list."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """CLI with help command."""
        pass

    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["--help"])

    assert result.exit_code == 0
    assert "help" in result.output
    assert "Show help information." in result.output


def test_help_command_only_command_in_cli():
    """Help command should still work even if it's the only command."""
    runner = CliRunner()

    @click.group()
    def test_cli():
        """CLI with only help command."""
        pass

    test_cli.add_command(help_command)

    result = runner.invoke(test_cli, ["help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output
    assert "help" in result.output