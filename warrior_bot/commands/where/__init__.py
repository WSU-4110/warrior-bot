"""Where command implementation."""

import click


@click.command()
def where():
    """Where command."""
    click.echo("Executing where command")
