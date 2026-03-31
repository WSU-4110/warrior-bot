import webbrowser
import click
from warrior_bot.commands.help import goHelpCommand, showHelp


@click.command(cls=goHelpCommand)
@click.argument("resource", required=False)
@click.pass_context
def go(ctx, resource):
    showHelp(ctx, resource)
    click.echo("Executing go command")

    if resource == "academica":
        click.echo("Taking user to WSU Academica site!")
        webbrowser.open("http://academica.aws.wayne.edu/", new=1, autoraise=True)
    elif resource == "library":
        click.echo("Taking user to WSU Library site!")
        webbrowser.open("https://library.wayne.edu/", new=1, autoraise=True)
    elif resource == "bookstore":
        click.echo("Taking user to WSU Bookstore site!")
    else:
        click.echo("invalid command")

