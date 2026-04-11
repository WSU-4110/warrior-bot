"""Help command - shows main help (alias for wb --help)."""

import click


@click.command(name="help")
@click.pass_context
def help(ctx: click.Context) -> None:
    """Show the main help message."""
    if ctx.parent:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(ctx.get_help())
