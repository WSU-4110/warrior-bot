import webbrowser
import click
from warrior_bot.commands.help import showHelp


class URL_Command:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def execute(self):
        click.echo("Executing go command.")
        webbrowser.open(self.url, new=1, autoraise=True)


commands = {
    "academica": URL_Command("WSU Academica", "https://academica.aws.wayne.edu/"),
    "library": URL_Command("WSU Library", "https://library.wayne.edu/"),
    "bookstore": URL_Command("WSU Bookstore", "https://waynestatebookstore.com/"),
}


@click.command()
@click.argument("resource")
def go(resource):
    cmd = commands.get(resource)
    if cmd:
        cmd.execute()
    else:
        click.echo("Invalid command")

class goHelpCommand(click.Command): #Help command information
    def format_help(self, ctx, formatter):
        formatter.write_text("Usage: wb go RESOURCE")
        formatter.write_paragraph()

        formatter.write_text("Go Command: Open a supported WSU website.")
        formatter.write_paragraph()

        formatter.write_text("RESOURCES:")
        formatter.write_text("  academica - Opens your browser to the Academica website")
        formatter.write_text("  library  -  Opens your browser to the WSU Library website")
        formatter.write_text("  bookstore - Opens your browser to the WSU Bookstore website")
        formatter.write_text("  help or --help - Show this message")
        formatter.write_paragraph()

        formatter.write_text("Help Menu:")
        formatter.write_text("  wb help or wb --help")


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
