import click


@click.command()
@click.pass_context
def help(ctx):
    """Show help information."""
    if ctx.parent:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(ctx.get_help())
