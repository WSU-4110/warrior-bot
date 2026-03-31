import click


def showHelp(ctx: click.Context, value: str | None) -> None:
    if value is None or value.lower() == "help":
        click.echo(ctx.get_help())
        ctx.exit()


@click.command(name="help")
@click.pass_context
def help(ctx: click.Context) -> None:
    """Shows this menu."""
    click.echo(ctx.parent.get_help() if ctx.parent else ctx.get_help())