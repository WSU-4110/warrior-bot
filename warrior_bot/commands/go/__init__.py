"""Go command implementation."""

import click


@click.command()
def go():
    """Go command."""
    click.echo("Executing go command")
