"""Go command implementation."""

import webbrowser
import click
import difflib

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
    "degreeworks": URL_Command("WSU Degree Works", "https://degreeworks.wayne.edu/")
}


@click.command()
@click.argument("resource")
def go(resource):
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
