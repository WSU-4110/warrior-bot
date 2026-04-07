"""Go command implementation."""

import difflib
import webbrowser

import click
from warrior_bot.commands.help import goHelpCommand

class URL_Command:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def execute(self):
        click.echo("Executing go command.")
        try:
            success = webbrowser.open(self.url, new=1, autoraise=True)
            if not success:
                click.echo("ERROR: Could not access local browser.")
        except Exception:
            click.echo("ERROR: Could not access local browser.")


commands = {
    "academica": URL_Command("WSU Academica", "https://academica.aws.wayne.edu/"),
    "library": URL_Command("WSU Library", "https://library.wayne.edu/"),
    "bookstore": URL_Command("WSU Bookstore", "https://waynestatebookstore.com/"),
    "degreeworks": URL_Command("WSU Degree Works", "https://degreeworks.wayne.edu/"),
}


@click.command(cls=goHelpCommand)
@click.argument("resource", required=False)
@click.pass_context
def go(ctx, resource):
    # If no argument OR help requested → show custom help
    if resource is None or resource.lower() == "help":
        click.echo(ctx.get_help())
        return

    resource = resource.lower()
    cmd = commands.get(resource)

    if cmd:
        cmd.execute()
    else:
        matches = difflib.get_close_matches(resource, commands.keys(), n=1)
        if matches:
            click.echo(f"Invalid resource -- did you mean '{matches[0]}'?")
        else:
            click.echo("Invalid resource.")
            click.echo("Available resources: " + ", ".join(commands.keys()))
