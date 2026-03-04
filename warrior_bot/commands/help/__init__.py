import click

@click.command(name="help")
@click.pass_context
def help(ctx: click.Context) -> None:
    """Show help information."""
    # Show the top-level help for the CLI
    click.echo(ctx.parent.get_help() if ctx.parent else ctx.get_help())