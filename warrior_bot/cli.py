"""CLI entry point using Click."""

import click

from warrior_bot.commands import book, go, where


@click.group()
def cli():
    """Warrior Bot CLI."""
    pass


# Register commands
cli.add_command(go.go)
cli.add_command(where.where)
cli.add_command(book.book)
